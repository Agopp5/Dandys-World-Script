# AERSP 301: Shear of Thin-Walled Beams (5 videos)

The same step-by-step style as the AERSP 309 lessons. The concepts come first, with visuals,
and then HW 3 is worked as the application. Built from the lecture decks *Shear of Beams:
Open C/S* and *Closed C/S* (Megson Ch. 17).

| Part | Video | What it covers |
|---|---|---|
| 1 | `part1_shear_flow` | why shear loads create shear flow; $q = \tau t$; element equilibrium $\partial q/\partial s + t\,\partial\sigma_z/\partial z = 0$ derived line by line; the open-section $q_s$ formula; what $\int t\,y\,ds$ means |
| 2 | `part2_shear_center` | why a channel twists; the shear center; symmetry shortcuts; the channel worked fully: $I_{xx}$, $q$ in every wall, flange couple, $e = 3b^2/(h+6b)$ |
| 3 | `part3_hw3_problem1_channel` | **HW 3 P1**: centroid, $I_{xx}, I_{yy}, I_{xy}$, the $97/9$ determinant, moments about the corner (only the top flange counts), $\xi_s = -45a/97$, $\eta_s = 46a/97$ |
| 4 | `part4_closed_sections` | cut and close: $q = q_b + q_{s,0}$; why $\oint p\,ds = 2A$ (animated); rate of twist; zero-twist condition for the shear center |
| 5 | `part5_hw3_problem2_triangle` | **HW 3 P2**: extra-credit $I_{xx}$; $q_b$ cut at the apex; $q_{s,0}$ from moments about the apex; final distribution, principal values, directions, checks |

All results were checked symbolically (sympy): resultant force equals the applied load,
the moment balance holds, and $q = 0$ at free edges.

**Note on Problem 1:** the stated answer ($-45a/97,\ 46a/97$) requires the **web and the top
flange to both be $2t$**, with the bottom flange $t$. That matches the bold lines in the figure.
Reading only the top flange as $2t$ gives $(-9a/17,\ 8a/17)$ instead.

## Rebuilding

From `astronautics_video/`:

```bash
export OPENROUTER_API_KEY=sk-or-...
python tts.py --project structures      # narration -> structures/audio
cd structures && python render.py       # -> structures/output/part<N>_*_1080p30.mp4
```
