"""S26: the work potential of a bar (BRIEF.md S26)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: W = P u(L) + integral of f u dx. Check with u = a x (the next scene's shape): W = P a L + f a L^2 / 2.
_P, _f, _a, _L = 3.0, 2.0, 0.1, 5.0
_x = np.linspace(0, _L, 20001)
_Wnum = _P * _a * _L + np.trapezoid(_f * _a * _x, _x)
assert np.isclose(_Wnum, _P * _a * _L + _f * _a * _L ** 2 / 2)

X0, X1, Y = -6.0, 4.4, 1.8      # bar from the wall to the tip, centre height
H = 0.62                        # bar thickness


class S26_Bar_W(VScene):
    budget = 107

    def construct(self):
        # the bar, fixed at the left wall
        w = wall(np.array([X0, Y, 0]), side=LEFT, h=1.9)
        b = bar(X0, X1, y=Y, h=H)
        tip = np.array([X1, Y, 0])
        fP = force(tip, d=RIGHT, length=1.3, label=None)
        lP = M("P", size=48, color=ROSE).next_to(fP, UP, buff=.15)
        uL = Arrow(np.array([X1, Y - .75, 0]), np.array([X1 + 1.0, Y - .75, 0]), buff=0, color=SKY,
                   stroke_width=7, max_tip_length_to_length_ratio=.3)
        luL = M("u(L)", size=44, color=SKY).next_to(uL, DOWN, buff=.15)
        tipbox = SurroundingRectangle(Line(tip + .4 * UP, tip + .4 * DOWN), color=ROSE, buff=.12)
        self.add(w, b)

        eqP = E(r"P|u(L)", size=60).move_to(np.array([0, -1.1, 0]))
        paint(eqP, {1: SKY})
        self.beat("The work potential is load times displacement, as always. The tip load P acts where the bar moves u of L, so it gives P times u at L.",
                  [GrowFromPoint(fP, tip), FadeIn(lP)], Create(tipbox), [GrowArrow(uL), FadeIn(luL)], .1,
                  Write(eqP), w=(.25, .15, .25, .1, .25))

        # the spread-out load: a row of small f arrows, and one slice dx
        fl = dist_load(X0 + .3, X1 - .3, Y + .62, n=11, d=RIGHT)
        lf = M("f", size=44, color=ROSE).next_to(fl, LEFT, buff=.2).shift(.05 * UP)
        sx0, sx1 = -0.3, 0.3
        slc = Rectangle(width=sx1 - sx0, height=H, stroke_color=INK, stroke_width=4,
                        fill_color=GOLD, fill_opacity=.45).move_to(np.array([(sx0 + sx1) / 2, Y, 0]))
        sdx = span(np.array([sx0, Y - H / 2 - .05, 0]), np.array([sx1, Y - H / 2 - .05, 0]),
                   M("dx", size=40), side=DOWN)
        fdx = force(np.array([sx0, Y + 1.25, 0]), d=RIGHT, length=.9, label=None)
        lfdx = M(r"f|\,dx", size=44)
        paint(lfdx, {0: ROSE})
        lfdx.next_to(fdx, UP, buff=.12)
        us = Arrow(np.array([sx0 - 1.6, Y - .75, 0]), np.array([sx0 - .7, Y - .75, 0]), buff=0, color=SKY,
                   stroke_width=7, max_tip_length_to_length_ratio=.3)
        lus = M("u", size=44, color=SKY).next_to(us, DOWN, buff=.15)
        eqI = E(r"\int_0^L|f|u|\,dx", size=60).move_to(np.array([0, -2.6, 0]))
        self.beat("The spread-out load acts everywhere. A slice d x carries f d x, and moves u, so add up f u d x along the bar.",
                  [FadeOut(tipbox), LaggedStart(*[FadeIn(a, shift=.2 * RIGHT) for a in fl], lag_ratio=.12), FadeIn(lf)],
                  [FadeIn(slc), FadeIn(sdx)], [GrowFromPoint(fdx, fdx.get_left()), FadeIn(lfdx)], [GrowArrow(us), FadeIn(lus)],
                  Write(eqI), w=(.25, .15, .15, .15, .3))

        # assemble W, then Pi
        wl = E(r"W|=|P|u(L)|+|\int_0^L|f|u|\,dx", size=60).move_to(np.array([0, -1.1, 0]))
        paint(wl, {3: SKY})
        pl = E(r"\Pi|=|U|-|W", size=64).move_to(np.array([0, -2.75, 0]))
        old = VGroup(*eqP, *eqI)
        with self.say("So W equals P u at L, plus the integral of f u d x. And Pi is U minus W, as before.") as d:
            self.play(*morph(old, wl, [(0, 2), (1, 3), (2, 5), (3, 6), (4, 7), (5, 8)]), run_time=.35 * d)
            self.play(Circumscribe(wl, color=EMBER), run_time=.2 * d)
            self.play(Write(pl), run_time=.25 * d)
            gpl = glow(pl, GOLD)
            self.play(FadeIn(gpl), run_time=.1 * d)
            self.wait(.1 * d)

        # the problem: Pi depends on a whole function
        dots = VGroup(*[Dot(np.array([x, Y, 0]), radius=.09, color=SKY)
                        for x in np.linspace(X0 + .4, X1, 22)])
        q = M(r"\frac{\partial \Pi}{\partial\, u(x)}", size=60).move_to(np.array([-1.0, -2.2, 0]))
        qm = M("?", size=110, color=ACCENT).next_to(q, RIGHT, buff=.5)
        note = T("a value at every point", size=34, color=MUTED).next_to(dots, UP, buff=1.25)
        self.beat("But here's the problem. Pi now depends on a whole function, u of x. We can't take a partial derivative with respect to every point. We need a trick.",
                  [FadeOut(wl), FadeOut(gpl), pl.animate.move_to(np.array([0, -.9, 0])).scale(.85)],
                  [FadeOut(VGroup(fl, lf, fdx, lfdx, slc, sdx)), LaggedStart(*[GrowFromCenter(p) for p in dots], lag_ratio=.08)],
                  FadeIn(note),
                  Write(q), [FadeIn(qm, scale=1.4), FadeIn(glow(qm, ACCENT))], .15,
                  w=(.15, .25, .1, .2, .15, .15))
        self.wipe()
