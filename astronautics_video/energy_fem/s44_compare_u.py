"""S44: FEM displacement of the column compared with the exact answer (BRIEF.md S44)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# ---- facts ----------------------------------------------------------------------------------------
# exact: u = (rho g / E)(x^2/2 - L x) = (rho g L^2 / 2E) * xi (xi - 2), xi = x / L
def ue(xi):
    return xi * (xi - 2.0)

rgE, Lc = 0.37, 2.3          # arbitrary rho g / E and L: check the normalisation
for xi in (0.2, 0.5, 0.9):
    x = xi * Lc
    assert np.isclose(rgE * (x ** 2 / 2 - Lc * x), rgE * Lc ** 2 / 2 * ue(xi))
XS = [1 / 3, 2 / 3, 1.0]
VALS = [-5 / 9, -8 / 9, -1.0]
for xi, v in zip(XS, VALS):
    assert np.isclose(ue(xi), v)
# FEM: (EA/l)[[2,-1,0],[-1,2,-1],[0,-1,1]] q = (c l / 2){2,2,1}, c = -rho A g, l = L/3
# -> q = (c l^2 / 2EA) K^-1 {2,2,1} = -(1/9)(rho g L^2 / 2E) K^-1 {2,2,1}
Kr = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 1]], float)
qfem = -np.linalg.solve(Kr, [2, 2, 1]) / 9
assert np.allclose(qfem, VALS)      # FEM nodes equal the exact values here
# largest gap between chord and parabola in an element: h^2/8 * |u''| = (1/9)/8 * 2 = 1/36 (small)
gap = max(((ue(a) + (ue(b) - ue(a)) * (t - a) / (b - a)) - ue(t))
          for a, b in zip([0] + XS[:-1], XS) for t in np.linspace(a, b, 2001))
assert np.isclose(gap, 1 / 36, rtol=1e-4)

FEMC = interpolate_color(SKY, WHITE, 0.5)


class S44_Compare_u(VScene):
    budget = 99

    def construct(self):
        # ---- formula and axes --------------------------------------------------------------------
        eq = E(r"u|(x)|=|\frac{\rho g}{E}|\Big(\frac{x^2}{2} - L x\Big)", size=52)
        eq.to_edge(UP, buff=0.3)

        ax = Axes(x_range=[0, 1.1, 1 / 3], y_range=[-1.2, 0.1, 0.1], x_length=10.2, y_length=4.8,
                  axis_config={"color": AXIS, "include_tip": False, "stroke_width": 3},
                  y_axis_config={"include_ticks": False})
        ax.shift(RIGHT * 0.9 + (1.45 - ax.c2p(0, 0)[1]) * UP)
        xt = VGroup(*[M(s, size=36, color=INK2).next_to(ax.c2p(x, 0), UP, buff=0.15)
                      for s, x in [("0", 0), (r"\frac{1}{3}", 1 / 3), (r"\frac{2}{3}", 2 / 3), ("1", 1)]])
        xt[0].next_to(ax.c2p(0, 0), UL, buff=0.12)
        xl = M(r"x / L", size=40, color=INK).next_to(ax.c2p(1.1, 0), DOWN, buff=0.25)
        yl = E(r"u|\,\big/\,|\frac{\rho g L^2}{2E}", size=40)
        fit(yl, 2.5, 1.2)
        yl.next_to(ax.c2p(0, -0.6), LEFT, buff=0.2)
        frame_mobs = VGroup(ax, xt, xl, yl)

        curve = ax.plot(ue, x_range=[0, 1], color=SKY, stroke_width=6)

        self.beat("This column has an exact answer: u of x equals rho g over E, times x squared over two minus L x. Let's plot it.",
                  Write(eq), [Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl)], Create(curve), .1,
                  w=(.4, .2, .25, .15))

        # ---- node values ---------------------------------------------------------------------------
        dots, guides, labs = VGroup(), VGroup(), VGroup()
        for xi, v, s in zip(XS, VALS, [r"-\frac{5}{9}", r"-\frac{8}{9}", "-1"]):
            d = Dot(ax.c2p(xi, v), radius=0.1, color=SKY).set_z_index(5)
            g = DashedLine(ax.c2p(xi, 0), ax.c2p(xi, v), color=MUTED, stroke_width=2, dash_length=0.08)
            lab = M(s, size=40, color=SKY).next_to(d, DL, buff=0.12)
            dots.add(d); guides.add(g); labs.add(lab)
        labs[2].next_to(dots[2], DOWN, buff=0.15)

        self.beat("At x over L equal to one third, two thirds and one, it gives minus five ninths, minus eight ninths and minus one. The exact values at the nodes.",
                  *[[Create(guides[i]), GrowFromCenter(dots[i]), FadeIn(labs[i], shift=0.2 * DOWN)] for i in range(3)],
                  .2, w=(.27, .27, .26, .2))

        # ---- FEM broken line -----------------------------------------------------------------------
        pts = [ax.c2p(0, 0)] + [ax.c2p(x, v) for x, v in zip(XS, VALS)]
        poly = VMobject().set_points_as_corners(pts)
        fem = DashedVMobject(poly, num_dashes=45).set_stroke(FEMC, width=5).set_z_index(3)

        sw_e = Line(ORIGIN, RIGHT * 0.9, color=SKY, stroke_width=6)
        sw_f = DashedLine(ORIGIN, RIGHT * 0.9, color=FEMC, stroke_width=5, dash_length=0.12)
        legend = VGroup(
            VGroup(sw_e, T("exact", size=36, color=INK)).arrange(RIGHT, buff=0.25),
            VGroup(sw_f, T("finite elements", size=36, color=INK)).arrange(RIGHT, buff=0.25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        legend.move_to(ax.c2p(0.74, -0.28)).align_to(ax.c2p(0.7, 0), LEFT)

        self.beat("Now the finite element answer: straight lines between those same node values.",
                  Create(fem), FadeIn(legend), .2, w=(.55, .25, .2))

        # ---- nodes exact, interior gaps ------------------------------------------------------------
        rings = VGroup(*[Circle(radius=0.24, color=GOOD, stroke_width=5).move_to(d) for d in dots])
        note1 = T("nodes: exact here", size=32, color=GOOD)
        note2 = VGroup(T("other structures:", size=32, color=MUTED),
                       T("close, not exact", size=32, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        notes = VGroup(note1, note2).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        notes.move_to(ax.c2p(0.03, -1.0)).align_to(ax.c2p(0.04, 0), LEFT)

        gaps = VGroup()
        for a, b in zip([0] + XS[:-1], XS):
            cpts = [ax.c2p(t, ue(t)) for t in np.linspace(a, b, 40)]
            gaps.add(Polygon(*cpts, color=BAD, stroke_width=0, fill_color=BAD, fill_opacity=0.55))
        gaps.set_z_index(1)
        focus = ax.c2p(0.5, (ue(1 / 3) + ue(2 / 3)) / 2 - 0.01)

        with self.say("For a simple bar like this, linear elements put the nodes exactly right. In other structures the nodes are close, not exact. And between the nodes, straight lines can't quite follow the curve.") as d:
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.3), FadeIn(note1), run_time=.15 * d)
            self.wait(.13 * d)
            self.play(FadeIn(note2), run_time=.1 * d)
            self.wait(.14 * d)
            self.play(FadeIn(gaps), run_time=.1 * d)
            self.play(self.camera.frame.animate.scale(0.32).move_to(focus), run_time=.2 * d)
            self.wait(.18 * d)
        self.wipe()
