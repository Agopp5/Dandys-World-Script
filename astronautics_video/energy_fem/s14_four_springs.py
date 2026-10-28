"""S14: the course slides' four-node example (BRIEF.md S14)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the four-node sample's U, its q2 derivative, and the 4 by 4 matrix, checked on random numbers
_rng = np.random.default_rng(14)
_k1, _k2, _k3 = _rng.uniform(1, 9, 3)
_KM = np.array([[_k1, -_k1, 0, 0], [-_k1, _k1 + 2 * _k2, -2 * _k2, 0],
                [0, -2 * _k2, 2 * _k2 + _k3, -_k3], [0, 0, -_k3, _k3]])


def _U(q):
    q1, q2, q3, q4 = q
    return .5 * _k1 * (q2 - q1) ** 2 + 2 * (.5 * _k2 * (q3 - q2) ** 2) + .5 * _k3 * (q4 - q3) ** 2


for _ in range(5):
    _q = _rng.normal(size=4)
    assert np.isclose(_U(_q), .5 * _q @ _KM @ _q)                  # U = 1/2 q^T K q
    q1, q2, q3, q4 = _q
    _dU2 = _k1 * (q2 - q1) - 2 * _k2 * (q3 - q2)                   # dU/dq2 as on screen
    _h = 1e-6
    _e = np.array([0, _h, 0, 0])
    assert np.isclose((_U(_q + _e) - _U(_q - _e)) / (2 * _h), _dU2, rtol=1e-5)
    assert np.isclose(_dU2, -_k1 * q1 + (_k1 + 2 * _k2) * q2 - 2 * _k2 * q3)   # the collected row
    assert np.isclose(_dU2, (_KM @ _q)[1])                          # = row 2 of the matrix
assert np.allclose(_KM.sum(axis=1), 0)                              # rows sum to zero


class S14_Four_Springs(VScene):
    budget = 235

    def construct(self):
        # ---- figure (built at y = 0, then shifted up) ----
        X1, X2, X3, X4, H = -5.0, -2.4, 1.2, 3.8, .5
        p = lambda x, y=0: np.array([x, y, 0])
        wl = wall(p(X1), side=LEFT)
        n1, n2, n3, n4 = [node(p(x)) for x in (X1, X2, X3, X4)]
        k1 = spring(p(X1), p(X2))
        k3 = spring(p(X3), p(X4))
        k1.add(E("k_1", size=36).next_to(k1, UP, buff=.1))
        k3.add(E("k_3", size=36).next_to(k3, UP, buff=.1))
        b1 = badge(1).move_to(p(X1 + .4, .95))
        b3, b4 = [badge(i).move_to(p(x, .95)) for i, x in ((3, X3), (4, X4))]
        b2 = badge(2).move_to(p(X2 - .42, .95))   # left of node 2: its top carries the F2 stem
        cL = Line(p(X2, -H), p(X2, H), color=INK, stroke_width=4)
        cR = Line(p(X3, -H), p(X3, H), color=INK, stroke_width=4)
        up = spring(p(X2, H), p(X3, H))
        up_lab = E("k_2", size=36).next_to(up, UP, buff=.1).shift(RIGHT * .8)   # clear of the F2 label
        lo = spring(p(X2, -H), p(X3, -H))
        lo_lab = E("k_2", size=36).next_to(lo, DOWN, buff=.12)
        pair = VGroup(cL, cR, up, lo, up_lab, lo_lab)
        fig = VGroup(wl, k1, k3, pair, n1, n2, n3, n4, b1, b2, b3, b4)
        for b in (b1, b2, b3, b4, n1, n2, n3, n4):
            b.set_z_index(3)
        fig.shift(UP * 1.4)

        with self.say("Here's an example from the course slides, built one spring at a time. Node one sits on "
                      "the wall. Spring k one joins node one to node two. Spring k three joins node three to "
                      "node four.") as d:
            self.play(FadeIn(wl), FadeIn(n1), FadeIn(b1), run_time=.2 * d)
            self.wait(.12 * d)
            self.play(Create(k1), run_time=.2 * d)
            self.play(FadeIn(n2), FadeIn(b2), run_time=.08 * d)
            self.wait(.05 * d)
            self.play(FadeIn(n3), FadeIn(b3), run_time=.08 * d)
            self.play(Create(k3), run_time=.17 * d)
            self.play(FadeIn(n4), FadeIn(b4), run_time=.08 * d)

        term = E(r"2\cdot\tfrac12|k_2|(|q_3|-|q_2|)^2", size=50).move_to(DOWN * 1.2)
        g_up, g_lo = glow(up, LILAC), glow(lo, LILAC)
        with self.say("Between nodes two and three there are two springs, both k two, side by side. Both share "
                      "the same two end points, so they stretch by the same amount, and together they store "
                      "twice the energy of one. That's why you'll see two k two.") as d:
            self.play(Create(cL), Create(cR), run_time=.08 * d)
            self.play(Create(up), Create(lo), FadeIn(up_lab), FadeIn(lo_lab), run_time=.2 * d)
            self.wait(.1 * d)
            self.play(FadeIn(g_up), FadeIn(g_lo), run_time=.12 * d)
            self.wait(.15 * d)
            self.play(Write(term), run_time=.18 * d)
            self.play(Circumscribe(term[0], color=LILAC), run_time=.12 * d)

        U = E(r"U|=|\tfrac12|k_1|(|q_2|-|q_1|)^2|+|2\cdot\tfrac12|k_2|(|q_3|-|q_2|)^2|+|\tfrac12|k_3|(|q_4|-|q_3|)^2",
              size=46)
        fit(U, 13.2, 1.2)
        U.move_to(UP * .3)
        t1, t2, t3 = VGroup(*U[2:9]), VGroup(*U[10:17]), VGroup(*U[18:25])
        with self.say("So U is one half k one, q two minus q one, squared, plus two times one half k two, q three "
                      "minus q two, squared, plus one half k three, q four minus q three, squared.") as d:
            self.play(FadeOut(g_up), FadeOut(g_lo), fig.animate.move_to(UP * 2.55),
                      term.animate.move_to(DOWN * 1.6), run_time=.12 * d)
            self.play(FadeIn(U[0]), FadeIn(U[1]), Write(t1), run_time=.25 * d)
            self.play(FadeIn(U[9]), *morph(term, t2, [(i, i) for i in range(7)]), run_time=.28 * d)
            self.remove(term)
            self.add(t2)
            self.play(FadeIn(U[17]), Write(t3), run_time=.25 * d)

        Wq = E(r"W|=|F_2|q_2|+|F_4|q_4", size=48, cmap={"F_4": ROSE}).move_to(DOWN * 1.0)
        top2 = cL.get_top() + UP * .6                     # F2 acts at node 2: stem up from the pair's link
        f2 = VGroup(Line(cL.get_top(), top2, color=INK, stroke_width=4), force(top2, d=RIGHT, length=.8))
        f2.add(E("F_2", size=40).next_to(f2[1], RIGHT, buff=.08))
        f4 = force(n4.get_center(), d=RIGHT, length=1.0)
        f4.add(E("F_4", size=40, cmap={"F_4": ROSE}).next_to(f4, RIGHT, buff=.08))
        box1 = SurroundingRectangle(t1, color=ACCENT, buff=.08)
        box2 = SurroundingRectangle(t2, color=ACCENT, buff=.08)
        with self.say("The loads are F two and F four, so W is F two q two plus F four q four. Take the partial "
                      "derivative with respect to q two. It appears in two terms: k one's, and the k two "
                      "pair.") as d:
            self.play(GrowFromEdge(f2, LEFT), GrowFromEdge(f4, LEFT), run_time=.12 * d)
            self.play(Write(Wq), run_time=.2 * d)
            self.wait(.15 * d)
            self.play(Indicate(U[5], color=SKY), Indicate(U[15], color=SKY), run_time=.15 * d)
            self.play(Create(box1), run_time=.12 * d)
            self.play(Create(box2), run_time=.12 * d)

        dPi = E(r"\frac{\partial\Pi}{\partial q_2}|=|k_1|(|q_2|-|q_1|)|-|2|k_2|(|q_3|-|q_2|)|-|F_2|=|0", size=46)
        dPi.move_to(DOWN * 1.15)
        row = E(r"-|k_1|q_1|+|(|k_1|+|2|k_2|)|q_2|-|2|k_2|q_3|=|F_2", size=48).move_to(DOWN * 2.85)
        with self.say("That gives k one times q two minus q one, minus two k two times q three minus q two, "
                      "minus F two. Set it to zero and multiply out: minus k one q one, plus k one plus two k "
                      "two, times q two, minus two k two q three, equals F two.") as d:
            self.play(FadeOut(Wq), run_time=.06 * d)
            self.play(FadeIn(dPi[0]), FadeIn(dPi[1]), TransformFromCopy(t1[1:], VGroup(*dPi[2:8])),
                      run_time=.12 * d)
            self.play(FadeIn(dPi[8]), TransformFromCopy(VGroup(t2[0][0], t2[1:]), VGroup(*dPi[9:16])),
                      run_time=.12 * d)
            self.play(FadeIn(dPi[16]), FadeIn(dPi[17]), run_time=.08 * d)
            self.play(FadeIn(dPi[18:]), FadeOut(box1), FadeOut(box2), run_time=.07 * d)
            self.wait(.05 * d)
            self.play(Write(VGroup(*row[0:3])), run_time=.1 * d)
            self.play(Write(VGroup(*row[3:11])), run_time=.14 * d)
            self.play(Write(VGroup(*row[11:15])), run_time=.1 * d)
            self.play(Write(VGroup(*row[15:])), run_time=.06 * d)

        ents = [["k_1", "-k_1", "0", "0"], ["-k_1", "k_1+2k_2", "-2k_2", "0"],
                ["0", "-2k_2", "2k_2+k_3", "-k_3"], ["0", "0", "-k_3", "k_3"]]
        mat = Matrix(ents, element_to_mobject=lambda s: MathTex(s, font_size=42,
                                                                 color=MUTED if s == "0" else LILAC),
                     h_buff=1.9, v_buff=.75)
        mat.get_brackets().set_color(INK)
        lhs = E(r"K|=", size=48)
        KM = VGroup(lhs, mat).arrange(RIGHT, buff=.25).move_to(DOWN * .55)
        rbox = SurroundingRectangle(mat.get_rows()[1], color=ACCENT, buff=.12)
        with self.say("Do that for every node, and you get this four by four matrix. Row two is the one we just "
                      "built.") as d:
            self.play(FadeOut(U), FadeOut(dPi), row.animate.move_to(DOWN * 3.15), run_time=.15 * d)
            self.play(FadeIn(lhs), Create(mat.get_brackets()), run_time=.12 * d)
            self.play(LaggedStart(*[FadeIn(r) for r in mat.get_rows()], lag_ratio=.3), run_time=.25 * d)
            self.wait(.08 * d)
            self.play(Create(rbox), run_time=.12 * d)
            self.play(Indicate(row, color=ACCENT, scale_factor=1.05), run_time=.16 * d)

        self.wipe()
