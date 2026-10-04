"""Generate narration audio with OpenRouter TTS.

Usage:
    export OPENROUTER_API_KEY=sk-or-...
    python tts.py                 # generate missing / changed segments
    python tts.py --voice Puck    # use a different voice (regenerates all)
    python tts.py --only dcm_3    # regenerate specific segments
    python tts.py --project lesson   # voice lesson/narration.py into lesson/audio/

Writes audio/<segment_id>.wav (24 kHz mono) and audio/manifest.json, which
records each clip's duration so the Manim scenes can sync to it.
"""
import argparse
import concurrent.futures as cf
import hashlib
import importlib.util
import json
import os
import sys
import time
import urllib.error
import urllib.request
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://openrouter.ai/api/v1/audio/speech"
MODEL = "google/gemini-3.8-flash-tts"
SAMPLE_RATE = 24000  # Gemini TTS returns raw 16-bit PCM at 24 kHz, mono


def load_project(project):
    """Load <project>/narration.py; audio goes to <project>/audio/."""
    root = os.path.join(HERE, project)
    spec = importlib.util.spec_from_file_location("narration", os.path.join(root, "narration.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, os.path.join(root, "audio")


def fingerprint(text, voice, style):
    return hashlib.sha1(f"{MODEL}|{voice}|{style}|{text}".encode()).hexdigest()


def synthesize(text, voice, key, style, retries=8):
    body = json.dumps({
        "model": MODEL,
        "input": text,
        "voice": voice,
        "instructions": style,
        "response_format": "pcm",
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    })
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = resp.read()
            if len(data) < SAMPLE_RATE:  # under 0.5 s of audio: treat as failure
                raise RuntimeError(f"suspiciously short audio ({len(data)} bytes)")
            return data
        except (urllib.error.URLError, RuntimeError, TimeoutError) as e:
            if attempt == retries:
                raise
            wait = min(60, 2 ** (attempt + 1))
            print(f"  retry in {wait}s: {e}", file=sys.stderr)
            time.sleep(wait)


def write_wav(path, pcm):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm)
    return len(pcm) / 2 / SAMPLE_RATE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="Achird")
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--project", default=".")
    args = ap.parse_args()
    narration, audio_dir = load_project(args.project)
    style = narration.STYLE
    manifest_path = os.path.join(audio_dir, "manifest.json")

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("Set OPENROUTER_API_KEY first.")
    os.makedirs(audio_dir, exist_ok=True)
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}

    todo = []
    for scene, seg_id, text in narration.all_segments():
        fp = fingerprint(text, args.voice, style)
        wav = os.path.join(audio_dir, f"{seg_id}.wav")
        stored = os.path.join(audio_dir, manifest.get(seg_id, {}).get("file", f"{seg_id}.wav"))
        fresh = manifest.get(seg_id, {}).get("fp") == fp and os.path.exists(stored)
        if (args.only and seg_id in args.only) or (not args.only and not fresh):
            todo.append((seg_id, text, fp, wav))

    print(f"{len(todo)} segment(s) to synthesize with voice {args.voice}")

    def job(item):
        seg_id, text, fp, wav = item
        dur = write_wav(wav, synthesize(text, args.voice, key, style))
        return seg_id, {"file": f"{seg_id}.wav", "duration": round(dur, 3), "fp": fp}

    with cf.ThreadPoolExecutor(args.jobs) as ex:
        for fut in cf.as_completed([ex.submit(job, t) for t in todo]):
            seg_id, entry = fut.result()
            manifest[seg_id] = entry
            print(f"  {seg_id}: {entry['duration']:.1f}s")
            json.dump(manifest, open(manifest_path, "w"), indent=1)

    total = sum(v["duration"] for v in manifest.values())
    print(f"Total narration: {total / 60:.1f} min")


if __name__ == "__main__":
    main()
