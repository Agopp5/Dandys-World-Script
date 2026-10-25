"""S17: recap of idealization, boom jumps and multi-cell torsion (BRIEF.md S17)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})


# facts: the three summary formulas, checked on numbers from earlier scenes
def boom(tD, b, ratio):
    """B_1 = (t_D b / 6)(2 + sigma_2/sigma_1)."""
    return tD * b / 6 * (2 + ratio)

# the moment balance about boom 2 reproduces the formula (sigma_1 = 1, sigma_2 = r)
for r in (1.0, -1.0, 0.3):
    tD, b = 10.0, 500.0
    lhs = r * tD * b**2 / 2 + 0.5 * (1 - r) * tD * b * (2 / 3) * b
    assert np.isclose(lhs / b, boom(tD, b, r))
assert np.isclose(boom(10, 500, 1), 2500)        # HW P1 skin share
assert np.isclose(boom(10, 300, -1), 500)        # HW P1 left web share
# boom jump on the channel: q_12 = 0 - 1e-4 * 300 * 200 = -6 N/mm
assert np.isclose(0 - 4800 / 48e6 * 300 * 200, -6)
# multi-cell torsion, HW P2 per unit torque: T = 2 A_I q_I + 2 A_II q_II
qII = 1 / (2 * 232_000 * 1.569 + 2 * 258_000)
assert np.isclose(qII, 0.804e-6, rtol=2e-3)
assert np.isclose(24_200 / 27_600, 0.8768, rtol=1e-3)   # t* = (G/G_REF) t for the skins


def card(n, heading, maths, buff=1.0):
    """One recap row: numbered heading on top, the formulas in a line under it, on a SURFACE panel."""
    head = VGroup(badge(n), T(heading, size=38, color=INK)).arrange(RIGHT, buff=.3)
    body = VGroup(*maths).arrange(RIGHT, buff=buff, aligned_edge=DOWN)
    inner = VGroup(head, body).arrange(DOWN, buff=.35, aligned_edge=LEFT)
    body.shift(RIGHT * .55)
    return panel(inner), head, body


class S17_Recap(VScene):
    budget = 94

    def construct(self):
        # card 1: idealization
        b1 = E(r"B_1|=|\frac{t_D\,b}{6}|\Big(2+|\frac{\sigma_2}{\sigma_1}|\Big)", size=56)
        paint(b1, {4: GOLD})
        n1 = T("skin's direct stress, lumped into the booms", size=30, color=MUTED)
        c1, h1, m1 = card(1, "Booms carry the direct stress; the skin carries shear",
                          [b1, n1], buff=.7)

        # card 2: boom jumps and closing a section
        jump = E(r"q_2|-|q_1|=|-\Big(|S_y|/I_{xx}\Big)|B_r|y_r", size=56)
        close = E(r"q_s|=|q_b|+|q_{s,0}", size=56)
        paint(close, {0: SKY})
        n2 = T("cut, march, close", size=30, color=MUTED)
        closeg = VGroup(close, n2).arrange(DOWN, buff=.15)
        c2, h2, m2 = card(2, "Shear flow: constant between booms, jumps at each one",
                          [jump, closeg], buff=1.2)

        # card 3: multi-cell torsion
        tq = E(r"T|=|\sum_R 2A_R|\,q_R", size=56)
        paint(tq, {3: SKY})
        twist = VGroup(M(r"\frac{d\theta}{dz}", size=56), T("equal in every cell", size=34, color=INK2)
                       ).arrange(RIGHT, buff=.25)
        ts = E(r"t^*|=|\frac{G}{G_{\mathrm{ref}}}|\,t", size=56)
        paint(ts, {2: ACCENT})
        c3, h3, m3 = card(3, "Pure torsion: one constant shear flow per cell",
                          [tq, twist, ts], buff=.9)

        cards = VGroup(c1, c2, c3)
        w = max(c.width for c in cards)
        for c in cards:      # equal-width rows, left-aligned content
            c[0].stretch_to_fit_width(w)
        cards.arrange(DOWN, buff=.3)
        assert False, [(len(c), [(type(s).__name__, round(s.width, 2), round(s.height, 2)) for s in c]) for c in cards] + [(h1.width, m1.width, m3.width, h3.height, m2.height)]
        cards.move_to(ORIGIN)
        for c, inner in ((c1, VGroup(h1, m1)), (c2, VGroup(h2, m2)), (c3, VGroup(h3, m3))):
            inner.align_to(c[0], LEFT).shift(RIGHT * .35)

        self.beat("Let's recap. Booms carry the direct stress. The skin carries shear, and any direct stress it takes is added to the booms with t D b over six times two plus the stress ratio.",
                  FadeIn(c1[0]), FadeIn(h1), .1, Write(b1), FadeIn(n1, shift=UP * .1), .1,
                  Circumscribe(b1[2:], color=GOLD), w=(.06, .1, .3, .14, .25))

        self.beat("The shear flow is constant between booms, and jumps by minus S y over I x x, B r y r, at each one. Closed sections: cut, march, then close with q s zero.",
                  FadeIn(c2[0]), FadeIn(h2), Write(jump), Indicate(jump[4:]), .05,
                  Write(close), FadeIn(n2), Indicate(close[4], color=MINT),
                  w=(.04, .08, .2, .18, .17, .1, .18))

        self.beat("In pure torsion, each cell has one shear flow. The torque gives one equation, and equal twist gives the rest. Different materials just scale the thickness.",
                  FadeIn(c3[0]), FadeIn(h3), .05, Write(tq), .05, FadeIn(twist), .05, Write(ts),
                  Circumscribe(ts, color=ACCENT), w=(.04, .1, .17, .17, .17, .18))
        self.wait(1.5)
        self.wipe()
