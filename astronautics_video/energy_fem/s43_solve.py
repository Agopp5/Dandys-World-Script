"""S43: solving the column's reduced system (BRIEF.md S43)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the reduced system in units of c l^2 / (2 E A), and the scale factor
K_red = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 1]], float)
rhs = np.array([2, 2, 1], float)
xs = np.linalg.solve(K_red, rhs)
assert np.allclose(xs, [5, 8, 9])
assert np.isclose(-xs[1] + xs[2], 1)            # last row: x4 - x3 = 1
assert np.isclose(-xs[0] + xs[1], 3)            # row 2 + row 3: x3 - x2 = 3
assert np.isclose(2 * xs[0] - xs[1] + (-xs[0] + xs[1]), 5)   # row 1 + that: x2 = 5
# scale: c = -rho A g, l = L/3 -> c l^2 / (2 E A) = -rho g L^2 / (18 E)   (rho = g = L = E = A = 1 test values)
rho, g, L, Ey, A = 1.3, 9.81, 2.0, 7.0, 0.4
c, l = -rho * A * g, L / 3
scale = c * l ** 2 / (2 * Ey * A)
assert np.isclose(scale, -rho * g * L ** 2 / (18 * Ey))
q = scale * xs
assert np.allclose(q, rho * g * L ** 2 / (2 * Ey) * np.array([-5 / 9, -8 / 9, -1]))
# exact column: u(x) = (rho g / E)(x^2/2 - L x): nodes agree
ex = lambda x: rho * g / Ey * (x ** 2 / 2 - L * x)
assert np.allclose(q, [ex(L / 3), ex(2 * L / 3), ex(L)])
assert np.isclose(q[2], -rho * g * L ** 2 / (2 * Ey))   # top sinks by rho g L^2 / 2E

DROP = np.array([0, 5 / 9, 8 / 9, 1.0])   # node displacements (downward), in units of the top's


def vmat(rows, color, braces=False):
    """A manim Matrix at main-math size, entries colored by meaning, brackets INK."""
    kw = dict(left_bracket="\\{", right_bracket="\\}") if braces else {}
    m = Matrix(rows, element_to_mobject_config={"font_size": 50, "color": color},
               v_buff=0.85, h_buff=0.95, **kw)
    m.get_brackets().set_color(INK)
    return m


class S43_Solve(VScene):
    budget = 180

    def construct(self):
        # ---------- the column (left half) ----------
        cx, y0, y3 = -4.3, -2.85, 3.05
        ln = (y3 - y0) / 3
        ys = [y0 + i * ln for i in range(4)]
        W = 1.5

        def elem(ya, yb):
            return Rectangle(width=W, height=yb - ya, stroke_color=INK2, stroke_width=3,
                             fill_color=SURFACE, fill_opacity=1).move_to([cx, (ya + yb) / 2, 0])

        elems = VGroup(*[elem(ys[i], ys[i + 1]) for i in range(3)])
        ground = Line([cx - 1.1, y0, 0], [cx + 1.1, y0, 0], color=INK2, stroke_width=4)
        hatch = VGroup(*[Line([cx - 1.0 + 0.25 * k, y0, 0], [cx - 1.2 + 0.25 * k, y0 - 0.3, 0],
                              color=INK2, stroke_width=2.5) for k in range(9)])
        nodes = VGroup(*[node([cx, y, 0], r=0.1) for y in ys])
        qlab = VGroup(*[M("q_%d" % (i + 1), size=44, color=SKY).next_to(nodes[i], LEFT, buff=1.05)
                        for i in range(4)])
        xarr = Arrow([cx + 1.3, y0 + 0.15, 0], [cx + 1.3, y0 + 1.5, 0], buff=0, color=INK2, stroke_width=4)
        xlab = M("x", size=40, color=INK2).next_to(xarr, RIGHT, buff=0.12)
        column = VGroup(ground, hatch, elems, nodes, qlab, xarr, xlab)
        qlab[0].shift(0.4 * UP)
        for m in qlab:
            m.set_z_index(3)
        nodes.set_z_index(2)

        # ---------- beat 1: scale factor + reduced system ----------
        RX = 3.55
        note = E(r"q|=|\frac{c\,l^2}{2EA}|\,x", size=48, cmap={r"\,x": SKY})
        note_t = T("measure each q in these units", size=30, color=MUTED)
        notebox = VGroup(note, note_t).arrange(DOWN, buff=0.18).move_to([RX, 2.7, 0])
        Km = vmat([["2", "-1", "0"], ["-1", "2", "-1"], ["0", "-1", "1"]], LILAC)
        Xv = vmat([["x_2"], ["x_3"], ["x_4"]], SKY, braces=True)
        eqs = M("=", size=50)
        Fv = vmat([["2"], ["2"], ["1"]], ROSE, braces=True)
        sysm = VGroup(Km, Xv, eqs, Fv).arrange(RIGHT, buff=0.25)
        fit(sysm, 6.6, 3.0)
        sysm.move_to([RX, 0.55, 0])
        self.beat("To keep the numbers clean, measure every q in units of c l squared over two E A. Then the system is just: two, minus one, zero; minus one, two, minus one; zero, minus one, one, times the q's, equals two, two, one.",
                  FadeIn(column), Write(note), FadeIn(note_t), .05, FadeIn(sysm), w=(.15, .25, .1, .45))

        def rowbox(k, color=GOLD):
            return VGroup(*[SurroundingRectangle(mx.get_rows()[k], buff=0.1, color=color, stroke_width=3)
                            for mx in (Km, Xv, Fv)])

        # ---------- beat 2: last row ----------
        LX = 0.75
        lineA = E(r"x_4|-|x_3|=|1", size=50, cmap={"x_4": SKY, "x_3": SKY, "1": ROSE})
        lineA.move_to([0, -1.55, 0]).align_to([LX, 0, 0], LEFT)
        tagA = T("row 3", size=30, color=MUTED).next_to(lineA, RIGHT, buff=0.6)
        box3 = rowbox(2)
        self.beat("The last row says minus x three plus x four equals one.",
                  Create(box3), Write(lineA), FadeIn(tagA), w=(.3, .5, .2))

        # ---------- beat 3: row 2 + row 3 ----------
        lineB = E(r"x_3|-|x_2|=|3", size=50, cmap={"x_3": SKY, "x_2": SKY, "3": ROSE})
        lineB.move_to([0, -2.45, 0]).align_to([LX, 0, 0], LEFT)
        tagB = T("row 2 + row 3", size=30, color=MUTED).next_to(lineB, RIGHT, buff=0.6)
        tagB.align_to(tagA, LEFT)
        box2 = rowbox(1)
        self.beat("Add the last row to the middle row: minus x two plus x three equals three.",
                  Create(box2), .1, Write(lineB), FadeIn(tagB), w=(.3, .4, .2))

        # ---------- beat 4: x2, x3, x4 ----------
        box1 = rowbox(0)
        sols = VGroup(*[E(r"x_%d|=|%d" % (i + 2, v), size=52, cmap={"x_%d" % (i + 2): SKY})
                        for i, v in enumerate((5, 8, 9))]).arrange(RIGHT, buff=0.85)
        sols.move_to([RX, -3.4, 0])
        sboxes = VGroup(*[SurroundingRectangle(s, buff=0.14, color=SKY, stroke_width=3) for s in sols])
        with self.say("Add that result to the first row, and you get x two equals five. Then x three is eight, and x four is nine.") as d:
            self.play(FadeOut(box2), FadeOut(box3), Create(box1), Indicate(lineB, color=GOLD), run_time=.2 * d)
            self.play(Write(sols[0]), Create(sboxes[0]), run_time=.25 * d)
            self.play(Indicate(lineB, color=GOLD), Write(sols[1]), Create(sboxes[1]), run_time=.22 * d)
            self.play(Indicate(lineA, color=GOLD), Write(sols[2]), Create(sboxes[2]), run_time=.22 * d)
            self.wait(.11 * d)

        # ---------- beat 5: units back ----------
        xrow = VGroup(sols, sboxes)
        subs = M(r"c = -\rho A g,\qquad l = \frac{L}{3}", size=40, color=INK2)
        scl = E(r"\frac{c\, l^2}{2EA}|=|-\frac{\rho g L^2}{18E}", size=52)
        qv = r"\begin{Bmatrix}q_2\\q_3\\q_4\end{Bmatrix}"
        fin = E(qv + r"|=|\frac{\rho g L^2}{2E}|\begin{Bmatrix}-5/9\\-8/9\\-1\end{Bmatrix}", size=52)
        fin[0].set_color(SKY)
        fin[3].set_color(SKY)
        fit(fin, 6.4, 3.0)
        finbox = SurroundingRectangle(fin, buff=0.22, color=GOLD, stroke_width=4)
        with self.say("Now put the units back. c l squared over two E A, with c equal to minus rho A g and l equal to L over three, is minus rho g L squared over eighteen E. So the q's are rho g L squared over two E, times minus five ninths, minus eight ninths, and minus one.") as d:
            self.play(FadeOut(VGroup(note, note_t, sysm, box1, lineA, tagA, lineB, tagB)),
                      xrow.animate.scale(.85).move_to([RX, 2.95, 0]), run_time=.1 * d)
            subs.move_to([RX, 1.95, 0])
            scl.move_to([RX, 0.75, 0])
            fin.move_to([RX, -1.95, 0])
            finbox.move_to(fin)
            self.play(Write(scl[0]), run_time=.1 * d)
            self.play(FadeIn(subs, shift=.2 * DOWN), run_time=.1 * d)
            self.play(Write(scl[1:]), run_time=.17 * d)
            self.wait(.05 * d)
            self.play(Write(fin), run_time=.25 * d)
            halo = glow(fin, GOLD)
            self.play(Create(finbox), FadeIn(halo), run_time=.1 * d)
            self.wait(.13 * d)

        # ---------- beat 6: the column sinks ----------
        S = 1.25    # exaggerated drop of the top, in scene units
        new_ys = [ys[i] - S * DROP[i] for i in range(4)]
        ghost = DashedVMobject(Rectangle(width=W, height=y3 - y0, color=MUTED, stroke_width=2.5)
                               .move_to([cx, (y0 + y3) / 2, 0]), num_dashes=40)
        ax_ = cx + 1.3
        arrows = VGroup(*[Arrow([ax_, ys[i], 0], [ax_, ys[i] - S * DROP[i], 0], buff=0, color=SKY,
                                stroke_width=6, max_tip_length_to_length_ratio=.45) for i in (1, 2, 3)])
        alab = VGroup(*[M(t, size=40, color=SKY).next_to(arrows[k], RIGHT, buff=0.15)
                        for k, t in enumerate(("-5/9", "-8/9", "-1"))])
        exag = T("sinking exaggerated", size=30, color=MUTED).move_to([cx + 0.4, y0 - 0.65, 0])
        card = panel(VGroup(T("FIRST QUESTION", size=32, color=GOLD, weight=BOLD),
                            T("How much does the flagpole", size=40),
                            T("shorten?", size=40)).arrange(DOWN, buff=0.25))
        fit(card, 5.6, 2.6)
        card.move_to([RX, -2.6, 0])
        tick = M(r"\checkmark", size=72, color=GOOD).next_to(card, RIGHT, buff=0.15)
        if tick.get_right()[0] > 6.9:
            tick.next_to(card, UP, buff=0.1).align_to(card, RIGHT)
        with self.say("All negative: every point sinks. The top sinks most, by rho g L squared over two E. That answers our first question: that's how much the flagpole shortens.") as d:
            self.play(FadeOut(xrow), FadeOut(subs), FadeOut(scl),
                      VGroup(halo, fin, finbox).animate.move_to([RX, 1.2, 0]), run_time=.08 * d)
            self.add(ghost)
            self.play(FadeIn(ghost),
                      *[Transform(elems[i], elem(new_ys[i], new_ys[i + 1])) for i in range(3)],
                      *[nodes[i].animate.move_to([cx, new_ys[i], 0]) for i in range(4)],
                      *[qlab[i].animate.shift((new_ys[i] - ys[i]) * UP) for i in range(4)],
                      FadeOut(xarr), FadeOut(xlab),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.3),
                      FadeIn(alab), FadeIn(exag), run_time=.3 * d)
            self.play(Indicate(arrows[2], color=GOLD), Indicate(alab[2], color=GOLD), run_time=.17 * d)
            self.play(FadeIn(card, shift=.2 * UP), run_time=.15 * d)
            self.play(Write(tick), Flash(tick, color=GOOD), run_time=.15 * d)
            self.wait(.15 * d)
        self.wipe()
