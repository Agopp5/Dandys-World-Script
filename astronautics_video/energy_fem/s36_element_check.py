"""S36: checking the element stiffness matrix (BRIEF.md S36)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts
E_mod, A_area, l_len = 70_000, 100, 250          # N/mm^2, mm^2, mm (checkpoint 5.1)
assert np.isclose(E_mod * A_area / l_len, 28_000)  # N/mm
K_unit = np.array([[1, -1], [-1, 1]])
assert np.allclose(K_unit.sum(axis=1), 0)          # each row sums to zero
assert np.allclose(K_unit @ np.array([1.0, 1.0]), 0)  # equal end motion -> zero nodal force
d_val = 1.0
assert np.isclose(0.5 * (d_val - d_val) ** 2, 0)   # stretch u2 - u1 = 0 -> U_e = 0


class S36_Element_Check(VScene):
    budget = 60

    def construct(self):
        # ---- beat 1: the problem, then the checkpoint
        formula = E(r"k|=|\frac{E A}{l}", size=60)
        vals = VGroup(
            M(r"E = 70{,}000\ \text{N/mm}^2", size=44),
            M(r"A = 100\ \text{mm}^2", size=44),
            M(r"l = 250\ \text{mm}", size=44),
        ).arrange(DOWN, buff=.35, aligned_edge=LEFT)
        top = VGroup(formula, vals).arrange(RIGHT, buff=1.4).move_to(UP * 1.2)
        self.beat("Your turn: pause and do checkpoint five point one in your guide.",
                  Write(formula), LaggedStart(*[FadeIn(v, shift=.2 * RIGHT) for v in vals], lag_ratio=.3),
                  w=(.4, .6))
        self.checkpoint("5.1", "Element stiffness: E = 70,000 N/mm2, A = 100 mm2, l = 250 mm")

        # ---- beat 2: the arithmetic
        calc = E(r"\frac{70{,}000 \times 100}{250}|=|28{,}000\text{ N/mm}", size=60)
        calc.next_to(top, DOWN, buff=1.0)
        calc[2].set_color(LILAC)
        self.beat("Seventy thousand times one hundred, over two hundred fifty: twenty eight thousand newtons per millimeter.",
                  Write(calc[0]), .1, FadeIn(calc[1]), Write(calc[2]), FadeIn(glow(calc[2], LILAC)),
                  w=(.45, .05, .35, .15))

        # ---- beat 3: rigid translation, rows sum to zero
        # left half: one element, drawn large
        y0 = .9
        x1, x2 = -6.4, -2.6
        el = bar(x1, x2, y=y0, h=.7)
        n1, n2 = node([x1, y0, 0], r=.14), node([x2, y0, 0], r=.14)
        l1 = M(r"u_1", size=44, color=SKY).next_to(n1, UP, buff=.5)
        l2 = M(r"u_2", size=44, color=SKY).next_to(n2, UP, buff=.5)
        elem = VGroup(el, n1, n2, l1, l2)
        ghost = DashedVMobject(Rectangle(width=x2 - x1, height=.7).move_to([(x1 + x2) / 2, y0, 0])
                               .set_stroke(MUTED, 3), num_dashes=40)
        shift = 1.5
        ya = y0 - .85
        a1 = Arrow([x1, ya, 0], [x1 + shift, ya, 0], buff=0, color=SKY, stroke_width=7,
                   max_tip_length_to_length_ratio=.3)
        a2 = Arrow([x2, ya, 0], [x2 + shift, ya, 0], buff=0, color=SKY, stroke_width=7,
                   max_tip_length_to_length_ratio=.3)
        d1 = M("d", size=44, color=SKY).next_to(a1, DOWN, buff=.15)
        d2 = M("d", size=44, color=SKY).next_to(a2, DOWN, buff=.15)
        moves = VGroup(a1, a2, d1, d2)
        stretch = E(r"u_2 - u_1|=|d - d|=|0", size=48).move_to([(x1 + x2 + shift) / 2, -1.9, 0])
        stretch[4].set_color(GOOD)

        # right half: the element matrix with its row sums
        mat = Matrix([["1", "-1"], ["-1", "1"]], h_buff=1.3, v_buff=1.0,
                     element_to_mobject_config={"color": INK})
        mat.get_brackets().set_color(INK)
        pre = E(r"k|=|\frac{E A}{l}", size=56)
        mat.scale(1.25)
        kmat = VGroup(pre, mat).arrange(RIGHT, buff=.25)
        rows = mat.get_rows()
        sums = VGroup(
            M(r"1 - 1 = 0", size=44, color=GOOD),
            M(r"-1 + 1 = 0", size=44, color=GOOD),
        )
        right = VGroup(kmat, sums)
        right.move_to([3.5, .9, 0])
        kmat.move_to([2.6, .9, 0])
        for s_, r_ in zip(sums, rows):
            s_.next_to(mat, RIGHT, buff=.45).set_y(r_.get_y())
            s_.align_to(sums[1] if s_ is sums[0] else s_, RIGHT)
        sums[0].align_to(sums[1], RIGHT)
        fz = E(r"F|=|0,\quad|U_e|=|0", size=48).move_to([3.5, -1.9, 0])
        fz[0].set_color(ROSE)

        old = VGroup(formula, vals, calc)
        with self.say("And a sanity check. Move both ends the same amount: the element slides without stretching. Each row of the matrix adds to zero, so that motion takes no force and stores no energy.") as d:
            self.play(FadeOut(old), FadeIn(elem), FadeIn(kmat), run_time=.12 * d)
            self.add(ghost)
            self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(d1), FadeIn(d2),
                      elem.animate.shift(shift * RIGHT), run_time=.2 * d)
            self.play(Write(stretch), run_time=.12 * d)
            self.wait(.04 * d)
            for r_, s_ in zip(rows, sums):
                self.play(Indicate(r_, color=GOLD), FadeIn(s_, shift=.2 * RIGHT), run_time=.13 * d)
            self.play(FadeIn(fz), FadeIn(glow(fz, GOOD)), run_time=.12 * d)
            self.wait(.14 * d)
        self.wipe()
