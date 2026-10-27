"""S09: Newton's way, node by node (BRIEF.md S09)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the node equations on screen, checked with the series' two-spring numbers
k1, k2, F1, F2, q1, q2 = 40.0, 20.0, 40.0, 20.0, 1.5, 2.5
assert np.isclose(-k1 * q1 + k2 * (q2 - q1) + F1, 0)                 # node 1 balance
assert np.isclose(-k1 * q1 + k2 * q2 - k2 * q1, -F1)                  # multiplied out, F1 moved across
assert np.isclose((k1 + k2) * q1 - k2 * q2, F1)                       # signs flipped, q1 terms grouped
assert np.isclose(-k2 * (q2 - q1) + F2, 0)                            # node 2 balance
assert np.isclose(-k2 * q1 + k2 * q2, F2)                             # node 2 multiplied out
assert np.allclose(np.array([[k1 + k2, -k2], [-k2, k2]]) @ [q1, q2], [F1, F2])

LAB = 38      # arrow labels
EQ = 48       # main equations
RX = 3.55     # right column centre


def arrow(a, b, color):
    return Arrow(a, b, buff=0, color=color, stroke_width=6, max_tip_length_to_length_ratio=0.22)


def cut_circle(c, r=0.5):
    return DashedVMobject(Circle(radius=r, color=INK2, stroke_width=3).move_to(c), num_dashes=24)


class S09_Newton(VScene):
    budget = 200

    def construct(self):
        self.section("Newton's way, node by node")

        # the two-spring system, small, along the top left
        y0 = 2.0
        pw, p1, p2 = np.array([-6.6, y0, 0]), np.array([-4.3, y0, 0]), np.array([-2.0, y0, 0])
        w = wall(pw, side=LEFT, h=1.0)
        s1 = spring(pw, p1, coils=4, label="k_1")
        s2 = spring(p1, p2, coils=4, label="k_2")
        n1, n2 = node(p1), node(p2)
        fa = arrow(p1 + UP * 0.75, p1 + UP * 0.75 + RIGHT * 0.8, ROSE)
        f1 = VGroup(fa, E("F_1", size=32).next_to(fa, UP, buff=0.06))
        f2 = force(p2, RIGHT, length=0.8, label="F_2")
        d1, d2 = disp(p1, "q_1"), disp(p2, "q_2")
        system = VGroup(w, s1, s2, n1, n2, f1, f2, d1, d2)

        # node 1 cut out
        c1 = np.array([-4.3, -0.1, 0])
        ring1_sys = cut_circle(p1, 0.4)
        ring1 = cut_circle(c1)
        fn1 = node(c1, r=0.11)
        a1 = arrow(c1 + LEFT * 0.5, c1 + LEFT * 1.8, LILAC)
        a2 = arrow(c1 + RIGHT * 0.46 + UP * 0.2, c1 + RIGHT * 1.8 + UP * 0.2, LILAC)
        a3 = arrow(c1 + RIGHT * 0.46 + DOWN * 0.2, c1 + RIGHT * 1.8 + DOWN * 0.2, ROSE)
        l1 = E("k_1|q_1", size=LAB).next_to(a1, UP, buff=0.15)
        l2 = E("k_2|(|q_2|-|q_1|)", size=LAB).next_to(a2, UP, buff=0.15).align_to(a2, LEFT)
        l3 = E("F_1", size=LAB).next_to(a3, DOWN, buff=0.15)
        tag1 = T("node 1", size=30, color=MUTED).next_to(ring1, DOWN, buff=0.2)

        with self.say("First, Newton's way, so we have something to compare with. "
                      "Cut out node one and list the forces on it.") as d:
            self.play(FadeIn(system), run_time=0.2 * d)
            self.play(Create(ring1_sys), run_time=0.12 * d)
            self.play(TransformFromCopy(ring1_sys, ring1), TransformFromCopy(n1, fn1), FadeIn(tag1),
                      run_time=0.2 * d)
            self.play(GrowArrow(a1), run_time=0.12 * d)
            self.play(GrowArrow(a2), run_time=0.12 * d)
            self.play(GrowArrow(a3), run_time=0.12 * d)
            self.wait(0.12 * d)

        self.beat("Spring one pulls it back, to the left, with k one q one. Spring two pulls it forward, "
                  "to the right, with k two times its stretch, q two minus q one. And the load F one pushes right.",
                  [Write(l1), Indicate(a1, color=LILAC), Indicate(s1, color=LILAC)], .05,
                  [Write(l2), Indicate(a2, color=LILAC), Indicate(s2, color=LILAC)], .05,
                  [Write(l3), Indicate(a3, color=ROSE), Indicate(f1, color=ROSE)], .1,
                  w=(.3, .4, .2))

        # node 1 balance
        bal = E("-|k_1|q_1|+|k_2|(|q_2|-|q_1|)|+|F_1|=|0", size=EQ).move_to([RX, 1.25, 0])
        self.beat("Balance: minus k one q one, plus k two times q two minus q one, plus F one, equals zero.",
                  [FadeIn(bal[0]), TransformFromCopy(l1, bal[1:3])],
                  [FadeIn(bal[3]), TransformFromCopy(l2, bal[4:10])],
                  [FadeIn(bal[10]), TransformFromCopy(l3, bal[11])],
                  FadeIn(bal[12:]), .15,
                  w=(.25, .35, .15, .1))

        # multiply out, move F1 across, then flip signs and group the q1 terms
        ex = E("-|k_1|q_1|+|k_2|q_2|-|k_2|q_1|=|-|F_1", size=EQ).move_to([RX, 0.05, 0])
        co = E(r"(|k_1|+|k_2|)\,|q_1|-|k_2|q_2|=|F_1", size=EQ).move_to([RX, -1.15, 0])
        box_a = SurroundingRectangle(ex[0:3], color=SKY, buff=0.08, corner_radius=0.08)
        box_b = SurroundingRectangle(ex[6:9], color=SKY, buff=0.08, corner_radius=0.08)
        with self.say("Multiply out and move F one across: minus k one q one, plus k two q two, minus k two q one, "
                      "equals minus F one. Flip every sign and group the q one terms: k one plus k two, "
                      "times q one, minus k two q two, equals F one.") as d:
            self.play(TransformFromCopy(bal[0:3], ex[0:3]), TransformFromCopy(bal[3], ex[3]),
                      TransformFromCopy(bal[4], ex[4]), TransformFromCopy(bal[6], ex[5]),
                      TransformFromCopy(bal[4], ex[7]), TransformFromCopy(bal[7], ex[6]),
                      TransformFromCopy(bal[8], ex[8]), run_time=0.2 * d)
            self.play(TransformFromCopy(bal[12], ex[9]), TransformFromCopy(bal[11], ex[11]), FadeIn(ex[10]),
                      Indicate(bal[11], color=ROSE), run_time=0.17 * d)
            self.wait(0.08 * d)
            self.play(Create(box_a), Create(box_b), ex[2].animate.set_color(SKY), ex[8].animate.set_color(SKY),
                      run_time=0.1 * d)
            q_extra = ex[8].copy()
            self.play(FadeIn(co[0]), TransformFromCopy(ex[1], co[1]), FadeIn(co[2]),
                      TransformFromCopy(ex[7], co[3]), FadeIn(co[4]),
                      TransformFromCopy(ex[2], co[5]), q_extra.animate.move_to(co[5]), run_time=0.17 * d)
            self.remove(q_extra)
            self.play(FadeIn(co[6]), TransformFromCopy(ex[4:6], co[7:9]),
                      FadeIn(co[9]), TransformFromCopy(ex[11], co[10]), run_time=0.15 * d)
            self.play(Circumscribe(co, color=SKY), run_time=0.05 * d)
            self.wait(0.08 * d)

        # node 2: clear node 1's working, keep its result
        c2 = np.array([-4.3, -2.55, 0])
        ring2_sys = cut_circle(p2, 0.4)
        ring2 = cut_circle(c2)
        fn2 = node(c2, r=0.11)
        b1 = arrow(c2 + LEFT * 0.5, c2 + LEFT * 1.9, LILAC)
        b2 = arrow(c2 + RIGHT * 0.5, c2 + RIGHT * 1.8, ROSE)
        m1 = E("k_2|(|q_2|-|q_1|)", size=LAB).next_to(b1, UP, buff=0.15).align_to(b1, RIGHT).shift(LEFT * 0.35)
        m2 = E("F_2", size=LAB).next_to(b2, UP, buff=0.15)
        tag2 = T("node 2", size=30, color=MUTED).next_to(ring2, DOWN, buff=0.2)
        bal2 = E("-|k_2|(|q_2|-|q_1|)|+|F_2|=|0", size=EQ).move_to([RX, -0.75, 0])
        co2 = E("-|k_2|q_1|+|k_2|q_2|=|F_2", size=EQ).move_to([RX, -1.95, 0])
        with self.say("Node two: spring two pulls it back with k two times q two minus q one, and F two pulls "
                      "forward. So minus k two times q two minus q one, plus F two, equals zero. "
                      "Multiply out: minus k two q one, plus k two q two, equals F two.") as d:
            self.play(FadeOut(bal), FadeOut(ex), FadeOut(box_a), FadeOut(box_b),
                      co.animate.move_to([RX, 1.25, 0]), Create(ring2_sys), run_time=0.12 * d)
            self.play(TransformFromCopy(ring2_sys, ring2), TransformFromCopy(n2, fn2), FadeIn(tag2),
                      run_time=0.1 * d)
            self.play(GrowArrow(b1), Write(m1), Indicate(s2, color=LILAC), run_time=0.14 * d)
            self.play(GrowArrow(b2), Write(m2), Indicate(f2, color=ROSE), run_time=0.1 * d)
            self.play(FadeIn(bal2[0]), TransformFromCopy(m1, bal2[1:7]), run_time=0.14 * d)
            self.play(FadeIn(bal2[7]), TransformFromCopy(m2, bal2[8]), FadeIn(bal2[9:]), run_time=0.1 * d)
            self.wait(0.04 * d)
            self.play(FadeIn(co2[0]), TransformFromCopy(bal2[1], co2[1]), TransformFromCopy(bal2[5], co2[2]),
                      FadeIn(co2[3]), TransformFromCopy(bal2[1], co2[4]), TransformFromCopy(bal2[3], co2[5]),
                      FadeIn(co2[6]), TransformFromCopy(bal2[8], co2[7]), run_time=0.16 * d)
            self.play(Circumscribe(co2, color=SKY), run_time=0.04 * d)
            self.wait(0.06 * d)

        # the pair goes into a "Newton" panel at the top right
        pair = VGroup(co.copy(), co2.copy()).arrange(DOWN, buff=0.35).scale(0.85)
        card = panel(pair, color=HAIR)
        head = T("Newton", size=32, color=INK2, weight=BOLD)
        box = VGroup(head, card).arrange(DOWN, buff=0.15).to_corner(UR, buff=0.4)
        card[0].set_z_index(0)
        for m in (pair, co, co2):
            m.set_z_index(3)
        with self.say("Two equations, two unknowns. Keep these on the side. "
                      "Now let's get the very same equations from energy alone.") as d:
            self.play(FadeOut(bal2), co.animate.move_to([RX, 0.4, 0]),
                      co2.animate.move_to([RX, -0.6, 0]), run_time=0.15 * d)
            self.play(Circumscribe(VGroup(co, co2), color=SKY), run_time=0.2 * d)
            self.play(FadeOut(VGroup(ring1, fn1, a1, a2, a3, l1, l2, l3, tag1,
                                     ring2, fn2, b1, b2, m1, m2, tag2, ring1_sys, ring2_sys, system)),
                      FadeIn(card[0]), FadeIn(head),
                      ReplacementTransform(co, card[1][0]), ReplacementTransform(co2, card[1][1]),
                      run_time=0.3 * d)
            self.wait(0.35 * d)
        self.wipe()
