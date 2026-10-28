"""S08: two springs in a row; the stretch of spring two is a difference (BRIEF.md S08)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts (the series' two-spring numbers): stretch of spring 2 is q2 - q1, and a common shift stores nothing
q1n, q2n = 1.5, 2.5
assert np.isclose(q2n - q1n, 1.0)                 # spring 2 stretch = q2 - q1 = 1.0 mm
assert np.isclose((q2n + .7) - (q1n + .7), q2n - q1n)   # same shift added to both ends: stretch unchanged

D1, D2 = 0.8, 1.8              # picture displacements for q1, q2 (scene units, two_spring_fig's d1, d2)
NX1, NX2, NY = -3.0, 0.0, 2.45  # two_spring_fig default: node 1, node 2 reference positions, spring line


class S08_Two_Springs(VScene):
    budget = 161

    def construct(self):
        # beat 1: the question
        card = qcard("?", T("which way is easier?", size=34))
        card.move_to(ORIGIN)
        self.beat("Last time, one spring, where Newton and energy were equally easy. With more springs, which one is easier? Let's find out, on two springs in a row.",
                  FadeIn(card, shift=UP * .3), .25, card.animate.to_corner(DR, buff=.15), w=(.35, .4))

        # beat 2: the shared figure (identical in S08-S12)
        fig = two_spring_fig()
        nl1 = T("node 1", size=30, color=INK2).move_to(np.array([NX1, NY - 1.3, 0]))
        nl2 = T("node 2", size=30, color=INK2).move_to(np.array([NX2, NY - 1.3, 0]))
        self.beat("A wall, spring one, a junction we'll call node one, spring two, and the end, node two. There's a load on each node, F one and F two, and each node moves right: q one and q two. Those are our unknowns.",
                  [FadeIn(fig.wall), Create(fig.s1), FadeIn(fig.k1)], [FadeIn(fig.n1), FadeIn(nl1)],
                  [Create(fig.s2), FadeIn(fig.k2)], [FadeIn(fig.n2), FadeIn(nl2)],
                  [FadeIn(fig.F1, shift=RIGHT * .2), FadeIn(fig.F2, shift=RIGHT * .2)],
                  [FadeIn(fig.q1), FadeIn(fig.q2)],
                  w=(.12, .1, .12, .1, .26, .3))
        self.remove(*fig.submobjects)
        self.add(fig)

        # beat 3: spring 1 stretches by q1
        eq1 = E(r"\text{stretch}_1|=|q_1", size=48)
        eq1.move_to(np.array([-3.5, -0.3, 0]), aligned_edge=LEFT)
        self.beat("Before anything else we need one fact: how much does each spring stretch? Spring one is easy. Its left end is on the wall, its right end moves q one, so it stretches q one.",
                  .3, Transform(fig, two_spring_fig(d1=D1)), [Indicate(fig.k1, color=LILAC), Indicate(fig.q1)],
                  Write(eq1), FadeIn(glow(eq1[2], SKY)), w=(.2, .15, .2, .15))

        # beat 4: spring 2 stretches by the difference (marked under the spring, clear of the card)
        tick = DashedLine(np.array([NX2 + D1, NY - .15, 0]), np.array([NX2 + D1, NY - 1.95, 0]), color=MUTED)
        dbl = DoubleArrow(np.array([NX2 + D1, NY - 1.8, 0]), np.array([NX2 + D2, NY - 1.8, 0]), buff=0,
                          color=SKY, stroke_width=4, tip_length=.18, max_tip_length_to_length_ratio=.3)
        dlab = E("q_2|-|q_1", size=36)
        dlab.next_to(dbl, RIGHT, buff=.15)
        eq2 = E(r"\text{stretch}_2|=|q_2|-|q_1", size=48)
        eq2.next_to(eq1, DOWN, buff=.5, aligned_edge=LEFT)
        self.beat("Spring two is the one to watch. Both of its ends move. Its left end moves q one, and its right end moves q two. So its stretch is the difference: q two minus q one.",
                  Indicate(fig.k2, color=LILAC), [Indicate(fig.n1), Indicate(fig.q1)], FadeIn(tick),
                  [Transform(fig, two_spring_fig(d1=D1, d2=D2)), Indicate(fig.q2)],
                  [GrowFromCenter(dbl), FadeIn(dlab)], Write(eq2),
                  w=(.1, .17, .08, .2, .2, .25))

        # beat 5: a common shift stores nothing
        note = T("same shift: no stretch", size=32, color=MUTED)
        note.next_to(eq2, DOWN, buff=.55, aligned_edge=LEFT)
        with self.say("If both ends moved the same amount, the spring would just slide along without stretching at all. Only the difference counts.") as d:
            self.play(FadeOut(tick), FadeOut(dbl), FadeOut(dlab), Transform(fig, two_spring_fig()), run_time=.2 * d)
            self.play(Transform(fig, two_spring_fig(d1=.9, d2=.9)), run_time=.35 * d)
            self.play(FadeIn(note), Indicate(fig.k2, color=LILAC), run_time=.2 * d)
            self.play(Circumscribe(VGroup(*eq2[2:]), color=SKY), run_time=.25 * d)
        self.wipe()
