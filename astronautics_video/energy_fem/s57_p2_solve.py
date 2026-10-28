"""S57: HW P2 part b, the displacements (BRIEF.md S57)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# ---- facts (HW P2, pounds and inches) ----
E_, A_, L_ = 10e3, 2.0, 40.0
EA = E_ * A_
assert np.isclose(EA, 20000)
l_ = L_ / 2
k_ = EA / l_
assert np.isclose(k_, 1000)
c_ = -5.0
Qe = c_ * l_ / 2
assert np.isclose(Qe, -50)
P1, P2 = 50.0, 100.0
F1 = Qe + Qe + P1            # node 1 collects -50 from each element plus P1
F2 = Qe + P2                 # node 2: -50 from element 2 plus P2
assert np.isclose(F1, -50) and np.isclose(F2, 50)
Kg = k_ * np.array([[1, -1, 0], [-1, 2, -1], [0, -1, 1]])
Kr = Kg[1:, 1:]                                       # q0 = 0: drop row and column 0
assert np.allclose(Kr, 1000 * np.array([[2, -1], [-1, 1]]))
qs = np.linalg.solve(Kr, [F1, F2])
assert np.allclose(qs, [0.0, 0.05])
# adding the two rows: q2 coefficients cancel, q1 coefficient is 1000, right side -50 + 50 = 0
assert np.isclose(Kr[0, 1] + Kr[1, 1], 0) and np.isclose(Kr[0, 0] + Kr[1, 0], 1000) and np.isclose(F1 + F2, 0)
assert np.isclose(F2 / 1000 + 0, 0.05)               # 1000 (q2 - 0) = 50

# ---- the homework bar, drawn as in S54 ----
X0, X1, X2 = -6.0, -0.8, 4.4          # wall / node 1 (x = 20 in) / tip (x = 40 in)
YB, HB = 2.0, 0.6
assert np.isclose(X0 + (X2 - X0) * 20 / 40, X1)
EX = 0.6                              # exaggerated tip motion on screen (true: 0.05 in)


def vec(entries, color):
    m = Matrix([[e] for e in entries], left_bracket="\\{", right_bracket="\\}",
               element_to_mobject_config={"font_size": 48})
    m.get_entries().set_color(color)
    return m


def mat(rows, color=LILAC):
    m = Matrix(rows, element_to_mobject_config={"font_size": 48}, h_buff=1.0)
    m.get_entries().set_color(color)
    return m


class S57_P2_Solve(VScene):
    budget = 92

    def construct(self):
        # figure
        wl = wall(np.array([X0, YB, 0]), side=LEFT, h=1.6)
        br = bar(X0, X2, y=YB, h=HB)
        fl = dist_load(X0 + 0.3, X2 - 0.6, YB, n=15, d=LEFT, color=ROSE)
        n0, n1, n2 = (node(np.array([x, YB, 0])).set_z_index(3) for x in (X0, X1, X2))
        b0, b1, b2 = (badge(i).move_to(np.array([x, YB - HB / 2 - 0.42, 0])) for i, x in enumerate((X0, X1, X2)))
        p1 = force(np.array([X1, YB + HB / 2 + 0.32, 0]), d=RIGHT, length=1.1)
        p1l = M(r"P_1 = 50\text{ lb}", size=36, color=ROSE).next_to(p1, RIGHT, buff=.15)
        p2 = force(np.array([X2, YB, 0]), d=RIGHT, length=1.0)
        p2l = M(r"P_2 = 100\text{ lb}", size=36, color=ROSE).next_to(p2, UP, buff=.25)
        fll = M(r"f = 5\text{ lb/in}", size=36, color=ROSE).move_to(np.array([-3.4, YB + HB / 2 + 0.36, 0]))
        fig = VGroup(wl, br, fl, n0, n1, n2, b0, b1, b2, p1, p1l, p2, p2l, fll)

        # full 3 by 3 system (from part a)
        Km = mat([["1", "-1", "0"], ["-1", "2", "-1"], ["0", "-1", "1"]])
        qv = vec(["q_0", "q_1", "q_2"], SKY)
        Fv = vec(["R-50", "-50", "50"], ROSE)
        full = VGroup(M("1000", size=48), Km, qv, M("=", size=48), Fv).arrange(RIGHT, buff=.2)
        full.move_to(np.array([0, -1.3, 0]))
        Ke, qe, Fe = Km.get_entries(), qv.get_entries(), Fv.get_entries()

        # reduced 2 by 2 system
        Krm = mat([["2", "-1"], ["-1", "1"]])
        qrv = vec(["q_1", "q_2"], SKY)
        Frv = vec(["-50", "50"], ROSE)
        red = VGroup(M("1000", size=48), Krm, qrv, M("=", size=48), Frv).arrange(RIGHT, buff=.2)
        red.move_to(np.array([-3.55, -0.45, 0]))
        Kre, qre, Fre = Krm.get_entries(), qrv.get_entries(), Frv.get_entries()

        # the constrained equation, set aside
        alab = T("constrained equation (set aside)", size=30, color=MUTED)
        aeq = E(r"1000\,(|q_0|-|q_1|)|=|R|-50", size=44, cmap={"q_0": SKY})
        acard = panel(VGroup(alab, aeq).arrange(DOWN, buff=.2))
        acard.move_to(np.array([-3.55, -2.95, 0]))

        colx = Line(Km.get_columns()[0].get_top() + UP * .15, Km.get_columns()[0].get_bottom() + DOWN * .15,
                    color=BAD, stroke_width=7)
        sq0 = Line(qe[0].get_corner(DL) + LEFT * .08, qe[0].get_corner(UR) + RIGHT * .08, color=BAD, stroke_width=6)

        with self.say("The wall holds node zero, so q zero is zero. Cross out column zero, set row zero aside, "
                      "and keep the two by two.") as d:
            self.play(FadeIn(fig), FadeIn(full), run_time=.14 * d)
            self.play(Indicate(qe[0], color=SKY, scale_factor=1.3), Flash(n0, color=SKY),
                      Indicate(b0, color=SKY), run_time=.14 * d)
            self.play(Create(colx), Create(sq0), run_time=.16 * d)
            self.play(FadeIn(acard[0]), FadeIn(alab),
                      ReplacementTransform(VGroup(Ke[0], Ke[1], Ke[2], qe[0], Fe[0]), aeq),
                      FadeOut(colx), FadeOut(sq0), run_time=.2 * d)
            self.play(FadeOut(VGroup(Ke[3], Ke[6])),
                      ReplacementTransform(full[0], red[0]),
                      ReplacementTransform(Km.get_brackets(), Krm.get_brackets()),
                      *[ReplacementTransform(Ke[i], Kre[j]) for i, j in ((4, 0), (5, 1), (7, 2), (8, 3))],
                      ReplacementTransform(qv.get_brackets(), qrv.get_brackets()),
                      ReplacementTransform(qe[1], qre[0]), ReplacementTransform(qe[2], qre[1]),
                      ReplacementTransform(full[3], red[3]),
                      ReplacementTransform(Fv.get_brackets(), Frv.get_brackets()),
                      ReplacementTransform(Fe[1], Fre[0]), ReplacementTransform(Fe[2], Fre[1]),
                      run_time=.26 * d)
            self.wait(.1 * d)

        # right column of results
        XR = 0.75
        eq_a = E(r"1000\,|q_1|=|0", size=48)
        eq_b = E(r"q_1|=|0", size=52)
        eq_c = E(r"1000\,(|q_2|-|0|)|=|50", size=48, cmap={"0": SKY})
        eq_d = E(r"q_2|=|0.05\text{ in}", size=52)
        for m, y in ((eq_a, 0.3), (eq_b, -0.6), (eq_c, -1.65), (eq_d, -2.7)):
            m.move_to(np.array([0, y, 0])).align_to(np.array([XR, 0, 0]), LEFT)
        r0 = VGroup(Kre[0], Kre[1], Fre[0])
        r1 = VGroup(Kre[2], Kre[3], Fre[1])
        s1, s2 = strike(Kre[1]), strike(Kre[3])
        nk = M(r"-1+1=0", size=36, color=LILAC).next_to(Krm, DOWN, buff=.18).align_to(Kre[1], RIGHT)
        nf = M(r"-50+50=0", size=36, color=ROSE).next_to(Frv, DOWN, buff=.18)
        gb = glow(eq_b, GOLD)

        with self.say("Add the two equations. The q two terms cancel: one thousand q one equals zero. "
                      "So q one is zero.") as d:
            self.play(Indicate(r0, color=GOLD), Indicate(r1, color=GOLD), run_time=.18 * d)
            self.play(Create(s1), Create(s2), FadeIn(nk), Indicate(qre[1], color=SKY), run_time=.2 * d)
            self.play(FadeIn(nf), run_time=.08 * d)
            self.play(Write(eq_a), run_time=.2 * d)
            self.play(Write(eq_b), FadeIn(gb), Flash(n1, color=SKY), run_time=.2 * d)
            self.wait(.14 * d)

        abox = answer_box(eq_d)
        tag = chip("part b", ACCENT).next_to(abox, RIGHT, buff=.3)
        # deformed shape: node 1 stays, the right half stretches (exaggerated)
        ghost = DashedLine(np.array([X2, YB - .45, 0]), np.array([X2, YB + .45, 0]), color=MUTED)
        br2 = bar(X0, X2 + EX, y=YB, h=HB)
        sc = (X2 + EX - X1) / (X2 - X1)
        fmoves = [a.animate.shift(RIGHT * ((a.get_center()[0] - X1) * (sc - 1)))
                  for a in fl if a.get_center()[0] > X1]
        dq = Arrow(np.array([X2, 0.65, 0]), np.array([X2 + EX, 0.65, 0]), buff=0, color=SKY,
                   stroke_width=5, max_tip_length_to_length_ratio=.35)
        dql = M(r"q_2", size=36, color=SKY).next_to(dq, DOWN, buff=.1)
        exn = T("displacements exaggerated", size=30, color=MUTED).move_to(np.array([-3.4, YB - HB / 2 - 0.42, 0]))

        with self.say("Then the second equation: one thousand times q two minus zero equals fifty. "
                      "So q two is zero point zero five inches.") as d:
            self.play(FadeOut(VGroup(s1, s2, nk, nf)), eq_a.animate.set_opacity(.45), run_time=.1 * d)
            self.play(Indicate(r1, color=GOLD), Indicate(qre, color=SKY), run_time=.14 * d)
            self.play(Write(eq_c), run_time=.24 * d)
            self.wait(.06 * d)
            self.play(Write(eq_d), Create(abox), FadeIn(tag), run_time=.2 * d)
            self.add(ghost)
            self.play(Transform(br, br2), *fmoves,
                      VGroup(n2, b2, p2, p2l).animate.shift(RIGHT * EX),
                      GrowArrow(dq), FadeIn(dql), FadeIn(exn), FadeIn(ghost), run_time=.2 * d)
            self.wait(.06 * d)

        qm = M("?", size=96, color=GOLD).move_to(np.array([X1, YB + HB / 2 + 1.0, 0]))
        with self.say("Wait. Point one doesn't move at all, even though a load pushes right on it? That's "
                      "surprising. Hold that thought; we'll explain it in a moment.") as d:
            self.play(Indicate(VGroup(p1, p1l), color=ROSE), Flash(n1, color=SKY), run_time=.2 * d)
            self.play(FadeIn(qm, scale=1.6), Indicate(eq_b, color=GOLD), run_time=.2 * d)
            self.play(Wiggle(qm), run_time=.2 * d)
            self.wait(.4 * d)
        self.wipe()
