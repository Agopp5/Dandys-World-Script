"""Render the twelve AERSP 309 orbital-mechanics videos at 1080p30.

    python render.py                  # all lessons -> output/part<N>_<name>_1080p30.mp4
    python render.py --only 3 5       # just parts 3 and 5
    python render.py --preview        # quick 480p15 build
    python render.py --resume         # skip scenes that are already rendered
"""
import argparse
import concurrent.futures as cf
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LESSONS = {
    1: ("O1Concept", "keplers_laws"),
    2: ("O2Concept", "inverse_square_and_two_body"),
    3: ("O3Concept", "constants_of_motion"),
    4: ("O4Concept", "orbit_equation_and_conics"),
    5: ("O5Concept", "ellipse_energy_period"),
    6: ("O6Concept", "velocity_on_the_orbit"),
    7: ("O7Concept", "parabolas_and_hyperbolas"),
    8: ("O8Examples", "examples_closed_orbits"),
    9: ("O9Examples", "examples_escape_trajectories"),
    10: ("O10Problem", "hw3_p1_velocity_frame"),
    11: ("O11Problem", "hw3_p2_keplers_equation"),
    12: ("O12Problem", "hw3_p4_orbital_elements"),
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
    ap.add_argument("--resume", action="store_true", help="skip scenes that already have a rendered video")
    args = ap.parse_args()
    res, fps, qdir = ("854,480", 15, "480p15") if args.preview else ("1920,1080", 30, "1080p30")
    nums = args.only or sorted(LESSONS)
    jobs = [(f"o{n}", LESSONS[n][0]) for n in nums]
    if args.resume:
        jobs = [(m, s) for m, s in jobs
                if not os.path.exists(os.path.join(HERE, "media", "videos", m, qdir, f"{s}.mp4"))]

    # compile all LaTeX serially first so parallel renders don't race on the cache
    for n in sorted({int(m[1:]) for m, _ in jobs}):
        subprocess.call(["manim", "render", "--disable_caching", "-ql", "--dry_run", f"o{n}.py", LESSONS[n][0]],
                        cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with cf.ProcessPoolExecutor(args.jobs) as ex:
        for f in cf.as_completed([ex.submit(render, m, s, res, fps, qdir) for m, s in jobs]):
            scene, dt = f.result()
            print(f"  rendered {scene:12s} in {dt / 60:4.1f} min", flush=True)

    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    for n in nums:
        parts = [os.path.join(HERE, "media", "videos", f"o{n}", qdir, f"{LESSONS[n][0]}.mp4")]
        missing = [p for p in parts if not os.path.exists(p)]
        if missing:
            sys.exit(f"missing: {missing}")
        out = os.path.join(HERE, "output", f"part{n}_{LESSONS[n][1]}_{qdir}.mp4")
        stitch(parts, out)
        print(f"done: {out}", flush=True)


if __name__ == "__main__":
    main()
