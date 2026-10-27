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

FY = 0.5                       # figure height
WX, X1, X2 = -6.2, -1.6, 2.8   # wall face, node 1, node 2 (reference positions)
D1, D2 = 0.6, 1.5              # picture displacements for q1, q2 (screen units)


class S08_Two_Springs(VScene):
    budget = 161

    def construct(self):
        t1, t2 = ValueTracker(0), ValueTracker(0)
        p1 = lambda: np.array([X1 + t1.get_value(), FY, 0])
        p2 = lambda: np.array([X2 + t2.get_value(), FY, 0])
        wp = np.array([WX, FY, 0])

        # beat 1: the question
        card = qcard("?", T("which way is easier?", size=34))
        card.move_to(ORIGIN)
        self.beat("Last time, one spring, where Newton and energy were equally easy. With more springs, which one is easier? Let's find out, on two springs in a row.",
                  FadeIn(card, shift=UP * .3), .25, card.animate.to_corner(UR, buff=.3), w=(.35, .4))

        # beat 2: the figure
        wl = wall(wp, side=LEFT)
        s1 = always_redraw(lambda: spring(wp, p1()))
        s2 = always_redraw(lambda: spring(p1(), p2()))
        k1 = E("k_1", size=40)
        k1.add_updater(lambda m: m.move_to((wp + p1()) / 2 + DOWN * .55))
        k2 = E("k_2", size=40)
        k2.add_updater(lambda m: m.move_to((p1() + p2()) / 2 + DOWN * .55))
        n1 = node(p1())
        n1.add_updater(lambda m: m.move_to(p1()))
        n2 = node(p2())
        n2.add_updater(lambda m: m.move_to(p2()))
        nl1 = T("node 1", size=30, color=INK2)
        nl1.add_updater(lambda m: m.next_to(p1(), DOWN, buff=1.25))
        nl2 = T("node 2", size=30, color=INK2)
        nl2.add_updater(lambda m: m.next_to(p2(), DOWN, buff=1.25))
        f1 = force(p1() + RIGHT * .1 + UP * .5, length=.9, label="F_1")
        f1c = f1.get_center() - p1()
        f1.add_updater(lambda m: m.move_to(p1() + f1c))
        f2 = force(p2() + RIGHT * .1, label="F_2")
        f2c = f2.get_center() - p2()
        f2.add_updater(lambda m: m.move_to(p2() + f2c))
        d1 = disp(np.array([X1, FY, 0]), label="q_1")
        d2 = disp(np.array([X2, FY, 0]), label="q_2")
        self.beat("A wall, spring one, a junction we'll call node one, spring two, and the end, node two. There's a load on each node, F one and F two, and each node moves right: q one and q two. Those are our unknowns.",
                  [FadeIn(wl), Create(s1), FadeIn(k1)], [FadeIn(n1), FadeIn(nl1)],
                  [Create(s2), FadeIn(k2)], [FadeIn(n2), FadeIn(nl2)],
                  [FadeIn(f1, shift=RIGHT * .2), FadeIn(f2, shift=RIGHT * .2)],
                  [FadeIn(d1), FadeIn(d2)],
                  w=(.12, .1, .12, .1, .26, .3))

        # beat 3: spring 1 stretches by q1
        eq1 = E(r"\text{stretch}_1|=|q_1", size=48)
        eq1.move_to(np.array([-2.0, -1.9, 0]), aligned_edge=LEFT)
        self.beat("Before anything else we need one fact: how much does each spring stretch? Spring one is easy. Its left end is on the wall, its right end moves q one, so it stretches q one.",
                  .3, t1.animate.set_value(D1), [Indicate(k1, color=LILAC), Indicate(d1)], Write(eq1),
                  FadeIn(glow(eq1[2], SKY)), w=(.2, .15, .2, .15))

        # beat 4: spring 2 stretches by the difference
        tick = DashedLine(np.array([X2 + D1, FY - .3, 0]), np.array([X2 + D1, FY + 1.45, 0]), color=MUTED)
        dbl = DoubleArrow(np.array([X2 + D1, FY + 1.2, 0]), np.array([X2 + D2, FY + 1.2, 0]), buff=0,
                          color=SKY, stroke_width=4, tip_length=.18, max_tip_length_to_length_ratio=.3)
        dlab = E("q_2|-|q_1", size=36)
        dlab.next_to(dbl, UP, buff=.12)
        eq2 = E(r"\text{stretch}_2|=|q_2|-|q_1", size=48)
        eq2.next_to(eq1, DOWN, buff=.5, aligned_edge=LEFT)
        self.beat("Spring two is the one to watch. Both of its ends move. Its left end moves q one, and its right end moves q two. So its stretch is the difference: q two minus q one.",
                  Indicate(k2, color=LILAC), [Indicate(n1), Indicate(d1)], FadeIn(tick),
                  [t2.animate.set_value(D2), Indicate(d2)], [GrowFromCenter(dbl), FadeIn(dlab)], Write(eq2),
                  w=(.1, .17, .08, .2, .2, .25))

        # beat 5: a common shift stores nothing
        note = T("same shift: no stretch", size=32, color=MUTED)
        note.move_to(np.array([0.9, FY + 1.5, 0]))
        with self.say("If both ends moved the same amount, the spring would just slide along without stretching at all. Only the difference counts.") as d:
            self.play(FadeOut(tick), FadeOut(dbl), FadeOut(dlab), t1.animate.set_value(0), t2.animate.set_value(0),
                      run_time=.2 * d)
            self.play(t1.animate.set_value(.9), t2.animate.set_value(.9), run_time=.35 * d)
            self.play(FadeIn(note), Indicate(k2, color=LILAC), run_time=.2 * d)
            self.play(Circumscribe(VGroup(*eq2[2:]), color=SKY), run_time=.25 * d)
        for m in (s1, s2, k1, k2, n1, n2, nl1, nl2, f1, f2):
            m.clear_updaters()
        self.wipe()
