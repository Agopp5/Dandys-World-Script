"""S10: the energy of two springs (BRIEF.md S10)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: Pi(q1, q2) = 1/2 k1 q1^2 + 1/2 k2 (q2 - q1)^2 - F1 q1 - F2 q2 is stationary at the Newton answer
_k1, _k2, _F1, _F2 = 40.0, 20.0, 40.0, 20.0
def _Pi(q1, q2):
    return .5 * _k1 * q1 ** 2 + .5 * _k2 * (q2 - q1) ** 2 - _F1 * q1 - _F2 * q2
_h = 1e-6
assert abs((_Pi(1.5 + _h, 2.5) - _Pi(1.5 - _h, 2.5)) / (2 * _h)) < 1e-4
assert abs((_Pi(1.5, 2.5 + _h) - _Pi(1.5, 2.5 - _h)) / (2 * _h)) < 1e-4
# stretch of spring 2 is the difference: a rigid shift of both nodes leaves its energy unchanged
assert np.isclose(.5 * _k2 * ((2.5 + 1) - (1.5 + 1)) ** 2, .5 * _k2 * (2.5 - 1.5) ** 2)


class S10_Two_Energy(VScene):
    budget = 129

    def construct(self):
        # ---- the two-spring figure (top) ----
        fig = two_spring_fig()            # the shared Episode 2 figure (S08-S12)
        w, s1, s2, n1, n2 = fig.wall, fig.s1, fig.s2, fig.n1, fig.n2
        f1, f2, d1, d2 = fig.F1, fig.F2, fig.q1, fig.q2

        # per-spring energy tags under each spring's middle
        yt = fig.get_bottom()[1] - .35
        m1 = np.array([s1.get_x(), yt, 0])
        m2 = np.array([s2.get_x(), yt, 0])
        u1 = M(r"U_1", size=36, color=MINT).move_to(m1)
        u2 = M(r"U_2", size=36, color=MINT).move_to(m2)

        # ---- beat 1: the rule for one spring, then add ----
        rule = E(r"U_{\text{spring}}|=|\tfrac12|k|(\text{stretch})^2", size=48)
        paint(rule, {0: MINT})
        rule.move_to(DOWN * .1)
        total = E(r"U|=|U_1|+|U_2", size=48)
        paint(total, {2: MINT, 4: MINT})
        total.move_to(DOWN * 1.4)
        g1, g2 = glow(s1, MINT), glow(s2, MINT)
        self.beat("Strain energy first. Each spring stores one half, its stiffness, times its stretch squared. "
                  "Then we add them up, because energy is just a number, and numbers add.",
                  FadeIn(fig), Write(rule),
                  [FadeIn(g1), FadeIn(u1)], [FadeOut(g1), FadeIn(g2), FadeIn(u2)], FadeOut(g2),
                  Write(total), .15,
                  w=(.12, .2, .12, .12, .06, .18))

        # ---- beat 2: the two terms, each with its own stretch ----
        U = E(r"U|=|\tfrac12|k_1|q_1^2|+|\tfrac12|k_2|(|q_2|-|q_1|)^2", size=50)
        paint(U, {4: SKY})
        U.move_to(DOWN * .1)
        st1 = M(r"\text{stretch }", r"q_1", size=36).move_to(m1)
        st1[1].set_color(SKY)
        st2 = M(r"\text{stretch }", r"q_2-q_1", size=36).move_to(m2)
        st2[1].set_color(SKY)
        g1, g2 = glow(s1, MINT), glow(s2, MINT)
        with self.say("Spring one stores one half k one q one squared. "
                      "Spring two stores one half k two, times q two minus q one, squared.") as d:
            self.play(FadeOut(rule), FadeOut(total[2:]), ReplacementTransform(total[0:2], U[0:2]),
                      run_time=.1 * d)
            self.play(FadeIn(g1), ReplacementTransform(u1, st1), Write(U[2:5]), run_time=.3 * d)
            self.play(FadeOut(g1), Write(U[5]), run_time=.08 * d)
            self.play(FadeIn(g2), ReplacementTransform(u2, st2), Write(U[6:13]), run_time=.37 * d)
            self.play(FadeOut(g2), run_time=.08 * d)
            self.wait(.07 * d)

        # ---- beat 3: the crux, the stretch is a difference ----
        # spotlight frames (not the dense math itself), with sharp copies of the math lifted above the dimmer
        box_u = SurroundingRectangle(U[8:13], color=GOLD, buff=.12, corner_radius=.08)
        box_s = SurroundingRectangle(st2, color=GOLD, buff=.08, corner_radius=.06)
        sharp = VGroup(U[8:13].copy(), st2.copy()).set_z_index(1000)
        self.beat("Pay close attention to that second term, because this is where most mistakes happen. "
                  "It's the stretch, q two minus q one, that gets squared, not q two by itself.",
                  self.spotlight(box_u, box_s), FadeIn(sharp), .2,
                  Circumscribe(sharp[0], color=GOLD), .4,
                  w=(.15, .1, .15), style="slower and deliberate, stressing the key words")

        # ---- beat 4: work potential ----
        W = E(r"W|=|F_1|q_1|+|F_2|q_2", size=50).move_to(DOWN * 1.4)
        W.align_to(U, LEFT)
        self.beat("The work potential is each load times the displacement of its own node: "
                  "F one q one plus F two q two.",
                  [self.unspot(), FadeOut(box_u), FadeOut(box_s), FadeOut(sharp)], Write(W[0:2]),
                  [Indicate(f1, color=ROSE), Indicate(d1, color=SKY), Write(W[2:4])],
                  [Indicate(f2, color=ROSE), Indicate(d2, color=SKY), Write(W[4:7])], .2,
                  w=(.1, .1, .3, .3))

        # ---- beat 5: Pi = U - W, then the whole thing on one line ----
        Pi = E(r"\Pi|=|U|-|W", size=50).move_to(DOWN * 2.75)
        Pf = E(r"\Pi|=|\tfrac12|k_1|q_1^2|+|\tfrac12|k_2|(|q_2|-|q_1|)^2|-|F_1|q_1|-|F_2|q_2", size=46)
        paint(Pf, {4: SKY})
        fit(Pf, 13.0, 1.2)
        Pf.move_to(DOWN * 2.75)
        with self.say("And Pi is U minus W. One function of two unknowns. The stationary principle says: "
                      "at the real answer, Pi is stationary in every direction.") as d:
            self.play(Write(Pi), run_time=.14 * d)
            self.play(Indicate(Pi[2], color=MINT), Indicate(U[0], color=MINT),
                      Indicate(Pi[4], color=EMBER), Indicate(W[0], color=EMBER), run_time=.12 * d)
            moves = [TransformFromCopy(U[i], Pf[i]) for i in range(2, 13)]
            moves += [TransformFromCopy(W[2], Pf[14]), TransformFromCopy(W[3], Pf[15]),
                      TransformFromCopy(W[5], Pf[17]), TransformFromCopy(W[6], Pf[18])]
            moves += [ReplacementTransform(Pi[0], Pf[0]), ReplacementTransform(Pi[1], Pf[1]),
                      ReplacementTransform(Pi[3], Pf[13]), FadeOut(Pi[2]), FadeOut(Pi[4]), FadeIn(Pf[16])]
            self.play(*moves, run_time=.24 * d)
            self.wait(.1 * d)
            self.play(Circumscribe(Pf, color=GOLD), Indicate(d1, color=SKY), Indicate(d2, color=SKY), run_time=.25 * d)
            self.wait(.15 * d)
        self.wipe()
