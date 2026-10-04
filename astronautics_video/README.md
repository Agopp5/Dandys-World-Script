# Same Arrow, Different Observers

A 3Blue1Brown-style explainer (≈15 min, 1080p30) covering the AERSP 309 kinematics unit:
reference frames, direction cosine matrices, Euler angles, angular velocity, the transport
theorem, and acceleration (relative, tangential, Coriolis, centripetal). Worked examples come
from the lecture notes and HW2 (Endurance docking, the UFO over State College, the
merry-go-round, polar coordinates → Kepler).

Animation: [Manim Community](https://www.manim.community/) · Narration: `google/gemini-3.8-flash-tts`
through OpenRouter (voice *Achird*).

## Chapters

| Scene | Content |
|---|---|
| `Intro` | The hovering UFO: 0 m/s or 356 m/s? |
| `Frames` | Vectors as arrows, frames, components as shadows, `r_(N)` vs `r_(B)` |
| `DCM` | Building `C_BN` from dot products, orthogonality, `r_(B) = C_BN r_(N)`, 3 DOF, Endurance example |
| `Euler` | 3-2-1 yaw/pitch/roll, `C_BA = C1(φ)C2(θ)C3(ψ)`, the 12 sets, extracting angles, gimbal lock |
| `AngularVelocity` | `ω^{B/N}`, `ᴺd/dt b̂ = ω × b̂`, adding rates through the chain, kinematic ODE and its `1/cos θ` |
| `Transport` | Derivation of `ᴺd/dt r = ᴮd/dt r + ω × r`, two observers of a disk, cylindrical coordinates |
| `UFO` | HW2 P1: inertial position, velocity, acceleration of the UFO |
| `Acceleration` | Five-term acceleration, frictionless puck, merry-go-round, polar coordinates → Kepler |
| `Outro` | Recap |

## Rebuilding

```bash
pip install manim            # also needs LaTeX (texlive) and ffmpeg
export OPENROUTER_API_KEY=sk-or-...   # never commit this
python tts.py                # narration -> audio/*.wav (cached by text + voice)
python render.py             # -> output/astronautics_kinematics_1080p30.mp4
python render.py --preview   # quick 480p15 check
```

- Edit narration in `narration.py`; `tts.py` only regenerates changed lines, and every scene
  times its animations to the clip lengths in `audio/manifest.json`.
- Change the voice with `python tts.py --voice Puck` (any Gemini TTS voice).
- `proj3d.py` draws the 3D scenes as ordinary 2D shapes through a small perspective camera;
  Manim's surface-based 3D objects were ~1 s/frame with the Cairo renderer.
