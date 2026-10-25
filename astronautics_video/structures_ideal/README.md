# AERSP 301: Booms, Shear Flow and Multi-Cell Torsion (6 videos, 27 min, with a practice guide)

From the slide decks "7. Structural Idealization" and "8. Torsion of Multi-Cell Cross-Sections" and HW 5.
This is the slow cut, made for a viewer who has not been to the lectures. It starts from what the parts of a
wing box are, defines every term before using it, reads every number aloud, shows every algebra step, and holds
each result on screen. Both homework problems are then worked step by step.
(The first, faster 13-minute cut is in `old/` and in the git history.)

| Ep | Video (`output/`) | Length | What it covers |
|---|---|---|---|
| 1 | `ep1_wing_box_parts` | 3:38 | skins, spars, stringers, ribs and what each one carries; direct stress from bending, $\sigma_z = M_xy/I_{xx}$; shear stress and shear flow $q = \tau t$ |
| 2 | `ep2_why_booms` | 3:37 | booms carry the direct stress, skin carries shear; $B_1 = \frac{t_Db}{6}(2 + \sigma_2/\sigma_1)$ derived from a moment balance; ratio $+1$ (skins) and $-1$ (webs in bending) |
| 3 | `ep3_shear_flow_with_booms` | 4:43 | the jump at a boom, $q_2 - q_1 = -(S_y/I_{xx})B_ry_r$; the slide's channel ($-6, -12, -6$ N/mm, back to 0); what the shear centre is; closed sections: cut, march, close with $q_{s,0}$ |
| 4 | `ep4_hw_problem_1` | 6:08 | **HW P1**: idealize the box (booms 4000 and 3556 mm$^2$), $I_{xx} = 340.0\times10^6$ mm$^4$, basic flow, zero twist gives $q_{s,0}$, shear centre $\xi = 224.8$ mm from the left web |
| 5 | `ep5_closed_section_torsion` | 4:59 | a single cell: $T = 2Aq$ (500 x 250 mm cell, 10 kN m: $q$ = 40 N/mm, $\tau$ = 20 N/mm$^2$); rate of twist $\frac{d\theta}{dz} = \frac{1}{2AG}\oint q\,\frac{ds}{t}$ (0.25 deg/m); many cells, equal twist; $t^* = (G/G_{REF})t$ |
| 6 | `ep6_hw_problem_2` | 3:49 | **HW P2**: two-cell box with different $G$: $q_I = 1.261\times10^{-6}\,T$, $q_{II} = 0.804\times10^{-6}\,T$ ($T$ in N mm); per 1 kN m: 1.26, 0.80, spar 0.46 N/mm |

**HW P2 note:** the sheet gives no torque magnitude, so the answer is per unit torque; multiply by the torque
your professor gives. The boom areas in that problem are irrelevant in pure torsion (the video says so).

## Practice guide

`output/practice_guide.pdf` (source `guide.tex`, numbers asserted in `check_guide.py`) has five checkpoints:

| Checkpoint | Video time | Task |
|---|---|---|
| 2.1 | Ep 2, 3:18 | area a 300 mm web in bending adds to each boom (the video answers next) |
| 3.1 | Ep 3, 2:16 | finish the channel past booms 2, 3, 4 (the video answers next) |
| 4.1 | Ep 4, 6:05 | practice box (600 x 240): booms 3204 / 2925 mm$^2$, shear centre 276.3 mm |
| 5.1 | Ep 5, 3:30 | twist rate of cell I of a two-cell box (the video answers next) |
| 6.1 | Ep 6, 3:00 | practice two-cell box, $T$ = 15 kN m: $q_I$ = 30.0, $q_{II}$ = 25.0, spar 5.0 N/mm, 0.32 deg/m |

A fresh agent worked every checkpoint cold before release; its answers matched, and the statements were clarified
where it found a gap (boom numbering, $\tau = q/t$, the twist-rate formula with $G_{REF}$).

## Rebuilding

Made with [ManimToolkit](https://github.com/abhichavali/ManimToolkit) (`mtk`); narration is OpenRouter TTS
(`google/gemini-3.8-flash-tts`, voice Achird, slow tutor style), cached in `audio/`. Shared drawing kit: `sect.py`.
Script: `BRIEF.md`. Verified solutions: `solve.py` (HW and slide examples), `practice.py`, `check_guide.py`.

```bash
cd astronautics_video/structures_ideal
mtk check && mtk render -q h -o structures_ideal && mtk episodes BRIEF.md
mtk guide guide.tex && mtk site --out <dir>
# re-voicing (only if a narration line changes): export OPENROUTER_API_KEY=... ; python3 voice_brief.py
```
