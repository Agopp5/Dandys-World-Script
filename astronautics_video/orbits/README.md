# AERSP 309: Two-Body Orbital Mechanics (12 videos)

The same step-by-step style as the kinematics lessons. Parts 1–7 build the ideas slowly,
with every algebra step on screen and a grey note saying *why* each step is allowed.
Parts 8–9 work the assigned textbook problems, and parts 10–12 work HW 3. Each of the
HW videos introduces the one new tool its problem needs.

Sources: the 9/18–10/9 lecture notes (`Aersp 309.pdf`), Kluever, *Space Flight Dynamics*,
Ch. 2 (plus §3.3 for the orbital elements and §4.2 for Kepler's equation), and `309_HW3_FL26.pdf`.

| Part | Video | What it covers |
|---|---|---|
| 1 | `part1_keplers_laws` | Kepler's three laws (string ellipse, equal-area wedges, the $T^2 \propto a^3$ line); the rotating polar frame, $\dot{\hat e}_r = \dot\theta\hat e_\theta$; $\vec v = \dot r\hat e_r + r\dot\theta\hat e_\theta$; equal areas $\Rightarrow \vec r\times\vec v$ constant $\Rightarrow$ central force |
| 2 | `part2_inverse_square_and_two_body` | polar acceleration; $u = 1/r$ and $f = -h^2u^2(u''+u)$; ellipse $\Rightarrow$ inverse square; Kepler III $\Rightarrow \mu$; the two-body problem, $\mu = G(M+m)$ |
| 3 | `part3_constants_of_motion` | $\vec h$ constant, planar orbits (3D), $h = rv\cos\gamma = r_pv_p$; energy $v^2/2 - \mu/r$ derived line by line; the potential well |
| 4 | `part4_orbit_equation_and_conics` | the eccentricity vector derivation; $r = p/(1+e\cos\theta)$; $\vec e$ points to periapsis; slicing a cone; sweeping $e$; focus–directrix |
| 5 | `part5_ellipse_energy_period` | $p = a(1-e^2)$, $r_{p,a}$, $c = ae$, $b$; nomenclature; $\mathcal E = -\mu/2a$; vis-viva; circular and escape speeds (launch animation); $T = 2\pi\sqrt{a^3/\mu}$ |
| 6 | `part6_velocity_on_the_orbit` | perifocal and orbital frames, $C^{\mathcal{OP}} = C_3(\theta)$; $v_r$, $v_\theta$; flight-path angle; the hodograph; $\dot\theta$ |
| 7 | `part7_parabolas_and_hyperbolas` | $\gamma = \theta/2$ on a parabola; $a < 0$; $\theta_\infty$, $v_\infty$, turning angle $\sin(\delta/2) = 1/e$; the four conics |
| 8 | `part8_examples_closed_orbits` | **HW 3 P3** (all three identities); textbook **2.16, 2.17, 2.28, 2.32** |
| 9 | `part9_examples_escape_trajectories` | textbook **2.19, 2.20, 2.21, 2.22, 2.42** |
| 10 | `part10_hw3_p1_velocity_frame` | **HW 3 P1**: $C^{\mathcal{VO}} = C_3(-\beta)$ with $\beta = \gamma$; $\omega^{\mathcal V/\mathcal P}$ and $\alpha^{\mathcal V/\mathcal P}$ in $e, f$ |
| 11 | `part11_hw3_p2_keplers_equation` | auxiliary circle $\Rightarrow r = a(1-e\cos E)$ and Kepler's equation; **HW 3 P2**: about 100 days inside 1 AU |
| 12 | `part12_hw3_p4_orbital_elements` | $i, \Omega, \omega, u$ in 3D, the 3-1-3 sequence; **HW 3 P4**: $a = 3R_e$, $e = 0.2$, $i = 30^\circ$, $\Omega = 45^\circ$, $\omega = 345^\circ$, $f_1 = 320^\circ$, $f_2 = 85.6^\circ$ |

All numbers were checked in Python. Textbook problems use $\mu_\oplus = 3.986\times10^5$
km³/s² and $R_\oplus = 6378$ km, as the chapter says. Moon and Jupiter values are from
Appendix A.

**Notes**

- **HW 3 P3:** the sheet prints $p = 2r_pr_a/(r_p + r_a + a)$. The extra $+a$ looks like a
  typo; the correct form is $2r_pr_a/(r_p + r_a)$. A circle ($r_p = r_a = r$) must give $p = r$.
- **HW 3 P4:** this assumes the satellite goes from $\vec r_1$ to $\vec r_2$ the short way
  ($\Delta f < 180^\circ$). "Ascending/descending" is answered by the sign of the flight-path angle:
  $f_1 = 320^\circ$ is descending and $f_2 = 85.6^\circ$ is ascending. In latitude, both points are
  northbound.

## Rebuilding

From `astronautics_video/`:

```bash
export OPENROUTER_API_KEY=sk-or-...      # never commit this
python tts.py --project orbits           # narration -> orbits/audio
cd orbits && python render.py            # -> orbits/output/part<N>_*_1080p30.mp4
python render.py --only 10 11            # re-render specific parts
```
