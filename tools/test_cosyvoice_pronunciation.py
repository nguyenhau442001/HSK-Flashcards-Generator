#!/usr/bin/env python3
"""Generate one CosyVoice3 pronunciation-inpainting candidate for manual QA."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cosyvoice-root", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--prompt-wav", type=Path, required=True)
    parser.add_argument("--prompt-text", required=True)
    parser.add_argument("--text", required=True, help="Text may contain CosyVoice pinyin tokens such as [q][ǐ]")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--speed", type=float, default=1.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sys.path.insert(0, str(args.cosyvoice_root))
    sys.path.insert(0, str(args.cosyvoice_root / "third_party" / "Matcha-TTS"))

    import torch
    import torchaudio
    from cosyvoice.cli.cosyvoice import AutoModel

    torch.manual_seed(20260802)
    model = AutoModel(model_dir=str(args.model_dir))
    chunks = list(model.inference_zero_shot(
        args.text,
        f"You are a helpful assistant.<|endofprompt|>{args.prompt_text}",
        str(args.prompt_wav),
        stream=False,
        speed=args.speed,
    ))
    if not chunks:
        raise RuntimeError("CosyVoice returned no audio")
    speech = torch.cat([chunk["tts_speech"] for chunk in chunks], dim=1)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary_wav = args.output.with_suffix(".wav")
    torchaudio.save(str(temporary_wav), speech.cpu(), model.sample_rate)
    print(f"Generated {temporary_wav} at {model.sample_rate} Hz")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
