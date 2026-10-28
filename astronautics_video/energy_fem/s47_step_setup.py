"""S47: the stepped bar problem (BRIEF.md S47)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: every number the narration says, and the solution it leads to (BRIEF facts, Episode 7)
E_AL, A1, A2, L_EL, K_SP, P_LOAD = 70000, 200, 100, 500, 14000, 7000
assert np.isclose(E_AL * A1 / L_EL, 28000) and np.isclose(E_AL * A2 / L_EL, 14000)
_q = np.linalg.solve(np.array([[42000., -14000.], [-14000., 28000.]]), [P_LOAD, 0.])
assert np.allclose(_q, [0.2, 0.1])
assert np.isclose(P_LOAD + 28000 * (0 - _q[0]) + (-K_SP * _q[1]), 0)


class S47_Step_Setup(VScene):
    budget = 158

    def construct(self):
        g = stepped_bar()

        # beat 1: wall, thick element 1, thin element 2
        self.beat("Let's do a brand new problem from start to finish, with real numbers. An aluminum bar, "
                  "fixed to a wall on the left, made of two pieces: a thick one, then a thin one.",
                  .15, Create(g.wl), [FadeIn(g.e1), FadeIn(g.elabs[0])], [FadeIn(g.e2), FadeIn(g.elabs[1])])

        # beat 2: spring, right wall, the load, the question
        q_lines = T("How does the load split between the two walls?", size=40)
        qc = panel(q_lines, color=ROSE)
        qc.move_to([0, -1.2, 0])
        self.beat("Then a spring connects the end of the thin piece to a second wall on the right. And a load of "
                  "seven thousand newtons pushes right, at the step between the two pieces. The question: how "
                  "does that load divide between the two walls?",
                  [Create(g.sp), FadeIn(g.wr)], .1, [FadeIn(g.load, shift=.3 * RIGHT), FadeIn(g.plab)],
                  .15, FadeIn(qc, shift=.2 * UP))

        # beat 3: data card part 1
        rows = [E(r"E|=|70{,}000\ \text{N/mm}^2", size=50),
                E(r"A_1|=|200\ \text{mm}^2", size=50),
                E(r"A_2|=|100\ \text{mm}^2", size=50),
                E(r"l|=|500\ \text{mm (each)}", size=50),
                E(r"K|=|14{,}000\ \text{N/mm}", size=50)]
        r1 = VGroup(*rows[:3]).arrange(RIGHT, buff=0.9)
        rows[3].next_to(rows[0], DOWN, buff=0.4, aligned_edge=LEFT)
        rows[4].next_to(rows[3], RIGHT, buff=0.9).align_to(rows[1], LEFT).match_y(rows[3])
        col = VGroup(r1, rows[3], rows[4])
        card = panel(col)
        fit(card, 13.4, 2.2)
        card.move_to([0, -2.95, 0])
        self.beat("The material first. Aluminum: E is seventy thousand newtons per square millimeter. The thick "
                  "piece has an area of two hundred square millimeters, the thin one one hundred.",
                  [FadeIn(card[0]), FadeIn(rows[0])], .1,
                  [FadeIn(rows[1]), Indicate(g.e1, color=LILAC, scale_factor=1.03)], .1,
                  [FadeIn(rows[2]), Indicate(g.e2, color=LILAC, scale_factor=1.06)], .15)

        # beat 4: data card part 2
        self.beat("Each piece is five hundred millimeters long. And the spring's stiffness is fourteen thousand "
                  "newtons per millimeter.",
                  [FadeIn(rows[3]), Create(g.dims)], .1,
                  [FadeIn(rows[4]), FadeIn(g.klab), Indicate(g.sp, color=LILAC)], .2)

        # beat 5: nodes, q1 q2, goals
        def goal(word, tex, color):
            return VGroup(T(word, size=36), M(tex, size=58, color=color)).arrange(RIGHT, buff=0.2)
        goal_rows = VGroup(goal("displacements", r"q_1,\ q_2", SKY), goal("stresses", r"\sigma_1,\ \sigma_2", ACCENT),
                           goal("wall reactions", r"R_0,\ R_3", ROSE)).arrange(RIGHT, buff=0.7)
        goals = panel(goal_rows)
        fit(goals, 13.6, 1.2)
        goals.move_to(qc)
        self.beat("Number the nodes: zero at the left wall, one at the step, two at the end of the thin piece, "
                  "three at the right wall. We want the displacements, the stresses, and the wall reactions.",
                  LaggedStart(*[FadeIn(VGroup(g.nodes[i], g.nums[i]), scale=1.3) for i in range(4)],
                              lag_ratio=.6),
                  FadeIn(g.qs, shift=.2 * RIGHT), .05, [FadeOut(qc), FadeIn(goals)], .2,
                  w=(.45, .2, .35))
        self.wipe()
