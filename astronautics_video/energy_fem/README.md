# AERSP 301: Energy Methods and the Finite Element Method (8 videos, 70 min, with a practice guide)

From the slide decks "9. Stationary Principle", "10. FEM" and "11. FEM b", and HW 6. Made for a viewer who has not
been to the lectures, at the slower MTK cadence: every term is defined before it is used, every algebra step is its
own beat, every number is read aloud, and each result is held on screen. The homework gives no FEM practice beyond
Problem 2, so the videos add two worked FEM examples of their own (a column under its own weight, and a stepped bar
with a spring).

| Ep | Video (`output/`) | Length | What it covers |
|---|---|---|---|
| 1 | `ep1_work_energy_and_the_bowl` | 8:07 | work under a growing force; strain energy $U = \frac12Kq^2$; the work potential $W = Fq$ (no one half, and why); $\Pi = U - W$ is a bowl whose bottom is equilibrium; the stationary principle |
| 2 | `ep2_many_springs` | 10:43 | two springs by Newton and by energy; partial derivatives give the matrix equation $Kq = F$; why energy scales; the slides' four-node example; the pattern each spring adds to $K$ |
| 3 | `ep3_homework_problem_1` | 8:56 | **HW P1**: reading the figure, every spring's stretch, $\Pi$, three partial derivatives, solving by substitution: $q_2 = \frac{P_1 + 2(P_2+P_3+P_4)}{2K_1+K_2}$, $q_1 = \frac{P_1 + K_2q_2}{2K_2}$, $q_3 = q_2 + P_4/K_3$; a numeric check |
| 4 | `ep4_from_springs_to_bars` | 10:16 | a bar has infinitely many unknowns; $U = \int \frac12 EA\,u'^2\,dx$; assume a shape; how good the guess is; the slides' beam (0.02053 vs exact 0.02083 $PL^3/EI$); from one shape to many pieces |
| 5 | `ep5_one_finite_element` | 8:28 | nodes and elements; local coordinate; shape functions $N_1, N_2$; strain in an element; $k = \frac{EA}{l}\begin{bmatrix}1&-1\\-1&1\end{bmatrix}$; load vector $\frac{cl}{2}\{1,1\}$ |
| 6 | `ep6_assembly_and_solving` | 9:20 | column under its own weight, 3 elements: assembling $K$ and $F$, deleting the support row, solving ($-\frac59, -\frac89, -1$ times $\rho gL^2/2E$), the stress staircase, the reaction $R = \rho gAL$ from the set-aside row |
| 7 | `ep7_a_new_example` | 6:33 | stepped aluminum bar plus a spring between two walls: $q = 0.2, 0.1$ mm, $\sigma = 28, -14$ MPa, reactions 5600 N and 1400 N, Newton check |
| 8 | `ep8_homework_problem_2` | 7:46 | **HW P2**: two elements, $K$ and $F$, $q_1 = 0$, $q_2 = 0.05$ in, wall reaction $R = 50$ lb; why point 1 doesn't move (and what four elements say about the point at 10 in); recap |

**HW P1 assumptions** (the videos say both out loud): the unlabeled spring between the junction and the bar is
taken as a second $K_2$, since the label sits between the two; if the instructor says otherwise, only that one
stiffness changes. The vertical bar is rigid and slides without tilting, so every spring end on it moves $q_2$.

**Not covered:** the rotated (truss) element from "11. FEM b"; HW 6 does not use it.

## Practice guide

`output/energy_fem_guide.pdf` (source `guide.tex`, every number asserted in `check_guide.py`) has 13 checkpoints,
two fresh practice problems (A: three springs by the stationary principle; B: a steel bar by three finite
elements), hints, and full solutions.

| Checkpoint | Video time | Task |
|---|---|---|
| 1.1 | Ep 1, 6:02 | one spring: write $\Pi$, find its minimum |
| 2.1 | Ep 2, 6:04 | two springs: solve the 2 by 2 system |
| 2.2 | Ep 2, 9:51 | row 3 of the four-node stiffness matrix |
| 3.1 | Ep 3, 4:17 | HW P1: $\partial\Pi/\partial q_2$ |
| 3.2 | Ep 3, 7:46 | HW P1 with numbers, Newton check |
| 4.1 | Ep 4, 6:58 | straight-line guess vs exact at mid-bar |
| 5.1 | Ep 5, 6:19 | an element's stiffness $EA/l$ |
| 6.1 | Ep 6, 2:52 | the column's global load vector |
| 6.2 | Ep 6, 7:29 | stress in element 2 of the column |
| 7.1 | Ep 7, 1:52 | assemble the stepped bar's 4 by 4 $K$ |
| 7.2 | Ep 7, 4:49 | stress in the thin piece |
| 8.1 | Ep 8, 2:12 | HW P2: $K$ and $F$ |
| 8.2 | Ep 8, 4:04 | HW P2: the wall reaction |

A fresh agent worked every checkpoint and both practice problems cold before release; all answers matched, and the
statements were clarified where it found missing givens.

## Rebuilding

Made with ManimToolkit (`mtk`), slow-cadence update; narration is OpenRouter TTS, cached in `audio/` (cached by
text, so re-rendering needs no key unless a line changes). Shared drawing kit: `efem.py`. Script: `BRIEF.md`.
Verified solutions: `solve.py` (all lesson numbers), `check_guide.py` (all guide numbers).

```
mtk check                 # storyboards in media/board/
mtk render -q h -o energy_fem
mtk episodes BRIEF.md
mtk guide guide.tex
```
