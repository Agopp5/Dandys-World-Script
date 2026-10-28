# AERSP 309: Orbit Determination (6 videos, 23 min, with a practice guide)

Kluever Ch. 3, from the orbit-determination notes. The point of the series is to make every
orbital element a picture before it becomes a formula. Episodes 1–3 build the six elements
and the rotation matrix $C_{PN}$. Episodes 4–5 work the Molniya example (Example 3.1) in both
directions. Episode 6 covers J2. Every algebra step is on screen, numbers included.

Colors stay fixed for the whole series: $\Omega$ blue, $i$ orange, $\omega$ green, $\theta$ gold,
$\vec h$ purple, $\vec e$ / $\hat p$ / periapsis pink, and $\hat q$ / $\vec n$ lime.

| Ep | Video (`output/`) | Length | What it covers |
|---|---|---|---|
| 1 | `ep1_an_orbits_address` | 2:36 | why r and v are hard to picture; the ECI frame (vernal equinox, why it doesn't spin); state vector vs. the six classical elements |
| 2 | `ep2_placing_the_orbit_in_space` | 3:59 | the three turns: $\Omega$ about $\hat K$, $i$ about the node line (ascending/descending node, prograde/polar/retrograde), $\omega$ about $\hat h$, then $\theta_0$; the Molniya built turn by turn; special cases $u$, $\varpi$, $l$ |
| 3 | `ep3_the_perifocal_frame` | 4:12 | the perifocal frame $\hat p, \hat q, \hat h$; $C_{PN}$ as dot products; $C_{PN} = C_3(\omega)C_1(i)C_3(\Omega)$; multiplying out row 3 and column 3; reading $i$, $\Omega$, $\omega$ back with atan2 |
| 4 | `ep4_from_r_and_v_to_the_elements` | 5:44 | Molniya from $\vec r_0, \vec v_0$: energy → $a$; $\vec h$ and $\vec e$ component by component; building $C_{PN}$; $\Omega$ two ways (matrix and node vector); $\omega$ (atan2 vs. the $e_Z$ check); $\theta_0$ with the $\vec r\cdot\vec v$ sign check |
| 5 | `ep5_going_back` | 2:19 | elements → $\vec r_P, \vec v_P$ in the perifocal frame → $C_{PN}^T$ back to ECI, with the round trip matching the measured $\vec r_0, \vec v_0$ |
| 6 | `ep6_earth_is_not_a_sphere` | 4:22 | the J2 bulge; node drift $\dot\Omega$ (ISS −5.0°/day, sun-synchronous 98.2° at 700 km); $\dot\omega$ and the critical inclination 63.43°, which is why Molniya sits at 63.4°; recap |

Each video has a `.vtt` caption file next to it. All numbers were checked in Python against
the Example 3.1 state vector, and each scene file asserts the numbers it shows.

## Practice guide

`output/practice_guide.pdf` (source `guide.tex`) has eight checkpoints. Each video stops at its
checkpoints with a "Your turn" card; on the study page the video pauses there and shows the problem.

| Checkpoint | Video time | Task |
|---|---|---|
| 2.1 | Ep 2, 2:52 | $i = 120^\circ$: which way at the ascending node, and where $\hat h$ points (the video answers next) |
| 3.1 | Ep 3, 1:57 | multiply out row 3 of $C_{PN}$ (the video answers next) |
| 4.1 | Ep 4, 2:08 | practice orbit: $\mathcal E$, $a$, $\vec h$, $\vec e$, $e$, $r_p$, $r_a$ |
| 4.2 | Ep 4, 4:49 | practice orbit: $C_{PN}$, then $i$, $\Omega$, $\omega$ two ways |
| 4.3 | Ep 4, 5:12 | what decides $80^\circ$ vs $280^\circ$; the practice orbit's $\theta_0$ |
| 5.1 | Ep 5, 2:00 | practice orbit: elements back to $\vec r$, $\vec v$ |
| 6.1 | Ep 6, 1:55 | practice orbit's $\dot\Omega$; sun-synchronous inclination at 600 km |
| 6.2 | Ep 6, 2:32 | critical inclination; practice orbit's $\dot\omega$ |

The practice orbit is $\vec r_0 = (-5404.7, -9275.9, 2171.6)$ km, $\vec v_0 = (3.4111, -2.2048, 4.8031)$ km/s,
designed so that $\Omega$ (third quadrant), $\omega$ (fourth quadrant) and $\theta_0$ ($\vec r\cdot\vec v > 0$)
each test a different sign check from the Molniya example. `python3 check_guide.py` asserts every number in the
guide. A fresh agent worked the checkpoints cold before release, and its answers matched.

**Notes**

- The drawn orbits are not to scale (Molniya drawn at $a = 3$, $e = 0.6$ Earth radii) so that
  they fit next to the globe. The numbers on screen are the true values.
- Worked numbers use 4-digit unit vectors, so a few products land 1 off in the last digit
  (shown with ≈).

## Rebuilding

Made with [ManimToolkit](https://github.com/abhichavali/ManimToolkit) (`mtk`). Narration is OpenRouter TTS
(`google/gemini-3.8-flash-tts`, voice Achird), cached in `audio/`. The shared 3D kit is `orbit3d.py`, and
the script is `BRIEF.md`.

```bash
cd astronautics_video/orbit_det
mtk check                      # storyboards in media/board/, no API key needed (audio is cached)
mtk render -q h -o orbit_determination
mtk episodes BRIEF.md          # out/ep0N.mp4 + web copies, captions, chapters, checkpoint times
mtk guide guide.tex            # out/guide.pdf with video times, checkpoint crops for the site
mtk site --out <dir>           # the study page (index.html + videos)
# re-voicing (only if a narration line in BRIEF.md changes):
export OPENROUTER_API_KEY=sk-or-...   # never commit this
python voice_brief.py
```
