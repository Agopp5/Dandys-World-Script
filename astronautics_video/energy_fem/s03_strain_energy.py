"""S03: strain energy (BRIEF.md S03)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: U = 1/2 K q^2 with K = 20 N/mm is the plotted parabola 10 q^2; zero at q = 0, growing faster and faster
K_N = 20.0
U_of = lambda q: 0.5 * K_N * q * q
assert np.isclose(U_of(1.0), 10.0) and np.isclose(U_of(5.0), 250.0) and U_of(0) == 0
assert U_of(2) - U_of(1) < U_of(3) - U_of(2) < U_of(4) - U_of(3)     # "faster and faster"
# the S02 triangle: base q, height K q, area 1/2 K q^2 = U
assert np.isclose(0.5 * 5.0 * (K_N * 5.0), U_of(5.0))


class S03_Strain_Energy(VScene):
    budget = 82

    def construct(self):
        # --- the S02 triangle, kept small at top right
        o = np.array([4.3, 1.75, 0])
        tw, th = 1.9, 1.3
        tri = Polygon(o, o + RIGHT * tw, o + RIGHT * tw + UP * th, color=MINT, stroke_width=3)
        tri.set_fill(MINT, opacity=0.35)
        base = Line(o + LEFT * .15, o + RIGHT * (tw + .25), color=AXIS, stroke_width=2)
        tq = E("q", size=32).next_to(tri, DOWN, buff=.15)
        tk = E("K|q", size=32).next_to(tri, RIGHT, buff=.15)
        tu = E("U", size=32).move_to(o + RIGHT * tw * .68 + UP * th * .27)
        tri_g = VGroup(base, tri, tq, tk, tu)

        # --- the spring at left, held stretched
        y = 2.1
        wl = wall(np.array([-6.0, y, 0]), side=LEFT)
        rest_x, str_x = -3.4, -2.1
        xt = ValueTracker(str_x)
        sp = always_redraw(lambda: spring(np.array([-6.0, y, 0]), np.array([xt.get_value(), y, 0])))
        nd = always_redraw(lambda: node(np.array([xt.get_value(), y, 0]), r=.1))
        rest_tick = DashedLine([rest_x, y - .55, 0], [rest_x, y + .55, 0], color=MUTED, stroke_width=2)
        q_arrow = Arrow([rest_x, y - .7, 0], [str_x, y - .7, 0], buff=0, color=SKY, stroke_width=4,
                        max_tip_length_to_length_ratio=.3)
        q_lab = E("q", size=32).next_to(q_arrow, DOWN, buff=.1)
        self.add(tri_g, wl, rest_tick)

        with self.say("Where does that work go? The spring is now stretched, and it's holding that energy inside. "
                      "Let it go, and it snaps back and gives the energy back.") as d:
            self.play(FadeIn(sp), FadeIn(nd), GrowArrow(q_arrow), FadeIn(q_lab), run_time=.12 * d)
            glow_line = spring(np.array([-6.0, y, 0]), np.array([str_x, y, 0])).set_color(MINT).set_stroke(width=9)
            self.play(ShowPassingFlash(glow_line, time_width=.6), run_time=.2 * d)
            self.wait(.15 * d)
            self.play(FadeOut(q_arrow), FadeOut(q_lab), xt.animate(rate_func=rush_into).set_value(rest_x - .7),
                      run_time=.1 * d)
            self.play(xt.animate(rate_func=smooth).set_value(rest_x + .45), run_time=.12 * d)
            self.play(xt.animate(rate_func=smooth).set_value(rest_x), run_time=.11 * d)
            sp_static = spring(np.array([-6.0, y, 0]), np.array([rest_x, y, 0]))
            flash = sp_static.copy().set_color(MINT).set_stroke(width=9)
            self.play(ShowPassingFlash(flash, time_width=.6), Indicate(tri, color=MINT, scale_factor=1.08),
                      run_time=.2 * d)

        # --- the name and the formula
        title = T("strain energy", size=44, color=MINT, weight=BOLD).move_to([-3.6, .45, 0])
        eq = E(r"U|=|\frac12|K|q^2", size=60).move_to([-3.6, -1.05, 0])
        paint(eq, {4: SKY})
        self.beat("Energy stored in a deformed elastic body is called strain energy. We'll call it capital U. "
                  "For a spring, U equals one half K q squared.",
                  Write(title), .2, FadeIn(eq[0], shift=UP * .2), .15,
                  [Write(eq[1:]), Indicate(tu, color=MINT)], .1, FadeIn(glow(eq[0], MINT)),
                  w=(.2, .1, .2, .05))

        # --- the parabola U(q)
        ax = axes((0, 5, 1), (0, 250, 50), width=5.2, height=3.0, xlabel="", ylabel="")
        ax.move_to([3.2, -1.6, 0])
        xl = M("q", size=40, color=SKY).next_to(ax.c2p(5, 0), RIGHT, buff=.2)
        yl = M("U", size=40, color=MINT).next_to(ax.c2p(0, 250), UP, buff=.15)
        curve = ax.plot(U_of, x_range=[0, 5], color=MINT, stroke_width=5)
        kl = TX(r"$K = 20$ N/mm", size=30, color=INK2).move_to(ax.c2p(1.45, 210))
        kl.align_to(ax.c2p(.2, 0), LEFT)
        units = T("U in N mm,  q in mm", size=30, color=MUTED).next_to(kl, DOWN, buff=.2, aligned_edge=LEFT)
        qt = ValueTracker(0)
        dot = always_redraw(lambda: Dot(ax.c2p(qt.get_value(), U_of(qt.get_value())), radius=.1, color=MINT))
        drop_line = always_redraw(lambda: Line(ax.c2p(qt.get_value(), 0),
                                               ax.c2p(qt.get_value(), U_of(qt.get_value())),
                                               color=SKY, stroke_width=3, stroke_opacity=.7))
        zero_mark = Circle(radius=.2, color=INK2, stroke_width=3).move_to(ax.c2p(0, 0))
        self.beat("Here's a picture to keep. Plot U against q. It's a parabola that opens upward: zero at q equals "
                  "zero, and growing faster and faster as you stretch.",
                  [Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(units)], .05, [Create(curve), FadeIn(kl)], [FadeIn(dot), Create(zero_mark), FadeIn(drop_line)],
                  [qt.animate(rate_func=rush_into).set_value(5)], .1,
                  w=(.17, .22, .1, .36))
        self.wipe()
