"""S06: the channel, step by step (BRIEF.md S06)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

# facts: the slide's channel. Four booms B = 300 mm^2 at y = +-200 mm, S_y = 4.8 kN through the shear centre.
B, H, S_Y = 300.0, 200.0, 4.8e3
IXX = 4 * B * H ** 2
assert np.isclose(IXX, 48e6)
K = S_Y / IXX
assert np.isclose(K, 1e-4)
YS = {1: H, 2: H, 3: -H, 4: -H}
Q = [0.0]
for r in (1, 2, 3, 4):                       # q_after - q_before = -(S_y/I_xx) B_r y_r
    Q.append(Q[-1] - K * B * YS[r])
q12, q23, q34, q_end = Q[1:]
assert np.allclose([q12, q23, q34, q_end], [-6, -12, -6, 0])
# shear centre (where the S_y arrow is drawn): flange couple balances S_y xi about the web
XI = (-q12) * 200 * 400 / S_Y
assert np.isclose(XI, 100.0)
S_POS = [0, 200, 600, 800]                   # arc length s (mm) at booms 1..4: flange 200, web 400, flange 200


class S06_Channel(VScene):
    budget = 137

    def construct(self):
        sec = channel(width=2.6, center=(-4.3, -0.2))
        walls = sec.draw()
        booms = sec.booms({n: B for n in (1, 2, 3, 4)})
        names = sec.names(size=30)
        mm = (sec.p(1)[0] - sec.p(2)[0]) / 200.0
        xs = sec.p(2)[0] - XI * mm
        sy_arr = Arrow([xs, -1.3, 0], [xs, 0.9, 0], buff=0, color=ROSE, stroke_width=6)
        sy_lab = VGroup(M("S_y", size=40, color=ROSE), M(r"4.8\ \text{kN}", size=32, color=ROSE)).arrange(DOWN, buff=0.12)
        sy_lab.next_to(sy_arr, DOWN, buff=0.15)
        b_lab = E(r"B|=|300\ \text{mm}^2", size=40).move_to(sec.mid(2, 3)).shift(1.4 * RIGHT)

        # staircase plot of q along s (bottom right)
        ax = axes((-100, 900, 200), (-14, 2, 2), width=8.2, height=2.5, xlabel="s", ylabel="q").to_corner(DR, buff=0.4)
        ax.shift(0.15 * UP)
        bl = VGroup(*[DashedLine(ax.c2p(s, 1.5), ax.c2p(s, -13.5), color=EMBER, stroke_width=2, dash_length=0.08)
                      for s in S_POS])
        bnum = VGroup(*[T(str(i + 1), 26, EMBER).next_to(bl[i], UP, buff=0.05) for i in range(4)])
        lvl = [-4, -9, -3]                           # shape only: arbitrary step heights
        gpts = [(-100, 0), (0, 0), (0, lvl[0]), (200, lvl[0]), (200, lvl[1]), (600, lvl[1]),
                (600, lvl[2]), (800, lvl[2]), (800, 0), (900, 0)]
        ghost = DashedVMobject(VMobject(color=MUTED, stroke_width=4).set_points_as_corners([ax.c2p(*p) for p in gpts]),
                               num_dashes=60)
        flats = VGroup(*[Line(ax.c2p(a, v), ax.c2p(b, v), color=INK2, stroke_width=7)
                         for a, b, v in [(0, 200, lvl[0]), (200, 600, lvl[1]), (600, 800, lvl[2])]])
        jumps = VGroup(*[Dot(ax.c2p(s, (lvl + [0])[i] / 2 + ([0] + lvl)[i] / 2), radius=0.09, color=EMBER)
                         for i, s in enumerate(S_POS)])
        shape_note = T("shape only: flat between booms", 26, MUTED).next_to(ax, UP, buff=0.15).align_to(ax, RIGHT)

        self.beat("Between booms the skin carries no direct stress, so the shear flow is constant. It only changes when it crosses a boom.",
                  [Create(walls), FadeIn(booms), FadeIn(names)], [GrowArrow(sy_arr), FadeIn(sy_lab), FadeIn(b_lab)],
                  [Create(ax), FadeIn(bl), FadeIn(bnum)], [Create(ghost), FadeIn(shape_note)],
                  [Create(flats), Indicate(walls, color=SKY)], [FadeIn(jumps, scale=1.6), Indicate(booms, color=EMBER, scale_factor=1.3)],
                  w=(.17, .13, .15, .17, .2, .18))

        # beat 2: I_xx and S_y / I_xx
        ix = E(r"I_{xx}|=|4\,|(300)|(200)^2|=|48\times 10^6\ \text{mm}^4", size=40)
        paint(ix, {3: EMBER})
        ix_note = TX(r"four booms of $300\ \text{mm}^2$, each at $y=\pm 200$ mm", size=26).set_color(MUTED)
        k = E(r"S_y|/|I_{xx}|=|4.8\times 10^3|/|48\times 10^6|=|10^{-4}\ \text{N/mm}^4", size=40)
        paint(k, {3: ROSE})
        alg = VGroup(ix, ix_note, k).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        alg[2].shift(0.2 * DOWN)
        alg.to_corner(UR, buff=0.5).shift(0.1 * DOWN)
        g_k = glow(k[6], GOLD)
        self.beat("For this channel, I x x is four times three hundred times two hundred squared: forty eight million. So S y over I x x is ten to the minus four.",
                  [FadeOut(ghost), FadeOut(flats), FadeOut(jumps), FadeOut(shape_note)], Write(ix), FadeIn(ix_note), .1,
                  Write(k), FadeIn(g_k), w=(.1, .3, .1, .05, .33, .12))

        # beat 3: fold, the jump rule, first boom
        kbox = VGroup(E(r"S_y|/|I_{xx}|=|10^{-4}", size=40))
        kbox = panel(kbox[0], color=GOLD)
        rule = E(r"q_2|-|q_1|=|-\,|S_y|/|I_{xx}|\,B_r|\,y_r", size=40)
        paint(rule, {6: EMBER})
        top = VGroup(rule, kbox).arrange(RIGHT, buff=0.5)
        top.to_corner(UR, buff=0.45)
        rule_note = T("the jump at each boom", 26, MUTED).next_to(rule, DOWN, buff=0.12).align_to(rule, LEFT)
        l1 = E(r"q_{12}|=|0|-|10^{-4}|(300)|(200)|=|-6\ \text{N/mm}", size=40)
        paint(l1, {0: SKY, 5: EMBER, 8: SKY})
        l1_note = T("boom 1", 26, EMBER)
        row1 = VGroup(l1_note, l1).arrange(RIGHT, buff=0.35)
        row1.next_to(rule_note, DOWN, buff=0.4).align_to(rule, LEFT)
        f12 = flow(sec, 1, 2, q12, label="-6")
        st0 = Line(ax.c2p(-100, 0), ax.c2p(0, 0), color=SKY, stroke_width=6)
        st1 = VMobject(color=SKY, stroke_width=6).set_points_as_corners(
            [ax.c2p(0, 0), ax.c2p(0, -6), ax.c2p(200, -6)])
        v1 = M("-6", size=30, color=SKY).next_to(ax.c2p(100, -6), UP, buff=0.1)
        free = T("free edge", 26, MUTED).next_to(sec.p(1), RIGHT, buff=0.5).shift(0.15 * DOWN)
        self.beat("Start at the free edge, where q is zero. Crossing boom one: zero minus ten to the minus four, times three hundred, times two hundred. Minus six newtons per millimeter.",
                  [FadeOut(ix), FadeOut(ix_note), FadeOut(g_k), ReplacementTransform(k, kbox[1]), FadeIn(kbox[0])],
                  [FadeIn(free), Flash(sec.p(1), color=SKY), Create(st0)], [Write(rule), FadeIn(rule_note)],
                  [FadeIn(l1_note), Write(l1[:8])], [Indicate(booms[0], color=EMBER, scale_factor=1.5), Create(st1)],
                  [Write(l1[8:]), FadeIn(f12), FadeIn(v1)],
                  w=(.1, .17, .2, .25, .13, .15))

        # beat 4: checkpoint cue
        self.beat("Your turn. Pause here and do checkpoint two point one in your guide.",
                  Circumscribe(VGroup(booms[1], booms[2], booms[3]), color=EMBER), .5)
        self.checkpoint("2.1", "Carry the shear flow past booms 2, 3 and 4")

        # beat 5: booms 2, 3, 4; the staircase completes
        def row(tag, tex, cols):
            e = E(tex, size=40)
            paint(e, cols)
            return VGroup(T(tag, 26, EMBER), e).arrange(RIGHT, buff=0.35)
        r2 = row("boom 2", r"q_{23}|=|-6|-|10^{-4}|(300)|(200)|=|-12", {0: SKY, 2: SKY, 5: EMBER, 8: SKY})
        r3 = row("boom 3", r"q_{34}|=|-12|-|10^{-4}|(300)|(-200)|=|-6", {0: SKY, 2: SKY, 5: EMBER, 8: SKY})
        r4 = row("boom 4", r"q_{\text{end}}|=|-6|-|10^{-4}|(300)|(-200)|=|0", {0: SKY, 2: SKY, 5: EMBER, 8: SKY})
        rows = VGroup(r2, r3, r4).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows.next_to(rule_note, DOWN, buff=0.45).align_to(rule, LEFT)
        for r in rows:                          # line the equals signs up
            r[1].shift((rows[0][1][1].get_x() - r[1][1].get_x()) * RIGHT)
        f23 = flow(sec, 2, 3, q23, label="-12")
        f34 = flow(sec, 3, 4, q34, label="-6")
        st2 = VMobject(color=SKY, stroke_width=6).set_points_as_corners([ax.c2p(200, -6), ax.c2p(200, -12), ax.c2p(600, -12)])
        st3 = VMobject(color=SKY, stroke_width=6).set_points_as_corners([ax.c2p(600, -12), ax.c2p(600, -6), ax.c2p(800, -6)])
        st4 = VMobject(color=SKY, stroke_width=6).set_points_as_corners([ax.c2p(800, -6), ax.c2p(800, 0), ax.c2p(900, 0)])
        v2 = M("-12", size=30, color=SKY).next_to(ax.c2p(400, -12), UP, buff=0.1)
        v3 = M("-6", size=30, color=SKY).next_to(ax.c2p(700, -6), UP, buff=0.1)
        v4 = M("0", size=30, color=SKY).next_to(ax.c2p(850, 0), DOWN, buff=0.12)
        g4 = glow(r4[1][8], GOOD)
        free2 = T("free edge", 26, MUTED).next_to(sec.p(4), RIGHT, buff=0.5).shift(0.15 * UP)
        self.beat("Boom two adds another minus six: minus twelve in the web. Boom three sits at minus two hundred, so it adds plus six: back to minus six. And boom four brings it to zero at the free edge, as it must.",
                  [FadeOut(row1), FadeOut(free)], [FadeIn(r2[0]), Write(r2[1]), Indicate(booms[1], color=EMBER, scale_factor=1.5)],
                  [Create(st2), FadeIn(f23), FadeIn(v2)],
                  [FadeIn(r3[0]), Write(r3[1]), Indicate(booms[2], color=EMBER, scale_factor=1.5)],
                  [Create(st3), FadeIn(f34), FadeIn(v3)],
                  [FadeIn(r4[0]), Write(r4[1]), Indicate(booms[3], color=EMBER, scale_factor=1.5)],
                  [Create(st4), FadeIn(v4), FadeIn(free2), FadeIn(g4)], .4,
                  w=(.05, .14, .1, .16, .1, .14, .11, .2))
        self.wipe()
