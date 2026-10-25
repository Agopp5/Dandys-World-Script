"""S07: closed sections, cut then close (BRIEF.md S07)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

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


def cond(eq, note):
    """A boxed condition: equation over a grey 'why' note."""
    body = VGroup(eq, note).arrange(DOWN, buff=.3)
    return panel(body)


class S07_Closed(VScene):
    budget = 96

    def construct(self):
        sec = hw_box(width=8.0, center=(0, -0.5))
        walls = sec.draw()
        booms = sec.booms({1: B_L, 2: B_R, 3: B_R, 4: B_L})
        names = sec.names(size=38)

        # the cut: a gap in the top wall with two short ticks
        cp = sec.p(1) + .3 * (sec.p(2) - sec.p(1))
        gap = Rectangle(width=.16, height=.4, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(cp)
        ticks = VGroup(*[Line(cp + dx * RIGHT + .28 * UP, cp + dx * RIGHT + .28 * DOWN, color=ACCENT, stroke_width=5)
                         for dx in (-.1, .1)])
        cut = VGroup(gap, ticks).set_z_index(3)
        cut_lbl = T("cut", size=34, color=ACCENT).next_to(ticks, UP, buff=.2)

        self.beat("In a closed section there is no free edge to start from. So we make one: cut any wall.",
                  Create(walls), [FadeIn(booms), FadeIn(names)], .1, [FadeIn(cut), FadeIn(cut_lbl)],
                  w=(.4, .25, .35))

        # basic open flow, wall by wall from the cut
        f12 = T("0", size=48, color=SKY).move_to(sec.mid(1, 2) + .7 * RIGHT + .5 * DOWN)
        f23 = flow(sec, 2, 3, QB23, label="q_b", size=48)
        f34 = T("0", size=48, color=SKY).move_to(sec.mid(3, 4) + .5 * UP)
        f41 = flow(sec, 4, 1, QB41, label="q_b", size=48)
        s_lbl = T("start at the cut: zero", size=30, color=MUTED).next_to(walls, DOWN, buff=.45)
        self.beat("With the cut, it's an open section. March around from the cut, jumping at each boom. "
                  "That's the basic shear flow, q b.",
                  [FadeIn(f12), FadeIn(s_lbl)], Indicate(sec.boom_m[2], color=EMBER), FadeIn(f23),
                  Indicate(sec.boom_m[3], color=EMBER), FadeIn(f34),
                  Indicate(sec.boom_m[4], color=EMBER), FadeIn(f41),
                  w=(.12, .12, .14, .12, .12, .12, .26))

        # close the cut: one constant flow round the cell
        ring = cell_flow(walls.get_center(), radius=1.1, color=MINT, ccw=True, label=r"q_{s,0}", size=48)
        eq = E(r"q_s|=|q_b|+|q_{s,0}", size=56, cmap=CMAP)
        eq.move_to(UP * 3.25)
        g = glow(eq[4], MINT)
        self.beat("Closing the cut adds one constant shear flow, q s zero, all the way around the cell.",
                  [FadeOut(cut), FadeOut(cut_lbl), FadeOut(s_lbl)], Create(ring), Write(eq), FadeIn(g),
                  w=(.15, .35, .35, .15))

        # two ways to pin down q_s0
        # slide the picture left (scaled .85: 48 -> 41 labels, 38 -> 32 boom numbers) to make room
        pic = VGroup(walls, booms, names, f12, f23, f34, f41, ring)
        pic.generate_target()
        pic.target.scale(.85, about_point=walls.get_center()).shift((-3.05 - walls.get_x()) * RIGHT)
        head = VGroup(eq, g)
        c1 = cond(E(r"S_y\,|\xi|=|\oint p\,|q_s|\,ds", size=48, cmap=CMAP),
                  VGroup(T("moment balance", size=30, color=MUTED), T("p = lever arm", size=30, color=MUTED)).arrange(DOWN, buff=.12))
        c2 = cond(E(r"\oint|q_s|\,\frac{ds}{|G|\,t}|=|0", size=48, cmap=CMAP),
                  T("shear center: no twist", size=32, color=MUTED))
        stack = VGroup(c1, c2).arrange(DOWN, buff=.4)
        stack.move_to(RIGHT * 4.1 + DOWN * .8)
        self.beat("To find q s zero, use moments. If the load passes through the shear center, there's another "
                  "condition: the section must not twist. The integral of q d s over G t around the cell is zero.",
                  [MoveToTarget(pic), head.animate.move_to(RIGHT * 3.95 + UP * 3.25)],
                  FadeIn(c1, shift=UP * .2), .1, FadeIn(c2, shift=UP * .2), Circumscribe(c2, color=ACCENT),
                  w=(.12, .2, .38, .3))
        self.wipe()
