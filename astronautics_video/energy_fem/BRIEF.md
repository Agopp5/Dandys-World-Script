# Energy Methods and the Finite Element Method  (~70 min, 8 episodes)

**Viewer**: an AERSP 301 (aerospace structures) student who has NOT been coming to class and has HW 6 due: Problem 1
(springs, stationary principle) and Problem 2 (a bar by the finite element method). They need the ideas from zero,
slowly, and the homework worked in full. PACE: unhurried. Every term is defined in plain words before it is used,
every algebra step is its own beat, every number is read aloud, and each result is held on screen before moving on.
**Knows**: algebra; derivatives, partial derivatives and the chain rule; definite integrals (including a change of
variable); a matrix times a vector, and solving 2 by 2 and 3 by 3 linear systems; Hooke's law for a spring, force
equals stiffness times stretch; stress is force over area, strain is change in length over length, and sigma equals
E times epsilon; free-body diagrams and force balance; beam bending moment M equals minus E I times v double prime.
Nothing about work and energy in structures, strain energy, the stationary principle, or finite elements.
**Hook**: a spring with a weight on it. The way they already know finds the stretch by balancing forces. There is a
second way: write down one number, the energy, and find the bottom of a bowl. That second way grows into the finite
element method, the tool behind every structural simulation.
**Insight**: the true displacement is the one that makes the total potential energy, strain energy minus the work
potential of the loads, as small as possible; setting its derivatives to zero gives the equilibrium equations, as a
matrix, and FEM is that idea applied to a structure chopped into small pieces with simple straight-line shapes.
**Payoff**: Episode 8 solves the homework's bar with the same steps as Episode 1's single spring, now as matrices.
**Crux**: (1) W has no one half but U does: U is the area under a rising force line, while the work potential treats
the load as already at full value (misconception: "both should have a half"). (2) A spring's stretch is the
DIFFERENCE of its end displacements (misconception: stretch equals the node's own displacement). (3) Each element is
just a spring with k equal to E A over l, and assembly adds overlapping entries (misconception: elements are solved
separately). (4) A fixed node's row and column are removed before solving, and the removed row later gives the
reaction (misconception: invert the full matrix, which is singular).
**Ladder**:
1. (support, 1:00) two ways to find a spring's stretch: forces, or energy
2. (core, 4:30) work under a rising force is a triangle, U equals one half K q squared; W equals F q, no half
3. (core, 4:00) Pi equals U minus W is a bowl; its bottom, d Pi d q equals zero, is K q equals F
4. (core, 10:00) several springs: stretch is a difference; partial derivatives give the stiffness matrix; pattern
5. (core, 10:00) HW P1 worked in full
6. (core, 11:00) bars: strain energy density, U for a bar, assumed shapes (Rayleigh-Ritz), beam check, why FEM
7. (core, 11:00) one element: local coordinate s, shape functions, element stiffness E A over l, load vector c l over 2
8. (core, 12:00) assembly, boundary conditions, solve, stresses, reactions: the column under its own weight vs exact
9. (core, 10:00) a new worked example: stepped aluminum bar with a spring
10. (core, 10:00) HW P2 worked in full; why point 1 does not move; recap
11. (aside, cut) the rotated (2D truss) bar element from the slides; kinetic energy and dynamics

Every file starts:
```python
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})
```
Hues: strain energy U MINT; work potential W EMBER; total potential Pi GOLD; displacements (q, u) SKY; loads and
reactions (F, P, f, R, Q) ROSE; stiffness (K, k, and the springs themselves) LILAC; shape functions and the local
coordinate s LIME; stress and strain ACCENT. Walls, bars and text INK/INK2; notes MUTED.
`efem.py` (shared kit; `from efem import *` also imports mtk): `wall`, `spring`, `node`, `force`, `disp`, `bar`,
`fem_bar`, `dist_load`. Its docstring lists the API. Springs are always LILAC zigzags, loads ROSE arrows,
displacements small SKY arrows under the node. Bars are SURFACE rectangles with INK2 outline.
Readability (the viewer struggles with small text): main math size 44 to 56, labels and cards at least 32, notes at
least 30. At most about 3 equation lines plus a figure at once. Hold each new result still for a moment.
Matrices: build with `M(r"\begin{bmatrix} ... \end{bmatrix}")` or manim `Matrix`; color entries by meaning.

## Facts (assert the ones your scene shows; every number below is derived in solve.py)
- Units: Episodes 1, 2, 5, 7 use newtons and millimeters (stiffness N/mm, stress N/mm squared, which is MPa).
  Episode 8 (the homework) uses pounds and inches (psi = lb per square inch). Episode 6 is symbolic.
- Work under a force that grows in step with the stretch, from 0 to F as u goes from 0 to q: integral of K u du
  from 0 to q equals one half K q squared (area of a triangle, base q, height K q).
- Strain energy U: the energy stored in the deformed elastic body; for a spring U = (1/2) K q^2. A rigid body has no
  strain, so no strain energy. A rigid translation of a spring (both ends move together) stores nothing.
- Work potential W of a load: W = F q, the load times the displacement of its point, with F at its full, fixed value
  (a "dead load"). No one half. Slides: "W(q) = F q (not work done by the force)".
- Total potential energy Pi(q) = U(q) - W(q) (the slides write pi or capital Pi; we use capital Pi everywhere).
- Stationary principle (principle of minimum total potential energy): among all geometrically possible
  displacements (ones that respect the supports), the actual one makes Pi stationary, and for a stable elastic
  structure a minimum. Setting d Pi / d q = 0 gives the equilibrium equations; same as Newton's method.
- One spring example: K = 20 N/mm, F = 100 N. Pi(q) = 10 q^2 - 100 q (N mm). Pi at q = 0, 3, 5, 7, 10:
  0, -210, -250, -210, 0. Minimum at q = 5 mm. There U = 250 N mm, W = 500 N mm, Pi = -250 N mm. U is half of W at
  equilibrium (the triangle is half the rectangle).
- Two springs in series (slides' figure): wall - k1 - node 1 - k2 - node 2. Loads F1 at node 1, F2 at node 2, both
  in +x. Stretch of spring 1 = q1; stretch of spring 2 = q2 - q1.
  Newton: node 1: -k1 q1 + k2 (q2 - q1) + F1 = 0 -> (k1 + k2) q1 - k2 q2 = F1. Node 2: -k2 (q2 - q1) + F2 = 0 ->
  -k2 q1 + k2 q2 = F2. Matrix [[k1 + k2, -k2], [-k2, k2]] {q1, q2} = {F1, F2}.
  Energy: U = (1/2) k1 q1^2 + (1/2) k2 (q2 - q1)^2; W = F1 q1 + F2 q2.
  d Pi/d q1 = k1 q1 + k2 (q2 - q1)(-1) - F1 = 0 (chain rule: derivative of (q2 - q1) with respect to q1 is -1).
  d Pi/d q2 = k2 (q2 - q1) - F2 = 0. Same equations.
  Numbers: k1 = 40 N/mm, k2 = 20 N/mm, F1 = 40 N, F2 = 20 N -> matrix [[60, -20], [-20, 20]], q1 = 1.5 mm,
  q2 = 2.5 mm. Newton check: spring 1 carries F1 + F2 = 60 N -> stretch 60/40 = 1.5; spring 2 carries 20 N ->
  stretch 20/20 = 1.0 = q2 - q1.
- Slides' four-node sample: wall - k1 - node 2 - two springs k2 in parallel - node 3 - k3 - node 4 (node 1 is the
  wall end, displacement q1 kept as a symbol in the slides). U = (1/2) k1 (q2 - q1)^2 + 2 [(1/2) k2 (q3 - q2)^2] +
  (1/2) k3 (q4 - q3)^2 (two parallel k2 springs: twice the energy). Loads: only F2 and F4 (P1 = P3 = 0).
  Matrix [[k1, -k1, 0, 0], [-k1, k1 + 2k2, -2k2, 0], [0, -2k2, 2k2 + k3, -k3], [0, 0, -k3, k3]].
- The pattern: a spring of stiffness k between nodes i and j adds +k at (i,i) and (j,j) and -k at (i,j) and (j,i).
  Every row sums to zero before supports are applied (moving everything together stores no energy).
- HW P1 (spring system). Figure: a wall on the left. K1 runs from the wall to a vertical bar (the bar's displacement
  is q2). K2 runs from the wall to a junction whose displacement is q1; a second spring, unlabeled in the figure, runs
  from that junction to the bar; WE TREAT IT AS A SECOND K2 (the label sits between the two; say so, and say to check
  with the instructor). K3 runs from the bar to an outer node whose displacement is q3. Loads: P1 at the q1 junction,
  P2 and P3 on the bar, P4 at the q3 node; all point right (+x). The bar is rigid and translates without rotating, so
  every spring end on it moves q2.
  Stretches: K1: q2; first K2: q1; second K2: q2 - q1; K3: q3 - q2.
  U = (1/2)K1 q2^2 + (1/2)K2 q1^2 + (1/2)K2 (q2 - q1)^2 + (1/2)K3 (q3 - q2)^2;  W = P1 q1 + (P2 + P3) q2 + P4 q3.
  d/dq1: K2 q1 - K2 (q2 - q1) - P1 = 0 -> 2K2 q1 - K2 q2 = P1.
  d/dq2: K1 q2 + K2 (q2 - q1) - K3 (q3 - q2) - (P2 + P3) = 0 -> -K2 q1 + (K1 + K2 + K3) q2 - K3 q3 = P2 + P3.
  d/dq3: K3 (q3 - q2) - P4 = 0 -> -K3 q2 + K3 q3 = P4.
  Matrix [[2K2, -K2, 0], [-K2, K1 + K2 + K3, -K3], [0, -K3, K3]] {q1, q2, q3} = {P1, P2 + P3, P4}.
  Solve: third equation gives K3 (q3 - q2) = P4. Add it to the second: -K2 q1 + (K1 + K2) q2 = P2 + P3 + P4.
  First: q1 = (P1 + K2 q2) / (2K2). Substitute: (K1 + K2/2) q2 - P1/2 = P2 + P3 + P4 ->
  q2 = (P1 + 2(P2 + P3 + P4)) / (2K1 + K2).
  q1 = ((K1 + K2) P1 + K2 (P2 + P3 + P4)) / (K2 (2K1 + K2)).   q3 = q2 + P4 / K3.
  Sanity numbers: all K = 100 N/mm, all P = 30 N -> q2 = 210/300 = 0.7 mm, q1 = (30 + 70)/200 = 0.5 mm,
  q3 = 0.7 + 0.3 = 1.0 mm. Newton checks: K3 carries P4: 100 x 0.3 = 30 N. Whole system: the wall springs carry
  everything: K1 q2 + K2 q1 = 70 + 50 = 120 N = 4 x 30.
- Bar (continuum): axial load only; displacement u(x); boundary condition u(0) = 0 at a fixed wall. Infinitely many
  degrees of freedom.
- Strain energy per unit volume U* = integral of sigma d epsilon = (1/2) E epsilon^2 (area under the stress-strain
  line, a triangle again). Strain epsilon = du/dx.
- Bar strain energy U = integral over the volume of U* = (1/2) integral from 0 to L of E A (du/dx)^2 dx.
  Uniform bar stretched evenly: u = q x / L -> U = (1/2)(E A / L) q^2: a spring with K = E A / L.
- Work potential of a bar: W = P u(L) + integral from 0 to L of f u dx (P a tip load, f a distributed load per length).
  Pi(u) = U - W.
- Assumed shape (the Rayleigh-Ritz idea; slides call it an assumed displacement): pick a shape with a few unknown
  numbers that respects the supports; then Pi is an ordinary function of those numbers.
  Example: bar fixed at x = 0, uniform distributed load f (per length) along +x, no tip load. Assume u = a x.
  U = (1/2) E A a^2 L; W = f a L^2 / 2; d Pi / d a = E A a L - f L^2 / 2 = 0 -> a = f L / (2 E A).
  Tip: a L = f L^2 / (2 E A). Exact: u(x) = (f / E A)(L x - x^2 / 2); tip f L^2 / (2 E A): the same.
  Middle (x = L/2): assumed (1/4) f L^2 / E A, exact (3/8) f L^2 / E A. So the shape is approximate inside.
- Slides' beam sample: simply supported, length L, stiffness E I, point load at mid-span. The slides call that load
  W, the same letter as work potential, so the video calls it P and says once "the slides call it W".
  Assume v = v_B sin(pi z / L) (zero at both ends, peak v_B at the middle, flat there). U = integral of M^2/(2EI) dz
  with M = -E I v''. v'' = -v_B (pi/L)^2 sin(pi z / L). U = pi^4 E I v_B^2 / (4 L^3). Pi = pi^4 E I v_B^2/(4L^3) - P v_B.
  d Pi/d v_B = pi^4 E I v_B / (2 L^3) - P = 0 -> v_B = 2 P L^3 / (pi^4 E I) = 0.02053 P L^3 / E I.
  Exact beam theory: P L^3 / (48 E I) = 0.02083 P L^3 / E I. Difference 1.45 percent ("about one and a half percent").
- FEM idea: chop the bar into short pieces (elements) joined at points (nodes). Inside each element u is a straight
  line between its two nodal displacements. Neighbours share a node, so u is continuous. Global degrees of freedom
  q1 ... qN (nodal displacements of the whole bar); local (element) DOFs u1, u2 at its two ends.
  Slides' 3-element bar: nodes 1-4, element i runs from node i to node i+1: u1 of element 1 = q1, u2 of element 1 =
  q2 = u1 of element 2, and so on.
- Local coordinate: element from x1 to x2, length l = x2 - x1. s = (x - x1)/l runs from 0 to 1. x = (1 - s) x1 + s x2.
  dx = l ds.
- Shape functions: u(s) = (1 - s) u1 + s u2 = N1(s) u1 + N2(s) u2, with N1 = 1 - s, N2 = s. N1 is 1 at node 1 and 0
  at node 2; N2 the reverse; N1 + N2 = 1. (Derivation: assume u = b1 s + b2; at s = 0, u = u1 so b2 = u1; at s = 1,
  u = u2 so b1 = u2 - u1.)
- Strain in an element: du/dx = (du/ds)(ds/dx) = (u2 - u1)(1/l), constant in the element; = (1/l)[-1 1]{u1; u2}.
- Element strain energy: U_e = (1/2) integral from 0 to 1 of E A ((u2 - u1)/l)^2 l ds = (1/2)(E A / l)(u2 - u1)^2
  = (1/2) [u1 u2] (E A / l)[[1, -1], [-1, 1]] {u1; u2}. Element stiffness matrix k = (E A / l)[[1, -1], [-1, 1]]: the
  same as a spring with K = E A / l. (If E A varies, use its mean over the element: (EA)_mean / l.) Rows sum to zero.
- Numeric element (Episode 5): E A = 2 x 10^6 N, l = 500 mm -> E A / l = 4000 N/mm.
- Element load vector: W_e = integral of f u dx = u1 Q1 + u2 Q2 with Q1 = integral of f (1 - s) l ds,
  Q2 = integral of f s l ds. Uniform f = c: Q1 = Q2 = c l / 2: half the element's total load c l to each node.
- Assembly: U = sum of element U_e; each element's 2 by 2 block is added into the global matrix at its two global
  DOFs; where neighbouring elements share a node the entries add (k22 of element 1 plus k11 of element 2). Same for
  loads: a middle node collects c l / 2 from each side = c l. Point loads and the reaction R are added at their node.
- Column under its own weight (slides "vertical column under its own weight", the flag pole problem): height L, fixed at the base
  x = 0, x upward, constant A and E, weight per length f = -rho A g (down = minus x). Three equal elements l = L/3.
  Global K = (E A / l) [[1, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 1]] (1 + 1 = 2 at shared nodes).
  Global F = (c l / 2) {1, 2, 2, 1} + {R, 0, 0, 0} with c = -rho A g.
  Boundary condition q1 = 0: delete row 1 and column 1 -> (E A / l)[[2, -1, 0], [-1, 2, -1], [0, -1, 1]] {q2, q3, q4}
  = (c l / 2){2, 2, 1}. Solution {q2, q3, q4} = (rho g L^2 / 2E) {-5/9, -8/9, -1}.
  Exact: u(x) = (rho g / E)(x^2/2 - L x) = (rho g L^2 / 2E)(x/L)(x/L - 2): at x/L = 1/3, 2/3, 1 gives -5/9, -8/9, -1.
  FEM nodes exact here (do not expect this in general); between nodes FEM is a straight line, exact is a curve.
  Stress per element sigma = E (q_b - q_a)/l (constant): element 1: -5/6 rho g L; element 2: -1/2 rho g L;
  element 3: -1/6 rho g L. Exact sigma = -rho g L (1 - x/L), a straight line from -rho g L to 0; the FEM staircase
  equals it at each element's centre (x/L = 1/6, 1/2, 5/6). Stress is less accurate than displacement: it is the
  derivative of the assumed shape (one order lower).
  Reaction from the deleted row 1: (E A / l)(q1 - q2) = c l / 2 + R -> R = rho g A L (the column's whole weight,
  pushing up).
- Generated example (Episode 7), stepped aluminum bar: E = 70 000 N/mm^2. Left wall at node 0. Element 1: A = 200
  mm^2, l = 500 mm, node 0 to node 1. Element 2: A = 100 mm^2, l = 500 mm, node 1 to node 2. A spring K = 14 000 N/mm
  from node 2 to a right wall (node 3). Load P = 7000 N at node 1 (the step), pointing right.
  k1 = 70 000 x 200 / 500 = 28 000 N/mm. k2 = 70 000 x 100 / 500 = 14 000 N/mm. Spring 14 000 N/mm.
  Global 4 by 4: [[28000, -28000, 0, 0], [-28000, 42000, -14000, 0], [0, -14000, 28000, -14000], [0, 0, -14000,
  14000]]; F = {R0, 7000, 0, R3}. Both walls fixed: q0 = q3 = 0; delete rows/columns 0 and 3:
  [[42000, -14000], [-14000, 28000]] {q1, q2} = {7000, 0}. Determinant 42000 x 28000 - 14000^2 = 9.8 x 10^8.
  q1 = 7000 x 28000 / 9.8e8 = 0.2 mm; q2 = 7000 x 14000 / 9.8e8 = 0.1 mm.
  Stress element 1 = 70 000 x (0.2 - 0) / 500 = 28 MPa (tension); element 2 = 70 000 x (0.1 - 0.2)/500 = -14 MPa
  (compression). Spring force 14 000 x 0.1 = 1400 N (compressed, pushing on the right wall).
  Reactions from the deleted rows: R0 = 28000 (0 - 0.2) = -5600 N (the left wall pulls left);
  R3 = -14000 x 0.1 = -1400 N (the right wall pushes left). Check: 7000 - 5600 - 1400 = 0.
  Newton cross-check: from node 1, the left path has stiffness 28 000; the right path is element 2 and the spring in
  series: 1/(1/14000 + 1/14000) = 7000. Load splits 28 000 : 7000 = 4 : 1 -> 5600 N and 1400 N.
- HW P2 (bar by FEM): E = 10 x 10^3 psi, A = 2 in^2, L = 40 in, so E A = 20 000 lb. Wall at x = 0. Point 1 at x = L/2
  = 20 in carries P1 = 50 lb (pointing right); point 2 is the tip, x = 40 in, carrying P2 = 100 lb (right). f = 5 lb/in
  pointing LEFT (minus x) along the whole bar, so c = -5 lb/in. Point 3 at x = L/4 = 10 in is marked but not asked.
  Two elements of l = 20 in: node 0 (wall), node 1 (x = 20), node 2 (x = 40). Each element k = E A / l = 1000 lb/in.
  Each element's load vector c l / 2 = -5 x 20 / 2 = -50 lb at each of its nodes.
  Global K = 1000 [[1, -1, 0], [-1, 2, -1], [0, -1, 1]] lb/in. Global F = {-50 + R, -50 - 50 + 50, -50 + 100} =
  {R - 50, -50, 50} lb.
  Delete row/column 0 (q0 = 0): 1000 [[2, -1], [-1, 1]] {q1, q2} = {-50, 50}. Adding the two equations:
  1000 q1 = 0 -> q1 = 0. Then 1000 (q2 - 0) = 50 -> q2 = 0.05 in.
  Reaction from the constrained (deleted) row 0: 1000 (q0 - q1) = R - 50 -> 0 = R - 50 -> R = 50 lb, the wall pushes
  the bar in +x. Global check: R + P1 + P2 + total f = 50 + 50 + 100 - 200 = 0.
  Why q1 = 0: internal force N(x) = loads to the right of x = P2 + P1 (if x < 20) - 5 (40 - x). Left half:
  N = -50 + 5x lb: compression -50 at the wall, rising to +50 at x = 20. Its stretch integral over 0..20 is zero, so
  point 1 ends where it started. Right half: N = 100 - 5 (40 - x) = -100 + 5x (0 just right of x = 20, 100 at the tip).
  Exact u(L/4) = u(10) = integral 0..10 of (-50 + 5x)/20000 dx = (-500 + 250)/20000 = -0.0125 in; FEM (straight line
  from q0 = 0 to q1 = 0) gives 0 there: nodes exact, interior approximate; more elements would fix it.
- Rotated bar element (2D trusses) is in the slides but not in this HW: not covered (say so once in the recap).

## Guide checkpoints (ids identical in brief, code and guide.tex)
1.1 (Ep 1) one spring: K = 20 N/mm, F = 100 N: write Pi(q), find the q that makes it smallest.
2.1 (Ep 2) solve the two-spring system for q1, q2.  2.2 (Ep 2) write row 3 of the four-node sample's matrix.
3.1 (Ep 3) HW P1: take d Pi / d q2.  3.2 (Ep 3) plug in all K = 100 N/mm, all P = 30 N.
4.1 (Ep 4) with u = a x and a = f L / (2 E A), what is u at the middle, compared with exact?
5.1 (Ep 5) k for E = 70 000 N/mm^2, A = 100 mm^2, l = 250 mm (answer 28 000 N/mm).
6.1 (Ep 6) assemble the global load vector of the column under its own weight.  6.2 (Ep 6) stress in element 2.
7.1 (Ep 7) assemble the stepped bar's 4 by 4 matrix.  7.2 (Ep 7) the stress in element 2.
8.1 (Ep 8) HW P2: assemble K and F.  8.2 (Ep 8) HW P2: the reaction from the constrained equation.

# Episode 1: Work, Energy and the Bowl | one spring, two ways

## S01_Hook [166] Two ways to find a stretch
Picture: left half: a wall, a LILAC spring, a node, a ROSE load arrow F; right half empty at first.
1. "Here's a spring fixed to a wall, and a force pulling on its free end. How far does it stretch? You already know one way to answer that."
   → draw wall, spring, node; grow the force arrow F; the spring stretches a little and settles; a SKY arrow q under the node
2. "Balance the forces. The spring pulls back with stiffness times stretch, K times q. The load pulls forward with F. At rest they're equal, so K q equals F."
   → a free-body sketch of the node: a LILAC arrow left labeled K q, the ROSE arrow right labeled F; then E("K|q|=|F") appears large
3. "That's Newton's way. In this series you'll learn a second way, and it sounds completely different. Instead of balancing forces, we'll write down a single number, an energy, and look for the bottom of a bowl."
   → right half: a GOLD parabola (a bowl) fades in, a dot rolls down to its bottom and stops; the word "energy" near it
4. "Both ways give the same answer. But the energy way grows into something much bigger: the finite element method, the tool behind nearly every structural simulation you'll ever run."
   → under the bowl, a bar chopped into small elements with nodes appears (fem_bar), then the label "finite elements"
5. "Here's the plan: springs first, then your first homework problem, then bars and finite elements, and your second homework problem. Along the way, the video will pause for you to try things in your practice guide, a short PDF that goes with these videos."
   → a road map of 3 tags in a row: springs and HW 1, bars, finite elements and HW 2; the first glows; then a small PDF icon labeled "practice guide"

## S02_Work [214] Work under a growing force
Picture: top: the wall-spring-node; bottom: axes, force on the vertical axis, stretch u on the horizontal axis.
1. "Start with work. When a constant force pushes something through a distance, it does work: force times distance. On a graph of force against distance, that's the area of a rectangle."
   → a box pushed by a constant ROSE arrow through a distance d; small axes with a flat force line and the shaded rectangle under it
2. "A spring is different. If you slam the full force on at once, the spring bounces around. We want the slow, settled stretch, so we pull gently, and the force grows as the spring stretches."
   → main axes: horizontal u (stretch), vertical force; as a ValueTracker u moves from 0 to q, the spring stretches and a point climbs a straight LILAC line
3. "At a stretch u, the force is K times u. It starts at zero and climbs in a straight line, up to its full value at the final stretch q. That full value is F, which equals K q."
   → label the line "K u"; mark u = q on the axis and the height at its end labeled E("F = Kq"); dashed guides
4. "How much work does a force that keeps changing do? Chop the stretch into tiny steps d u. Over one tiny step the force barely changes, so the work is force times d u: a thin strip."
   → thin vertical strips under the line, one highlighted, labeled E("K u\,du")
5. "Add up all the strips, and you get the area under the force line. Here it's a triangle: base q, height K q. Half base times height: one half K q squared. That's the integral of K u d u, from zero to q."
   → the strips merge into a MINT triangle; E("\int_0^{q} K u\,du|=|\tfrac12|\,q|\cdot|Kq|=|\tfrac12 K q^2") built piece by piece, each part flashing its side of the triangle
6. "With numbers: K is twenty newtons per millimeter, and the final stretch is five millimeters. One half, times twenty, times five squared, is two hundred fifty newton millimeters."
   → E("\tfrac12 (20)(5)^2|=|250\text{ N mm}") under the triangle; 250 glows

## S03_Strain_Energy [82] Strain energy
Picture: the triangle from S02 kept small at the top right; the spring at left; then an energy parabola.
1. "Where does that work go? The spring is now stretched, and it's holding that energy inside. Let it go, and it snaps back and gives the energy back."
   → the spring stretched; a release: it snaps back and forth once; a MINT glow along the coils
2. "Energy stored in a deformed elastic body is called strain energy. We'll call it capital U. For a spring, U equals one half K q squared."
   → title words "strain energy" then E("U|=|\tfrac12|K|q^2") large, U in MINT
3. "Here's a picture to keep. Plot U against q. It's a parabola that opens upward: zero at q equals zero, and growing faster and faster as you stretch."
   → axes q horizontal, energy vertical; the MINT parabola U = 10 q^2 for K = 20 N/mm; a dot runs along it

## S04_Work_Potential [166] The work potential: no one half
Picture: a weight hanging from the spring's end over a pulley-free sketch (the load as a dead weight); then the force-stretch axes with the triangle and the rectangle.
1. "Now the load's side of the story. Think of the load F as a heavy weight hanging on the end of the spring. It always weighs the same, F, no matter how far the spring stretches."
   → the spring drawn vertically, a block of weight F hanging from it; a ROSE arrow F on the block
2. "When the end moves down by q, the weight drops by q, so it loses potential energy, F times q. That's called the work potential of the load, capital W. W equals F q."
   → the block drops by q; a SKY span q beside it; E("W|=|F|\,q") large, W in EMBER
3. "Pay close attention here, because this is the step everybody trips on. Strain energy has a one half, and the work potential doesn't. Why?" (style: slower and deliberate, stressing the key words)
   → self.spotlight on the two formulas side by side: E("U = \tfrac12 K q^2") and E("W = F q"); hold 2 s
4. "The spring's energy builds up from nothing: its force starts at zero and grows, so its energy is a triangle. The weight is full size the whole way down: the energy it gives up is a full rectangle, height F, width q."
   → lift the spotlight; on the force-stretch axes: the MINT triangle, then an EMBER rectangle of height F and width q drawn over it; the triangle is visibly half of it
5. "In other words, U is the triangle, W is the whole rectangle. With our numbers, W is one hundred newtons times five millimeters, five hundred newton millimeters. Exactly twice U."
   → E("W|=|(100)(5)|=|500\text{ N mm}") and next to it E("U = 250"); a brace "W = 2U at the answer"

## S05_Total_Potential [165] Total potential energy: a bowl
Picture: one set of axes, q from 0 to 10 mm horizontal, energy vertical; three curves U, W, Pi.
1. "Now combine them. As the spring stretches, it stores energy, U. And the weight gives energy up, W. So the total energy of the whole system, spring plus load, is U minus W."
   → the hanging spring again: a MINT tank filling labeled U, an EMBER tank draining labeled W
2. "This is the definition everything else rests on, so let it land. The total potential energy, capital Pi, is strain energy minus work potential. Pi equals U minus W." (style: slower and deliberate, stressing the key words)
   → self.spotlight(E("\Pi|=|U|-|W")); hold 2 s
3. "For our spring, that's one half K q squared, minus F q. With twenty and one hundred, Pi equals ten q squared minus one hundred q."
   → unspot; E("\Pi|=|\tfrac12 K q^2|-|F q") then below E("\Pi|=|10 q^2|-|100 q") with the numbers flashing
4. "Let's draw all three. U is the upward parabola. W is a straight line, rising. Subtract the line from the parabola, and you get Pi: a bowl that dips below zero."
   → plot MINT U = 10 q^2, EMBER W = 100 q, then the GOLD Pi curve; the space between U and W shaded briefly
5. "Look at a few values. At q equals zero, Pi is zero. At three, minus two hundred ten. At seven, also minus two hundred ten. At ten, back to zero."
   → dots on the GOLD curve at q = 0, 3, 7, 10 with their values in small cards; the symmetric pair 3 and 7 linked by a dashed line
6. "So where is the bottom of this bowl? Make a guess before we work it out."
   → self.predict("Where is the bottom of the bowl?", this line)

## S06_Minimum [169] The bottom of the bowl is equilibrium
Picture: the GOLD bowl on the left; algebra on the right.
1. "The bottom of a smooth bowl is where it's flat: the slope is zero. So we take the derivative of Pi with respect to q and set it to zero."
   → a tangent line slides along the bowl, tilting, and goes flat at the bottom; E("\frac{d\Pi}{dq}|=|0")
2. "Your turn: pause and do checkpoint one point one in your guide. Find the bottom of the bowl."
   → self.checkpoint("1.1", "One spring: find the q where Pi is lowest")
3. "The derivative of ten q squared is twenty q. The derivative of minus one hundred q is minus one hundred. So twenty q minus one hundred equals zero."
   → E("\frac{d\Pi}{dq}|=|20q|-|100|=|0") built term by term
4. "Twenty q equals one hundred, so q is five millimeters. There's the bottom of the bowl, at five, where Pi is minus two hundred fifty."
   → E("q|=|5\text{ mm}") glows; the dot settles at q = 5 on the bowl; a card "Pi = -250 N mm"
5. "Now do it with letters. The derivative of one half K q squared is K q. The derivative of F q is F. So K q minus F equals zero. Which says K q equals F."
   → E("\frac{d\Pi}{dq}|=|Kq|-|F|=|0") then E("Kq|=|F") below it
6. "This is the key step, so take it in slowly: setting the slope of the energy to zero gave us exactly Newton's force balance. Same equation, reached without drawing a single force." (style: slower and deliberate, stressing the key words)
   → self.spotlight(E("Kq = F")); next to it the S01 free-body equation slides in and matches; hold 2 s

## S07_Principle [168] The stationary principle
Picture: the bowl again with several trial displacements; then the wall end; then a key_box.
1. "Let's say what just happened in general. Imagine trying every stretch the spring could possibly have: two millimeters, eight, five. Each one gives a value of Pi."
   → trial dots at q = 2, 8, 5 drop onto the bowl one at a time, each with its Pi value
2. "Here's the principle: among all the geometrically possible displacements, the real one is the one that makes Pi stationary, and for a stable structure, a minimum. It's called the stationary principle, or the principle of minimum total potential energy."
   → q = 5 glows; title "stationary principle" appears with the statement in words
3. "Why should we believe it? Because, as you just saw, its slope condition is exactly force balance. Minimizing Pi and balancing forces are the same thing."
   → the two equations dPi/dq = 0 and Kq = F side by side with an equals sign between them
4. "Geometrically possible means the trial must respect the supports. The end bolted to the wall never moves, so no trial is allowed to move it."
   → the wall end of the spring flashes with a lock icon and "0" under it; a trial that moves the wall end is shown and crossed out
5. "Stationary means flat: the slope is zero. For a stable structure, the flat spot is the bottom of a bowl, a minimum."
   → the flat tangent at the bottom flashes
6. "So, stepping back: one spring, two routes. Balance forces, or minimize Pi equals U minus W. Next, we'll see why the energy route wins when there are many springs."
   → key_box("U = \tfrac12 K q^2", "W = F q", r"\Pi = U - W,\ \ \frac{d\Pi}{dq} = 0 \Rightarrow Kq = F", label="KEY IDEA")

# Episode 2: Many Springs | the stationary principle at work

## S08_Two_Springs [161] Two springs in a row
Picture: wall, spring k1, node 1, spring k2, node 2; loads F1 at node 1 and F2 at node 2; SKY q1, q2 under the nodes.
1. "Last time, one spring, where Newton and energy were equally easy. With more springs, which one is easier? Let's find out, on two springs in a row."
   → a small question card "which way is easier?" fades in and moves to a corner
2. "A wall, spring one, a junction we'll call node one, spring two, and the end, node two. There's a load on each node, F one and F two, and each node moves right: q one and q two. Those are our unknowns."
   → draw wall, spring k_1, node 1, spring k_2, node 2; ROSE arrows F_1, F_2; SKY disp arrows q_1, q_2 under the nodes
3. "Before anything else we need one fact: how much does each spring stretch? Spring one is easy. Its left end is on the wall, its right end moves q one, so it stretches q one."
   → animate node 1 moving right by q1; spring 1 stretches; E("\text{stretch}_1|=|q_1")
4. "Spring two is the one to watch. Both of its ends move. Its left end moves q one, and its right end moves q two. So its stretch is the difference: q two minus q one."
   → both nodes move; a double arrow over spring 2 marks its change in length; E("\text{stretch}_2|=|q_2|-|q_1")
5. "If both ends moved the same amount, the spring would just slide along without stretching at all. Only the difference counts."
   → both nodes move together by the same amount; spring 2 keeps its length; a small note "same shift: no stretch"

## S09_Newton [200] Newton's way, node by node
Picture: free-body diagrams of node 1 and node 2 on the left; equations on the right.
1. "First, Newton's way, so we have something to compare with. Cut out node one and list the forces on it."
   → node 1 isolated in a circle; three arrows appear one at a time
2. "Spring one pulls it back, to the left, with k one q one. Spring two pulls it forward, to the right, with k two times its stretch, q two minus q one. And the load F one pushes right."
   → arrows labeled k_1 q_1 (left), k_2 (q_2 - q_1) (right), F_1 (right)
3. "Balance: minus k one q one, plus k two times q two minus q one, plus F one, equals zero."
   → E("-k_1 q_1|+|k_2(q_2-q_1)|+|F_1|=|0")
4. "Multiply out and move F one across: minus k one q one, plus k two q two, minus k two q one, equals minus F one. Flip every sign and group the q one terms: k one plus k two, times q one, minus k two q two, equals F one."
   → the expanded line, then E("(k_1+k_2)\,q_1|-|k_2 q_2|=|F_1") below, the q1 terms tinted as they group
5. "Node two: spring two pulls it back with k two times q two minus q one, and F two pulls forward. So minus k two times q two minus q one, plus F two, equals zero. Multiply out: minus k two q one, plus k two q two, equals F two."
   → node 2 diagram; E("-k_2(q_2-q_1)|+|F_2|=|0") then E("-k_2 q_1|+|k_2 q_2|=|F_2")
6. "Two equations, two unknowns. Keep these on the side. Now let's get the very same equations from energy alone."
   → the two collected equations shrink into a boxed panel at the top right labeled "Newton"

## S10_Two_Energy [129] The energy of two springs
Picture: the two-spring figure at top; U, W, Pi built below.
1. "Strain energy first. Each spring stores one half, its stiffness, times its stretch squared. Then we add them up, because energy is just a number, and numbers add."
   → each spring glows MINT in turn as its term appears
2. "Spring one stores one half k one q one squared. Spring two stores one half k two, times q two minus q one, squared."
   → E("U|=|\tfrac12 k_1 q_1^2|+|\tfrac12 k_2 (q_2-q_1)^2")
3. "Pay close attention to that second term, because this is where most mistakes happen. It's the stretch, q two minus q one, that gets squared, not q two by itself." (style: slower and deliberate, stressing the key words)
   → self.spotlight on the (q_2 - q_1)^2 part; hold 2 s
4. "The work potential is each load times the displacement of its own node: F one q one plus F two q two."
   → unspot; E("W|=|F_1 q_1|+|F_2 q_2")
5. "And Pi is U minus W. One function of two unknowns. The stationary principle says: at the real answer, Pi is stationary in every direction."
   → E("\Pi|=|U|-|W") then the full expression on one line, fit to width

## S11_Partials [223] Two partial derivatives
Picture: Pi at top; two derivative lines below; the Newton panel from S09 on the right.
1. "With two unknowns, stationary means: the partial derivative with respect to q one is zero, and the partial derivative with respect to q two is zero."
   → E("\frac{\partial \Pi}{\partial q_1}|=|0") and E("\frac{\partial \Pi}{\partial q_2}|=|0")
2. "Take q one first. One half k one q one squared gives k one q one. For the second spring, use the chain rule: two times one half is one, times k two times q two minus q one, times the inside derivative."
   → E("\frac{\partial \Pi}{\partial q_1}|=|k_1 q_1|+|k_2(q_2-q_1)\cdot(-1)") built term by term
3. "And the inside derivative, the derivative of q two minus q one with respect to q one, is minus one. That minus sign is why our equations have minus signs between neighbors."
   → circle the (-1) in ACCENT
4. "Then the load: F one q one gives F one, with a minus sign. Set it all to zero: k one q one, minus k two q two, plus k two q one, minus F one, equals zero."
   → append -F_1 = 0; then the expanded line E("k_1 q_1|-|k_2 q_2|+|k_2 q_1|-|F_1|=|0")
5. "Group the q one terms and move F one across: k one plus k two, times q one, minus k two q two, equals F one. Exactly Newton's first equation."
   → the collected form slides next to the Newton panel's first equation; both glow GOOD
6. "Now q two. Only two terms contain it: the second spring gives k two times q two minus q one, and the load gives minus F two. Set to zero and multiply out: minus k two q one plus k two q two equals F two. Newton's second equation. We never drew an arrow."
   → E("\frac{\partial \Pi}{\partial q_2}|=|k_2(q_2-q_1)|-|F_2|=|0") then the collected form, matched with the Newton panel's second equation; both tick GOOD

## S12_Two_Matrix [191] As a matrix, with numbers
Picture: the matrix equation in the center; the two-spring figure small at the top.
1. "Stack the two equations into one matrix equation. Row one is node one's balance; row two is node two's. Each equation's coefficients drop into its row."
   → the two equations; their coefficients fly into M(r"\begin{bmatrix} k_1+k_2 & -k_2 \\ -k_2 & k_2 \end{bmatrix} \begin{Bmatrix} q_1 \\ q_2 \end{Bmatrix} = \begin{Bmatrix} F_1 \\ F_2 \end{Bmatrix}") row by row; stiffness LILAC, q SKY, F ROSE
2. "The matrix is called the stiffness matrix. Like K for one spring, it multiplies displacements and gives forces."
   → the matrix boxed, labeled "stiffness matrix"; a small E("K q = F") echo beside it
3. "Now numbers. k one is forty newtons per millimeter, k two is twenty. F one is forty newtons, F two is twenty. So the matrix is sixty, minus twenty, minus twenty, twenty."
   → value cards next to the figure; the numeric matrix [[60, -20], [-20, 20]] {q} = {40, 20}; hold it
4. "Your turn: pause and do checkpoint two point one in your guide, and solve for q one and q two."
   → self.checkpoint("2.1", "Solve the two-spring system for q1 and q2")
5. "Add the two equations: the q two terms cancel, leaving forty q one equals sixty, so q one is one point five millimeters. Then the second equation: twenty times q two minus one point five equals twenty, so q two is two point five millimeters."
   → the two rows added visually; E("40 q_1 = 60") then E("q_1 = 1.5\text{ mm}"); then E("20(q_2 - 1.5) = 20") and E("q_2 = 2.5\text{ mm}")
6. "Quick check with Newton. Cut through spring one: everything to its right carries forty plus twenty, sixty newtons, so it stretches sixty over forty, one point five. Spring two carries only F two, twenty, so it stretches one. Two point five minus one point five is one. It all agrees."
   → a dashed cut through spring 1 with the loads to its right summed; stretches 1.5 and 1.0 shown; GOOD ticks

## S13_Why_Energy [146] Why bother with energy?
Picture: a node with many springs attached; then a fake-3D surface of Pi(q1, q2).
1. "So which way was easier? For two springs, about the same. But picture a node with five springs on it. Newton needs five arrows, each with the right direction and the right sign. Energy needs one more term in a sum."
   → a node with 5 springs; Newton side: 5 arrows with signs, some flashing red as "sign?"; energy side: the sum U grows by one term per spring
2. "That's the first reason: energy is a scalar, a single number, with no directions to keep track of."
   → the arrows fade; the single symbol Pi remains, glowing GOLD
3. "And the picture still works. With two unknowns, Pi is a bowl over a floor. One floor direction is q one, the other is q two. The answer is the lowest point of the bowl: one point five and two point five, where Pi is minus fifty five."
   → SurfaceImage of Pi = 20 q1^2 + 10 (q2 - q1)^2 - 40 q1 - 20 q2 (k1 = 40, k2 = 20, F1 = 40, F2 = 20 N, mm); trace the q1 and q2 floor axes first; then a dot drops to the minimum (1.5, 2.5), value -55 N mm read out
4. "Second reason: it scales. For a hundred springs, you write one sum for U, one sum for W, and take derivatives mechanically. A computer can do that without ever drawing a free-body diagram. That's exactly what finite elements do."
   → a long chain of many springs scrolls past; a note "one function, many derivatives"

## S14_Four_Springs [235] The course slides' four-node example
Picture: the course slides' figure, built one spring at a time: wall with node 1 on it, k1, node 2, two springs k2 in parallel, node 3, k3, node 4, load F4.
1. "Here's an example from the course slides, built one spring at a time. Node one sits on the wall. Spring k one joins node one to node two. Spring k three joins node three to node four."
   → wall with node 1; k1 to node 2; then (leaving a gap) node 3, k3, node 4; nodes numbered in circles
2. "Between nodes two and three there are two springs, both k two, side by side. Both share the same two end points, so they stretch by the same amount, and together they store twice the energy of one. That's why you'll see two k two."
   → the parallel pair is added last; both glow; E("2\cdot\tfrac12 k_2 (q_3-q_2)^2")
3. "So U is one half k one, q two minus q one, squared, plus two times one half k two, q three minus q two, squared, plus one half k three, q four minus q three, squared."
   → E("U|=|\tfrac12 k_1(q_2-q_1)^2|+|2\cdot\tfrac12 k_2(q_3-q_2)^2|+|\tfrac12 k_3(q_4-q_3)^2") fit to width
4. "The loads are F two and F four, so W is F two q two plus F four q four. Take the partial derivative with respect to q two. It appears in two terms: k one's, and the k two pair."
   → E("W|=|F_2 q_2|+|F_4 q_4"); the two terms containing q2 highlight
5. "That gives k one times q two minus q one, minus two k two times q three minus q two, minus F two. Set it to zero and multiply out: minus k one q one, plus k one plus two k two, times q two, minus two k two q three, equals F two."
   → E("\frac{\partial\Pi}{\partial q_2}|=|k_1(q_2-q_1)|-|2k_2(q_3-q_2)|-|F_2|=|0") then the collected row
6. "Do that for every node, and you get this four by four matrix. Row two is the one we just built."
   → the 4 by 4 matrix [[k1, -k1, 0, 0], [-k1, k1 + 2k2, -2k2, 0], [0, -2k2, 2k2 + k3, -k3], [0, 0, -k3, k3]]; row 2 highlighted

## S15_Pattern [231] The pattern in the matrix
Picture: the 4 by 4 matrix with each spring's contribution shown as a colored 2 by 2 block; then the wall node removed.
1. "Look at that matrix one spring at a time, and a pattern jumps out."
   → the matrix with all entries faded
2. "A spring of stiffness k between nodes i and j puts plus k on the diagonal at i, plus k on the diagonal at j, and minus k in the two spots that connect them."
   → k1's block lights (rows/cols 1-2), then the 2k2 block (2-3), then k3's block (3-4), each in its own tint; where blocks overlap on the diagonal the entries add
3. "This is the key idea for everything that follows: each spring brings its own little two by two block, and where blocks share a node, the entries simply add." (style: slower and deliberate, stressing the key words)
   → self.spotlight on the overlapping diagonal entries k1 + 2k2 and 2k2 + k3; hold 2 s
4. "Use the pattern: pause and do checkpoint two point two in your guide, and write row three."
   → unspot; self.checkpoint("2.2", "Four-node springs: write row 3 of the stiffness matrix")
5. "Row three: minus two k two, then two k two plus k three, then minus k three. And notice: every row adds up to zero. Shift every node by the same amount, and no spring stretches, so no force is needed. That's what a zero row sum says."
   → row 3 highlighted; row sums computed to 0; the chain slides rigidly
6. "But node one is on the wall: q one is zero, and the wall supplies whatever force it needs. So its row and column don't belong in the equations we solve. Cross them out, and three equations remain, for q two, q three and q four. Our two-spring matrix was like that too: its wall node was never in it."
   → row 1 and column 1 struck out; the remaining 3 by 3 boxed; the S12 matrix appears small with a note "wall node already left out"
7. "So, stepping back: write U and W, take one partial derivative per free node, and the stiffness matrix builds itself from little blocks. Next, your first homework problem."
   → key_box(r"\text{stretch} = q_j - q_i", r"\frac{\partial \Pi}{\partial q_i} = 0\ \text{for every free node}", r"\text{each spring adds } k\begin{bmatrix}1&-1\\-1&1\end{bmatrix}", label="KEY IDEA")

# Episode 3: Homework Problem 1 | springs by the stationary principle

## S16_P1_Read [191] Reading the figure
Picture: the HW figure redrawn large: wall at left; K1 (top) from the wall to a tall vertical bar; K2 from the wall to the q1 junction, then a second spring from the junction to the bar; K3 from the bar to an outer node; loads P1 (junction), P2 and P3 (bar), P4 (outer node); SKY q1, q2, q3.
1. "Here's problem one. Use the stationary principle to find q one, q two and q three, in terms of the spring stiffnesses and the loads. Let's read the figure slowly, piece by piece."
   → the figure builds left to right; the problem statement in words at the top, then it shrinks away
2. "On the left, a wall. Along the top, spring K one runs from the wall to this tall vertical bar. The bar moves to the right by q two."
   → K1 and the bar highlight; the bar's q2 arrow appears
3. "Along the bottom, spring K two runs from the wall to a junction that moves q one. Then a second spring runs from that junction to the bar. The figure doesn't label that second spring. We'll take it to be another K two, since the label sits right between them. If your instructor says otherwise, only that one stiffness changes."
   → the bottom chain highlights; the unlabeled spring gets a dashed "K_2 (assumed)" tag in MUTED with a question mark that resolves to K_2
4. "On the right, spring K three joins the bar to an outer point that moves q three."
   → K3 and the q3 arrow highlight
5. "The loads: P one pulls the junction, P two and P three both push on the bar, and P four pulls the outer point. All to the right."
   → the four ROSE arrows pulse in turn
6. "One assumption about the bar: it's rigid and slides without tilting. So every spring attached to it moves exactly q two at that end."
   → the bar slides right as one piece; the three attachment points on it all glow SKY with the same q2

## S17_P1_Stretches [130] The stretch of every spring
Picture: the figure on the left; a four-row table on the right: spring | its two ends | stretch.
1. "Step one, the one that decides everything: the stretch of each spring. Remember, a stretch is the right end's displacement minus the left end's."
   → table header appears: spring, left end, right end, stretch
2. "K one: left end on the wall, which doesn't move, right end on the bar, which moves q two. Stretch: q two."
   → row 1: K_1 | 0 | q_2 | q_2; the spring K1 glows
3. "The first K two: wall to the junction. Stretch: q one. The second K two: junction to bar. Its left end moves q one, its right end q two. Stretch: q two minus q one."
   → rows 2 and 3, each spring glowing as its row appears
4. "K three: bar to the outer point. Stretch: q three minus q two."
   → row 4
5. "This is the step to get right, so let's say it once more: a spring between two moving points stretches by the difference of their displacements. Get these four right, and the rest is just algebra." (style: slower and deliberate, stressing the key words)
   → self.spotlight on the stretch column; hold 2 s

## S18_P1_Pi [113] Writing Pi
Picture: the table shrinks to the top left; U, W and Pi built on the right.
1. "Now the strain energy: one half, stiffness, times stretch squared, for each spring, all added up."
   → each row of the table flies into a term
2. "U equals one half K one q two squared, plus one half K two q one squared, plus one half K two, q two minus q one, squared, plus one half K three, q three minus q two, squared."
   → E("U|=|\tfrac12 K_1 q_2^2|+|\tfrac12 K_2 q_1^2|+|\tfrac12 K_2 (q_2-q_1)^2|+|\tfrac12 K_3 (q_3-q_2)^2") fit to width, two lines if needed
3. "The work potential: each load times the displacement of the point it's on. P one acts at q one. P two and P three both act on the bar, at q two. P four acts at q three."
   → E("W|=|P_1 q_1|+|(P_2+P_3)\,q_2|+|P_4 q_3"); arrows from each load in the mini figure to its term
4. "And Pi is U minus W. Three unknowns, so we'll take three partial derivatives and set each one to zero."
   → E("\Pi|=|U|-|W"); three empty slots labeled d Pi / d q1, d q2, d q3

## S19_P1_Derivs [250] Three partial derivatives
Picture: Pi in compact form at the top; the three derivative lines below, one at a time.
1. "Start with q one. It appears in two springs: the first K two, and the second K two, where it shows up inside q two minus q one."
   → the two terms containing q1 highlight in Pi
2. "The first gives K two q one. The second gives K two times q two minus q one, times minus one, from the chain rule. And the load gives minus P one."
   → E("\frac{\partial \Pi}{\partial q_1}|=|K_2 q_1|-|K_2(q_2-q_1)|-|P_1|=|0")
3. "Multiply out: K two q one, minus K two q two, plus K two q one, minus P one, equals zero. The two K two q one terms make two K two q one. So: two K two q one, minus K two q two, equals P one."
   → the expanded line E("K_2 q_1|-|K_2 q_2|+|K_2 q_1|-|P_1|=|0"); the two K2 q1 terms merge; then E("2K_2 q_1|-|K_2 q_2|=|P_1") glows
4. "Now q two. It appears in three springs and one load term. Your turn first: pause and do checkpoint three point one in your guide."
   → the three springs containing q2 highlight; then self.checkpoint("3.1", "HW 1: take the partial derivative of Pi with respect to q2")
5. "K one gives K one q two. The second K two gives plus K two times q two minus q one. K three gives K three times q three minus q two, times minus one. And the loads give minus P two plus P three."
   → E("\frac{\partial \Pi}{\partial q_2}|=|K_1 q_2|+|K_2(q_2-q_1)|-|K_3(q_3-q_2)|-|(P_2+P_3)|=|0") fit to width
6. "Multiply out and group by unknown: minus K two q one, plus K one plus K two plus K three, times q two, minus K three q three, equals P two plus P three."
   → the expanded terms regroup by q1, q2, q3 into E("-K_2 q_1|+|(K_1+K_2+K_3)\,q_2|-|K_3 q_3|=|P_2+P_3")
7. "Last, q three. Only K three and P four contain it: K three times q three minus q two, minus P four, equals zero. So minus K three q two, plus K three q three, equals P four."
   → E("\frac{\partial \Pi}{\partial q_3}|=|K_3(q_3-q_2)|-|P_4|=|0") then E("-K_3 q_2|+|K_3 q_3|=|P_4")

## S20_P1_Matrix [73] The stiffness matrix
Picture: the 3 by 3 matrix equation centered; the figure small at top left.
1. "Stack the three equations as a matrix."
   → M(r"\begin{bmatrix} 2K_2 & -K_2 & 0 \\ -K_2 & K_1+K_2+K_3 & -K_3 \\ 0 & -K_3 & K_3 \end{bmatrix} \begin{Bmatrix} q_1 \\ q_2 \\ q_3 \end{Bmatrix} = \begin{Bmatrix} P_1 \\ P_2+P_3 \\ P_4 \end{Bmatrix}")
2. "Check it against the pattern from last episode. Each spring adds plus k on the diagonal of each free node it touches, and minus k between them. Springs tied to the wall only add to one diagonal, because the wall's row and column are left out."
   → per-spring tinted overlays: K1 only on (2,2), first K2 only on (1,1), second K2 on the (1,2) block, K3 on the (2,3) block
3. "And it's symmetric: each spring puts the same minus k in both of its off-diagonal spots. Now let's solve it."
   → a mirror line along the diagonal; matching off-diagonal pairs flash

## S21_P1_Solve [265] Solving by substitution
Picture: the three equations stacked on the left; the working on the right; results boxed.
1. "Here's the plan: get rid of q three first, then q one, until one equation is left with q two alone. Look at the third equation: K three times q three minus q two equals P four."
   → a three-step plan in words; the third equation rewritten as E("K_3(q_3-q_2)|=|P_4")
2. "Add it to the second equation. The K three terms cancel, and we're left with minus K two q one, plus K one plus K two times q two, equals P two plus P three plus P four."
   → the two equations added; K3 terms struck out; the result E("-K_2 q_1|+|(K_1+K_2)\,q_2|=|P_2+P_3+P_4")
3. "That makes sense physically. It's the force balance of the bar together with the outer point: the two springs on the bar's left side, K one and the second K two, hold P two, P three and P four together."
   → a small sketch: a dashed box around the bar and the outer node; K1 and the second K2 carry the three loads
4. "From the first equation, q one equals P one plus K two q two, all over two K two."
   → E("q_1|=|\frac{P_1+K_2 q_2}{2K_2}")
5. "Substitute. Minus K two times q one is minus one half P one, minus one half K two q two."
   → E("-K_2 q_1|=|-\tfrac12 P_1|-|\tfrac12 K_2 q_2")
6. "So the q two terms are K one plus K two, minus one half K two, which is K one plus one half K two. The equation becomes: K one plus one half K two, times q two, minus one half P one, equals P two plus P three plus P four."
   → E("(K_1+K_2-\tfrac12 K_2)\,q_2|=|(K_1+\tfrac12 K_2)\,q_2") then E("(K_1+\tfrac12 K_2)\,q_2|-|\tfrac12 P_1|=|P_2+P_3+P_4")
7. "Multiply through by two and solve. q two equals P one, plus two times the sum of P two, P three and P four, all over two K one plus K two."
   → E("q_2|=|\frac{P_1+2(P_2+P_3+P_4)}{2K_1+K_2}") boxed, glowing
8. "Then q one is P one plus K two q two, over two K two, and q three is q two plus P four over K three."
   → E("q_1|=|\frac{P_1+K_2 q_2}{2K_2}") and E("q_3|=|q_2|+|\frac{P_4}{K_3}") boxed; a MUTED note: "put q2 in for a formula in the loads alone"

## S22_P1_Check [181] Does it make sense?
Picture: the three boxed answers at top; a numeric check below; the figure with forces.
1. "Never hand in a formula you haven't tested. Pick easy numbers: every spring one hundred newtons per millimeter, every load thirty newtons. Pause and do checkpoint three point two in your guide."
   → value cards; then self.checkpoint("3.2", "HW 1 check: all K = 100 N/mm, all P = 30 N")
2. "q two is thirty plus two times ninety, which is two hundred ten, over three hundred: zero point seven millimeters."
   → E("q_2|=|\frac{30 + 2(90)}{300}|=|0.7\text{ mm}") boxed
3. "q one: P one plus K two q two is thirty plus seventy, one hundred, over two hundred: zero point five. q three is zero point seven plus thirty over one hundred: one millimeter."
   → E("q_1|=|\frac{30+70}{200}|=|0.5\text{ mm}"), E("q_3|=|0.7+0.3|=|1.0\text{ mm}") boxed
4. "Now Newton, as a check. Spring K three holds only P four, so it should carry thirty newtons: one hundred times its stretch, zero point three, is thirty. Good."
   → K3 glows with 100 x 0.3 = 30 N; GOOD tick
5. "And the two springs on the wall must hold all four loads together, one hundred twenty newtons. K one carries seventy, the first K two carries fifty. Seventy plus fifty is one hundred twenty."
   → the wall springs glow with 70 N and 50 N; sum 120 = 4 x 30; GOOD tick
6. "So, stepping back: stretches, then U and W, then one derivative per unknown, then solve and check. That's the whole method. Next, we leave springs behind and look at a real bar."
   → key_box("1. stretch = right end minus left end", "2. Pi = U - W", "3. one partial derivative per unknown", "4. solve, then check with Newton", label="THE METHOD")

# Episode 4: From Springs to Bars | assumed shapes

## S23_Bar_Problem [159] A bar has infinitely many unknowns
Picture: a bar fixed to a wall at x = 0, length L, a row of small ROSE arrows f along it, a tip load P; an x axis.
1. "So far every structure had a handful of points that move. Now take a bar: fixed to a wall at the left, pulled along its length by a load spread over it, f per unit length, and a load P at the tip."
   → wall, bar from x = 0 to L, dist_load f, tip force P; the x axis below
2. "A bar like this is loaded along its axis, so it only stretches or shortens. That's what makes it a bar, as opposed to a beam, which is loaded sideways and bends."
   → the bar stretches slightly, then a small beam inset bends under a sideways load, labeled "beam: bends"
3. "Every point along the bar moves a little to the right, by an amount that depends on where it is. Call it u of x. At the wall, u is zero."
   → a SKY curve u(x) drawn above the bar from 0 to its tip value; little arrows at many points along the bar; "u(0) = 0" at the wall
4. "So how many unknowns is that? Every point has its own displacement: infinitely many. We can't list them as q one, q two, q three."
   → the arrows multiply until they form a continuous band; a label "infinitely many unknowns"
5. "Here's the plan. First, find the strain energy and work potential of a bar. Then, find a clever way to turn infinitely many unknowns into just a few."
   → two steps listed in words

## S24_Energy_Density [159] Strain energy, piece by piece
Picture: zoom on a tiny slice dx of the bar on the left; the stress-strain line on the right.
1. "To find the energy in the bar, zoom in on a tiny slice, of length d x. Inside it, the material is stretched by a strain epsilon, and carries a stress sigma."
   → camera zooms on a small slice; it stretches slightly; labels epsilon and sigma in ACCENT
2. "For an elastic material, stress and strain are related by Hooke's law: sigma equals E times epsilon. On a graph, a straight line from the origin with slope E."
   → axes epsilon horizontal, sigma vertical; the line sigma = E epsilon with slope E marked
3. "Now connect it to the spring. Stress times the slice's area A is a force. Strain times its length d x is a stretch. So this graph is just the spring's force-stretch graph, rescaled."
   → the axes relabel: sigma times A becomes force, epsilon times dx becomes stretch; a ghost of the S02 spring triangle overlays
4. "So the slice stores the area of the triangle under the line, times A d x. Per unit volume, the energy is just the triangle's area: half base times height, one half, epsilon, times E epsilon."
   → the MINT triangle under the line; E("U^*|=|\tfrac12|\,\varepsilon|\,\cdot|\,E\varepsilon|=|\tfrac12 E \varepsilon^2") step by step
5. "We'll call it U star: the strain energy per unit volume. It's the same shape as one half K q squared. Stiffness, times deformation, squared, times one half."
   → E("\tfrac12 K q^2") beside E("\tfrac12 E\varepsilon^2"); matching parts tinted alike

## S25_Bar_U [208] The strain energy of a bar
Picture: the bar on top with one slice highlighted; the formula built below.
1. "To get the whole bar's energy, add up every slice. A slice has volume A, the bar's cross-sectional area, times d x. So it stores one half E epsilon squared, times A d x."
   → the slice highlighted, its cross-section shaded and labeled A; E("dU|=|\tfrac12 E\varepsilon^2\,A\,dx")
2. "What's the strain of a slice? Its left face moves u, its right face moves u plus d u, so it grows by d u. Its length is d x. Change in length over length: d u over d x."
   → a slice with u at its left end and u + du at its right; E("\varepsilon|=|\frac{du}{dx}")
3. "Add up the slices with an integral from zero to L, and the bar's strain energy is one half, the integral of E A, times d u d x, squared, d x."
   → slices sweep along the bar; E("U|=|\tfrac12 \int_0^L E A \Big(\frac{du}{dx}\Big)^2 dx")
4. "This is the formula the whole rest of the series stands on, so let's make sure it feels familiar. Stiffness, times how much it deforms, squared, times one half. Exactly the spring's formula, spread along the bar." (style: slower and deliberate, stressing the key words)
   → self.spotlight on U = ½ ∫ EA (du/dx)^2 dx; hold 2 s
5. "In fact, if the bar stretches evenly, so its tip moves q, then d u d x is q over L everywhere, and U becomes one half, E A over L, q squared. A spring with stiffness E A over L."
   → unspot; E("\frac{du}{dx}|=|\frac{q}{L}") then E("U|=|\tfrac12|\frac{EA}{L}|q^2"); EA/L tinted LILAC and labeled "a spring's K"
6. "And if the bar just slides along without stretching, d u d x is zero, and so is U. No stretch, no stored energy."
   → the bar slides rigidly; E("U = 0")

## S26_Bar_W [107] The work potential of a bar
Picture: the bar with its loads; W built below; then Pi.
1. "The work potential is load times displacement, as always. The tip load P acts where the bar moves u of L, so it gives P times u at L."
   → tip highlighted; E("P\,u(L)")
2. "The spread-out load acts everywhere. A slice d x carries f d x, and moves u, so add up f u d x along the bar."
   → slices with tiny f arrows; E("\int_0^L f\,u\,dx")
3. "So W equals P u at L, plus the integral of f u d x. And Pi is U minus W, as before."
   → E("W|=|P\,u(L)|+|\int_0^L f\,u\,dx") then E("\Pi|=|U|-|W")
4. "But here's the problem. Pi now depends on a whole function, u of x. We can't take a partial derivative with respect to every point. We need a trick."
   → a question mark beside "d Pi / d u(x) ?"

## S27_Assume_Shape [241] The trick: assume a shape
Picture: the bar with uniform f and no tip load; the assumed straight-line shape u = a x above it; algebra on the right.
1. "Here's the trick. Guess the shape of u of x, but leave a number in it to adjust. Then Pi depends only on that number, and we're back to finding the bottom of an ordinary bowl."
   → a family of straight lines u = a x fans out from the wall as a slider for a changes
2. "Let's try it. Only the spread load f, no tip load. Assume u equals a times x. It's zero at the wall, so it respects the support. Then d u d x is just a."
   → E("u|=|a\,x"), E("\frac{du}{dx}|=|a"), the wall end flagged "u(0) = 0"
3. "U is one half, E A a squared, integrated over the length: one half E A a squared L. W is the integral of f times a x: one half f a L squared."
   → E("U|=|\tfrac12 EA\,a^2 L") and E("W|=|\int_0^L f\,a x\,dx|=|\tfrac12 f a L^2")
4. "So Pi of a is one half E A a squared L, minus one half f a L squared. A parabola in a: a bowl, just like the spring's."
   → E("\Pi(a)|=|\tfrac12 EA\,a^2 L|-|\tfrac12 f a L^2"); a small bowl over an a axis
5. "Set its derivative to zero: E A a L minus one half f L squared equals zero. So a equals f L over two E A."
   → E("\frac{d\Pi}{da}|=|EA\,a L|-|\tfrac12 f L^2|=|0") then E("a|=|\frac{fL}{2EA}") boxed
6. "Why is that the best straight line? The true shape has the lowest Pi of all. So among straight lines, the one with the lowest Pi is the one closest to the truth. Its tip moves a times L: f L squared over two E A."
   → E("u(L)|=|\frac{fL^2}{2EA}"); the tip arrow glows
7. "Pay close attention, because this is the idea finite elements are built on. Assume a shape that respects the supports, with a few unknown numbers in it, and the infinite problem becomes a small one." (style: slower and deliberate, stressing the key words)
   → self.spotlight(E("u(x) = a\,x")); hold 2 s

## S28_Compare_Exact [170] How good is the guess?
Picture: axes x from 0 to L, u vertical (units of f L^2 / EA); the exact curve and the straight-line guess.
1. "How good is that guess? This simple bar has an exact answer. Cut it at x: the piece beyond the cut carries f times L minus x, so the strain there is f times L minus x, over E A. Integrate that, and you get u of x equals f over E A, times L x minus x squared over two."
   → a cut at x with the outer piece's load f(L - x); E("\varepsilon|=|\frac{f(L-x)}{EA}") then E("u_{\text{exact}}|=|\frac{f}{EA}\Big(Lx - \frac{x^2}{2}\Big)"); the exact SKY curve drawn
2. "At the tip, the exact answer is f L squared over two E A. Exactly what our straight line gave."
   → the straight line (SKY dashed) meets the curve at the tip; both tip values side by side
3. "Your turn: pause and do checkpoint four point one in your guide. Compare the two at the middle of the bar."
   → self.checkpoint("4.1", "Assumed u = a x: compare u at the middle with exact")
4. "At the middle, the straight line gives one quarter f L squared over E A. The exact answer is three eighths. The line sits too low everywhere inside the bar. The tip matching was a lucky coincidence, not a rule."
   → at x = L/2 the gap between line and curve is marked: 1/4 vs 3/8 (units f L^2 / EA); the whole gap region shaded
5. "That's the honest truth about assumed shapes: they're approximate. A better shape gives a better answer. But choosing one good shape for a whole real structure is hard."
   → a sketch of an odd-shaped wing rib with a question mark

## S29_Beam [277] The course slides' beam example
Picture: a simply supported beam with a load P at mid-span; the assumed sine shape; algebra on the right.
1. "The course slides use the same trick on a beam, so let's see it once. A beam of length L, stiffness E I, supported at both ends, with a point load at the middle. The slides call that load W; we'll call it P, so it doesn't clash with work potential."
   → beam on two supports; ROSE arrow P at mid-span; a MUTED note "slides: W"
2. "Measure z along the beam, and let v be how far it sags, positive downward, the way the load points. Call the middle point B, and its sag v B."
   → a z axis along the beam; v measured downward; point B at mid-span with v_B
3. "Assume the sag is a sine hump: v equals v B times sine of pi z over L. It's zero at both supports, and peaks at v B in the middle. It respects the supports."
   → the sine hump drawn under the beam; zeros at the supports flagged; v_B marked
4. "For a beam, the deformation is the bending, the curvature, and the strain energy is the integral of M squared over two E I, with M equal to minus E I times v double prime. Same pattern: one half, stiffness, times deformation squared."
   → E("U|=|\int_0^L \frac{M^2}{2EI}\,dz") with a note "= ½ EI (curvature)^2, integrated"
5. "Put the sine in. Its second derivative is minus v B, pi over L squared, times the sine. Square it and integrate, and U comes out to pi to the fourth, E I, v B squared, over four L cubed."
   → E("v''|=|-v_B\frac{\pi^2}{L^2}\sin\frac{\pi z}{L}") then E("U|=|\frac{\pi^4 EI\,v_B^2}{4L^3}")
6. "Pi is that, minus P times v B. Set its derivative with respect to v B to zero: v B equals two P L cubed over pi to the fourth E I. That's zero point zero two zero five three, P L cubed over E I."
   → E("v_B|=|\frac{2PL^3}{\pi^4 EI}|\approx|0.02053\,\frac{PL^3}{EI}") boxed
7. "Beam theory's exact answer is P L cubed over forty eight E I, which is zero point zero two zero eight three. A one-line guess, within about one and a half percent."
   → E("\frac{PL^3}{48EI}|\approx|0.02083\,\frac{PL^3}{EI}"); a bar comparing the two; "1.45 percent low"

## S30_To_FEM [152] From one shape to many pieces
Picture: the bar, then the bar chopped into elements, each with its own straight-line piece of u.
1. "So assumed shapes work, but one shape for the whole structure is hard to choose, and our single straight line missed the curve inside the bar."
   → the S28 picture briefly: the straight line under the curve
2. "Here's the way out, and it's the whole idea of finite elements. Chop the bar into short pieces. In each piece, use the simplest shape there is, a straight line. The pieces join at shared points."
   → the bar splits into 4 elements (fem_bar); a broken-line SKY shape follows the exact curve closely, one straight segment per element
3. "And now the unknowns are just the displacements of those shared points: q one, q two, q three, q four. A handful of numbers again, exactly like our springs."
   → the joint displacements labeled; the broken line moves as each one is adjusted; hold
4. "Lots of short straight lines can follow any curve. And each piece is so simple that we can work out its energy once, for good."
   → elements increase to 8; the broken line hugs the curve
5. "So, stepping back: the strain energy of a bar is one half the integral of E A times strain squared. Assume a shape, and Pi becomes a bowl again. Next time: one element, worked out completely."
   → key_box(r"U = \tfrac12\int_0^L EA\Big(\frac{du}{dx}\Big)^2 dx", r"W = P\,u(L) + \int_0^L f\,u\,dx", r"\text{assume a shape} \Rightarrow \Pi \text{ depends on a few numbers}", label="KEY IDEA")

# Episode 5: One Finite Element | shape functions, stiffness and loads

## S31_Discretize [156] Elements and nodes
Picture: a cantilever bar with a tip load, chopped into 3 elements and 4 nodes; global labels q1 to q4 under the nodes.
1. "Take the bar fixed to a wall, and chop it into three pieces. Each piece is called an element. The points where they join, and the two ends, are called nodes."
   → fem_bar with 3 elements; the word "element" points at one; "node" at the joints
2. "The displacements of the nodes, q one, q two, q three, q four, are our unknowns. Just four numbers, instead of infinitely many. Each one is called a degree of freedom: a number the structure is free to choose."
   → SKY q labels under the 4 nodes; a count "4 degrees of freedom"
3. "Between the nodes, we assume the displacement is a straight line. So once we know the four node values, we know u everywhere."
   → a SKY broken line through the four node values above the bar
4. "Neighbors share a node, so the displacement can't jump: the right end of element one moves exactly as much as the left end of element two."
   → the bar explodes into 3 separate elements; at each gap, matching arrows show the end displacements are equal; then it reassembles
5. "When we study one element on its own, we'll call its two end displacements u one and u two. For element two, its u one is the bar's q two, and its u two is q three."
   → element 2 lifted out; its ends labeled u_1, u_2; arrows to the global q_2, q_3

## S32_Local_Coord [153] A coordinate inside one element
Picture: one element alone, from x1 to x2; a ruler s from 0 to 1 below it.
1. "Why can we study one element alone? The bar's energy is an integral along the bar, and an integral along the bar splits into one integral per element. Work out one element's energy, and the bar's is just the sum."
   → the U integral over [0, L] splits into three integrals over the three elements; E("U|=|U_1|+|U_2|+|U_3")
2. "So lift out one element. It starts at x one and ends at x two. Its length is l, x two minus x one."
   → element alone; x_1, x_2 marked; span with label l
3. "Measuring from the global x is clumsy, so give the element its own ruler, called s. It runs from zero at the left end to one at the right end, whatever the element's length."
   → a LIME ruler s under the element: 0, 0.25, 0.5, 0.75, 1
4. "The conversion is s equals x minus x one, over l. Halfway along the element, s is one half."
   → E("s|=|\frac{x - x_1}{l}"); a marker at the midpoint shows s = 1/2
5. "Flip it around: x equals x one plus s times l. So as s moves a tiny step d s, x moves l times that. d x equals l d s. We'll need that inside integrals."
   → E("x|=|x_1|+|s\,l") then E("dx|=|l\,ds") boxed

## S33_Shape_Functions [181] Shape functions
Picture: the element with SKY end displacements u1, u2; above it, a plot over s of the straight line from u1 to u2; then N1 and N2 drawn separately.
1. "Inside the element, we said u is a straight line. Write it as b one times s, plus b two, and choose the b's to match the ends."
   → E("u(s)|=|b_1 s|+|b_2")
2. "At s equals zero, u must be u one, so b two is u one. At s equals one, u must be u two, so b one plus b two is u two, and b one is u two minus u one."
   → the line pinned at its two ends as each condition is applied; E("b_2 = u_1"), E("b_1 = u_2 - u_1")
3. "Put them back and rearrange: u of s equals one minus s, times u one, plus s, times u two."
   → E("u(s)|=|(1-s)\,u_1|+|s\,u_2")
4. "This is the key picture of the whole method, so let's go slowly. One minus s is a ramp that is one at the left node and zero at the right. s is a ramp that is zero at the left and one at the right. They're called shape functions, N one and N two." (style: slower and deliberate, stressing the key words)
   → plots of N1 = 1 - s and N2 = s in LIME, each with its 1 and 0 marked; then self.spotlight on both plots; hold 2 s
5. "In other words, each node gets a ramp that is one at its own node and zero at the other. Multiply each ramp by its node's displacement, add, and you get the straight line between them."
   → unspot; N1 scaled by u1 plus N2 scaled by u2 add up into the straight line; E("u|=|N_1 u_1|+|N_2 u_2")

## S34_Strain [106] Strain inside an element
Picture: the element; its straight-line u; algebra.
1. "Strain is d u d x. Our u is written in s, so use the chain rule: d u d x equals d u d s, times d s d x."
   → E("\frac{du}{dx}|=|\frac{du}{ds}|\cdot|\frac{ds}{dx}")
2. "d u d s is u two minus u one: the slope of our straight line in s. And d s d x is one over l."
   → each factor computed below its spot
3. "So the strain is u two minus u one, over l. The element's change in length, over its length. Exactly what strain means."
   → E("\varepsilon|=|\frac{u_2 - u_1}{l}") boxed; the element stretches by u2 - u1
4. "Notice it doesn't depend on s at all. Inside one element, the strain is constant. Remember that; it will matter when we look at stresses."
   → the strain shown as a flat ACCENT line across the element; note "constant in each element"

## S35_Element_K [247] The element stiffness matrix
Picture: algebra in the center; a spring icon appears at the end.
1. "Now the strain energy of one element: one half, the integral of E A times strain squared, d x. Change to s: d x is l d s, and s runs from zero to one."
   → E("U_e|=|\tfrac12\int_0^1 EA\Big(\frac{u_2-u_1}{l}\Big)^2\,l\,ds")
2. "Everything inside is constant, and the integral of d s from zero to one is one. So U e is one half, E A over l, times u two minus u one, squared."
   → E("U_e|=|\tfrac12\,\frac{EA}{l}\,(u_2-u_1)^2")
3. "Pay close attention, because you've seen this before. It's a spring! An element of a bar behaves exactly like a spring with stiffness E A over l, stretched by u two minus u one." (style: slower and deliberate, stressing the key words)
   → self.spotlight on the formula; a LILAC spring morphs out of the element, labeled k = EA/l; hold 2 s
4. "Now write it with a matrix. Expand the square: u two minus u one, squared, is u one squared, minus two u one u two, plus u two squared."
   → unspot; E("(u_2-u_1)^2|=|u_1^2|-|2u_1u_2|+|u_2^2")
5. "Here's a row, times a matrix, times a column, that gives exactly that: the row u one, u two, times the matrix one, minus one, minus one, one, times the column u one, u two. Multiply it out and the same three terms appear."
   → M(r"\begin{bmatrix}u_1 & u_2\end{bmatrix}\begin{bmatrix}1&-1\\-1&1\end{bmatrix}\begin{Bmatrix}u_1\\u_2\end{Bmatrix}") then, step by step, the matrix times the column gives {u1 - u2, -u1 + u2}, then the row times that gives u1^2 - 2u1u2 + u2^2
6. "So U e is one half, the row, times E A over l times that matrix, times the column. That matrix, E A over l times one, minus one, minus one, one, is the element stiffness matrix. The same block a spring added in episode two."
   → E("U_e = \tfrac12\,[u_1\ u_2]") with M(r"\frac{EA}{l}\begin{bmatrix}1&-1\\-1&1\end{bmatrix}") and the column; the matrix boxed and labeled "element stiffness matrix k"
7. "A quick number: if E A is two million newtons and the element is five hundred millimeters long, its stiffness is four thousand newtons per millimeter."
   → E("\frac{EA}{l}|=|\frac{2\times 10^6}{500}|=|4000\text{ N/mm}")

## S36_Element_Check [60] Checking the stiffness matrix
Picture: the element stiffness matrix; a small animation of the element.
1. "Your turn: pause and do checkpoint five point one in your guide."
   → self.checkpoint("5.1", "Element stiffness: E = 70,000 N/mm2, A = 100 mm2, l = 250 mm")
2. "Seventy thousand times one hundred, over two hundred fifty: twenty eight thousand newtons per millimeter."
   → E("\frac{70{,}000 \times 100}{250}|=|28{,}000\text{ N/mm}")
3. "And a sanity check. Move both ends the same amount: the element slides without stretching. Each row of the matrix adds to zero, so that motion takes no force and stores no energy."
   → the element translates; rows of the matrix summed: 1 - 1 = 0

## S37_Load_Vector [167] The element load vector
Picture: one element with a uniform distributed load (row of ROSE arrows); algebra; then two nodal arrows.
1. "Last piece: the work potential of a spread-out load f on one element. It's the integral of f times u, d x. Put in our u and d x equals l d s."
   → E("W_e|=|\int_0^1 f\,\big[(1-s)u_1 + s\,u_2\big]\,l\,ds")
2. "Split it in two. The part multiplying u one is the integral of f times one minus s times l. Call it Q one. The part multiplying u two is the integral of f times s times l. Call it Q two."
   → E("W_e|=|u_1 Q_1|+|u_2 Q_2"); the two integrals defined beneath, each under its brace
3. "Q one and Q two together are called the element load vector. They're the forces at the two nodes that do the same work as the spread-out load."
   → the column {Q1, Q2} boxed and labeled "element load vector"
4. "Now take the common case, f constant, equal to c. The integral of one minus s from zero to one is one half, and so is the integral of s. So Q one and Q two are both c l over two."
   → E("Q_1|=|c\,l\int_0^1(1-s)\,ds|=|\frac{cl}{2}") and the same for Q2
5. "In plain words: the element carries a total load of c times l, and half of it goes to each end node."
   → the row of distributed arrows slides and collapses into two thick ROSE arrows, one at each node, each labeled cl/2

## S38_Element_Recap [105] One element, completely
Picture: the element as a LILAC spring with two nodal arrows; then a key_box.
1. "So, stepping back. An element is a short piece of bar whose displacement is a straight line between its two nodes."
   → the element with its straight-line u
2. "Its stiffness is E A over l, exactly a spring. And a uniform spread load becomes two equal forces, c l over two, one at each node."
   → the element morphs into a spring with two nodal arrows
3. "Its energy is one half u k u, minus u Q. Take a derivative for each end, and you'd get k times u equals Q: a spring equation, for one element. Next time, we join elements together, add up their energies, apply the supports, and solve a real problem."
   → E(r"\Pi_e = \tfrac12\,u^{T} k\,u - u^{T} Q") then E("k\,u|=|Q") with a MUTED note "one element alone"
4. "Here's everything about one element in one place."
   → key_box(r"u(s) = (1-s)\,u_1 + s\,u_2", r"k = \frac{EA}{l}\begin{bmatrix}1&-1\\-1&1\end{bmatrix}", r"Q_1 = Q_2 = \frac{cl}{2}\ \ (f = c)", label="ONE ELEMENT")

# Episode 6: Assembly and Solving | a column under its own weight

## S39_Column_Setup [128] A column under its own weight
Picture: a vertical column standing on the ground, x upward from the base, its weight shown as small downward ROSE arrows; then the 3-element version beside it.
1. "A flagpole stands on the ground and carries nothing but its own weight. How much does it shorten? And where inside it is the stress highest? Let's answer both with finite elements."
   → a vertical column on a hatched ground; the two questions as cards
2. "This example is from the course slides. The column has height L, fixed at its base. Measure x upward from the base."
   → x axis upward from x = 0 at the base to L at the top
3. "Its weight acts all along it, pointing down. Per unit length that's rho, times A, times g: density, times area, times gravity. Since x points up, the load is negative: f equals minus rho A g. In our element formulas, c equals minus rho A g."
   → small ROSE arrows down along the column; E("f|=|c|=|-\rho A g") with a MUTED note "density x area x gravity"
4. "Use three equal elements, each of length l equals L over three. Nodes one to four, from the base to the top. Node one sits on the ground."
   → the column split into 3 elements; nodes numbered 1 (base) to 4 (top); q1 to q4 in SKY; "l = L/3"

## S40_Assembly_K [239] Assembling the stiffness matrix
Picture: Pi as a sum; then a 4 by 4 grid with rows and columns labeled 1 to 4; three tinted 2 by 2 element blocks (element 1 GOLD tint, element 2 MINT tint, element 3 SKY tint, as in the slides) dropped onto it.
1. "First, connect this back to the bowl. The column's Pi is the sum of every element's strain energy, minus the work potential of the loads. Take a partial derivative for each node and set it to zero, just as we did for the springs in episode two."
   → E("\Pi|=|U_1+U_2+U_3|-|W"); four cards "dPi / dq_i = 0"
2. "Each element's energy is the spring formula, with stiffness E A over l. So the result is the same kind of matrix we built from springs: a stiffness matrix K, times the displacements q, equals the loads F."
   → three small 2 by 2 blocks EA/l [[1, -1], [-1, 1]] appear beside an empty 4 by 4 grid labeled 1 to 4 on rows and columns; E("Kq = F")
3. "Element one connects nodes one and two. Its local spot one-one goes to the big matrix's spot one-one, and its block fills rows and columns one and two."
   → element 1's block slides into the top-left corner; its local (1,1) entry traced to global (1,1)
4. "Element two connects nodes two and three. Its local spot one-one goes to the big matrix's spot two-two. But spot two-two is already taken by element one."
   → element 2's block slides in; its local (1,1) entry traced to global (2,2), overlapping element 1's entry there
5. "This is the key step of assembly, so watch it closely. Where two blocks land on the same spot, their entries add. One plus one gives two. Why? Because q two appears in two elements' energies, so the derivative with respect to q two picks up a term from each." (style: slower and deliberate, stressing the key words)
   → self.spotlight on entry (2,2) showing 1 + 1 -> 2, with U_1 and U_2 both lighting up; hold 2 s
6. "Element three goes into rows and columns three and four, adding at spot three-three. Everywhere no element touches, it's zero. The result: E A over l, times one, minus one, zero, zero; minus one, two, minus one, zero; zero, minus one, two, minus one; zero, zero, minus one, one."
   → unspot; element 3 lands; (3,3) becomes 1 + 1 = 2; empty cells fill with 0; the finished global matrix, tints fading to INK, boxed: "global stiffness matrix K"

## S41_Assembly_F [167] Assembling the load vector
Picture: the column with nodal arrows on the left; the load vector being assembled on the right.
1. "The loads assemble the same way. Each element carries a total weight c l, with c equal to minus rho A g, and sends half of it to each of its two nodes."
   → each element's distributed arrows collapse to two arrows c l / 2 at its nodes
2. "Your turn: pause and do checkpoint six point one in your guide, and build the load vector."
   → self.checkpoint("6.1", "Column under its own weight: assemble the load vector")
3. "Node one gets c l over two from element one. Node two is shared: c l over two from element one, plus c l over two from element two. That's c l. Node three also gets c l. Node four, at the top, only c l over two."
   → each node's arrows stack up; the vector c l / 2 times {1, 2, 2, 1} appears entry by entry
4. "And one more force: the ground pushes up on node one with a reaction R that we don't know yet. R is a force at node one like any other, so it goes in node one's entry. We include it so that row one stays a true equation we can use later."
   → an upward ROSE arrow R at the base; entry 1 becomes c l / 2 + R
5. "So K times q equals F, with four equations. But we can't solve it yet. Something's missing."
   → the full system K q = F displayed; a question mark

## S42_BC [156] Applying the support
Picture: the 4 by 4 system; row 1 and column 1 highlighted, then removed.
1. "Remember: every row of this matrix adds to zero, because sliding the whole column along stores no energy. So the bowl has a flat valley instead of a single lowest point, and the matrix has no inverse. Without its support, the column would just slide away under its weight."
   → row sums shown as 0; a bowl with a flat trough; the column, detached from the ground, slides downward rigidly; a MUTED note "no support: no single answer"
2. "What's missing is the support. The base is fixed, so q one is zero. We know it."
   → the base node pinned; E("q_1|=|0") in SKY
3. "Here's what to do, and why. Because q one is zero, everything in column one gets multiplied by zero, so we can cross out column one. And row one is the equation that contains the unknown reaction R, so we set it aside for later." (style: slower and deliberate, stressing the key words)
   → self.spotlight on row 1 and column 1; column 1 is crossed out, then row 1 slides off to the side, labeled "set aside: has R"; hold 2 s
4. "What's left is a three by three system for q two, q three and q four: E A over l, times two, minus one, zero; minus one, two, minus one; zero, minus one, one. On the right, c l over two, times two, two, one."
   → unspot; the reduced system M(r"\frac{EA}{l}\begin{bmatrix}2&-1&0\\-1&2&-1\\0&-1&1\end{bmatrix}\begin{Bmatrix}q_2\\q_3\\q_4\end{Bmatrix} = \frac{cl}{2}\begin{Bmatrix}2\\2\\1\end{Bmatrix}") boxed

## S43_Solve [180] Solving the column
Picture: the reduced system; the working; the solution; the deformed column.
1. "To keep the numbers clean, measure every q in units of c l squared over two E A. Then the system is just: two, minus one, zero; minus one, two, minus one; zero, minus one, one, times the q's, equals two, two, one."
   → the scale factor pulled out; M(r"\begin{bmatrix}2&-1&0\\-1&2&-1\\0&-1&1\end{bmatrix}\begin{Bmatrix}x_2\\x_3\\x_4\end{Bmatrix} = \begin{Bmatrix}2\\2\\1\end{Bmatrix}") with a note "q = (c l^2 / 2EA) x"
2. "The last row says minus x three plus x four equals one."
   → row 3 highlighted; E("x_4 - x_3|=|1")
3. "Add the last row to the middle row: minus x two plus x three equals three."
   → rows 2 and 3 added; E("x_3 - x_2|=|3")
4. "Add that result to the first row, and you get x two equals five. Then x three is eight, and x four is nine."
   → E("x_2|=|5"), E("x_3|=|8"), E("x_4|=|9") boxed
5. "Now put the units back. c l squared over two E A, with c equal to minus rho A g and l equal to L over three, is minus rho g L squared over eighteen E. So the q's are rho g L squared over two E, times minus five ninths, minus eight ninths, and minus one."
   → E("\frac{c l^2}{2EA}|=|-\frac{\rho g L^2}{18E}") then E("\begin{Bmatrix}q_2\\q_3\\q_4\end{Bmatrix}|=|\frac{\rho g L^2}{2E}|\begin{Bmatrix}-5/9\\-8/9\\-1\end{Bmatrix}") boxed and glowing
6. "All negative: every point sinks. The top sinks most, by rho g L squared over two E. That answers our first question: that's how much the flagpole shortens."
   → the column shortens; node arrows point down, growing toward the top; the first question card ticks

## S44_Compare_u [99] Compared with the exact answer
Picture: axes x / L horizontal, u in units of rho g L^2 / 2E vertical; the exact curve and the FEM broken line.
1. "This column has an exact answer: u of x equals rho g over E, times x squared over two minus L x. Let's plot it."
   → the exact SKY curve on axes; the formula above
2. "At x over L equal to one third, two thirds and one, it gives minus five ninths, minus eight ninths and minus one. The exact values at the nodes."
   → three dots on the curve labeled with their values
3. "Now the finite element answer: straight lines between those same node values."
   → the FEM broken line drawn on top in a lighter SKY dashed style, meeting the curve at every node
4. "For a simple bar like this, linear elements put the nodes exactly right. In other structures the nodes are close, not exact. And between the nodes, straight lines can't quite follow the curve."
   → the small gaps between line and curve inside each element highlighted

## S45_Stress [232] Stresses: a staircase
Picture: axes x / L horizontal, stress in units of rho g L vertical; the exact line and the FEM staircase.
1. "Now stress. In each element, sigma is E times strain, and the strain is the change in displacement over the length: q of the top node minus q of the bottom node, over l."
   → E("\sigma|=|E\,\frac{q_{\text{top}} - q_{\text{bottom}}}{l}")
2. "Element one: q two minus q one is minus five ninths, times rho g L squared over two E. Divide by L over three, multiply by E: minus five sixths rho g L."
   → the arithmetic one step at a time; E("\sigma_1|=|-\tfrac56\,\rho g L")
3. "Your turn: pause and do checkpoint six point two in your guide. Find the stress in element two."
   → self.checkpoint("6.2", "Column under its own weight: the stress in element 2")
4. "Element two: minus eight ninths plus five ninths is minus three ninths. The stress is minus one half rho g L. And element three, minus one sixth rho g L."
   → E("\sigma_2|=|-\tfrac12\,\rho g L"), E("\sigma_3|=|-\tfrac16\,\rho g L")
5. "Plot them. Each element's stress is a flat step, because its strain is constant. The exact stress is a straight line, from minus rho g L at the base to zero at the top."
   → the ACCENT staircase and the exact line
6. "Look closely at where they meet. At x over L equal to one sixth, the middle of element one, the exact stress is minus five sixths rho g L: exactly the step's value. Each step crosses the line right at its element's middle."
   → the three midpoints x/L = 1/6, 1/2, 5/6 flagged where they cross; the first one zoomed with -5/6 on both; hold
7. "That answers our second question: the stress is highest at the base, where the column holds up its whole weight. And stresses are rougher than displacements, because they come from the slope of the straight-line guess. More elements, finer steps."
   → the second question card ticks; a quick 6-element staircase hugging the line closer

## S46_Reaction [104] The row we set aside
Picture: the set-aside row 1 returns; the column with its base reaction.
1. "Remember row one, the one we set aside? Now that we know q two, it tells us the reaction."
   → row 1 slides back in
2. "It says E A over l, times q one minus q two, equals c l over two plus R. q one is zero, and q two we just found."
   → E("\frac{EA}{l}(q_1 - q_2)|=|\frac{cl}{2}|+|R")
3. "Put the numbers in, and R comes out to rho g A L. The ground pushes up with exactly the column's whole weight. As it must."
   → E("R|=|\rho g A L") boxed; the upward base arrow glows; a note "= the column's weight"
4. "So, stepping back: assemble the blocks, add the loads, fix the supports by removing their rows and columns, solve, then get stresses and use the removed rows for the reactions."
   → key_box("1. assemble K and F (overlaps add)", "2. remove supported rows and columns", "3. solve for the free q's", r"4. \sigma = E\,(q_b - q_a)/l;\ \ \text{removed rows give } R", label="THE FEM RECIPE")

# Episode 7: A New Example | a stepped bar and a spring

## S47_Step_Setup [158] The problem
Picture: left wall; a thick bar (element 1) then a thin bar (element 2); a LILAC spring from the thin bar's end to a right wall; load P at the step; nodes 0 to 3.
1. "Let's do a brand new problem from start to finish, with real numbers. An aluminum bar, fixed to a wall on the left, made of two pieces: a thick one, then a thin one."
   → left wall, thick element 1, thin element 2
2. "Then a spring connects the end of the thin piece to a second wall on the right. And a load of seven thousand newtons pushes right, at the step between the two pieces. The question: how does that load divide between the two walls?"
   → spring to the right wall; ROSE arrow P = 7000 N at the step; a question card "how does the load split?"
3. "The material first. Aluminum: E is seventy thousand newtons per square millimeter. The thick piece has an area of two hundred square millimeters, the thin one one hundred."
   → data card part 1: E = 70,000 N/mm2; A1 = 200 mm2; A2 = 100 mm2; hold
4. "Each piece is five hundred millimeters long. And the spring's stiffness is fourteen thousand newtons per millimeter."
   → data card part 2: l = 500 mm each; K = 14,000 N/mm; hold
5. "Number the nodes: zero at the left wall, one at the step, two at the end of the thin piece, three at the right wall. We want the displacements, the stresses, and the wall reactions."
   → nodes 0 to 3 labeled; q1, q2 in SKY under nodes 1 and 2; goals listed in words

## S48_Step_k [69] Three springs in disguise
Picture: each piece replaced by its spring, with stiffness written on it.
1. "Each piece of bar is an element, and each element is a spring with stiffness E A over l."
   → element 1 and element 2 morph into LILAC springs
2. "Thick piece: seventy thousand times two hundred, over five hundred: twenty eight thousand newtons per millimeter. Thin piece: half the area, so half the stiffness, fourteen thousand."
   → E("k_1|=|\frac{70{,}000 \times 200}{500}|=|28{,}000") and E("k_2|=|14{,}000\text{ N/mm}")
3. "And the real spring is already a spring, fourteen thousand. So the whole thing is three springs in a row, between two walls."
   → the chain: wall, 28,000, node 1, 14,000, node 2, 14,000, wall

## S49_Step_Assemble [128] Assembling four by four
Picture: a 4 by 4 grid for nodes 0 to 3; three 2 by 2 blocks dropped in.
1. "Four nodes, so a four by four matrix. Each of the three springs drops in its two by two block."
   → empty 4 by 4 grid with rows labeled 0 to 3
2. "Your turn first: pause and do checkpoint seven point one in your guide, and assemble it yourself."
   → self.checkpoint("7.1", "Stepped bar: assemble the 4 by 4 stiffness matrix")
3. "Element one, nodes zero and one: twenty eight thousand on the diagonal at zero and one, minus twenty eight thousand between them."
   → block 1 lands at rows/cols 0-1
4. "Element two, nodes one and two: fourteen thousand. At spot one-one it adds to the twenty eight thousand already there, making forty two thousand."
   → block 2 lands; (1,1) shows 28,000 + 14,000 -> 42,000
5. "The spring, nodes two and three: fourteen thousand again. At spot two-two, fourteen plus fourteen, twenty eight thousand."
   → block 3 lands; (2,2) shows 14,000 + 14,000 -> 28,000; zeros fill the rest
6. "The load vector: the reaction R zero at node zero, seven thousand at node one, nothing at node two, and the reaction R three at node three."
   → the column {R0, 7000, 0, R3} beside the matrix

## S50_Step_BC [70] Two walls, two deletions
Picture: the 4 by 4 system; rows/columns 0 and 3 crossed out; the 2 by 2 remains.
1. "Both walls are fixed, so q zero and q three are both zero. Same move as last time: cross out their columns, because they multiply zero."
   → q0 = 0 and q3 = 0 flagged; columns 0 and 3 crossed out
2. "And set their rows aside, because those rows hold the unknown reactions. We'll come back to them."
   → rows 0 and 3 slide off to the side, labeled "set aside: reactions"
3. "What's left is two by two: forty two thousand, minus fourteen thousand; minus fourteen thousand, twenty eight thousand. Times q one, q two, equals seven thousand, zero."
   → M(r"\begin{bmatrix}42{,}000 & -14{,}000\\-14{,}000 & 28{,}000\end{bmatrix}\begin{Bmatrix}q_1\\q_2\end{Bmatrix} = \begin{Bmatrix}7000\\0\end{Bmatrix}") boxed

## S51_Step_Solve [109] Solving
Picture: the 2 by 2 system; elimination step by step; the answers on the bar.
1. "Two equations. Start with the second one: minus fourteen thousand q one, plus twenty eight thousand q two, equals zero. So q one is twice q two."
   → row 2 highlighted; E("-14{,}000\,q_1|+|28{,}000\,q_2|=|0") then E("q_1|=|2\,q_2")
2. "Put that into the first: forty two thousand times two q two, minus fourteen thousand q two, equals seven thousand. That's eighty four thousand minus fourteen thousand, seventy thousand q two, equals seven thousand."
   → E("42{,}000\,(2q_2)|-|14{,}000\,q_2|=|7000") then E("70{,}000\,q_2|=|7000")
3. "So q two is zero point one millimeters, and q one, twice that, is zero point two millimeters."
   → E("q_2|=|0.1\text{ mm}") and E("q_1|=|0.2\text{ mm}") boxed
4. "Picture it. The step moves two tenths of a millimeter to the right. The end moves only one tenth. So the thin piece got shorter, and the spring got squeezed."
   → the bar deforms (exaggerated): node 1 shifts 0.2, node 2 shifts 0.1; the thin piece visibly shortens; the spring compresses; a MUTED note "displacements exaggerated"

## S52_Step_Stress [110] Stresses
Picture: the two elements, each tinted by its stress; arithmetic on the right.
1. "Stress in each element is E times its strain: the displacement of its right node minus its left node, over its length. The same formula as the column."
   → E("\sigma|=|E\,\frac{q_b - q_a}{l}") with q_b, q_a pointed at an element's right and left nodes
2. "Thick piece: seventy thousand times zero point two minus zero, over five hundred. Twenty eight newtons per square millimeter. That unit is also called a megapascal, M P a. Positive, so tension."
   → E("\sigma_1|=|70{,}000\cdot\frac{0.2 - 0}{500}|=|28\text{ N/mm}^2|=|28\text{ MPa}") with a "tension" tag
3. "Your turn: pause and do checkpoint seven point two in your guide, and find the stress in the thin piece."
   → self.checkpoint("7.2", "Stepped bar: the stress in the thin piece")
4. "Thin piece: seventy thousand times zero point one minus zero point two, over five hundred. Minus fourteen megapascals: compression. The load pulls the thick piece and pushes the thin one."
   → E("\sigma_2|=|70{,}000\cdot\frac{0.1 - 0.2}{500}|=|-14\text{ MPa}") with a "compression" tag; arrows on each piece showing pull and push

## S53_Step_Reactions [176] The reactions, and a check
Picture: the set-aside rows return; the two walls with their reaction arrows; then a sum check.
1. "Now the rows we set aside. Row zero: twenty eight thousand times q zero, minus twenty eight thousand times q one, equals R zero. That's minus twenty eight thousand times zero point two: minus fifty six hundred newtons."
   → row 0 returns; E("R_0|=|-28{,}000 \times 0.2|=|-5600\text{ N}")
2. "Row three: minus fourteen thousand times q two, equals R three. Minus fourteen hundred newtons."
   → row 3 returns; E("R_3|=|-14{,}000 \times 0.1|=|-1400\text{ N}")
3. "Pay close attention to this move, because problem two of your homework tests exactly this. The rows we set aside to solve the system are the ones that give back the wall forces." (style: slower and deliberate, stressing the key words)
   → self.spotlight on the two returned rows; hold 2 s
4. "Both reactions point left. At the left wall, the thick piece is in tension, so the wall pulls it back. At the right wall, the spring is squeezed, so the wall pushes it back."
   → unspot; two leftward ROSE arrows at the walls, one labeled "pulls", the other "pushes"
5. "Together, fifty six hundred plus fourteen hundred is seven thousand. They balance the load exactly. So four fifths of the load goes to the left wall, through the stiff thick piece, and one fifth goes right, through the softer path."
   → E("7000 - 5600 - 1400 = 0") with a GOOD tick; a bar split 4 : 1 labeled 5600 and 1400; the question card from S47 ticks
6. "So, stepping back: the same recipe as the column, now with real numbers and two supports."
   → key_box(r"q_1 = 0.2\text{ mm},\ q_2 = 0.1\text{ mm}", r"\sigma_1 = 28,\ \sigma_2 = -14\text{ MPa}", r"R_0 = -5600,\ R_3 = -1400\text{ N}", label="STEPPED BAR")

# Episode 8: Homework Problem 2 | a bar by finite elements

## S54_P2_Read [199] Reading the problem
Picture: the HW figure redrawn large: wall at left; bar of length L; leftward ROSE arrows f along the whole bar; P1 at the middle (point 1), P2 at the tip (point 2); a dashed mark at x = L/4 labeled 3.
1. "Problem two. Using at least two elements, analyze this bar. Find the global stiffness matrix and load vector, then the displacements at points one and two, then the reaction at the wall, using the constrained equation. That's the wall's row, the one we always set aside."
   → the three tasks a, b, c listed in words, with "constrained equation = the wall's row" under c; then they shrink to the top
2. "The data. E is ten thousand psi, pounds per square inch. That's far softer than any real metal, but homework uses round numbers. The area is two square inches, and the length is forty inches. So E A is twenty thousand pounds."
   → data card; E("EA|=|10{,}000 \times 2|=|20{,}000\text{ lb}")
3. "Point one is at the middle, twenty inches out, with a load P one of fifty pounds to the right. Point two is the tip, forty inches out, with P two, one hundred pounds to the right."
   → P1 and P2 arrows pulse; x = 20 and x = 40 marked
4. "And the spread load f, five pounds per inch: this is what we called c in our element formulas. Watch its direction. Its arrows point left, against x. So c equals minus five. Getting that sign wrong is the most common mistake on this problem."
   → the f arrows flash; E("f|=|c|=|-5\text{ lb/in}") with the minus sign glowing ACCENT
5. "The figure also marks a point three at a quarter of the length. The questions don't ask about it, but we'll use it at the end to learn something."
   → the dashed x = L/4 mark glows MUTED, "point 3: later"

## S55_P2_Elements [95] Two elements
Picture: the bar split at point 1 into two elements; nodes 0, 1, 2; each element's stiffness and nodal loads.
1. "Two elements, split at point one. Why there? A point load can only enter the load vector at a node, so every point load needs a node under it. Node zero at the wall, node one at the middle, node two at the tip. Each element is twenty inches long."
   → fem_bar with 2 elements; nodes 0, 1, 2 labeled; "l = 20 in"; P1 and P2 sitting on nodes 1 and 2
2. "Each element's stiffness is E A over l: twenty thousand over twenty, one thousand pounds per inch."
   → E("k|=|\frac{EA}{l}|=|\frac{20{,}000}{20}|=|1000\text{ lb/in}")
3. "Each element's share of the spread load: c l over two at each of its nodes. Minus five times twenty over two: minus fifty pounds at each end."
   → each element's arrows collapse into two leftward arrows of 50 lb; E("\frac{cl}{2}|=|\frac{(-5)(20)}{2}|=|-50\text{ lb}")

## S56_P2_Assemble [128] Part a: K and F
Picture: the 3 by 3 global matrix and load vector assembled from the two elements.
1. "Your turn first: pause and do checkpoint eight point one in your guide, and assemble K and F."
   → self.checkpoint("8.1", "HW 2: assemble the global K and F")
2. "Stiffness: two blocks of one thousand. They overlap at node one, where one plus one gives two. So K is one thousand times one, minus one, zero; minus one, two, minus one; zero, minus one, one."
   → two blocks drop in; (1,1) adds to 2; M(r"K = 1000\begin{bmatrix}1&-1&0\\-1&2&-1\\0&-1&1\end{bmatrix}\ \text{lb/in}")
3. "Loads, node by node. Node zero: minus fifty from element one, plus the reaction R. The wall node still gets its share of the spread load; the wall then has to hold it."
   → entry 0 fills: R - 50
4. "Node one: minus fifty from each element, plus P one, fifty. That's minus fifty. Node two: minus fifty from element two, plus P two, one hundred. That's fifty."
   → entries fill with their sums shown: -50 - 50 + 50 = -50; -50 + 100 = 50
5. "So F is R minus fifty, minus fifty, and fifty. That's part a."
   → M(r"F = \begin{Bmatrix} R - 50 \\ -50 \\ 50 \end{Bmatrix}\ \text{lb}") boxed beside K; a tag "part a"

## S57_P2_Solve [92] Part b: the displacements
Picture: the reduced 2 by 2 system; the solution; the bar's deformed shape.
1. "The wall holds node zero, so q zero is zero. Cross out column zero, set row zero aside, and keep the two by two."
   → column 0 crossed out; row 0 slides aside "constrained equation"; the reduced system M(r"1000\begin{bmatrix}2&-1\\-1&1\end{bmatrix}\begin{Bmatrix}q_1\\q_2\end{Bmatrix} = \begin{Bmatrix}-50\\50\end{Bmatrix}")
2. "Add the two equations. The q two terms cancel: one thousand q one equals zero. So q one is zero."
   → the rows added; E("1000\,q_1|=|0") then E("q_1|=|0") glowing
3. "Then the second equation: one thousand times q two minus zero equals fifty. So q two is zero point zero five inches."
   → E("1000\,(q_2 - 0)|=|50") then E("q_2|=|0.05\text{ in}") boxed; "part b"
4. "Wait. Point one doesn't move at all, even though a load pushes right on it? That's surprising. Hold that thought; we'll explain it in a moment."
   → a question mark over node 1

## S58_P2_Reaction [131] Part c: the reaction
Picture: the set-aside row 0 returns; the wall with its reaction arrow; then a global check.
1. "Part c asks for the reaction using the constrained equation. That's the row we set aside: row zero. Your turn: pause and do checkpoint eight point two in your guide, and find the reaction."
   → row 0 slides back; then self.checkpoint("8.2", "HW 2: find the wall reaction from the constrained row")
2. "It says: one thousand times q zero, minus one thousand times q one, equals R minus fifty. Both q's are zero, so zero equals R minus fifty."
   → E("1000\,q_0|-|1000\,q_1|=|R|-|50") then E("0|=|R|-|50")
3. "This is the step the homework is really testing, so let's say it plainly. The equation we removed to solve the system is the one that gives the reaction back. Here, R equals fifty pounds." (style: slower and deliberate, stressing the key words)
   → self.spotlight(E("R = 50\text{ lb}")); hold 2 s
4. "Positive, so the wall pushes the bar to the right, with fifty pounds. Check the whole bar: fifty, plus fifty, plus one hundred, minus the spread load, five times forty, two hundred. Zero. Balanced."
   → unspot; a rightward ROSE arrow at the wall; E("50 + 50 + 100 - 200 = 0") with a GOOD tick; "part c"

## S59_P2_Why [281] Why point one doesn't move
Picture: the bar with its internal force plotted above it; then the exact displacement vs the FEM straight lines.
1. "Now, why does point one stay put? Cut the bar anywhere. The force inside the bar at the cut, call it N, tension positive, must balance all the loads on the piece to the right of the cut."
   → a cut at some x; the loads to its right highlighted; label "N(x) = sum of loads to the right (tension +)"
2. "Cut right at the wall. To the right: fifty plus one hundred pushing right, and the whole spread load, two hundred, pulling left. One fifty minus two hundred: N is minus fifty. Compression."
   → E("N(0)|=|150|-|200|=|-50\text{ lb}")
3. "Now cut just left of point one. The spread load to the right is only one hundred now. One fifty minus one hundred: plus fifty. Tension. In between, N climbs in a straight line, and crosses zero at x equals ten."
   → E("N(20^-)|=|150|-|100|=|+50\text{ lb}"); the plot of N(x) = -50 + 5x from x = 0 to 20, crossing zero at x = 10
4. "A slice shortens or stretches by N over E A, times its length. So the change in length of the left half is the area under N, divided by E A. And look: the area below zero and the area above zero are equal triangles."
   → the two triangles under N(x), from 0 to 10 and from 10 to 20, shaded; equal and opposite, each with area 250
5. "Minus two hundred fifty plus two hundred fifty is zero. The left half shortens near the wall and stretches near the middle by exactly the same amount, so point one ends up where it started."
   → the left half deforms: its first part shortens, its second part lengthens; node 1 returns to its original spot
6. "But inside that half, the bar does move. At point three, x equals ten, the area so far is minus two hundred fifty. Divide by twenty thousand: point three moves minus zero point zero one two five inches, to the left."
   → E("u(10)|=|\frac{-250}{20{,}000}|=|-0.0125\text{ in}"); the exact u(x) curve dipping below zero on the left half
7. "Pay close attention to this last point. Our two-element model draws a straight line from zero to zero there, so it says point three doesn't move. The nodes are right, but between them the model is only approximate. More elements, and the straight lines follow the true curve." (style: slower and deliberate, stressing the key words)
   → the FEM straight line (flat at 0 on the left half) vs the curve; self.spotlight on the gap at x = 10; hold 2 s; then unspot and show a 4-element version dipping toward the curve

## S60_Recap [145] Everything in one picture
Picture: a flow of small panels: one spring bowl -> springs matrix -> bar energy -> one element -> assembly -> solve.
1. "Let's step back and look at the whole road. We started with one spring and one idea: the real displacement makes Pi, strain energy minus work potential, as small as possible."
   → panel 1: the bowl with Pi = U - W
2. "For many springs, that idea gave one equation per unknown, and a stiffness matrix built from little blocks. That's how you solved problem one."
   → panel 2: the spring chain and its block matrix
3. "For a bar, we found its strain energy, and the trick of assuming a shape. Finite elements use the simplest shape, a straight line, on many short pieces. Each piece is just a spring, E A over l."
   → panel 3: the bar chopped into elements, each morphing into a spring
4. "Then the recipe, five steps: assemble, remove the supports, solve, find the stresses, and use the removed rows for the reactions. That's how you solved problem two."
   → panel 4: the recipe as five numbered steps
5. "If you remember one thing, make it this: finite elements are the energy method, applied to a structure cut into pieces simple enough to handle." (style: slower and deliberate, stressing the key words)
   → self.spotlight on a final card E(r"\Pi = U - W \ \Rightarrow\ K q = F"); hold 2 s; a MUTED line underneath: "next in your slides: the rotated bar element, for trusses"

