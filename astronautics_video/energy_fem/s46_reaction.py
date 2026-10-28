"""S46: the row we set aside gives the reaction (BRIEF.md S46)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: column under its own weight, three elements l = L/3, q1 = 0, c = -rho A g.
_rho, _g, _A, _L, _E = 2.7, 9.81, 3.0, 7.0, 200.0
_l, _c = _L / 3, -_rho * _A * _g
_q2 = -(5 / 9) * _rho * _g * _L ** 2 / (2 * _E)          # from the reduced 3x3 solve (S44)
_R = (_E * _A / _l) * (0 - _q2) - _c * _l / 2               # row 1: (EA/l)(q1 - q2) = c l / 2 + R
assert np.isclose((_E * _A / _l) * (0 - _q2), (5 / 6) * _rho * _g * _A * _L)   # left side = 5/6 rho g A L
assert np.isclose(_c * _l / 2, -(1 / 6) * _rho * _g * _A * _L)                 # c l / 2 = -1/6 rho g A L
assert np.isclose(_R, _rho * _g * _A * _L)                                     # R = rho g A L, whole weight
assert np.isclose(5 / 6 + 1 / 6, 1)


def column_figure():
    """Vertical column, three elements, base fixed, x upward. Big labels (>= 36)."""
    cx, y0, y1, w = -4.9, -2.55, 2.85, 1.3
    ys = [y0 + i * (y1 - y0) / 3 for i in range(4)]
    elems = VGroup(*[Rectangle(width=w, height=ys[i + 1] - ys[i]).set_fill(SURFACE, 1)
                     .set_stroke(INK2, 3).move_to([cx, (ys[i] + ys[i + 1]) / 2, 0]) for i in range(3)])
    nodes = VGroup(*[node([cx, y, 0], r=0.1) for y in ys])
    qlab = VGroup(*[M("q_%d" % (i + 1), size=44, color=SKY).next_to(nodes[i], RIGHT, buff=0.75)
                    for i in range(4)])
    ticks = VGroup(*[Line([cx + w / 2, y, 0], [cx + w / 2 + 0.55, y, 0], color=HAIR, stroke_width=2) for y in ys])
    ground = wall([cx, y0, 0], side=DOWN, h=1.7)
    # weight per length: small ROSE arrows down the left side
    wts = VGroup(*[Arrow([cx - w / 2 - 0.45, y + 0.3, 0], [cx - w / 2 - 0.45, y - 0.3, 0], buff=0,
                         color=ROSE, stroke_width=4, max_tip_length_to_length_ratio=0.35)
                   for y in np.linspace(y0 + 0.6, y1 - 0.4, 6)])
    wlab = M(r"\rho g A", size=40, color=ROSE).next_to(wts, LEFT, buff=0.2)
    react = Arrow([cx, y0 - 1.3, 0], [cx, y0 - 0.05, 0], buff=0, color=ROSE, stroke_width=8,
                  max_tip_length_to_length_ratio=0.3).set_z_index(5)
    rlab = M("R", size=48, color=ROSE).next_to(react, LEFT, buff=0.2).set_z_index(5)
    body = VGroup(ground, elems, ticks, nodes, qlab, wts, wlab)
    return body, react, rlab, qlab


class S46_Reaction(VScene):
    budget = 104

    def construct(self):
        body, react, rlab, qlab = column_figure()

        # row 1 of the full 4x4 system, the one deleted when q1 = 0 was imposed
        row1 = E(r"\frac{EA}{l}|\begin{bmatrix}1 & -1 & 0 & 0\end{bmatrix}|"
                 r"\begin{Bmatrix}q_1\\q_2\\q_3\\q_4\end{Bmatrix}|=|\frac{cl}{2}|+|R", size=48)
        row1[2].set_color(SKY)
        row1.move_to([2.4, 0.6, 0])
        tag = T("row 1, set aside", size=34, color=MUTED).next_to(row1, UP, buff=0.45)

        self.beat("Remember row one, the one we set aside? Now that we know q two, it tells us the reaction.",
                  FadeIn(body), [FadeIn(row1, shift=LEFT * 3), FadeIn(tag)], .1,
                  Indicate(qlab[1], color=SKY, scale_factor=1.3), w=(.25, .3, .35))

        eq = E(r"\frac{EA}{l}|(q_1 - q_2)|=|\frac{cl}{2}|+|R", size=52)
        tint(eq[1], [((1, 3), SKY), ((4, 6), SKY)])
        eq.move_to([2.4, 2.3, 0])
        n1 = E(r"q_1|=|0|,\qquad|q_2|=|-\frac59\,\frac{\rho g L^2}{2E}", size=44).move_to([2.4, 0.4, 0])
        with self.say("It says E A over l, times q one minus q two, equals c l over two plus R. "
                      "q one is zero, and q two we just found.") as d:
            self.play(FadeOut(tag), *morph(row1, eq, [(0, 0), (3, 2), (4, 3), (5, 4), (6, 5)]), run_time=.3 * d)
            self.wait(.25 * d)
            self.play(FadeIn(n1[0:3]), Indicate(qlab[0], color=SKY, scale_factor=1.3), run_time=.2 * d)
            self.play(FadeIn(n1[3:]), Indicate(qlab[1], color=SKY, scale_factor=1.3), run_time=.2 * d)
            self.wait(.05 * d)

        n2 = E(r"c|=|-\rho A g|,\qquad|l|=|\frac{L}{3}", size=44).move_to([2.4, -1.3, 0])
        b1 = E(r"\frac{3EA}{L}\Big(\frac59\,\frac{\rho g L^2}{2E}\Big)|=|-\frac{\rho A g L}{6}|+|R", size=48)
        b1.move_to([2.4, 0.4, 0])
        b2 = E(r"\frac56\,\rho g A L|=|-\frac16\,\rho g A L|+|R", size=48).move_to([2.4, 0.4, 0])
        rr = E(r"R|=|\rho g A L", size=56).move_to([2.4, -1.5, 0])
        box = SurroundingRectangle(rr, color=ROSE, buff=0.25, stroke_width=4)
        note = T("= the column's whole weight", size=34, color=MUTED).next_to(box, DOWN, buff=0.35)
        with self.say("Put the numbers in, and R comes out to rho g A L. "
                      "The ground pushes up with exactly the column's whole weight. As it must.") as d:
            self.play(FadeIn(n2), run_time=.1 * d)
            self.play(FadeOut(n1), FadeOut(n2), FadeIn(b1), run_time=.12 * d)
            self.play(*morph(b1, b2, [(1, 1), (3, 3)]), run_time=.13 * d)
            self.play(Write(rr), Create(box), run_time=.15 * d)
            self.wait(.05 * d)
            self.play(GrowArrow(react), FadeIn(rlab), run_time=.12 * d)
            self.play(FadeIn(glow(react, ROSE)), FadeIn(note), run_time=.13 * d)
            self.wait(.2 * d)

        # summary panel (own build: key_box shrinks lines below the readable size)
        head = T("THE FEM RECIPE", size=36, color=GOLD, weight=BOLD)
        lines = [T("assemble K and F (overlaps add)", size=38),
                 T("remove supported rows and columns", size=38),
                 T("solve for the free q's", size=38),
                 VGroup(E(r"\sigma|=|E\,(q_b - q_a)/l", size=44), T(";  removed rows give", size=38),
                        M("R", size=44, color=ROSE)).arrange(RIGHT, buff=0.2)]
        rows = VGroup(*[VGroup(badge(i + 1), ln).arrange(RIGHT, buff=0.4) for i, ln in enumerate(lines)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        card = panel(VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.55), color=GOLD)
        card.scale_to_fit_width(11.6).move_to(ORIGIN)
        with self.say("So, stepping back: assemble the blocks, add the loads, fix the supports by removing their "
                      "rows and columns, solve, then get stresses and use the removed rows for the reactions.") as d:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=.08 * d)
            self.play(FadeIn(card[0]), FadeIn(head), run_time=.08 * d)
            for r, t in zip(rows, (.14, .24, .14, .2)):
                self.play(FadeIn(r, shift=RIGHT * .3), run_time=.07 * d)
                self.wait((t - .07) * d)
            self.wait(.04 * d)
        self.wipe()
