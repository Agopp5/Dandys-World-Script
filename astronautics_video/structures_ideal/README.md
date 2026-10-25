# AERSP 301: Booms, Shear Flow and Multi-Cell Torsion (5 videos, 13 min, with a practice guide)

From the slide decks "7. Structural Idealization" and "8. Torsion of Multi-Cell Cross-Sections" and HW 5.
Concepts come first, then both homework problems step by step. Every substitution is on screen.

| Ep | Video (`output/`) | Length | What it covers |
|---|---|---|---|
| 1 | `ep1_why_booms` | 2:22 | booms carry direct stress, skin carries shear; effective boom area $B_1 = \frac{t_Db}{6}(2 + \sigma_2/\sigma_1)$ derived from a moment balance; ratio $+1$ (skins) and $-1$ (webs in bending) |
| 2 | `ep2_shear_flow_with_booms` | 2:25 | the jump at a boom, $q_2 - q_1 = -(S_y/I_{xx})B_ry_r$; the slide's channel ($-6, -12, -6$ N/mm, back to 0); closed sections: cut, march, close with $q_{s,0}$ |
| 3 | `ep3_hw_problem_1` | 3:27 | **HW P1**: idealize the box (booms 4000 and 3556 mm$^2$), $I_{xx} = 340.0\times10^6$ mm$^4$, basic flow, zero twist gives $q_{s,0}$, shear centre $\xi = 224.8$ mm from the left web |
| 4 | `ep4_multicell_torsion` | 1:51 | one constant $q$ per cell, $T = \sum 2A_Rq_R$, equal rate of twist in every cell, modulus-weighted thickness $t^* = (G/G_{REF})t$; slide 3-cell check (7.1, 8.9, 4.2 N/mm) |
| 5 | `ep5_hw_problem_2` | 2:53 | **HW P2**: two-cell box with different $G$: $q_I = 1.261\times10^{-6}\,T$, $q_{II} = 0.804\times10^{-6}\,T$ ($T$ in N mm); per 1 kN m: 1.26, 0.80, spar 0.46 N/mm |

**HW P2 note:** the sheet gives no torque magnitude, so the answer is per unit torque; multiply by the torque
your professor gives. The boom areas in that problem are irrelevant in pure torsion (the video says so).

## Practice guide

`output/practice_guide.pdf` (source `guide.tex`, numbers asserted in `check_guide.py`) has five checkpoints:

| Checkpoint | Video time | Task |
|---|---|---|
| 1.1 | Ep 1, 2:12 | area a 300 mm web in bending adds to each boom (the video answers next) |
| 2.1 | Ep 2, 1:22 | finish the channel past booms 2, 3, 4 (the video answers next) |
| 3.1 | Ep 3, 3:24 | practice box (600 x 240): booms 3204 / 2925 mm$^2$, shear centre 276.3 mm |
| 4.1 | Ep 4, 0:53 | twist rate of cell I of a two-cell box (the video answers next) |
| 5.1 | Ep 5, 2:08 | practice two-cell box, $T$ = 15 kN m: $q_I$ = 30.0, $q_{II}$ = 25.0, spar 5.0 N/mm, 0.32 deg/m |

A fresh agent worked every checkpoint cold before release; its answers matched, and the statements were clarified
where it found a gap (boom numbering, $\tau = q/t$, the twist-rate formula with $G_{REF}$).

## Rebuilding

Made with [ManimToolkit](https://github.com/abhichavali/ManimToolkit) (`mtk`); narration is OpenRouter TTS
(`google/gemini-3.8-flash-tts`, voice Achird), cached in `audio/`. Shared drawing kit: `sect.py`. Script: `BRIEF.md`.
Verified solutions: `solve.py` (HW and slide examples), `practice.py`, `check_guide.py`.

```bash
cd astronautics_video/structures_ideal
mtk check && mtk render -q h -o structures_ideal && mtk episodes BRIEF.md
mtk guide guide.tex && mtk site --out <dir>
# re-voicing (only if a narration line changes): export OPENROUTER_API_KEY=... ; python3 voice_brief.py
```
