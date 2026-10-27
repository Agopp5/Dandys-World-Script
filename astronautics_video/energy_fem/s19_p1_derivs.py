"""S19: three partial derivatives of Pi for HW P1 (BRIEF.md S19)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})


# facts: every derivative line and its expanded form, checked against a numerical derivative of Pi
def _check_derivs():
    rng = np.random.default_rng(19)
    K1, K2, K3, P1, P2, P3, P4 = rng.uniform(1, 5, 7)

    def Pi(q1, q2, q3):
        return (.5 * K1 * q2 ** 2 + .5 * K2 * q1 ** 2 + .5 * K2 * (q2 - q1) ** 2 + .5 * K3 * (q3 - q2) ** 2
                - P1 * q1 - (P2 + P3) * q2 - P4 * q3)

    q = rng.uniform(-2, 2, 3)
    q1, q2, q3 = q
    h = 1e-4   # central difference: exact for a quadratic up to rounding

    def dPi(i):
        e = np.zeros(3)
        e[i] = h
        return (Pi(*(q + e)) - Pi(*(q - e))) / (2 * h)

    assert np.isclose(dPi(0), K2 * q1 - K2 * (q2 - q1) - P1)
    assert np.isclose(dPi(0), K2 * q1 - K2 * q2 + K2 * q1 - P1)
    assert np.isclose(dPi(0), 2 * K2 * q1 - K2 * q2 - P1)
    assert np.isclose(dPi(1), K1 * q2 + K2 * (q2 - q1) - K3 * (q3 - q2) - (P2 + P3))
    assert np.isclose(dPi(1), K1 * q2 + K2 * q2 - K2 * q1 - K3 * q3 + K3 * q2 - (P2 + P3))
    assert np.isclose(dPi(1), -K2 * q1 + (K1 + K2 + K3) * q2 - K3 * q3 - (P2 + P3))
    assert np.isclose(dPi(2), K3 * (q3 - q2) - P4)
    assert np.isclose(dPi(2), -K3 * q2 + K3 * q3 - P4)
    # sanity numbers from the brief: all K = 100 N/mm, all P = 30 N -> q = (0.5, 0.7, 1.0) mm solves all three
    K, P, (a, b, c) = 100.0, 30.0, (0.5, 0.7, 1.0)
    assert np.isclose(2 * K * a - K * b, P)
    assert np.isclose(-K * a + 3 * K * b - K * c, 2 * P)
    assert np.isclose(-K * b + K * c, P)


_check_derivs()

PI_Y, D_Y, W_Y = 3.4, 1.35, 0.1         # Pi (two lines from here down), derivative line, working line
TX, TY = 2.0, [-1.15, -2.1, -3.05]      # tray: results stacked, "=" aligned at x = TX


class S19_P1_Derivs(VScene):
    budget = 250

    def construct(self):
        # Pi on two lines (strain energy, then the loads); pi[i] numbers the parts across both lines
        la = E(r"\Pi|=|\tfrac12 K_1 q_2^2|+|\tfrac12 K_2 q_1^2|+|\tfrac12 K_2(q_2-q_1)^2|+|\tfrac12 K_3(q_3-q_2)^2",
               size=48)
        lb = E(r"-|P_1 q_1|-|(P_2+P_3)\,q_2|-|P_4 q_3|", size=48)
        la.move_to([0, PI_Y, 0])
        lb.next_to(la, DOWN, buff=.25).align_to(la[2], LEFT)
        pi = VGroup(*la, *lb)
        paint(pi, {2: MINT, 4: MINT, 6: MINT, 8: MINT, 10: EMBER, 12: EMBER, 14: EMBER})
        terms = [2, 4, 6, 8, 10, 12, 14]
        state = {"boxes": VGroup()}

        def focus(idxs):
            """Box the Pi terms that contain the current unknown; dim the rest."""
            old = state["boxes"]
            new = VGroup(*[SurroundingRectangle(pi[i], color=SKY, buff=.07, stroke_width=3) for i in idxs])
            state["boxes"] = new
            anims = [pi[i].animate.set_opacity(1 if i in idxs else .3) for i in terms]
            anims += [Create(new)]
            if len(old):
                anims.append(FadeOut(old))
            return anims

        def unfocus():
            anims = [pi[i].animate.set_opacity(1) for i in terms]
            if len(state["boxes"]):
                anims.append(FadeOut(state["boxes"]))
                state["boxes"] = VGroup()
            return anims

        def at(m, y):
            fit(m, 13.4, 1.4)
            return m.move_to([0, y, 0])

        def tray_target(r, eq_i, k):
            t = r.copy()
            t.shift([TX - t[eq_i].get_center()[0], TY[k] - t[eq_i].get_center()[1], 0])
            return t

        # ---------- q1 ----------
        self.beat("Start with q one. It appears in two springs: the first K two, and the second K two, where it shows up inside q two minus q one.",
                  FadeIn(pi), .1, focus([4, 6]), w=(.3, .6))

        d1 = at(E(r"\frac{\partial \Pi}{\partial q_1}|=|K_2 q_1|-|K_2(q_2-q_1)|-|P_1|=|0", size=48), D_Y)
        with self.say("The first gives K two q one. The second gives K two times q two minus q one, times minus one, from the chain rule. And the load gives minus P one.") as d:
            self.play(Write(d1[0:2]), run_time=.1 * d)
            self.play(TransformFromCopy(pi[4], d1[2]), run_time=.15 * d)
            self.play(TransformFromCopy(pi[6], d1[3:5]), run_time=.2 * d)
            chain = T("chain rule: times minus one", size=30, color=MUTED).next_to(d1[3:5], DOWN, buff=.3)
            self.play(Indicate(d1[3], color=ROSE), FadeIn(chain), run_time=.2 * d)
            self.wait(.08 * d)
            self.play(pi[6].animate.set_opacity(.3), pi[10].animate.set_opacity(1),
                      TransformFromCopy(pi[10], d1[5:7]), FadeIn(d1[7:]), run_time=.17 * d)
            self.wait(.1 * d)

        e1 = at(E(r"K_2 q_1|-|K_2 q_2|+|K_2 q_1|-|P_1|=|0", size=48), W_Y)
        r1 = at(E(r"2K_2 q_1|-|K_2 q_2|=|P_1", size=48), W_Y)
        with self.say("Multiply out: K two q one, minus K two q two, plus K two q one, minus P one, equals zero. The two K two q one terms make two K two q one. So: two K two q one, minus K two q two, equals P one.") as d:
            self.play(FadeOut(chain), *unfocus(), TransformFromCopy(d1[2], e1[0]),
                      TransformFromCopy(d1[3:5], e1[1:5]), TransformFromCopy(d1[5:], e1[5:]), run_time=.4 * d)
            self.play(Indicate(e1[0], color=GOLD), Indicate(e1[4], color=GOLD), run_time=.12 * d)
            self.play(ReplacementTransform(VGroup(e1[0], e1[4]), r1[0]), ReplacementTransform(e1[1], r1[1]),
                      ReplacementTransform(e1[2], r1[2]), FadeOut(e1[3]), FadeOut(e1[5]), FadeOut(e1[8]),
                      ReplacementTransform(e1[7], r1[3]), ReplacementTransform(e1[6], r1[4]), run_time=.2 * d)
            self.wait(.06 * d)
            g1 = glow(r1, GOOD)
            self.play(FadeIn(g1), run_time=.12 * d)
            self.wait(.1 * d)

        # ---------- q2 ----------
        t1 = tray_target(r1, 3, 0)
        self.beat("Now q two. It appears in three springs and one load term. Your turn first: pause and do checkpoint three point one in your guide.",
                  [FadeOut(g1), FadeOut(d1), Transform(r1, t1)], .05, focus([2, 6, 8, 12]), w=(.3, .65))
        self.checkpoint("3.1", "HW 1: take the partial derivative of Pi with respect to q2")

        d2 = at(E(r"\frac{\partial \Pi}{\partial q_2}|=|K_1 q_2|+|K_2(q_2-q_1)|-|K_3(q_3-q_2)|-|(P_2+P_3)|=|0",
                  size=48), D_Y)
        paint(d2, {8: ROSE})
        with self.say("K one gives K one q two. The second K two gives plus K two times q two minus q one. K three gives K three times q three minus q two, times minus one. And the loads give minus P two plus P three.") as d:
            self.play(Write(d2[0:2]), TransformFromCopy(pi[2], d2[2]), run_time=.17 * d)
            self.wait(.03 * d)
            self.play(TransformFromCopy(pi[6], d2[3:5]), run_time=.2 * d)
            self.wait(.05 * d)
            self.play(TransformFromCopy(pi[8], d2[5:7]), run_time=.2 * d)
            self.play(Indicate(d2[5], color=ROSE), run_time=.1 * d)
            self.play(TransformFromCopy(pi[12], d2[7:9]), FadeIn(d2[9:]), run_time=.17 * d)
            self.wait(.08 * d)

        ex = at(E(r"K_1 q_2|+|K_2 q_2|-|K_2 q_1|-|K_3 q_3|+|K_3 q_2|=|P_2+P_3", size=48), W_Y)
        paint(ex, {10: ROSE})
        r2 = at(E(r"-K_2 q_1|+|(K_1+K_2+K_3)\,q_2|-|K_3 q_3|=|P_2+P_3", size=48), W_Y)
        paint(r2, {6: ROSE})
        with self.say("Multiply out and group by unknown: minus K two q one, plus K one plus K two plus K three, times q two, minus K three q three, equals P two plus P three.") as d:
            self.play(*unfocus(), TransformFromCopy(d2[2], ex[0]), TransformFromCopy(d2[3:5], ex[1:5]),
                      TransformFromCopy(d2[5:7], ex[5:9]), TransformFromCopy(d2[7:], ex[9:]), run_time=.25 * d)
            self.wait(.04 * d)
            self.play(ReplacementTransform(VGroup(ex[3], ex[4]), r2[0]), FadeIn(r2[1]),
                      ReplacementTransform(VGroup(ex[0], ex[1], ex[2], ex[7], ex[8]), r2[2]),
                      ReplacementTransform(ex[5], r2[3]), ReplacementTransform(ex[6], r2[4]),
                      ReplacementTransform(ex[9], r2[5]), ReplacementTransform(ex[10], r2[6]), run_time=.25 * d)
            self.play(Circumscribe(r2[2], color=SKY), run_time=.2 * d)
            g2 = glow(r2, GOOD)
            self.play(FadeIn(g2), run_time=.12 * d)
            self.wait(.14 * d)

        # ---------- q3 ----------
        t2 = tray_target(r2, 5, 1)
        d3 = at(E(r"\frac{\partial \Pi}{\partial q_3}|=|K_3(q_3-q_2)|-|P_4|=|0", size=48), D_Y)
        r3 = at(E(r"-K_3 q_2|+|K_3 q_3|=|P_4", size=48), W_Y)
        with self.say("Last, q three. Only K three and P four contain it: K three times q three minus q two, minus P four, equals zero. So minus K three q two, plus K three q three, equals P four.") as d:
            self.play(FadeOut(g2), FadeOut(d2), Transform(r2, t2), *focus([8, 14]), run_time=.15 * d)
            self.play(Write(d3[0:2]), TransformFromCopy(pi[8], d3[2]), run_time=.15 * d)
            self.play(TransformFromCopy(pi[14], d3[3:5]), FadeIn(d3[5:]), run_time=.15 * d)
            self.wait(.12 * d)
            self.play(TransformFromCopy(d3[2], r3[0:3]), FadeIn(r3[3]), TransformFromCopy(d3[4], r3[4]),
                      run_time=.2 * d)
            g3 = glow(r3, GOOD)
            self.play(FadeIn(g3), run_time=.1 * d)
            self.wait(.13 * d)
        t3 = tray_target(r3, 3, 2)
        self.play(FadeOut(g3), FadeOut(d3), Transform(r3, t3), *unfocus(), run_time=1.2)
        self.play(Circumscribe(VGroup(r1, r2, r3), color=LILAC, buff=.2), run_time=1.2)
        self.wait(1)
        self.wipe()
