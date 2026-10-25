"""S08: idealize the HW P1 box into four booms (BRIEF.md S08)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

# facts (BRIEF.md, HW P1)
A_L = (60 + 50 - 10) * 10
A_R = (50 + 40 - 8) * 8
assert A_L == 1000 and A_R == 656
B_skin = 10 * 500 / 6 * (2 + 1)
assert np.isclose(B_skin, 2500) and np.isclose(B_skin, 10 * 500 / 2)
B_wl = 10 * 300 / 6 * (2 - 1)
B_wr = 8 * 300 / 6 * (2 - 1)
assert np.isclose(B_wl, 500) and np.isclose(B_wr, 400)
B1 = A_L + B_skin + B_wl
B2 = A_R + B_skin + B_wr
assert np.isclose(B1, 4000) and np.isclose(B2, 3556)

RX = 3.75         # centre x of the algebra column


def angle_L(c, ax, ay, lh, lv, t, s):
    """Filled L angle at corner c: horizontal leg lh along ax, vertical leg lv along ay, thickness t (mm)."""
    ax, ay = np.array([ax, 0, 0.0]), np.array([0, ay, 0.0])
    lh, lv, t = lh * s, lv * s, t * s
    pts = [c, c + ax * lh, c + ax * lh + ay * t, c + ax * t + ay * t, c + ax * t + ay * lv, c + ay * lv]
    return Polygon(*pts, color=EMBER, fill_color=EMBER, fill_opacity=.85, stroke_width=1.5).set_z_index(3)


def col(g, y, x0=.6):
    """Algebra column: left edge at x0, vertical centre y; asserts it stays inside the frame."""
    g.move_to([RX, y, 0]).align_to(np.array([x0, 0, 0]), LEFT)
    assert g.get_right()[0] < 6.95, g.get_right()
    return g


def row(eq, note=None):
    g = VGroup(eq)
    if note is not None:
        g.add(note.next_to(eq, DOWN, buff=.15, aligned_edge=LEFT))
    return g


class S08_P1_Booms(VScene):
    budget = 96

    def construct(self):
        self.section("Idealize the box")
        sec = hw_box()
        sec = Section(sec.pts, sec.walls, width=6.5, center=(-3.1, -0.4))
        s = sec.s
        walls = sec.draw()
        P = {k: sec.p(k) for k in (1, 2, 3, 4)}
        # into-the-box directions per corner (x sign, y sign)
        into = {1: (1, -1), 2: (-1, -1), 3: (-1, 1), 4: (1, 1)}
        angles = {1: angle_L(P[1], 1, -1, 60, 50, 10, s), 4: angle_L(P[4], 1, 1, 60, 50, 10, s),
                  2: angle_L(P[2], -1, -1, 50, 40, 8, s), 3: angle_L(P[3], -1, 1, 50, 40, 8, s)}
        ang = VGroup(*angles.values())

        tl = {(1, 2): M(r"t=10", size=32, color=INK2).move_to(sec.mid(1, 2) + .42 * DOWN),
              (3, 4): M(r"t=10", size=32, color=INK2).move_to(sec.mid(3, 4) + .42 * UP),
              (4, 1): M(r"t=10", size=32, color=INK2).move_to(sec.mid(4, 1) + .85 * RIGHT),
              (2, 3): M(r"t=8", size=32, color=INK2).move_to(sec.mid(2, 3) + .7 * LEFT)}
        tlab = VGroup(*tl.values())
        # outside the box: angle names above, dimensions below and left
        lab_L = M(r"60\times 50\times 10", size=32, color=EMBER).next_to(P[1], UP, buff=.3).shift(1.0 * RIGHT)
        lab_R = M(r"50\times 40\times 8", size=32, color=EMBER).next_to(P[2], UP, buff=.3).shift(.9 * LEFT)
        ya = P[4][1] - .32
        d500 = VGroup(DoubleArrow([P[4][0], ya, 0], [P[3][0], ya, 0], buff=0, color=AXIS, stroke_width=2,
                                  tip_length=.15),
                      M(r"500\ \mathrm{mm}", size=32, color=INK2))
        d500[1].next_to(d500[0], DOWN, buff=.1)
        xa = P[4][0] - .28
        d300 = VGroup(DoubleArrow([xa, P[4][1], 0], [xa, P[1][1], 0], buff=0, color=AXIS, stroke_width=2,
                                  tip_length=.15),
                      M(r"300\ \mathrm{mm}", size=32, color=INK2).rotate(PI / 2))
        d300[1].next_to(d300[0], LEFT, buff=.08)

        # beat 1: the box, the angles, the dimensions
        self.beat("Here's the box. Each corner has an angle: sixty by fifty by ten on the left, fifty by forty by eight on the right.",
                  Create(walls), [FadeIn(d500), FadeIn(d300), FadeIn(tlab)], .1,
                  [FadeIn(angles[1]), FadeIn(angles[4]), Write(lab_L)], .1,
                  [FadeIn(angles[2]), FadeIn(angles[3]), Write(lab_R)], w=(.3, .2, .25, .25))

        # each corner shows its running boom total just inside the corner
        def slot(k):
            sx, sy = into[k]
            return P[k] + np.array([sx * 1.05, sy * .55, 0])

        def tot_at(v, k):
            return M(str(int(round(v))), size=34, color=EMBER).move_to(slot(k))

        def grow(cur, vals, d_frac, d):
            """Corner totals morph to the new running values."""
            new = {k: tot_at(vals[k], k) for k in cur}
            self.play(*[ReplacementTransform(cur[k], new[k]) for k in cur],
                      *[Flash(slot(k), color=EMBER, line_length=.15, flash_radius=.5) for k in cur],
                      run_time=d_frac * d)
            return new

        # beat 2: angle areas
        r1 = row(E(r"A_L|=|(60+50-10)\times 10|=|1000", size=40),
                 T("legs minus overlap, times thickness", size=26, color=MUTED))
        r2 = row(E(r"A_R|=|(50+40-8)\times 8|=|656", size=40),
                 T("areas in square millimeters", size=26, color=MUTED))
        paint(r1[0], {4: EMBER}); paint(r2[0], {4: EMBER})
        alg2 = VGroup(r1, r2).arrange(DOWN, buff=.7, aligned_edge=LEFT)
        col(alg2, .3)
        cur = {k: tot_at(A_L if k in (1, 4) else A_R, k) for k in (1, 2, 3, 4)}
        self.beat("An angle's area is the sum of its legs minus the overlap, times thickness. Left: one thousand square millimeters. Right: six hundred fifty six.",
                  [Write(r1[0]), FadeIn(r1[1])], .05,
                  [Indicate(lab_L), Indicate(angles[1]), Indicate(angles[4])],
                  [TransformFromCopy(r1[0][4], cur[1]), TransformFromCopy(r1[0][4], cur[4])],
                  [Write(r2[0]), FadeIn(r2[1])],
                  [Indicate(lab_R), TransformFromCopy(r2[0][4], cur[2]), TransformFromCopy(r2[0][4], cur[3])],
                  w=(.25, .12, .15, .25, .2))

        # beat 3: skins, ratio one
        f3 = row(E(r"B|=|\frac{t_D\, b}{6}\Big(2+|\frac{\sigma_2}{\sigma_1}|\Big)", size=44),
                 T("skins: same stress at both edges", size=26, color=MUTED))
        paint(f3[0], {3: GOLD})
        n3 = E(r"\frac{\sigma_2}{\sigma_1}=1:|\quad B|=|\frac{10\times 500}{6}(2+1)", size=40)
        paint(n3, {0: GOLD})
        n3b = E(r"=|\frac{10\times 500}{2}|=|2500", size=40)
        paint(n3b, {3: EMBER})
        alg3 = VGroup(f3, n3, n3b).arrange(DOWN, buff=.55, aligned_edge=LEFT)
        n3b.align_to(n3, RIGHT)
        col(alg3, .2)
        skins = [sec.walls_m[(1, 2)], sec.walls_m[(3, 4)]]
        src = {k: M(r"+2500", size=32, color=EMBER).move_to(sec.mid(*((1, 2) if k in (1, 2) else (3, 4)))
                                                             + (1.0 * DOWN if k in (1, 2) else 1.0 * UP))
               for k in (1, 2, 3, 4)}
        with self.say("The top and bottom skins have the same stress at both ends, ratio one. Each gives ten times five hundred over two: twenty five hundred to each corner.") as d:
            self.play(FadeOut(alg2), Write(f3), *[Indicate(w_, color=GOLD, scale_factor=1.03) for w_ in skins],
                      run_time=.3 * d)
            self.play(Write(n3), run_time=.2 * d)
            self.play(Write(n3b), *[FadeIn(src[k]) for k in (1, 3)], run_time=.15 * d)
            self.add(src[2], src[4])
            self.play(*[src[k].animate.move_to(slot(k)).set_opacity(0) for k in src], run_time=.15 * d)
            self.remove(*src.values())
            cur = grow(cur, {1: A_L + B_skin, 4: A_L + B_skin, 2: A_R + B_skin, 3: A_R + B_skin}, .12, d)

        # beat 4: webs, ratio minus one; then the booms
        f4 = row(E(r"\frac{\sigma_2}{\sigma_1}=-1:|\quad B|=|\frac{t_D\, b}{6}(2-1)", size=40),
                 T("webs cross the neutral axis", size=26, color=MUTED))
        paint(f4[0], {0: GOLD})
        n4l = E(r"\text{left: }|\frac{10\times 300}{6}|=|500\ \mathrm{mm^2}", size=40)
        n4r = E(r"\text{right: }|\frac{8\times 300}{6}|=|400\ \mathrm{mm^2}", size=40)
        paint(n4l, {3: EMBER}); paint(n4r, {3: EMBER})
        alg4 = VGroup(f4, n4l, n4r).arrange(DOWN, buff=.55, aligned_edge=LEFT)
        col(alg4, .2)
        webs = [sec.walls_m[(4, 1)], sec.walls_m[(2, 3)]]
        t1 = E(r"B_1|=|1000+2500+500|=|4000", size=40)
        t2 = E(r"B_2|=|656+2500+400|=|3556", size=40)
        paint(t1, {4: EMBER}); paint(t2, {4: EMBER})
        n1 = T("angle plus skin plus web", size=26, color=MUTED)
        n2 = T("by symmetry: boom 4 as 1, boom 3 as 2", size=26, color=MUTED)
        tot = VGroup(t1, n1, t2, n2).arrange(DOWN, buff=.3, aligned_edge=LEFT)
        n1.shift(.1 * UP); t2.shift(.25 * DOWN); n2.shift(.15 * DOWN)
        col(tot, .2)
        # dot radius r0 + k sqrt(B), steepened so 4000 vs 3556 reads at a glance (radii 0.28 vs 0.19)
        sec.booms({1: B1, 2: B2, 3: B2, 4: B1}, r0=-1.3, k=.025)
        assert sec.boom_m[1].width > 1.3 * sec.boom_m[2].width
        names = sec.names()
        with self.say("The webs cross the neutral axis, ratio minus one: five hundred from the left web, four hundred from the right.") as d:
            self.play(FadeOut(alg3), Write(f4), *[Indicate(w_, color=GOLD, scale_factor=1.03) for w_ in webs],
                      run_time=.2 * d)
            self.play(Write(n4l), Write(n4r), run_time=.2 * d)
            cur = grow(cur, {1: B1, 4: B1, 2: B2, 3: B2}, .14, d)
            self.snap("webs")
            self.play(FadeOut(alg4), FadeIn(tot), FadeOut(d300), run_time=.14 * d)
            self.play(*[ReplacementTransform(angles[k], sec.boom_m[k]) for k in (1, 2, 3, 4)],
                      FadeIn(names), run_time=.18 * d)
            self.play(FadeIn(glow(t1[4], EMBER)), FadeIn(glow(t2[4], EMBER)), run_time=.1 * d)
        self.wait(.6)
        self.wipe()
