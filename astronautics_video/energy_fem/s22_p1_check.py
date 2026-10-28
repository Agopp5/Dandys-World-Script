"""S22: HW P1, does it make sense? (BRIEF.md S22)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: HW P1 sanity numbers (all K = 100 N/mm, all P = 30 N)
K1 = K2 = K3 = 100.0
P1 = P2 = P3 = P4 = 30.0
assert P2 + P3 + P4 == 90
assert 2 * K1 + K2 == 300 and P1 + 2 * 90 == 210
q2 = (P1 + 2 * (P2 + P3 + P4)) / (2 * K1 + K2)
assert np.isclose(q2, 0.7)
assert np.isclose(K2 * q2, 70) and np.isclose(2 * K2, 200)
q1 = (P1 + K2 * q2) / (2 * K2)
assert np.isclose(q1, 0.5)
assert np.isclose(q1, ((K1 + K2) * P1 + K2 * (P2 + P3 + P4)) / (K2 * (2 * K1 + K2)))
q3 = q2 + P4 / K3
assert np.isclose(P4 / K3, 0.3) and np.isclose(q3, 1.0)
assert np.isclose(K3 * (q3 - q2), 30) and np.isclose(K3 * (q3 - q2), P4)       # K3 carries only P4
assert np.isclose(K1 * q2, 70) and np.isclose(K2 * q1, 50)                      # the two wall springs
assert np.isclose(K1 * q2 + K2 * q1, 120) and np.isclose(120, 4 * 30)
# the equilibrium equations hold with these numbers
assert np.isclose(2 * K2 * q1 - K2 * q2, P1)
assert np.isclose(-K2 * q1 + (K1 + K2 + K3) * q2 - K3 * q3, P2 + P3)
assert np.isclose(-K3 * q2 + K3 * q3, P4)

LAB = 40      # figure labels
EQ = 50       # main equations


def lab(tex, pos, size=LAB):
    return E(tex, size=size).move_to(pos)


class S22_P1_Check(VScene):
    budget = 181

    def construct(self):
        self.section("HW 1: does it make sense?")

        # ---------- the HW P1 figure, left half ----------
        wx = -6.4
        yk1, yk2, yk3 = 1.8, -1.4, 0.4
        xj, xb0, xb1, xo = -4.7, -2.9, -2.6, -1.1
        W_ = wall(np.array([wx, 0.2, 0]), side=LEFT, h=4.6)
        rod = Rectangle(width=xb1 - xb0, height=4.6, color=INK2, fill_color=SURFACE, fill_opacity=1,
                        stroke_width=3).move_to([(xb0 + xb1) / 2, 0.3, 0])
        sk1 = spring(np.array([wx, yk1, 0]), np.array([xb0, yk1, 0]), coils=6)
        sk2a = spring(np.array([wx, yk2, 0]), np.array([xj, yk2, 0]), coils=4)
        sk2b = spring(np.array([xj, yk2, 0]), np.array([xb0, yk2, 0]), coils=4)
        sk3 = spring(np.array([xb1, yk3, 0]), np.array([xo, yk3, 0]), coils=4)
        nj = node(np.array([xj, yk2, 0]), r=0.1)
        no = node(np.array([xo, yk3, 0]), r=0.1)
        fP1 = force(np.array([xj, yk2 - 0.5, 0]), RIGHT, length=0.8)
        fP2 = force(np.array([xb1, 2.35, 0]), RIGHT, length=0.9)
        fP3 = force(np.array([xb1, -1.75, 0]), RIGHT, length=0.9)
        fP4 = force(np.array([xo, yk3, 0]), RIGHT, length=0.7)
        dq1 = disp(np.array([xj, yk2, 0]), label=None, below=1.1)
        dq2 = disp(np.array([(xb0 + xb1) / 2, -2.0, 0]), label=None, below=0.5)
        dq3 = disp(np.array([xo, yk3, 0]), label=None, below=0.5)
        lK1 = lab("K_1", [(wx + xb0) / 2, yk1 + 0.5, 0])
        lK2a = lab("K_2", [(wx + xj) / 2, yk2 + 0.5, 0])
        lK2b = lab("K_2", [(xj + xb0) / 2, yk2 + 0.5, 0])
        lK3 = lab("K_3", [(xb1 + xo) / 2, yk3 + 0.5, 0])
        lP1 = lab("P_1", fP1.get_right() + RIGHT * 0.35)
        lP2 = lab("P_2", fP2.get_right() + RIGHT * 0.35)
        lP3 = lab("P_3", fP3.get_right() + RIGHT * 0.35)
        lP4 = lab("P_4", fP4.get_right() + RIGHT * 0.35)
        lq1 = lab("q_1", dq1.get_right() + RIGHT * 0.3)
        lq2 = lab("q_2", dq2.get_right() + RIGHT * 0.3)
        lq3 = lab("q_3", dq3.get_right() + RIGHT * 0.3)
        springs = VGroup(sk1, sk2a, sk2b, sk3)
        fig = VGroup(W_, sk1, sk2a, sk2b, sk3, rod, nj, no, fP1, fP2, fP3, fP4, dq1, dq2, dq3,
                     lK1, lK2a, lK2b, lK3, lP1, lP2, lP3, lP4, lq1, lq2, lq3)
        for m in (lK1, lK2a, lK2b, lK3, lP1, lP2, lP3, lP4, lq1, lq2, lq3):
            m.set_z_index(3)

        # ---------- value cards, right half ----------
        cx = 3.65
        kv = E(r"K_1|=|K_2|=|K_3|=|100\text{ N/mm}", size=44)
        pv = E(r"P_1|=|P_2|=|P_3|=|P_4|=|30\text{ N}", size=44)
        vals = VGroup(kv, pv).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        card = panel(vals)
        fit(card, 6.6, 1.9)
        card.move_to([cx, 2.55, 0])

        # ---------- the three numeric answers ----------
        e2 = E(r"q_2|=|\frac{30 + 2(90)}{300}|=|0.7\text{ mm}", size=EQ).move_to([cx, 0.85, 0])
        e1 = E(r"q_1|=|\frac{30+70}{200}|=|0.5\text{ mm}", size=EQ).move_to([cx, -0.7, 0])
        e3 = E(r"q_3|=|0.7+0.3|=|1.0\text{ mm}", size=EQ).move_to([cx, -1.95, 0])
        for e in (e2, e1, e3):
            fit(e, 6.6, 1.5)
        b2, b1, b3 = (SurroundingRectangle(e, color=INK2, buff=0.15, corner_radius=0.1) for e in (e2, e1, e3))

        # 1
        self.beat("Never hand in a formula you haven't tested. Pick easy numbers: every spring one hundred "
                  "newtons per millimeter, every load thirty newtons. Pause and do checkpoint three point two "
                  "in your guide.",
                  FadeIn(fig), .15, FadeIn(card[0]), FadeIn(kv), Indicate(springs, color=LILAC, scale_factor=1.05),
                  FadeIn(pv), Indicate(VGroup(lP1, lP2, lP3, lP4), color=ROSE),
                  w=(.12, .06, .12, .18, .12, .2))
        self.checkpoint("3.2", "HW 1 check: all K = 100 N/mm, all P = 30 N")

        # 2
        self.beat("q two is thirty plus two times ninety, which is two hundred ten, over three hundred: "
                  "zero point seven millimeters.",
                  Write(e2[:3]), Indicate(VGroup(lP2, lP3, lP4), color=ROSE), .1,
                  Write(e2[3:]), [Create(b2), Indicate(lq2, color=SKY, scale_factor=1.4)],
                  w=(.3, .15, .2, .15))

        # 3
        with self.say("q one: P one plus K two q two is thirty plus seventy, one hundred, over two hundred: "
                      "zero point five. q three is zero point seven plus thirty over one hundred: one "
                      "millimeter.") as d:
            self.play(Write(e1[:3]), Indicate(VGroup(lP1, lK2b), color=ROSE), run_time=.3 * d)
            self.play(Write(e1[3:]), run_time=.12 * d)
            self.play(Create(b1), Indicate(lq1, color=SKY, scale_factor=1.4), run_time=.13 * d)
            self.play(Write(e3[:3]), Indicate(VGroup(lP4, lK3), color=ROSE), run_time=.25 * d)
            self.play(Write(e3[3:]), Create(b3), Indicate(lq3, color=SKY, scale_factor=1.4), run_time=.15 * d)

        # 4
        c4 = E(r"100 \times 0.3|=|30\text{ N}|=|P_4", size=EQ)
        t4 = M(r"\checkmark", size=60, color=GOOD)
        row4 = VGroup(c4, t4).arrange(RIGHT, buff=0.35).move_to([cx, -3.15, 0])
        g3 = glow(sk3, LILAC)
        n30 = T("30 N", size=36, color=ROSE).move_to([(xb1 + xo) / 2, yk3 + 1.15, 0])
        self.beat("Now Newton, as a check. Spring K three holds only P four, so it should carry thirty "
                  "newtons: one hundred times its stretch, zero point three, is thirty. Good.",
                  [FadeIn(g3), Indicate(lK3, color=LILAC), Indicate(lP4, color=ROSE)], FadeIn(n30),
                  [Write(c4), Indicate(e3[2], color=GOLD)], FadeIn(t4, scale=1.5),
                  w=(.3, .15, .35, .2))

        # 5
        g1, g2 = glow(sk1, LILAC), glow(sk2a, LILAC)
        n70 = T("70 N", size=36, color=ROSE).move_to([(wx + xb0) / 2, yk1 - 0.55, 0])
        n50 = T("50 N", size=36, color=ROSE).move_to([(wx + xj) / 2, yk2 + 1.05, 0])
        c5 = E(r"70|+|50|=|120\text{ N}|=|4 \times 30", size=EQ)
        t5 = M(r"\checkmark", size=60, color=GOOD)
        row5 = VGroup(c5, t5).arrange(RIGHT, buff=0.35).move_to(row4)
        self.beat("And the two springs on the wall must hold all four loads together, one hundred twenty "
                  "newtons. K one carries seventy, the first K two carries fifty. Seventy plus fifty is one "
                  "hundred twenty.",
                  [FadeOut(row4), FadeOut(g3), FadeOut(n30), Indicate(VGroup(lP1, lP2, lP3, lP4), color=ROSE)],
                  [FadeIn(g1), FadeIn(n70)], [FadeIn(g2), FadeIn(n50)], Write(c5), FadeIn(t5, scale=1.5),
                  w=(.3, .15, .2, .22, .13))

        # 6
        m1 = TX(r"1. stretch $=$ right end minus left end", size=46)
        m2 = E(r"2.\ |\Pi|=|U|-|W", size=52)
        m3 = TX(r"3. one partial derivative per unknown", size=46)
        m4 = TX(r"4. solve, then check with Newton", size=46)
        lines = VGroup(m1, m2, m3, m4).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        head = T("THE METHOD", size=34, color=ACCENT, weight=BOLD)
        kb = panel(VGroup(head, lines).arrange(DOWN, buff=0.45), color=ACCENT)
        fit(kb, 13.2, 6.4)
        kb.move_to(DOWN * 0.35)
        rest = VGroup(fig, card, e1, e2, e3, b1, b2, b3, row5, g1, g2, n70, n50)
        self.beat("So, stepping back: stretches, then U and W, then one derivative per unknown, then solve and "
                  "check. That's the whole method. Next, we leave springs behind and look at a real bar.",
                  FadeOut(rest), FadeIn(kb, shift=UP * 0.2), Indicate(m1, color=SKY, scale_factor=1.05),
                  Indicate(m2, color=GOLD, scale_factor=1.05), Indicate(m3, color=LILAC, scale_factor=1.05),
                  Indicate(m4, color=GOOD, scale_factor=1.05), Circumscribe(kb, color=ACCENT),
                  w=(.08, .1, .1, .1, .12, .14, .2))
        self.wipe()
