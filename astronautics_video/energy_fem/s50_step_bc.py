"""S50: two walls, two deletions (BRIEF.md S50)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the stepped aluminum bar (BRIEF facts, Episode 7)
E_AL, A1, A2, LEN, KS, PLOAD = 70000, 200, 100, 500, 14000, 7000
k1, k2 = E_AL * A1 / LEN, E_AL * A2 / LEN
assert k1 == 28000 and k2 == 14000 and KS == 14000
KG = np.array([[k1, -k1, 0, 0], [-k1, k1 + k2, -k2, 0], [0, -k2, k2 + KS, -KS], [0, 0, -KS, KS]])
assert np.allclose(KG, [[28000, -28000, 0, 0], [-28000, 42000, -14000, 0],
                        [0, -14000, 28000, -14000], [0, 0, -14000, 14000]])
assert np.allclose(KG.sum(axis=1), 0)                 # rows sum to zero before supports
KR = KG[1:3, 1:3]                                     # delete rows/columns 0 and 3 (q0 = q3 = 0)
assert np.allclose(KR, [[42000, -14000], [-14000, 28000]])
assert np.isclose(np.linalg.det(KR), 9.8e8)
assert np.allclose(np.linalg.solve(KR, [PLOAD, 0]), [0.2, 0.1])


def fmt(v):
    v = int(v)
    if v == 0:
        return "0"
    return ("-" if v < 0 else "") + "{:,}".format(abs(v)).replace(",", "{,}")


class S50_Step_BC(VScene):
    budget = 70

    def construct(self):
        # ---- the stepped bar (top half) ----
        y = 2.25
        x0, x1, x2, x3 = -6.0, -1.5, 2.5, 6.0
        w0 = wall(np.array([x0, y, 0]), side=LEFT, h=2.0)
        w3 = wall(np.array([x3, y, 0]), side=RIGHT, h=2.0)
        e1 = bar(x0, x1, y=y, h=1.0)
        e2 = bar(x1, x2, y=y, h=0.5)
        sp = spring(np.array([x2, y, 0]), np.array([x3, y, 0]), coils=6, amp=0.3, color=LILAC)
        dots = VGroup(*[node(np.array([x, y, 0]), r=0.1) for x in (x0, x1, x2, x3)])
        nlabs = VGroup(*[M(str(i), size=40, color=INK).move_to([x, y - 0.8, 0])
                         for i, x in enumerate((x0 + 0.35, x1, x2, x3 - 0.35))])
        arr = Arrow(np.array([x1, y + 0.42, 0]), np.array([x1 + 1.6, y + 0.42, 0]), buff=0,
                    color=ROSE, stroke_width=8, max_tip_length_to_length_ratio=0.25)
        plab = M(r"P = 7000\ \mathrm{N}", size=40, color=ROSE).next_to(arr, UP, buff=0.12)
        plab.align_to(arr, LEFT)
        fig = VGroup(w0, w3, e1, e2, sp, dots, nlabs, arr, plab)
        f0 = E(r"q_0|=|0", size=40, cmap={"q_0": SKY}).move_to([x0 + 0.75, y - 1.55, 0])
        f3 = E(r"q_3|=|0", size=40).move_to([x3 - 0.75, y - 1.55, 0])

        # ---- the 4 by 4 system (bottom half) ----
        cfg = {"font_size": 46}
        Km = Matrix([[fmt(v) for v in row] for row in KG], element_to_mobject_config=cfg,
                    h_buff=1.95, v_buff=0.72)
        Km.get_entries().set_color(LILAC)
        qv = Matrix([["q_0"], ["q_1"], ["q_2"], ["q_3"]], left_bracket="\\{", right_bracket="\\}",
                    element_to_mobject_config=cfg, v_buff=0.72)
        qv.get_entries().set_color(SKY)
        eq = M("=", size=46)
        Fv = Matrix([["R_0"], ["7000"], ["0"], ["R_3"]], left_bracket="\\{", right_bracket="\\}",
                    element_to_mobject_config=cfg, v_buff=0.72)
        Fv.get_entries().set_color(ROSE)
        system = VGroup(Km, qv, eq, Fv).arrange(RIGHT, buff=0.3)
        fit(system, 13.4, 3.9)
        system.move_to([0, -1.95, 0])

        rows, cols = Km.get_rows(), Km.get_columns()
        qe, Fe = qv.get_entries(), Fv.get_entries()

        def slash(m):
            c, hw = m.get_center(), max(m.width / 2, 0.22) + 0.06
            return Line(c + np.array([-hw, -0.24, 0]), c + np.array([hw, 0.24, 0]), color=BAD, stroke_width=6)

        sl = {(r, j): slash(rows[r][j]) for r in range(4) for j in (0, 3)}
        cross_cols = VGroup(*sl.values())
        s0 = Line(qe[0].get_corner(DL) + LEFT * .05, qe[0].get_corner(UR) + RIGHT * .05, color=BAD, stroke_width=6)
        s3 = Line(qe[3].get_corner(DL) + LEFT * .05, qe[3].get_corner(UR) + RIGHT * .05, color=BAD, stroke_width=6)

        with self.say("Both walls are fixed, so q zero and q three are both zero. Same move as last time: cross out their columns, because they multiply zero.") as d:
            self.play(FadeIn(fig), FadeIn(system), run_time=0.15 * d)
            self.play(Write(f0), Write(f3), Indicate(qe[0], color=SKY, scale_factor=1.3),
                      Indicate(qe[3], color=SKY, scale_factor=1.3),
                      Indicate(w0, color=SKY), Indicate(w3, color=SKY), run_time=0.3 * d)
            self.wait(0.1 * d)
            self.play(Create(cross_cols), Create(s0), Create(s3),
                      cols[0].animate.set_opacity(0.3), cols[3].animate.set_opacity(0.3),
                      run_time=0.3 * d)

        # ---- set rows 0 and 3 aside ----
        a0 = E(r"28{,}000|\,q_0|-|28{,}000|\,q_1|=|R_0", size=40,
               cmap={r"\,q_0": SKY, r"\,q_1": SKY, "R_0": ROSE})
        paint(a0, {0: LILAC, 3: LILAC})
        a3 = E(r"-14{,}000|\,q_2|+|14{,}000|\,q_3|=|R_3", size=40,
               cmap={r"\,q_2": SKY, r"\,q_3": SKY, "R_3": ROSE})
        paint(a3, {0: LILAC, 3: LILAC})
        lab = T("set aside: reactions", size=34, color=INK2)
        aside = VGroup(lab, a0, a3).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        aside.move_to([0, 2.45, 0])
        abox = SurroundingRectangle(aside, color=HAIR, buff=0.25, corner_radius=0.12)

        with self.say("And set their rows aside, because those rows hold the unknown reactions. We'll come back to them.") as d:
            self.play(FadeOut(fig), FadeOut(f0), FadeOut(f3), run_time=0.2 * d)
            self.play(ReplacementTransform(VGroup(rows[0], Fe[0], sl[0, 0], sl[0, 3]), a0),
                      ReplacementTransform(VGroup(rows[3], Fe[3], sl[3, 0], sl[3, 3]), a3),
                      run_time=0.4 * d)
            self.play(FadeIn(lab, shift=DOWN * 0.2), Create(abox), run_time=0.2 * d)

        # ---- the 2 by 2 that remains ----
        red = E(r"\begin{bmatrix}42{,}000 & -14{,}000\\-14{,}000 & 28{,}000\end{bmatrix}"
                r"|\begin{Bmatrix}q_1\\q_2\end{Bmatrix}|=|\begin{Bmatrix}7000\\0\end{Bmatrix}", size=60)
        paint(red, {0: LILAC, 1: SKY, 3: ROSE})
        red.move_to([0, -1.7, 0])
        rbox = SurroundingRectangle(red, color=GOLD, buff=0.3, stroke_width=5)
        keep = VGroup(rows[1][1], rows[1][2], rows[2][1], rows[2][2])
        gone = VGroup(rows[1][0], rows[1][3], rows[2][0], rows[2][3], sl[1, 0], sl[1, 3], sl[2, 0], sl[2, 3], s0, s3, qe[0], qe[3])

        with self.say("What's left is two by two: forty two thousand, minus fourteen thousand; minus fourteen thousand, twenty eight thousand. Times q one, q two, equals seven thousand, zero.") as d:
            self.play(FadeOut(gone), run_time=0.12 * d)
            self.play(ReplacementTransform(VGroup(keep, Km.get_brackets()), red[0]),
                      ReplacementTransform(VGroup(qe[1], qe[2], qv.get_brackets()), red[1]),
                      ReplacementTransform(eq, red[2]),
                      ReplacementTransform(VGroup(Fe[1], Fe[2], Fv.get_brackets()), red[3]),
                      run_time=0.25 * d)
            self.play(Create(rbox), run_time=0.13 * d)
            self.play(Indicate(red[0], color=LILAC, scale_factor=1.05), run_time=0.25 * d)
            self.play(Indicate(red[3], color=ROSE, scale_factor=1.1), run_time=0.15 * d)

        self.wipe()
