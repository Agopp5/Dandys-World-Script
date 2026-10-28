"""S58: HW P2 part c, the reaction from the constrained row (BRIEF.md S58)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# ---- facts (HW P2): assert every number the scene shows ----
E_mod, A_bar, L_bar = 10e3, 2.0, 40.0
EA = E_mod * A_bar
assert np.isclose(EA, 20000)
l_el = L_bar / 2
k_el = EA / l_el
assert np.isclose(k_el, 1000)
c = -5.0
Q = c * l_el / 2
assert np.isclose(Q, -50)
P1, P2 = 50.0, 100.0
Kg = k_el * np.array([[1, -1, 0], [-1, 2, -1], [0, -1, 1]], float)
Ff = np.array([Q + Q + P1, Q + P2])            # free rows 1, 2: {-50, 50}
assert np.allclose(Ff, [-50, 50])
q1, q2 = np.linalg.solve(Kg[1:, 1:], Ff)
assert np.isclose(q1, 0) and np.isclose(q2, 0.05)
q0 = 0.0
# constrained row 0: 1000 q0 - 1000 q1 = R - 50
R = k_el * q0 - k_el * q1 + 50
assert np.isclose(R, 50)
assert np.isclose(-c * L_bar, 200) and np.isclose(5 * 40, 200)
assert np.isclose(R + P1 + P2 + c * L_bar, 0)      # 50 + 50 + 100 - 200 = 0

# ---- the homework bar, drawn as in S54/S55 ----
YB = 2.6             # bar centerline (hw2_bar y)
XW = -6.0            # wall face (hw2_bar x0)
HB = 0.6


def load(x, label, y=YB, length=1.0):
    """Rightward ROSE load arrow on the bar centerline, label (size 40) above it."""
    a = Arrow([x, y, 0], [x + length, y, 0], buff=0, color=ROSE, stroke_width=7,
              max_tip_length_to_length_ratio=0.3).set_z_index(3)
    lab = M(label, size=40, color=ROSE)
    lab.next_to([x + 0.42, y + HB / 2, 0], UP, buff=0.12, aligned_edge=LEFT)
    lab.align_to([x + 0.42, 0, 0], LEFT)
    return VGroup(a, lab)


class S58_P2_Reaction(VScene):
    budget = 131

    def construct(self):
        fig = hw2_bar(y=YB, x0=XW)
        self.add(fig)

        # beat 1: the set-aside row 0 slides back
        row = E(r"1000|\begin{bmatrix}1 & -1 & 0\end{bmatrix}|\begin{Bmatrix}q_0\\ q_1\\ q_2\end{Bmatrix}|=|R|-|50",
                size=48)
        paint(row, {0: LILAC, 1: LILAC, 2: SKY, 6: ROSE})
        rtag = T("row 0", size=36, color=MUTED)
        rowg = VGroup(rtag, row).arrange(RIGHT, buff=0.6).move_to([0, 0.0, 0])
        start = rowg.copy().scale(0.6).move_to([3.2, -3.3, 0]).set_opacity(0.35)
        self.beat("Part c asks for the reaction using the constrained equation. That's the row we set aside: row "
                  "zero. Your turn: pause and do checkpoint eight point two in your guide, and find the reaction.",
                  FadeIn(start), .1, ReplacementTransform(start, rowg), Circumscribe(row, color=ACCENT), .3,
                  w=(.12, .3, .18))
        self.checkpoint("8.2", "HW 2: find the wall reaction from the constrained row")

        # beat 2: write it out, both q's are zero
        l1 = E(r"1000\,|q_0|-|1000\,|q_1|=|R|-|50", size=52)
        paint(l1, {0: LILAC, 1: SKY, 3: LILAC, 4: SKY, 6: ROSE})
        l1.move_to([0, -1.7, 0])
        l2 = E(r"0|=|R|-|50", size=52)
        paint(l2, {2: ROSE})
        l2.move_to([0, -2.9, 0])
        l2.shift((l1[5].get_center()[0] - l2[1].get_center()[0]) * RIGHT)
        zeros = VGroup(*[M("0", size=36, color=SKY).next_to(l1[i], DOWN, buff=0.12) for i in (1, 4)])
        self.beat("It says: one thousand times q zero, minus one thousand times q one, equals R minus fifty. Both "
                  "q's are zero, so zero equals R minus fifty.",
                  Write(l1), .15, [Indicate(l1[1], color=SKY), Indicate(l1[4], color=SKY), FadeIn(zeros)],
                  morph(l1.copy(), l2, [(5, 1), (6, 2), (7, 3), (8, 4)]),
                  w=(.35, .25, .25))

        # beat 3: the key step, R = 50 lb
        res = E(r"R| = 50\text{ lb}", size=60)
        paint(res, {0: ROSE})
        res.move_to([0, -2.3, 0])
        with self.say("This is the step the homework is really testing, so let's say it plainly. The equation we "
                      "removed to solve the system is the one that gives the reaction back. Here, R equals fifty "
                      "pounds.", style="slower and deliberate, stressing the key words") as d:
            self.play(FadeOut(VGroup(rowg, zeros)), VGroup(l1, l2).animate.shift(1.9 * UP), run_time=.15 * d)
            box = SurroundingRectangle(l1, color=ACCENT, buff=0.15)
            self.play(Create(box), run_time=.12 * d)
            self.wait(.2 * d)
            self.play(FadeOut(box), Write(res), run_time=.15 * d)
            self.play(self.spotlight(res), run_time=.1 * d)
            self.snap("spotlight on")
            self.wait(max(2.1, .27 * d))   # hold the spotlight at least 2 s

        # beat 4: the wall pushes right; global check
        ra = load(XW, r"R = 50\text{ lb}")
        bal = E(r"50|+|50|+|100|-|200|=|0", size=56).move_to([-0.4, -0.6, 0])
        paint(bal, {0: ROSE, 2: ROSE, 4: ROSE, 6: ROSE})
        names = VGroup(*[M(t, size=36, color=ROSE).next_to(bal[i], DOWN, buff=0.3)
                         for i, t in ((0, "R"), (2, "P_1"), (4, "P_2"), (6, r"5\times 40"))])
        tick = M(r"\checkmark", size=72, color=GOOD).next_to(bal, RIGHT, buff=0.5)
        done = chip("part c", GOOD).scale(1.7).move_to([0, -2.6, 0])
        bal_line = T("Balanced.", size=36, color=GOOD).next_to(tick, RIGHT, buff=0.3)
        self.beat("Positive, so the wall pushes the bar to the right, with fifty pounds. Check the whole bar: fifty, "
                  "plus fifty, plus one hundred, minus the spread load, five times forty, two hundred. Zero. "
                  "Balanced.",
                  self.unspot(),
                  [FadeOut(VGroup(l1, l2)), GrowArrow(ra[0]), ReplacementTransform(res, ra[1])],
                  Indicate(ra, color=ROSE),
                  [Write(bal[:6]), FadeIn(names)],
                  [Write(bal[6:]), FadeIn(tick, scale=1.4), FadeIn(bal_line), FadeIn(done)],
                  .1,
                  w=(.05, .18, .1, .42, .15))
        self.wipe()
