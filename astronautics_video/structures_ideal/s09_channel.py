"""S09: the channel, step by step (BRIEF.md S09). Rework of old/s06_channel.py."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# facts: the slide's channel. Four booms B = 300 mm^2 at y = +-200 mm, S_y = 4.8 kN through the shear centre.
B, H, S_Y = 300.0, 200.0, 4.8e3
IXX = 4 * B * H ** 2
assert np.isclose(IXX, 48e6)
K = S_Y / IXX
assert np.isclose(K, 1e-4)
YS = {1: H, 2: H, 3: -H, 4: -H}
JUMP = {r: -K * B * YS[r] for r in YS}       # q_after - q_before = -(S_y/I_xx) B_r y_r
assert np.allclose([JUMP[1], JUMP[2], JUMP[3], JUMP[4]], [-6, -6, 6, 6])
Q = [0.0]
for r in (1, 2, 3, 4):
    Q.append(Q[-1] + JUMP[r])
q12, q23, q34, q_end = Q[1:]
assert np.allclose([q12, q23, q34, q_end], [-6, -12, -6, 0])
# shear centre (where the S_y arrow is drawn): flange couple balances S_y e about the web
XI = (-q12) * 200 * 400 / S_Y
assert np.isclose(XI, 100.0)
S_POS = [0, 200, 600, 800]                   # arc length s (mm) at booms 1..4: flange 200, web 400, flange 200
LX = -1.1                                    # left edge of the algebra column


class S09_Channel(VScene):
    budget = 174

    def construct(self):
        # ---------- the staircase plot (built at its final spot, shown big first) ----------
        ax = axes((-200, 900, 100), (-14, 2, 2), width=6.8, height=2.3, xlabel="s", ylabel="q")
        ax.move_to([3.15, -1.95, 0])
        bl = VGroup(*[DashedLine(ax.c2p(s, 2), ax.c2p(s, -14), color=EMBER, stroke_width=2, dash_length=0.08)
                      for s in S_POS])
        bnum = VGroup(*[T(str(i + 1), 34, EMBER).next_to(bl[i], DOWN, buff=0.06) for i in range(4)])
        plot = VGroup(ax, bl, bnum)
        home = plot.get_center()
        plot.scale(1.6).move_to([0, 0.2, 0])

        lvl = [-4, -9, -3]                           # shape only: arbitrary step heights
        flats = VGroup(*[Line(ax.c2p(a, v), ax.c2p(b, v), color=INK2, stroke_width=7)
                         for a, b, v in [(-100, 0, 0), (0, 200, lvl[0]), (200, 600, lvl[1]),
                                         (600, 800, lvl[2]), (800, 900, 0)]])
        tops = [0] + lvl
        bots = lvl + [0]
        jumps = VGroup(*[Line(ax.c2p(s, tops[i]), ax.c2p(s, bots[i]), color=EMBER, stroke_width=7)
                         for i, s in enumerate(S_POS)])
        n_flat = T("flat between booms", 30, INK2).next_to(bnum, DOWN, buff=0.3).align_to(ax, LEFT).shift(0.6 * RIGHT)
        n_jump = T("jumps at the booms", 30, EMBER).next_to(n_flat, RIGHT, buff=0.8)
        n_shape = T("shape only", 30, MUTED).next_to(ax, UP, buff=0.25).align_to(ax, RIGHT)

        self.beat("Between booms the skin carries no direct stress, so the shear flow can't change there. It's constant, and it only jumps when it crosses a boom.",
                  [Create(ax), FadeIn(bl), FadeIn(bnum), FadeIn(n_shape)], .08,
                  [Create(flats, lag_ratio=0.3), FadeIn(n_flat)], .1,
                  [Create(jumps, lag_ratio=0.3), FadeIn(n_jump)], .2,
                  w=(.22, .2, .2))

        # ---------- beat 2: the channel ----------
        sec = channel(width=2.6, center=(-3.6, -0.2))
        walls = sec.draw()
        booms = sec.booms({n: B for n in (1, 2, 3, 4)})
        names = sec.names(size=34)
        mm = (sec.p(1)[0] - sec.p(2)[0]) / 200.0
        y0 = (sec.p(2)[1] + sec.p(3)[1]) / 2
        xs = sec.p(2)[0] - XI * mm
        na = DashedLine([xs - 0.3, y0, 0], [sec.p(1)[0] + 0.5, y0, 0], color=MUTED, stroke_width=2.5, dash_length=0.12)
        na_lab = M("x", size=36, color=MUTED).next_to(na, RIGHT, buff=0.1)
        sx = sec.p(2)[0] + 1.45
        sp_top = DoubleArrow([sx, y0, 0], [sx, sec.p(2)[1], 0], buff=0, color=MUTED, stroke_width=3,
                             tip_length=0.18, max_tip_length_to_length_ratio=0.1)
        sp_bot = DoubleArrow([sx, y0, 0], [sx, sec.p(3)[1], 0], buff=0, color=MUTED, stroke_width=3,
                             tip_length=0.18, max_tip_length_to_length_ratio=0.1)
        yl_top = E(r"y|=|200", size=36).next_to(sp_top, RIGHT, buff=0.12)
        yl_bot = E(r"y|=|-200", size=36).next_to(sp_bot, RIGHT, buff=0.12)
        b_lab = E(r"B|=|300\ \text{mm}^2", size=44).move_to([sec.mid(3, 4)[0], -3.72, 0])

        self.beat("Here's the channel from your slides: four booms of three hundred square millimeters, two hundred millimeters above and below the axis.",
                  [FadeOut(flats), FadeOut(jumps), FadeOut(n_flat), FadeOut(n_jump), FadeOut(n_shape),
                   plot.animate.scale(1 / 1.6).move_to(home)],
                  Create(walls), [FadeIn(booms, scale=1.6), FadeIn(names)], [FadeIn(b_lab)], .08,
                  [Create(na), FadeIn(na_lab)], [GrowFromCenter(sp_top), FadeIn(yl_top)],
                  [GrowFromCenter(sp_bot), FadeIn(yl_bot)], .15,
                  w=(.12, .1, .14, .1, .1, .1, .11))

        # ---------- beat 3: I_xx and S_y / I_xx ----------
        ix = E(r"I_{xx}|=|4\,|(300)|(200)^2", size=44)
        paint(ix, {3: EMBER})
        ix.move_to([0, 3.4, 0]).align_to([LX, 0, 0], LEFT)
        ix2 = E(r"=|48\times 10^6\ \text{mm}^4", size=44)
        ix2.next_to(ix, DOWN, buff=0.3)
        ix2.shift((ix[1].get_x() - ix2[0].get_x()) * RIGHT)
        ix_note = T("four booms, each 200 mm from the axis", 30, MUTED).next_to(ix2, DOWN, buff=0.2).align_to(ix, LEFT)
        k = E(r"S_y|/|I_{xx}|=|4800|/|48\times 10^6", size=44)
        paint(k, {4: ROSE})
        k.next_to(ix_note, DOWN, buff=0.55).align_to(ix, LEFT)
        k2 = E(r"=|10^{-4}\ \text{N/mm}^4", size=44)
        k2.next_to(k, DOWN, buff=0.3)
        k2.shift((k[3].get_x() - k2[0].get_x()) * RIGHT)
        g_k = glow(k2[1], GOLD)
        sy_arr = Arrow([xs, y0 - 1.1, 0], [xs, y0 + 1.1, 0], buff=0, color=ROSE, stroke_width=7)
        sy_lab = E(r"S_y", size=44).next_to(sy_arr, UP, buff=0.1)
        sy_val = M(r"4.8\ \text{kN}", size=36, color=ROSE).next_to(sy_arr, DOWN, buff=0.12)
        sc_dot = Dot([xs, y0, 0], radius=0.07, color=ROSE)

        self.beat("I x x is four times three hundred times two hundred squared. That's forty eight million. So S y over I x x is forty eight hundred over forty eight million: ten to the minus four.",
                  [Write(ix[:3])], [Write(ix[3:5]), Indicate(booms, color=EMBER, scale_factor=1.3)], .06,
                  [Write(ix2), FadeIn(ix_note)], .1,
                  [GrowArrow(sy_arr), FadeIn(sy_lab), FadeIn(sy_val), FadeIn(sc_dot)], [Write(k[:3])],
                  [Write(k[3:])], [Write(k2), FadeIn(g_k)], .16,
                  w=(.08, .14, .12, .1, .06, .1, .08))

        # ---------- beat 4: fold, the jump rule, boom 1 ----------
        kb_eq = E(r"S_y|/|I_{xx}|=|10^{-4}", size=44)
        kbox = panel(kb_eq, color=HAIR)
        kbox.move_to([0, 3.35, 0]).align_to([LX, 0, 0], LEFT)
        kbox[1].set_z_index(3)
        rule = E(r"q_2|-|q_1|=|-|S_y|/|I_{xx}|\;B_r|\;y_r", size=44)
        paint(rule, {7: EMBER})
        rule.move_to([0, 2.35, 0]).align_to([LX, 0, 0], LEFT)
        rule_note = T("the jump at each boom (last scene)", 30, MUTED).next_to(rule, DOWN, buff=0.15).align_to(rule, LEFT)
        l1 = E(r"q_{12}|=|0|-|10^{-4}|(300)|(200)|=|-6\ \text{N/mm}", size=44)
        paint(l1, {0: SKY, 2: SKY, 5: EMBER, 8: SKY})
        fit(l1, 7.9, 1)
        l1.move_to([0, 1.05, 0]).align_to([LX, 0, 0], LEFT)
        free = T("free edge", 30, MUTED).next_to(names[0], UP, buff=0.12)
        f12 = flow(sec, 1, 2, q12, label="-6", size=34)
        st0 = Line(ax.c2p(-100, 0), ax.c2p(0, 0), color=SKY, stroke_width=7)
        st1 = VMobject(color=SKY, stroke_width=7).set_points_as_corners(
            [ax.c2p(0, 0), ax.c2p(0, -6), ax.c2p(200, -6)])
        v1 = M("-6", size=34, color=SKY).next_to(ax.c2p(100, -6), UP, buff=0.1)

        self.beat("Start at the free edge, where the shear flow is zero. Crossing boom one: zero, minus ten to the minus four, times three hundred, times two hundred. That's minus six newtons per millimeter.",
                  [FadeOut(ix), FadeOut(ix2), FadeOut(ix_note), FadeOut(g_k),
                   ReplacementTransform(VGroup(k, k2), kb_eq), FadeIn(kbox[0])],
                  [FadeIn(rule), FadeIn(rule_note)],
                  [FadeIn(free), Flash(sec.p(1), color=SKY), Create(st0)], .08,
                  [Write(l1[:3]), Indicate(booms[0], color=EMBER, scale_factor=1.6)],
                  [Write(l1[3:7])], .06,
                  [Write(l1[7:]), FadeIn(f12), Create(st1), FadeIn(v1)], .16,
                  w=(.08, .1, .12, .1, .2, .1))

        # ---------- beat 5: checkpoint cue ----------
        self.beat("Your turn. Pause here and do checkpoint three point one in your guide.",
                  Circumscribe(VGroup(booms[1], booms[2], booms[3]), color=EMBER), .5)
        self.checkpoint("3.1", "Carry the shear flow past booms 2, 3 and 4")

        # ---------- beat 6: boom 2 ----------
        def row(tex):
            e = E(tex, size=44)
            paint(e, {0: SKY, 2: SKY, 4: EMBER, 6: SKY})
            return e
        r12 = row(r"q_{12}|=|0|-|6|=|-6")
        r23 = row(r"q_{23}|=|-6|-|6|=|-12")
        r34 = row(r"q_{34}|=|-12|+|6|=|-6")
        r4 = row(r"q_{\text{end}}|=|-6|+|6|=|0")
        rows = VGroup(r12, r23, r34, r4).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        xe = max(r[1].get_x() for r in rows)
        for r in rows:                               # line the equals signs up
            r.shift((xe - r[1].get_x()) * RIGHT)
        rows.move_to([0, 0.95, 0]).align_to([LX, 0, 0], LEFT)
        nx = max(r.get_right()[0] for r in rows) + 0.5
        notes = [T("boom 1", 30, EMBER), T("boom 2, same y", 30, EMBER),
                 T("boom 3, below axis", 30, EMBER), T("boom 4", 30, EMBER)]
        for n, r in zip(notes, rows):
            n.move_to([0, r.get_y(), 0]).align_to([nx, 0, 0], LEFT)
        f23 = VGroup(flow(sec, 2, 3, q23))
        f23.add(M("-12", size=34, color=SKY).next_to(f23[0], RIGHT, buff=0.12).set_y(y0 + 0.7))
        st2 = VMobject(color=SKY, stroke_width=7).set_points_as_corners(
            [ax.c2p(200, -6), ax.c2p(200, -12), ax.c2p(600, -12)])
        v2 = M("-12", size=34, color=SKY).next_to(ax.c2p(400, -12), UP, buff=0.1)
        rule_up = VGroup(rule, rule_note)

        self.beat("Boom two adds another minus six. That's minus twelve in the web.",
                  [FadeOut(kbox), FadeOut(kb_eq), FadeOut(free), rule_up.animate.shift(1.0 * UP),
                   *morph(l1, r12, [(0, 0), (1, 1), (2, 2), (3, 3), (5, 4), (7, 5), (8, 6)]), FadeIn(notes[0])],
                  .06, [Indicate(booms[1], color=EMBER, scale_factor=1.6), Write(r23[:5]), FadeIn(notes[1])], .08,
                  [Write(r23[5:]), FadeIn(f23), Create(st2), FadeIn(v2)], .18,
                  w=(.2, .26, .22))

        # ---------- beat 7: booms 3 and 4; the staircase completes ----------
        f34 = flow(sec, 3, 4, q34, label="-6", size=34)
        st3 = VMobject(color=SKY, stroke_width=7).set_points_as_corners(
            [ax.c2p(600, -12), ax.c2p(600, -6), ax.c2p(800, -6)])
        st4 = VMobject(color=SKY, stroke_width=7).set_points_as_corners(
            [ax.c2p(800, -6), ax.c2p(800, 0), ax.c2p(900, 0)])
        v3 = M("-6", size=34, color=SKY).next_to(ax.c2p(700, -6), UP, buff=0.1)
        v4 = M("0", size=34, color=SKY).next_to(ax.c2p(850, 0), UP, buff=0.1)
        g4 = glow(r4[6], GOOD)

        self.beat("Boom three is two hundred below the axis, so its jump is plus six. Back to minus six. And boom four brings it to zero at the free edge, just as it must.",
                  [Indicate(booms[2], color=EMBER, scale_factor=1.6), Indicate(yl_bot), FadeIn(notes[2])],
                  [Write(r34[:5])], [Write(r34[5:]), FadeIn(f34), Create(st3), FadeIn(v3)], .08,
                  [Indicate(booms[3], color=EMBER, scale_factor=1.6), Write(r4[:5]), FadeIn(notes[3])],
                  [Write(r4[5:]), Create(st4), FadeIn(v4), Flash(sec.p(4), color=SKY)],
                  [FadeIn(g4), Indicate(VGroup(st0, st1, st2, st3, st4), color=SKY, scale_factor=1.03)], .2,
                  w=(.12, .1, .14, .14, .12, .1))
        self.wipe()
