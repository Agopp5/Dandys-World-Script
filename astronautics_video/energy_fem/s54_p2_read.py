"""S54: HW P2, reading the problem (BRIEF.md S54)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts (HW P2)
E_, A_, L_ = 10_000, 2, 40          # psi, in^2, in
EA = E_ * A_
assert EA == 20_000                 # lb
P1, P2 = 50, 100                    # lb, both +x
x1_in, x2_in, x3_in = L_ / 2, L_, L_ / 4
assert (x1_in, x2_in, x3_in) == (20, 40, 10)
c = -5                              # lb/in, f points in -x
assert c < 0 and abs(c) == 5

# figure: the shared homework bar (efem.hw2_bar), placed in the lower half
YB = -0.6


class S54_P2_Read(VScene):
    budget = 199

    def construct(self):
        # ---------- tasks ----------
        head = T("Problem 2", size=46, weight=BOLD).to_edge(UP, buff=0.6)
        ta = TX(r"(a) the global stiffness matrix $K$ and load vector $F$", size=40)
        tb = TX(r"(b) the displacements at points 1 and 2", size=40)
        tc = TX(r"(c) the reaction at the wall, from the constrained equation", size=40)
        tn = TX(r"constrained equation $=$ the wall's row", size=36).set_color(ACCENT)
        tasks = VGroup(ta, tb, tc).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        tn.next_to(tc, DOWN, buff=0.3).align_to(tc, LEFT).shift(RIGHT * 0.9)
        allt = VGroup(tasks, tn)
        fit(allt, 13.0, 5.0)
        allt.next_to(head, DOWN, buff=0.6)
        compact = TX(r"(a) $K$ and $F$ \qquad (b) $q$ at points 1, 2 \qquad (c) wall reaction $R$",
                     size=36).to_edge(UP, buff=0.35)

        # ---------- figure ----------
        hb = hw2_bar(y=YB)
        X = hb.X
        X0, X1 = X(0), X(40)
        fig = hb
        fl, f_lab = hb.farr, hb.flab
        a1, a2 = hb.P1, hb.P2
        c1, c2 = hb.rings[1], hb.rings[2]

        self.beat("Problem two. Using at least two elements, analyze this bar. Find the global stiffness matrix "
                  "and load vector, then the displacements at points one and two, then the reaction at the wall, "
                  "using the constrained equation. That's the wall's row, the one we always set aside.",
                  FadeIn(head), Write(ta), Write(tb), Write(tc), .05, FadeIn(tn, shift=UP * 0.2),
                  Indicate(tn, color=ACCENT), .08,
                  [FadeOut(head), ReplacementTransform(allt, compact)],
                  FadeIn(fig, lag_ratio=0.05),
                  w=(.03, .1, .08, .12, .08, .07, .08, .16))

        # ---------- data ----------
        rows = VGroup(M(r"E = 10{,}000\text{ psi}", size=40),
                      M(r"A = 2\text{ in}^2", size=40),
                      M(r"L = 40\text{ in}", size=40)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        card = panel(rows)
        card.move_to([-4.6, 1.75, 0])
        ea = E(r"EA|=|10{,}000 \times 2|=|20{,}000\text{ lb}", size=48).move_to([2.6, 2.6, 0])
        soft = T("far softer than real metal: round numbers", size=30, color=MUTED).next_to(ea, DOWN, buff=0.3)
        ly = min(hb.rings.get_bottom()[1], hb.flab.get_bottom()[1]) - 0.55
        span_l = DoubleArrow([X0, ly, 0], [X1, ly, 0], buff=0, color=INK2, stroke_width=3,
                             tip_length=0.2)
        span_lab = backed(M(r"L = 40\text{ in}", size=36).move_to([X(20), ly, 0]))
        span_g = VGroup(span_l, span_lab)

        self.beat("The data. E is ten thousand psi, pounds per square inch. That's far softer than any real metal, "
                  "but homework uses round numbers. The area is two square inches, and the length is forty inches. "
                  "So E A is twenty thousand pounds.",
                  FadeIn(card[0]), Write(rows[0]), FadeIn(soft), .1, Write(rows[1]), Write(rows[2]),
                  GrowFromCenter(span_g), Write(ea[0:3]), Write(ea[3:]), FadeIn(glow(ea[4])),
                  w=(.03, .08, .12, .1, .1, .08, .1, .1, .09))

        # ---------- point loads ----------
        xl1 = M(r"x = 20\text{ in}", size=36).move_to([X(20), ly, 0])
        xl2 = M(r"x = 40\text{ in}", size=36).move_to([X1, ly, 0])
        xl2.shift(LEFT * max(0, xl2.get_right()[0] - 6.8))
        self.beat("Point one is at the middle, twenty inches out, with a load P one of fifty pounds to the right. "
                  "Point two is the tip, forty inches out, with P two, one hundred pounds to the right.",
                  FadeOut(span_g), [Indicate(c1, color=ROSE), FadeIn(xl1, shift=UP * 0.2)],
                  Indicate(a1, color=ROSE, scale_factor=1.2), .1,
                  [Indicate(c2, color=ROSE), FadeIn(xl2, shift=UP * 0.2)],
                  Indicate(a2, color=ROSE, scale_factor=1.2), .1,
                  w=(.05, .15, .2, .15, .2))

        # ---------- distributed load ----------
        feq = E(r"f|=|c|=\\;|-5|\\text{ lb/in}", size=52).move_to([2.6, 1.6, 0])
        paint(feq, {2: ROSE})
        w0 = feq[4].width
        feq[4].scale(60 / 52, about_edge=LEFT).set_color(ACCENT)
        feq[5].shift(RIGHT * (feq[4].width - w0))
        feq.move_to([2.6, 1.6, 0])
        mbox = SurroundingRectangle(feq[4], color=ACCENT, buff=0.1, stroke_width=3)
        warn = T("the sign: most common mistake", size=30, color=ACCENT).next_to(feq, DOWN, buff=0.3)
        self.beat("And the spread load f, five pounds per inch: this is what we called c in our element formulas. "
                  "Watch its direction. Its arrows point left, against x. So c equals minus five. Getting that sign "
                  "wrong is the most common mistake on this problem.",
                  FadeOut(soft), [Indicate(fl, color=ROSE, scale_factor=1.25), Indicate(f_lab, color=ROSE)],
                  Write(feq[0:3]), .05,
                  Wiggle(fl, scale_value=1.15), Indicate(fl, color=ACCENT, scale_factor=1.2),
                  Write(feq[3:]), Create(mbox),
                  FadeIn(warn), .1,
                  w=(.03, .12, .1, .12, .12, .12, .08, .08))

        # ---------- point 3 ----------
        later = T("point 3: later", size=32, color=MUTED).move_to([X(10), ly, 0])
        later.shift(LEFT * max(0, later.get_right()[0] - (xl1.get_left()[0] - 0.3)))
        self.beat("The figure also marks a point three at a quarter of the length. The questions don't ask about "
                  "it, but we'll use it at the end to learn something.",
                  [Indicate(hb.tick3, color=MUTED, scale_factor=1.3), Indicate(hb.ring3, color=INK2)], .1, FadeIn(later, shift=UP * 0.2), .3,
                  w=(.3, .2))
        self.wipe()
