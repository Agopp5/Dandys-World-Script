"""S53: the reactions, and a check (BRIEF.md S53)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the stepped aluminum bar (BRIEF facts, Episode 7)
E_al, A1, A2, L1, L2, KS, P_LOAD = 70_000, 200, 100, 500, 500, 14_000, 7000
k1, k2 = E_al * A1 / L1, E_al * A2 / L2
assert np.isclose(k1, 28_000) and np.isclose(k2, 14_000)
Kg = np.array([[k1, -k1, 0, 0], [-k1, k1 + k2, -k2, 0], [0, -k2, k2 + KS, -KS], [0, 0, -KS, KS]])
qf = np.linalg.solve(Kg[1:3, 1:3], [P_LOAD, 0])
q = np.array([0, qf[0], qf[1], 0])
assert np.allclose(q, [0, 0.2, 0.1, 0])
sig1, sig2 = E_al * (q[1] - q[0]) / L1, E_al * (q[2] - q[1]) / L2
assert np.isclose(sig1, 28) and np.isclose(sig2, -14)
R0 = Kg[0] @ q                     # row 0, set aside: 28000 q0 - 28000 q1 = R0
R3 = Kg[3] @ q                     # row 3, set aside: -14000 q2 + 14000 q3 = R3
assert np.isclose(R0, -28_000 * 0.2) and np.isclose(R0, -5600)
assert np.isclose(R3, -14_000 * 0.1) and np.isclose(R3, -1400)
assert np.isclose(P_LOAD + R0 + R3, 0) and np.isclose(5600 + 1400, 7000)
assert np.isclose(5600 / 7000, 4 / 5) and np.isclose(1400 / 7000, 1 / 5)
right_path = 1 / (1 / k2 + 1 / KS)  # element 2 and spring in series
assert np.isclose(right_path, 7000) and np.isclose(k1 / right_path, 4)

CM = {"q_0": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY, "R_0": ROSE, "R_3": ROSE,
      r"\sigma_1": ACCENT, r"\sigma_2": ACCENT}


class S53_Step_Reactions(VScene):
    budget = 176

    def construct(self):
        # ---- the stepped bar (top half of the frame) ----
        y0 = 1.25
        x0, x1, x2, x3 = -5.6, -2.0, 1.4, 5.6
        wl = wall(np.array([x0, y0, 0]), side=LEFT, h=1.9)
        wr = wall(np.array([x3, y0, 0]), side=RIGHT, h=1.9)
        e1 = bar(x0, x1, y=y0, h=0.9)          # thick element 1 (twice as tall)
        e2 = bar(x1, x2, y=y0, h=0.45)         # thin element 2
        sp = spring(np.array([x2, y0, 0]), np.array([x3, y0, 0]), coils=6, amp=0.26, color=LILAC)
        xs = [x0, x1, x2, x3]
        dots = VGroup(*[node(np.array([x, y0, 0]), r=0.09) for x in xs])
        nlab = VGroup()
        for i, x in enumerate(xs):
            dx = 0.3 if i == 0 else (-0.3 if i == 3 else 0)
            nlab.add(M(str(i), size=40, color=INK).move_to([x + dx, y0 - 0.85, 0]))
        p_arr = force(np.array([x1 + 0.06, y0 + 0.62, 0]), d=RIGHT, length=1.5)
        p_lab = M(r"P = 7000\text{ N}", size=40, color=ROSE).next_to(p_arr, UP, buff=0.12)
        p_lab.align_to(p_arr, LEFT)
        fig = VGroup(wl, wr, e1, e2, sp, dots, nlab, p_arr, p_lab)

        # ---- the set-aside rows (bottom half: two columns) ----
        lab0 = T("row 0, set aside", 30, color=MUTED).move_to([-3.55, -0.3, 0])
        row0 = E(r"28{,}000\,|q_0|-|28{,}000\,|q_1|=|R_0", size=48, cmap=CM).move_to([-3.55, -1.15, 0])
        r0 = E(r"R_0|=|-28{,}000 \times 0.2|=|-5600\text{ N}", size=48, cmap=CM)
        r0.move_to([-3.55, -2.45, 0])
        lab3 = T("row 3, set aside", 30, color=MUTED).move_to([3.55, -0.3, 0])
        row3 = E(r"-14{,}000\,|q_2|+|14{,}000\,|q_3|=|R_3", size=48, cmap=CM).move_to([3.55, -1.15, 0])
        r3 = E(r"R_3|=|-14{,}000 \times 0.1|=|-1400\text{ N}", size=48, cmap=CM)
        r3.move_to([3.55, -2.45, 0])
        for m in (row0, row3):
            fit(m, 6.7, 1.2)
        for m in (r0, r3):      # result on two lines: the final "= value" sits under the first "="
            m[3:].next_to(m[1], DOWN, buff=0.45, aligned_edge=LEFT)
            m.move_to([m.get_center()[0], -2.55, 0])

        self.beat("Now the rows we set aside. Row zero: twenty eight thousand times q zero, minus twenty eight "
                  "thousand times q one, equals R zero. That's minus twenty eight thousand times zero point two: "
                  "minus fifty six hundred newtons.",
                  FadeIn(fig), [FadeIn(lab0), FadeIn(row0, shift=UP * 0.3)], .1,
                  Write(r0), Indicate(r0[4], color=ROSE))
        self.beat("Row three: minus fourteen thousand times q two, equals R three. Minus fourteen hundred newtons.",
                  [FadeIn(lab3), FadeIn(row3, shift=UP * 0.3)], Write(r3), Indicate(r3[4], color=ROSE))
        self.beat("Pay close attention to this move, because problem two of your homework tests exactly this. "
                  "The rows we set aside to solve the system are the ones that give back the wall forces.",
                  self.spotlight(VGroup(lab0, row0, r0), VGroup(lab3, row3, r3)), .45,
                  style="slower and deliberate, stressing the key words")

        # ---- reaction arrows at the walls ----
        ya = y0 + 1.15
        a0 = Arrow([x0 + 1.75, ya, 0], [x0 + 0.1, ya, 0], buff=0, color=ROSE, stroke_width=8,
                   max_tip_length_to_length_ratio=0.25)
        a3 = Arrow([x3 - 0.1, ya - 0.35, 0], [x3 - 1.75, ya - 0.35, 0], buff=0, color=ROSE, stroke_width=8,
                   max_tip_length_to_length_ratio=0.25)
        t0 = T("pulls", 36, color=ROSE).next_to(a0, UP, buff=0.1)
        t3 = T("pushes", 36, color=ROSE).next_to(a3, UP, buff=0.1)
        m0 = M("R_0", size=40, color=ROSE).next_to(a0, RIGHT, buff=0.15)
        m3 = M("R_3", size=40, color=ROSE).next_to(a3, LEFT, buff=0.15)
        self.beat("Both reactions point left. At the left wall, the thick piece is in tension, so the wall pulls it "
                  "back. At the right wall, the spring is squeezed, so the wall pushes it back.",
                  self.unspot(), [GrowArrow(a0), FadeIn(m0)], Indicate(e1, color=ACCENT), FadeIn(t0), .1,
                  [GrowArrow(a3), FadeIn(m3)], Indicate(sp, color=LILAC), FadeIn(t3))

        # ---- the sum check, the 4 : 1 split, the question card ----
        old = VGroup(lab0, row0, r0, lab3, row3, r3)
        tot = E(r"7000|-|5600|-|1400|=|0", size=52).move_to([-3.9, -0.75, 0])
        tick = M(r"\checkmark", size=60, color=GOOD).next_to(tot, RIGHT, buff=0.35)
        bx = -3.6
        seg_l = Rectangle(width=4.8, height=0.6, stroke_color=INK2, stroke_width=3,
                          fill_color=ROSE, fill_opacity=0.55).move_to([bx - 0.6, -2.35, 0])
        seg_r = Rectangle(width=1.2, height=0.6, stroke_color=INK2, stroke_width=3,
                          fill_color=ROSE, fill_opacity=0.25).next_to(seg_l, RIGHT, buff=0)
        f_l = M(r"\frac45", size=40, color=INK).next_to(seg_l, UP, buff=0.12)
        f_r = M(r"\frac15", size=40, color=INK).next_to(seg_r, UP, buff=0.12)
        n_l = M(r"5600\text{ N}", size=40, color=ROSE).next_to(seg_l, DOWN, buff=0.15)
        n_r = M(r"1400\text{ N}", size=40, color=ROSE).next_to(seg_r, DOWN, buff=0.15)
        split = VGroup(seg_l, seg_r, f_l, f_r, n_l, n_r)
        # S47's question card (a panel); the top-right corner holds the figure here, so it sits bottom-right
        card = panel(VGroup(T("how does the", 36), T("load split?", 36)).arrange(DOWN, buff=0.15))
        card.move_to([3.9, -1.75, 0])
        ctick = M(r"\checkmark", size=72, color=GOOD).next_to(card, DOWN, buff=0.2)
        self.beat("Together, fifty six hundred plus fourteen hundred is seven thousand. They balance the load "
                  "exactly. So four fifths of the load goes to the left wall, through the stiff thick piece, and "
                  "one fifth goes right, through the softer path.",
                  FadeOut(old), Write(tot), FadeIn(tick, scale=1.5), .05,
                  [FadeIn(split[0]), FadeIn(split[2]), FadeIn(split[4]), Indicate(a0, color=ROSE)],
                  [FadeIn(split[1]), FadeIn(split[3]), FadeIn(split[5]), Indicate(a3, color=ROSE)],
                  FadeIn(card), FadeIn(ctick, scale=1.6))

        # ---- summary panel (own build: key_box shrinks lines) ----
        head = T("STEPPED BAR", 36, color=ACCENT, weight=BOLD)
        l1 = E(r"q_1|=|0.2\text{ mm},\ |q_2|=|0.1\text{ mm}", size=48, cmap=CM)
        l2 = E(r"\sigma_1|=|28,\ |\sigma_2|=|-14\text{ MPa}", size=48, cmap=CM)
        l3 = E(r"R_0|=|-5600,\ |R_3|=|-1400\text{ N}", size=48, cmap=CM)
        body = VGroup(head, l1, l2, l3).arrange(DOWN, buff=0.45)
        summ = panel(body, color=ACCENT)
        summ.scale(min(11.5 / summ.width, 6.2 / summ.height))
        summ.move_to(DOWN * 0.3)
        everything = VGroup(fig, a0, a3, t0, t3, m0, m3, tot, tick, split, card, ctick)
        self.beat("So, stepping back: the same recipe as the column, now with real numbers and two supports.",
                  FadeOut(everything), FadeIn(summ, shift=UP * 0.2))
        self.wipe()
