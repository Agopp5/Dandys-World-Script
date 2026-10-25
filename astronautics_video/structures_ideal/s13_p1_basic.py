"""S13: I_xx and the basic shear flow of the idealized HW P1 box (BRIEF.md S13). Rework of old/s09_p1_basic.py."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

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

RX = 0.45                       # left edge of the algebra column
TOP = 3.0                       # top of the algebra column


def note(s):
    return T(s, size=30, color=MUTED)


def at_top(m, top=TOP):
    fit(m, 7.0 - RX, 6.6)
    m.next_to([RX, top, 0], DOWN, buff=0, aligned_edge=LEFT)
    m.align_to([RX, 0, 0], LEFT)
    return m


def below(m, other, buff=0.35):
    fit(m, 7.0 - RX, 6.6)
    m.next_to(other, DOWN, buff=buff)
    m.align_to([RX, 0, 0], LEFT)
    return m


def eq_under(new, old, i_new=0, i_old=1, buff=0.3):
    """Put `new` below `old` with new[i_new] (an '=') under old[i_old]."""
    new.next_to(old, DOWN, buff=buff)
    new.shift((old[i_old].get_center()[0] - new[i_new].get_center()[0]) * RIGHT)
    return new


def jump(tex):
    """A jump line; the \\frac{S_y}{I_{xx}} part (index 4) gets S_y in ROSE."""
    m = E(tex, size=44, cmap=QC)
    m[4][0:2].set_color(ROSE)
    return m


def boxed(m):
    return VGroup(SurroundingRectangle(m, color=HAIR, buff=0.16, corner_radius=0.1), m)


class S13_P1_Basic(VScene):
    budget = 197

    def construct(self):
        head = self.section("I xx and the basic shear flow")
        sec = hw_box(width=5.9, center=(-3.7, -0.25))
        walls = sec.draw()
        booms = sec.booms({1: B1, 2: B2, 3: B2, 4: B1})
        names = sec.names(size=36)
        c = (sec.p(1) + sec.p(3)) / 2
        top_y, bot_y = sec.p(1)[1], sec.p(4)[1]
        left_x, right_x = sec.p(1)[0], sec.p(2)[0]
        axis = DashedLine([left_x - 0.25, c[1], 0], [right_x + 0.25, c[1], 0], color=MUTED, stroke_width=2,
                          dash_length=0.12)
        axl = T("middle", size=30, color=MUTED).next_to([left_x + 0.66 * (right_x - left_x), c[1], 0], UP + RIGHT, buff=0.08)
        sx = left_x + 0.25 * (right_x - left_x)
        yup = span([sx, c[1], 0], [sx, top_y, 0], r"y=+150", side=RIGHT, off=0.25, color=INK2, size=34)
        ydn = span([sx, bot_y, 0], [sx, c[1], 0], r"y=-150", side=RIGHT, off=0.25, color=INK2, size=34)

        # beat 1: number the booms, mark y = +-150
        with self.say("Number the booms: one at the top left, then clockwise: two, three, four. Every boom is one hundred fifty millimeters above or below the middle.") as d:
            self.play(Create(walls), FadeIn(booms), run_time=.1 * d)
            for i in range(4):
                self.play(FadeIn(names[i], scale=1.6), Indicate(sec.boom_m[i + 1], color=EMBER, scale_factor=1.6),
                          run_time=.07 * d)
            self.wait(.08 * d)
            self.play(Create(axis), FadeIn(axl), run_time=.1 * d)
            self.play(GrowFromCenter(yup), run_time=.1 * d)
            self.play(GrowFromCenter(ydn), run_time=.1 * d)
            self.wait(.24 * d)

        # boom-area labels, outside each corner, toward the box's middle horizontally
        blab = VGroup()
        for n, b in ((1, B1), (2, B2), (3, B2), (4, B1)):
            p = sec.p(n)
            h = RIGHT if p[0] < c[0] else LEFT
            v = UP if p[1] > c[1] else DOWN
            blab.add(M(str(int(b)), size=36, color=EMBER).move_to(p + 0.42 * v + 0.85 * h))

        # beat 2: I_xy = 0, I_xx = sum B y^2 = 340 x 10^6
        lxy = E(r"I_{xy}|=|0", size=48)
        nxy = note("symmetric top to bottom")
        g0 = at_top(VGroup(lxy, nxy).arrange(RIGHT, buff=0.45))
        l1 = below(E(r"I_{xx}|=|\sum|B_r|\,y_r^2", size=48), g0, buff=0.55)
        n1 = note("y is 150 for every boom").next_to(l1, DOWN, buff=0.2).align_to(l1, LEFT)
        l2 = eq_under(E(r"=|2\,\big(|4000|+|3556|\big)|\,(150)^2", size=48, cmap=QC), l1, buff=0.85)
        l3 = eq_under(E(r"=|340.0\times 10^{6}\ \text{mm}^4", size=48), l2, buff=0.35)
        with self.say("The box is symmetric top to bottom, so I x y is zero. I x x is each boom area times one fifty squared, added up: two times four thousand plus three thousand five hundred fifty six, times one fifty squared. That's three hundred forty million.") as d:
            self.play(Write(lxy), FadeIn(nxy), Indicate(axis, color=INK), run_time=.12 * d)
            self.wait(.08 * d)
            self.play(Write(l1), run_time=.1 * d)
            self.play(FadeIn(n1), FadeIn(blab), Indicate(booms, color=EMBER, scale_factor=1.4), run_time=.12 * d)
            self.play(Write(l2[:2]), Indicate(VGroup(blab[0], blab[3]), color=EMBER), run_time=.12 * d)
            self.play(Write(l2[2:5]), Indicate(VGroup(blab[1], blab[2]), color=EMBER), run_time=.12 * d)
            self.play(Write(l2[5:]), Indicate(VGroup(yup, ydn), color=INK), run_time=.1 * d)
            self.play(Write(l3), run_time=.1 * d)
            gl3 = glow(l3[1], ACCENT)
            self.play(FadeIn(gl3), run_time=.06 * d)
            self.wait(.08 * d)

        # fold I_xx into one boxed result
        ixxq = E(r"I_{xx}|=|340.0\times 10^{6}\ \text{mm}^4", size=44)
        ixxg = at_top(boxed(ixxq))

        # beat 3: S_y at an unknown xi
        xs = left_x + 0.42 * (right_x - left_x)
        sy = Arrow([xs, c[1] - 1.25, 0], [xs, c[1] + 1.2, 0], color=ROSE, buff=0, stroke_width=8,
                   max_tip_length_to_length_ratio=0.16)
        syl = M("S_y", size=44, color=ROSE).next_to(sy.get_start(), DOWN, buff=0.1)
        xi = span([left_x, bot_y, 0], [xs, bot_y, 0], r"\xi", side=DOWN, off=0.85, color=ROSE, size=40)
        xq = T("unknown", size=30, color=MUTED).next_to(xi, RIGHT, buff=0.25)
        goal = VGroup(T("Goal: the shear centre, at", size=34), M(r"\xi=\,?", size=44, color=ROSE)).arrange(RIGHT, buff=0.2)
        below(goal, ixxg, buff=0.6)
        with self.say("We want the shear centre. So put a vertical load S y at an unknown distance xi from the left web.") as d:
            self.play(FadeOut(VGroup(lxy, nxy, l1, n1, l2, l3[0])), ReplacementTransform(l3[1:], ixxq[2:]),
                      FadeIn(ixxq[:2]), FadeIn(ixxg[0]), FadeOut(VGroup(yup, ydn, gl3)), run_time=.16 * d)
            self.play(FadeIn(goal), run_time=.14 * d)
            self.wait(.08 * d)
            self.play(GrowArrow(sy), FadeIn(syl), run_time=.16 * d)
            self.play(GrowFromCenter(xi), FadeIn(xq), Indicate(sec.walls_m[(4, 1)], color=ROSE), run_time=.18 * d)
            self.wait(.28 * d)

        # beat 4: cut wall 12, direction s, q_b12 = 0
        cx = sec.mid(1, 2)[0] + 0.2
        gap = Rectangle(width=0.18, height=0.32, fill_color=BG, fill_opacity=1, stroke_width=0).move_to([cx, top_y, 0])
        cut = VGroup(gap, *[Line([cx + dx - 0.1, top_y - 0.3, 0], [cx + dx + 0.1, top_y + 0.3, 0],
                                 color=INK, stroke_width=4) for dx in (-0.08, 0.08)])
        cutl = T("cut", size=34, color=INK).next_to(cut, UP, buff=0.08)
        s_ar = Arrow([cx + 0.35, top_y + 0.4, 0], [cx + 1.35, top_y + 0.4, 0], color=INK, buff=0, stroke_width=4,
                     max_tip_length_to_length_ratio=0.3)
        s_l = M("s", size=38).next_to(s_ar, UP, buff=0.06)
        loop = VMobject().set_points_as_corners([[cx + 0.1, top_y, 0], sec.p(2), sec.p(3), sec.p(4), sec.p(1),
                                                 [cx - 0.1, top_y, 0]])
        runner = Dot([cx + 0.1, top_y, 0], radius=0.11, color=SKY)
        z12 = M(r"q_{b,12}=0", size=40, color=SKY).next_to([left_x + 1.2, top_y, 0], DOWN, buff=0.4)
        r12 = E(r"q_{b,12}|=|0", size=44, cmap=QC)
        n12 = note("the flow starts at zero at the cut")
        g12 = below(VGroup(r12, n12).arrange(RIGHT, buff=0.4), ixxg, buff=0.6)
        with self.say("Cut the top wall. Then go around in order: one, two, three, four. Wall one two starts at zero, because of the cut.") as d:
            self.play(FadeOut(goal), FadeOut(xq), FadeIn(cut), FadeIn(cutl), run_time=.14 * d)
            self.wait(.06 * d)
            self.play(GrowArrow(s_ar), FadeIn(s_l), FadeIn(runner), run_time=.08 * d)
            self.play(MoveAlongPath(runner, loop, rate_func=linear),
                      Succession(Wait(.25), *[Indicate(names[i], color=SKY, scale_factor=1.6) for i in (1, 2, 3, 0)]),
                      run_time=.3 * d)
            self.play(FadeOut(runner), run_time=.04 * d)
            self.play(FadeIn(z12), Indicate(sec.walls_m[(1, 2)], color=SKY), Write(r12), FadeIn(n12), run_time=.16 * d)
            self.wait(.22 * d)

        # beat 5: jump at boom 2 -> right web
        rule = jump(r"q_2-q_1|=|-|\,|\frac{S_y}{I_{xx}}|\,B_r|\,y_r")
        nrule = note("the jump crossing boom r")
        grule = below(VGroup(rule, nrule).arrange(DOWN, aligned_edge=LEFT, buff=0.12), ixxg, buff=0.4)
        b = below(jump(r"q_{b,23}|=|0|-|\frac{S_y}{I_{xx}}|(3556)|(150)"), grule, buff=0.45)
        cc = eq_under(E(r"=|-1.569\times 10^{-3}|S_y", size=44), b, buff=0.3)
        nb = note("boom 2: B = 3556, y = +150").next_to(cc, DOWN, buff=0.22).align_to(b, LEFT)
        f23 = flow(sec, 2, 3, q23, label=r"q_{b,23}", size=40)
        f23[-1].next_to(f23[0], LEFT, buff=0.14)
        with self.say("Crossing boom two: minus S y over I x x, times three five five six, times one fifty. That's minus one point five six nine times ten to the minus three, S y, in the right web.") as d:
            self.play(FadeOut(g12), FadeIn(grule), run_time=.12 * d)
            self.wait(.06 * d)
            self.play(Write(b[:5]), Indicate(sec.boom_m[2], color=EMBER, scale_factor=1.8), run_time=.12 * d)
            self.play(Write(b[5]), Indicate(blab[1], color=EMBER), run_time=.08 * d)
            self.play(Write(b[6:]), FadeIn(nb), run_time=.08 * d)
            self.wait(.08 * d)
            self.play(Write(cc), run_time=.16 * d)
            self.play(FadeIn(f23), Indicate(sec.walls_m[(2, 3)], color=SKY), FadeIn(gcc := glow(cc[1:], SKY)), run_time=.14 * d)
            self.wait(.16 * d)

        # beat 6: boom 3 cancels it -> bottom wall zero
        q23q = E(r"q_{b,23}|=|-1.569\times 10^{-3}|S_y", size=44, cmap=QC)
        grule6 = grule.copy()
        at_top(grule6)
        q23b = below(boxed(q23q), grule6, buff=0.35)
        d1 = below(jump(r"q_{b,34}|=|q_{b,23}|-|\frac{S_y}{I_{xx}}|(3556)|(-150)"), q23b, buff=0.45)
        d2 = eq_under(E(r"=|0", size=44), d1, buff=0.3)
        nd = note("boom 3: y = -150, so it cancels").next_to(d2, DOWN, buff=0.22).align_to(d1, LEFT)
        z34 = M(r"q_{b,34}=0", size=40, color=SKY).next_to([sec.mid(3, 4)[0] + 1.0, bot_y, 0], UP, buff=0.4)
        with self.say("Boom three is one fifty below the middle, so it cancels that exactly: the bottom wall is zero.") as d:
            self.play(FadeOut(VGroup(ixxg, b, nb, cc[0], gcc)),
                      grule.animate.move_to(grule6), ReplacementTransform(cc[1:], q23q[2:]),
                      FadeIn(q23q[:2]), FadeIn(q23b[0]), run_time=.16 * d)
            self.play(Write(d1), Indicate(sec.boom_m[3], color=EMBER, scale_factor=1.8), run_time=.2 * d)
            self.play(Indicate(d1[6], color=EMBER), run_time=.1 * d)
            self.play(Write(d2), FadeIn(nd), run_time=.12 * d)
            self.play(FadeIn(z34), Indicate(sec.walls_m[(3, 4)], color=SKY), run_time=.14 * d)
            self.wait(.28 * d)

        # beat 7: boom 4 -> left web
        q23n = at_top(q23b.copy())
        q34q = E(r"q_{b,34}|=|0", size=44, cmap=QC)
        q34b = boxed(q34q).next_to(q23n, DOWN, buff=0.3).align_to(q23n, LEFT)
        e1 = below(jump(r"q_{b,41}|=|0|-|\frac{S_y}{I_{xx}}|(4000)|(-150)"), q34b, buff=0.55)
        e2 = eq_under(E(r"=|+1.765\times 10^{-3}|S_y", size=44), e1, buff=0.3)
        ne = note("boom 4: B = 4000, y = -150").next_to(e2, DOWN, buff=0.22).align_to(e1, LEFT)
        f41 = flow(sec, 4, 1, q41, label=r"q_{b,41}", size=40)
        with self.say("Boom four is also below the middle, and bigger: the left web gets plus one point seven six five times ten to the minus three, S y.") as d:
            self.play(FadeOut(VGroup(grule, d1[2:], d2[0], nd)), q23b.animate.move_to(q23n),
                      ReplacementTransform(d1[:2], q34q[:2]), ReplacementTransform(d2[1], q34q[2]), FadeIn(q34b[0]),
                      run_time=.14 * d)
            self.play(Write(e1[:5]), Indicate(sec.boom_m[4], color=EMBER, scale_factor=1.8), run_time=.14 * d)
            self.play(Write(e1[5:]), Indicate(blab[3], color=EMBER), Indicate(blab[2], color=EMBER), FadeIn(ne),
                      run_time=.14 * d)
            self.wait(.06 * d)
            self.play(Write(e2), run_time=.16 * d)
            self.play(FadeIn(f41), Indicate(sec.walls_m[(4, 1)], color=SKY), FadeIn(ge2 := glow(e2[1:], SKY)),
                      run_time=.14 * d)
            self.wait(.22 * d)
        self.wait(1.5)
        self.wipe()
