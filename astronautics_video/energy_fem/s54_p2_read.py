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

# figure geometry: bar from screen X0 (wall face) to X1 (tip)
X0, X1, YB, HB = -6.0, 4.4, -1.2, 0.6
def X(xin):
    return X0 + (X1 - X0) * xin / L_


def circ(n, p, color=INK2):
    lab = M(str(n), size=36, color=color)
    ring = Circle(radius=0.3, color=color, stroke_width=3).move_to(p)
    lab.move_to(p)
    return VGroup(ring, lab)


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
        w = wall(np.array([X0, YB, 0]), side=LEFT, h=1.8)
        b = bar(X0, X1, y=YB, h=HB)
        fl = dist_load(X0 + 0.25, X1 - 0.05, YB + HB / 2 + 0.32, n=15, d=LEFT, color=ROSE, length=0.42)
        f_lab = M("f", size=40, color=ROSE).move_to([X0 + 0.9, YB + HB / 2 + 0.95, 0])
        a1 = force(np.array([X(20), YB, 0]), d=RIGHT, length=1.1, color=ROSE).set_z_index(3)
        a2 = force(np.array([X1, YB, 0]), d=RIGHT, length=1.1, color=ROSE).set_z_index(3)
        p1_lab = M(r"P_1 = 50\text{ lb}", size=36, color=ROSE).move_to([X(20) + 0.55, YB + HB / 2 + 1.0, 0])
        p2_lab = M(r"P_2 = 100\text{ lb}", size=36, color=ROSE).move_to([X1 + 0.55, YB + HB / 2 + 1.0, 0])
        p2_lab.shift(LEFT * max(0, p2_lab.get_right()[0] - 6.8))
        d1 = Dot([X(20), YB, 0], radius=0.07, color=INK).set_z_index(4)
        d2 = Dot([X1, YB, 0], radius=0.07, color=INK).set_z_index(4)
        mark3 = DashedLine([X(10), YB - 0.55, 0], [X(10), YB + 0.55, 0], color=MUTED,
                           stroke_width=4, dash_length=0.1).set_z_index(2)
        yc = YB - HB / 2 - 0.5
        c1 = circ(1, [X(20), yc, 0])
        c2 = circ(2, [X1, yc, 0])
        c3 = circ(3, [X(10), yc, 0], color=MUTED)
        fig = VGroup(w, b, fl, f_lab, a1, a2, p1_lab, p2_lab, d1, d2, mark3, c1, c2, c3)

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
        ly = YB - HB / 2 - 1.35
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
                  [Indicate(a1, color=ROSE, scale_factor=1.3), Indicate(p1_lab, color=ROSE)], .1,
                  [Indicate(c2, color=ROSE), FadeIn(xl2, shift=UP * 0.2)],
                  [Indicate(a2, color=ROSE, scale_factor=1.3), Indicate(p2_lab, color=ROSE)], .1,
                  w=(.05, .15, .2, .15, .2))

        # ---------- distributed load ----------
        feq = E(r"f|=|c|=|-|5\text{ lb/in}", size=52).move_to([2.6, 1.6, 0])
        paint(feq, {2: ROSE})
        warn = T("the sign: most common mistake", size=30, color=ACCENT).next_to(feq, DOWN, buff=0.3)
        self.beat("And the spread load f, five pounds per inch: this is what we called c in our element formulas. "
                  "Watch its direction. Its arrows point left, against x. So c equals minus five. Getting that sign "
                  "wrong is the most common mistake on this problem.",
                  FadeOut(soft), [Indicate(fl, color=ROSE, scale_factor=1.25), Indicate(f_lab, color=ROSE)],
                  Write(feq[0:3]), .05,
                  Wiggle(fl, scale_value=1.15), Indicate(fl, color=ACCENT, scale_factor=1.2),
                  [Write(feq[3:]), feq[4].animate.set_color(ACCENT)], FadeIn(glow(feq[4], ACCENT)),
                  FadeIn(warn), .1,
                  w=(.03, .12, .1, .12, .12, .12, .08, .08))

        # ---------- point 3 ----------
        later = T("point 3: later", size=32, color=MUTED).move_to([X(10), ly, 0])
        later.shift(LEFT * max(0, later.get_right()[0] - (xl1.get_left()[0] - 0.3)))
        self.beat("The figure also marks a point three at a quarter of the length. The questions don't ask about "
                  "it, but we'll use it at the end to learn something.",
                  [FadeIn(glow(mark3, MUTED)), Indicate(c3, color=INK2)], .1, FadeIn(later, shift=UP * 0.2), .3,
                  w=(.3, .2))
        self.wipe()
