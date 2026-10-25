"""S09: I_xx and the basic shear flow of the idealized HW P1 box (BRIEF.md S09)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

# ---- facts (HW P1) ----
B1, B2 = 4000.0, 3556.0          # left booms 1, 4 and right booms 2, 3 (mm^2)
Y = 150.0                        # |y| of every boom (mm)
IXX = 2 * (B1 + B2) * Y ** 2
assert np.isclose(IXX, 340.0e6, rtol=1e-3)
k = 1.0 / IXX                    # S_y / I_xx per unit S_y
q12 = 0.0
q23 = q12 - k * B2 * Y
q34 = q23 - k * B2 * (-Y)
q41 = q34 - k * B1 * (-Y)
check(q23, -1.569e-3)
assert np.isclose(q34, 0.0, atol=1e-12)
check(q41, 1.765e-3)

QC = {"q_{b,12}": SKY, "q_{b,23}": SKY, "q_{b,34}": SKY, "q_{b,41}": SKY, "I_{xx}": INK,
      "4000": EMBER, "3556": EMBER, "(3556)": EMBER, "(4000)": EMBER}

RX = 0.4                        # left edge of the algebra column


def col(*rows, top=2.7, buff=0.3):
    """Stack rows down the right column, left-aligned at RX."""
    for r in rows:
        fit(r, 7.0 - RX, 6.6)
    g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    g.next_to([RX, top, 0], DOWN, buff=0, aligned_edge=LEFT)
    g.align_to([RX, 0, 0], LEFT)
    return g


def note(s):
    return T(s, size=26, color=MUTED)


def eq_under(new, old, i_new=0, i_old=1):
    """Put `new` below `old` with new[i_new] (an '=') under old[i_old]."""
    new.next_to(old, DOWN, buff=0.3)
    new.shift((old[i_old].get_center()[0] - new[i_new].get_center()[0]) * RIGHT)
    return new


class S09_P1_Basic(VScene):
    budget = 131

    def construct(self):
        head = self.section("The basic shear flow")
        sec = hw_box(width=6.2, center=(-3.35, -0.4))
        walls = sec.draw()
        booms = sec.booms({1: B1, 2: B2, 3: B2, 4: B1})
        names = sec.names()
        c = (sec.p(1) + sec.p(3)) / 2
        axis = DashedLine(c + 3.4 * LEFT, c + 3.4 * RIGHT, color=MUTED, stroke_width=2, dash_length=0.12)
        axl = M("x", size=30, color=MUTED).next_to(axis.get_end(), UP + LEFT, buff=0.1)
        # boom-area labels, tucked diagonally inside each corner
        blab = VGroup()
        for n, b in ((1, B1), (2, B2), (3, B2), (4, B1)):
            p = sec.p(n)
            d = (c - p) / np.linalg.norm(c - p)
            blab.add(M(str(int(b)), size=32, color=EMBER).move_to(p + 0.62 * d + 0.35 * (RIGHT if d[0] > 0 else LEFT)))
        self.add(walls, booms, names)

        # beat 1: I_xy = 0, then I_xx = sum B y^2
        lxy = E(r"I_{xy}|=|0", size=44)
        nxy = note("symmetric about the horizontal axis")
        l1 = E(r"I_{xx}|=|\textstyle\sum|B_r|\,y_r^2", size=44)
        l2 = E(r"=|2\,\big(|4000|+|3556|\big)|\,(150)^2", size=44, cmap=QC)
        l3 = E(r"=|340.0\times 10^{6}\ \text{mm}^4", size=44)
        n1 = note("two of each boom, all at y = 150 mm")
        blk = col(VGroup(lxy, nxy).arrange(DOWN, aligned_edge=LEFT, buff=0.15), l1, top=2.9, buff=0.45)
        eq_under(l2, l1)
        eq_under(l3, l2)
        n1.next_to(l3, DOWN, buff=0.25).align_to(l1, LEFT)
        self.beat("The box is symmetric about its horizontal axis, so I x y is zero. I x x is two times four thousand plus three thousand five hundred fifty six, times one fifty squared.",
                  [Create(axis), FadeIn(axl), Write(lxy), FadeIn(nxy)], .05, Write(l1),
                  [FadeIn(blab), Write(l2), Indicate(booms, color=EMBER)], .05, [Write(l3), FadeIn(n1)],
                  Circumscribe(l3[1], color=ACCENT),
                  w=(.2, .15, .3, .25, .1))

        # fold the I_xx work into one boxed result
        ixx = VGroup(E(r"I_{xx}|=|340.0\times 10^{6}\ \text{mm}^4", size=40))
        ixx_box = SurroundingRectangle(ixx, color=HAIR, buff=0.18, corner_radius=0.1)
        ixxg = VGroup(ixx_box, ixx).next_to([RX, 3.0, 0], DOWN, buff=0, aligned_edge=LEFT).align_to([RX, 0, 0], LEFT)

        # beat 2: S_y at unknown xi, cut wall 12, direction s
        xs = sec.p(1)[0] + 0.45 * (sec.p(2)[0] - sec.p(1)[0])
        sy = Arrow([xs, c[1] - 1.1, 0], [xs, c[1] + 1.25, 0], color=ROSE, buff=0, stroke_width=7,
                   max_tip_length_to_length_ratio=0.18)
        syl = M("S_y", size=40, color=ROSE).next_to(sy.get_start(), DOWN, buff=0.12)
        xi = span([sec.p(4)[0], sec.p(4)[1], 0], [xs, sec.p(4)[1], 0], r"\xi", side=DOWN, off=0.75, color=ROSE)
        xq = T("unknown", size=26, color=MUTED).next_to(xi, RIGHT, buff=0.2).shift(0.15 * DOWN)
        cx = sec.mid(1, 2)[0] + 1.2
        top_y = sec.p(1)[1]
        gap = Rectangle(width=0.16, height=0.3, fill_color=BG, fill_opacity=1, stroke_width=0).move_to([cx, top_y, 0])
        cut = VGroup(gap, *[Line([cx + dx - 0.1, top_y - 0.28, 0], [cx + dx + 0.1, top_y + 0.28, 0],
                                 color=INK, stroke_width=4) for dx in (-0.08, 0.08)])
        cutl = T("cut", size=26, color=INK).next_to(cut, UP, buff=0.1)
        s_ar = Arrow([cx + 0.35, top_y + 0.42, 0], [cx + 1.25, top_y + 0.42, 0], color=INK, buff=0, stroke_width=4,
                     max_tip_length_to_length_ratio=0.3)
        s_l = M("s", size=36).next_to(s_ar, UP, buff=0.06)
        self.beat("Put a vertical load S y somewhere, at a distance xi from the left web. Cut the top wall, and go around: one, two, three, four.",
                  [FadeOut(VGroup(lxy, nxy, l1, l2, l3, n1, axis, axl)), FadeIn(ixxg)],
                  [GrowArrow(sy), FadeIn(syl)], [GrowFromCenter(xi), FadeIn(xq)], .05,
                  [FadeIn(cut), FadeIn(cutl)], [GrowArrow(s_ar), FadeIn(s_l)],
                  *[Indicate(names[i], color=SKY, scale_factor=1.5) for i in range(4)],
                  w=(.1, .12, .14, .1, .1, .1, .1, .1, .1))

        # beat 3: q_b12 = 0, jump at boom 2
        rule = E(r"q_2-q_1|=|-\,(|S_y|/I_{xx})|\,B_r|\,y_r", size=40)
        nrule = note("jump crossing boom r")
        a = E(r"q_{b,12}|=|0", size=44, cmap=QC)
        na = note("the cut makes wall 12 start at zero")
        b = E(r"q_{b,23}|=|0|-|(|S_y|/I_{xx})|(3556)|(150)", size=42, cmap=QC)
        cc = E(r"=|-1.569\times 10^{-3}|\,S_y", size=44)
        nb = note("crossing boom 2: B = 3556, y = +150")
        g3 = col(VGroup(rule, nrule).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
                 VGroup(a, na).arrange(DOWN, aligned_edge=LEFT, buff=0.12), b, top=1.15, buff=0.4)
        eq_under(cc, b)
        nb.next_to(cc, DOWN, buff=0.25).align_to(b, LEFT)
        z12 = M(r"q_{b,12}=0", size=34, color=SKY).next_to([sec.mid(1, 2)[0] - 1.15, top_y, 0], DOWN, buff=0.5)
        f23 = flow(sec, 2, 3, q23, label=r"q_{b,23}", size=34)
        b2 = sec.boom_m[2]
        self.beat("Wall one two: zero. Crossing boom two: minus S y over I x x, times three five five six, times one fifty. That's minus one point five six nine times ten to the minus three, S y.",
                  [FadeOut(VGroup(cutl, xq)), FadeIn(rule), FadeIn(nrule)], [Write(a), FadeIn(na), FadeIn(z12)],
                  [Write(b), Indicate(b2, color=EMBER, scale_factor=1.8), FadeIn(nb)], .05,
                  [Write(cc), FadeIn(f23)], Circumscribe(cc[1:], color=SKY),
                  w=(.08, .17, .35, .25, .1))

        # beat 4: q_b34 = 0, q_b41
        q23box = E(r"q_{b,23}|=|-1.569\times 10^{-3}|\,S_y", size=40, cmap=QC)
        q23b = VGroup(SurroundingRectangle(q23box, color=HAIR, buff=0.16, corner_radius=0.1), q23box)
        q23b.next_to(ixxg, DOWN, buff=0.3).align_to(ixxg, LEFT)
        d1 = E(r"q_{b,34}|=|q_{b,23}|-|(|S_y|/I_{xx})|(3556)|(-150)", size=40, cmap=QC)
        d2 = E(r"=|0", size=44)
        nd = note("boom 3 sits at y = -150: the jump cancels")
        e1 = E(r"q_{b,41}|=|0|-|(|S_y|/I_{xx})|(4000)|(-150)", size=40, cmap=QC)
        e2 = E(r"=|+1.765\times 10^{-3}|\,S_y", size=44)
        ne = note("crossing boom 4: B = 4000, y = -150")
        for m in (d1, e1):
            fit(m, 7.0 - RX, 2)
        d1.next_to(q23b, DOWN, buff=0.5).align_to(q23b, LEFT)
        eq_under(d2, d1)
        nd.next_to(d2, DOWN, buff=0.2).align_to(d1, LEFT)
        e1.next_to(nd, DOWN, buff=0.45).align_to(d1, LEFT)
        eq_under(e2, e1)
        ne.next_to(e2, DOWN, buff=0.2).align_to(e1, LEFT)
        z34 = M(r"q_{b,34}=0", size=34, color=SKY).next_to([sec.mid(3, 4)[0] + 0.95, sec.p(3)[1], 0], UP, buff=0.75)
        f41 = flow(sec, 4, 1, q41, label=r"q_{b,41}", size=34)
        with self.say("Boom three is at minus one fifty, so it cancels that: wall three four is zero. Boom four brings the left web to plus one point seven six five times ten to the minus three.") as d:
            self.play(FadeOut(VGroup(rule, nrule, a, na, b, nb, cc[0])), ReplacementTransform(cc[1:], q23box[2:]),
                      FadeIn(q23b[0]), FadeIn(q23box[:2]), run_time=.1 * d)
            self.play(Write(d1), Indicate(sec.boom_m[3], color=EMBER, scale_factor=1.8), run_time=.17 * d)
            self.play(Write(d2), FadeIn(nd), FadeIn(z34), run_time=.15 * d)
            self.wait(.04 * d)
            self.play(Write(e1), Indicate(sec.boom_m[4], color=EMBER, scale_factor=1.8), run_time=.17 * d)
            self.play(Write(e2), FadeIn(ne), FadeIn(f41), run_time=.17 * d)
            self.play(Circumscribe(e2[1:], color=SKY), Indicate(f41, color=SKY), run_time=.12 * d)
            self.wait(.08 * d)
        self.wipe()
