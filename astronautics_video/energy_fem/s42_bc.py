"""S42: applying the support, q1 = 0 removes row and column 1 (BRIEF.md S42)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the column under its own weight, three equal elements (units of E A / l and c l / 2)
K4 = np.array([[1, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 1]], float)
F4 = np.array([1, 2, 2, 1], float)                       # times c l / 2, plus R in row 1
assert np.allclose(K4.sum(axis=1), 0)                     # every row adds to zero (rigid slide stores nothing)
assert np.allclose(K4 @ np.ones(4), 0) and np.isclose(np.linalg.det(K4), 0)   # singular: no inverse
K3 = K4[1:, 1:]                                           # q1 = 0: delete row 1 and column 1
assert np.allclose(K3, [[2, -1, 0], [-1, 2, -1], [0, -1, 1]]) and np.allclose(F4[1:], [2, 2, 1])
assert not np.isclose(np.linalg.det(K3), 0)               # the reduced matrix has an inverse
q = np.linalg.solve(K3, F4[1:])                           # in units of c l^2 / (2 E A)
assert np.allclose(q, [5, 8, 9])                          # (c = -rho A g: -5/9, -8/9, -1 times rho g L^2 / 2E)

ENT = [["1", "-1", "0", "0"], ["-1", "2", "-1", "0"], ["0", "-1", "2", "-1"], ["0", "0", "-1", "1"]]


def mat(rows, size=48, braces=False, hb=0.92, vb=0.78, color=INK):
    kw = dict(left_bracket="\\{", right_bracket="\\}") if braces else {}
    return Matrix(rows, element_to_mobject=lambda s: M(s, size=size, color=color), h_buff=hb, v_buff=vb,
                  bracket_h_buff=0.12, **kw)


class S42_BC(VScene):
    budget = 156

    def construct(self):
        self.section("Applying the support")

        # ---- the column: x upward, base node 1 at the bottom, three equal elements
        xc, yb, H = -5.7, -2.7, 5.0
        l = H / 3
        ys = [yb + i * l for i in range(4)]
        bars = VGroup(*[bar(ys[i], ys[i + 1], h=0.56).rotate(PI / 2, about_point=ORIGIN).shift(xc * RIGHT)
                        for i in range(3)])
        nodes = VGroup(*[node([xc, y, 0], r=0.1) for y in ys])
        qlab = VGroup(*[E("q_%d" % (i + 1), size=40).next_to(nodes[i], RIGHT, buff=0.42) for i in range(4)])
        wts = VGroup(*[Arrow([xc - 0.62, y + 0.28, 0], [xc - 0.62, y - 0.28, 0], buff=0, color=ROSE,
                             stroke_width=5, max_tip_length_to_length_ratio=0.35)
                       for y in np.linspace(yb + 0.55, yb + H - 0.35, 5)])
        flab = E("f", size=44).next_to(wts[2], LEFT, buff=0.15)
        col = VGroup(bars, nodes, qlab, wts, flab)
        gap = DashedLine([xc - 0.85, yb, 0], [xc + 0.85, yb, 0], color=MUTED, dash_length=0.12)

        # ---- the 4 by 4 system, built from pieces so rows and columns can move
        pre = E(r"\frac{EA}{l}", size=48).set_color(LILAC)
        K = mat(ENT)
        qv = mat([["q_1"], ["q_2"], ["q_3"], ["q_4"]], braces=True, color=SKY)
        eq = M("=", size=48)
        lp = E(r"\frac{cl}{2}", size=48).set_color(ROSE)
        fv = mat([["1"], ["2"], ["2"], ["1"]], braces=True)
        pl = M("+", size=48)
        rv = mat([["R"], ["0"], ["0"], ["0"]], braces=True)
        rv.get_entries()[0].set_color(ROSE)
        sys4 = VGroup(pre, K, qv, eq, lp, fv, pl, rv).arrange(RIGHT, buff=0.18)
        sys4.move_to([1.35, 1.45, 0])
        r0 = K.get_rows()
        for v in (qv, fv, rv):                     # line every vector's rows up with the matrix rows
            v.shift((r0[0].get_y() - v.get_entries()[0].get_y()) * UP)
        rows, cols = K.get_rows(), K.get_columns()
        sums = VGroup(*[M(r"\to\ 0", size=48).move_to([qv.get_center()[0] + 0.25, r.get_y(), 0]) for r in rows])

        # ---- the bowl with a flat valley: Pi depends only on (q_a - q_b), so no single lowest point
        def proj(s, w):                          # cabinet view of Pi = w^2: w across the valley, s along it (receding)
            return 1.2 * np.array([w + 0.6 * s, 0.8 * w ** 2 + 0.35 * s, 0.0])
        ss, ws = np.linspace(-1.6, 1.6, 9), [-1.2, -0.8, -0.4, 0.4, 0.8, 1.2]
        cross = VGroup(*[ParametricFunction(lambda w, s=s: proj(s, w), t_range=[-1.2, 1.2], color=GOLD,
                                            stroke_width=5 if abs(s) > 1.5 else 3,
                                            stroke_opacity=1 if abs(s) > 1.5 else 0.5) for s in ss])
        along = VGroup(*[Line(proj(-1.6, w), proj(1.6, w), color=GOLD, stroke_width=4 if abs(w) > 1.1 else 2,
                              stroke_opacity=0.9 if abs(w) > 1.1 else 0.4) for w in ws])
        floor = Line(proj(-1.6, 0), proj(1.6, 0), color=GOLD, stroke_width=9)
        bowl = VGroup(cross, along, floor)
        off = np.array([-0.3, -2.15, 0]) - bowl.get_center()
        bowl.shift(off)
        pil = E(r"\Pi", size=52).next_to(bowl, LEFT, buff=0.25).shift(0.5 * UP)
        tt = ValueTracker(-1.2)
        ball = Dot(color=INK, radius=0.13).set_z_index(3)
        ball.add_updater(lambda m: m.move_to(proj(tt.get_value(), 0) + off + 0.12 * UP))
        note = VGroup(T("no support:", 32, MUTED), T("no single answer", 32, MUTED)).arrange(DOWN, buff=0.2)
        note.move_to([4.75, -2.0, 0])
        ghost = VGroup(*[DashedVMobject(b.copy().set_fill(opacity=0).set_stroke(MUTED, 2), num_dashes=24)
                         for b in bars])

        with self.say("Remember: every row of this matrix adds to zero, because sliding the whole column along "
                      "stores no energy. So the bowl has a flat valley instead of a single lowest point, and the "
                      "matrix has no inverse. Without its support, the column would just slide away under its "
                      "weight.") as d:
            self.play(FadeIn(col), Create(gap), Write(pre), Write(K), run_time=0.12 * d)
            self.play(LaggedStart(*[AnimationGroup(Indicate(r, color=INK, scale_factor=1.08), FadeIn(s))
                                    for r, s in zip(rows, sums)], lag_ratio=0.6), run_time=0.22 * d)
            self.wait(0.08 * d)
            self.play(Create(bowl), FadeIn(pil), run_time=0.08 * d)
            self.play(FadeIn(ball), Indicate(floor, color=GOLD), run_time=0.04 * d)
            self.play(tt.animate.set_value(1.2), run_time=0.08 * d)
            self.play(tt.animate.set_value(-0.3), Circumscribe(K, color=BAD), run_time=0.1 * d)
            self.play(FadeIn(ghost), col.animate.shift(0.9 * DOWN), run_time=0.15 * d)
            self.play(FadeIn(note), run_time=0.07 * d)
            self.wait(0.06 * d)

        ball.clear_updaters()
        ground = wall([xc, yb, 0], side=LEFT, h=1.7).rotate(PI / 2, about_point=[xc, yb, 0])
        q1eq = E("q_1|=|0", size=48).set_color(SKY)
        q1eq.next_to(nodes[0], RIGHT, buff=0.42).shift(0.9 * UP + 0.28 * UP)
        self.beat("What's missing is the support. The base is fixed, so q one is zero. We know it.",
                  [FadeOut(bowl), FadeOut(pil), FadeOut(ball), FadeOut(note), FadeOut(sums)],
                  [col.animate.shift(0.9 * UP), FadeOut(ghost)],
                  [Create(ground), FadeOut(gap)],
                  Flash(nodes[0].get_center() + 0.9 * UP, color=SKY, flash_radius=0.35),
                  morph(qlab[0], q1eq, [(0, 0)]), .3,
                  w=(.12, .14, .12, .1, .17))

        # ---- beat 3: cross out column 1, set row 1 aside
        q1 = qv.get_entries()[0]
        f1, R1 = fv.get_entries()[0], rv.get_entries()[0]
        colstrike = Line(cols[0].get_top() + 0.2 * UP, cols[0].get_bottom() + 0.2 * DOWN, color=BAD,
                         stroke_width=7).set_z_index(4)
        qstrike = Line(q1.get_corner(DL) + 0.12 * (DL), q1.get_corner(UR) + 0.12 * UR, color=BAD,
                       stroke_width=7).set_z_index(4)
        moving = VGroup(*rows[0][1:], f1, R1)
        r1eq = E(r"\frac{EA}{l}|(|q_1|-|q_2|)|=|\frac{cl}{2}|+|R", size=48)
        r1eq[0].set_color(LILAC)
        r1eq[7].set_color(ROSE)
        r1eq.move_to([1.35, -1.75, 0])
        aside = VGroup(T("set aside: has", 34, INK2), M("R", size=44, color=ROSE)).arrange(RIGHT, buff=0.15)
        aside.next_to(r1eq, DOWN, buff=0.4)
        with self.say("Here's what to do, and why. Because q one is zero, everything in column one gets multiplied "
                      "by zero, so we can cross out column one. And row one is the equation that contains the "
                      "unknown reaction R, so we set it aside for later.",
                      style="slower and deliberate, stressing the key words") as d:
            self.play(LaggedStart(FadeIn(qv), FadeIn(eq), FadeIn(lp), FadeIn(fv), FadeIn(pl), FadeIn(rv),
                                  lag_ratio=0.25), run_time=0.12 * d)
            self.play(self.spotlight(*rows[0], *cols[0][1:], q1, f1, R1), run_time=0.07 * d)
            self.play(Indicate(q1, color=SKY), Circumscribe(cols[0], color=BAD), run_time=0.12 * d)
            self.play(Create(colstrike), Create(qstrike), run_time=0.1 * d)
            self.snap("column 1 crossed out")
            self.play(Circumscribe(R1, color=ROSE), Circumscribe(rows[0], color=INK), run_time=0.12 * d)
            # the spotlight's halos stay where they were drawn: lift it before row 1 moves, then light the new home
            self.play(self.unspot(), run_time=0.05 * d)
            self.play(moving.animate.shift((r1eq.get_y() - rows[0].get_y()) * UP),
                      VGroup(cols[0], q1).animate.set_opacity(0.5), run_time=0.12 * d)
            self.play(FadeTransform(moving, r1eq), FadeIn(aside, shift=0.2 * UP), run_time=0.1 * d)
            self.play(self.spotlight(r1eq, aside), run_time=0.06 * d)
            self.wait(0.14 * d)
        self.wait(2)

        # ---- beat 4: the reduced 3 by 3 system
        red = E(r"\frac{EA}{l}|\begin{bmatrix}2&-1&0\\-1&2&-1\\0&-1&1\end{bmatrix}|"
                r"\begin{Bmatrix}q_2\\q_3\\q_4\end{Bmatrix}|=|\frac{cl}{2}|\begin{Bmatrix}2\\2\\1\end{Bmatrix}",
                size=52)
        red[0].set_color(LILAC)
        red[2].set_color(SKY)
        red[4].set_color(ROSE)
        red.move_to([1.35, 1.45, 0])
        box = SurroundingRectangle(red, color=INK2, buff=0.3, corner_radius=0.12, stroke_width=4)
        Kin = VGroup(K.get_brackets(), *[rows[i][j] for i in range(1, 4) for j in range(1, 4)])
        gone = VGroup(cols[0], colstrike, qstrike, q1, pl, rv.get_brackets(), *rv.get_entries()[1:])
        hb = red[1].height
        rowbox = Rectangle(width=red[1].width + 0.1, height=hb / 3.1, color=LILAC, stroke_width=5)
        rowbox.move_to(red[1].get_center() + hb / 3 * UP)
        with self.say("What's left is a three by three system for q two, q three and q four: E A over l, times two, "
                      "minus one, zero; minus one, two, minus one; zero, minus one, one. On the right, c l over "
                      "two, times two, two, one.") as d:
            self.play(self.unspot(), FadeOut(gone),
                      FadeTransform(pre, red[0]), FadeTransform(Kin, red[1]),
                      FadeTransform(VGroup(qv.get_brackets(), *qv.get_entries()[1:]), red[2]),
                      FadeTransform(eq, red[3]), FadeTransform(lp, red[4]),
                      FadeTransform(VGroup(fv.get_brackets(), *fv.get_entries()[1:]), red[5]),
                      run_time=0.16 * d)
            self.play(Indicate(red[2], color=SKY, scale_factor=1.1), run_time=0.12 * d)
            self.play(Create(rowbox), Indicate(red[0], color=LILAC), run_time=0.1 * d)
            self.play(rowbox.animate.shift(hb / 3 * DOWN), run_time=0.13 * d)
            self.play(rowbox.animate.shift(hb / 3 * DOWN), run_time=0.13 * d)
            self.play(Transform(rowbox, SurroundingRectangle(red[4:], color=ROSE, buff=0.12, stroke_width=5)),
                      run_time=0.12 * d)
            self.play(FadeOut(rowbox), Create(box), run_time=0.12 * d)
            self.wait(0.12 * d)
        self.wipe()
