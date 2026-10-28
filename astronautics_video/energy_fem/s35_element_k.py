"""S35: the element stiffness matrix (BRIEF.md S35)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# ---- facts -------------------------------------------------------------------------------------------
EA_num, l_num = 2e6, 500.0
assert np.isclose(EA_num / l_num, 4000.0)                       # 2 x 10^6 N / 500 mm = 4000 N/mm
_u1, _u2 = 0.13, 0.41
_s = np.linspace(0, 1, 2001)
_Ue_int = 0.5 * np.trapezoid(np.full_like(_s, EA_num * ((_u2 - _u1) / l_num) ** 2 * l_num), _s)
assert np.isclose(_Ue_int, 0.5 * EA_num / l_num * (_u2 - _u1) ** 2)  # integral of ds over 0..1 is 1
_K = np.array([[1, -1], [-1, 1]])
_uv = np.array([_u1, _u2])
assert np.allclose(_K @ _uv, [_u1 - _u2, -_u1 + _u2])           # matrix times column
assert np.isclose(_uv @ _K @ _uv, (_u2 - _u1) ** 2)              # row times that
assert np.isclose((_u2 - _u1) ** 2, _u1 ** 2 - 2 * _u1 * _u2 + _u2 ** 2)
assert np.allclose(_K.sum(axis=1), 0)                             # rows sum to zero

SQ = {"{u_1}^2": SKY, "{u_2}^2": SKY}
EQ_SIZE = 52
ENT = 50


def rowvec():
    return Matrix([["u_1", "u_2"]], element_to_mobject=lambda s: E(s, size=ENT), h_buff=1.05)


def colvec(entries):
    return Matrix([[a] for a in entries], element_to_mobject=lambda s: E(s, size=ENT),
                  left_bracket="\\{", right_bracket="\\}", v_buff=0.85)


def kmat(color=INK):
    return Matrix([["1", "-1"], ["-1", "1"]], element_to_mobject=lambda s: M(s, size=ENT, color=color),
                  h_buff=1.15, v_buff=0.85)


class S35_Element_K(VScene):
    budget = 247

    def regroup(self, g):
        """Make g one top-level mobject again (after part-wise morphs/transforms)."""
        self.remove(*g.get_family())
        self.add(g)

    def construct(self):
        # ---- beat 1: U_e in x, then in s -------------------------------------------------------------
        eqA = E(r"U_e|=|\frac12\int_{x_1}^{x_2}|EA|\,\varepsilon^2|\,dx", size=EQ_SIZE).move_to(UP * 1.3)
        paint(eqA, {4: ACCENT})
        eqB = E(r"U_e|=|\frac12\int_0^1|EA|\Big(\frac{u_2-u_1}{l}\Big)^2|\,l\,d|s", size=EQ_SIZE).move_to(UP * 1.3)
        for i in (1, 2, 4, 5):          # u_2 = glyphs 1-2, u_1 = glyphs 4-5 of the bracket part
            eqB[4][i].set_color(SKY)
        n1 = E(r"\varepsilon|=|\frac{u_2-u_1}{l}", size=44)
        for i in (0, 1, 3, 4):
            n1[2][i].set_color(SKY)
        n2 = E(r"dx|=|l\,d|s|,\qquad|0\le|s|\le 1", size=44)
        notes1 = VGroup(n1, n2).arrange(RIGHT, buff=1.4).move_to(DOWN * 1.3)
        self.beat("Now the strain energy of one element: one half, the integral of E A times strain squared, d x. "
                  "Change to s: d x is l d s, and s runs from zero to one.",
                  Write(eqA), .05, FadeIn(n1, shift=.2 * UP), FadeIn(n2, shift=.2 * UP),
                  morph(eqA, eqB, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]), .2,
                  w=(.25, .13, .13, .24))
        self.regroup(eqB)

        # ---- beat 2: constants out, integral of ds is one ----------------------------------------------
        eqC = E(r"U_e|=|\frac12|\frac{EA}{l}|(|u_2|-|u_1|)^2", size=EQ_SIZE).move_to(UP * 1.3)
        n3 = E(r"\int_0^1 d|s|=|1", size=44)
        n4 = E(r"\frac{l}{l^2}|=|\frac{1}{l}", size=44)
        notes2 = VGroup(n3, n4).arrange(RIGHT, buff=2.2).move_to(DOWN * 1.3)
        self.beat("Everything inside is constant, and the integral of d s from zero to one is one. "
                  "So U e is one half, E A over l, times u two minus u one, squared.",
                  FadeOut(notes1), [Circumscribe(eqB[3], color=INK2), Circumscribe(eqB[4], color=INK2)],
                  FadeIn(n3, shift=.2 * UP), FadeIn(n4, shift=.2 * UP),
                  morph(eqB, eqC, [(0, 0), (1, 1), (2, 2), (3, 3)]), .23,
                  w=(.08, .17, .12, .12, .28))
        self.regroup(eqC)

        # ---- beat 3: it's a spring ------------------------------------------------------------------
        xa, xb, yb = -4.5, 4.5, -0.45
        pa, pb = np.array([xa, yb, 0]), np.array([xb, yb, 0])
        elem = bar(xa, xb, y=yb, h=0.62)
        na, nb = node(pa, r=0.13), node(pb, r=0.13)
        tag = T("one element", size=38, color=INK2).next_to(elem, UP, buff=0.4)
        da = disp(pa, label="u_1", length=1.2, below=0.8, size=44)
        db = disp(pb, label="u_2", length=1.2, below=0.8, size=44)
        spr = spring(pa, pb, coils=7, amp=0.4)
        klab = E(r"k|=|\frac{EA}{l}", size=48).next_to(spr, UP, buff=0.35)
        paint(klab, {2: LILAC})
        stretch = E(r"\text{stretch}|=|u_2|-|u_1|", size=44).move_to(DOWN * 3.15)
        for m in (elem, spr, tag, da, db, klab, stretch):     # the figure sits above the spotlight scrim (z 89)
            m.set_z_index(91)
        na.set_z_index(93)
        nb.set_z_index(93)
        with self.say("Pay close attention, because you've seen this before. It's a spring! An element of a bar "
                      "behaves exactly like a spring with stiffness E A over l, stretched by u two minus u one.",
                      style="slower and deliberate, stressing the key words") as d:
            self.play(FadeOut(notes2), eqC.animate.move_to(UP * 2.65), run_time=.08 * d)
            self.play(self.spotlight(eqC), run_time=.1 * d)
            self.play(FadeIn(elem), FadeIn(na), FadeIn(nb), FadeIn(tag), FadeIn(da), FadeIn(db), run_time=.1 * d)
            self.wait(.05 * d)
            self.play(ReplacementTransform(elem, spr), FadeOut(tag), run_time=.14 * d)
            self.play(TransformFromCopy(eqC[3], klab[2]), FadeIn(klab[0]), FadeIn(klab[1]), run_time=.12 * d)
            self.play(TransformFromCopy(VGroup(eqC[5], eqC[6], eqC[7]), VGroup(stretch[2], stretch[3], stretch[4])),
                      FadeIn(stretch[0]), FadeIn(stretch[1]), run_time=.12 * d)
            self.wait(.29 * d)
        self.regroup(klab)
        self.regroup(stretch)

        # ---- beat 4: expand the square --------------------------------------------------------------
        ex = E(r"(|u_2|-|u_1|)^2|=|{u_1}^2|-|2|u_1|u_2|+|{u_2}^2", size=EQ_SIZE, cmap=SQ).move_to(UP * 0.3)
        self.beat("Now write it with a matrix. Expand the square: u two minus u one, squared, is u one squared, "
                  "minus two u one u two, plus u two squared.",
                  [self.unspot(), FadeOut(VGroup(spr, na, nb, da, db, klab, stretch))],
                  TransformFromCopy(VGroup(*eqC[4:9]), VGroup(*ex[0:5])),
                  [FadeIn(ex[5]), FadeIn(ex[6], shift=.15 * UP)],
                  FadeIn(VGroup(*ex[7:11]), shift=.15 * UP),
                  FadeIn(VGroup(*ex[11:13]), shift=.15 * UP), .23,
                  w=(.12, .2, .15, .15, .15))
        self.regroup(ex)

        # ---- beat 5: row x matrix x column, multiplied out step by step ----------------------------
        row5, mat5, col5 = rowvec(), kmat(), colvec(["u_1", "u_2"])
        P = VGroup(row5, mat5, col5).arrange(RIGHT, buff=0.25).move_to(UP * 0.35)
        eq1, row5b = M("=", size=EQ_SIZE), rowvec()
        V = colvec(["u_1|-|u_2", "-|u_1|+|u_2"])
        B1 = VGroup(eq1, row5b, V).arrange(RIGHT, buff=0.25).move_to(DOWN * 2.3)
        B2 = E(r"=|u_1|(|u_1|-|u_2|)|+|u_2|(-|u_1|+|u_2|)", size=EQ_SIZE).move_to(DOWN * 2.3)
        B3 = E(r"=|{u_1}^2|-|2|u_1|u_2|+|{u_2}^2", size=EQ_SIZE, cmap=SQ).move_to(DOWN * 2.3)
        rows = mat5.get_rows()
        r1 = SurroundingRectangle(rows[0], color=GOLD, buff=0.12, corner_radius=0.08)
        c1 = SurroundingRectangle(col5.get_entries(), color=GOLD, buff=0.12, corner_radius=0.08)
        with self.say("Here's a row, times a matrix, times a column, that gives exactly that: the row u one, u two, "
                      "times the matrix one, minus one, minus one, one, times the column u one, u two. "
                      "Multiply it out and the same three terms appear.") as d:
            self.play(FadeOut(eqC), ex.animate.move_to(UP * 2.75), run_time=.08 * d)
            self.play(Write(P), run_time=.1 * d)
            self.wait(.03 * d)
            self.play(Circumscribe(row5, color=SKY), run_time=.08 * d)
            self.play(Circumscribe(mat5, color=INK2), run_time=.1 * d)
            self.play(Circumscribe(col5, color=SKY), run_time=.08 * d)
            self.play(Create(r1), Create(c1), FadeIn(eq1), FadeIn(V.get_brackets()),
                      TransformFromCopy(row5, row5b), run_time=.08 * d)
            self.play(TransformFromCopy(VGroup(rows[0], col5.get_entries()), V.get_entries()[0]), run_time=.08 * d)
            self.play(r1.animate.move_to(rows[1]), run_time=.03 * d)
            self.play(TransformFromCopy(VGroup(rows[1], col5.get_entries()), V.get_entries()[1]), run_time=.08 * d)
            self.regroup(B1)
            self.play(FadeOut(r1), FadeOut(c1), *morph(B1, B2, [(0, 0)]), run_time=.08 * d)
            self.regroup(B2)
            self.play(*morph(B2, B3, [(0, 0)]), run_time=.08 * d)
            self.regroup(B3)
            self.play(Circumscribe(VGroup(*B3[1:]), color=GOLD), Circumscribe(VGroup(*ex[6:]), color=GOLD),
                      run_time=.08 * d)
            self.wait(.02 * d)

        # ---- beat 6: the element stiffness matrix -------------------------------------------------
        head6 = E(r"U_e|=|\frac12", size=EQ_SIZE)
        row6, mat6, col6 = rowvec(), kmat(), colvec(["u_1", "u_2"])
        kf = M(r"\frac{EA}{l}", size=EQ_SIZE, color=LILAC)
        M6 = VGroup(head6, row6, kf, mat6, col6).arrange(RIGHT, buff=0.22)
        VGroup(kf, mat6, col6).shift(.3 * RIGHT)       # room for the box between the vectors
        col6.shift(.3 * RIGHT)
        M6.move_to(UP * 1.2)
        box = SurroundingRectangle(VGroup(kf, mat6), color=LILAC, buff=0.18, corner_radius=0.1)
        lab = VGroup(T("element stiffness matrix", size=38), E("k", size=EQ_SIZE)).arrange(RIGHT, buff=0.3)
        lab.next_to(box, DOWN, buff=0.35)
        ia, ib = np.array([-4.2, -2.45, 0]), np.array([1.8, -2.45, 0])
        sp6 = spring(ia, ib, coils=6, amp=0.32)
        k6 = E(r"k|=|\frac{EA}{l}", size=44).next_to(sp6, RIGHT, buff=0.4)
        paint(k6, {2: LILAC})
        icon = VGroup(sp6, node(ia, r=0.12).set_z_index(3), node(ib, r=0.12).set_z_index(3), k6)
        icon.move_to(DOWN * 2.45)
        ep2 = T("the same block a single spring adds (episode 2)", size=30, color=MUTED).move_to(DOWN * 3.45)
        self.beat("So U e is one half, the row, times E A over l times that matrix, times the column. That matrix, "
                  "E A over l times one, minus one, minus one, one, is the element stiffness matrix. "
                  "The same block a spring added in episode two.",
                  [FadeOut(ex), FadeOut(B3)],
                  [ReplacementTransform(row5, row6), ReplacementTransform(mat5, mat6),
                   ReplacementTransform(col5, col6), FadeIn(head6, shift=.3 * RIGHT)],
                  FadeIn(kf, shift=.2 * DOWN), .05,
                  [mat6.animate.set_color(LILAC), Create(box)],
                  [FadeIn(lab, shift=.15 * UP)], .08,
                  [Create(sp6), FadeIn(icon[1]), FadeIn(icon[2]), FadeIn(k6), FadeIn(ep2)], .14,
                  w=(.07, .16, .1, .14, .1, .16))
        self.regroup(M6)

        # ---- beat 7: a number -----------------------------------------------------------------------
        given = M(r"EA = 2\times 10^6\text{ N},\qquad l = 500\text{ mm}", size=44, color=INK2).move_to(DOWN * 0.15)
        num = E(r"k|=|\frac{EA}{l}|=|\frac{2\times 10^6\text{ N}}{500\text{ mm}}|=|4000\text{ N/mm}",
                size=EQ_SIZE, cmap={r"\frac{EA}{l}": LILAC, r"4000\text{ N/mm}": LILAC}).move_to(DOWN * 2.1)
        g6 = VGroup(M6, box)
        self.beat("A quick number: if E A is two million newtons and the element is five hundred millimeters long, "
                  "its stiffness is four thousand newtons per millimeter.",
                  [FadeOut(lab), FadeOut(icon), FadeOut(ep2)],
                  g6.animate.move_to(UP * 2.35),
                  FadeIn(given, shift=.15 * UP),
                  Write(VGroup(*num[0:3])), Write(VGroup(*num[3:5])), Write(VGroup(*num[5:7])),
                  FadeIn(glow(num[6], LILAC)), .15,
                  w=(.08, .08, .17, .12, .15, .15, .1))
        self.wipe()
