"""S17: the stretch of every spring in HW P1 (BRIEF.md S17)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the stretches (right end minus left end) with the brief's sanity numbers (all K = 100, all P = 30)
Kv, Pv = 100.0, 30.0
q1, q2, q3 = 0.5, 0.7, 1.0
st = {"K1": q2 - 0, "K2a": q1 - 0, "K2b": q2 - q1, "K3": q3 - q2}
assert np.isclose(st["K1"], 0.7) and np.isclose(st["K2a"], 0.5)
assert np.isclose(st["K2b"], 0.2) and np.isclose(st["K3"], 0.3)
# Newton checks with these stretches: junction, bar, outer node, whole system
assert np.isclose(-Kv * st["K2a"] + Kv * st["K2b"] + Pv, 0)
assert np.isclose(-Kv * st["K1"] - Kv * st["K2b"] + Kv * st["K3"] + 2 * Pv, 0)
assert np.isclose(-Kv * st["K3"] + Pv, 0)
assert np.isclose(Kv * st["K1"] + Kv * st["K2a"], 4 * Pv)


def table():
    head_txt = ["spring", "left end", "right end", "stretch"]
    rows_tex = [["K_1", "0", "q_2", "q_2"],
                ["K_2", "0", "q_1", "q_1"],
                ["K_2", "q_1", "q_2", "q_2|-|q_1"],
                ["K_3", "q_2", "q_3", "q_3|-|q_2"]]
    xs = [0.0, 1.5, 3.0, 4.75]
    pitch = 0.95
    head = VGroup(*[VGroup(*[T(w, size=32, color=INK2) for w in t.split()]).arrange(DOWN, buff=0.12)
                    .move_to([x, 0.15, 0]) for t, x in zip(head_txt, xs)])
    rule = Line([xs[0] - 0.8, -0.42, 0], [xs[-1] + 1.05, -0.42, 0], color=HAIR, stroke_width=2)
    rows = VGroup()
    for r, cells in enumerate(rows_tex):
        y = -(r + 1) * pitch - 0.05
        row = VGroup(*[E(c, size=46).move_to([x, y, 0]) for c, x in zip(cells, xs)])
        rows.add(row)
    tab = VGroup(head, rule, rows)
    fit(tab, 6.4, 6.0)
    tab.move_to([3.6, -0.2, 0])
    tab.head, tab.rule, tab.rows = head, rule, rows
    return tab


class S17_P1_Stretches(VScene):
    budget = 130

    def construct(self):
        fig = hw_figure(k2b_label=True)   # shared HW P1 figure (S16-S22); we treat the unlabeled spring as K2
        fig.scale(0.6)
        fig.move_to([-3.65, -0.2, 0]).align_to(np.array([-6.85, 0, 0]), LEFT)
        tab = table()
        print('FIGX', fig.get_left()[0], fig.get_right()[0], 'TABX', tab.get_left()[0])
        s1, s2a, s2b, s3 = fig.k1, fig.k2a, fig.k2b, fig.k3
        dq1, dq2, dq3 = fig.q[1], fig.q[2], fig.q[3]
        rows = tab.rows

        # 1. header
        self.beat("Step one, the one that decides everything: the stretch of each spring. Remember, a stretch is the right end's displacement minus the left end's.",
                  FadeIn(fig), .1, FadeIn(tab.head, shift=DOWN * 0.2), Create(tab.rule), .15,
                  Indicate(tab.head[2], color=SKY), Indicate(tab.head[1], color=SKY), Indicate(tab.head[3]),
                  w=(.3, .2, .15, .15, .1, .1))

        # 2. K1: wall to bar
        g1 = glow(s1, LILAC)
        self.beat("K one: left end on the wall, which doesn't move, right end on the bar, which moves q two. Stretch: q two.",
                  [FadeIn(g1), FadeIn(rows[0][0])], Indicate(fig.wall, color=MUTED), FadeIn(rows[0][1]),
                  Indicate(dq2), FadeIn(rows[0][2]), .1, FadeIn(rows[0][3]), Circumscribe(rows[0][3], color=SKY),
                  w=(.12, .16, .1, .16, .12, .12, .22))

        # 3. both K2 springs
        g2a, g2b = glow(s2a, LILAC), glow(s2b, LILAC)
        with self.say("The first K two: wall to the junction. Stretch: q one. The second K two: junction to bar. Its left end moves q one, its right end q two. Stretch: q two minus q one.") as d:
            self.play(FadeOut(g1), FadeIn(g2a), FadeIn(rows[1][0]), run_time=.08 * d)
            self.play(Indicate(fig.wall, color=MUTED), FadeIn(rows[1][1]), run_time=.08 * d)
            self.play(Indicate(dq1), FadeIn(rows[1][2]), run_time=.08 * d)
            self.play(FadeIn(rows[1][3]), run_time=.08 * d)
            self.wait(.04 * d)
            self.play(FadeOut(g2a), FadeIn(g2b), FadeIn(rows[2][0]), run_time=.1 * d)
            self.wait(.06 * d)
            self.play(Indicate(dq1), FadeIn(rows[2][1]), run_time=.1 * d)
            self.play(Indicate(dq2), FadeIn(rows[2][2]), run_time=.1 * d)
            self.wait(.06 * d)
            self.play(FadeIn(rows[2][3]), run_time=.1 * d)
            self.play(Circumscribe(rows[2][3], color=SKY), run_time=.12 * d)

        # 4. K3
        g3 = glow(s3, LILAC)
        self.beat("K three: bar to the outer point. Stretch: q three minus q two.",
                  [FadeOut(g2b), FadeIn(g3), FadeIn(rows[3][0])],
                  [Indicate(dq2), FadeIn(rows[3][1])], [Indicate(dq3), FadeIn(rows[3][2])],
                  FadeIn(rows[3][3]), .1, w=(.25, .25, .25, .25))

        # 5. the key step: spotlight the stretch column, hold
        col = VGroup(tab.head[3], *[r[3] for r in rows])
        box = SurroundingRectangle(col, color=SKY, buff=0.18, corner_radius=0.08, stroke_width=4)
        self.beat("This is the step to get right, so let's say it once more: a spring between two moving points stretches by the difference of their displacements. Get these four right, and the rest is just algebra.",
                  FadeOut(g3), Create(box), self.spotlight(box), .1, col.animate.set_opacity(1), .45,
                  w=(.15, .25, .35, .25), style="slower and deliberate, stressing the key words")
        self.wipe()
