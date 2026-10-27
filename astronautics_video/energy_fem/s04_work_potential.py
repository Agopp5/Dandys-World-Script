"""S04: the work potential, no one half (BRIEF.md S04)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the one-spring example (N, mm)
K_, F_ = 20, 100
Q_ = F_ / K_                      # equilibrium stretch
U_ = 0.5 * K_ * Q_ ** 2           # triangle
W_ = F_ * Q_                      # rectangle (dead load, no one half)
assert np.isclose(Q_, 5) and np.isclose(K_ * Q_, F_)
assert np.isclose(U_, 250) and np.isclose(W_, 500) and np.isclose(W_, 100 * 5)
assert np.isclose(W_, 2 * U_)


class S04_Work_Potential(VScene):
    budget = 166

    def construct(self):
        # ---- beat 1: a dead weight on a vertical spring
        X, TOP, END0, DROP = -4.2, 2.9, 0.9, 1.1
        ceil = wall(np.array([X, TOP, 0]), side=LEFT, h=1.6).rotate(-PI / 2, about_point=np.array([X, TOP, 0]))
        spr = spring(np.array([X, TOP, 0]), np.array([X, END0, 0]), coils=6, label=None)
        k_lab = M("K", size=40, color=LILAC).next_to(spr, LEFT, buff=.35)
        block = Rectangle(width=1.1, height=0.75, color=INK2, fill_color=SURFACE, fill_opacity=1, stroke_width=3)
        block.next_to(np.array([X, END0, 0]), DOWN, buff=0)
        arrow = force(block.get_bottom(), d=DOWN, length=1.0, label=None)
        arrow.add(M("F", size=44, color=ROSE).next_to(arrow, RIGHT, buff=.2))
        self.beat("Now the load's side of the story. Think of the load F as a heavy weight hanging on the end of "
                  "the spring. It always weighs the same, F, no matter how far the spring stretches.",
                  FadeIn(ceil), [Create(spr), FadeIn(k_lab)], FadeIn(block, shift=DOWN * .2),
                  FadeIn(arrow, shift=DOWN * .2), Indicate(block, color=ROSE), .3)

        # ---- beat 2: the weight drops by q; W = F q
        ref = DashedLine(np.array([X - 1.0, END0, 0]), np.array([X + 1.0, END0, 0]), color=MUTED, stroke_width=2)
        spr2 = spring(np.array([X, TOP, 0]), np.array([X, END0 - DROP, 0]), coils=6, label=None)
        dim = span(np.array([X + .85, END0, 0]), np.array([X + .85, END0 - DROP, 0]), "", side=RIGHT)
        dim.set_color(SKY)
        dim.add(M("q", size=44, color=SKY).next_to(dim, RIGHT, buff=.15))
        w_eq = E(r"W|=|F|\,q", size=60).move_to(np.array([2.6, 1.2, 0]))
        w_name = T("work potential of the load", size=32, color=INK2).next_to(w_eq, DOWN, buff=.45)
        self.beat("When the end moves down by q, the weight drops by q, so it loses potential energy, F times q. "
                  "That's called the work potential of the load, capital W. W equals F q.",
                  FadeIn(ref),
                  [Transform(spr, spr2), VGroup(block, arrow).animate.shift(DOWN * DROP),
                   k_lab.animate.shift(DOWN * DROP / 2)],
                  FadeIn(dim), .1, Write(w_eq), FadeIn(w_name), .2, w=(.1, .25, .15, .3, .1))

        # ---- beat 3: the key contrast, side by side
        u_eq = E(r"U|=|\tfrac12|K|q^2", size=56)
        u_eq[4].set_color(SKY)
        w_eq2 = E(r"W|=|F|\,q", size=56)
        pair = VGroup(u_eq, w_eq2).arrange(RIGHT, buff=1.2).move_to(np.array([2.6, 2.2, 0]))
        self.beat("Pay close attention here, because this is the step everybody trips on. Strain energy has a one "
                  "half, and the work potential doesn't. Why?",
                  [FadeOut(w_name), ReplacementTransform(w_eq, w_eq2), FadeIn(u_eq, shift=RIGHT * .2)],
                  self.spotlight(u_eq, w_eq2), [Indicate(u_eq[2], color=MINT, scale_factor=1.3)], .45,
                  style="slower and deliberate, stressing the key words", w=(.25, .2, .2))

        # ---- beat 4: triangle vs rectangle on the force-stretch axes
        ax = axes((0, 7, 1), (0, 140, 20), width=6, height=4, xlabel="", ylabel="")
        ax.move_to(np.array([-3.4, -0.6, 0]))
        o, qx = ax.c2p(0, 0), ax.c2p(Q_, 0)
        ax_lab = VGroup(M("u", size=38, color=SKY).next_to(ax.c2p(7, 0), RIGHT, buff=.15),
                        T("force", size=30, color=INK2).next_to(ax.c2p(0, 140), UP, buff=.15))
        line = ax.plot(lambda u: K_ * u, x_range=[0, 6.5], color=LILAC, stroke_width=4)
        tri = Polygon(o, qx, ax.c2p(Q_, F_), color=MINT, fill_color=MINT, fill_opacity=.55, stroke_width=3)
        rect = Polygon(o, qx, ax.c2p(Q_, F_), ax.c2p(0, F_), color=EMBER, fill_color=EMBER, fill_opacity=.25,
                       stroke_width=4)
        tri_lab = M("U", size=44, color=MINT).move_to(ax.c2p(Q_ * .68, F_ * .3))
        rect_lab = M("W", size=44, color=EMBER).move_to(ax.c2p(Q_ * .28, F_ * .72))
        h_lab = M("F", size=36, color=ROSE).next_to(ax.c2p(0, F_), LEFT, buff=.15)
        q_lab = M("q", size=36, color=SKY).next_to(qx, DOWN, buff=.15)
        kline_lab = M("K u", size=34, color=LILAC).next_to(ax.c2p(6.5, K_ * 6.5), RIGHT, buff=.1)
        fig = VGroup(ceil, spr, k_lab, block, arrow, ref, dim)
        with self.say("The spring's energy builds up from nothing: its force starts at zero and grows, so its energy "
                      "is a triangle. The weight is full size the whole way down: the energy it gives up is a full "
                      "rectangle, height F, width q.") as d:
            self.play(self.unspot(), FadeOut(fig), run_time=.08 * d)
            self.play(Create(ax), FadeIn(ax_lab), run_time=.1 * d)
            self.play(Create(line), FadeIn(kline_lab), run_time=.1 * d)
            self.play(DrawBorderThenFill(tri), FadeIn(tri_lab), Indicate(u_eq, color=MINT), run_time=.2 * d)
            self.wait(.07 * d)
            self.play(Create(rect), FadeIn(h_lab), FadeIn(q_lab), run_time=.2 * d)
            self.play(FadeIn(rect_lab), Indicate(w_eq2, color=EMBER), run_time=.12 * d)
            self.wait(.13 * d)

        # ---- beat 5: the numbers, W = 2U
        w_num = E(r"W|=|(100)(5)|=|500\text{ N mm}", size=48)
        u_num = E(r"U|=|250\text{ N mm}", size=48)
        nums = VGroup(w_num, u_num).arrange(DOWN, buff=.5, aligned_edge=LEFT).move_to(np.array([3.3, .2, 0]))
        br_lab = VGroup(E(r"W|=|2|U", size=48), T("at the answer", size=32, color=INK2)).arrange(RIGHT, buff=.3)
        br = Brace(nums, DOWN, color=INK2)
        br_lab.next_to(br, DOWN, buff=.2)
        self.beat("In other words, U is the triangle, W is the whole rectangle. With our numbers, W is one hundred "
                  "newtons times five millimeters, five hundred newton millimeters. Exactly twice U.",
                  [Indicate(tri, color=MINT), Indicate(tri_lab)], [Indicate(rect, color=EMBER), Indicate(rect_lab)],
                  Write(w_num), FadeIn(u_num, shift=UP * .2), [GrowFromCenter(br), FadeIn(br_lab)],
                  FadeIn(glow(br_lab[0], GOLD)), .2, w=(.12, .12, .3, .14, .1, .05))
        self.wipe()
