#!/usr/bin/env python3
"""Generate prebuilt Mandarin audio for one HSK vocabulary level.

The script is deliberately separate from the static web app. It loads Qwen3-TTS
once, resumes around existing MP3 files, and writes a small manifest consumed by
the browser. Use --dry-run to validate the dataset and planned paths without
installing the model runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
DEFAULT_WORD_INSTRUCT = "请用清晰、自然、标准的普通话读出这个词，发音准确。"
DEFAULT_EXAMPLE_INSTRUCT = ""
DEFAULT_EXAMPLE_TEMPO = 1.0
EXAMPLE_PAUSE_FILTER = "silenceremove=stop_periods=-1:stop_duration=0.08:stop_threshold=-45dB:stop_silence=0.03"


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def visible_text(value: Any) -> str:
    parser = _TextExtractor()
    parser.feed(html.unescape(str(value or "")))
    parser.close()
    return "".join(parser.parts).strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", default="hsk1", choices=[f"hsk{i}" for i in range(1, 7)])
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--revision", default="main", help="Model revision or commit hash")
    parser.add_argument("--speaker", default="Serena")
    parser.add_argument("--instruct", help="Override the instruction for both clip kinds")
    parser.add_argument("--word-instruct", default=DEFAULT_WORD_INSTRUCT)
    parser.add_argument("--example-instruct", default=DEFAULT_EXAMPLE_INSTRUCT)
    parser.add_argument("--device", default="auto", help="auto, cuda:0, mps, or cpu")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--bitrate", default="64k")
    parser.add_argument("--word-tempo", type=float, default=1.0)
    parser.add_argument("--example-tempo", type=float, default=DEFAULT_EXAMPLE_TEMPO)
    parser.add_argument("--compact-example-pauses", action="store_true")
    parser.add_argument(
        "--pinyin-guide",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Guide Qwen with the pinyin stored in the vocabulary database",
    )
    parser.add_argument("--skip-manifest", action="store_true", help="Do not publish generated clips to the web manifest")
    parser.add_argument("--seed", type=int, default=20260802)
    parser.add_argument("--limit", type=int, help="Only plan/generate the first N vocabulary rows")
    parser.add_argument("--start-id", type=int, help="Skip rows whose numeric id is lower than this")
    parser.add_argument("--ids", help="Comma-separated vocabulary ids to generate")
    parser.add_argument("--kind", choices=["both", "word", "example"], default="both")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--flash-attention", action="store_true")
    parser.add_argument(
        "--deterministic",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Disable sampling for steadier output (default: disabled)",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_rows(level: str, start_id: int | None, limit: int | None) -> list[dict[str, Any]]:
    source = REPO_ROOT / "database" / "vocabs" / f"{level}_vocabularies.json"
    with source.open(encoding="utf-8") as handle:
        rows = json.load(handle)
    if not isinstance(rows, list):
        raise ValueError(f"Expected a JSON array in {source}")

    normalized: list[dict[str, Any]] = []
    for row in rows:
        try:
            word_id = int(row["id"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid vocabulary id: {row!r}") from exc
        if start_id is not None and word_id < start_id:
            continue
        hanzi = visible_text(row.get("hanzi"))
        pinyin = visible_text(row.get("pinyin"))
        example = visible_text(row.get("example_zh"))
        example_pinyin = visible_text(row.get("expected_pinyin"))
        if not hanzi or not pinyin or not example or not example_pinyin:
            raise ValueError(
                f"Vocabulary id {word_id} has empty Mandarin text, pinyin, or expected_pinyin"
            )
        normalized.append({
            "id": word_id,
            "word": hanzi,
            "word_pinyin": pinyin,
            "example": example,
            "example_pinyin": example_pinyin,
        })

    normalized.sort(key=lambda row: row["id"])
    return normalized[:limit] if limit is not None else normalized


def output_path(level: str, word_id: int, kind: str) -> Path:
    folder = "words" if kind == "word" else "examples"
    return REPO_ROOT / "database" / "prebuilt_audio" / level / folder / f"{word_id:04d}.mp3"


def build_tasks(rows: list[dict[str, Any]], level: str, kind: str) -> list[dict[str, Any]]:
    kinds = ["word", "example"] if kind == "both" else [kind]
    return [
        {
            "id": row["id"],
            "kind": audio_kind,
            "text": row[audio_kind],
            "pinyin": row[f"{audio_kind}_pinyin"],
            "output": output_path(level, row["id"], audio_kind),
        }
        for row in rows
        for audio_kind in kinds
    ]


def load_generation_overrides(level: str) -> dict[str, Any]:
    path = REPO_ROOT / "database" / "prebuilt_audio" / level / "generation_overrides.json"
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8") as handle:
        overrides = json.load(handle)
    if not isinstance(overrides, dict):
        raise ValueError(f"Expected an object in {path}")
    return overrides


def apply_generation_overrides(
    tasks: list[dict[str, Any]],
    overrides: dict[str, Any],
) -> None:
    allowed = {
        "instruct", "synthesis_text", "synthesis_segments", "segment_pauses_ms",
        "tempo", "target_duration", "compact_pauses",
    }
    for task in tasks:
        item = overrides.get(str(task["id"]), {})
        override = item.get(task["kind"], {}) if isinstance(item, dict) else {}
        if not isinstance(override, dict):
            raise ValueError(f"Invalid override for {task['id']}/{task['kind']}")
        unknown = set(override) - allowed
        if unknown:
            raise ValueError(f"Unknown override keys for {task['id']}/{task['kind']}: {sorted(unknown)}")
        if "tempo" in override and not 0.5 <= float(override["tempo"]) <= 2:
            raise ValueError(f"Invalid tempo for {task['id']}/{task['kind']}")
        if "target_duration" in override and not 0.4 <= float(override["target_duration"]) <= 10:
            raise ValueError(f"Invalid target duration for {task['id']}/{task['kind']}")
        task.update(override)


def resolve_device(torch: Any, requested: str) -> str:
    if requested != "auto":
        return requested
    if torch.cuda.is_available():
        return "cuda:0"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load_model(args: argparse.Namespace) -> tuple[Any, Any, str]:
    try:
        import torch
        from qwen_tts import Qwen3TTSModel
    except ImportError as exc:
        raise RuntimeError(
            "Missing Qwen runtime. Create the Python 3.12 environment described "
            "in tools/TTS_TESTING.md first."
        ) from exc

    device = resolve_device(torch, args.device)
    dtype = torch.bfloat16 if device.startswith("cuda") else torch.float32
    model_options: dict[str, Any] = {
        "device_map": device,
        "dtype": dtype,
        "revision": args.revision,
    }
    if args.flash_attention:
        if not device.startswith("cuda"):
            raise ValueError("--flash-attention requires a CUDA device")
        model_options["attn_implementation"] = "flash_attention_2"

    print(f"Loading {args.model} ({args.revision}) on {device}...", flush=True)
    model = Qwen3TTSModel.from_pretrained(args.model, **model_options)
    return model, torch, device


def encode_mp3(
    wav_path: Path,
    destination: Path,
    bitrate: str,
    tempo: float = 1.0,
    compact_pauses: bool = False,
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".mp3.tmp")
    audio_filters = []
    if compact_pauses:
        audio_filters.append(EXAMPLE_PAUSE_FILTER)
    audio_filters.extend([f"atempo={tempo}", "loudnorm=I=-18:TP=-2:LRA=7"])
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(wav_path),
        "-af", ",".join(audio_filters),
        "-ar", "24000", "-ac", "1", "-codec:a", "libmp3lame",
        "-b:a", bitrate, "-map_metadata", "-1", "-f", "mp3", str(temporary),
    ]
    subprocess.run(command, check=True)
    if temporary.stat().st_size < 256:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"Encoded audio is unexpectedly small: {destination}")
    temporary.replace(destination)


def audio_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def expected_syllables(task: dict[str, Any]) -> int:
    if task["kind"] == "word":
        return max(1, sum("\u3400" <= character <= "\u9fff" for character in task["text"]))
    return max(1, sum(any(character.isalpha() for character in token) for token in task["pinyin"].split()))


def validate_duration(task: dict[str, Any]) -> float:
    duration = audio_duration(task["output"])
    syllables = expected_syllables(task)
    minimum = max(0.25, syllables * 0.18)
    maximum = max(2.0, syllables * 0.9 + 1.0)
    if not minimum <= duration <= maximum:
        task["output"].unlink(missing_ok=True)
        raise RuntimeError(
            f"Implausible duration {duration:.2f}s for {syllables} syllables "
            f"({minimum:.2f}s..{maximum:.2f}s): {task['text']}"
        )
    return duration


def generate_batch(
    model: Any,
    tasks: list[dict[str, Any]],
    args: argparse.Namespace,
    temp_dir: Path,
) -> None:
    segmented = [task for task in tasks if "synthesis_segments" in task]
    if segmented:
        if len(tasks) != 1:
            raise RuntimeError("Segmented synthesis must be generated one clip at a time")
        task = segmented[0]
        segments = task["synthesis_segments"]
        if not isinstance(segments, list) or not segments or not all(
            isinstance(segment, dict) and segment.get("text") and segment.get("pinyin")
            for segment in segments
        ):
            raise ValueError(f"Invalid synthesis_segments for {task['id']}/{task['kind']}")
        segment_options: dict[str, Any] = {
            "text": [segment["text"] for segment in segments],
            "language": ["Chinese"] * len(segments),
            "speaker": [args.speaker] * len(segments),
            "instruct": [
                f"只读“{segment['text']}”，严格发音为“{segment['pinyin']}”，不要添加其他音。"
                for segment in segments
            ],
        }
        if args.deterministic:
            segment_options["do_sample"] = False
            segment_options["subtalker_dosample"] = False
        segment_wavs, sample_rate = model.generate_custom_voice(**segment_options)
        if len(segment_wavs) != len(segments):
            raise RuntimeError(f"Qwen returned {len(segment_wavs)} segments for {len(segments)} inputs")
        pauses = task.get("segment_pauses_ms", [20] * (len(segments) - 1))
        if not isinstance(pauses, list) or len(pauses) != len(segments) - 1:
            raise ValueError(f"Invalid segment_pauses_ms for {task['id']}/{task['kind']}")
        import numpy as np
        pieces = []
        for index, wav in enumerate(segment_wavs):
            pieces.append(wav)
            if index < len(pauses):
                pieces.append(np.zeros(round(sample_rate * float(pauses[index]) / 1000), dtype=wav.dtype))
        wav = np.concatenate(pieces)
        import soundfile as sf
        wav_path = temp_dir / f"segmented-{task['id']}-{task['kind']}.wav"
        sf.write(wav_path, wav, sample_rate)
        raw_duration = len(wav) / sample_rate
        tempo = raw_duration / float(task["target_duration"]) if "target_duration" in task else task.get("tempo", 1.0)
        if not 0.5 <= tempo <= 2:
            raise RuntimeError(f"Required segmented tempo {tempo:.2f} is outside 0.5..2: {task['text']}")
        encode_mp3(wav_path, task["output"], args.bitrate, tempo, task.get("compact_pauses", False))
        duration = validate_duration(task)
        print(f"generated {task['output'].relative_to(REPO_ROOT)} ({duration:.2f}s, segmented)", flush=True)
        return

    options: dict[str, Any] = {
        "text": [task.get("synthesis_text", task["text"]) for task in tasks],
        "language": ["Chinese"] * len(tasks),
        "speaker": [args.speaker] * len(tasks),
    }
    instructions = []
    for task in tasks:
        if "instruct" in task:
            instruction = task["instruct"]
        elif args.instruct is not None:
            instruction = args.instruct
        elif args.pinyin_guide and task["kind"] == "word":
            instruction = (
                f"请自然清晰地读出“{task['text']}”，严格按拼音“{task['pinyin']}”发音，"
                "不要添加其他内容。"
            )
        elif args.pinyin_guide:
            instruction = (
                f"请自然连贯地读完整句，严格按照拼音发音：{task['pinyin']}。"
                "不要添加停顿。"
            )
        else:
            instruction = args.word_instruct if task["kind"] == "word" else args.example_instruct
        instructions.append(instruction)
    if any(instructions):
        options["instruct"] = instructions
    if args.deterministic:
        options["do_sample"] = False
        options["subtalker_dosample"] = False

    wavs, sample_rate = model.generate_custom_voice(**options)
    if len(wavs) != len(tasks):
        raise RuntimeError(f"Qwen returned {len(wavs)} clips for {len(tasks)} inputs")

    import soundfile as sf

    for index, (task, wav) in enumerate(zip(tasks, wavs, strict=True)):
        wav_path = temp_dir / f"batch-{task['id']}-{task['kind']}-{index}.wav"
        sf.write(wav_path, wav, sample_rate)
        raw_duration = len(wav) / sample_rate
        if "target_duration" in task:
            tempo = raw_duration / float(task["target_duration"])
            if not 0.5 <= tempo <= 2:
                raise RuntimeError(
                    f"Required tempo {tempo:.2f} is outside 0.5..2 for target duration "
                    f"{task['target_duration']}s: {task['text']}"
                )
        else:
            tempo = task.get(
                "tempo",
                args.word_tempo if task["kind"] == "word" else args.example_tempo,
            )
        encode_mp3(
            wav_path,
            task["output"],
            args.bitrate,
            tempo,
            compact_pauses=task.get(
                "compact_pauses",
                args.compact_example_pauses and task["kind"] == "example",
            ),
        )
        duration = validate_duration(task)
        print(
            f"generated {task['output'].relative_to(REPO_ROOT)} ({duration:.2f}s)",
            flush=True,
        )


def write_manifest(rows: list[dict[str, Any]], args: argparse.Namespace, device: str) -> Path:
    manifest_path = REPO_ROOT / "database" / "prebuilt_audio" / args.level / "manifest.json"
    items: dict[str, dict[str, str]] = {}
    for row in rows:
        clips: dict[str, str] = {}
        for kind in ("word", "example"):
            path = output_path(args.level, row["id"], kind)
            if path.is_file() and path.stat().st_size >= 256:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
                clips[kind] = f"{path.relative_to(REPO_ROOT).as_posix()}?v={digest}"
        if clips:
            items[str(row["id"])] = clips

    manifest = {
        "version": 1,
        "level": args.level,
        "model": args.model,
        "revision": args.revision,
        "speaker": args.speaker,
        "deterministic": args.deterministic,
        "pinyin_guide": args.pinyin_guide,
        "instructions": {
            "word": args.instruct if args.instruct is not None else (
                "dynamic from word pinyin" if args.pinyin_guide else args.word_instruct
            ),
            "example": args.instruct if args.instruct is not None else (
                "dynamic from expected_pinyin" if args.pinyin_guide else args.example_instruct
            ),
        },
        "postprocess_tempo": {
            "word": args.word_tempo,
            "example": args.example_tempo,
        },
        "example_pause_compaction": {
            "enabled": args.compact_example_pauses,
            "trigger_seconds": 0.08,
            "retained_seconds": 0.03,
        },
        "generation_overrides": load_generation_overrides(args.level),
        "device_used_for_generation": device,
        "items": items,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = manifest_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(manifest_path)
    return manifest_path


def main() -> int:
    args = parse_args()
    if args.batch_size < 1:
        raise ValueError("--batch-size must be at least 1")
    if args.limit is not None and args.limit < 1:
        raise ValueError("--limit must be at least 1")
    if not 0.5 <= args.word_tempo <= 2:
        raise ValueError("--word-tempo must be between 0.5 and 2")
    if not 0.5 <= args.example_tempo <= 2:
        raise ValueError("--example-tempo must be between 0.5 and 2")
    if shutil.which("ffmpeg") is None and not args.dry_run:
        raise RuntimeError("ffmpeg is required to encode browser-friendly MP3 files")

    rows = load_rows(args.level, args.start_id, args.limit)
    if args.ids:
        selected_ids = {int(value.strip()) for value in args.ids.split(",") if value.strip()}
        rows = [row for row in rows if row["id"] in selected_ids]
        missing_ids = selected_ids - {row["id"] for row in rows}
        if missing_ids:
            raise ValueError(f"Vocabulary ids not found after filtering: {sorted(missing_ids)}")
    tasks = build_tasks(rows, args.level, args.kind)
    generation_overrides = load_generation_overrides(args.level)
    apply_generation_overrides(tasks, generation_overrides)
    pending = [task for task in tasks if args.overwrite or not task["output"].is_file()]
    print(
        f"{args.level}: {len(rows)} rows, {len(tasks)} planned clips, "
        f"{len(pending)} pending clips"
    )
    if args.dry_run:
        for task in pending[:10]:
            print(f"  {task['kind']:7} {task['id']:4}: {task['text']} -> {task['output'].relative_to(REPO_ROOT)}")
        if len(pending) > 10:
            print(f"  ... and {len(pending) - 10} more")
        return 0
    if not pending:
        if args.skip_manifest:
            print("Nothing to generate; manifest left unchanged.")
            return 0
        manifest = write_manifest(load_rows(args.level, None, None), args, "not-loaded")
        print(f"Nothing to generate; refreshed {manifest.relative_to(REPO_ROOT)}")
        return 0

    random.seed(args.seed)
    model, torch, device = load_model(args)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)

    failures: list[tuple[dict[str, Any], str]] = []
    with tempfile.TemporaryDirectory(prefix="hsk-tts-") as temp_name:
        temp_dir = Path(temp_name)
        for offset in range(0, len(pending), args.batch_size):
            batch = pending[offset:offset + args.batch_size]
            try:
                generate_batch(model, batch, args, temp_dir)
            except Exception as batch_error:
                print(f"Batch failed ({batch_error}); retrying each clip...", file=sys.stderr)
                for task in batch:
                    try:
                        generate_batch(model, [task], args, temp_dir)
                    except Exception as item_error:
                        failures.append((task, str(item_error)))
                        print(
                            f"FAILED {task['kind']} {task['id']}: {item_error}",
                            file=sys.stderr,
                            flush=True,
                        )

    if args.skip_manifest:
        print("Manifest left unchanged (--skip-manifest).")
    else:
        manifest = write_manifest(load_rows(args.level, None, None), args, device)
        print(f"Wrote {manifest.relative_to(REPO_ROOT)}")
    if failures:
        print(f"Completed with {len(failures)} failed clips. Re-run the same command to resume.", file=sys.stderr)
        return 1
    print(f"Completed {len(pending)} clips successfully.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted. Existing MP3 files are kept; re-run to resume.", file=sys.stderr)
        raise SystemExit(130)
