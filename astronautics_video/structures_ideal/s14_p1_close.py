"""S14: close the cut with zero twist (BRIEF.md S14). Rework of old/s10_p1_close.py, slower and larger."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# ---- facts (HW P1), every number on screen ----
B1, B2 = 4000, 3556
assert (60 + 50 - 10) * 10 == 1000 and (50 + 40 - 8) * 8 == 656
assert 1000 + 2500 + 500 == B1 and 656 + 2500 + 400 == B2
Ixx = 2 * (B1 + B2) * 150 ** 2
assert np.isclose(Ixx / 1e6, 340.0, atol=0.05)
qb23 = -B2 * 150 / Ixx                      # per unit S_y
qb34 = qb23 - B2 * (-150) / Ixx
qb41 = -B1 * (-150) / Ixx
assert np.isclose(qb23 * 1e3, -1.569, atol=5e-4) and np.isclose(qb41 * 1e3, 1.765, atol=5e-4)
assert np.isclose(qb34, 0, atol=1e-12)
dst = {"top": 500 / 10, "right": 300 / 8, "bottom": 500 / 10, "left": 300 / 10}
assert dst == {"top": 50, "right": 37.5, "bottom": 50, "left": 30}
dtot = sum(dst.values())
assert dtot == 167.5
t23, t41 = qb23 * 37.5, qb41 * 30
assert np.isclose(t23 * 1e3, -58.83, atol=5e-3) and np.isclose(t41 * 1e3, 52.94, atol=5e-3)
assert np.isclose((t23 + t41) * 1e3, -5.89, atol=5e-3)
qs0 = -(t23 + t41) / dtot
assert np.isclose(qs0 * 1e5, 3.52, atol=5e-3)
assert np.isclose(-5.89e-3 + 167.5 * qs0, 0, atol=1e-5)
q23, q41 = qb23 + qs0, qb41 + qs0
assert np.isclose(q23 * 1e3, -1.534, atol=5e-4) and np.isclose(q41 * 1e3, 1.800, atol=5e-4)
assert np.isclose(qs0 * 1e3, 0.035, atol=5e-4)   # on-picture label, in units of 10^-3 S_y


class S14_P1_Close(VScene):
    budget = 180

    def construct(self):
        sec = hw_box(width=6.3, center=(-3.3, 0.35))
        walls = sec.draw()
        booms = sec.booms({1: B1, 2: B2, 3: B2, 4: B1})
        names = sec.names(size=34)

        def wall(a, b):
            return sec.walls_m[(a, b)] if (a, b) in sec.walls_m else sec.walls_m[(b, a)]

        def wl(a, b, tex, d=0.85, color=SKY):
            m = M(tex, size=40, color=color)
            m.move_to(sec.mid(a, b) + d * sec.inward(a, b))
            return m

        f23 = flow(sec, 2, 3, qb23)
        f41 = flow(sec, 4, 1, qb41)
        l12 = wl(1, 2, "0", d=0.6)
        l34 = wl(3, 4, "0", d=0.6)
        l23 = wl(2, 3, "-1.569", d=1.1)
        l41 = wl(4, 1, "+1.765", d=1.1)
        bottom_y = sec.p(3)[1]
        legend = VGroup(T("flows in units of", size=30, color=MUTED),
                        M(r"10^{-3}\,S_y\ \text{N/mm}", size=38, color=MUTED)).arrange(RIGHT, buff=0.15)
        legend.move_to([sec.mid(3, 4)[0], bottom_y - 0.85, 0])

        # ---- beat 1: zero twist -> the condition ----
        X = 3.7
        tw = E(r"\oint|\frac{q}{G\,t}|\,ds|=|0", size=48).move_to([X, 2.85, 0])
        paint(tw, {1: SKY})
        tw_why = T("no twist: the load acts at the shear center", size=30, color=MUTED)
        fit(tw_why, 6.4, 1)
        tw_why.next_to(tw, DOWN, buff=0.25)
        head = E(r"\oint|\big(|q_b|+|q_{s,0}|\big)|\,\frac{ds}{t}|=|0", size=48).move_to([X, 0.75, 0])
        head_why = T("one material: G drops out", size=30, color=MUTED)
        fit(head_why, 6.4, 1)
        head_why.next_to(head, DOWN, buff=0.25)

        self.beat("Now close the cut with a constant q s zero. Because the load is at the shear centre, the box doesn't twist. With one material, that means the integral of q d s over t, all the way around, is zero.",
                  [Create(walls), FadeIn(booms), FadeIn(names)],
                  [FadeIn(f23), FadeIn(f41), FadeIn(l12), FadeIn(l34), FadeIn(l23), FadeIn(l41), FadeIn(legend)],
                  .06,
                  [Write(tw), FadeIn(tw_why, shift=UP * .1)], .1,
                  [Write(head), FadeIn(head_why, shift=UP * .1)], .16,
                  w=(.12, .12, .22, .22))

        # ---- beats 2-3: the table of ds/t ----
        head_top = head.copy().scale(46 / 48).move_to([X, 3.15, 0])
        th = VGroup(T("wall", size=30, color=MUTED), T("length over thickness", size=30, color=MUTED))
        RX0, RX1 = 0.55, 3.0
        th[0].move_to([RX0 + th[0].width / 2, 2.3, 0])
        th[1].move_to([RX1 + th[1].width / 2, 2.3, 0])
        rows_spec = [("top", (1, 2), r"\frac{500}{10}", "50"),
                     ("right web", (2, 3), r"\frac{300}{8}", "37.5"),
                     ("bottom", (3, 4), r"\frac{500}{10}", "50"),
                     ("left web", (4, 1), r"\frac{300}{10}", "30")]
        rows = VGroup()
        for k, (name, _, fr, val) in enumerate(rows_spec):
            lab = T(name, size=34, color=INK2)
            eq = E(fr + "|=|" + val, size=44)
            paint(eq, {2: ACCENT})
            y = 1.35 - 1.0 * k
            lab.move_to([RX0 + lab.width / 2, y, 0])
            eq.move_to([RX1 + eq.width / 2, y, 0])
            rows.add(VGroup(lab, eq))
        rule = Line([RX0, -2.25, 0], [6.9, -2.25, 0], color=HAIR, stroke_width=2)
        total = E(r"\oint|\,\frac{ds}{t}|=|167.5", size=46)
        paint(total, {3: ACCENT})
        total.move_to([X, -2.95, 0])

        def row_step(k):
            a, b = rows_spec[k][1]
            return [FadeIn(rows[k][0]), Write(rows[k][1]),
                    Indicate(wall(a, b), color=ACCENT, scale_factor=1.0)]

        self.beat("d s over t is each wall's length over its thickness. Top: five hundred over ten, fifty. Right: three hundred over eight, thirty seven and a half.",
                  [FadeOut(VGroup(tw, tw_why, head_why)), ReplacementTransform(head, head_top)],
                  FadeIn(th), .08, row_step(0), .1, row_step(1), .14,
                  w=(.12, .18, .22, .22))

        tglow = glow(total[3], ACCENT)
        self.beat("Bottom: fifty again. Left: three hundred over ten, thirty. In total, one hundred sixty seven and a half.",
                  row_step(2), .08, row_step(3), .08, [Create(rule), Write(total)],
                  [Indicate(total[3], color=ACCENT), FadeIn(tglow)], .14,
                  w=(.18, .22, .2, .1))

        # ---- beat 4: substitute ----
        tot_small = E(r"\oint|\,\frac{ds}{t}|=|167.5", size=44)
        paint(tot_small, {3: ACCENT})
        tot_small.move_to([sec.mid(3, 4)[0], -3.2, 0])
        tot_box = SurroundingRectangle(tot_small, color=HAIR, buff=0.15)

        note3 = T("top and bottom: no basic flow", size=30, color=MUTED)
        note3.move_to([X, 2.3, 0])
        L1 = E(r"(-1.569\times10^{-3})|\,(37.5)", size=46)
        paint(L1, {0: SKY, 1: ACCENT})
        L2 = E(r"+\;|(1.765\times10^{-3})|\,(30)", size=46)
        paint(L2, {1: SKY, 2: ACCENT})
        L3 = E(r"+\;|167.5|\,|q_{s,0}|=|0", size=46)
        paint(L3, {1: ACCENT})
        L1.move_to([X, 1.3, 0])
        L2.move_to([X, 0.15, 0])
        L3.move_to([X, -1.0, 0])
        L2.align_to(L1, LEFT)
        L3.align_to(L1, LEFT)

        self.beat("Only the two webs have basic flow. So: minus one point five six nine times thirty seven and a half, plus one point seven six five times thirty, plus one sixty seven and a half times q s zero, equals zero.",
                  [FadeOut(VGroup(rows, th, rule, tglow)),
                   ReplacementTransform(total, tot_small), Create(tot_box)],
                  [FadeIn(note3), Indicate(l12, color=MUTED), Indicate(l34, color=MUTED)], .05,
                  [Write(L1), Indicate(l23, scale_factor=1.3), Indicate(wall(2, 3), color=ACCENT, scale_factor=1.0)], .04,
                  [Write(L2), Indicate(l41, scale_factor=1.3), Indicate(wall(4, 1), color=ACCENT, scale_factor=1.0)], .04,
                  [Write(L3), Indicate(tot_small[3], color=ACCENT)], .12,
                  w=(.1, .1, .2, .2, .15))

        # ---- beat 5: combine, solve for q_s0 ----
        L4 = E(r"-5.89\times10^{-3}|+|167.5|\,|q_{s,0}|=|0", size=46)
        paint(L4, {0: SKY, 2: ACCENT})
        L4.move_to([X, 1.3, 0])
        note4 = M(r"(-58.83 + 52.94)\times10^{-3}", size=36, color=MUTED)
        note4.next_to(L4, DOWN, buff=0.25)
        res = E(r"q_{s,0}|=|3.52\times10^{-5}|\,|S_y", size=50)
        paint(res, {2: MINT})
        res.move_to([X, -1.0, 0])
        res_box = SurroundingRectangle(res, color=MINT, buff=0.2)
        rglow = glow(res, MINT)
        cen = (sec.p(1) + sec.p(3)) / 2
        cf = cell_flow(cen, radius=0.65, color=MINT, ccw=False)
        cfl = M(r"q_{s,0}", size=40, color=MINT).move_to(cen)
        res_why = T("a small correction, all the way around", size=30, color=MUTED)
        res_why.next_to(res_box, DOWN, buff=0.3)

        self.beat("The first two terms add up to minus five point eight nine times ten to the minus three. So q s zero is three point five two times ten to the minus five, S y. A small correction, all the way around.",
                  [FadeOut(VGroup(note3, L3)), ReplacementTransform(VGroup(L1, L2), L4)],
                  FadeIn(note4), .1,
                  [Write(res), Create(res_box), FadeIn(rglow)], .1,
                  [Create(cf), FadeIn(cfl), FadeIn(res_why)], .16,
                  w=(.2, .08, .2, .16))

        # ---- beat 6: the final shear flows ----
        res_top = VGroup(rglow, res, res_box)
        hdr = E(r"q|=|q_b|+|q_{s,0}", size=46)
        tots = VGroup(
            E(r"q_{12}=q_{34}|=|3.52\times10^{-5}|\,|S_y", size=44),
            E(r"q_{23}|=|-1.534\times10^{-3}|\,|S_y", size=44),
            E(r"q_{41}|=|+1.800\times10^{-3}|\,|S_y", size=44),
        )
        for t in tots:
            paint(t, {0: SKY})
        tots.arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        hdr.move_to([X, 1.55, 0])
        tots.next_to(hdr, DOWN, buff=0.45).set_x(X)

        f12 = flow(sec, 1, 2, qs0)
        f34 = flow(sec, 3, 4, qs0)
        n12 = wl(1, 2, "+0.035", d=0.6)
        n34 = wl(3, 4, "+0.035", d=0.6)
        n23 = wl(2, 3, "-1.534", d=1.1)
        n41 = wl(4, 1, "+1.800", d=1.1)

        self.beat("Add it to every wall to get the final shear flows.",
                  [FadeOut(VGroup(L4, note4, res_why, head_top)), res_top.animate.move_to([X, 2.9, 0])],
                  Write(hdr),
                  [FadeIn(f12), FadeIn(f34), ReplacementTransform(l12, n12), ReplacementTransform(l34, n34),
                   ReplacementTransform(l23, n23), ReplacementTransform(l41, n41),
                   FadeIn(tots, lag_ratio=0.3)],
                  .2, w=(.15, .15, .4))
        self.wait(1.0)
        self.wipe()
