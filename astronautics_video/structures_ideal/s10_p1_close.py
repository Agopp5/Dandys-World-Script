"""S10: close the cut with zero twist (BRIEF.md S10)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

# ---- facts (HW P1), every number on screen ----
B1, B2 = 4000, 3556
assert (60 + 50 - 10) * 10 == 1000 and (50 + 40 - 8) * 8 == 656
assert 1000 + 2500 + 500 == B1 and 656 + 2500 + 400 == B2
Ixx = 2 * (B1 + B2) * 150 ** 2
assert np.isclose(Ixx / 1e6, 340.0, atol=0.05)
qb23 = -B2 * 150 / Ixx                      # per unit S_y
qb41 = -B1 * (-150) / Ixx
assert np.isclose(qb23 * 1e3, -1.569, atol=5e-4) and np.isclose(qb41 * 1e3, 1.765, atol=5e-4)
dst = {"top": 500 / 10, "right": 300 / 8, "bottom": 500 / 10, "left": 300 / 10}
assert dst == {"top": 50, "right": 37.5, "bottom": 50, "left": 30}
dtot = sum(dst.values())
assert dtot == 167.5
t23, t41 = qb23 * 37.5, qb41 * 30
assert np.isclose(t23 * 1e3, -58.83, atol=5e-3) and np.isclose(t41 * 1e3, 52.94, atol=5e-3)
assert np.isclose((t23 + t41) * 1e3, -5.89, atol=5e-3)
qs0 = -(t23 + t41) / dtot
assert np.isclose(qs0 * 1e5, 3.52, atol=5e-3)
q23, q41 = qb23 + qs0, qb41 + qs0
assert np.isclose(q23 * 1e3, -1.534, atol=5e-4) and np.isclose(q41 * 1e3, 1.800, atol=5e-4)
assert np.isclose(qs0 * 1e3, 0.035, atol=5e-4)


class S10_P1_Close(VScene):
    budget = 124

    def construct(self):
        sec = hw_box(width=5.6, center=(-3.4, 0.5))
        walls = sec.draw()
        booms = sec.booms({1: B1, 2: B2, 3: B2, 4: B1})
        names = sec.names()

        def wall(a, b):
            return sec.walls_m[(a, b)] if (a, b) in sec.walls_m else sec.walls_m[(b, a)]

        def wl(a, b, tex, d=0.85, color=SKY):
            m = M(tex, size=32, color=color)
            m.move_to(sec.mid(a, b) + d * sec.inward(a, b))
            return m

        f23 = flow(sec, 2, 3, qb23)
        f41 = flow(sec, 4, 1, qb41)
        l12 = wl(1, 2, "0", d=0.55)
        l34 = wl(3, 4, "0", d=0.55)
        l23 = wl(2, 3, "-1.569", d=1.0)
        l41 = wl(4, 1, "+1.765", d=1.0)
        bottom_y = sec.p(3)[1]
        legend = TX(r"flows in units of $10^{-3}\,S_y$ N/mm", size=26, color=MUTED)
        legend.move_to([sec.mid(3, 4)[0], bottom_y - 0.85, 0])

        # ---- right column: the zero-twist condition ----
        X = 3.55
        head = E(r"\oint|\big(|q_b|+|q_{s,0}|\big)|\,\frac{ds}{t}|=|0", size=48).move_to([X, 2.75, 0])
        why = T("no twist at the shear center, one material", size=26, color=MUTED)
        why.next_to(head, DOWN, buff=0.25)

        self.beat("At the shear center the box doesn't twist. With one material, that means the integral of q d s over t around the box is zero.",
                  [Create(walls), FadeIn(booms), FadeIn(names)],
                  [FadeIn(f23), FadeIn(f41),
                   FadeIn(l12), FadeIn(l34), FadeIn(l23), FadeIn(l41), FadeIn(legend)],
                  Write(head), FadeIn(why, shift=UP * .1), .1, w=(.2, .2, .3, .15))

        # ---- beat 2: table of ds/t ----
        rows_spec = [("top", (1, 2), r"\frac{500}{10}", "50"),
                     ("right web", (2, 3), r"\frac{300}{8}", "37.5"),
                     ("bottom", (3, 4), r"\frac{500}{10}", "50"),
                     ("left web", (4, 1), r"\frac{300}{10}", "30")]
        rows = VGroup()
        for name, _, fr, val in rows_spec:
            lab = T(name, size=30, color=INK2)
            eq = E(fr + "|=|" + val, size=40)
            paint(eq, {2: ACCENT})
            rows.add(VGroup(lab, eq))
        for k, r in enumerate(rows):
            r[0].move_to([1.15 + r[0].width / 2, 1.45 - 0.98 * k, 0])
            r[1].move_to([4.2, 1.45 - 0.98 * k, 0], aligned_edge=LEFT)
        total = E(r"\oint|\,\frac{ds}{t}|=|50+37.5+50+30|=|167.5", size=40)
        paint(total, {4: ACCENT})
        fit(total, 6.0, 2)
        total.move_to([X, -2.6, 0])

        steps = []
        for (name, (a, b), _, _), r in zip(rows_spec, rows):
            steps.append([FadeIn(r[0]), Write(r[1]), Indicate(wall(a, b), color=ACCENT, scale_factor=1.0)])
        self.beat("d s over t for each wall: fifty on top, thirty seven and a half on the right, fifty on the bottom, thirty on the left. One hundred sixty seven and a half in total.",
                  *steps, Write(total), Indicate(total[4], color=ACCENT),
                  w=(.17, .17, .17, .17, .22, .1))

        # ---- beat 3: substitute ----
        tot_small = E(r"\oint|\,\frac{ds}{t}|=|167.5", size=40)
        paint(tot_small, {3: ACCENT})
        tot_small.move_to([sec.mid(3, 4)[0], -2.95, 0])
        tot_box = SurroundingRectangle(tot_small, color=HAIR, buff=0.15)

        L1 = E(r"(-1.569\times10^{-3})|(37.5)", size=40)
        paint(L1, {0: SKY, 1: ACCENT})
        L2 = E(r"+\;|(1.765\times10^{-3})|(30)", size=40)
        paint(L2, {1: SKY, 2: ACCENT})
        L3 = E(r"+\;|167.5|\,|q_{s,0}|=|0", size=40)
        paint(L3, {1: ACCENT})
        L1.move_to([X, 1.25, 0])
        L2.move_to([X, 0.25, 0])
        L3.move_to([X, -0.75, 0])
        L2.align_to(L1, LEFT)
        L3.align_to(L1, LEFT)
        note3 = TX(r"top and bottom: $q_b = 0$, they drop out", size=26, color=MUTED)
        note3.next_to(L1, UP, buff=0.3).set_x(X)
        L4 = E(r"-5.89\times10^{-3}|+|167.5|\,|q_{s,0}|=|0", size=40)
        paint(L4, {2: ACCENT})
        L4.move_to([X, -2.0, 0])
        note4 = TX(r"$-58.83\times10^{-3} + 52.94\times10^{-3}$", size=26, color=MUTED)
        note4.next_to(L4, DOWN, buff=0.2)

        self.beat("Only the two webs have basic flow. Minus one point five six nine times thirty seven and a half, plus one point seven six five times thirty, plus one sixty seven and a half q s zero, equals zero.",
                  [FadeOut(rows), FadeOut(why), ReplacementTransform(total, tot_small), Create(tot_box),
                   Indicate(l12, color=MUTED), Indicate(l34, color=MUTED), FadeIn(note3)],
                  [Write(L1), Indicate(l23, scale_factor=1.3)],
                  [Write(L2), Indicate(l41, scale_factor=1.3)],
                  Write(L3), [Write(L4), FadeIn(note4)], .05,
                  w=(.18, .2, .2, .16, .2))

        # ---- beat 4: q_s0 and the totals ----
        res = E(r"q_{s,0}|=|+3.52\times10^{-5}|\,|S_y", size=48)
        paint(res, {2: MINT})
        res.move_to([X, 1.55, 0])
        res_box = SurroundingRectangle(res, color=MINT, buff=0.18)
        tots = VGroup(
            E(r"q_{12}=q_{34}|=|+3.52\times10^{-5}|\,|S_y", size=36),
            E(r"q_{23}|=|-1.534\times10^{-3}|\,|S_y", size=36),
            E(r"q_{41}|=|+1.800\times10^{-3}|\,|S_y", size=36),
        )
        for t in tots:
            paint(t, {0: SKY})
        tots.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        tlab = TX(r"totals: $q = q_b + q_{s,0}$", size=26, color=MUTED)
        card = VGroup(tlab, tots).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        card_p = panel(card)
        fit(card_p, 6.4, 3.4)
        card_p.move_to([X, -1.35, 0])

        cf = cell_flow((sec.p(1) + sec.p(3)) / 2, radius=0.5, color=MINT, ccw=False)
        f12 = flow(sec, 1, 2, qs0)
        f34 = flow(sec, 3, 4, qs0)
        n12 = wl(1, 2, "+0.035", d=0.6)
        n34 = wl(3, 4, "+0.035", d=0.6)
        n23 = wl(2, 3, "-1.534", d=1.0)
        n41 = wl(4, 1, "+1.800", d=1.0)

        self.beat("So q s zero is three point five two times ten to the minus five, S y. A small correction, all the way around.",
                  [FadeOut(VGroup(L1, L2, L3, L4, note3, note4, head))],
                  [Write(res), Create(res_box), FadeIn(glow(res, MINT))],
                  [Create(cf)],
                  [FadeIn(f12), FadeIn(f34), ReplacementTransform(l12, n12), ReplacementTransform(l34, n34),
                   ReplacementTransform(l23, n23), ReplacementTransform(l41, n41), FadeIn(card_p)],
                  .25, w=(.08, .22, .15, .3))
        self.wipe()
