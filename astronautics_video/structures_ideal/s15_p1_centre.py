"""S15: where the shear centre is (BRIEF.md S15). Rework of old/s11_p1_centre.py, slower and larger."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# facts (per unit S_y): HW P1 final flows
Ixx = 2 * (4000 + 3556) * 150 ** 2
assert np.isclose(Ixx, 340.0e6, rtol=1e-3)
qb23 = -3556 * 150 / Ixx
qb41 = 4000 * 150 / Ixx
qs0 = -(qb23 * 37.5 + qb41 * 30) / 167.5
assert np.isclose(qs0, 3.52e-5, rtol=3e-3)
q23 = qb23 + qs0
q41 = qb41 + qs0
assert np.isclose(q23, -1.534e-3, rtol=2e-3) and np.isclose(q41, 1.800e-3, rtol=2e-3)
FR, FL = -q23 * 300, q41 * 300
assert np.isclose(1.534e-3 * 300, 0.460, atol=6e-4) and np.isclose(1.800e-3 * 300, 0.540, atol=6e-4)
assert np.isclose(FR, 0.460, atol=6e-4) and np.isclose(FL, 0.540, atol=6e-4)
assert np.isclose(0.460 + 0.540, 1.000) and np.isclose(FR + FL, 1.000, atol=1e-6)
MR = 0.460 * 500
assert np.isclose(MR, 230.0) and np.isclose(FR * 500, 230.0, atol=0.2)
Msk = 3.52e-5 * 500 * 300
assert np.isclose(Msk, 5.28, atol=0.01) and np.isclose(qs0 * 500 * 300, 5.27, atol=0.01)
xi = 230.04 - 5.27
assert np.isclose(xi, 224.8, atol=0.05) and np.isclose(FR * 500, 230.04, atol=0.005) and np.isclose(FR * 500 - qs0 * 500 * 300, 224.8, atol=0.1)
assert 224.8 < 250 and np.isclose(500 / 2, 250)


class S15_P1_Centre(VScene):
    budget = 163

    def construct(self):
        self.section("Where the shear centre is")
        sec = hw_box(width=6.3, center=(-3.15, -0.3))
        walls = sec.draw()
        booms = sec.booms({1: 4000, 2: 3556, 3: 3556, 4: 4000})
        names = sec.names(size=34)
        box = VGroup(walls, booms, names)
        self.add(box)

        # final flows: both webs up (q_23 < 0 so the arrow on 2->3 points up)
        fRa = flow(sec, 2, 3, -1.534)
        fLa = flow(sec, 4, 1, 1.800)
        qR = M(r"1.534\times10^{-3}\,S_y", size=34, color=SKY).next_to(fRa, LEFT, buff=0.15).shift(DOWN * 0.7)
        qL = M(r"1.800\times10^{-3}\,S_y", size=34, color=SKY).next_to(fLa, RIGHT, buff=0.15).shift(UP * 1.3)
        FRl = M(r"0.460\,S_y", size=38, color=ROSE).move_to(qR).align_to(qR, RIGHT)
        FLl = M(r"0.540\,S_y", size=38, color=ROSE).move_to(qL).align_to(qL, LEFT)
        xh = sec.p(1)[0] + 0.55 * (sec.p(2)[0] - sec.p(1)[0])
        hspan = span([xh, sec.p(3)[1] + 0.1, 0], [xh, sec.p(2)[1] - 0.1, 0], "", side=LEFT)
        hspan = VGroup(hspan, M(r"300\text{ mm}", size=36, color=INK).next_to([xh, -0.3, 0], LEFT, buff=0.15))

        X0 = 3.7   # centre of the algebra column

        # ---------------- beat 1: flow times height
        n1 = T("force = flow x web height", size=30, color=MUTED)
        l1 = E(r"F_R|=|(1.534\times10^{-3}\,|S_y|)(300)", size=44)
        l2 = E(r"F_L|=|(1.800\times10^{-3}\,|S_y|)(300)", size=44)
        l1b = E(r"=|0.460\,|S_y", size=44)
        l2b = E(r"=|0.540\,|S_y", size=44)
        l3 = E(r"F_R+F_L|=|1.000\,|S_y", size=48)
        g1 = VGroup(n1, l1, l1b, l2, l2b, l3).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        for m in (l1b, l2b):
            m.shift(RIGHT * 1.2)
        l3.shift(DOWN * 0.15)
        fit(g1, 6.2, 6.6)
        g1.move_to([X0, -0.35, 0])
        self.beat("Both webs now carry shear flow upward. Multiply by their height, three hundred millimeters, to get forces.",
                  [GrowFromCenter(fRa), GrowFromCenter(fLa)], [FadeIn(qR), FadeIn(qL)], .1,
                  [FadeIn(hspan), FadeIn(n1)], [Write(l1), Indicate(qR)], [Write(l2), Indicate(qL)], .15,
                  w=(.13, .12, .15, .17, .17))

        # ---------------- beat 2: the forces, and the check
        chk = T("check: equals the load", size=30, color=GOOD).next_to(l3, DOWN, buff=0.25, aligned_edge=LEFT)
        gl3 = glow(l3, GOOD)
        self.beat("The right web carries zero point four six S y, and the left web zero point five four S y. Together, exactly S y. Good, that's our check.",
                  [FadeIn(l1b), ReplacementTransform(qR, FRl)], .08,
                  [FadeIn(l2b), ReplacementTransform(qL, FLl)], .1,
                  Write(l3), [FadeIn(chk), FadeIn(gl3)], .2,
                  w=(.2, .2, .16, .1))

        # ---------------- beat 3: moment of the right web about the left web
        pivot = Dot(sec.mid(4, 1), radius=0.11, color=ACCENT).set_z_index(6)
        arm = span(sec.p(4) + DOWN * 0.25, sec.p(3) + DOWN * 0.25, "", side=DOWN)
        arm = VGroup(arm, M(r"500\text{ mm}", size=36, color=INK).next_to(arm, DOWN, buff=0.12))
        arc = Arc(radius=0.75, start_angle=-PI * 0.4, angle=PI * 0.8, color=INK, stroke_width=5)
        arc.move_arc_center_to(sec.mid(4, 1))
        arc.add_tip(tip_length=0.22)
        m1 = E(r"M_R|=|0.460\,|S_y|\times 500", size=44)
        m1b = E(r"=|230.0\,|S_y", size=44)
        nm1 = T("counterclockwise", size=30, color=MUTED)
        g2 = VGroup(m1, m1b, nm1).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        m1b.shift(RIGHT * 1.2)
        fit(g2, 6.2, 3)
        g2.move_to([X0, 1.65, 0]).align_to(g1, LEFT)
        self.beat("Now take moments about the left web. The right web's force, zero point four six S y, is five hundred millimeters away. That's two hundred thirty S y.",
                  [FadeOut(g1), FadeOut(chk), FadeOut(gl3), FadeOut(hspan)],
                  [FadeIn(pivot, scale=2), Create(arc)], .08,
                  [FadeIn(arm), Indicate(FRl)], Write(m1), .08, FadeIn(m1b), FadeIn(nm1), .15,
                  w=(.1, .15, .16, .17, .1, .06))

        # ---------------- beat 4: the skins' small couple (top flows right, bottom flows left: clockwise)
        top = flow(sec, 1, 2, 0.6, color=SKY)
        bot = flow(sec, 3, 4, 0.6, color=SKY)
        topl = M(r"3.52\times10^{-5}\,S_y", size=34, color=SKY).next_to(sec.walls_m[(1, 2)], UP, buff=0.15)
        botl = M(r"3.52\times10^{-5}\,S_y", size=34, color=SKY).next_to(bot, UP, buff=0.12)
        r2 = E(r"M_R|=|230.0\,|S_y", size=44)
        res2 = panel(VGroup(r2, T("counterclockwise", size=30, color=MUTED)).arrange(DOWN, buff=0.15), color=HAIR)
        res2.move_to([X0, 2.2, 0])
        s0 = E(r"F_{sk}|=|3.52\times10^{-5}\,|S_y|\times 500", size=44)
        n0 = T("force in each skin; 300 mm apart", size=30, color=MUTED)
        s1 = E(r"M_{sk}|=|F_{sk}\times 300", size=44)
        s1b = E(r"=|5.27\,|S_y", size=44)
        ns1 = T("a couple: clockwise, the other way", size=30, color=MUTED)
        g3 = VGroup(s0, n0, s1, s1b, ns1).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        s1b.shift(RIGHT * 1.2)
        fit(g3, 6.2, 4.6)
        g3.next_to(res2, DOWN, buff=0.35).set_x(X0)
        self.beat("The small flows in the top and bottom skins point opposite ways, so they make a small couple, the other way: about five point three S y.",
                  [ReplacementTransform(g2, res2), GrowFromCenter(top), GrowFromCenter(bot)], [FadeIn(topl), FadeIn(botl)], .06,
                  [Write(s0), FadeIn(n0)], Write(s1), FadeIn(s1b), FadeIn(ns1), .12,
                  w=(.17, .1, .2, .14, .1, .08))

        # ---------------- beat 5: xi
        e1 = E(r"S_y|\,|\xi|=|230.04\,|S_y|-|5.27\,|S_y", size=48)
        ne1 = T("unrounded: 0.46007 x 500", size=30, color=MUTED)
        e2 = E(r"\xi|=|224.8\text{ mm}", size=60)
        ne2 = T("from the left web", size=30, color=MUTED)
        g4 = VGroup(e1, ne1, e2, ne2).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        e2.shift(RIGHT * 0.6)
        ne2.align_to(e2, LEFT)
        fit(g4, 6.2, 4)
        g4.move_to([X0, 1.2, 0])
        xs = sec.p(4)[0] + (sec.p(3)[0] - sec.p(4)[0]) * 224.8 / 500
        xm = sec.p(4)[0] + (sec.p(3)[0] - sec.p(4)[0]) * 0.5
        ytop, ybot = sec.p(1)[1] + 0.35, sec.p(4)[1] - 0.8
        sc = DashedLine([xs, ybot, 0], [xs, ytop, 0], color=ROSE, stroke_width=5, dash_length=0.14)
        sy = Arrow([xs, -1.1, 0], [xs, 0.5, 0], buff=0, color=ROSE, stroke_width=7)
        syl = M(r"S_y", size=44, color=ROSE).next_to(sy, LEFT, buff=0.12).shift(DOWN * 0.3)
        xi_span = span([sec.p(4)[0], ybot + 0.15, 0], [xs, ybot + 0.15, 0], "", side=DOWN)
        xil = M(r"\xi", size=48, color=ROSE).next_to(xi_span, LEFT, buff=0.2).shift(RIGHT * 0)
        xil.move_to([(sec.p(4)[0] + xs) / 2, ybot - 0.35, 0])
        self.beat("So S y times xi equals two thirty point zero four, minus five point two seven. xi is two hundred twenty four point eight millimeters from the left web. That's the answer.",
                  [FadeOut(res2), FadeOut(g3), FadeOut(arc), FadeOut(arm), FadeOut(topl), FadeOut(botl), FadeOut(pivot)],
                  [Write(e1), FadeIn(ne1)], .1, Write(e2), [FadeIn(glow(e2, ROSE)), FadeIn(ne2), Create(sc), GrowArrow(sy), FadeIn(syl)],
                  [FadeIn(xi_span), FadeIn(xil)], .18,
                  w=(.08, .2, .14, .2, .12))

        # ---------------- beat 6: left of the middle
        mid = DashedLine([xm, ybot, 0], [xm, ytop, 0], color=MUTED, stroke_width=3, dash_length=0.1)
        midl = M(r"\text{middle: }250\text{ mm}", size=34, color=MUTED).next_to(mid, UP, buff=0.1).shift(RIGHT * 0.9)
        ne = VGroup(T("the left booms are heavier:", size=30, color=MUTED),
                    E(r"B_1|=|4000\;>\;3556|=|B_2", size=44)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        ne.next_to(g4, DOWN, buff=0.6).align_to(g4, LEFT)
        self.beat("It sits left of the middle, because the left booms are heavier and carry more of the load.",
                  [Create(mid), FadeIn(midl)], .08, FadeIn(ne),
                  Indicate(VGroup(sec.boom_m[1], sec.boom_m[4]), color=EMBER, scale_factor=1.7),
                  Indicate(FLl), .15,
                  w=(.22, .17, .26, .14))

        # ---------------- beat 7: checkpoint cue
        self.beat("Your turn. Pause here and do checkpoint four point one: the same steps for the practice box.",
                  Circumscribe(e2, color=ROSE), .5)
        self.checkpoint("4.1", "Practice box: booms, then the shear centre")
        self.wipe()
