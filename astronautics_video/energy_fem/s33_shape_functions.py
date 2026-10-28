"""S33: shape functions (BRIEF.md S33)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# ---- facts (everything here is symbolic; U1, U2 are only display heights for u1, u2, never spoken)
U1, U2 = 0.6, 1.2
B2 = U1                     # s = 0:  u(0) = b2 = u1
B1 = U2 - B2                # s = 1:  b1 + b2 = u2  ->  b1 = u2 - u1
N1 = lambda s: 1 - s
N2 = lambda s: s
for s_ in np.linspace(0, 1, 11):
    assert np.isclose(B1 * s_ + B2, (U2 - U1) * s_ + U1)            # put the b's back
    assert np.isclose((U2 - U1) * s_ + U1, (1 - s_) * U1 + s_ * U2)  # rearrange
    assert np.isclose(N1(s_) * U1 + N2(s_) * U2, B1 * s_ + B2)       # u = N1 u1 + N2 u2
    assert np.isclose(N1(s_) + N2(s_), 1)                            # the ramps add to one
for a_, b_ in np.random.default_rng(33).normal(size=(6, 2)):          # any end values u1 = a_, u2 = b_
    bb2, bb1 = a_, b_ - a_
    assert np.isclose(bb1 * 0 + bb2, a_) and np.isclose(bb1 * 1 + bb2, b_)
assert N1(0) == 1 and N1(1) == 0 and N2(0) == 0 and N2(1) == 1


def ind(m, c):
    return Indicate(m, scale_factor=1.2, color=c)


class S33_Shape_Functions(VScene):
    budget = 181

    def construct(self):
        self.section("Shape functions")

        # ---------------- left half: plot of u over s, the element under it
        ax = axes([0, 1.12, 1], [0, 1.5, 5], width=5.6, height=3.3, xlabel="", ylabel="")
        ax.shift(np.array([-5.9, -0.55, 0]) - ax.c2p(0, 0))
        P = ax.c2p
        s_lab = M("s", size=40, color=LIME).next_to(ax.x_axis.get_end(), RIGHT, buff=.15)
        u_lab = M("u", size=40, color=SKY).next_to(ax.y_axis.get_end(), LEFT, buff=.2)
        t0 = M("0", size=36, color=INK2).next_to(P(0, 0), DOWN, buff=.2)
        t1 = M("1", size=36, color=INK2).next_to(P(1, 0), DOWN, buff=.2)
        guide = DashedLine(P(1, 0), P(1, 1.42), color=MUTED, stroke_width=2)

        xa, xb, yb = P(0, 0)[0], P(1, 0)[0], -1.8
        el = bar(xa, xb, y=yb)
        n1, n2 = node([xa, yb, 0], r=.1), node([xb, yb, 0], r=.1)
        d1 = disp([xa, yb, 0], label="u_1")
        d2 = disp([xb, yb, 0], label="u_2")
        nm1 = T("node 1", size=36, color=INK2).next_to(d1, DOWN, buff=.18).set_x(xa + .2)
        nm2 = T("node 2", size=36, color=INK2).next_to(d2, DOWN, buff=.18).set_x(xb + .2)
        element = VGroup(el, n1, n2, d1, d2, nm1, nm2)

        b1 = ValueTracker(-0.85)
        b2 = ValueTracker(1.25)
        line = always_redraw(lambda: Line(P(0, b2.get_value()), P(1, b1.get_value() + b2.get_value()),
                                          color=SKY, stroke_width=7))
        tg1 = Circle(radius=.15, color=SKY, stroke_width=4).move_to(P(0, U1))
        tg2 = Circle(radius=.15, color=SKY, stroke_width=4).move_to(P(1, U2))
        lu1 = M("u_1", size=40, color=SKY).next_to(P(0, U1), LEFT, buff=.3)
        lu2 = M("u_2", size=40, color=SKY).next_to(P(1, U2), RIGHT, buff=.3)
        pin1 = Dot(P(0, U1), radius=.11, color=SKY).set_z_index(3)
        pin2 = Dot(P(1, U2), radius=.11, color=SKY).set_z_index(3)

        # ---------------- right half: the algebra
        RX = 3.7
        eqA = E(r"u|(|s|)|=|b_1|s|+|b_2", size=56).move_to([RX, 2.55, 0])
        eqB = E(r"b_2|=|u_1", size=52)
        eqC = E(r"b_1|+|b_2|=|u_2", size=52)
        eqC2 = E(r"b_1|=|u_2|-|u_1", size=52)
        eqB.shift(np.array([eqA[4].get_x(), 1.05, 0]) - eqB[1].get_center())
        eqC.shift(np.array([eqA[4].get_x(), -0.45, 0]) - eqC[2].get_center())
        eqC2.shift(np.array([eqA[4].get_x(), -0.45, 0]) - eqC2[1].get_center())
        # 0 u, 1 (, 2 s, 3 ), 4 =, 5 (, 6 u_2, 7 -, 8 u_1, 9 ), 10 s, 11 +, 12 u_1
        eqA2 = E(r"u|(|s|)|=|(|u_2|-|u_1|)|s|+|u_1", size=54).move_to([RX, 2.55, 0])
        # 0 u, 1 (, 2 s, 3 ), 4 =, 5 (1-, 6 s, 7 ), 8 u_1, 9 +, 10 s, 11 u_2
        eqA3 = E(r"u|(|s|)|=|(1-|s|)|u_1|+|s|u_2", size=56).move_to([RX, 2.55, 0])

        # ---------------- beat 1
        with self.say("Inside the element, we said u is a straight line. Write it as b one times s, plus b two, "
                      "and choose the b's to match the ends.") as d:
            self.play(FadeIn(el), FadeIn(n1), FadeIn(n2), FadeIn(d1), FadeIn(d2), FadeIn(nm1), FadeIn(nm2),
                      run_time=.14 * d)
            self.play(Create(ax), FadeIn(s_lab), FadeIn(u_lab), FadeIn(t0), FadeIn(t1), Create(guide),
                      run_time=.14 * d)
            self.play(Create(line), run_time=.1 * d)
            self.play(Write(eqA), run_time=.22 * d)
            self.play(b2.animate.set_value(.3), b1.animate.set_value(.75), ind(d1, SKY), run_time=.13 * d)
            self.play(b2.animate.set_value(1.0), b1.animate.set_value(-.3), ind(d2, SKY), run_time=.13 * d)

        # ---------------- beat 2: pin the ends one condition at a time
        with self.say("At s equals zero, u must be u one, so b two is u one. At s equals one, u must be u two, "
                      "so b one plus b two is u two, and b one is u two minus u one.") as d:
            self.play(ind(t0, LIME), FadeIn(tg1), FadeIn(lu1), run_time=.12 * d)
            self.play(b2.animate.set_value(B2), run_time=.12 * d)
            self.play(FadeIn(pin1, scale=.4), Write(eqB), run_time=.12 * d)
            self.play(ind(t1, LIME), FadeIn(tg2), FadeIn(lu2), run_time=.12 * d)
            self.play(Write(eqC), run_time=.12 * d)
            self.play(b1.animate.set_value(B1), run_time=.12 * d)
            self.play(FadeIn(pin2, scale=.4), *morph(eqC, eqC2, [(0, 0), (2, 1), (3, 2)]), run_time=.16 * d)
        line.clear_updaters()
        self.remove(tg1, tg2)

        # ---------------- beat 3: put them back, then rearrange
        with self.say("Put them back and rearrange: u of s equals one minus s, times u one, plus s, "
                      "times u two.") as d:
            an = [ReplacementTransform(eqA[i], eqA2[j]) for i, j in [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4),
                                                                      (6, 10), (7, 11)]]
            an += [FadeOut(eqA[5], shift=DOWN * .2), FadeOut(eqA[8], shift=DOWN * .2),
                   FadeIn(eqA2[5]), FadeIn(eqA2[9]),
                   *[TransformFromCopy(eqC2[k], eqA2[k + 4]) for k in (2, 3, 4)],
                   TransformFromCopy(eqB[2], eqA2[12])]
            self.play(*an, run_time=.24 * d)
            self.remove(eqA, *eqA2)
            self.add(eqA2)
            self.play(*morph(eqA2, eqA3, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (12, 8), (6, 11), (10, 10),
                                          (11, 9)]),
                      FadeOut(eqB), FadeOut(eqC2), run_time=.24 * d)
            g3 = glow(eqA3, LIME)
            self.play(FadeIn(g3), run_time=.1 * d)
            self.play(ind(eqA3[5:9], LIME), run_time=.17 * d)
            self.play(ind(eqA3[10:12], LIME), run_time=.17 * d)
