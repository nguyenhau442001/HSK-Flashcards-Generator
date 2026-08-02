#!/usr/bin/env python3
"""Generate HSK MP3 files with CosyVoice3 and optional pinyin inpainting."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any

from generate_hsk_audio import REPO_ROOT, audio_duration, load_rows, output_path


DEFAULT_MODEL_ID = "FunAudioLLM/Fun-CosyVoice3-0.5B-2512"
SILENCE_FILTER = (
    "silenceremove=start_periods=1:start_duration=0.03:start_threshold=-45dB:"
    "stop_periods=-1:stop_duration=0.08:stop_threshold=-45dB:stop_silence=0.03,"
    "loudnorm=I=-18:TP=-2:LRA=7"
)


def encode_mp3(source: Path, destination: Path, bitrate: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".mp3.tmp")
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
        "-af", SILENCE_FILTER, "-ar", "24000", "-ac", "1", "-codec:a", "libmp3lame",
        "-b:a", bitrate, "-map_metadata", "-1", "-f", "mp3", str(temporary),
    ], check=True)
    if temporary.stat().st_size < 256:
        raise RuntimeError(f"Encoded audio is unexpectedly small: {destination}")
    temporary.replace(destination)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", default="hsk1", choices=[f"hsk{i}" for i in range(1, 7)])
    parser.add_argument("--cosyvoice-root", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--prompt-audio", type=Path, required=True)
    parser.add_argument("--prompt-text", required=True)
    parser.add_argument("--kind", choices=["both", "word", "example"], default="both")
    parser.add_argument("--ids")
    parser.add_argument("--start-id", type=int)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--bitrate", default="64k")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--skip-manifest", action="store_true")
    parser.add_argument("--seed", type=int, default=20260802)
    return parser.parse_args()


def load_overrides(level: str) -> dict[str, Any]:
    path = REPO_ROOT / "database" / "prebuilt_audio" / level / "cosyvoice_overrides.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def task_output(args: argparse.Namespace, word_id: int, kind: str) -> Path:
    if args.output_root is None:
        return output_path(args.level, word_id, kind)
    folder = "words" if kind == "word" else "examples"
    return args.output_root / folder / f"{word_id:04d}.mp3"


def write_manifest(rows: list[dict[str, Any]], args: argparse.Namespace) -> None:
    path = REPO_ROOT / "database" / "prebuilt_audio" / args.level / "manifest.json"
    items: dict[str, dict[str, str]] = {}
    for row in rows:
        clips: dict[str, str] = {}
        for kind in ("word", "example"):
            audio = output_path(args.level, row["id"], kind)
            if audio.is_file() and audio.stat().st_size >= 256:
                digest = hashlib.sha256(audio.read_bytes()).hexdigest()[:12]
                clips[kind] = f"{audio.relative_to(REPO_ROOT).as_posix()}?v={digest}"
        items[str(row["id"])] = clips
    manifest = {
        "version": 1,
        "level": args.level,
        "model": DEFAULT_MODEL_ID,
        "engine": "CosyVoice3",
        "voice": "zero-shot",
        "prompt_text": args.prompt_text,
        "speed": args.speed,
        "pronunciation_overrides": load_overrides(args.level),
        "items": items,
    }
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    args = parse_args()
    if not 0.5 <= args.speed <= 2:
        raise ValueError("--speed must be between 0.5 and 2")
    rows = load_rows(args.level, None, args.limit)
    if args.start_id is not None:
        rows = [row for row in rows if row["id"] >= args.start_id]
    if args.ids:
        selected = {int(value.strip()) for value in args.ids.split(",") if value.strip()}
        rows = [row for row in rows if row["id"] in selected]
        missing = selected - {row["id"] for row in rows}
        if missing:
            raise ValueError(f"Unknown ids: {sorted(missing)}")
    kinds = ("word", "example") if args.kind == "both" else (args.kind,)
    overrides = load_overrides(args.level)
    tasks = []
    for row in rows:
        for kind in kinds:
            override = overrides.get(str(row["id"]), {}).get(kind, {})
            tasks.append({
                "id": row["id"],
                "kind": kind,
                "text": override.get("text", row[kind]),
                "syllables": max(1, sum("\u3400" <= char <= "\u9fff" for char in row[kind])),
                "output": task_output(args, row["id"], kind),
            })
    pending = [task for task in tasks if args.overwrite or not task["output"].is_file()]
    print(f"{args.level}: {len(tasks)} planned clips, {len(pending)} pending clips", flush=True)
    if not pending:
        if not args.skip_manifest and args.output_root is None:
            write_manifest(load_rows(args.level, None, None), args)
        return 0

    sys.path.insert(0, str(args.cosyvoice_root))
    sys.path.insert(0, str(args.cosyvoice_root / "third_party" / "Matcha-TTS"))
    import torch
    import torchaudio
    from cosyvoice.cli.cosyvoice import AutoModel

    torch.manual_seed(args.seed)
    model = AutoModel(model_dir=str(args.model_dir))
    with tempfile.TemporaryDirectory(prefix="hsk-cosyvoice-") as temp_name:
        temp_dir = Path(temp_name)
        prompt_wav = temp_dir / "prompt.wav"
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(args.prompt_audio),
            "-ar", "16000", "-ac", "1", str(prompt_wav),
        ], check=True)
        prompt = f"You are a helpful assistant.<|endofprompt|>{args.prompt_text}"
        for index, task in enumerate(pending, 1):
            last_error: Exception | None = None
            for attempt in range(3):
                try:
                    torch.manual_seed(args.seed + task["id"] * 10 + attempt)
                    if task["kind"] == "word":
                        chunks = list(model.inference_cross_lingual(
                            f"You are a helpful assistant.<|endofprompt|>{task['text']}",
                            str(prompt_wav), stream=False, speed=args.speed,
                        ))
                    else:
                        chunks = list(model.inference_zero_shot(
                            task["text"], prompt, str(prompt_wav), stream=False, speed=args.speed,
                        ))
                    if not chunks:
                        raise RuntimeError("CosyVoice returned no audio")
                    speech = torch.cat([chunk["tts_speech"] for chunk in chunks], dim=1)
                    duration = speech.shape[1] / model.sample_rate
                    if duration < 0.3:
                        raise RuntimeError(f"raw audio is only {duration:.2f}s")
                    wav = temp_dir / f"{task['id']:04d}-{task['kind']}.wav"
                    torchaudio.save(str(wav), speech.cpu(), model.sample_rate)
                    encode_mp3(wav, task["output"], args.bitrate)
                    encoded_duration = audio_duration(task["output"])
                    minimum = 0.2 if task["kind"] == "word" else task["syllables"] * 0.12
                    maximum = 2.0 if task["kind"] == "word" else task["syllables"] * 0.5 + 0.8
                    if not minimum <= encoded_duration <= maximum:
                        task["output"].unlink(missing_ok=True)
                        raise RuntimeError(
                            f"encoded duration {encoded_duration:.2f}s outside "
                            f"{minimum:.2f}..{maximum:.2f}s"
                        )
                    break
                except Exception as error:
                    last_error = error
                    print(
                        f"retry {attempt + 1}/3 for {task['id']}/{task['kind']}: {error}",
                        file=sys.stderr,
                        flush=True,
                    )
            else:
                raise RuntimeError(
                    f"Failed {task['id']}/{task['kind']} after 3 attempts: {last_error}"
                )
            print(f"[{index}/{len(pending)}] generated {task['output']}", flush=True)

    if not args.skip_manifest and args.output_root is None:
        write_manifest(load_rows(args.level, None, None), args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
