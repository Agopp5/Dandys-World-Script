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

# geometry: the shared homework bar (efem.hw2_bar), 40 in drawn from x = -6.0 to 4.4
HB = hw2_bar()
X0, X1, X2 = HB.X(0), HB.X(20), HB.X(40)
YB = HB.bar.get_center()[1]
YD = HB.farr.get_center()[1]       # the f arrow row, just below the bar
YR = HB.rings.get_center()[1]      # the node-ring row
YS = HB.rings.get_bottom()[1] - 0.4   # element-length spans, below the rings
assert np.isclose(X1, (X0 + X2) / 2)


def left_arrow(x_tail, x_tip, y=YD):
    return Arrow([x_tail, y, 0], [x_tip, y, 0], buff=0, color=ROSE, stroke_width=8,
                 max_tip_length_to_length_ratio=0.25).set_z_index(3)


class S55_P2_Elements(VScene):
    budget = 95

    def construct(self):
        self.section("Two elements")

        hb = HB
        cut = DashedLine([X1, YB + 0.7, 0], [X1, YB - 0.7, 0], color=ACCENT, stroke_width=5)
        split = Line([X1, hb.bar.get_bottom()[1], 0], [X1, hb.bar.get_top()[1], 0], color=INK2,
                     stroke_width=4).set_z_index(2)
        el_tags = VGroup(T("element 1", size=36, color=INK2).move_to([X0 + 0.62 * (X1 - X0), YB, 0]),
                         T("element 2", size=36, color=INK2).move_to([(X1 + X2) / 2 + 0.6, YB, 0])).set_z_index(2)
        spans = VGroup()
        for a, b in [(X0, X1), (X1, X2)]:
            da = DoubleArrow([a + 0.05, YS, 0], [b - 0.05, YS, 0], buff=0, color=MUTED, stroke_width=3,
                             tip_length=0.2)
            lab = M(r"l = 20\text{ in}", size=40).next_to(da, DOWN, buff=0.15)
            spans.add(VGroup(da, lab))

        with self.say("Two elements, split at point one. Why there? A point load can only enter the load vector "
                      "at a node, so every point load needs a node under it. Node zero at the wall, node one at "
                      "the middle, node two at the tip. Each element is twenty inches long.") as d:
            self.play(FadeIn(hb), run_time=.08 * d)
            self.play(Create(cut), run_time=.05 * d)
            self.play(FadeOut(cut), FadeIn(split), FadeIn(el_tags), run_time=.06 * d)
            self.wait(.05 * d)
            self.play(Indicate(hb.P1, color=ROSE), Indicate(hb.P2, color=ROSE), run_time=.12 * d)
            self.wait(.14 * d)
            for i in range(3):
                self.play(Indicate(hb.rings[i], color=ACCENT, scale_factor=1.4),
                          Flash(hb.nodes[i], color=ACCENT), run_time=.06 * d)
                self.wait(.04 * d)
            self.wait(.06 * d)
            self.play(LaggedStart(*[FadeIn(sp) for sp in spans], lag_ratio=.4), run_time=.1 * d)
            self.wait(.04 * d)

        keq = E(r"k|=|\frac{EA}{l}|=|\frac{20{,}000}{20}|=|1000\text{ lb/in}", size=54).move_to([0, -1.75, 0])
        hh = hb.bar.height + 0.18
        el_boxes = VGroup(*[Rectangle(width=b - a + 0.1, height=hh, color=LILAC, stroke_width=4)
                            .move_to([(a + b) / 2, YB, 0]) for a, b in [(X0, X1), (X1, X2)]])
        self.beat("Each element's stiffness is E A over l: twenty thousand over twenty, one thousand pounds per inch.",
                  Write(keq[0:3]), .1, Write(keq[3:5]), .1, Write(keq[5:]),
                  [Create(el_boxes), FadeIn(glow(keq[6], LILAC))], w=(.25, .25, .15, .15))

        # each element's spread load collapses to its two nodes, 50 lb each, pointing left
        L = 1.6
        e1_pair = VGroup(left_arrow(X0 + L, X0 + 0.02), left_arrow(X1 - 0.02, X1 - L))
        e2_pair = VGroup(left_arrow(X1 + L, X1 + 0.02), left_arrow(X2 - 0.02, X2 - L))
        f1 = VGroup(*[a for a in hb.farr if a.get_center()[0] < X1])
        f2 = VGroup(*[a for a in hb.farr if a.get_center()[0] >= X1])
        # labels on the ring row, clear of the rings (rings at nodes 0, 1, 2 and the dashed 3)
        q_labs = VGroup(*[M(r"50\text{ lb}", size=38, color=ROSE).move_to([x, YR, 0])
                          for x in [X0 + 1.2, X1 - 1.0, X1 + 1.0, X2 - 0.9]])
        qeq = E(r"\frac{cl}{2}|=|\frac{(-5)(20)}{2}|=|-50\text{ lb}", size=54).move_to([0, -3.15, 0])
        paint(qeq, {4: ROSE})
        self.beat("Each element's share of the spread load: c l over two at each of its nodes. Minus five times "
                  "twenty over two: minus fifty pounds at each end.",
                  [FadeOut(spans), FadeOut(el_boxes), Write(qeq[0])],
                  [ReplacementTransform(f1, e1_pair), FadeOut(hb.flab)],
                  [ReplacementTransform(f2, e2_pair)], .1,
                  Write(qeq[1:3]), .1, [Write(qeq[3:]), FadeIn(q_labs)], .2,
                  w=(.12, .12, .12, .12, .12))
        self.wipe()
