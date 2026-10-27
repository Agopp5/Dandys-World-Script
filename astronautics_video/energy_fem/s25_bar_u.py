"""S25: the strain energy of a bar (BRIEF.md S25)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts
# strain energy density: integral of E eps d eps from 0 to eps = 1/2 E eps^2 (triangle)
_E, _eps = 70000.0, 1e-3
_e = np.linspace(0, _eps, 2001)
assert np.isclose(np.trapezoid(_E * _e, _e), 0.5 * _E * _eps ** 2)
# uniform stretch u = q x / L: du/dx = q/L everywhere, U = 1/2 int_0^L EA (q/L)^2 dx = 1/2 (EA/L) q^2
_EA, _L, _q = 2e6, 1000.0, 0.3
_x = np.linspace(0, _L, 2001)
_dudx = np.gradient(_q * _x / _L, _x)
assert np.allclose(_dudx, _q / _L)
assert np.isclose(0.5 * np.trapezoid(_EA * _dudx ** 2, _x), 0.5 * _EA / _L * _q ** 2)
# rigid slide u = c: du/dx = 0, U = 0
assert np.isclose(0.5 * np.trapezoid(_EA * np.gradient(0 * _x + 0.4, _x) ** 2, _x), 0.0)

LAB = 44   # figure labels
EQ = 58    # main equations

X0, X1, Y, H = -5.6, 4.9, 1.6, 1.3     # the bar
NS = 12                                  # slices
DX = (X1 - X0) / NS
STR = (X1 - X0 + 0.7) / (X1 - X0)        # even stretch: tip moves 0.7 on screen


class S25_Bar_U(VScene):
    budget = 208

    def construct(self):
        # ---- the bar and one slice ------------------------------------------------------------
        w = wall(np.array([X0, Y, 0]), side=LEFT, h=2.2)
        b = bar(X0, X1, y=Y, h=H)
        k = 6
        xl, xr = X0 + k * DX, X0 + (k + 1) * DX
        sl = Rectangle(width=DX, height=H).move_to([(xl + xr) / 2, Y, 0])
        sl.set_fill(MINT, .55).set_stroke(MINT, 3)
        cross = Ellipse(width=.42, height=H).move_to([xr, Y, 0])
        cross.set_fill(MINT, .9).set_stroke(INK, 2)
        a_lab = M("A", size=LAB).next_to(cross, UR, buff=.15).shift(UP * .1)
        a_ptr = Line(a_lab.get_corner(DL) + RIGHT * .05, cross.get_center() + UP * .2, color=INK2,
                     stroke_width=2)
        br = BraceBetweenPoints([xl, Y - H / 2, 0], [xr, Y - H / 2, 0], DOWN, color=INK2)
        dx_lab = M("dx", size=LAB).next_to(br, DOWN, buff=.1)

        eq1 = E(r"dU|=|\tfrac12 E|\varepsilon^2|\,A\,dx", size=EQ, cmap={"dU": MINT})
        eq1.move_to([-3.4, -0.9, 0])
        self.beat("To get the whole bar's energy, add up every slice. A slice has volume A, the bar's "
                  "cross-sectional area, times d x. So it stores one half E epsilon squared, times A d x.",
                  [FadeIn(w), FadeIn(b)], .1, FadeIn(sl), [FadeIn(cross), FadeIn(a_lab), Create(a_ptr)],
                  [GrowFromCenter(br), FadeIn(dx_lab)], Write(eq1),
                  w=(.14, .14, .22, .18, .32))

        # ---- strain of a slice ------------------------------------------------------------------
        ya = Y + H / 2 + .4
        tl = DashedLine([xl, Y + H / 2, 0], [xl, ya + .15, 0], color=INK2, stroke_width=2)
        tr = DashedLine([xr, Y + H / 2, 0], [xr, ya + .15, 0], color=INK2, stroke_width=2)
        al = Arrow([xl, ya, 0], [xl + .6, ya, 0], buff=0, color=SKY, stroke_width=6,
                   max_tip_length_to_length_ratio=.35)
        ar = Arrow([xr, ya, 0], [xr + 1.0, ya, 0], buff=0, color=SKY, stroke_width=6,
                   max_tip_length_to_length_ratio=.25)
        ul = M("u", size=LAB, color=SKY).next_to(al, UP, buff=.12)
        ur = M("u+du", size=LAB, color=SKY).next_to(ar, UP, buff=.12)
        eq2 = E(r"\varepsilon|=|\frac{du}{dx}", size=EQ, cmap={r"\frac{du}{dx}": ACCENT})
        eq2.move_to([3.6, -0.9, 0])
        self.beat("What's the strain of a slice? Its left face moves u, its right face moves u plus d u, "
                  "so it grows by d u. Its length is d x. Change in length over length: d u over d x.",
                  [FadeOut(a_lab), FadeOut(a_ptr), FadeOut(cross)],
                  [Create(tl), GrowArrow(al), FadeIn(ul)], [Create(tr), GrowArrow(ar), FadeIn(ur)],
                  Indicate(dx_lab, color=GOLD), Write(eq2),
                  w=(.1, .2, .25, .15, .3))

        # ---- add up the slices --------------------------------------------------------------------
        slices = VGroup(*[Rectangle(width=DX, height=H).move_to([X0 + (i + .5) * DX, Y, 0])
                          .set_fill(MINT, .3).set_stroke(MINT, 2.5) for i in range(NS)])
        U = E(r"U|=|\tfrac12|\int_0^L|E A|\Big(\frac{du}{dx}\Big)^2|dx", size=60,
              cmap={"E A": LILAC, r"\Big(\frac{du}{dx}\Big)^2": ACCENT})
        U.move_to([0, -2.65, 0])
        self.beat("Add up the slices with an integral from zero to L, and the bar's strain energy is one "
                  "half, the integral of E A, times d u d x, squared, d x.",
                  [FadeOut(VGroup(tl, tr, al, ar, ul, ur, br, dx_lab, sl))],
                  LaggedStart(*[FadeIn(s, scale=1.15) for s in slices], lag_ratio=.25), Write(U),
                  w=(.1, .35, .55))

        # ---- the key formula --------------------------------------------------------------------------
        with self.say("This is the formula the whole rest of the series stands on, so let's make sure it "
                      "feels familiar. Stiffness, times how much it deforms, squared, times one half. "
                      "Exactly the spring's formula, spread along the bar.",
                      style="slower and deliberate, stressing the key words") as d:
            self.play(self.spotlight(U), run_time=.12 * d)
            self.wait(.28 * d)
            self.play(Circumscribe(U[4], color=LILAC), run_time=.12 * d)
            self.play(Circumscribe(U[5], color=ACCENT), run_time=.14 * d)
            self.play(Circumscribe(U[2], color=GOLD), run_time=.12 * d)
            self.wait(.22 * d)

        # ---- even stretch: a spring ----------------------------------------------------------------
        bar_grp = VGroup(b, slices)
        lp = np.array([X0, Y, 0])
        tdash = DashedLine([X1, Y - H / 2 - .1, 0], [X1, ya + .15, 0], color=MUTED, stroke_width=2)
        tq = Arrow([X1, ya, 0], [X1 + .7, ya, 0], buff=0, color=SKY, stroke_width=6,
                   max_tip_length_to_length_ratio=.35)
        tql = M("q", size=LAB, color=SKY).next_to(tq, UP, buff=.12)
        eq3 = E(r"\frac{du}{dx}|=|\frac{q}{L}", size=EQ, cmap={r"\frac{du}{dx}": ACCENT})
        eq3[2][0].set_color(SKY)
        eq3.move_to([-4.0, -2.3, 0])
        eq4 = E(r"U|=|\tfrac12|\frac{EA}{L}|q^2", size=EQ, cmap={r"\frac{EA}{L}": LILAC})
        eq4.move_to([2.6, -2.3, 0])
        kg = glow(eq4[3], LILAC)
        kbr = Brace(eq4[3], DOWN, color=LILAC, buff=.1)
        klab = T("a spring's K", size=34, color=LILAC).next_to(kbr, DOWN, buff=.08)
        self.beat("In fact, if the bar stretches evenly, so its tip moves q, then d u d x is q over L "
                  "everywhere, and U becomes one half, E A over L, q squared. A spring with stiffness E A "
                  "over L.",
                  [self.unspot(), FadeOut(eq1), FadeOut(eq2), U.animate.move_to([0, -0.75, 0])],
                  [FadeIn(tdash), bar_grp.animate.stretch(STR, 0, about_point=lp), GrowArrow(tq),
                   FadeIn(tql)],
                  Write(eq3), Write(eq4), [FadeIn(kg), GrowFromCenter(kbr), FadeIn(klab)],
                  w=(.14, .2, .2, .22, .24))

        # ---- rigid slide: no energy ----------------------------------------------------------------
        sh = .7
        sq1 = Arrow([X0, ya, 0], [X0 + sh, ya, 0], buff=0, color=SKY, stroke_width=6,
                    max_tip_length_to_length_ratio=.35)
        sq2 = Arrow([X1, ya, 0], [X1 + sh, ya, 0], buff=0, color=SKY, stroke_width=6,
                    max_tip_length_to_length_ratio=.35)
        sl1 = M("q", size=LAB, color=SKY).next_to(sq1, UP, buff=.12)
        sl2 = M("q", size=LAB, color=SKY).next_to(sq2, UP, buff=.12)
        eq5 = E(r"\frac{du}{dx}|=|0", size=EQ, cmap={r"\frac{du}{dx}": ACCENT}).move_to([-3.0, -2.3, 0])
        eq6 = E(r"U|=|0", size=EQ).move_to([3.0, -2.3, 0])
        self.beat("And if the bar just slides along without stretching, d u d x is zero, and so is U. "
                  "No stretch, no stored energy.",
                  [FadeOut(VGroup(eq3, eq4, kg, kbr, klab, tq, tql, tdash)),
                   bar_grp.animate.stretch(1 / STR, 0, about_point=lp), FadeOut(w)],
                  [bar_grp.animate.shift(RIGHT * sh), GrowArrow(sq1), GrowArrow(sq2), FadeIn(sl1), FadeIn(sl2)],
                  Write(eq5), [Write(eq6), FadeIn(glow(eq6, MINT))],
                  w=(.18, .3, .24, .28))
        self.wipe()
