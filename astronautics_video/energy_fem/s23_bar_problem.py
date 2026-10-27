"""S23: a bar has infinitely many unknowns (BRIEF.md S23)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the drawn u(x) is the exact shape of a uniform bar, fixed at x = 0, uniform f along +x and a tip load
# P = f L / 2 (illustrative ratio). In units of f L^2 / EA with xi = x / L:  u = 1.5 xi - 0.5 xi^2.
def ushape(xi):
    return 1.5 * xi - 0.5 * xi ** 2

def ushape_n(xi):                 # normalized so the tip value is 1
    return ushape(xi) / ushape(1.0)

assert np.isclose(ushape(0.0), 0.0)                       # u(0) = 0 at the wall
assert np.isclose(-1.0 + 1.0, 0.0)                        # EA u'' + f = 0: u'' = -1 (units f / EA)
assert np.isclose(1.5 - 1.0, 0.5)                         # EA u'(L) = P = f L / 2
assert np.all(np.diff(ushape(np.linspace(0, 1, 201))) > 0)  # every point moves right, more further out

X0, X1 = -5.0, 5.0        # bar ends on screen (x = 0 and x = L)
YB, BH = -0.9, 0.62       # bar centre line and height
Y0, HU = 0.05, 2.45       # u(x) plot: baseline and height of the tip value
YA = -2.35                # x axis


def cx(xi):
    return X0 + (X1 - X0) * xi


def cy(xi):
    return Y0 + HU * ushape_n(xi)


def stems(n, width=3.5):
    return VGroup(*[Line([cx(t), Y0, 0], [cx(t), cy(t), 0], color=SKY, stroke_width=width)
                    for t in np.linspace(0, 1, n + 1)[1:]])


class S23_Bar_Problem(VScene):
    budget = 159

    def construct(self):
        # ---- beat 1: the bar, its loads, the x axis
        wl = wall([X0, YB, 0], side=LEFT, h=2.0)
        barr = bar(X0, X1, y=YB, h=BH)
        dl = dist_load(X0 + 0.35, X1 - 0.35, YB, n=9, d=RIGHT, length=0.5)
        flab = E("f", size=48).next_to(barr, UP, buff=0.18).shift(LEFT * 3.4)
        barg = VGroup(barr, dl, flab)
        parr = force([X1, YB, 0], d=RIGHT, length=1.3)
        plab = E("P", size=48).next_to(parr, UP, buff=0.12)
        pg = VGroup(parr, plab)
        xax = Arrow([X0 - 0.2, YA, 0], [X1 + 1.6, YA, 0], buff=0, color=AXIS, stroke_width=4)
        t0 = Line([X0, YA - 0.12, 0], [X0, YA + 0.12, 0], color=AXIS, stroke_width=4)
        tL = Line([X1, YA - 0.12, 0], [X1, YA + 0.12, 0], color=AXIS, stroke_width=4)
        l0 = M("0", size=40).next_to(t0, DOWN, buff=0.12)
        lL = M("L", size=40).next_to(tL, DOWN, buff=0.12)
        lx = M("x", size=44).next_to(xax.get_end(), UP, buff=0.12)
        axg = VGroup(xax, t0, tL, l0, lL, lx)
        self.beat("So far every structure had a handful of points that move. Now take a bar: fixed to a wall at the "
                  "left, pulled along its length by a load spread over it, f per unit length, and a load P at the tip.",
                  [FadeIn(wl), FadeIn(barr)], Create(axg), .1, [FadeIn(dl, lag_ratio=.2), FadeIn(flab)],
                  [FadeIn(parr, shift=RIGHT * .3), FadeIn(plab)], w=(.25, .15, .25, .25))

        # ---- beat 2: a bar stretches; a beam bends
        bl = T("bar: stretches", size=40, color=INK).move_to([-3.3, 2.75, 0])
        ba, bb = np.array([1.6, 2.85, 0]), np.array([5.6, 2.85, 0])
        beam = Line(ba, bb, color=INK2, stroke_width=12)
        sups = VGroup(*[Triangle(color=INK2, stroke_width=4).scale(0.2).next_to(p, DOWN, buff=0.06)
                        for p in (ba, bb)])
        bent = ArcBetweenPoints(ba, bb, angle=0.6, color=INK2, stroke_width=12)
        mid = (ba + bb) / 2
        bload = Arrow(mid + UP * 1.05, mid + UP * 0.08, buff=0, color=ROSE, stroke_width=6)
        bload_bent = Arrow(mid + UP * 0.77, mid + DOWN * 0.2, buff=0, color=ROSE, stroke_width=6)
        beaml = T("beam: bends", size=40, color=INK).move_to([3.6, 1.55, 0])
        with self.say("A bar like this is loaded along its axis, so it only stretches or shortens. That's what makes "
                      "it a bar, as opposed to a beam, which is loaded sideways and bends.") as d:
            self.play(barg.animate(rate_func=there_and_back).stretch(1.06, 0, about_edge=LEFT),
                      pg.animate(rate_func=there_and_back).shift(RIGHT * 0.6), FadeIn(bl), run_time=.35 * d)
            self.play(FadeIn(beam), FadeIn(sups), run_time=.12 * d)
            self.play(GrowArrow(bload), run_time=.1 * d)
            self.play(Transform(beam, bent), Transform(bload, bload_bent), FadeIn(beaml), run_time=.2 * d)
            self.wait(.23 * d)
        self.drop(bl, beam, sups, bload, beaml)

        # ---- beat 3: u(x), arrows at many points, u(0) = 0
        base = DashedLine([X0, Y0, 0], [X1, Y0, 0], color=MUTED, stroke_width=3)
        curve = ParametricFunction(lambda t: np.array([cx(t), cy(t), 0]), t_range=[0, 1], color=SKY,
                                   stroke_width=7)
        ulab = E("u|(x)", size=48).next_to(curve.get_end(), RIGHT, buff=0.15)
        ulab[1].set_color(SKY)
        st8 = stems(8)
        arrs = VGroup()
        for t in np.linspace(0, 1, 9)[1:]:
            p = np.array([cx(t), YB - BH / 2 - 0.42, 0])
            arrs.add(Arrow(p, p + RIGHT * 0.95 * ushape_n(t), buff=0, color=SKY, stroke_width=5,
                           max_tip_length_to_length_ratio=.4, max_stroke_width_to_length_ratio=12))
        dots = VGroup(*[Dot([cx(t), YB, 0], radius=0.07, color=SKY) for t in np.linspace(0, 1, 9)[1:]])
        wdot = Dot([X0, Y0, 0], radius=0.1, color=SKY)
        u0 = E("u|(0)|=|0", size=44).next_to(wdot, UP, buff=0.35).shift(RIGHT * 0.55)
        u0[0].set_color(SKY)
        self.beat("Every point along the bar moves a little to the right, by an amount that depends on where it is. "
                  "Call it u of x. At the wall, u is zero.",
                  [FadeIn(dots), LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=.15)], .05,
                  [Create(base), Create(curve), LaggedStart(*[Create(s) for s in st8], lag_ratio=.1)],
                  FadeIn(ulab), [FadeIn(wdot), FadeIn(u0)], w=(.3, .3, .12, .23))

        # ---- beat 4: the arrows multiply into a continuous band
        s16, s32, s64 = stems(16), stems(32), stems(64, width=3)
        pts = [[cx(t), cy(t), 0] for t in np.linspace(0, 1, 120)] + [[X1, Y0, 0], [X0, Y0, 0]]
        band = Polygon(*pts, stroke_width=0, fill_color=SKY, fill_opacity=0.45)
        ql = E(r"q_1|,\ |q_2|,\ |q_3|,\ |\dots", size=52).move_to([-3.4, 3.25, 0])
        qx = strike(ql)
        inf = T("infinitely many unknowns", size=42, color=INK).move_to([-2.2, 2.0, 0])
        with self.say("So how many unknowns is that? Every point has its own displacement: infinitely many. We can't "
                      "list them as q one, q two, q three.") as d:
            self.play(FadeOut(st8), FadeIn(s16), run_time=.1 * d)
            self.play(FadeOut(s16), FadeIn(s32), FadeOut(arrs), FadeOut(dots), run_time=.1 * d)
            self.play(FadeOut(s32), FadeIn(s64), run_time=.1 * d)
            self.play(FadeOut(s64), FadeIn(band), run_time=.12 * d)
            self.play(FadeIn(backed(inf)), run_time=.12 * d)
            self.play(Write(ql), run_time=.16 * d)
            self.play(Create(qx), run_time=.1 * d)
            self.wait(.2 * d)

        # ---- beat 5: the plan
        self.drop(base, curve, ulab, band, wdot, u0, ql, qx, inf)
        fig = VGroup(wl, barr, dl, flab, pg, axg)
        r1 = VGroup(badge(1), T("Find the strain energy", size=40), E("U", size=52),
                    T("and work potential", size=40), E("W", size=52), T("of a bar", size=40)
                    ).arrange(RIGHT, buff=0.22)
        r2 = VGroup(badge(2), T("Turn infinitely many unknowns into just a few", size=40)).arrange(RIGHT, buff=0.22)
        rows = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        fit(rows, 13.4, 3)
        rows.move_to([0, -1.35, 0])
        self.beat("Here's the plan. First, find the strain energy and work potential of a bar. Then, find a clever "
                  "way to turn infinitely many unknowns into just a few.",
                  fig.animate.scale(0.62).move_to([0, 2.1, 0]), FadeIn(r1, shift=UP * .2), .15,
                  FadeIn(r2, shift=UP * .2), w=(.15, .3, .4))
        self.wipe()
