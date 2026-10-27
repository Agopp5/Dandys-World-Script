"""S06: the bottom of the bowl is equilibrium (BRIEF.md S06)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: one spring, K = 20 N/mm, F = 100 N  ->  Pi(q) = 10 q^2 - 100 q  (N mm)
K_, F_ = 20.0, 100.0
Pi = lambda q: 0.5 * K_ * q ** 2 - F_ * q
dPi = lambda q: K_ * q - F_
assert np.isclose(0.5 * K_, 10) and np.isclose(K_, 20)        # d/dq of 10 q^2 is 20 q
assert np.allclose([Pi(q) for q in (0, 3, 5, 7, 10)], [0, -210, -250, -210, 0])
q_star = F_ / K_
assert np.isclose(q_star, 5) and np.isclose(dPi(q_star), 0)   # 20 q - 100 = 0 -> q = 5 mm
assert np.isclose(Pi(q_star), -250)                           # bottom of the bowl
assert np.isclose(0.5 * K_ * q_star ** 2, 250) and np.isclose(F_ * q_star, 500)


class S06_Minimum(VScene):
    budget = 169

    def construct(self):
        # ---- the bowl (left) ----
        ax = axes((0, 10.5, 5), (-300, 60, 100), width=6.0, height=5.0, xlabel="q", ylabel=r"\Pi")
        ax.move_to(LEFT * 3.0 + DOWN * 0.4)
        ticks = VGroup(*[M(str(v), size=28, color=INK2).next_to(ax.c2p(v, 0), UP, buff=.12) for v in (5, 10)],
                       *[M(str(v), size=28, color=INK2).next_to(ax.c2p(0, v), LEFT, buff=.12)
                         for v in (-100, -200)])
        bowl = ax.plot(Pi, x_range=[0, 10], color=GOLD, stroke_width=5)
        tk = ValueTracker(1.3)
        dot = always_redraw(lambda: Dot(ax.c2p(tk.get_value(), Pi(tk.get_value())), color=SKY, radius=0.1)
                            .set_z_index(3))

        def tan_line():
            q0 = tk.get_value()
            h = 1.3
            a = ax.c2p(q0 - h, Pi(q0) - dPi(q0) * h)
            b = ax.c2p(q0 + h, Pi(q0) + dPi(q0) * h)
            return Line(a, b, color=ACCENT, stroke_width=4).set_z_index(2)
        tan = always_redraw(tan_line)

        # ---- algebra (right) ----
        X = 3.9
        pi_n = E(r"\Pi|=|10|q^2|-|100|q", size=48)
        paint(pi_n, {3: SKY})
        pi_n.move_to(RIGHT * X + UP * 2.4)
        eq1 = E(r"\frac{d\Pi}{dq}|=|0", size=52).move_to(RIGHT * X + UP * 0.8)

        with self.say("The bottom of a smooth bowl is where it's flat: the slope is zero. So we take the derivative of Pi with respect to q and set it to zero.") as d:
            self.play(Create(ax), FadeIn(ticks), Create(bowl), FadeIn(pi_n), run_time=.18 * d)
            self.add(tan, dot)
            self.play(tk.animate.set_value(8.6), run_time=.22 * d, rate_func=smooth)
            self.play(tk.animate.set_value(5), run_time=.25 * d, rate_func=smooth)
            self.play(Write(eq1), run_time=.2 * d)
            self.play(Indicate(eq1[2], color=ACCENT), run_time=.15 * d)

        self.beat("Your turn: pause and do checkpoint one point one in your guide. Find the bottom of the bowl.",
                  Circumscribe(bowl, color=GOLD))
        self.checkpoint("1.1", "One spring: find the q where Pi is lowest")

        # d Pi / dq = 20 q - 100 = 0, term by term
        eq3 = E(r"\frac{d\Pi}{dq}|=|20|q|-|100|=|0", size=52).move_to(RIGHT * X + UP * 0.8)
        with self.say("The derivative of ten q squared is twenty q. The derivative of minus one hundred q is minus one hundred. So twenty q minus one hundred equals zero.") as d:
            self.play(ReplacementTransform(eq1[0], eq3[0]), ReplacementTransform(eq1[1], eq3[1]),
                      ReplacementTransform(eq1[2], eq3[7]), FadeIn(eq3[6]), run_time=.1 * d)
            self.play(Indicate(VGroup(pi_n[2], pi_n[3])),
                      TransformFromCopy(VGroup(pi_n[2], pi_n[3]), VGroup(eq3[2], eq3[3])), run_time=.25 * d)
            self.wait(.05 * d)
            self.play(Indicate(VGroup(pi_n[4], pi_n[5], pi_n[6])),
                      TransformFromCopy(VGroup(pi_n[4], pi_n[5], pi_n[6]), VGroup(eq3[4], eq3[5])),
                      run_time=.3 * d)
            self.play(Circumscribe(eq3, color=ACCENT), run_time=.3 * d)

        # q = 5 mm, the dot settles, Pi = -250
        qeq = E(r"q|=|5\text{ mm}", size=52).move_to(RIGHT * X + DOWN * 0.9)
        card = panel(E(r"\Pi|=|-250\text{ N mm}", size=40))
        card.move_to(ax.c2p(5, -95))
        vline = DashedLine(ax.c2p(5, 0), ax.c2p(5, -250), color=MUTED)
        five = ticks[0]
        with self.say("Twenty q equals one hundred, so q is five millimeters. There's the bottom of the bowl, at five, where Pi is minus two hundred fifty.") as d:
            self.play(TransformFromCopy(eq3[2:6], qeq), run_time=.25 * d)
            g = glow(qeq, SKY)
            self.play(FadeIn(g), run_time=.1 * d)
            self.play(tk.animate.set_value(6.4), run_time=.08 * d)
            self.play(tk.animate.set_value(4.3), run_time=.08 * d)
            self.play(tk.animate.set_value(5), run_time=.09 * d)
            self.play(Create(vline), Indicate(five, color=SKY), run_time=.12 * d)
            self.play(FadeIn(card, shift=UP * .2), run_time=.15 * d)
            self.play(Indicate(card[1], color=GOLD), run_time=.13 * d)

        # the same with letters
        pi_l = E(r"\Pi|=|\tfrac{1}{2}|K|q^2|-|F|q", size=48)
        paint(pi_l, {4: SKY})
        pi_l.move_to(RIGHT * X + UP * 2.4)
        eqL = E(r"\frac{d\Pi}{dq}|=|K|q|-|F|=|0", size=52).move_to(RIGHT * X + UP * 0.8)
        kqf = E(r"K|q|=|F", size=56).move_to(RIGHT * X + DOWN * 0.9)
        with self.say("Now do it with letters. The derivative of one half K q squared is K q. The derivative of F q is F. So K q minus F equals zero. Which says K q equals F.") as d:
            self.play(FadeOut(VGroup(eq3, qeq, g, card, vline)), FadeOut(pi_n), run_time=.06 * d)
            self.play(FadeIn(pi_l), run_time=.1 * d)
            self.play(FadeIn(eqL[0]), FadeIn(eqL[1]), FadeIn(eqL[6]), FadeIn(eqL[7]), run_time=.08 * d)
            self.play(Indicate(VGroup(pi_l[2], pi_l[3], pi_l[4])),
                      TransformFromCopy(VGroup(pi_l[2], pi_l[3], pi_l[4]), VGroup(eqL[2], eqL[3])),
                      run_time=.2 * d)
            self.play(Indicate(VGroup(pi_l[6], pi_l[7])),
                      TransformFromCopy(VGroup(pi_l[5], pi_l[6], pi_l[7]), VGroup(eqL[4], eqL[5])),
                      run_time=.2 * d)
            self.play(Circumscribe(eqL, color=ACCENT), run_time=.14 * d)
            self.play(TransformFromCopy(eqL[2], kqf[0]), TransformFromCopy(eqL[3], kqf[1]),
                      TransformFromCopy(eqL[5], kqf[3]), FadeIn(kqf[2]), run_time=.17 * d)
            self.wait(.05 * d)

        # energy result next to force balance
        blk = Square(0.7, color=INK2, fill_color=SURFACE, fill_opacity=1, stroke_width=3)
        up = force(blk.get_top(), d=UP, length=0.9, label="Kq", color=LILAC)
        dn = force(blk.get_bottom(), d=DOWN, length=0.9, label="F")
        fbd = VGroup(blk, up, dn)
        kqf_force = E(r"K|q|=|F", size=56)
        fb = VGroup(fbd, kqf_force).arrange(RIGHT, buff=.6)
        lab_e = T("from energy", size=30, color=MUTED)
        lab_f = T("from forces", size=30, color=MUTED)
        with self.say("This is the key step, so take it in slowly: setting the slope of the energy to zero gave us exactly Newton's force balance. Same equation, reached without drawing a single force.",
                      style="slower and deliberate, stressing the key words") as d:
            self.play(FadeOut(VGroup(pi_l, eqL)), kqf.animate.move_to(RIGHT * 1.4 + UP * 0.2),
                      run_time=.12 * d)
            lab_e.next_to(kqf, DOWN, buff=.45)
            fb.next_to(kqf, RIGHT, buff=1.0)
            kqf_force.align_to(kqf, DOWN)
            fbd.set_y(kqf.get_y())
            lab_f.next_to(kqf_force, DOWN, buff=.45)
            self.play(FadeIn(lab_e), run_time=.08 * d)
            self.play(FadeIn(fb, shift=LEFT * 1.5), run_time=.2 * d)
            self.play(FadeIn(lab_f), run_time=.07 * d)
            self.play(self.spotlight(kqf, fb, lab_e, lab_f), run_time=.15 * d)
            self.play(Indicate(kqf, color=GOLD), Indicate(kqf_force, color=GOLD), run_time=.15 * d)
            self.wait(.3 * d)
        self.wipe()
