# AERSP 309 Kinematics: A Slow, Step-by-Step Lesson Series

Six short videos (1080p30, about 7–9 minutes each), one concept per video. Each video first
explains the concept slowly, with every algebra step on screen and a short grey note beside
each line saying *why* that step is allowed, and then works examples. The examples follow
the HW1/HW2 problem types, but with **new numbers**.

| # | Video | Concept | Worked examples |
|---|---|---|---|
| 1 | `lesson1_vectors_and_frames` | dot & cross product as pictures, frames, why components are dot products, $\tilde a$ matrix | length/angle of a vector; dot and cross with checks; same arrow in two frames |
| 2 | `lesson2_direction_cosine_matrices` | building $C_{\mathcal{BN}}$ entry by entry, deriving $r_{(\mathcal B)} = C_{\mathcal{BN}} r_{(\mathcal N)}$, $CC^T = I$, $\det C = +1$, 3 DOF | rotate a vector by 30°; rebuild a DCM from missing entries (HW1 P1 style); LVLH frame from $\vec r,\vec v$ (HW1 P3 style); ECI→ECEF (HW1 P4 style) |
| 3 | `lesson3_euler_angles` | deriving $C_1, C_2, C_3$ (and $C_2$'s sign), chaining, multiplying out 3-2-1 row by row, angles from a DCM, gimbal lock | angles → DCM → angles; ground-station dish pointing: $C_{\mathcal{TN}}$, elevation, azimuth (HW1 P5 style) |
| 4 | `lesson4_angular_velocity` | $\vec\omega$, ${}^{\mathcal N}\tfrac{d}{dt}\hat b = \vec\omega\times\hat b$ shown two ways, adding rates, 3-2-1 rates → $\omega_{(\mathcal B)}$ with every substitution, the $1/\cos\theta$ singularity | Earth rotation and launch-site speeds (HW1 P7 style); Euler rates → $\vec\omega$ (HW2 P6 style) |
| 5 | `lesson5_transport_theorem` | why derivatives depend on the observer; the derivation line by line; a 5-step recipe | point on a disk; telescoping arm, checked the hard way (HW1 P6 style); cylindrical coordinates |
| 6 | `lesson6_acceleration` | the transport theorem applied twice; where the "2" in Coriolis comes from; each term's meaning; Coriolis puck | telescoping-arm acceleration; polar coordinates → Kepler's 2nd law and conic orbits |

## Rebuilding

From `astronautics_video/`:

```bash
export OPENROUTER_API_KEY=sk-or-...        # never commit this
python tts.py --project lesson             # narration -> lesson/audio (only changed lines are re-voiced)
cd lesson && python render.py              # -> lesson/output/lesson<N>_*_1080p30.mp4
python render.py --only 3                  # re-render one lesson
python render.py --preview                 # quick 480p check
```

The narration lives in `narration.py`. Every animation is timed to the clip lengths in
`audio/manifest.json`, so you can edit a sentence, re-run `tts.py`, and re-render.
