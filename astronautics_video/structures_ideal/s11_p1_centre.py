"""S11: where the shear centre is (BRIEF.md S11)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

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
assert np.isclose(FR, 0.460, atol=6e-4) and np.isclose(FL, 0.540, atol=6e-4)
assert np.isclose(FR + FL, 1.000, atol=1e-6)
MR = 0.460 * 500
assert np.isclose(MR, 230.0) and np.isclose(FR * 500, 230.0, atol=0.2)
Msk = 3.52e-5 * 500 * 300
assert np.isclose(Msk, 5.28, atol=0.01) and np.isclose(qs0 * 500 * 300, 5.27, atol=0.01)
xi = 230.0 - 5.27
assert np.isclose(xi, 224.8, atol=0.1) and xi < 250


class S11_P1_Centre(VScene):
    budget = 132

    def construct(self):
        self.section("Where the shear centre is")
        sec = hw_box(width=6.8, center=(-3.15, -0.35))
        walls = sec.draw()
        booms = sec.booms({1: 4000, 2: 3556, 3: 3556, 4: 4000})
        names = sec.names()
        box = VGroup(walls, booms, names)
        self.add(box)

        # final flows: both webs up (q_23 < 0 so the arrow on 2->3 points up)
        fRa = flow(sec, 2, 3, -1.534)
        fLa = flow(sec, 4, 1, 1.800)
        fR = VGroup(fRa, M(r"0.460\,S_y", size=34, color=ROSE).next_to(fRa, LEFT, buff=0.15))
        fL = VGroup(fLa, M(r"0.540\,S_y", size=34, color=ROSE).next_to(fLa, RIGHT, buff=0.15).shift(UP * 1.0))

        X0 = 3.95   # centre of the algebra column

        # ---------------- beat 1: web forces
        l1 = E(r"F_R|=|1.534\times10^{-3}\,|S_y|\cdot 300", size=40)
        l1b = E(r"=|0.460\,|S_y", size=44)
        l2 = E(r"F_L|=|1.800\times10^{-3}\,|S_y|\cdot 300", size=40)
        l2b = E(r"=|0.540\,|S_y", size=44)
        l3 = E(r"F_R+F_L|=|1.000\,|S_y", size=44)
        n1 = T("flow  x  web height (300 mm)", size=26, color=MUTED)
        g1 = VGroup(n1, l1, l1b, l2, l2b, l3).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        for m in (l1b, l2b):
            m.shift(RIGHT * 1.0)
        fit(g1, 5.6, 5.6)
        g1.move_to([X0, -0.1, 0])
        chk = T("check ✓", size=30, color=GOOD).next_to(l3, DOWN, buff=0.25, aligned_edge=LEFT)
        gl3 = glow(l3, GOOD)
        self.beat("Both webs now carry shear flow upward. Times three hundred millimeters, the right web carries zero point four six S y, the left web zero point five four. Together, exactly S y.",
                  [GrowFromCenter(fR), GrowFromCenter(fL)], FadeIn(n1),
                  [Write(l1), Indicate(fR)], FadeIn(l1b),
                  [Write(l2), Indicate(fL)], FadeIn(l2b),
                  Write(l3), [FadeIn(chk), FadeIn(gl3)],
                  w=(.13, .07, .2, .09, .2, .09, .13, .09))

        # fold beat 1 into one boxed result
        r1 = E(r"F_R=0.460\,|S_y|,\quad F_L=0.540\,|S_y", size=40)
        res1 = panel(r1, color=HAIR)
        res1.move_to([X0, 2.25, 0])

        # ---------------- beat 2: moment of the right web about the left web
        pivot = Dot(sec.mid(4, 1), radius=0.1, color=ACCENT).set_z_index(6)
        arm = span(sec.p(4) + DOWN * 0.15, sec.p(3) + DOWN * 0.15, r"500\text{ mm}", side=DOWN)
        arc = Arc(radius=0.75, start_angle=-PI * 0.4, angle=PI * 0.8, color=INK, stroke_width=5).move_arc_center_to(sec.mid(4, 1))
        arc.add_tip(tip_length=0.22)
        m1 = E(r"M_R|=|0.460\,|S_y|\times 500", size=44)
        m1b = E(r"=|230.0\,|S_y", size=44)
        nm1 = T("counterclockwise", size=26, color=MUTED)
        g2 = VGroup(m1, m1b, nm1).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        m1b.shift(RIGHT * 1.0)
        g2.move_to([X0, 0.55, 0])
        self.beat("Take moments about the left web. The right web's force, zero point four six S y, acts five hundred millimeters away: two hundred thirty S y.",
                  [FadeOut(g1), FadeOut(chk), FadeOut(gl3), FadeIn(res1)],
                  [FadeIn(pivot, scale=2), Create(arc)],
                  [FadeIn(arm), Indicate(fR)], Write(m1), FadeIn(m1b), FadeIn(nm1),
                  w=(.15, .18, .18, .24, .15, .1))

        # ---------------- beat 3: the skins' small couple
        top = flow(sec, 1, 2, 0.6, color=SKY)
        topl = M(r"3.52\times10^{-5}\,S_y", size=32, color=SKY).next_to(top, DOWN, buff=0.12)
        bot = flow(sec, 3, 4, 0.6, color=SKY)
        s1 = E(r"M_{sk}|=|3.52\times10^{-5}\,|S_y|\,(500)(300)", size=40)
        s1b = E(r"=|5.27\,|S_y", size=44)
        ns1 = T("a couple: clockwise, the other way", size=26, color=MUTED)
        g3 = VGroup(s1, s1b, ns1).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        s1b.shift(RIGHT * 1.0)
        fit(g3, 5.6, 3)
        g3.next_to(g2, DOWN, buff=0.55).set_x(X0)
        self.beat("The small flows in the top and bottom skins form a couple the other way, about five point three S y.",
                  [GrowFromCenter(top), GrowFromCenter(bot), FadeIn(topl)], Write(s1), FadeIn(s1b), FadeIn(ns1),
                  w=(.28, .36, .2, .16))

        # ---------------- beat 4: xi
        e1 = E(r"S_y|\,|\xi|=|230.0\,|S_y|-|5.3\,|S_y", size=44)
        e2 = E(r"\xi|=|224.8\text{ mm}", size=56)
        ne = T("left of the middle (250 mm):\nthe left booms are heavier", size=26, color=MUTED)
        g4 = VGroup(e1, e2, ne).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        g4.move_to([X0, -0.2, 0])
        xs = sec.p(4)[0] + (sec.p(3)[0] - sec.p(4)[0]) * 224.8 / 500
        xm = sec.p(4)[0] + (sec.p(3)[0] - sec.p(4)[0]) * 0.5
        ytop, ybot = sec.p(1)[1] + 0.3, sec.p(4)[1] - 0.75
        sc = DashedLine([xs, ybot, 0], [xs, ytop, 0], color=ROSE, stroke_width=5, dash_length=0.14)
        mid = DashedLine([xm, ybot, 0], [xm, ytop, 0], color=MUTED, stroke_width=3, dash_length=0.1)
        sy = Arrow([xs, -0.9, 0], [xs, 0.5, 0], buff=0, color=ROSE, stroke_width=7)
        syl = M(r"S_y", size=40, color=ROSE).next_to(sy, LEFT, buff=0.12)
        xil = M(r"\xi", size=44, color=ROSE)
        xi_span = span([sec.p(4)[0], ybot + 0.12, 0], [xs, ybot + 0.12, 0], "", side=DOWN)
        xil.next_to(xi_span, DOWN, buff=0.08)
        midl = T("middle", size=26, color=MUTED).next_to(mid, UP, buff=0.08).shift(RIGHT * 0.45)
        self.beat("So S y times xi equals two thirty minus five point three, and xi is two hundred twenty four point eight millimeters from the left web. Left of the middle, because the left booms are heavier.",
                  [FadeOut(g2), FadeOut(g3), FadeOut(arc), FadeOut(arm), FadeOut(topl)],
                  Write(e1), Write(e2), [FadeIn(glow(e2, ROSE)), Create(sc), GrowArrow(sy), FadeIn(syl)],
                  [FadeIn(xi_span), FadeIn(xil)], [Create(mid), FadeIn(midl), FadeIn(ne)],
                  Indicate(VGroup(sec.boom_m[1], sec.boom_m[4]), color=EMBER, scale_factor=1.6),
                  w=(.09, .18, .16, .16, .11, .16, .14))

        # ---------------- beat 5: checkpoint cue
        self.beat("Your turn. Pause here and do checkpoint three point one: the same steps for the practice box.",
                  Circumscribe(e2, color=ROSE), .5)
        self.checkpoint("3.1", "Practice box: booms, then the shear centre")
        self.wipe()
