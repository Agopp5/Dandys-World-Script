"""S39: a column under its own weight, the setup (BRIEF.md S39)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: three equal elements of length L/3 cover the column; four nodes, node 1 at the base
N_EL = 3
assert np.isclose(N_EL * (1 / 3), 1.0)          # l = L/3, three of them make L
assert N_EL + 1 == 4                            # nodes 1..4
# weight per length: f = c = -rho A g (x up, gravity down)
rho, A_, g = 2.7e-9, 100.0, 9810.0               # any positive values: the sign is what matters
assert -rho * A_ * g < 0

# geometry (frame units)
BASE, TOP = -3.0, 2.3
H = TOP - BASE
CX_L, CX_R, WID = -4.0, 2.0, 0.72


def column(cx):
    return Rectangle(width=WID, height=H, stroke_color=INK2, stroke_width=3,
                     fill_color=SURFACE, fill_opacity=1).move_to([cx, (BASE + TOP) / 2, 0])


class S39_Column_Setup(VScene):
    budget = 128

    def construct(self):
        # ---- beat 1: the flagpole and the two questions
        col = column(CX_L)
        floor_l = wall(np.array([CX_L, BASE, 0]), side=DOWN, h=2.4)
        q_a = panel(T("How much does it shorten?", size=36))
        q_b = panel(T("Where is the stress highest?", size=36))
        cards = VGroup(q_a, q_b).arrange(DOWN, buff=0.6).move_to([2.6, 0.2, 0])
        with self.say("A flagpole stands on the ground and carries nothing but its own weight. How much does it "
                      "shorten? And where inside it is the stress highest? Let's answer both with finite "
                      "elements.") as d:
            self.play(FadeIn(floor_l), GrowFromEdge(col, DOWN), run_time=.2 * d)
            self.play(FadeIn(q_a, shift=LEFT * .3), run_time=.15 * d)
            self.wait(.1 * d)
            self.play(FadeIn(q_b, shift=LEFT * .3), run_time=.15 * d)
            self.wait(.15 * d)
            self.play(Circumscribe(col, color=ACCENT), run_time=.2 * d)
            self.wait(.05 * d)

        # ---- beat 2: height L, fixed base, x upward
        ax_x = CX_L - 1.25
        x_arrow = Arrow([ax_x, BASE, 0], [ax_x, TOP + 0.7, 0], buff=0, color=INK2, stroke_width=4,
                        max_tip_length_to_length_ratio=0.06)
        x_lab = M("x", size=44).next_to(x_arrow.get_end(), LEFT, buff=0.2)
        t0 = Line([ax_x - .15, BASE, 0], [ax_x + .15, BASE, 0], color=INK2, stroke_width=4)
        tL = Line([ax_x - .15, TOP, 0], [ax_x + .15, TOP, 0], color=INK2, stroke_width=4)
        l0 = M("0", size=40).next_to(t0, LEFT, buff=0.2)
        lL = M("L", size=40).next_to(tL, LEFT, buff=0.2)
        guideL = DashedLine([ax_x, TOP, 0], [CX_L - WID / 2, TOP, 0], color=MUTED, stroke_width=2)
        rng = E(r"0|\le|x|\le|L", size=52).move_to([2.6, 0.7, 0])
        fixed = T("fixed at the base", size=34, color=MUTED).next_to(rng, DOWN, buff=0.5)
        with self.say("This example is from the course slides. The column has height L, fixed at its base. "
                      "Measure x upward from the base.") as d:
            self.play(FadeOut(cards), run_time=.15 * d)
            self.play(Create(tL), Create(guideL), FadeIn(lL), Indicate(col, color=ACCENT, scale_factor=1.02),
                      run_time=.2 * d)
            self.play(Indicate(floor_l, color=ACCENT), FadeIn(fixed), run_time=.2 * d)
            self.play(GrowArrow(x_arrow), Create(t0), FadeIn(l0), FadeIn(x_lab), run_time=.25 * d)
            self.play(Write(rng), run_time=.15 * d)
            self.wait(.05 * d)

        # ---- beat 3: the weight as a distributed load, f = c = -rho A g
        ys = np.linspace(BASE + 0.75, TOP - 0.05, 7)
        arrows = VGroup(*[force(np.array([CX_L + WID / 2 + 0.35, y, 0]), d=DOWN, length=0.55)
                          for y in ys])
        f_lab = M("f", size=44, color=ROSE).next_to(arrows, RIGHT, buff=0.25)
        rag = E(r"\rho A g", size=56).move_to([2.6, 1.3, 0])
        note = TX(r"density $\times$ area $\times$ gravity", size=32).set_color(MUTED)
        eqA = E(r"f|=|-|\rho A g", size=56).move_to([2.6, 1.3, 0])
        eqB = E(r"f|=|c|=|-|\rho A g", size=56).move_to([2.6, 1.3, 0])
        note.next_to(eqB, DOWN, buff=0.55)
        with self.say("Its weight acts all along it, pointing down. Per unit length that's rho, times A, times g: "
                      "density, times area, times gravity. Since x points up, the load is negative: f equals "
                      "minus rho A g. In our element formulas, c equals minus rho A g.") as d:
            self.play(FadeOut(rng), FadeOut(fixed), run_time=.06 * d)
            self.play(LaggedStart(*[FadeIn(a, shift=DOWN * .25) for a in arrows], lag_ratio=.15), FadeIn(f_lab),
                      run_time=.14 * d)
            self.play(Write(rag), run_time=.1 * d)
            self.play(FadeIn(note, shift=UP * .2), run_time=.1 * d)
            self.wait(.08 * d)
            # x up, load down: the minus sign
            self.play(Indicate(x_arrow, color=ACCENT), Indicate(arrows, color=ACCENT), run_time=.12 * d)
            self.play(*morph(rag, eqA, [(0, 3)]), run_time=.1 * d)
            self.play(Indicate(eqA[2], color=ACCENT, scale_factor=1.4), run_time=.08 * d)
            self.wait(.04 * d)
            self.play(*morph(eqA, eqB, [(0, 0), (1, 1), (2, 4), (3, 5)]), run_time=.1 * d)
            self.play(FadeIn(glow(eqB[2], ACCENT)), run_time=.06 * d)
            self.wait(.02 * d)

        # ---- beat 4: three equal elements, nodes 1..4, q1..q4, l = L/3
        floor_r = wall(np.array([CX_R, BASE, 0]), side=DOWN, h=2.4)
        whole_r = column(CX_R)
        ny = [BASE + k * H / N_EL for k in range(N_EL + 1)]
        elems = VGroup(*[Rectangle(width=WID, height=H / N_EL, stroke_color=INK2, stroke_width=3,
                                   fill_color=SURFACE, fill_opacity=1).move_to([CX_R, (ny[k] + ny[k + 1]) / 2, 0])
                         for k in range(N_EL)])
        dots = VGroup(*[node(np.array([CX_R, y, 0]), r=0.11) for y in ny]).set_z_index(3)
        nums = VGroup(*[M(str(k + 1), size=44).next_to([CX_R - WID / 2, y, 0], LEFT, buff=0.35)
                        for k, y in enumerate(ny)])
        q_arr = VGroup(*[Arrow([CX_R + WID / 2 + 0.25, y - 0.05, 0], [CX_R + WID / 2 + 0.25, y + 0.6, 0],
                               buff=0, color=SKY, stroke_width=5, max_tip_length_to_length_ratio=0.35)
                         for y in ny])
        q_lab = VGroup(*[E("q_%d" % (k + 1), size=44).next_to(q_arr[k], RIGHT, buff=0.15)
                         for k in range(N_EL + 1)])
        bx = CX_R + 2.2
        brace = BraceBetweenPoints([bx, ny[2], 0], [bx, ny[1], 0], direction=RIGHT, color=INK2)
        l_eq = E(r"l|=|\frac{L}{3}", size=48).next_to(brace, RIGHT, buff=0.2)
        with self.say("Use three equal elements, each of length l equals L over three. Nodes one to four, from "
                      "the base to the top. Node one sits on the ground.") as d:
            self.play(FadeOut(eqB), FadeOut(note), run_time=.08 * d)
            self.play(FadeIn(floor_r), TransformFromCopy(col, whole_r), run_time=.14 * d)
            self.add(elems)
            self.remove(whole_r)
            self.play(LaggedStart(*[GrowFromCenter(dt) for dt in dots], lag_ratio=.25), run_time=.14 * d)
            self.play(GrowFromCenter(brace), Write(l_eq), run_time=.12 * d)
            self.wait(.06 * d)
            self.play(LaggedStart(*[FadeIn(n, shift=UP * .15) for n in nums], lag_ratio=.3), run_time=.14 * d)
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(l)) for a, l in zip(q_arr, q_lab)],
                                  lag_ratio=.3), run_time=.14 * d)
            self.wait(.04 * d)
            self.play(Indicate(nums[0], color=ACCENT, scale_factor=1.4), Indicate(floor_r, color=ACCENT),
                      Flash(dots[0], color=ACCENT), run_time=.1 * d)
            self.wait(.04 * d)
        self.wipe()
