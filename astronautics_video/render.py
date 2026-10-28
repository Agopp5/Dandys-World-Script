"""Render every scene at 1080p30 and stitch them into one video.

    python render.py                 # full build -> output/astronautics_kinematics_1080p30.mp4
    python render.py --jobs 2        # fewer parallel renders
    python render.py --only DCM UFO  # re-render some scenes, then re-stitch
    python render.py --preview       # fast 480p15 build for checking timing
"""
import argparse
import concurrent.futures as cf
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SCENES = [
    ("scenes_a", "Intro"),
    ("scenes_a", "Frames"),
    ("scenes_a", "DCM"),
    ("scenes_b", "Euler"),
    ("scenes_b", "AngularVelocity"),
    ("scenes_c", "Transport"),
    ("scenes_c", "UFO"),
    ("scenes_c", "Acceleration"),
    ("scenes_c", "Outro"),
]


def render(module, scene, res, fps, quality_dir):
    t0 = time.time()
    cmd = ["manim", "render", "--disable_caching", "-r", res, "--fps", str(fps),
           f"{module}.py", scene]
    log = os.path.join(HERE, "media", f"{scene}.log")
    os.makedirs(os.path.dirname(log), exist_ok=True)
    with open(log, "w") as f:
        rc = subprocess.call(cmd, cwd=HERE, stdout=f, stderr=subprocess.STDOUT)
    out = os.path.join(HERE, "media", "videos", module, quality_dir, f"{scene}.mp4")
    if rc != 0 or not os.path.exists(out):
        raise RuntimeError(f"{scene} failed; see {log}")
    return scene, out, time.time() - t0


def warm_tex_cache():
    """Compile every LaTeX snippet once, serially, so parallel renders don't race on the cache."""
    cmd = ["manim", "render", "--disable_caching", "-ql", "--dry_run"]
    for module in dict.fromkeys(m for m, _ in SCENES):
        scenes = [s for m, s in SCENES if m == module]
        subprocess.call(cmd + [f"{module}.py", *scenes], cwd=HERE,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def stitch(paths, out):
    inputs = []
    for p in paths:
        inputs += ["-i", p]
    n = len(paths)
    graph = "".join(f"[{i}:v][{i}:a]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a0];" \
            "[a0]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]"
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.check_call(cmd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2)))
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()

    res, fps, qdir = ("854,480", 15, "480p15") if args.preview else ("1920,1080", 30, "1080p30")
    todo = [s for s in SCENES if not args.only or s[1] in args.only]

    print("warming LaTeX cache ...", flush=True)
    warm_tex_cache()
    # longest scenes first so the pool finishes evenly
    order = ["DCM", "Acceleration", "Euler", "Transport", "AngularVelocity", "UFO", "Frames", "Intro", "Outro"]
    todo.sort(key=lambda s: order.index(s[1]))
    with cf.ProcessPoolExecutor(args.jobs) as ex:
        futs = [ex.submit(render, m, s, res, fps, qdir) for m, s in todo]
        for f in cf.as_completed(futs):
            scene, out, dt = f.result()
            print(f"  rendered {scene:16s} in {dt / 60:5.1f} min", flush=True)

    paths = [os.path.join(HERE, "media", "videos", m, qdir, f"{s}.mp4") for m, s in SCENES]
    missing = [p for p in paths if not os.path.exists(p)]
    if missing:
        sys.exit(f"missing scene renders: {missing}")
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    out = os.path.join(HERE, "output", f"astronautics_kinematics_{qdir}.mp4")
    print("stitching ...", flush=True)
    stitch(paths, out)
    print(f"done: {out}")


if __name__ == "__main__":
    main()
