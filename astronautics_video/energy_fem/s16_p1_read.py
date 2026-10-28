"""S16: reading the HW P1 figure (BRIEF.md S16)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# The HW P1 figure comes from the kit: efem.hw_figure (S16-S22 all redraw it).

# facts: the figure as the brief reads it (4 loads, 3 unknowns, stretches) and the brief's sanity solution
K1 = K2 = K3 = 100.0
P1 = P2 = P3 = P4 = 30.0
q2 = (P1 + 2 * (P2 + P3 + P4)) / (2 * K1 + K2)
q1 = ((K1 + K2) * P1 + K2 * (P2 + P3 + P4)) / (K2 * (2 * K1 + K2))
q3 = q2 + P4 / K3
assert np.allclose([q1, q2, q3], [0.5, 0.7, 1.0])
A = np.array([[2 * K2, -K2, 0], [-K2, K1 + K2 + K3, -K3], [0, -K3, K3]])
assert np.allclose(A @ [q1, q2, q3], [P1, P2 + P3, P4])
# rigid bar: the three spring ends on it (K1 right end, second K2 right end, K3 left end) all move q2
assert np.isclose(K1 * q2 + K2 * q1, 4 * 30.0)


class S16_P1_Read(VScene):
    budget = 191

    def construct(self):
        fig = hw_figure()
        c0, S, at = fig.get_center(), min(1.2, (14.2 - 0.8) / fig.width), 0.3 * DOWN   # 0.4 margin each side
        fig.scale(S).move_to(at)
        mp = lambda m: m.scale(S, about_point=c0).shift(at - c0)      # kit coordinates -> on-screen figure
        head = T("Homework 6, Problem 1", size=36, color=ACCENT, weight=BOLD)
        task = TX(r"Stationary principle: find $q_1$, $q_2$, $q_3$ in terms of the $K$'s and $P$'s", size=32)
        stmt = VGroup(head, task).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.35)

        structure = [fig.wall, fig.k1, fig.k2a, fig.J, fig.k2b, fig.bar, fig.k3, fig.O]
        klabs = [fig.klab["K1"], fig.klab["K2a"], fig.klab["K3"]]
        loads = [VGroup(fig.stem, fig.P[1], fig.Plab[1])] + [VGroup(fig.P[i], fig.Plab[i]) for i in (2, 3, 4)]

        # 1: problem statement, then the figure builds left to right; the statement shrinks away
        with self.say("Here's problem one. Use the stationary principle to find q one, q two and q three, in terms "
                      "of the spring stiffnesses and the loads. Let's read the figure slowly, piece by piece.") as d:
            self.play(FadeIn(head, shift=0.2 * DOWN), Write(task), run_time=.22 * d)
            self.wait(.08 * d)
            self.play(LaggedStart(*[FadeIn(m) if m is fig.wall else Create(m) for m in structure],
                                  lag_ratio=.35), run_time=.35 * d)
            self.play(LaggedStart(*[FadeIn(m) for m in klabs + loads], lag_ratio=.2), run_time=.18 * d)
            self.play(stmt.animate.scale(.2).to_corner(UR).set_opacity(0), run_time=.12 * d)
            self.remove(stmt)

        # 2: K1 and the bar; q2 appears
        g_k1, g_bar = glow(fig.k1, LILAC), glow(fig.bar, INK)
        self.beat("On the left, a wall. Along the top, spring K one runs from the wall to this tall vertical bar. "
                  "The bar moves to the right by q two.",
                  Indicate(fig.wall, color=INK, scale_factor=1.05), .05,
                  [FadeIn(g_k1), Indicate(fig.klab["K1"], color=LILAC)], .1,
                  FadeIn(g_bar), .05, GrowFromEdge(fig.q[2], LEFT), .2,
                  w=(.15, .25, .12, .13))

        # 3: the bottom chain; the unlabeled spring gets an assumed K2 tag that resolves
        g_k2a, g_k2b = glow(fig.k2a, LILAC), glow(fig.k2b, LILAC)
        guess = M(r"K_2\,?", size=40 * S, color=MUTED).next_to(fig.k2b, UP, buff=0.25)
        box = DashedVMobject(SurroundingRectangle(guess, buff=0.1, color=MUTED, corner_radius=0.08), num_dashes=24)
        note = T("assumed", size=30, color=MUTED).next_to(box, UP, buff=0.08)
        k2b_lab = E("K_2", size=40 * S).move_to(guess, aligned_edge=LEFT)
        with self.say("Along the bottom, spring K two runs from the wall to a junction that moves q one. Then a "
                      "second spring runs from that junction to the bar. The figure doesn't label that second "
                      "spring. We'll take it to be another K two, since the label sits right between them. If your "
                      "instructor says otherwise, only that one stiffness changes.") as d:
            self.play(FadeOut(g_k1), FadeOut(g_bar), FadeIn(g_k2a), Indicate(fig.klab["K2a"], color=LILAC),
                      run_time=.08 * d)
            self.play(Indicate(fig.J, color=SKY, scale_factor=1.8), GrowFromEdge(fig.q[1], LEFT), run_time=.08 * d)
            self.wait(.04 * d)
            self.play(FadeIn(g_k2b), run_time=.08 * d)
            self.wait(.06 * d)
            self.play(Create(box), FadeIn(guess), FadeIn(note), run_time=.1 * d)
            self.wait(.16 * d)
            box2 = DashedVMobject(SurroundingRectangle(k2b_lab, buff=0.1, color=LILAC, corner_radius=0.08),
                                  num_dashes=20)
            self.play(ReplacementTransform(guess, k2b_lab), ReplacementTransform(box, box2), run_time=.12 * d)
            box = box2
            self.wait(.14 * d)
            self.play(Indicate(VGroup(box, k2b_lab), color=LILAC, scale_factor=1.1), run_time=.08 * d)
            self.wait(.06 * d)
        tag = VGroup(box, note, k2b_lab)

        # 4: K3 and q3
        g_k3 = glow(fig.k3, LILAC)
        self.beat("On the right, spring K three joins the bar to an outer point that moves q three.",
                  [FadeOut(g_k2a), FadeOut(g_k2b), FadeIn(g_k3), Indicate(fig.klab["K3"], color=LILAC)], .1,
                  [Indicate(fig.O, color=SKY, scale_factor=1.8), GrowFromEdge(fig.q[3], LEFT)], .2,
                  w=(.3, .4))

        # 5: the loads pulse in turn
        with self.say("The loads: P one pulls the junction, P two and P three both push on the bar, and P four "
                      "pulls the outer point. All to the right.") as d:
            self.play(FadeOut(g_k3), run_time=.06 * d)
            for ld in loads:
                self.play(Indicate(ld, color=ROSE, scale_factor=1.25), run_time=.1 * d)
                self.wait(.04 * d)
            arrows = VGroup(*[fig.P[i] for i in (1, 2, 3, 4)])
            self.play(LaggedStart(*[ApplyMethod(a.shift, .25 * RIGHT, rate_func=there_and_back) for a in arrows],
                                  lag_ratio=0), run_time=.14 * d)
            self.wait(.18 * d)

        # 6: rigid bar slides as one piece; its three attachment points glow SKY with q2
        dq = 0.55
        movers = VGroup(fig.bar, fig.P[2], fig.P[3], fig.Plab[2], fig.Plab[3])
        new = [mp(m) for m in fig.rebuild_springs(dq2=dq / S)]
        ends = [fig.pts["b_top"], fig.pts["b_bot"], fig.pts["b_mid"]]
        dots = VGroup(*[Dot(at + S * (p - c0) + dq * RIGHT, radius=0.1, color=SKY).set_z_index(5) for p in ends])
        dlabs = VGroup(*[E("q_2", size=40).next_to(dt, d_, buff=0.1).set_z_index(5)
                         for dt, d_ in zip(dots, (UL, UL, DR))])
        halos = VGroup(*[glow(dt, SKY) for dt in dots])
        with self.say("One assumption about the bar: it's rigid and slides without tilting. So every spring "
                      "attached to it moves exactly q two at that end.") as d:
            self.play(Indicate(fig.bar, color=INK, scale_factor=1.03), run_time=.12 * d)
            self.play(movers.animate.shift(dq * RIGHT), fig.q[2].animate.shift(dq * RIGHT),
                      Transform(fig.k1, new[0]), Transform(fig.k2b, new[2]), Transform(fig.k3, new[3]),
                      tag.animate.shift(dq * RIGHT / 2), run_time=.2 * d)
            self.wait(.06 * d)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(h), GrowFromCenter(dt)) for h, dt in zip(halos, dots)],
                                  lag_ratio=.4), run_time=.2 * d)
            self.play(LaggedStart(*[FadeIn(l, shift=.1 * UP) for l in dlabs], lag_ratio=.3), run_time=.16 * d)
            self.wait(.26 * d)
        self.wipe()
