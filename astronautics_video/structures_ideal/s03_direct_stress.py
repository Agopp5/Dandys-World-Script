"""S03: direct stress from bending (BRIEF.md S03)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# facts: the HW P1 box (500 x 300 mm), symmetric top/bottom, so the neutral axis is at mid-height (y = 0)
BOX_W, BOX_H = 500, 150
assert np.isclose((150 + -150) / 2, 0)
# I_xx = sum A y^2 (the same rule later gives the HW box: 2(4000 + 3556)(150)^2 = 340.0 x 10^6 mm^4)
assert np.isclose(2 * (4000 + 3556) * 150 ** 2 / 1e6, 340.0, atol=0.05)
# sigma_z = (M_x/I_xx) y is linear in y: zero at the axis, +/- equal at y = +/-150
PROFILE_Y = [150, 100, 50, -50, -100, -150]
assert all(np.isclose(-(y / 150), (-y) / 150) for y in PROFILE_Y)

SEC_W, SEC_C = 6.4, (-3.0, -0.2)


def vspan(top, bot, label, side=RIGHT, color=INK2, size=40):
    """Vertical dimension marker from bot to top with a TeX label beside it."""
    ln = Line(bot, top, color=color, stroke_width=3)
    t1 = Line(top + LEFT * .1, top + RIGHT * .1, color=color, stroke_width=3)
    t2 = Line(bot + LEFT * .1, bot + RIGHT * .1, color=color, stroke_width=3)
    lab = M(label, size=size, color=color).next_to(ln, side, buff=.12)
    return VGroup(ln, t1, t2, lab)


class S03_Direct_Stress(VScene):
    budget = 94

    def construct(self):
        sec = hw_box(width=SEC_W, center=SEC_C)
        o = (sec.p(1) + sec.p(4)) / 2                    # left web at y = 0
        k = (sec.p(2)[0] - sec.p(1)[0]) / BOX_W         # scene units per mm

        def P(x, y):
            return o + np.array([x * k, y * k, 0])

        walls = sec.draw()
        na = DashedLine(P(-40, 0), P(BOX_W + 40, 0), color=MUTED, stroke_width=3, dash_length=.15)
        na_lab = T("neutral axis", size=30, color=MUTED).next_to(P(20, 0), UR, buff=.12)
        sig = E(r"\sigma_z", size=64).move_to([4.6, 2.3, 0])
        sig_note = VGroup(T("direct stress", size=34),
                          T("points along the span (z)", size=30, color=MUTED)).arrange(DOWN, buff=.15)
        sig_note.next_to(sig, DOWN, buff=.3)

        self.section("Direct stress from bending")
        self.beat("Bending produces direct stress: stress that points along the span. We'll call it sigma z.",
                  Create(walls), [Create(na), FadeIn(na_lab)], .1,
                  FadeIn(sig_note, shift=UP * .2), .1, Write(sig), FadeIn(glow(sig, GOLD)), .2,
                  w=(.3, .2, .15, .1, .1))

        # beat 2: linear stress profile beside the section (tension + above, compression - below)
        x0 = 1.9
        L = 1.25                                          # arrow length at |y| = 150 mm
        ax_line = Line([x0, P(0, 165)[1], 0], [x0, P(0, -165)[1], 0], color=AXIS, stroke_width=3)
        zero_tick = DashedLine(P(BOX_W + 40, 0), [x0 + .3, o[1], 0], color=MUTED, stroke_width=2, dash_length=.12)
        arrows = {}
        for y in PROFILE_Y:
            Y = P(0, y)[1]
            arrows[y] = Arrow([x0, Y, 0], [x0 + L * y / 150, Y, 0], buff=0, color=GOLD, stroke_width=5,
                              max_tip_length_to_length_ratio=.25, max_stroke_width_to_length_ratio=20)
        up = VGroup(*[arrows[y] for y in PROFILE_Y if y > 0])
        dn = VGroup(*[arrows[y] for y in PROFILE_Y if y < 0])
        env = Line([x0 + L, P(0, 150)[1], 0], [x0 - L, P(0, -150)[1], 0], color=GOLD, stroke_width=3)
        ten = VGroup(T("tension", size=34), M("+", size=48, color=GOLD)).arrange(RIGHT, buff=.15)
        ten.next_to(arrows[150], RIGHT, buff=.2)
        com = VGroup(T("compression", size=34), M("-", size=48, color=GOLD)).arrange(RIGHT, buff=.15)
        com.next_to([x0, P(0, -150)[1], 0], RIGHT, buff=.25)
        zero = M("0", size=44, color=INK2).next_to([x0, o[1], 0], RIGHT, buff=.2).shift(UP * .25)
        cap = T("stress across the height", size=30, color=MUTED).next_to(ax_line, UP, buff=.25)
        self.beat("Above the neutral axis the material is stretched, and below it the material is squeezed. "
                  "The farther from the axis, the bigger the stress.",
                  [sig.animate.scale(.8).move_to([5.6, 3.2, 0]), FadeOut(sig_note), Create(ax_line), FadeIn(cap)],
                  LaggedStart(*[GrowArrow(a) for a in up], lag_ratio=.3),
                  FadeIn(ten), .1, LaggedStart(*[GrowArrow(a) for a in dn], lag_ratio=.3), FadeIn(com), .1,
                  [Create(env), FadeIn(zero), Create(zero_tick)], .2,
                  w=(.12, .16, .08, .16, .08, .16))
        profile = VGroup(ax_line, zero_tick, up, dn, env, ten, com, zero, cap)

        # beat 3: sigma_z = (M_x / I_xx) y, each symbol labelled once
        eq = E(r"\sigma_z|=|\frac{M_x}{I_{xx}}|\,y", size=60).move_to([3.9, 2.2, 0])
        rows = VGroup(*[VGroup(E(s, size=48), T(n, size=30, color=INK2)).arrange(RIGHT, buff=.35)
                        for s, n in [(r"M_x", "bending moment"), (r"I_{xx}", "second moment of area"),
                                     (r"y", "height above the neutral axis")]])
        rows.arrange(DOWN, buff=.4, aligned_edge=LEFT).next_to(eq, DOWN, buff=.6).set_x(3.9)
        fit(rows, 6.0, 3.0)
        pt = Dot(P(BOX_W, 100), radius=.1, color=GOLD)
        ysp = vspan(P(BOX_W - 45, 100), P(BOX_W - 45, 0), "y", side=LEFT, size=44)
        self.beat("The formula, for bending about the horizontal axis, is sigma z equals M x over I x x, times y. "
                  "Here y is the height above the neutral axis.",
                  [FadeOut(profile), ReplacementTransform(sig, eq[0])], Write(eq[1]), Write(eq[2]), Write(eq[3]),
                  .1, FadeIn(rows[0], shift=LEFT * .2), FadeIn(rows[1], shift=LEFT * .2), .05,
                  [FadeIn(rows[2], shift=LEFT * .2), FadeIn(pt), Create(ysp)], .2,
                  w=(.12, .05, .12, .08, .1, .1, .12))

        # beat 4: I_xx = sum A y^2, small squares at different heights
        pieces = [(1, 110, 150, UP, RIGHT), (2, BOX_W, 60, RIGHT, LEFT), (3, 330, -150, DOWN, RIGHT)]
        cm = {"A_1": EMBER, "A_2": EMBER, "A_3": EMBER, "A": EMBER}
        bits = []
        for i, x, y, aside, yside in pieces:
            sq = Square(.32, color=EMBER, fill_opacity=.85, stroke_width=2).move_to(P(x, y))
            a_lab = E("A_%d" % i, size=40, cmap=cm).next_to(sq, aside, buff=.15)
            sx = x - 45 if i == 2 else x
            sp = vspan(P(sx, y), P(sx, 0), "y_%d" % i, side=yside, size=40)
            if i == 2:
                sp = vspan(P(sx, y), P(sx, 0), "y_2", side=LEFT, size=40)
            bits.append(VGroup(sq, a_lab, sp))
        ix = E(r"I_{xx}|=|\sum|A|\,y^2", size=60, cmap=cm).next_to(eq, DOWN, buff=.8).set_x(3.9)
        ix_note = VGroup(T("each small piece:", size=30, color=INK2),
                         T("its area times its height squared,", size=30, color=INK2),
                         T("all added up", size=30, color=INK2)).arrange(DOWN, buff=.15)
        ix_note.next_to(ix, DOWN, buff=.45)
        self.beat("I x x measures how much area sits far from the axis. "
                  "For small pieces, it's just each area times its height squared, all added up.",
                  [FadeOut(rows), FadeOut(pt), FadeOut(ysp)], LaggedStart(*[FadeIn(b) for b in bits], lag_ratio=.5),
                  .1, [Write(ix[0]), Write(ix[1])], [Indicate(VGroup(*[b[0] for b in bits]), color=EMBER),
                                                      Write(ix[3])],
                  [Indicate(VGroup(*[b[2] for b in bits]), color=INK), Write(ix[4])], Write(ix[2]),
                  FadeIn(ix_note), FadeIn(glow(ix, GOLD)), .2,
                  w=(.08, .2, .08, .1, .1, .08, .1, .06))
        self.wait(1.0)
        self.wipe()
