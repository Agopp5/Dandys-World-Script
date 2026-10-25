"""S16: one closed cell under a torque (BRIEF.md S16)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# facts: rectangular cell 500 x 250 mm, all walls 2 mm, T = 10 kN m
W_MM, H_MM, T_WALL = 500, 250, 2
A_MM2 = W_MM * H_MM
assert A_MM2 == 125_000
T_NMM = 10 * 1e6                      # 10 kN m = 10 x 10^6 N mm
Q_VAL = T_NMM / (2 * A_MM2)
assert np.isclose(Q_VAL, 40.0)
TAU = Q_VAL / T_WALL
assert np.isclose(TAU, 20.0)

PTS = {1: (-W_MM / 2, H_MM / 2), 2: (W_MM / 2, H_MM / 2), 3: (W_MM / 2, -H_MM / 2), 4: (-W_MM / 2, -H_MM / 2)}
WALLS = [(1, 2, T_WALL), (2, 3, T_WALL), (3, 4, T_WALL), (4, 1, T_WALL)]
CCW = [(2, 1), (1, 4), (4, 3), (3, 2)]   # counterclockwise way round, the way the torque turns


def note(s):
    return T(s, size=30, color=MUTED)


def row(eq, nt):
    return VGroup(eq, nt).arrange(DOWN, buff=.16, aligned_edge=LEFT)


class S16_Torsion_Basics(VScene):
    budget = 134

    def construct(self):
        sec = Section(PTS, WALLS, width=6.4, center=(-2.95, -0.3))
        walls = sec.draw(t_scale=2.5)
        O = (sec.p(1) + sec.p(3)) / 2
        tq = torque(O + DOWN * .3, radius=0.7, ccw=True, label="T", size=44)

        # ---- beat 1: the cell and the torque
        self.beat("Now a different load: a pure twist. A torque T is applied to the wing box, and nothing else.",
                  Create(walls), FadeIn(tq), .25)

        # ---- beat 2: one constant shear flow, all the way round
        flows = VGroup(*[flow(sec, a, b, 1, label="q", size=36, frac=.5) for a, b in CCW])
        r0 = row(E(r"q|=|\text{same on every wall}", size=48), note("one value for the whole cell"))
        r1 = row(E(r"dT|=|p|\cdot|q|\,ds", size=48, cmap={"dT": LILAC}),
                 note("moment = lever arm x force"))
        r2 = row(E(r"p\,ds|=|2\,dA", size=48), note("twice the area of the thin triangle"))
        r3 = row(E(r"T|=|q|\oint p\,ds|=|2|A|q", size=52), note("A = area enclosed by the wall midline"))
        rows = VGroup(r0, r1, r2, r3).arrange(DOWN, buff=.42, aligned_edge=LEFT)
        place(rows, "right")
        self.beat("In a single closed cell under pure torque, the shear flow is the same all the way around. "
                  "Call it q.",
                  LaggedStart(*[GrowArrow(f[0]) if isinstance(f, VGroup) else Create(f) for f in flows],
                              lag_ratio=.3),
                  [FadeIn(f[1:]) for f in flows if isinstance(f, VGroup)],
                  Write(r0[0]), FadeIn(r0[1]), .2)

        # ---- beat 3: a little piece ds, its force q ds, lever arm p
        p1, p2 = sec.p(1), sec.p(2)
        a = p1 + (p2 - p1) * .70           # ds runs leftward (the flow direction) along the top wall
        b = p1 + (p2 - p1) * .58
        piece = Line(a, b, color=SKY, stroke_width=12)
        ds_lab = M(r"ds", size=36, color=SKY).next_to(piece, DOWN, buff=.18)
        f_arr = Arrow(a + UP * .32 + RIGHT * .1, b + UP * .32 + LEFT * .25, buff=0, color=SKY, stroke_width=6,
                      max_tip_length_to_length_ratio=.35)
        f_lab = M(r"q\,ds", size=36, color=SKY).next_to(f_arr, UP, buff=.1)
        foot = np.array([O[0], p1[1], 0])
        o_dot = Dot(O, radius=.08, color=INK)
        o_lab = M(r"O", size=34, color=INK).next_to(o_dot, DL, buff=.08)
        lever = DashedLine(O, foot, color=INK, stroke_width=4)
        p_lab = M(r"p", size=40, color=INK).next_to(lever, LEFT, buff=.12)
        k = .2
        corner = VMobject(color=INK, stroke_width=3).set_points_as_corners(
            [foot + DOWN * k, foot + DOWN * k + RIGHT * k, foot + RIGHT * k])
        ext = DashedLine(foot, b, color=MUTED, stroke_width=2)   # the wall's line of action, out to ds
        with self.say("Each little piece of wall carries a force q d s. "
                      "Its moment about the middle is that force times its lever arm.") as d:
            self.play(flows.animate.set_opacity(.25), FadeOut(tq), run_time=.08 * d)
            self.play(Create(piece), FadeIn(ds_lab), run_time=.1 * d)
            self.play(GrowArrow(f_arr), FadeIn(f_lab), run_time=.12 * d)
            self.wait(.1 * d)
            self.play(FadeIn(o_dot), FadeIn(o_lab), Create(lever), run_time=.12 * d)
            self.play(Create(corner), Create(ext), FadeIn(p_lab), run_time=.08 * d)
            self.play(Write(r1[0]), FadeIn(r1[1]), run_time=.2 * d)

        # ---- beat 4: p ds = 2 dA; triangles fill the cell; T = 2 A q
        tri0 = Polygon(O, a, b, color=INK2, stroke_width=2, fill_color=INK2, fill_opacity=.5)
        tris = VGroup()
        loop = [sec.p(2), sec.p(1), sec.p(4), sec.p(3), sec.p(2)]
        n_per = [10, 5, 10, 5]
        idx = 0
        for (u, v), n in zip(zip(loop[:-1], loop[1:]), n_per):
            for i in range(n):
                s0, s1 = u + (v - u) * i / n, u + (v - u) * (i + 1) / n
                tris.add(Polygon(O, s0, s1, color=HAIR, stroke_width=1.5, fill_color=INK2,
                                 fill_opacity=.18 if idx % 2 else .34))
                idx += 1
        tris.set_z_index(-1)
        box = SurroundingRectangle(r3[0][5:], color=LILAC, buff=.14, stroke_width=4)
        with self.say("Lever arm times d s is twice the area of the thin triangle it sweeps. "
                      "Going all the way around, the triangles fill the whole cell. "
                      "So the torque is two times the enclosed area, times q.") as d:
            self.play(FadeIn(tri0), run_time=.08 * d)
            self.play(Write(r2[0]), FadeIn(r2[1]), run_time=.14 * d)
            self.wait(.08 * d)
            self.play(FadeOut(VGroup(f_arr, f_lab, corner, ext)),
                      LaggedStart(*[FadeIn(t) for t in tris], lag_ratio=.12), run_time=.25 * d)
            self.play(Write(r3[0][:4]), run_time=.12 * d)
            self.play(Write(r3[0][4:]), FadeIn(r3[1]), run_time=.12 * d)
            g3 = glow(r3[0][5:])
            self.play(Create(box), FadeIn(g3), run_time=.08 * d)

        # ---- beat 5: the numbers
        self.play(FadeOut(VGroup(tris, tri0, piece, ds_lab, o_dot, o_lab, lever, p_lab, r0, r1, r2, r3, box, g3)),
                  flows.animate.set_opacity(1), FadeIn(tq), run_time=1.2)
        p1, p3, p4 = sec.p(1), sec.p(3), sec.p(4)
        y_d = p4[1] - .45
        dim_w = VGroup(DoubleArrow([p4[0], y_d, 0], [p3[0], y_d, 0], buff=0, color=MUTED, stroke_width=3,
                                   tip_length=.2),
                       M(r"500\ \text{mm}", size=36, color=INK2))
        dim_w[1].next_to(dim_w[0], DOWN, buff=.1)
        x_d = p4[0] - .3
        dim_h = VGroup(DoubleArrow([x_d, p4[1], 0], [x_d, p1[1], 0], buff=0, color=MUTED, stroke_width=3,
                                   tip_length=.2),
                       M(r"250\ \text{mm}", size=36, color=INK2).rotate(PI / 2))
        dim_h[1].next_to(dim_h[0], LEFT, buff=.1)
        t_lab = TX(r"all walls $t = 2$ mm", size=34).next_to(dim_w, DOWN, buff=.25)
        nA = row(E(r"A|=|500 \times 250|=|125\,000\ \text{mm}^2", size=46), note("width times height of the cell"))
        nq1 = E(r"q|=|\frac{T}{2A}", size=48)
        nq2 = E(r"=|\frac{10 \times 10^{6}}{2 \times 125\,000}|=|40\ \text{N/mm}", size=46)
        nq = VGroup(nq1, nq2, TX(r"$T$ = 10 kN m = $10 \times 10^{6}$ N mm", size=30, color=MUTED)).arrange(
            DOWN, buff=.2, aligned_edge=LEFT)
        nq2.shift(RIGHT * .45)
        nt = row(E(r"\tau|=|\frac{q}{t}|=|\frac{40}{2}|=|20\ \text{N/mm}^2", size=46),
                 note("shear stress in the 2 mm wall"))
        nums = VGroup(nA, nq, nt).arrange(DOWN, buff=.42, aligned_edge=LEFT)
        place(nums, "right")
        flows40 = VGroup(*[flow(sec, a_, b_, 1, label=r"40", size=36, frac=.5) for a_, b_ in CCW])
        with self.say("For a five hundred by two fifty cell, A is one hundred twenty five thousand square "
                      "millimeters. Under ten kilonewton meters, q is ten million over two hundred fifty "
                      "thousand: forty newtons per millimeter.") as d:
            self.play(FadeIn(dim_w), FadeIn(dim_h), run_time=.06 * d)
            self.play(Write(nA[0]), FadeIn(nA[1]), run_time=.14 * d)
            self.wait(.06 * d)
            self.play(Write(nq1), FadeIn(nq[2]), run_time=.1 * d)
            self.play(Write(nq2[:2]), run_time=.12 * d)
            self.play(Write(nq2[2:]), FadeIn(glow(nq2[3])), ReplacementTransform(flows, flows40),
                      run_time=.1 * d)
            self.wait(.06 * d)
            self.play(FadeIn(t_lab), Write(nt[0]), FadeIn(nt[1]), run_time=.14 * d)
            self.play(FadeIn(glow(nt[0][-1])), run_time=.04 * d)
        self.wait(1.2)
        self.wipe()
