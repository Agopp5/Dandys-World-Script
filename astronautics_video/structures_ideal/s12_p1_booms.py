"""S12: idealize the HW P1 box into four booms (BRIEF.md S12; rework of old/s08_p1_booms.py)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# facts (BRIEF.md, HW P1)
A_L = (60 + 50 - 10) * 10
A_R = (50 + 40 - 8) * 8
assert A_L == 1000 and A_R == 656
assert 60 + 50 - 10 == 100 and 50 + 40 - 8 == 82
B_skin = 10 * 500 / 6 * (2 + 1)
assert np.isclose(B_skin, 2500) and np.isclose(B_skin, 10 * 500 / 2)
B_wl = 10 * 300 / 6 * (2 - 1)
B_wr = 8 * 300 / 6 * (2 - 1)
assert np.isclose(B_wl, 500) and np.isclose(B_wr, 400)
B1 = A_L + B_skin + B_wl
B2 = A_R + B_skin + B_wr
assert np.isclose(B1, 4000) and np.isclose(B2, 3556)

X0 = 0.55         # left edge of the algebra column
NOTE = 30         # grey "why" notes
LAB = 34          # labels on the picture


def angle_L(c, ax, ay, lh, lv, t, s):
    """Filled L angle at corner c: horizontal leg lh along ax, vertical leg lv along ay, thickness t (mm)."""
    ax, ay = np.array([ax, 0, 0.0]), np.array([0, ay, 0.0])
    lh, lv, t = lh * s, lv * s, t * s
    pts = [c, c + ax * lh, c + ax * lh + ay * t, c + ax * t + ay * t, c + ax * t + ay * lv, c + ay * lv]
    return Polygon(*pts, color=EMBER, fill_color=EMBER, fill_opacity=.85, stroke_width=1.5).set_z_index(3)


def col(g, y):
    """Algebra column: left edge at X0, vertical centre y; asserts it stays inside the frame."""
    g.move_to([3.6, y, 0]).align_to(np.array([X0, 0, 0]), LEFT)
    assert g.get_right()[0] < 6.95, g.get_right()
    assert g.get_top()[1] < 3.0 and g.get_bottom()[1] > -3.85, (g.get_top(), g.get_bottom())
    return g


def note(s, color=MUTED):
    return T(s, size=NOTE, color=color)


class S12_P1_Booms(VScene):
    budget = 224

    def construct(self):
        self.section("Idealize the box")
        sec = hw_box(width=6.4, center=(-3.15, -0.45))
        s = sec.s
        walls = sec.draw(t_scale=1.4)
        P = {k: sec.p(k) for k in (1, 2, 3, 4)}
        into = {1: (1, -1), 2: (-1, -1), 3: (-1, 1), 4: (1, 1)}   # into-the-box directions per corner
        angles = {1: angle_L(P[1], 1, -1, 60, 50, 10, s), 4: angle_L(P[4], 1, 1, 60, 50, 10, s),
                  2: angle_L(P[2], -1, -1, 50, 40, 8, s), 3: angle_L(P[3], -1, 1, 50, 40, 8, s)}

        # thickness labels (inside), dimensions (outside: below and left)
        t_top = M(r"t=10", size=LAB, color=INK2).move_to(sec.mid(1, 2) + .45 * DOWN)
        t_bot = M(r"t=10", size=LAB, color=INK2).move_to(sec.mid(3, 4) + .45 * UP)
        t_lft = M(r"t=10", size=LAB, color=INK2).move_to(sec.mid(4, 1) + .75 * RIGHT)
        t_rgt = M(r"t=8", size=LAB, color=INK2).move_to(sec.mid(2, 3) + .6 * LEFT)
        ya = P[4][1] - .3
        d500 = VGroup(DoubleArrow([P[4][0], ya, 0], [P[3][0], ya, 0], buff=0, color=AXIS, stroke_width=2,
                                  tip_length=.18),
                      M(r"500\ \mathrm{mm}", size=LAB, color=INK2))
        d500[1].next_to(d500[0], DOWN, buff=.1)
        xa = P[4][0] - .3
        d300 = VGroup(DoubleArrow([xa, P[4][1], 0], [xa, P[1][1], 0], buff=0, color=AXIS, stroke_width=2,
                                  tip_length=.18),
                      M(r"300\ \mathrm{mm}", size=LAB, color=INK2).rotate(PI / 2))
        d300[1].next_to(d300[0], LEFT, buff=.08)

        # beat 1: the box
        self.beat("Here's homework problem one. A box, five hundred millimeters wide and three hundred tall. The top and bottom skins and the left web are ten millimeters thick. The right web is eight.",
                  Create(walls), .08, FadeIn(d500), FadeIn(d300), .08,
                  [FadeIn(t_top), FadeIn(t_bot), FadeIn(t_lft),
                   Indicate(sec.walls_m[(1, 2)], color=INK, scale_factor=1.02),
                   Indicate(sec.walls_m[(3, 4)], color=INK, scale_factor=1.02),
                   Indicate(sec.walls_m[(4, 1)], color=INK, scale_factor=1.02)],
                  [FadeIn(t_rgt), Indicate(sec.walls_m[(2, 3)], color=INK, scale_factor=1.02)], .14,
                  w=(.2, .12, .12, .28, .14))

        # beat 2: the corner angles
        lab_L = M(r"60\times 50\times 10", size=LAB, color=EMBER).next_to(P[1], UP, buff=.35).shift(1.2 * RIGHT)
        lab_R = M(r"50\times 40\times 8", size=LAB, color=EMBER).next_to(P[2], UP, buff=.35).shift(1.1 * LEFT)
        self.beat("Each corner has an angle, a little L shaped stiffener. Sixty by fifty by ten on the left. Fifty by forty by eight on the right.",
                  [FadeIn(angles[k], scale=1.4) for k in (1, 2, 3, 4)], .08,
                  [Write(lab_L), Indicate(angles[1]), Indicate(angles[4])], .08,
                  [Write(lab_R), Indicate(angles[2]), Indicate(angles[3])], .14,
                  w=(.25, .3, .3))

        # beat 3: four corner booms to fill
        def slot(k):
            sx, sy = into[k]
            return P[k] + np.array([sx * 1.15, sy * .6, 0])

        rings = VGroup(*[DashedVMobject(Circle(radius=.55, color=EMBER, stroke_width=3), num_dashes=24)
                         .move_to(P[k]) for k in (1, 2, 3, 4)])
        qs = VGroup(*[M(r"B_%d=\,?" % k, size=LAB, color=EMBER).move_to(slot(k)) for k in (1, 2, 3, 4)])
        self.beat("The problem asks us to replace all this with four corner booms, so let's add up what goes into each boom. First the angles.",
                  Create(rings), .06, [FadeIn(m_) for m_ in qs], .1,
                  FadeOut(rings), [Indicate(angles[k], scale_factor=1.3) for k in (1, 2, 3, 4)], .1,
                  w=(.25, .2, .15, .3))

        def tot_at(v, k):
            return M(str(int(round(v))), size=LAB + 4, color=EMBER).move_to(slot(k))

        def grow(cur, vals, run):
            """Corner totals morph to the new running values."""
            new = {k: tot_at(vals[k], k) for k in cur}
            self.play(*[ReplacementTransform(cur[k], new[k]) for k in cur],
                      *[Flash(slot(k), color=EMBER, line_length=.18, flash_radius=.55) for k in cur],
                      run_time=run)
            return new

        # beat 4: left angle area
        h4 = VGroup(note("area: two legs, minus overlap,"), note("times the thickness")).arrange(DOWN, buff=.12, aligned_edge=LEFT)
        e4a = E(r"(60+50-10)|\times 10", size=48)
        e4b = E(r"=|100\times 10|=|1000", size=48)
        paint(e4b, {3: EMBER})
        n4 = note("left angles, square mm", EMBER)
        alg4 = VGroup(h4, e4a, e4b, n4).arrange(DOWN, buff=.4, aligned_edge=LEFT)
        e4b.shift(.5 * RIGHT)
        col(alg4, 1.0)
        cur = {k: tot_at(A_L if k in (1, 4) else A_R, k) for k in (1, 2, 3, 4)}
        self.beat("An angle's area is the two leg lengths, minus the overlap, times the thickness. Sixty plus fifty minus ten is one hundred, times ten: one thousand square millimeters on the left.",
                  [FadeIn(h4), Indicate(lab_L)], .06, Write(e4a[0]), Write(e4a[1]), .05,
                  [Write(e4b[0]), Write(e4b[1])], [Write(e4b[2]), Write(e4b[3]), FadeIn(n4)],
                  [TransformFromCopy(e4b[3], cur[1]), TransformFromCopy(e4b[3], cur[4]), FadeOut(qs[0]), FadeOut(qs[3])], .14,
                  w=(.2, .2, .1, .15, .15, .2))

        # beat 5: right angle area
        e5a = E(r"(50+40-8)|\times 8", size=48)
        e5b = E(r"=|82\times 8|=|656", size=48)
        paint(e5b, {3: EMBER})
        n5 = note("right angles", EMBER)
        alg5 = VGroup(e5a, e5b, n5).arrange(DOWN, buff=.4, aligned_edge=LEFT)
        e5b.shift(.5 * RIGHT)
        col(alg5, -1.9)
        # squeeze the left result up so both fit: drop the long header note
        self.beat("Fifty plus forty minus eight is eighty two, times eight: six hundred fifty six on the right.",
                  [Indicate(lab_R), VGroup(e4a, e4b, n4).animate.shift(.75 * UP), FadeOut(h4)],
                  Write(e5a), [Write(e5b), FadeIn(n5)],
                  [TransformFromCopy(e5b[3], cur[2]), TransformFromCopy(e5b[3], cur[3]), FadeOut(qs[1]), FadeOut(qs[2])], .16,
                  w=(.15, .25, .3, .2))
        alg45 = VGroup(e4a, e4b, n4, e5a, e5b, n5)

        # beat 6: skins, ratio one
        f6 = E(r"B|=|\frac{t_D\, b}{6}\Big(2+|\frac{\sigma_2}{\sigma_1}|\Big)", size=48)
        n6 = VGroup(note("skins: same stress at both ends,"), note("so the ratio is 1")).arrange(DOWN, buff=.12, aligned_edge=LEFT)
        s6 = E(r"B|=|\frac{10\times 500}{6}(2+1)", size=48)
        r6 = E(r"=|\frac{10\times 500}{2}|=|2500", size=48)
        paint(r6, {3: EMBER})
        n6b = note("to each corner", EMBER)
        alg6 = VGroup(f6, n6, s6, r6, n6b).arrange(DOWN, buff=.32, aligned_edge=LEFT)
        r6.shift(.5 * RIGHT)
        n6b.shift(.5 * RIGHT)
        col(alg6, -.35)
        skins = [sec.walls_m[(1, 2)], sec.walls_m[(3, 4)]]
        src6 = {1: sec.mid(1, 2) + 1.05 * DOWN + 1.2 * LEFT, 2: sec.mid(1, 2) + 1.05 * DOWN + 1.2 * RIGHT,
                3: sec.mid(3, 4) + 1.05 * UP + 1.2 * RIGHT, 4: sec.mid(3, 4) + 1.05 * UP + 1.2 * LEFT}
        add6 = {k: M(r"+2500", size=LAB, color=EMBER).move_to(src6[k]) for k in src6}
        with self.say("Next the skins. Top and bottom skins have the same stress at both ends, so the ratio is one. Each gives ten times five hundred over two: twenty five hundred to each corner.") as d:
            self.play(FadeOut(alg45), Write(f6), *[Indicate(w_, color=GOLD, scale_factor=1.03) for w_ in skins],
                      run_time=.16 * d)
            self.play(FadeIn(n6), Indicate(f6[3], color=GOLD), run_time=.16 * d)
            self.wait(.06 * d)
            self.play(Write(s6), run_time=.14 * d)
            self.play(Write(r6), run_time=.14 * d)
            self.play(FadeIn(n6b), *[FadeIn(add6[k]) for k in add6], run_time=.1 * d)
            self.play(*[add6[k].animate.move_to(slot(k)).set_opacity(0) for k in add6], run_time=.08 * d)
            self.remove(*add6.values())
            cur = grow(cur, {1: A_L + B_skin, 4: A_L + B_skin, 2: A_R + B_skin, 3: A_R + B_skin}, .06 * d)
            self.wait(.1 * d)

        # beat 7: webs, ratio minus one
        f7 = E(r"\frac{\sigma_2}{\sigma_1}=-1:|\quad B|=|\frac{t_D\, b}{6}(2-1)", size=48)
        paint(f7, {0: GOLD})
        n7 = note("webs cross the neutral axis")
        l7 = E(r"\text{left: }|\frac{10\times 300}{6}|=|500", size=48)
        r7 = E(r"\text{right: }|\frac{8\times 300}{6}|=|400", size=48)
        paint(l7, {3: EMBER}); paint(r7, {3: EMBER})
        alg7 = VGroup(f7, n7, l7, r7).arrange(DOWN, buff=.4, aligned_edge=LEFT)
        col(alg7, -.35)
        webs = [sec.walls_m[(4, 1)], sec.walls_m[(2, 3)]]
        na = Line(sec.mid(4, 1) + 1.2 * RIGHT, sec.mid(2, 3) + 1.2 * LEFT, color=GOLD, stroke_width=3)
        na = DashedLine(na.get_start(), na.get_end(), color=GOLD, stroke_width=3, dash_length=.15)
        na_lab = T("neutral axis", size=NOTE, color=GOLD).next_to(na, UP, buff=.1)
        src7 = {1: sec.mid(4, 1) + 1.6 * RIGHT + .55 * UP, 4: sec.mid(4, 1) + 1.6 * RIGHT + .55 * DOWN,
                2: sec.mid(2, 3) + 1.6 * LEFT + .55 * UP, 3: sec.mid(2, 3) + 1.6 * LEFT + .55 * DOWN}
        add7 = {k: M(r"+500" if k in (1, 4) else r"+400", size=LAB, color=EMBER).move_to(src7[k]) for k in src7}
        with self.say("Last, the webs. They cross the neutral axis, so the ratio is minus one. The left web gives ten times three hundred over six: five hundred. The right web gives eight times three hundred over six: four hundred.") as d:
            self.play(FadeOut(alg6), FadeIn(f7), *[Indicate(w_, color=GOLD, scale_factor=1.03) for w_ in webs],
                      run_time=.12 * d)
            self.play(Create(na), FadeIn(na_lab), FadeIn(n7), run_time=.14 * d)
            self.wait(.06 * d)
            self.play(Write(l7), run_time=.14 * d)
            self.play(*[FadeIn(add7[k]) for k in (1, 4)], run_time=.06 * d)
            self.wait(.04 * d)
            self.play(Write(r7), run_time=.14 * d)
            self.play(*[FadeIn(add7[k]) for k in (2, 3)], run_time=.06 * d)
            self.play(*[add7[k].animate.move_to(slot(k)).set_opacity(0) for k in add7],
                      FadeOut(na), FadeOut(na_lab), run_time=.08 * d)
            self.remove(*add7.values())
            cur = grow(cur, {1: B1, 4: B1, 2: B2, 3: B2}, .06 * d)
            self.wait(.08 * d)

        # beat 8: the totals and the booms
        a8 = E(r"B_1=B_4|=|1000+2500+500", size=44)
        b8 = E(r"=|4000\ \mathrm{mm^2}", size=44)
        c8 = E(r"B_2=B_3|=|656+2500+400", size=44)
        d8 = E(r"=|3556\ \mathrm{mm^2}", size=44)
        for m_ in (a8[0], b8[1], c8[0], d8[1]):
            m_.set_color(EMBER)
        n8 = note("angle + skin + web")
        alg8 = VGroup(a8, b8, c8, d8, n8).arrange(DOWN, buff=.35, aligned_edge=LEFT)
        b8.align_to(a8[1], LEFT); d8.align_to(c8[1], LEFT)
        c8.shift(.25 * DOWN); d8.shift(.25 * DOWN); n8.shift(.25 * DOWN)
        col(alg8, -.35)
        # dot radius r0 + k sqrt(B), steepened so 4000 vs 3556 reads at a glance (radii 0.28 vs 0.19)
        sec.booms({1: B1, 2: B2, 3: B2, 4: B1}, r0=-1.3, k=.025)
        assert sec.boom_m[1].width > 1.3 * sec.boom_m[2].width
        names = VGroup(*[M(str(k), size=LAB, color=INK2).move_to(P[k] + (.55 if k in (1, 2) else -.55) * UP)
                         for k in (1, 2, 3, 4)])   # straight above/below: the algebra sits just right of the box
        with self.say("Adding it all up: each left boom is four thousand square millimeters, and each right boom is three thousand five hundred fifty six.") as d:
            self.play(FadeOut(alg7), FadeIn(a8), FadeIn(n8), run_time=.12 * d)
            self.play(Write(b8), Indicate(cur[1]), Indicate(cur[4]), run_time=.16 * d)
            self.wait(.08 * d)
            self.play(FadeIn(c8), run_time=.1 * d)
            self.play(Write(d8), Indicate(cur[2]), Indicate(cur[3]), run_time=.16 * d)
            self.play(*[ReplacementTransform(angles[k], sec.boom_m[k]) for k in (1, 2, 3, 4)],
                      FadeOut(lab_L), FadeOut(lab_R), FadeOut(d500), FadeOut(d300), FadeIn(names), run_time=.2 * d)
            self.play(FadeIn(glow(b8[1], EMBER)), FadeIn(glow(d8[1], EMBER)), run_time=.1 * d)
        self.wait(2.0)
        self.wipe()
