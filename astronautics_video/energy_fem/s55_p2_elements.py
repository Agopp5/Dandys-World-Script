"""S55: HW P2, two elements (BRIEF.md S55)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts (HW P2)
E_mod, A_area, L_bar = 10e3, 2.0, 40.0
EA = E_mod * A_area
assert np.isclose(EA, 20000)
l_el = L_bar / 2
assert np.isclose(l_el, 20)
k_el = EA / l_el
assert np.isclose(k_el, 1000)
c_load = -5.0
Q_end = c_load * l_el / 2
assert np.isclose(Q_end, -50)
P1, P2 = 50, 100
assert np.isclose(2 * 2 * Q_end + P1 + P2 + 50, 0)  # with R = 50: global balance

# geometry: 40 in of bar drawn over 10.8 units
X0, X2, YB, HB = -6.0, 4.8, 1.75, 0.8
X1 = (X0 + X2) / 2
YD = 0.7          # distributed-load arrow row (below the bar)
YS = -0.02         # element-length spans
assert np.isclose(X1, -0.6)


def node_badge(x, n):
    c = Circle(radius=0.36, color=INK, stroke_width=3).set_fill(BG, 1).move_to([x, YB, 0])
    t = M(str(n), size=44).move_to(c)
    return VGroup(c, t).set_z_index(4)


def left_arrow(x_tail, x_tip, y=YD):
    return Arrow([x_tail, y, 0], [x_tip, y, 0], buff=0, color=ROSE, stroke_width=8,
                 max_tip_length_to_length_ratio=0.25).set_z_index(3)


class S55_P2_Elements(VScene):
    budget = 95

    def construct(self):
        self.section("Two elements")

        # the homework bar, as drawn in S54
        wl = wall([X0, YB, 0], side=LEFT, h=2.4)
        whole = bar(X0, X2, y=YB, h=HB)
        fb = fem_bar([X0, X1, X2], y=YB, h=HB, elem_labels=False, node_labels=None)
        dl1 = dist_load(X0 + 0.1, X1 - 0.1, YD, n=6, d=LEFT, length=0.65)
        dl2 = dist_load(X1 + 0.1, X2 - 0.1, YD, n=6, d=LEFT, length=0.65)
        f_lab = M("f", size=40).next_to(dl2, RIGHT, buff=0.35)
        f_lab.set_color(ROSE)
        a1 = force([X1 + 0.36, YB, 0], d=RIGHT, length=1.2).set_z_index(3)
        a2 = force([X2 + 0.36, YB, 0], d=RIGHT, length=1.1).set_z_index(3)
        p1_lab = M(r"P_1 = 50\text{ lb}", size=40, color=ROSE).next_to(a1, UP, buff=0.55)
        p2_lab = M(r"P_2 = 100\text{ lb}", size=40, color=ROSE).next_to(a2, UP, buff=0.55)
        p2_lab.align_to([6.85, 0, 0], RIGHT)
        cut = DashedLine([X1, YB + 0.75, 0], [X1, YB - 0.75, 0], color=ACCENT, stroke_width=4)

        nodes = VGroup(*[node_badge(x, n) for n, x in enumerate([X0 + 0.38, X1, X2])])
        el_tags = VGroup(T("element 1", size=36, color=INK2).move_to([(X0 + X1) / 2 + 0.15, YB, 0]),
                         T("element 2", size=36, color=INK2).move_to([(X1 + X2) / 2 + 0.75, YB, 0])).set_z_index(2)
        spans = VGroup()
        for a, b in [(X0, X1), (X1, X2)]:
            da = DoubleArrow([a + 0.05, YS, 0], [b - 0.05, YS, 0], buff=0, color=MUTED, stroke_width=3,
                             tip_length=0.2)
            lab = M(r"l = 20\text{ in}", size=40).next_to(da, DOWN, buff=0.15)
            spans.add(VGroup(da, lab))

        with self.say("Two elements, split at point one. Why there? A point load can only enter the load vector "
                      "at a node, so every point load needs a node under it. Node zero at the wall, node one at "
                      "the middle, node two at the tip. Each element is twenty inches long.") as d:
            self.play(FadeIn(wl), FadeIn(whole), FadeIn(dl1), FadeIn(dl2), FadeIn(f_lab),
                      FadeIn(a1), FadeIn(a2), FadeIn(p1_lab), FadeIn(p2_lab), run_time=.08 * d)
            self.play(Create(cut), run_time=.05 * d)
            self.play(FadeOut(whole), FadeIn(fb), FadeOut(cut), FadeIn(el_tags), run_time=.06 * d)
            self.wait(.05 * d)
            self.play(Indicate(VGroup(a1, p1_lab), color=ROSE), Indicate(VGroup(a2, p2_lab), color=ROSE),
                      run_time=.12 * d)
            self.wait(.14 * d)
            for nd in nodes:
                self.play(FadeIn(nd, scale=1.4), run_time=.06 * d)
                self.wait(.04 * d)
            self.wait(.06 * d)
            self.play(LaggedStart(*[FadeIn(s) for s in spans], lag_ratio=.4), run_time=.1 * d)
            self.wait(.04 * d)

        keq = E(r"k|=|\frac{EA}{l}|=|\frac{20{,}000}{20}|=|1000\text{ lb/in}", size=54).move_to([0, -1.45, 0])
        el_boxes = VGroup(*[SurroundingRectangle(e, color=LILAC, buff=0.08, stroke_width=4)
                            for e in fb.elems])
        self.beat("Each element's stiffness is E A over l: twenty thousand over twenty, one thousand pounds per inch.",
                  Write(keq[0:3]), .1, Write(keq[3:5]), .1, Write(keq[5:]),
                  [Create(el_boxes), FadeIn(glow(keq[6], LILAC))], w=(.25, .25, .15, .15))

        # each element's spread load collapses to its two nodes, 50 lb each, pointing left
        L = 1.75
        e1_pair = VGroup(left_arrow(X0 + L, X0 + 0.02), left_arrow(X1 - 0.02, X1 - L))
        e2_pair = VGroup(left_arrow(X1 + L, X1 + 0.02), left_arrow(X2 - 0.02, X2 - L))
        q_labs = VGroup(*[M(r"50\text{ lb}", size=40, color=ROSE).next_to(ar, DOWN, buff=0.15)
                          for ar in [*e1_pair, *e2_pair]])
        qeq = E(r"\frac{cl}{2}|=|\frac{(-5)(20)}{2}|=|-50\text{ lb}", size=54).move_to([0, -3.0, 0])
        paint(qeq, {4: ROSE})
        self.beat("Each element's share of the spread load: c l over two at each of its nodes. Minus five times "
                  "twenty over two: minus fifty pounds at each end.",
                  [FadeOut(spans), FadeOut(el_boxes), Write(qeq[0])],
                  [ReplacementTransform(dl1, e1_pair), FadeOut(f_lab)],
                  [ReplacementTransform(dl2, e2_pair)], .1,
                  Write(qeq[1:3]), .1, [Write(qeq[3:]), FadeIn(q_labs)], .2,
                  w=(.12, .12, .12, .12, .12))
        self.wipe()
