"""S23: recap of idealization, boom jumps and multi-cell torsion (BRIEF.md S23; rework of old/s17_recap.py)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})


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
# single cell: q = T/(2A) on the 500 x 250 example: 40 N/mm
assert np.isclose(10e6 / (2 * 500 * 250), 40)
# multi-cell torsion, HW P2 per unit torque: T = 2 A_I q_I + 2 A_II q_II
qII = 1 / (2 * 232_000 * 1.569 + 2 * 258_000)
assert np.isclose(qII, 0.804e-6, rtol=2e-3)
assert np.isclose(24_200 / 27_600, 0.8768, rtol=1e-3)   # t* = (G/G_REF) t for the skins


def card(n, heading, rows, buff=1.0):
    """One recap card: numbered heading on top, formula rows under it, on a SURFACE panel."""
    head = VGroup(badge(n), T(heading, size=34, color=INK)).arrange(RIGHT, buff=.3)
    body = VGroup(*[VGroup(*r).arrange(RIGHT, buff=buff) for r in rows]).arrange(DOWN, buff=.2, aligned_edge=LEFT)
    inner = VGroup(head, body).arrange(DOWN, buff=.18, aligned_edge=LEFT)
    body.shift(RIGHT * .55)
    return panel(inner), head, body


class S23_Recap(VScene):
    budget = 96

    def construct(self):
        # card 1: idealization
        b1 = E(r"B_1|=|\frac{t_D\,b}{6}|\Big(2+|\frac{\sigma_2}{\sigma_1}|\Big)", size=52)
        paint(b1, {4: GOLD})
        n1 = T("skin's direct stress, lumped into the booms", size=32, color=MUTED)
        c1, h1, m1 = card(1, "Booms carry the direct stress; the skin carries shear", [[b1, n1]], buff=.7)

        # card 2: boom jumps and closing a section
        jump = E(r"q_2|-|q_1|=|-\Big(|S_y|/I_{xx}\Big)|B_r|y_r", size=52)
        close = E(r"q_s|=|q_b|+|q_{s,0}", size=52)
        paint(close, {0: SKY})
        n2 = T("cut, march, close", size=32, color=MUTED)
        c2, h2, m2 = card(2, "Shear flow: constant between booms, jumps at each one",
                          [[jump, close, n2]], buff=.8)

        # card 3: torsion, one cell then several
        one = E(r"T|=|2A|\,q", size=52)
        paint(one, {3: SKY})
        n3a = T("one cell", size=32, color=MUTED)
        many = E(r"T|=|\sum_R 2A_R|\,q_R", size=52)
        paint(many, {3: SKY})
        n3b = T("several cells, one q each", size=32, color=MUTED)
        twist = VGroup(M(r"\frac{d\theta}{dz}", size=52), T("equal in every cell", size=34, color=INK2)
                       ).arrange(RIGHT, buff=.25)
        ts = E(r"t^*|=|\frac{G}{G_{\mathrm{ref}}}|\,t", size=52)
        paint(ts, {2: ACCENT})
        c3, h3, m3 = card(3, "Torsion: one constant shear flow per cell",
                          [[one, n3a, many, n3b], [twist, ts]], buff=.6)

        cards = VGroup(c1, c2, c3)
        w = max(c.width for c in cards)
        for c in cards:      # equal-width rows, left-aligned content
            c[0].stretch_to_fit_width(w)
        cards.arrange(DOWN, buff=.1)
        w0, h0 = cards.width, cards.height
        fit(cards, 13.8, 7.8)
        s = min(cards.width / w0, cards.height / h0)
        assert s > .86, s    # math stays >= 44, notes >= 27.5
        cards.move_to(ORIGIN)
        for c, inner in ((c1, VGroup(h1, m1)), (c2, VGroup(h2, m2)), (c3, VGroup(h3, m3))):
            inner.align_to(c[0], LEFT).shift(RIGHT * .35)

        self.beat("Let's recap. Booms carry the direct stress, and the skin carries shear. Any direct stress the skin does carry is added to the booms with t D b over six, times two plus the stress ratio.",
                  FadeIn(c1[0]), FadeIn(h1), .12, Write(b1[:3]), Write(b1[3:]), FadeIn(n1, shift=UP * .1),
                  Circumscribe(b1[2:], color=GOLD), .15, w=(.06, .1, .12, .2, .14, .15))

        self.beat("Shear flow is constant between booms, and jumps at each one. For a closed section: cut, march around, then close with q s zero.",
                  FadeIn(c2[0]), FadeIn(h2), .1, Write(jump), .1, Write(close), FadeIn(n2),
                  Indicate(close[4], color=MINT), .12, w=(.05, .1, .22, .16, .12, .12))

        self.beat("In torsion, a single cell has T equals two A q. With several cells, each has its own q: the torque gives one equation, equal twist gives the rest, and different materials just scale the thickness.",
                  FadeIn(c3[0]), FadeIn(h3), Write(one), FadeIn(n3a), .06, Write(many), FadeIn(n3b), .04,
                  FadeIn(twist), .04, Write(ts), Circumscribe(ts, color=ACCENT), .1,
                  w=(.03, .07, .1, .06, .14, .08, .13, .12, .1))
        self.wait(2.0)
        self.wipe()
