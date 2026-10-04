"""Render the six lesson videos at 1080p30.

    python render.py                  # all lessons -> output/lesson<N>_<name>_1080p30.mp4
    python render.py --only 3 5       # just lessons 3 and 5
    python render.py --preview        # quick 480p15 build
"""
import argparse
import concurrent.futures as cf
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LESSONS = {
    1: "vectors_and_frames",
    2: "direction_cosine_matrices",
    3: "euler_angles",
    4: "angular_velocity",
    5: "transport_theorem",
    6: "acceleration",
}


def render(module, scene, res, fps, qdir):
    t0 = time.time()
    log = os.path.join(HERE, "media", f"{scene}.log")
    os.makedirs(os.path.dirname(log), exist_ok=True)
    with open(log, "w") as f:
        rc = subprocess.call(["manim", "render", "--disable_caching", "-r", res, "--fps", str(fps),
                              f"{module}.py", scene], cwd=HERE, stdout=f, stderr=subprocess.STDOUT)
    out = os.path.join(HERE, "media", "videos", module, qdir, f"{scene}.mp4")
    if rc != 0 or not os.path.exists(out):
        raise RuntimeError(f"{scene} failed; see {log}")
    return scene, time.time() - t0


def stitch(paths, out):
    inputs = []
    for p in paths:
        inputs += ["-i", p]
    n = len(paths)
    graph = "".join(f"[{i}:v][{i}:a]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a0];" \
            "[a0]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]"
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
                           "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-pix_fmt", "yuv420p", "-r", "30",
                           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", type=int)
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 2)
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()
    res, fps, qdir = ("854,480", 15, "480p15") if args.preview else ("1920,1080", 30, "1080p30")
    nums = args.only or sorted(LESSONS)
    jobs = [(f"v{n}", f"V{n}{part}") for n in nums for part in ("Concept", "Examples")]

    # compile all LaTeX serially first so parallel renders don't race on the cache
    for n in nums:
        subprocess.call(["manim", "render", "--disable_caching", "-ql", "--dry_run", f"v{n}.py",
                         f"V{n}Concept", f"V{n}Examples"], cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with cf.ProcessPoolExecutor(args.jobs) as ex:
        for f in cf.as_completed([ex.submit(render, m, s, res, fps, qdir) for m, s in jobs]):
            scene, dt = f.result()
            print(f"  rendered {scene:12s} in {dt / 60:4.1f} min", flush=True)

    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    for n in nums:
        parts = [os.path.join(HERE, "media", "videos", f"v{n}", qdir, f"V{n}{p}.mp4") for p in ("Concept", "Examples")]
        missing = [p for p in parts if not os.path.exists(p)]
        if missing:
            sys.exit(f"missing: {missing}")
        out = os.path.join(HERE, "output", f"lesson{n}_{LESSONS[n]}_{qdir}.mp4")
        stitch(parts, out)
        print(f"done: {out}", flush=True)


if __name__ == "__main__":
    main()
