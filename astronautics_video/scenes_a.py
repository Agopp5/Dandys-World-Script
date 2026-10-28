"""Part 0-2: Intro, reference frames, direction cosine matrices."""
from common import *  # noqa: F401,F403
from proj3d import Cam, Draw, grow, show, hide  # noqa: F401


# =================================================================== Intro
def make_earth(radius=1.6, with_land=True):
    disk = Circle(radius=radius, stroke_color="#7FB3FF", stroke_width=3,
                  fill_color="#16335C", fill_opacity=1)
    g = VGroup(disk)
    if with_land:
        rng = np.random.default_rng(3)
        for (ang, r, size) in [(0.4, 0.55, 0.45), (2.2, 0.5, 0.55), (3.9, 0.6, 0.4), (5.2, 0.3, 0.35)]:
            pts = []
            for k in range(9):
                t = TAU * k / 9
                rr = size * radius * (0.6 + 0.4 * rng.random())
                pts.append([rr * np.cos(t), rr * np.sin(t), 0])
            blob = Polygon(*pts).round_corners(radius * 0.08)
            blob.set_fill("#3E7D4A", 1).set_stroke(width=0)
            blob.move_to(r * radius * np.array([np.cos(ang), np.sin(ang), 0]))
            g.add(blob)
    return g


def make_ufo(scale=1.0):
    body = Ellipse(width=0.5, height=0.16, fill_color="#B8BCC8", fill_opacity=1, stroke_width=0)
    dome = Arc(radius=0.13, start_angle=0, angle=PI, fill_color="#9EE6C0",
               fill_opacity=1, stroke_width=0).shift(UP * 0.04)
    lights = VGroup(*[Dot(radius=0.018, color=YELLOW).move_to([x, -0.01, 0]) for x in (-0.14, 0, 0.14)])
    return VGroup(dome, body, lights).scale(scale)


class Intro(Scene2D):
    def construct(self):
        title = Tx(r"Same Arrow, Different Observers").scale(1.35)
        sub = Tx(r"Reference frames, DCMs, and the transport theorem", color=DIM).scale(0.75)
        tag = Tx(r"AERSP 309 $\cdot$ Astronautics", color=B_COL).scale(0.6)
        VGroup(title, sub, tag).arrange(DOWN, buff=0.35)

        with self.voice("intro_1"):
            self.play(Write(title), run_time=1.5)
            self.play(FadeIn(sub, shift=UP * 0.2), FadeIn(tag), run_time=0.8)
            self.wait(0.6)
            self.play(FadeOut(VGroup(title, sub, tag)), run_time=0.6)
            # side view: Earth, State College, the UFO
            earth = make_earth(2.2, with_land=False).shift(DOWN * 3.4)
            site = earth[0].point_at_angle(PI / 2 + 0.25)
            dot = Dot(site, color=YELLOW, radius=0.06)
            sc = Tx("State College", color=YELLOW).scale(0.5).next_to(dot, LEFT, buff=0.15)
            ufo = make_ufo(1.4)
            direction = normalize(site - earth[0].get_center())
            ufo.move_to(site + direction * 1.5)
            alt = DashedLine(site, ufo.get_bottom(), color=DIM)
            alt_lab = Tx("80 km", color=DIM).scale(0.5).next_to(alt, RIGHT, buff=0.1)
            q = Tx("How fast is it moving?").scale(1.0).to_edge(UP, buff=0.6)
            self.play(FadeIn(earth, shift=UP), run_time=1.0)
            self.play(FadeIn(dot), FadeIn(sc), FadeIn(ufo, shift=DOWN * 0.3), Create(alt), FadeIn(alt_lab))
            self.play(ufo.animate.shift(UP * 0.06), rate_func=there_and_back, run_time=0.8)
            self.play(Write(q), run_time=min(1.2, self.left()))
        side = VGroup(earth, dot, sc, ufo, alt, alt_lab)

        # two observers: top-down views from above the north pole
        with self.voice("intro_2"):
            self.play(FadeOut(side), q.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=0.8)
            L = make_earth(1.5).move_to(LEFT * 3.5 + DOWN * 0.3)
            R = make_earth(1.5).move_to(RIGHT * 3.5 + DOWN * 0.3)
            ufoL = make_ufo(0.7).move_to(L.get_center() + 1.9 * np.array([np.cos(1.1), np.sin(1.1), 0]))
            ufoR = make_ufo(0.7).move_to(R.get_center() + 1.9 * np.array([np.cos(1.1), np.sin(1.1), 0]))
            hL = Tx("Bob, on the ground", color=Q_COL).scale(0.7).next_to(L, UP, buff=0.75)
            hR = Tx("Someone out in space", color=B_COL).scale(0.7).next_to(R, UP, buff=0.75)
            vL = T(r"v = 0", color=Q_COL).next_to(L, DOWN, buff=0.55)
            vR = T(r"|\vec v| \approx 356\ \text{m/s}", color=B_COL).next_to(R, DOWN, buff=0.55)
            pole = Tx("view from above the North Pole", color=DIM).scale(0.45).to_edge(DOWN, buff=0.2)
            self.play(FadeIn(L), FadeIn(R), FadeIn(ufoL), FadeIn(ufoR), FadeIn(hL), FadeIn(hR), FadeIn(pole))
            self.play(Write(vL))
            spin = ValueTracker(0)
            grpR = VGroup(R, ufoR)
            trail = TracedPath(lambda: ufoR.get_center(), stroke_color=B_COL, stroke_width=2,
                               dissipating_time=2.5)
            self.add(trail)
            last = [0.0]

            def rot(m):
                a = spin.get_value()
                m.rotate(a - last[0], about_point=R.get_center())
                last[0] = a
            grpR.add_updater(rot)
            self.add(grpR)
            self.play(spin.animate.set_value(PI * 0.9), Write(vR, run_time=1.5),
                      run_time=self.left() - 0.2, rate_func=linear)
            grpR.remove_updater(rot)
        panels = VGroup(L, R, ufoL, ufoR, hL, hR, vL, vR, pole, trail)

        with self.voice("intro_3"):
            both = Tx("Both are right.").scale(1.1).move_to(UP * 0.5)
            self.play(FadeOut(panels), FadeOut(q), run_time=0.8)
            self.play(Write(both))
            self.wait(0.8)
            line2 = Tx(r"The difference isn't the UFO.\\It's the ", r"observer", ".").scale(0.95)
            line2[1].set_color(YELLOW)
            line2.next_to(both, DOWN, buff=0.5)
            self.play(FadeIn(line2, shift=UP * 0.2))
            self.wait(1.6)
            key = Tx(r"Who is looking, and how is their view turning?", color=B_COL).scale(0.8)
            key.next_to(line2, DOWN, buff=0.7)
            self.play(Write(key), run_time=min(2.0, self.left()))
        msg = VGroup(both, line2, key)

        with self.voice("intro_4"):
            self.play(FadeOut(msg))
            items = [
                ("1", "Reference frames \\& vectors"),
                ("2", "Direction cosine matrices"),
                ("3", "Euler angles"),
                ("4", "Angular velocity"),
                ("5", "The transport theorem"),
                ("6", "Acceleration: Coriolis \\& centripetal"),
            ]
            rows = VGroup()
            for n, t in items:
                rows.add(VGroup(Tx(n + ".", color=B_COL), Tx(t)).arrange(RIGHT, buff=0.3))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.85)
            dt = (self.left() - 3.0) / 6
            for r in rows:
                self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=0.5)
                self.wait(max(0, dt - 0.5))
            box = SurroundingRectangle(rows[4], color=YELLOW, buff=0.12)
            self.play(Create(box))
            self.hold()
        self.play(FadeOut(rows), FadeOut(box))


# ================================================================== Frames
R_VEC = np.array([1.6, 2.2, 1.7])
B_FRAME = euler321(np.radians(40), np.radians(-25), np.radians(30))


class Frames(Scene2D):
    def construct(self):
        cam = Cam(phi=70, theta=28, scale=1.15, center=(1.9, -0.9))
        D = Draw(cam)
        L = 2.6
        r_ar = D.arrow(ORIGIN, R_VEC, R_COL, width=6, k=0)
        r_lab = D.label(r"\vec r", R_VEC * 1.1 + np.array([0, 0, 0.15]), R_COL, 0.9)
        self.add(*cam.trackers())

        with self.voice("frames_1"):
            cap = Tx(r"A vector: a length and a direction").scale(0.75).to_corner(UL)
            self.add(r_ar, r_lab)
            self.play(*grow(r_ar), run_time=1.5)
            self.play(*show(r_lab), Write(cap))
            cam.start_spin(self, 0.035)
            self.wait(2.0)
            cap2 = Tx(r"No numbers needed", color=DIM).scale(0.65).next_to(cap, DOWN, aligned_edge=LEFT)
            self.play(FadeIn(cap2))
            self.hold()

        nf, nlabs = D.frame(np.eye(3), N_COL, L, [r"\hat n_1", r"\hat n_2", r"\hat n_3"])
        with self.voice("frames_2"):
            self.play(FadeOut(cap), FadeOut(cap2))
            o = D.dot(ORIGIN, WHITE, 0.06)
            olab = D.label("O", np.array([0.3, -0.3, -0.25]), WHITE, 0.6)
            self.add(nf, nlabs, o, olab)
            self.play(*show(olab), run_time=0.6)
            self.play(LaggedStart(*grow(*nf), lag_ratio=0.3), run_time=2)
            self.play(*show(*nlabs))
            eq1 = T(r"\mathcal N:\ \{O,\ \hat n_1,\ \hat n_2,\ \hat n_3\}").scale(0.8)
            eq2 = T(r"\hat n_i\cdot\hat n_j = \begin{cases}1 & i=j\\0 & i\neq j\end{cases}").scale(0.7)
            eq3 = T(r"\hat n_1\times\hat n_2 = \hat n_3").scale(0.8)
            panel = VGroup(eq1, eq2, eq3).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_corner(UL)
            self.play(Write(eq1))
            self.play(Write(eq2))
            self.play(Write(eq3), run_time=min(1.2, self.left()))
            self.hold()

        x, y, z = R_VEC
        with self.voice("frames_3"):
            self.play(FadeOut(panel))
            foot = np.array([x, y, 0])
            d1 = D.line(R_VEC, foot, DIM, 2, dashed=True, k=0)
            d2 = D.line(foot, [x, 0, 0], DIM, 2, dashed=True, k=0)
            d3 = D.line(foot, [0, y, 0], DIM, 2, dashed=True, k=0)
            d4 = D.line(R_VEC, [0, 0, z], DIM, 2, dashed=True, k=0)
            s1 = D.line(ORIGIN, [x, 0, 0], R_COL, 9, k=0)
            s2 = D.line(ORIGIN, [0, y, 0], R_COL, 9, k=0)
            s3 = D.line(ORIGIN, [0, 0, z], R_COL, 9, k=0)
            nshadow = VGroup(d1, d2, d3, d4, s1, s2, s3)
            self.add(nshadow, r_ar, r_lab)
            e1 = T(r"x = \vec r\cdot\hat n_1").scale(0.8)
            e2 = T(r"y = \vec r\cdot\hat n_2").scale(0.8)
            e3 = T(r"z = \vec r\cdot\hat n_3").scale(0.8)
            shadows = VGroup(e1, e2, e3).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UL).shift(DOWN * 0.6)
            hdr = Tx(r"Components are shadows", color=R_COL).scale(0.75).to_corner(UL)
            self.play(FadeIn(hdr))
            self.play(*grow(d1, d2), run_time=0.8)
            self.play(*grow(s1), Write(e1), run_time=1.0)
            self.wait(1.5)
            self.play(*grow(d3, s2), Write(e2), run_time=1.0)
            self.play(*grow(d4, s3), Write(e3), run_time=1.0)
            self.hold()

        with self.voice("frames_4"):
            col = T(r"\vec r = x\,\hat n_1 + y\,\hat n_2 + z\,\hat n_3"
                    r"\ \longleftrightarrow\ ",
                    r"r_{(\mathcal N)}", r"=\begin{bmatrix}%.1f\\%.1f\\%.1f\end{bmatrix}" % (x, y, z)).scale(0.72)
            col.to_corner(UL)
            self.play(FadeOut(shadows), FadeOut(hdr))
            self.play(Write(col), run_time=2.0)
            box = SurroundingRectangle(col[1], color=YELLOW, buff=0.08)
            self.play(Create(box))
            note = Tx(r"the arrow is the vector;\\the column is one description of it",
                      color=DIM).scale(0.6).next_to(col, DOWN, buff=0.4, aligned_edge=LEFT)
            self.play(FadeIn(note))
            self.hold()

        rb = B_FRAME @ R_VEC
        with self.voice("frames_5"):
            self.play(FadeOut(box), FadeOut(note), *[m.op.animate.set_value(0.25) for m in nshadow])
            bf, blabs = D.frame(B_FRAME, B_COL, L, [r"\hat b_1", r"\hat b_2", r"\hat b_3"])
            self.add(bf, blabs, r_ar, r_lab)
            self.play(LaggedStart(*grow(*bf), lag_ratio=0.3), run_time=1.6)
            self.play(*show(*blabs))
            bsh = VGroup()
            for i in range(3):
                q = rb[i] * B_FRAME[i]
                bsh.add(D.line(ORIGIN, q, B_COL, 9, k=0))
                bsh.add(D.line(R_VEC, q, B_COL, 2, dashed=True, k=0))
            self.add(bsh, r_ar, r_lab)
            self.play(LaggedStart(*grow(*bsh), lag_ratio=0.2), run_time=2.0)
            colb = T(r"r_{(\mathcal B)}", r"=\begin{bmatrix}%.2f\\%.2f\\%.2f\end{bmatrix}" % tuple(rb),
                     color=B_COL).scale(0.72)
            colb.next_to(col, DOWN, buff=0.5, aligned_edge=LEFT)
            self.play(Write(colb))
            tag = Tx(r"Same arrow, different numbers", color=YELLOW).scale(0.8).to_edge(DOWN)
            self.play(Write(tag))
            self.hold()
        cam.stop_spin()
        self.play(FadeOut(Group(*self.mobjects)))


# ===================================================================== DCM
class DCM(Scene2D):
    def construct(self):
        O = LEFT * 3.6 + DOWN * 0.6
        L = 2.6
        th = ValueTracker(0.0)

        def bvec(i):
            t = th.get_value()
            return [np.array([np.cos(t), np.sin(t), 0]), np.array([-np.sin(t), np.cos(t), 0])][i]

        n1 = Arrow(O, O + L * RIGHT, buff=0, color=N_COL, stroke_width=4)
        n2 = Arrow(O, O + L * UP, buff=0, color=N_COL, stroke_width=4)
        n1l = T(r"\hat n_1", color=N_COL).scale(0.8).next_to(n1.get_end(), RIGHT, buff=0.1)
        n2l = T(r"\hat n_2", color=N_COL).scale(0.8).next_to(n2.get_end(), UP, buff=0.1)
        out = VGroup(Circle(radius=0.12, color=WHITE, stroke_width=2), Dot(radius=0.035)).move_to(O)
        outl = T(r"\hat n_3 = \hat b_3", color=DIM).scale(0.6).next_to(O, DL, buff=0.1)
        b1 = always_redraw(lambda: Arrow(O, O + L * bvec(0), buff=0, color=B_COL, stroke_width=5))
        b2 = always_redraw(lambda: Arrow(O, O + L * bvec(1), buff=0, color=B_COL, stroke_width=5))
        b1l = always_redraw(lambda: T(r"\hat b_1", color=B_COL).scale(0.8).move_to(O + (L + 0.35) * bvec(0)))
        b2l = always_redraw(lambda: T(r"\hat b_2", color=B_COL).scale(0.8).move_to(O + (L + 0.35) * bvec(1)))
        arc1 = always_redraw(lambda: Arc(radius=0.9, start_angle=0, angle=th.get_value() + 1e-4,
                                         arc_center=O, color=YELLOW))
        arc1l = always_redraw(lambda: T(r"\theta", color=YELLOW).scale(0.7).move_to(
            O + 1.15 * np.array([np.cos(th.get_value() / 2), np.sin(th.get_value() / 2), 0])))

        with self.voice("dcm_1"):
            hdr = Tx("Direction Cosine Matrices", color=B_COL).scale(0.9).to_edge(UP, buff=0.3)
            self.play(Write(hdr))
            self.play(GrowArrow(n1), GrowArrow(n2), FadeIn(n1l), FadeIn(n2l), FadeIn(out), FadeIn(outl))
            self.play(FadeIn(b1), FadeIn(b2), FadeIn(b1l), FadeIn(b2l))
            self.add(arc1, arc1l)
            self.play(th.animate.set_value(np.radians(32)), run_time=2.0)
            self.hold()

        t0 = np.radians(32)
        tip1 = O + L * np.array([np.cos(t0), np.sin(t0), 0])
        tip2 = O + L * np.array([-np.sin(t0), np.cos(t0), 0])
        with self.voice("dcm_2"):
            drop = DashedLine(tip1, [tip1[0], O[1], 0], color=DIM)
            seg = Line(O, [tip1[0], O[1], 0], color=YELLOW, stroke_width=8)
            segl = T(r"\cos\theta", color=YELLOW).scale(0.7).next_to(seg, DOWN, buff=0.15)
            eq = T(r"\hat b_1\cdot\hat n_1", r"= |\hat b_1||\hat n_1|\cos\theta", r"= \cos\theta").scale(0.8)
            eq.move_to(RIGHT * 2.8 + UP * 2.2)
            self.play(Create(drop), Create(seg), run_time=1.2)
            self.play(Write(eq[0]))
            self.wait(1.5)
            self.play(Write(eq[1]), FadeIn(segl))
            self.play(Write(eq[2]), run_time=min(1.0, self.left()))
            self.hold()

        with self.voice("dcm_3"):
            drop2 = DashedLine(tip1, [O[0], tip1[1], 0], color=DIM)
            seg2 = Line(O, [O[0], tip1[1], 0], color=YELLOW, stroke_width=8)
            seg2l = T(r"\sin\theta", color=YELLOW).scale(0.7).next_to(seg2, LEFT, buff=0.15)
            arc90 = Arc(radius=0.6, start_angle=t0, angle=PI / 2 - t0, arc_center=O, color=V_COL)
            arc90l = T(r"90^\circ\!-\theta", color=V_COL).scale(0.5).move_to(O + 0.95 * np.array([np.cos(1.15), np.sin(1.15), 0]) + RIGHT * 0.25)
            eq2 = T(r"\hat b_1\cdot\hat n_2 = \cos(90^\circ-\theta) = \sin\theta").scale(0.8)
            eq2.next_to(eq, DOWN, buff=0.35, aligned_edge=LEFT)
            self.play(Create(arc90), FadeIn(arc90l), Write(eq2), run_time=1.5)
            self.play(Create(drop2), Create(seg2), FadeIn(seg2l))
            rows = VGroup(
                T(r"\hat b_1 = \phantom{-}\cos\theta\,\hat n_1 + \sin\theta\,\hat n_2"),
                T(r"\hat b_2 = -\sin\theta\,\hat n_1 + \cos\theta\,\hat n_2"),
                T(r"\hat b_3 = \hat n_3"),
            ).scale(0.75).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(eq2, DOWN, buff=0.5, aligned_edge=LEFT)
            self.play(Write(rows[0]))
            g2 = VGroup(DashedLine(tip2, [tip2[0], O[1], 0], color=DIM),
                        DashedLine(tip2, [O[0], tip2[1], 0], color=DIM))
            self.play(Create(g2), Write(rows[1]))
            self.play(Write(rows[2]), run_time=min(1.0, self.left()))
            self.hold()
        construction = VGroup(drop, seg, segl, drop2, seg2, seg2l, arc90, arc90l, g2)

        with self.voice("dcm_4"):
            self.play(FadeOut(eq), FadeOut(eq2), FadeOut(construction),
                      rows.animate.to_edge(UP, buff=1.0).shift(RIGHT * 0.3))
            dots = T(r"\begin{bmatrix}\hat b_1\\\hat b_2\\\hat b_3\end{bmatrix} =",
                     r"\begin{bmatrix}\hat b_1\!\cdot\!\hat n_1 & \hat b_1\!\cdot\!\hat n_2 & \hat b_1\!\cdot\!\hat n_3\\"
                     r"\hat b_2\!\cdot\!\hat n_1 & \hat b_2\!\cdot\!\hat n_2 & \hat b_2\!\cdot\!\hat n_3\\"
                     r"\hat b_3\!\cdot\!\hat n_1 & \hat b_3\!\cdot\!\hat n_2 & \hat b_3\!\cdot\!\hat n_3\end{bmatrix}",
                     r"\begin{bmatrix}\hat n_1\\\hat n_2\\\hat n_3\end{bmatrix}").scale(0.62)
            dots.move_to(RIGHT * 2.9 + DOWN * 0.9)
            self.play(Write(dots), run_time=2.0)
            self.wait(1.0)
            cs = T(r"\begin{bmatrix}\hat b_1\\\hat b_2\\\hat b_3\end{bmatrix} =",
                   r"\begin{bmatrix}\cos\theta & \sin\theta & 0\\-\sin\theta & \cos\theta & 0\\0&0&1\end{bmatrix}",
                   r"\begin{bmatrix}\hat n_1\\\hat n_2\\\hat n_3\end{bmatrix}").scale(0.72)
            cs.move_to(dots)
            self.play(TransformMatchingTex(dots, cs), run_time=1.5)
            br = Brace(cs[1], DOWN, color=YELLOW)
            brl = T(r"C_{\mathcal{BN}}", color=YELLOW).next_to(br, DOWN, buff=0.1)
            name = Tx("direction cosine matrix", color=YELLOW).scale(0.6).next_to(brl, DOWN, buff=0.1)
            self.play(GrowFromCenter(br), Write(brl), FadeIn(name))
            self.hold()

        with self.voice("dcm_5"):
            m = cs[1]
            row = Rectangle(width=m.width * 0.9, height=m.height / 3.4, color=B_COL).move_to(m.get_top() + DOWN * m.height / 6)
            rowl = T(r"\hat b_1 \text{ in } \mathcal N \text{ components}", color=B_COL).scale(0.6)
            rowl.next_to(rows, DOWN, buff=0.3).align_to(rows, LEFT)
            self.play(Create(row), FadeIn(rowl))
            self.wait(2.5)
            col = Rectangle(width=m.width / 3.3, height=m.height * 0.95, color=Q_COL).move_to(m.get_left() + RIGHT * m.width / 5.2)
            coll = T(r"\hat n_1 \text{ in } \mathcal B \text{ components}", color=Q_COL).scale(0.6)
            coll.next_to(rowl, DOWN, buff=0.15, aligned_edge=LEFT)
            self.play(ReplacementTransform(row, col), FadeIn(coll))
            self.hold()

        with self.voice("dcm_6"):
            self.play(FadeOut(col), FadeOut(rowl), FadeOut(coll), FadeOut(rows))
            props = VGroup(
                Tx(r"rows: unit length, mutually perpendicular"),
                T(r"C_{\mathcal{BN}}\,C_{\mathcal{BN}}^{T} = I"),
                T(r"C_{\mathcal{NB}} = C_{\mathcal{BN}}^{-1} = C_{\mathcal{BN}}^{T}"),
            ).scale(0.75).arrange(DOWN, buff=0.35).move_to(RIGHT * 2.8 + UP * 1.9)
            props[0].scale(0.85).set_color(DIM)
            self.play(FadeIn(props[0]))
            self.wait(2.5)
            self.play(Write(props[1]))
            self.wait(1.5)
            self.play(Write(props[2]))
            hl = SurroundingRectangle(props[2], color=YELLOW)
            self.play(Create(hl), run_time=min(1.0, self.left()))
            self.hold()

        # ---- live demo: the arrow stays put, the frame turns
        with self.voice("dcm_7"):
            arc1.clear_updaters()
            arc1l.clear_updaters()
            self.play(FadeOut(VGroup(cs, br, brl, name, props, hl)), FadeOut(arc1), FadeOut(arc1l))
            rv = np.array([2.0, 1.1, 0])
            r_ar = Arrow(O, O + rv, buff=0, color=R_COL, stroke_width=6)
            r_l = T(r"\vec r", color=R_COL).scale(0.8).next_to(r_ar.get_end(), UR, buff=0.05)
            law = T(r"r_{(\mathcal B)} = C_{\mathcal{BN}}\, r_{(\mathcal N)}").scale(0.9).move_to(RIGHT * 2.8 + UP * 2.2)
            rn = live_column([lambda: rv[0], lambda: rv[1], lambda: 0.0], color=N_COL)
            rb = live_column([lambda: np.cos(th.get_value()) * rv[0] + np.sin(th.get_value()) * rv[1],
                              lambda: -np.sin(th.get_value()) * rv[0] + np.cos(th.get_value()) * rv[1],
                              lambda: 0.0], color=B_COL)
            rnl = T(r"r_{(\mathcal N)} =", color=N_COL).scale(0.8)
            rbl = T(r"r_{(\mathcal B)} =", color=B_COL).scale(0.8)
            gN = VGroup(rnl, rn).arrange(RIGHT)
            gB = VGroup(rbl, rb).arrange(RIGHT)
            VGroup(gN, gB).arrange(RIGHT, buff=0.8).next_to(law, DOWN, buff=0.7)
            self.play(GrowArrow(r_ar), FadeIn(r_l))
            self.play(Write(law))
            self.play(FadeIn(gN), FadeIn(gB))
            self.play(th.animate.set_value(np.radians(75)), run_time=2.5)
            self.play(th.animate.set_value(np.radians(-20)), run_time=3.0)
            self.play(th.animate.set_value(np.radians(32)), run_time=max(1.0, self.left() - 0.3))
        demo = VGroup(r_ar, r_l, law, gN, gB)

        with self.voice("dcm_8"):
            for m in (b1, b2, b1l, b2l):
                m.clear_updaters()
            self.play(FadeOut(demo), FadeOut(VGroup(n1, n2, n1l, n2l, out, outl)), FadeOut(b1), FadeOut(b2),
                      FadeOut(b1l), FadeOut(b2l))
            C = T(r"C = \begin{bmatrix}C_{11}&C_{12}&C_{13}\\C_{21}&C_{22}&C_{23}\\C_{31}&C_{32}&C_{33}\end{bmatrix}").shift(LEFT * 3 + UP * 0.3)
            nine = Tx(r"9 numbers", color=DIM).scale(0.7).next_to(C, DOWN, buff=0.4)
            c1 = T(r"\hat b_i\cdot\hat b_i = 1", r"\quad (3)").scale(0.8)
            c1b = T(r"C_{11}^2 + C_{12}^2 + C_{13}^2 = 1", color=DIM).scale(0.6)
            c2 = T(r"\hat b_i\cdot\hat b_j = 0", r"\quad (3)").scale(0.8)
            c2b = T(r"C_{11}C_{21} + C_{12}C_{22} + C_{13}C_{23} = 0", color=DIM).scale(0.6)
            res = T(r"9 - 6 = 3", r"\text{ degrees of freedom}").scale(0.9)
            res[0].set_color(YELLOW)
            col = VGroup(c1, c1b, c2, c2b, res).arrange(DOWN, buff=0.28).shift(RIGHT * 3 + UP * 0.3)
            res.shift(DOWN * 0.3)
            self.play(Write(C), FadeIn(nine))
            self.play(Write(c1), FadeIn(c1b))
            self.wait(1.5)
            self.play(Write(c2), FadeIn(c2b))
            self.wait(1.5)
            self.play(Write(res))
            self.hold()

        # ---- Endurance docking example (HW2 problem 4)
        with self.voice("dcm_9"):
            self.play(FadeOut(VGroup(C, nine, col)))
            ctr = LEFT * 3.3 + DOWN * 0.4
            ring = VGroup(Circle(radius=1.6, color=GREY_B, stroke_width=6))
            for k in range(12):
                a = TAU * k / 12
                pod = Square(0.32, fill_color=GREY_C, fill_opacity=1, stroke_color=GREY_A, stroke_width=1.5)
                pod.rotate(a).move_to(1.6 * np.array([np.cos(a), np.sin(a), 0]))
                ring.add(pod)
            for k in range(4):
                a = TAU * k / 4 + PI / 4
                ring.add(Line(ORIGIN, 1.45 * np.array([np.cos(a), np.sin(a), 0]), color=GREY_C, stroke_width=3))
            ring.add(Circle(radius=0.25, fill_color=GREY_D, fill_opacity=1, color=GREY_B))
            e1 = Arrow(ORIGIN, RIGHT * 2.3, buff=0, color=B_COL, stroke_width=5)
            e1l = T(r"\hat e_1", color=B_COL).scale(0.7).next_to(e1.get_end(), RIGHT, buff=0.05)
            port = Dot(RIGHT * 1.6, color=YELLOW, radius=0.08)
            station = VGroup(ring, e1, e1l, port).move_to(ctr)
            nx = DashedLine(ctr, ctr + RIGHT * 2.5, color=N_COL)
            nxl = T(r"\hat n_1", color=N_COL).scale(0.7).next_to(nx.get_end(), DOWN, buff=0.1)
            title = Tx(r"HW2, Problem 4: docking with the \emph{Endurance}", color=B_COL).scale(0.7).to_edge(UP, buff=0.3)
            self.play(FadeOut(hdr), FadeIn(title), FadeIn(station), Create(nx), FadeIn(nxl))
            w = T(r"\vec\omega^{\mathcal E/\mathcal C} = 0.65\,\hat n_3\ \text{rad/s}").scale(0.75)
            t1 = T(r"t_1 = 6\ \text{s}\ \Rightarrow\ \theta = 0.65 \times 6 = 3.9\ \text{rad}\ (223.5^\circ)").scale(0.75)
            VGroup(w, t1).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 2.9 + UP * 1.8)
            clock = ValueTracker(0)
            tl = always_redraw(lambda: T(r"t = %.1f\ \text{s}" % clock.get_value(), color=YELLOW).scale(0.7)
                               .move_to(ctr + DOWN * 2.5))
            self.play(Write(w))
            self.add(tl)
            last = [0.0]

            def spin(m):
                v = clock.get_value()
                m.rotate(0.65 * (v - last[0]), about_point=ctr)
                last[0] = v
            station.add_updater(spin)
            self.play(clock.animate.set_value(6.0), Write(t1), run_time=6.0, rate_func=linear)
            station.remove_updater(spin)
            mat = T(r"C_{\mathcal{EN}}(t_1) = C_3(3.9) = "
                    r"\begin{bmatrix}-0.726 & -0.688 & 0\\ 0.688 & -0.726 & 0\\ 0&0&1\end{bmatrix}").scale(0.7)
            mat.next_to(t1, DOWN, buff=0.6).align_to(t1, LEFT)
            self.play(Write(mat), run_time=2.0)
            self.play(Circumscribe(mat, color=YELLOW), run_time=min(1.5, self.left()))
            self.hold()
        self.play(*[FadeOut(m) for m in self.mobjects])
