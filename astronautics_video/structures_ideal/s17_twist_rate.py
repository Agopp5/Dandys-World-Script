"""S17: how much one closed cell twists (BRIEF.md S17)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# facts: the S16 cell, 500 x 250 mm, all walls 2 mm, G = 27 000 N/mm^2, T = 10 kN m
W_MM, H_MM, T_MM, G_MOD, TORQUE = 500, 250, 2, 27000, 10e6
A_CELL = W_MM * H_MM
assert A_CELL == 125000
Q = TORQUE / (2 * A_CELL)
assert np.isclose(Q, 40)
PERIM = 2 * (W_MM + H_MM)
assert PERIM == 1500
DELTA = PERIM / T_MM
assert np.isclose(DELTA, 750)
RATE = Q * DELTA / (2 * A_CELL * G_MOD)          # rad/mm
assert np.isclose(RATE, 4.44e-6, rtol=2e-3)
DEG_PER_M = RATE * 1000 * 180 / np.pi
assert np.isclose(DEG_PER_M, 0.25, atol=0.01)     # 0.2546 deg/m: "about a quarter"

ANG = 12 * DEGREES                                # drawn twist, exaggerated (real: 4.4e-6 rad/mm)
CF = np.array([-3.85, -1.75, 0])                    # front section centre
DEPTH = np.array([1.2, 2.1, 0])                   # oblique offset of the section a distance dz behind


def rot(v, a=ANG):
    c, s = np.cos(a), np.sin(a)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0])


class S17_Twist_Rate(VScene):
    budget = 152

    def construct(self):
        pts = {"1": (0, H_MM), "2": (W_MM, H_MM), "3": (W_MM, 0), "4": (0, 0)}
        walls = [("1", "2", T_MM), ("2", "3", T_MM), ("3", "4", T_MM), ("4", "1", T_MM)]
        sec = Section(pts, walls, width=5.0, center=tuple(CF[:2]))
        corners = [sec.p(k) for k in ("1", "2", "3", "4")]
        local = [c - CF for c in corners]

        # back section (a distance dz behind), faint
        back_pts = [c + DEPTH for c in corners]
        back = sec.draw(t_scale=2.0).copy().shift(DEPTH).set_stroke(opacity=.55)
        # front section: opaque cut face + walls
        face = Polygon(*corners, stroke_width=0, fill_color=BG, fill_opacity=.92)
        front = VGroup(face, sec.draw(t_scale=2.0))
        front.set_z_index(2)
        tq_local = np.array([-1.5, 0, 0])
        tq = torque(CF + tq_local, radius=.55, color=LILAC, label="T").set_z_index(4)

        edges = always_redraw(lambda: VGroup(*[
            Line(back_pts[i], face.get_vertices()[i], color=INK2, stroke_width=3) for i in range(4)]))

        # ghost of the untwisted front section + the twist angle
        ghost = DashedVMobject(Polygon(*corners, color=MUTED, stroke_width=3), num_dashes=40).set_z_index(3)
        r_end = CF + np.array([2.5, 0, 0])
        rad0 = DashedLine(CF, r_end, color=MUTED, stroke_width=3).set_z_index(3)
        rad1 = Line(CF, CF + rot([2.5, 0]), color=INK, stroke_width=3).set_z_index(3)
        arc = Arc(radius=2.05, start_angle=0, angle=ANG, arc_center=CF, color=INK, stroke_width=4).set_z_index(3)
        dth = E(r"d\theta", size=40).move_to(CF + 2.95 * rot([1, 0], ANG / 2) + np.array([0, .05, 0]))
        dth = backed(dth).set_z_index(5)

        # dz marker along the bottom-right edge
        p0, p1 = CF + rot(local[2]), back_pts[2]
        u = (p1 - p0) / np.linalg.norm(p1 - p0)
        nrm = np.array([u[1], -u[0], 0])
        dz_arrow = DoubleArrow(p0 + .4 * nrm, p1 + .4 * nrm, buff=0, color=INK, stroke_width=3,
                               tip_length=.2, max_tip_length_to_length_ratio=.2)
        dz_lab = E(r"dz", size=40).move_to((p0 + p1) / 2 + .85 * nrm)
        note_x = T("(twist drawn exaggerated)", size=30, color=MUTED)
        note_x.move_to([-6.7 + note_x.width / 2, 3.5, 0])

        rate_word = T("rate of twist", size=36, color=INK2)
        rate_m = E(r"\frac{d\theta}{dz}", size=60)
        rate_note = T("twist per unit length of span", size=30, color=MUTED)
        rate_card = VGroup(rate_word, rate_m, rate_note).arrange(DOWN, buff=.35).move_to([3.7, 1.0, 0])

        self.beat("The torque also twists the box a little. The twist per unit length along the span is called the rate of twist, d theta by d z.",
                  [FadeIn(front), FadeIn(tq)], [Create(back), Create(edges)], .06,
                  [Rotate(front, ANG, about_point=CF), tq.animate.shift(rot(tq_local) - tq_local),
                   FadeIn(ghost)],
                  [Create(rad0), Create(rad1), Create(arc), FadeIn(dth), FadeIn(note_x)],
                  [GrowFromCenter(dz_arrow), FadeIn(dz_lab)],
                  .06, FadeIn(rate_word), Write(rate_m), FadeIn(rate_note), .1,
                  w=(.08, .1, .14, .12, .08, .06, .1, .06))
        edges.clear_updaters()

        # labels: G above the box, t at the bottom wall
        g_word = T("shear modulus", size=34, color=INK2)
        g_m = E(r"G", size=44)
        g_lab = VGroup(g_word, g_m).arrange(RIGHT, buff=.25).move_to([-2.9, 2.4, 0])
        top_mid = CF + rot([0, local[0][1]])
        t_m = E(r"t", size=44).move_to(top_mid + np.array([0, .85, 0])).set_z_index(5)
        t_arrow = Arrow(t_m.get_bottom() + DOWN * .05, top_mid + UP * .08, buff=0, color=INK, stroke_width=3,
                        tip_length=.18)
        t_word = backed(T("thickness", size=34, color=INK2).next_to(t_m, LEFT, buff=.3)).set_z_index(5)

        self.beat("How much it twists depends on the material's shear stiffness, the shear modulus G, and on how thin the walls are.",
                  .05, [FadeIn(g_word), Write(g_m)], Indicate(g_m, color=ACCENT), .08,
                  [FadeIn(t_word), Write(t_m), GrowArrow(t_arrow)],
                  Indicate(front[1], color=INK, scale_factor=1.03), .15,
                  w=(.2, .12, .25, .15))

        # beat 3: the formula, read piece by piece
        L1 = E(r"\frac{d\theta}{dz}|=|\frac{1}{2AG}|\oint|\frac{q\,ds}{t}", size=50)
        L1[2][-1].set_color(ACCENT)          # the G in 2AG
        L1[4][0].set_color(SKY)              # the q
        L1.next_to([0.7, 2.75, 0], RIGHT, buff=0)
        n1 = VGroup(E(r"A", size=36), T("area enclosed by the wall", size=30, color=MUTED)).arrange(RIGHT, buff=.25)
        n2 = VGroup(E(r"\oint", size=36), T("once all the way around the cell", size=30, color=MUTED)).arrange(RIGHT, buff=.25)
        notes1 = VGroup(n1, n2).arrange(DOWN, aligned_edge=LEFT, buff=.2).next_to(L1, DOWN, buff=.35, aligned_edge=LEFT)

        self.beat("The formula is: d theta by d z equals one over two A G, times the integral of q d s over t, all the way around.",
                  [FadeOut(rate_word), FadeOut(rate_note), ReplacementTransform(rate_m, L1[0])],
                  [Write(L1[1]), Write(L1[2])], .05, Write(L1[3]), Write(L1[4]),
                  Circumscribe(L1[3], color=INK2), FadeIn(notes1), .15,
                  w=(.14, .18, .1, .16, .1, .1))

        # beat 4: delta, and its value for this cell
        L2 = E(r"\delta|=|\int|\frac{ds}{t}", size=50).next_to(notes1, DOWN, buff=.55, aligned_edge=LEFT)
        L2n = T("for one wall", size=30, color=MUTED).next_to(L2, RIGHT, buff=.5)
        t_new = E(r"t = 2\ \text{mm}", size=44)
        t_new.next_to(t_m.get_left(), RIGHT, buff=0)
        t_new = backed(t_new).set_z_index(5)
        t_word2 = backed(T("every wall", size=34, color=INK2).next_to(t_new, LEFT, buff=.3)).set_z_index(5)
        perim = VGroup(T("perimeter", size=30, color=MUTED), E(r"2(500 + 250) = 1500\ \text{mm}", size=36)).arrange(RIGHT, buff=.25)
        L3 = E(r"\oint|\frac{ds}{t}|=|\frac{1500}{2}|=|750", size=50).next_to(L2, DOWN, buff=.5, aligned_edge=LEFT)
        perim.next_to(L3, DOWN, buff=.4, aligned_edge=LEFT)
        g3 = glow(L3[5], ACCENT)

        self.beat("We'll call the integral of d s over t, for a wall, delta. For our cell, every wall is two millimeters thick, so delta around the cell is fifteen hundred over two: seven fifty.",
                  [Write(L2), FadeIn(L2n)], .1,
                  [ReplacementTransform(t_m, t_new), ReplacementTransform(t_word, t_word2)],
                  Indicate(front[1], color=INK, scale_factor=1.03), FadeIn(perim),
                  Write(L3[0:2]), Write(L3[2:4]), Write(L3[4:]), FadeIn(g3), .15,
                  w=(.16, .12, .08, .1, .08, .12, .08, .06))

        # beat 5: plug in and convert
        lab_a = E(r"A = 125\,000\ \text{mm}^2", size=34).move_to(CF + rot([0.95, .68])).set_z_index(5)
        lab_q = E(r"q| = 40\ \text{N/mm}", size=34).move_to(CF + rot([0.95, -.68])).set_z_index(5)
        g_val = E(r"=|27\,000\ \text{N/mm}^2", size=44)
        g_tgt = VGroup(g_word.copy(), g_m.copy(), g_val).arrange(RIGHT, buff=.22).move_to([-3.55, 2.4, 0])
        L3_tgt = L3.copy().next_to(L1, DOWN, buff=.45, aligned_edge=LEFT)
        L4 = E(r"=|\frac{40 \times 750}{2 \times 125\,000 \times 27\,000}", size=48)
        L4.next_to(L3_tgt, DOWN, buff=.45, aligned_edge=LEFT)
        L5 = E(r"=|4.44 \times 10^{-6}|\ \text{rad/mm}", size=48).next_to(L4, DOWN, buff=.4, aligned_edge=LEFT)
        L5[0].shift(LEFT * .12)
        box5 = SurroundingRectangle(L5[1:], color=GOOD, buff=.1)
        L6 = E(r"\approx|0.25^{\circ}\ \text{per meter}", size=48).next_to(L5, DOWN, buff=.4, aligned_edge=LEFT)
        L6n = VGroup(T("converted:", size=30, color=MUTED), E(r"\times 1000 \times \frac{180}{\pi}", size=38)).arrange(RIGHT, buff=.25)
        L6n.next_to(L6, DOWN, buff=.25, aligned_edge=LEFT)

        self.beat("So the rate of twist is forty times seven fifty, over two times one twenty five thousand times twenty seven thousand. That's four point four four times ten to the minus six radians per millimeter: about a quarter of a degree per meter.",
                  [FadeOut(notes1), FadeOut(L2), FadeOut(L2n), FadeOut(perim), FadeOut(g3), Transform(L3, L3_tgt)],
                  [FadeIn(lab_a), FadeIn(lab_q), g_word.animate.move_to(g_tgt[0]), g_m.animate.move_to(g_tgt[1]),
                   FadeIn(g_val)],
                  Write(L4[0]), Write(L4[1]), .1, Write(L5), Create(box5), .1,
                  Write(L6), FadeIn(L6n), .1,
                  w=(.07, .1, .03, .2, .16, .05, .12, .05))
        self.wait(1.0)
        self.wipe()
