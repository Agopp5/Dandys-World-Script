"""S27: the trick: assume a shape (BRIEF.md S27)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: check the symbolic results on sample numbers (EA, L, f arbitrary)
_EA, _L, _f = 2.3, 1.7, 0.9
_x = np.linspace(0, _L, 20001)
_trap = getattr(np, "trapezoid", None) or np.trapz
def _Pi(a):
    U = _trap(0.5 * _EA * a ** 2 * np.ones_like(_x), _x)       # (1/2) int EA (du/dx)^2 dx, du/dx = a
    W = _trap(_f * a * _x, _x)                                  # int f u dx, u = a x
    assert np.isclose(U, 0.5 * _EA * a ** 2 * _L) and np.isclose(W, 0.5 * _f * a * _L ** 2)
    return U - W
_a_star = _f * _L / (2 * _EA)
_as = np.linspace(0, 2 * _a_star, 401)
assert np.isclose(_as[np.argmin([_Pi(a) for a in _as])], _a_star)                  # bottom of the bowl
assert np.isclose(_EA * _a_star * _L - 0.5 * _f * _L ** 2, 0)                       # dPi/da = 0 there
assert np.isclose(_a_star * _L, _f * _L ** 2 / (2 * _EA))                           # tip u(L) = a L
assert np.isclose(_f / _EA * (_L * _L - _L ** 2 / 2), _f * _L ** 2 / (2 * _EA))     # exact tip agrees

# figure geometry (left half): axes origin at the wall face, x = L at the bar's end
OX, OY, LW = -6.0, -1.0, 5.0
O = np.array([OX, OY, 0])
BAR_Y = -2.55
A_LO, A_HI, A_BEST = 0.12, 0.66, 0.46      # display slopes (screen units)
RX = 3.6                                   # right column centre


def slope_line(t, color=SKY, width=6):
    return Line(O, O + np.array([LW, t * LW, 0]), color=color, stroke_width=width)


class S27_Assume_Shape(VScene):
    budget = 241

    def construct(self):
        # ---- figure: u-x axes above the bar
        xax = Arrow(O + LEFT * 0.05, O + RIGHT * (LW + 0.55), buff=0, color=AXIS, stroke_width=3,
                    max_tip_length_to_length_ratio=0.05)
        uax = Arrow(O + DOWN * 0.05, O + UP * 4.0, buff=0, color=AXIS, stroke_width=3,
                    max_tip_length_to_length_ratio=0.06)
        xl = M("x", size=40).next_to(xax.get_end(), DOWN, buff=0.15)
        ul = M("u", size=40, color=SKY).next_to(uax.get_end(), RIGHT, buff=0.15)
        tick = Line(O + RIGHT * LW + UP * 0.1, O + RIGHT * LW + DOWN * 0.1, color=AXIS, stroke_width=3)
        Ll = M("L", size=40).next_to(tick, DOWN, buff=0.12)
        frame = VGroup(xax, uax, xl, ul, tick, Ll)

        fam = VGroup(*[slope_line(t, color=MUTED, width=2.5).set_stroke(opacity=0.6)
                       for t in np.linspace(A_LO, A_HI, 7)])
        tr = ValueTracker(0.3)
        live_line = always_redraw(lambda: slope_line(tr.get_value()))
        shape_lab = E(r"u|=|a\,x", size=44).move_to([-4.35, 2.15, 0])

        # slider for a
        s0, s1 = np.array([-4.3, 3.55, 0]), np.array([-1.0, 3.55, 0])
        track = Line(s0, s1, color=HAIR, stroke_width=5)
        knob = Dot(radius=0.13, color=INK)
        knob.add_updater(lambda m: m.move_to(s0 + (s1 - s0) * (tr.get_value() - A_LO) / (A_HI - A_LO)))
        a_lab = M("a", size=44).next_to(track, LEFT, buff=0.3)
        slider = VGroup(track, a_lab)

        tease = E(r"\Pi|(a)", size=64).move_to([RX, 0.6, 0])
        tease_note = T("one number to adjust", size=34, color=MUTED).next_to(tease, DOWN, buff=0.45)

        self.beat("Here's the trick. Guess the shape of u of x, but leave a number in it to adjust. Then Pi depends "
                  "only on that number, and we're back to finding the bottom of an ordinary bowl.",
                  [Create(frame), FadeIn(slider), FadeIn(knob)],
                  LaggedStart(*[Create(l) for l in fam], lag_ratio=0.15),
                  [FadeIn(live_line), Write(shape_lab)],
                  tr.animate.set_value(A_HI), tr.animate.set_value(A_LO), tr.animate.set_value(A_BEST - 0.08),
                  [FadeIn(tease), FadeIn(tease_note)],
                  w=(.12, .14, .08, .14, .14, .12, .12))

        # ---- the bar: wall, bar, spread load f (pointing +x), no tip load
        wl = wall(np.array([OX, BAR_Y, 0]), side=LEFT, h=1.5)
        br = bar(OX, OX + LW, y=BAR_Y, h=0.55)
        fl = dist_load(OX + 0.25, OX + LW - 0.75, BAR_Y + 0.62, n=7, d=RIGHT, length=0.45)
        flab = M("f", size=44, color=ROSE).next_to(fl, RIGHT, buff=0.25)
        barfig = VGroup(wl, br, fl, flab)

        e_u = E(r"u|=|a\,x", size=56).move_to([RX, 2.4, 0])
        e_du = E(r"\frac{du}{dx}|=|a", size=56).move_to([RX, 0.6, 0])
        odot = Dot(O, radius=0.11, color=SKY)
        flag = backed(M(r"u(0) = 0", size=40, color=SKY)).next_to(O, RIGHT, buff=0.25).shift(UP * 0.3)

        self.beat("Let's try it. Only the spread load f, no tip load. Assume u equals a times x. It's zero at the "
                  "wall, so it respects the support. Then d u d x is just a.",
                  [FadeOut(tease), FadeOut(tease_note)],
                  FadeIn(barfig), Indicate(flab, color=ROSE),
                  Write(e_u), [FadeIn(odot, scale=2), FadeIn(flag), Indicate(wl)],
                  Write(e_du),
                  w=(.08, .12, .1, .2, .3, .2))

        # ---- U and W
        e_U0 = E(r"U|=|\tfrac12\int_0^L EA\,a^2\,dx", size=52)
        e_U = E(r"U|=|\tfrac12 EA\,a^2 L", size=52)
        e_W = E(r"W|=|\int_0^L|f|\,a x\,dx|=|\tfrac12|f|a L^2", size=52)
        fit(e_W, 6.0, 2)
        e_U0.move_to([RX, 0.5, 0]); e_U.move_to([RX, 0.5, 0]).align_to(e_U0, LEFT)
        e_W.move_to([RX, -1.6, 0])
        with self.say("U is one half, E A a squared, integrated over the length: one half E A a squared L. W is "
                      "the integral of f times a x: one half f a L squared.") as d:
            self.play(FadeOut(e_u), e_du.animate.move_to([RX, 2.4, 0]), FadeOut(flag), run_time=.08 * d)
            self.play(Write(e_U0), Indicate(e_du[2]), run_time=.17 * d)
            self.play(*morph(e_U0, e_U, [(0, 0), (1, 1), (2, 2)]), run_time=.15 * d)
            self.play(Indicate(e_U[2], color=MINT), run_time=.1 * d)
            self.play(Write(VGroup(*e_W[:5])), Indicate(fl, color=ROSE), run_time=.25 * d)
            self.play(Write(VGroup(*e_W[5:])), run_time=.15 * d)
            self.wait(.1 * d)

        # ---- Pi(a) and the bowl
        e_Pi = E(r"\Pi|(a)|=|\tfrac12 EA\,a^2 L|-|\tfrac12|f|a L^2", size=52)
        fit(e_Pi, 6.0, 2)
        e_Pi.move_to([RX, 2.6, 0])
        bc = np.array([RX, 1.0, 0])                       # a-axis level (Pi = 0) for the bowl
        bw, bh = 4.2, 1.35                                  # Pi = a^2 - 2a on a in [-0.15, 2.15]
        b2p = lambda a: bc + np.array([(a - 1) * bw / 2.3, (a * a - 2 * a) * bh, 0])
        a_ax = Arrow(b2p(-0.2) * [1, 0, 0] + [0, bc[1], 0], [RX + 2.6, bc[1], 0], buff=0, color=AXIS,
                     stroke_width=3, max_tip_length_to_length_ratio=0.06)
        a_axl = M("a", size=40).next_to(a_ax.get_end(), DOWN, buff=0.12)
        bowl = ParametricFunction(b2p, t_range=[-0.15, 2.15], color=GOLD, stroke_width=6)
        bowl_lab = M(r"\Pi", size=44, color=GOLD).next_to(b2p(-0.15), LEFT, buff=0.15)
        bowlfig = VGroup(a_ax, a_axl, bowl, bowl_lab)

        self.beat("So Pi of a is one half E A a squared L, minus one half f a L squared. A parabola in a: a bowl, "
                  "just like the spring's.",
                  [FadeOut(e_du), Write(VGroup(e_Pi[0], e_Pi[1], e_Pi[2]))],
                  [TransformFromCopy(e_U[2], e_Pi[3]), FadeIn(e_Pi[4]),
                   TransformFromCopy(VGroup(*e_W[6:]), VGroup(*e_Pi[5:]))],
                  [FadeOut(e_U), FadeOut(e_W)],
                  Create(bowlfig),
                  w=(.2, .3, .1, .4))

        # ---- derivative, minimum
        e_d = E(r"\frac{d\Pi}{da}|=|EA\,a L|-|\tfrac12|f|L^2|=|0", size=50)
        fit(e_d, 6.0, 2)
        e_d.move_to([RX, -1.55, 0])
        e_a = E(r"a|=|\frac{fL}{2EA}", size=56).move_to([RX, -3.05, 0])
        tint(e_a[2], [((0, 1), ROSE)])
        box_a = SurroundingRectangle(e_a, color=SKY, buff=0.18, stroke_width=4)
        bot = Dot(b2p(1), radius=0.12, color=GOLD)
        tang = DashedLine(b2p(0.45) * [1, 0, 0] + [0, b2p(1)[1], 0], b2p(1.55) * [1, 0, 0] + [0, b2p(1)[1], 0],
                          color=GOLD, stroke_width=3)

        self.beat("Set its derivative to zero: E A a L minus one half f L squared equals zero. So a equals f L over "
                  "two E A.",
                  [Create(tang), FadeIn(bot, scale=2)],
                  Write(e_d),
                  [Write(e_a), Create(box_a)],
                  w=(.25, .4, .35))

        # ---- the best straight line; its tip
        tip = O + np.array([LW, 0, 0]) + (BAR_Y - OY) * UP
        tip_arr = Arrow(tip + DOWN * 0.6 + LEFT * 0.05, tip + DOWN * 0.6 + RIGHT * 0.95, buff=0, color=SKY,
                        stroke_width=6, max_tip_length_to_length_ratio=0.3)
        tip_lab = M("u(L)", size=40, color=SKY).next_to(tip_arr, DOWN, buff=0.12)
        aL_mark = always_redraw(lambda: DashedLine(O + RIGHT * LW, O + np.array([LW, tr.get_value() * LW, 0]),
                                                   color=SKY, stroke_width=3))
        aL_lab = M(r"a\,L", size=40, color=SKY).next_to(O + np.array([LW, A_BEST * LW / 2, 0]), RIGHT, buff=0.15)
        n1 = TX(r"true $u(x)$: lowest $\Pi$ of all", size=38)
        n2 = TX(r"best line: lowest $\Pi$ of the lines", size=38)
        notes = VGroup(n1, n2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        fit(notes, 6.4, 2)
        notes.move_to([RX, 0.6, 0])
        e_tip = E(r"u|(L)|=|a\,L|=|\frac{fL^2}{2EA}", size=56).move_to([RX, -1.6, 0])
        a_grp = VGroup(e_a, box_a)
        with self.say("Why is that the best straight line? The true shape has the lowest Pi of all. So among straight "
                      "lines, the one with the lowest Pi is the one closest to the truth. Its tip moves a times L: f L "
                      "squared over two E A.") as d:
            self.play(FadeOut(VGroup(e_Pi, e_d, bowlfig, tang, bot)), a_grp.animate.move_to([RX, 2.5, 0]),
                      run_time=.08 * d)
            self.play(FadeIn(n1, shift=UP * 0.2), run_time=.12 * d)
            self.play(FadeIn(n2, shift=UP * 0.2), FadeOut(fam), tr.animate.set_value(A_BEST), run_time=.2 * d)
            self.play(Indicate(live_line, color=SKY, scale_factor=1.0), run_time=.12 * d)
            self.play(Create(aL_mark), FadeIn(aL_lab), GrowArrow(tip_arr), FadeIn(tip_lab), run_time=.12 * d)
            self.play(Write(VGroup(*e_tip[:4])), run_time=.12 * d)
            self.play(Write(VGroup(*e_tip[4:])), FadeIn(glow(tip_arr, SKY)), run_time=.14 * d)
            self.wait(.1 * d)

        # ---- the idea FEM is built on
        big = E(r"u(x)|=|a\,x", size=72).move_to([RX, 1.5, 0])
        paint(big, {0: SKY})
        k1 = T("respects the supports", size=36)
        k2 = T("a few unknown numbers", size=36)
        k3 = T("infinite problem becomes a small one", size=36)
        keys = VGroup(k1, k2, k3).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        fit(keys, 6.4, 3)
        keys.move_to([RX, -1.4, 0])
        self.beat("Pay close attention, because this is the idea finite elements are built on. Assume a shape that "
                  "respects the supports, with a few unknown numbers in it, and the infinite problem becomes a small "
                  "one.",
                  [FadeOut(VGroup(notes, e_tip, a_grp)), FadeIn(big)],
                  self.spotlight(big, live_line, keys),
                  [FadeIn(k1), Indicate(odot)], [FadeIn(k2), Indicate(a_lab)], FadeIn(k3), .15,
                  w=(.12, .2, .15, .15, .15), style="slower and deliberate, stressing the key words")
        knob.clear_updaters()
        self.wipe()
