"""S11: closed sections, cut then close (BRIEF.md S11). Rework of old/s07_closed.py."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# facts (HW P1 box, cut in wall 12, s runs 1 -> 2 -> 3 -> 4 -> 1), basic flows per unit S_y
B_L, B_R, Y = 4000.0, 3556.0, 150.0
IXX = 2 * (B_L + B_R) * Y ** 2
assert np.isclose(IXX, 340.0e6, rtol=1e-3)
QB12 = 0.0                                   # starts at the cut: zero
QB23 = QB12 - (1 / IXX) * B_R * Y            # jump at boom 2
QB34 = QB23 - (1 / IXX) * B_R * (-Y)         # jump at boom 3
QB41 = QB34 - (1 / IXX) * B_L * (-Y)         # jump at boom 4
assert np.isclose(QB23, -1.569e-3, rtol=2e-3) and np.isclose(QB34, 0.0, atol=1e-12)
assert np.isclose(QB41, 1.765e-3, rtol=2e-3)

CMAP = {"q_s": SKY}
RX = 4.15                                    # centre line of the right-hand column


def note(*lines, size=32):
    return VGroup(*[T(s, size=size, color=MUTED) for s in lines]).arrange(DOWN, buff=.14)


def cond(eq, why):
    """A boxed condition: equation over a grey 'why' note."""
    return panel(VGroup(eq, why).arrange(DOWN, buff=.3))


class S11_Closed(VScene):
    budget = 131

    def construct(self):
        sec = hw_box(width=6.8, center=(-3.1, -0.3))
        walls = sec.draw()
        booms = sec.booms({1: B_L, 2: B_R, 3: B_R, 4: B_L})
        names = sec.names(size=40)

        # beat 1: a closed box, no free edge
        n1 = VGroup(T("closed section", size=44, color=INK),
                    note("walls go all the way round", "no free edge with zero flow", size=34)).arrange(DOWN, buff=.35)
        n1.move_to(RIGHT * RX + UP * .6)
        self.beat("A box is a closed section. Its walls go all the way around, so there's no free edge where we "
                  "know the shear flow is zero.",
                  Create(walls), [FadeIn(booms), FadeIn(names)], .08, FadeIn(n1[0]), FadeIn(n1[1]), .15,
                  w=(.3, .12, .12, .23))

        # beat 2: cut the top wall
        cp = sec.p(1) + .3 * (sec.p(2) - sec.p(1))
        gap = Rectangle(width=.18, height=.42, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(cp)
        ticks = VGroup(*[Line(cp + dx * RIGHT + .3 * UP, cp + dx * RIGHT + .3 * DOWN, color=ACCENT, stroke_width=6)
                         for dx in (-.11, .11)])
        cut = VGroup(gap, ticks).set_z_index(3)
        cut_lbl = T("cut", size=36, color=ACCENT).next_to(ticks, UP, buff=.2)
        n2 = VGroup(T("cut one wall", size=44, color=INK),
                    E(r"q|=|0", size=48), note("at the cut:", "an open section again", size=34)).arrange(DOWN, buff=.35)
        n2.move_to(RIGHT * RX + UP * .6)
        self.beat("So we make one. Imagine cutting any wall. Now it's an open section, and the shear flow is zero "
                  "at the cut.",
                  FadeOut(n1), .05, [FadeIn(cut), FadeIn(cut_lbl)], Circumscribe(ticks, color=ACCENT), .05,
                  [FadeIn(n2[0]), FadeIn(n2[2])], FadeIn(n2[1]), .15,
                  w=(.08, .15, .12, .2, .2))

        # beat 3: basic open flow, wall by wall from the cut
        f12 = T("0", size=48, color=SKY).move_to(sec.mid(1, 2) + .9 * RIGHT + .5 * DOWN)
        f23 = flow(sec, 2, 3, QB23, label="q_b", size=46)
        f34 = T("0", size=48, color=SKY).move_to(sec.mid(3, 4) + .5 * UP)
        f41 = flow(sec, 4, 1, QB41, label="q_b", size=46)
        n3 = VGroup(T("basic shear flow", size=44, color=INK), E(r"q_b", size=60),
                    note("constant between booms,", "jumps at each boom", size=34)).arrange(DOWN, buff=.35)
        n3.move_to(RIGHT * RX + UP * .6)
        self.beat("March around from the cut, jumping at each boom, exactly as for the channel. The result is "
                  "called the basic shear flow, q b.",
                  FadeOut(n2), FadeIn(f12), Indicate(sec.boom_m[2], color=EMBER), FadeIn(f23),
                  Indicate(sec.boom_m[3], color=EMBER), FadeIn(f34),
                  Indicate(sec.boom_m[4], color=EMBER), FadeIn(f41), [FadeIn(n3[0]), FadeIn(n3[2])],
                  FadeIn(n3[1]), .12,
                  w=(.05, .08, .07, .09, .07, .09, .07, .09, .13, .14))

        # beat 4: close the cut, one constant flow round the cell
        ring = cell_flow(walls.get_center(), radius=1.0, color=MINT, ccw=True, label=r"q_{s,0}", size=46)
        eq = E(r"q_s|=|q_b|+|q_{s,0}", size=60, cmap=CMAP)
        eq.move_to(RIGHT * RX + UP * 2.7)
        g = glow(eq[4], MINT)
        why = note("one constant,", "all the way round", size=34).next_to(eq, DOWN, buff=.35)
        self.beat("Of course, the real box isn't cut. Closing the cut adds one extra constant shear flow, q s zero, "
                  "all the way around.",
                  [FadeOut(n3), FadeOut(cut), FadeOut(cut_lbl)], .08, Create(ring),
                  Write(eq[:3]), [Write(eq[3:]), FadeIn(g)], FadeIn(why), .15,
                  w=(.1, .2, .17, .2, .1))

        # beat 5: two ways to pin down q_s0
        c1 = cond(E(r"S_y\,|\xi|=|\oint p\,|q_s|\,ds", size=46, cmap=CMAP),
                  note("moment balance:", "same moment as the load", size=30))
        c2 = cond(E(r"\oint|q_s|\,\frac{ds}{|G|\,t}|=|0", size=46, cmap=CMAP),
                  note("load at shear centre:", "the box must not twist", size=30))
        stack = VGroup(c1, c2).arrange(DOWN, buff=.35)
        stack.next_to(eq, DOWN, buff=.4).set_x(RX)
        with self.say("To find q s zero, use moments: the shear flows must make the same moment as the load. And if "
                      "the load is at the shear centre, there's a simpler condition: the box must not twist.") as d:
            self.play(FadeOut(why), run_time=.06 * d)
            self.play(FadeIn(c1, shift=UP * .2), run_time=.14 * d)
            self.wait(.28 * d)
            self.play(FadeIn(c2, shift=UP * .2), run_time=.14 * d)
            self.play(Circumscribe(c2, color=ACCENT), run_time=.18 * d)
            self.wait(.2 * d)
        self.wait(1.0)
        self.wipe()
