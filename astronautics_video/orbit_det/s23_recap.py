"""S23: recap, a stack of key boxes, ending on the Molniya orbit (BRIEF.md S23)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# facts
I_CRIT = np.degrees(np.arcsin(np.sqrt(4 / 5)))
assert np.isclose(I_CRIT, 63.43, atol=5e-3)
# the drawn Molniya: a = 3.0, e = 0.6 (not to scale); orientation from Example 3.1
M_OM, M_I, M_W = np.radians(145.0), np.radians(63.4), np.radians(270.0)
_C = cpn(M_OM, M_I, M_W)
assert np.allclose(_C[2], [0.5129, 0.7324, 0.4478], atol=2e-3)           # h-hat row
assert np.isclose(np.degrees(np.arccos(_C[2, 2])), 63.4, atol=1e-6)     # i = arccos C33
assert np.isclose(np.degrees(np.arctan2(_C[2, 0], -_C[2, 1])), 145.0)   # Omega = atan2(C31, -C32)
assert np.isclose(np.degrees(np.arctan2(_C[0, 2], _C[1, 2])) % 360, 270.0)  # omega = atan2(C13, C23)


def row(*parts):
    """'$tex' -> colored math at 40, anything else -> words at 30."""
    mobs = []
    for p in parts:
        if isinstance(p, str):
            mobs.append(E(p[1:], size=40) if p.startswith("$") else T(p, size=30, color=INK2))
        else:
            mobs.append(p)
    return VGroup(*mobs).arrange(RIGHT, buff=.18)


def card(n, *rows):
    body = VGroup(*rows).arrange(DOWN, buff=.14, aligned_edge=LEFT)
    return panel(VGroup(badge(n), body).arrange(RIGHT, buff=.35))


class S23_Recap(VScene):
    budget = 145

    def construct(self):
        # 1. ECI frame
        k1 = card(1, row("ECI frame:", r"$\hat I", "at the vernal equinox,", r"$\hat K", "at the North Pole"),
                  row("it does not spin with the Earth"))
        # 2. six elements
        r2a = row("$a", "size,", "$e", "shape,", r"$\theta", "where the satellite is")
        r2b = row("three turns:", r"$\Omega", "about", r"$\hat K|,", "$i", "about the node line,",
                  r"$\omega", "about", r"$\hat h")
        k2 = card(2, r2a, r2b)
        # 3. C_PN and the angles back out
        cpn_eq = E(r"C_{PN}|=|C_3(|\omega|)\,C_1(|i|)\,C_3(|\Omega|)", size=40)
        acos = E(r"i|=|\arccos C_{33}", size=40)
        at1 = E(r"\Omega|=|\operatorname{atan2}(C_{31},-C_{32})", size=40)
        at2 = E(r"\omega|=|\operatorname{atan2}(C_{13},C_{23})", size=40)
        k3 = card(3, VGroup(cpn_eq, acos).arrange(RIGHT, buff=.8), VGroup(at1, at2).arrange(RIGHT, buff=.8))
        # 4. from r and v
        r4a = row("energy", r"$\mathcal{E}", "gives", "$a|;", r"$\vec h|,\,|\vec e", "give", "$e",
                  "and the frame", r"$\hat p|,\,|\hat q|,\,|\hat h")
        r4b = row(r"$\vec r\cdot\vec v", "settles", r"$\theta|;", "the transpose", r"$C_{PN}^{T}",
                  "takes you back")
        k4 = card(4, r4a, r4b)
        # 5. J2
        dots = E(r"\dot\Omega|,\;|\dot\omega", size=40)
        paint(dots, {0: SKY, 2: MINT})
        r5b = row("except at the critical inclination", r"$i|=|63.4^\circ", ", where", r"$\dot\omega|=|0")
        paint(r5b[3], {0: MINT})
        k5 = card(5, row("Earth's bulge slowly turns the node and the perigee", dots), r5b)

        boxes = [k1, k2, k3, k4, k5]
        stack = VGroup(*boxes).arrange(DOWN, buff=.14, aligned_edge=LEFT)
        stack.shift(-VGroup(*boxes[:4]).get_center())   # four boxes fit at full size; box 5 scrolls box 1 off
        lift = (k1.get_top() - k2.get_top())[1] * UP
        k5.shift(lift)

        def add(k, j):
            dim = [boxes[m].animate.set_opacity(.5) for m in range(j)]
            return [FadeIn(k, shift=.2 * UP)] + dim

        self.beat("Let's recap. The E C I frame points I at the vernal equinox and K at the North Pole, "
                  "and it doesn't spin with the Earth.", add(k1, 0))
        syms = [r2b[1], r2b[5], r2b[7]]
        self.beat("Six elements place any orbit: a and e for size and shape, three turns for orientation, "
                  "capital Omega about K, i about the node line, little omega about h, and theta for where "
                  "the satellite is.", add(k2, 1), .05, Indicate(VGroup(r2a[0], r2a[2]), scale_factor=1.3),
                  LaggedStart(*[Indicate(s, scale_factor=1.4) for s in syms], lag_ratio=.5),
                  Indicate(r2a[4], scale_factor=1.4), w=(.15, .15, .5, .15))
        self.beat("Those three turns are the rows of C P N, C three of omega, C one of i, C three of Omega. "
                  "The angles come back out with an arc cosine and two atan twos.",
                  add(k3, 2), Circumscribe(cpn_eq, color=ACCENT), .1,
                  LaggedStart(*[Indicate(m) for m in (acos, at1, at2)], lag_ratio=.5), w=(.15, .3, .45))
        self.beat("From r and v: energy gives a, h and the eccentricity vector give e and the frame, "
                  "and r dot v settles theta. The transpose takes you back.",
                  add(k4, 3), Indicate(r4a[1]), Indicate(r4a[5]), Indicate(r4b[0]), Indicate(r4b[4]),
                  w=(.15, .2, .25, .2, .2))

        # the closing picture: the Molniya orbit (drawn a = 3, e = 0.6, not to scale), perigee frozen
        view = View(elev=16, azim=20, scale=0.85, center=(-3.0, -1.6))
        earth = globe(view)
        f = orbit(3.0, 0.6, M_OM, M_I, M_W)
        orb = curve(view, f, 0, 2 * np.pi, INK, width=5, R=1.0)
        kax = arrow3(view, (0, 0, 0), (0, 0, 2.2), INK2)
        klab = label3(view, r"\hat K", (0, 0, 2.5), INK2, 40)
        peri = dot3(view, f(0.0), ROSE)
        plab = T("perigee", size=30, color=ROSE).next_to(peri, RIGHT, buff=.25)
        side = VGroup(T("Molniya", size=40, weight=BOLD),
                      E(r"i|=|63.4^\circ", size=48),
                      VGroup(E(r"\dot\omega|\approx|0", size=44), T("perigee frozen", size=30, color=INK2))
                      .arrange(RIGHT, buff=.3)).arrange(DOWN, buff=.45)
        paint(side[2][0], {0: MINT})
        place(side, "right")
        with self.say("And Earth's bulge slowly turns the node and the perigee, except at the critical "
                      "inclination, where the perigee stands still.") as d:
            self.play(FadeOut(k1), FadeIn(k5, shift=.2 * UP),
                      *[boxes[m].animate.shift(lift).set_opacity(.5) for m in (1, 2, 3)], run_time=.2 * d)
            self.play(Indicate(r5b[1]), run_time=.25 * d)
            self.snap("key line 5")
            self.play(FadeOut(VGroup(*boxes[1:])), FadeIn(earth), FadeIn(side), FadeIn(kax), FadeIn(klab), run_time=.2 * d)
            self.play(grow(orb), run_time=.25 * d)
            self.play(FadeIn(peri), FadeIn(plab), run_time=.1 * d)
        self.wait(1.5)
        self.wipe()
