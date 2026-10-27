"""S16: reading the HW P1 figure (BRIEF.md S16)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# ---------------------------------------------------------------------------------------------------------------
# The HW P1 figure (S16-S22 all redraw it).  Layout, in frame units, before `at` shifts it:
#   wall face x = -5.8 (hatching left of it), y in [-2, 2]
#   top row    y = +0.9 : K1   wall -> bar left face (x = 0.9)
#   bottom row y = -1.1 : K2a  wall -> junction J (x = -2.6, moves q1);  K2b  J -> bar left face
#   middle row y =  0.0 : K3   bar right face (x = 1.4) -> outer node O (x = 4.4, moves q3)
#   bar: rigid vertical rectangle x in [0.9, 1.4], y in [-2, 2] (moves q2)
#   loads (ROSE, all +x): P1 starts below J on a short stem; P2 (y = +1.7) and P3 (y = -1.7) end on the bar's
#   left face; P4 starts at O.  Displacements (SKY): q1 under the P1 stem, q2 under the bar, q3 under O.
# Returned VGroup has named parts: wall, k1, k2a, k2b, k3, bar, J, O, stem, P (dict 1-4), Plab, q (dict 1-3),
# klab (dict "K1","K2a","K3"; K2b has none: the figure leaves it unlabeled), and `pts` (anchor points, shifted).
# `fig.rebuild_springs(dq2=0, dq1=0, dq3=0)` returns new spring mobjects for a displaced state.
HW_WALL_X, HW_BAR_X0, HW_BAR_X1, HW_J_X, HW_O_X = -5.8, 0.9, 1.4, -2.6, 4.4
HW_TOP_Y, HW_BOT_Y, HW_MID_Y, HW_BAR_H = 0.9, -1.1, 0.0, 4.0


def hw_figure(at=ORIGIN, k2b_label=False):
    o = np.array(at, dtype=float)
    P = lambda x, y: o + np.array([x, y, 0.0])
    pts = dict(w_top=P(HW_WALL_X, HW_TOP_Y), w_bot=P(HW_WALL_X, HW_BOT_Y), b_top=P(HW_BAR_X0, HW_TOP_Y),
               b_bot=P(HW_BAR_X0, HW_BOT_Y), b_mid=P(HW_BAR_X1, HW_MID_Y), J=P(HW_J_X, HW_BOT_Y),
               O=P(HW_O_X, HW_MID_Y))
    g = VGroup()
    g.pts = pts
    g.wall = wall(P(HW_WALL_X, 0), side=LEFT, h=HW_BAR_H)
    g.k1 = spring(pts["w_top"], pts["b_top"], coils=7)
    g.k2a = spring(pts["w_bot"], pts["J"], coils=5)
    g.k2b = spring(pts["J"], pts["b_bot"], coils=5)
    g.k3 = spring(pts["b_mid"], pts["O"], coils=5)
    g.bar = bar(HW_BAR_X0, HW_BAR_X1, h=HW_BAR_H).shift(o)
    g.J = node(pts["J"])
    g.O = node(pts["O"])
    lab = lambda tex, m: E(tex, size=36).next_to(m, UP, buff=0.12)
    g.klab = {"K1": lab("K_1", g.k1), "K2a": lab("K_2", g.k2a), "K3": lab("K_3", g.k3)}
    if k2b_label:
        g.klab["K2b"] = lab("K_2", g.k2b)
    # loads
    g.stem = Line(pts["J"], pts["J"] + 0.5 * DOWN, color=INK2, stroke_width=3)
    g.P = {1: force(pts["J"] + 0.5 * DOWN, RIGHT, length=0.8),
           2: force(P(HW_BAR_X0, 1.7), RIGHT, length=0.9, tail=True),
           3: force(P(HW_BAR_X0, -1.7), RIGHT, length=0.9, tail=True),
           4: force(pts["O"], RIGHT, length=0.9)}
    g.Plab = {1: E("P_1", size=36).next_to(g.P[1], RIGHT, buff=0.1),
              2: E("P_2", size=36).next_to(g.P[2], LEFT, buff=0.1),
              3: E("P_3", size=36).next_to(g.P[3], LEFT, buff=0.1),
              4: E("P_4", size=36).next_to(g.P[4], RIGHT, buff=0.1)}
    # displacements
    g.q = {1: disp(pts["J"] + 0.5 * DOWN, label="q_1", below=0.5),
           2: disp(P((HW_BAR_X0 + HW_BAR_X1) / 2, -HW_BAR_H / 2), label="q_2", below=0.4),
           3: disp(pts["O"], label="q_3", below=0.45)}
    g.add(g.wall, g.k1, g.k2a, g.k2b, g.k3, g.bar, g.J, g.O, *g.klab.values(), g.stem,
          *g.P.values(), *g.Plab.values(), *g.q.values())

    def rebuild_springs(dq1=0.0, dq2=0.0, dq3=0.0):
        s = lambda d: d * RIGHT
        return (spring(pts["w_top"], pts["b_top"] + s(dq2), coils=7),
                spring(pts["w_bot"], pts["J"] + s(dq1), coils=5),
                spring(pts["J"] + s(dq1), pts["b_bot"] + s(dq2), coils=5),
                spring(pts["b_mid"] + s(dq2), pts["O"] + s(dq3), coils=5))
    g.rebuild_springs = rebuild_springs
    return g


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
        fig = hw_figure(at=0.35 * DOWN)
        head = T("Homework 6, Problem 1", size=36, color=ACCENT, weight=BOLD)
        task = TX(r"Stationary principle: find $q_1$, $q_2$, $q_3$ in terms of the $K$'s and $P$'s", size=32)
        tint(task, [])
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
                  w=(.15, .05, .2, .1, .15, .05, .15, .15))

        # 3: the bottom chain; the unlabeled spring gets an assumed K2 tag that resolves
        g_k2a, g_k2b = glow(fig.k2a, LILAC), glow(fig.k2b, LILAC)
        guess = M(r"K_2\,?", size=36, color=MUTED).next_to(fig.k2b, UP, buff=0.12)
        box = DashedVMobject(SurroundingRectangle(guess, buff=0.1, color=MUTED, corner_radius=0.08), num_dashes=24)
        note = T("assumed", size=26, color=MUTED).next_to(box, UP, buff=0.08)
        k2b_lab = E("K_2", size=36).move_to(guess, aligned_edge=LEFT)
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
            self.play(ReplacementTransform(guess[0][0:2], k2b_lab[0]), FadeOut(guess[0][2:]),
                      box.animate.set_color(LILAC), run_time=.12 * d)
            self.wait(.14 * d)
            self.play(Indicate(VGroup(box, k2b_lab), color=LILAC, scale_factor=1.1), run_time=.08 * d)
            self.wait(.06 * d)
        tag = VGroup(box, note, k2b_lab)

        # 4: K3 and q3
        g_k3 = glow(fig.k3, LILAC)
        self.beat("On the right, spring K three joins the bar to an outer point that moves q three.",
                  [FadeOut(g_k2a), FadeOut(g_k2b), FadeIn(g_k3), Indicate(fig.klab["K3"], color=LILAC)], .1,
                  [Indicate(fig.O, color=SKY, scale_factor=1.8), GrowFromEdge(fig.q[3], LEFT)], .2,
                  w=(.25, .1, .3, .35))

        # 5: the loads pulse in turn
        with self.say("The loads: P one pulls the junction, P two and P three both push on the bar, and P four "
                      "pulls the outer point. All to the right.") as d:
            self.play(FadeOut(g_k3), run_time=.06 * d)
            for i, (a, b) in zip((1, 2, 3, 4), ((.1, .2), (.32, .42), (.44, .54), (.6, .7))):
                self.play(Indicate(loads[i - 1], color=ROSE, scale_factor=1.25), run_time=.1 * d)
                self.wait(.04 * d)
            arrows = VGroup(*[fig.P[i] for i in (1, 2, 3, 4)])
            self.play(LaggedStart(*[ApplyMethod(a.shift, .25 * RIGHT, rate_func=there_and_back) for a in arrows],
                                  lag_ratio=0), run_time=.14 * d)
            self.wait(.18 * d)

        # 6: rigid bar slides as one piece; its three attachment points glow SKY with q2
        dq = 0.55
        movers = VGroup(fig.bar, fig.P[2], fig.P[3], fig.Plab[2], fig.Plab[3])
        new = fig.rebuild_springs(dq2=dq)
        ends = [fig.pts["b_top"], fig.pts["b_bot"], fig.pts["b_mid"]]
        dots = VGroup(*[Dot(p + dq * RIGHT, radius=0.1, color=SKY).set_z_index(5) for p in ends])
        dlabs = VGroup(*[E("q_2", size=32).next_to(dt, d_, buff=0.12).set_z_index(5)
                         for dt, d_ in zip(dots, (UR, UR, UR))])
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
