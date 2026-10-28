"""Lesson 1: Vectors and reference frames."""
from lcommon import *  # noqa: F401,F403


class V1Concept(Lesson):
    def construct(self):
        with self.voice("v1_01"):
            card = title_card(self, 1, "Vectors and Reference Frames",
                              "turning an arrow into three numbers, and back again")
            self.hold()
        self.play(FadeOut(card))

        # ---- a vector is an arrow
        with self.voice("v1_02"):
            hdr = header("What is a vector?")
            self.play(FadeIn(hdr))
            o = np.array([-2.5, -1.5, 0])
            tip = o + np.array([4.0, 2.4, 0])
            r = Arrow(o, tip, buff=0, color=R_COL, stroke_width=7)
            rl = T(r"\vec r", color=R_COL).next_to(r.get_end(), UR, buff=0.1)
            self.play(GrowArrow(r), FadeIn(rl))
            mag = Brace(Line(o, tip), direction=rotate_vector(normalize(tip - o), -PI / 2), color=DIM)
            magl = Tx(r"magnitude $|\vec r|$ (its length)", color=DIM).scale(0.6).next_to(mag.get_center(), DR, buff=0.2)
            self.play(GrowFromCenter(mag), FadeIn(magl))
            dirl = Tx("direction: where it points", color=DIM).scale(0.6).next_to(tip, DR, buff=0.3)
            self.play(FadeIn(dirl))
            self.wait(1.5)
            note = Tx(r"The arrow exists on its own,\\no numbers needed.", color=YELLOW).scale(0.75).to_edge(DOWN, buff=0.5)
            grp = VGroup(r, rl)
            self.play(FadeOut(mag), FadeOut(magl), FadeOut(dirl))
            self.play(grp.animate.shift(LEFT * 1.0 + UP * 0.5), rate_func=there_and_back, run_time=2.0)
            self.play(Write(note))
            self.hold()
        self.play(FadeOut(VGroup(r, rl, note)))

        # ---- dot product
        O = np.array([-4.5, -1.8, 0])
        th = 38 * DEGREES
        a_vec = 3.6 * np.array([np.cos(th), np.sin(th), 0])
        b_vec = np.array([4.2, 0, 0])
        A = Arrow(O, O + a_vec, buff=0, color=R_COL, stroke_width=6)
        Bv = Arrow(O, O + b_vec, buff=0, color=B_COL, stroke_width=6)
        Al = T(r"\vec a", color=R_COL).next_to(A.get_end(), UP, buff=0.1)
        Bl = T(r"\vec b", color=B_COL).next_to(Bv.get_end(), DOWN, buff=0.1)
        arc = Arc(radius=0.9, start_angle=0, angle=th, arc_center=O, color=YELLOW)
        arcl = T(r"\theta", color=YELLOW).scale(0.8).move_to(O + 1.2 * np.array([np.cos(th / 2), np.sin(th / 2), 0]))
        with self.voice("v1_03"):
            self.play(Transform(hdr, header("Tool 1: the dot product")))
            self.play(GrowArrow(A), GrowArrow(Bv), FadeIn(Al), FadeIn(Bl))
            self.play(Create(arc), FadeIn(arcl))
            dot_def = T(r"\vec a\cdot\vec b", r"=", r"|\vec a|", r"\,|\vec b|", r"\cos\theta").scale(1.0)
            dot_def.move_to(RIGHT * 2.8 + UP * 2.0)
            self.play(Write(dot_def), run_time=2.0)
            self.hold()

        foot = O + np.array([a_vec[0], 0, 0])
        with self.voice("v1_04"):
            drop = DashedLine(O + a_vec, foot, color=DIM)
            ra = RightAngle(Line(foot, O), Line(foot, O + a_vec), length=0.2, color=DIM)
            shadow = Line(O, foot, color=YELLOW, stroke_width=10)
            shl = T(r"|\vec a|\cos\theta", color=YELLOW).scale(0.75).next_to(shadow, DOWN, buff=0.45)
            self.play(Create(drop), Create(ra))
            self.play(Create(shadow), run_time=1.2)
            self.play(Write(shl))
            l2 = T(r"\vec a\cdot\vec b = ", r"(|\vec a|\cos\theta)", r"\times|\vec b|").scale(0.85)
            l2[1].set_color(YELLOW)
            l2.next_to(dot_def, DOWN, buff=0.6)
            words = Tx(r"(shadow of $\vec a$ on $\vec b$) $\times$ (length of $\vec b$)", color=REASON).scale(0.6).next_to(l2, DOWN, buff=0.25)
            self.play(Write(l2))
            self.play(FadeIn(words))
            self.hold()

        with self.voice("v1_05"):
            unit = Arrow(O, O + RIGHT * 1.4, buff=0, color=B_COL, stroke_width=7)
            unitl = T(r"\hat b", color=B_COL).next_to(unit.get_end(), DOWN, buff=0.1)
            self.play(ReplacementTransform(Bv, unit), ReplacementTransform(Bl, unitl))
            ul = Tx(r"unit vector: $|\hat b| = 1$", color=B_COL).scale(0.65).next_to(unitl, DOWN, buff=0.2)
            self.play(FadeIn(ul))
            l3 = T(r"\vec a\cdot\hat b = |\vec a|\cos\theta", r"= \text{shadow of } \vec a \text{ along } \hat b").scale(0.8)
            l3.next_to(words, DOWN, buff=0.6)
            box = SurroundingRectangle(l3, color=YELLOW, buff=0.15)
            self.play(Write(l3), run_time=2.0)
            self.play(Create(box))
            self.hold()
        dotfig = VGroup(A, Al, unit, unitl, ul, arc, arcl, drop, ra, shadow, shl)
        self.play(FadeOut(VGroup(dotfig, l2, words, l3, box)), dot_def.animate.move_to(UP * 2.4))

        with self.voice("v1_06"):
            c1 = VGroup(T(r"\theta = 90^\circ"), T(r"\vec a\cdot\vec b = |\vec a||\vec b|\cos 90^\circ = 0", color=Q_COL),
                        Tx("perpendicular $\\Rightarrow$ dot product is zero", color=REASON).scale(0.75)).arrange(DOWN, buff=0.3)
            c2 = VGroup(T(r"\hat u\cdot\hat u"), T(r"= (1)(1)\cos 0^\circ = 1", color=Q_COL),
                        Tx("a unit vector dotted with itself is one", color=REASON).scale(0.75)).arrange(DOWN, buff=0.3)
            VGroup(c1, c2).scale(0.85).arrange(RIGHT, buff=1.5).move_to(DOWN * 0.3)
            p1 = VGroup(Arrow(ORIGIN, RIGHT * 1.3, buff=0, color=R_COL), Arrow(ORIGIN, UP * 1.3, buff=0, color=B_COL))
            p1.add(RightAngle(Line(ORIGIN, RIGHT), Line(ORIGIN, UP), length=0.2, color=DIM)).next_to(c1, UP, buff=0.4)
            self.play(FadeIn(p1), Write(c1[0]))
            self.play(Write(c1[1]))
            self.play(FadeIn(c1[2]))
            self.wait(1.0)
            self.play(Write(c2[0]))
            self.play(Write(c2[1]))
            self.play(FadeIn(c2[2]))
            self.hold()
        self.play(FadeOut(VGroup(c1, c2, p1, dot_def)))

        # ---- cross product
        with self.voice("v1_07"):
            self.play(Transform(hdr, header("Tool 2: the cross product")))
            O2 = np.array([-4.8, -2.2, 0])
            a2 = np.array([3.4, 0.4, 0])
            b2 = np.array([1.3, 2.6, 0])
            A2 = Arrow(O2, O2 + a2, buff=0, color=R_COL, stroke_width=6)
            B2 = Arrow(O2, O2 + b2, buff=0, color=B_COL, stroke_width=6)
            A2l = T(r"\vec a", color=R_COL).next_to(A2.get_end(), DOWN, buff=0.1)
            B2l = T(r"\vec b", color=B_COL).next_to(B2.get_end(), LEFT, buff=0.1)
            par = Polygon(O2, O2 + a2, O2 + a2 + b2, O2 + b2, stroke_width=0, fill_color=V_COL, fill_opacity=0.3)
            self.play(GrowArrow(A2), GrowArrow(B2), FadeIn(A2l), FadeIn(B2l))
            cr = T(r"|\vec a\times\vec b|", r"=", r"|\vec a|\,|\vec b|\sin\theta").move_to(RIGHT * 2.8 + UP * 2.0)
            self.play(Write(cr), run_time=1.8)
            self.play(FadeIn(par))
            # height of the parallelogram
            a_hat = normalize(a2)
            hfoot = O2 + a_hat * np.dot(b2, a_hat)
            hline = DashedLine(O2 + b2, hfoot, color=YELLOW)
            hl = T(r"|\vec b|\sin\theta", color=YELLOW).scale(0.65).next_to(hline, RIGHT, buff=0.1)
            self.play(Create(hline), FadeIn(hl))
            area = Tx(r"= base $\times$ height = area of the parallelogram", color=V_COL).scale(0.65).next_to(cr, DOWN, buff=0.4)
            self.play(Write(area))
            self.hold()
        flat2d = VGroup(A2, B2, A2l, B2l, par, hline, hl)

        # 3D view for the direction
        cam = Cam(phi=65, theta=-60, scale=0.95, center=(-3.0, -1.6))
        D = Draw(cam)
        self.add(*cam.trackers())
        a3, b3 = np.array([2.2, 0.0, 0]), np.array([0.6, 2.0, 0])
        c3 = np.cross(a3, b3) / 2.2
        with self.voice("v1_08"):
            self.play(FadeOut(flat2d))
            ga = D.arrow(ORIGIN, a3, R_COL, 6, k=0)
            gb = D.arrow(ORIGIN, b3, B_COL, 6, k=0)
            gc = D.arrow(ORIGIN, c3, V_COL, 6, k=0)
            gcn = D.arrow(ORIGIN, -c3, V_COL, 4, k=0)
            pl = D.polygon([ORIGIN, a3, a3 + b3, b3], V_COL, 0.25)
            la = D.label(r"\vec a", a3 * 1.15, R_COL)
            lb = D.label(r"\vec b", b3 * 1.15, B_COL)
            lc = D.label(r"\vec a\times\vec b", c3 * 1.15 + np.array([0, 0, 0.2]), V_COL)
            lcn = D.label(r"\vec b\times\vec a", -c3 * 1.15, V_COL)
            self.add(pl, ga, gb, gc, gcn, la, lb, lc, lcn)
            self.play(*grow(ga, gb), *show(la, lb))
            perp = Tx(r"perpendicular to both $\vec a$ and $\vec b$", color=V_COL).scale(0.65).next_to(area, DOWN, buff=0.45)
            self.play(*grow(gc), *show(lc), FadeIn(perp), run_time=1.5)
            rh = Tx(r"right-hand rule: fingers along $\vec a$,\\curl toward $\vec b$, thumb gives $\vec a\times\vec b$",
                    color=WHITE).scale(0.65).next_to(perp, DOWN, buff=0.4)
            self.play(FadeIn(rh))
            cam.start_spin(self, 0.12)
            self.wait(2.5)
            anti = T(r"\vec b\times\vec a = -\,\vec a\times\vec b", color=YELLOW).scale(0.8).next_to(rh, DOWN, buff=0.4)
            self.play(*grow(gcn), *show(lcn), Write(anti))
            self.hold()
        cam.stop_spin()
        g3 = flat(pl, ga, gb, gc, gcn, la, lb, lc, lcn)
        self.play(*hide(*g3), FadeOut(VGroup(cr, area, perp, rh, anti)))
        self.remove(*g3)

        # ---- reference frame
        cam2 = Cam(phi=70, theta=28, scale=0.95, center=(-4.4, -1.2))
        D2 = Draw(cam2)
        self.add(*cam2.trackers())
        L = 2.5
        nf, nl = D2.frame(np.eye(3), N_COL, L, [r"\hat n_1", r"\hat n_2", r"\hat n_3"])
        o = D2.label("O", np.array([0.35, -0.35, -0.25]), WHITE, 0.6)
        with self.voice("v1_09"):
            self.play(Transform(hdr, header("A reference frame")))
            self.add(nf, nl, o)
            self.play(*show(o))
            self.play(LaggedStart(*grow(*nf), lag_ratio=0.35), run_time=2.0)
            self.play(*show(*nl))
            fdef = T(r"\mathcal N = \{\,O,\ \hat n_1,\ \hat n_2,\ \hat n_3\,\}").scale(0.9).move_to(RIGHT * 2.8 + UP * 2.4)
            self.play(Write(fdef))
            self.hold()

        with self.voice("v1_10"):
            bd = Board(self, left=0.4, top=1.7, scale=0.75)
            bd.line(r"\hat n_i\cdot\hat n_i = 1", reason="unit length")
            bd.line(r"\hat n_i\cdot\hat n_j = 0\quad (i\neq j)", reason="perpendicular")
            self.wait(1.0)
            bd.line(r"\hat n_1\times\hat n_2 = \hat n_3", reason="right-handed")
            bd.line(r"\hat n_2\times\hat n_3 = \hat n_1", rt=0.9)
            bd.line(r"\hat n_3\times\hat n_1 = \hat n_2", rt=0.9)
            self.hold()

        rv = np.array([1.5, 2.0, 1.6])
        r3 = D2.arrow(ORIGIN, rv, R_COL, 6, k=0)
        rl3 = D2.label(r"\vec r", rv * 1.12, R_COL, 0.9)
        with self.voice("v1_11"):
            bd.clear()
            self.add(r3, rl3)
            self.play(*grow(r3), *show(rl3))
            claim = T(r"\vec r = x\,\hat n_1 + y\,\hat n_2 + z\,\hat n_3").scale(0.85).move_to(RIGHT * 3.0 + UP * 1.5)
            self.play(Write(claim), run_time=2.0)
            q = T(r"x,\ y,\ z = \ ?", color=YELLOW).scale(0.85).next_to(claim, DOWN, buff=0.4)
            self.play(FadeIn(q))
            self.hold()

        with self.voice("v1_12"):
            self.play(FadeOut(q), FadeOut(fdef), claim.animate.move_to(RIGHT * 2.9 + UP * 2.6))
            bd = Board(self, left=-1.6, top=1.9, scale=0.8, buff=0.42)
            bd.line(r"\vec r\cdot\hat n_1 = (x\,\hat n_1 + y\,\hat n_2 + z\,\hat n_3)\cdot\hat n_1",
                    reason="dot both sides with $\\hat n_1$", below=True)
            bd.line(r"= x\,(\hat n_1\cdot\hat n_1) + y\,(\hat n_2\cdot\hat n_1) + z\,(\hat n_3\cdot\hat n_1)",
                    reason="the dot product distributes over the sum", indent=0.6, below=True)
            self.hold()

        with self.voice("v1_13"):
            l3 = bd.line(r"= x\,(1)", r"+ y\,(0)", r"+ z\,(0)", reason="frame rules", indent=0.6)
            self.play(l3[1].animate.set_opacity(0.35), l3[2].animate.set_opacity(0.35))
            l4 = bd.line(r"x = \vec r\cdot\hat n_1", color=YELLOW, indent=0.6)
            bd.box(l4)
            self.hold()

        x, y, z = rv
        foot = np.array([x, y, 0])
        with self.voice("v1_14"):
            l5 = bd.line(r"y = \vec r\cdot\hat n_2,\qquad z = \vec r\cdot\hat n_3", color=YELLOW, indent=0.6, reason="same steps")
            sh = [D2.line(ORIGIN, [x, 0, 0], YELLOW, 9, k=0), D2.line(ORIGIN, [0, y, 0], YELLOW, 9, k=0),
                  D2.line(ORIGIN, [0, 0, z], YELLOW, 9, k=0)]
            dl = [D2.line(rv, foot, DIM, 2, dashed=True, k=0), D2.line(foot, [x, 0, 0], DIM, 2, dashed=True, k=0),
                  D2.line(foot, [0, y, 0], DIM, 2, dashed=True, k=0), D2.line(rv, [0, 0, z], DIM, 2, dashed=True, k=0)]
            self.add(*sh, *dl, r3)
            self.play(*grow(*dl), run_time=1.0)
            self.play(LaggedStart(*grow(*sh), lag_ratio=0.4), run_time=2.0)
            shadow = Tx("each component = a shadow on one axis", color=YELLOW).scale(0.65).to_edge(DOWN, buff=0.4).shift(RIGHT * 2.5)
            self.play(FadeIn(shadow))
            self.hold()

        with self.voice("v1_15"):
            bd.clear()
            self.play(FadeOut(shadow), FadeOut(claim))
            col = T(r"r_{(\mathcal N)}", r"= \begin{bmatrix} x\\ y\\ z\end{bmatrix} = "
                    r"\begin{bmatrix} \vec r\cdot\hat n_1\\ \vec r\cdot\hat n_2\\ \vec r\cdot\hat n_3\end{bmatrix}").scale(0.85)
            col.move_to(RIGHT * 2.9 + UP * 1.2)
            self.play(Write(col), run_time=2.0)
            sub = SurroundingRectangle(col[0], color=YELLOW, buff=0.08)
            subl = Tx(r"``$\vec r$ expressed in frame $\mathcal N$''", color=YELLOW).scale(0.6).next_to(col, DOWN, buff=0.35)
            self.play(Create(sub), FadeIn(subl))
            warn = Tx(r"arrow $\vec r$ = the vector\\column $r_{(\mathcal N)}$ = one description of it",
                      color=REASON).scale(0.65).next_to(subl, DOWN, buff=0.45)
            self.play(FadeIn(warn))
            self.hold()
        frame_stuff = flat(nf, nl, o, r3, rl3, *sh, *dl)
        self.play(*hide(*frame_stuff), FadeOut(VGroup(col, sub, subl, warn)))
        self.remove(*frame_stuff)

        # ---- dot product in components
        with self.voice("v1_16"):
            self.play(Transform(hdr, header("Dot product in components")))
            bd = Board(self, left=-6.3, top=2.4, scale=0.72, buff=0.4)
            bd.line(r"\vec a\cdot\vec b = (a_1\hat n_1 + a_2\hat n_2 + a_3\hat n_3)\cdot(b_1\hat n_1 + b_2\hat n_2 + b_3\hat n_3)")
            grid = VGroup()
            for i in range(1, 4):
                row = VGroup()
                for j in range(1, 4):
                    t = T(r"a_%d b_%d(\hat n_%d\cdot\hat n_%d)" % (i, j, i, j)).scale(0.6)
                    if i != j:
                        t.set_opacity(0.3)
                    row.add(t)
                row.arrange(RIGHT, buff=0.6)
                grid.add(row)
            grid.arrange(DOWN, buff=0.25).next_to(bd.lines[-1], DOWN, buff=0.45).align_to(bd.lines[-1], LEFT).shift(RIGHT * 0.6)
            for r in grid:
                self.play(FadeIn(r), run_time=0.7)
            gl = Tx(r"faded terms vanish: $\hat n_i\cdot\hat n_j = 0$ for $i\neq j$", color=REASON).scale(0.55).next_to(grid, DOWN, buff=0.2).align_to(grid, LEFT)
            self.play(FadeIn(gl))
            res = T(r"\vec a\cdot\vec b = a_1 b_1 + a_2 b_2 + a_3 b_3 = a_{(\mathcal N)}^{T}\, b_{(\mathcal N)}", color=YELLOW).scale(0.8)
            res.next_to(gl, DOWN, buff=0.45).align_to(bd.lines[-1], LEFT)
            self.play(Write(res), run_time=2.0)
            self.play(Create(SurroundingRectangle(res, color=YELLOW, buff=0.12)))
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not hdr and not isinstance(m, ValueTracker)])))

        with self.voice("v1_17"):
            self.play(Transform(hdr, header("Cross product in components")))
            det = T(r"\vec a\times\vec b = \begin{vmatrix}\hat n_1 & \hat n_2 & \hat n_3\\ a_1 & a_2 & a_3\\ b_1 & b_2 & b_3\end{vmatrix}").scale(0.85)
            det.move_to(UP * 1.6)
            self.play(Write(det), run_time=2.0)
            exp = T(r"= (a_2 b_3 - a_3 b_2)\,\hat n_1", r"+ (a_3 b_1 - a_1 b_3)\,\hat n_2", r"+ (a_1 b_2 - a_2 b_1)\,\hat n_3").scale(0.75)
            exp.next_to(det, DOWN, buff=0.6)
            for part in exp:
                self.play(Write(part), run_time=1.3)
            self.hold()

        with self.voice("v1_18"):
            self.play(FadeOut(det), exp.animate.to_edge(UP, buff=1.0))
            til = T(r"\tilde a = \begin{bmatrix} 0 & -a_3 & a_2\\ a_3 & 0 & -a_1\\ -a_2 & a_1 & 0\end{bmatrix}").scale(0.8)
            prod = T(r"(\vec a\times\vec b)_{(\mathcal N)} = \tilde a\, b_{(\mathcal N)} = "
                     r"\begin{bmatrix} a_2 b_3 - a_3 b_2\\ a_3 b_1 - a_1 b_3\\ a_1 b_2 - a_2 b_1\end{bmatrix}").scale(0.8)
            VGroup(til, prod).arrange(DOWN, buff=0.6).next_to(exp, DOWN, buff=0.6)
            self.play(Write(til), run_time=2.0)
            zl = Tx("zeros on the diagonal; $a$'s entries with alternating signs", color=REASON).scale(0.55).next_to(til, RIGHT, buff=0.4)
            if zl.get_right()[0] > 6.9:
                zl.scale_to_fit_width(6.9 - til.get_right()[0] - 0.5).next_to(til, RIGHT, buff=0.4)
            self.play(FadeIn(zl))
            self.play(Write(prod), run_time=2.0)
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))


class V1Examples(Lesson):
    def construct(self):
        # ---- Example 1: length and angle
        with self.voice("v1_19"):
            hdr = header("Example 1: length and angle")
            self.play(FadeIn(hdr))
            ax = NumberPlane(x_range=[-0.5, 4.5, 1], y_range=[-0.5, 4.5, 1], x_length=3.6, y_length=3.6,
                             background_line_style={"stroke_color": "#2A2F3A", "stroke_width": 1}).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
            n1 = Arrow(ax.c2p(0, 0), ax.c2p(1, 0), buff=0, color=N_COL)
            n2 = Arrow(ax.c2p(0, 0), ax.c2p(0, 1), buff=0, color=N_COL)
            n1l = T(r"\hat n_1", color=N_COL).scale(0.6).next_to(n1, DOWN, buff=0.05)
            n2l = T(r"\hat n_2", color=N_COL).scale(0.6).next_to(n2, LEFT, buff=0.05)
            r = Arrow(ax.c2p(0, 0), ax.c2p(3, 4), buff=0, color=R_COL, stroke_width=6)
            rl = T(r"\vec r", color=R_COL).next_to(r.get_end(), UP, buff=0.1)
            self.play(FadeIn(ax), GrowArrow(n1), GrowArrow(n2), FadeIn(n1l), FadeIn(n2l))
            self.play(GrowArrow(r), FadeIn(rl))
            given = T(r"r_{(\mathcal N)} = \begin{bmatrix}3\\4\\0\end{bmatrix}").scale(0.8).move_to(RIGHT * 1.2 + UP * 2.3)
            ask = Tx(r"Find $|\vec r|$, and the angle $\alpha$\\between $\vec r$ and $\hat n_1$.", color=YELLOW).scale(0.65)
            ask.next_to(given, RIGHT, buff=0.5)
            self.play(Write(given), FadeIn(ask))
            self.hold()

        with self.voice("v1_20"):
            bd = Board(self, left=-1.6, top=1.2, scale=0.75)
            bd.line(r"|\vec r|^2 = \vec r\cdot\vec r = 3^2 + 4^2 + 0^2", reason="dot product in components")
            bd.line(r"= 9 + 16 + 0 = 25", indent=1.0)
            l = bd.line(r"|\vec r| = \sqrt{25} = 5", color=YELLOW, indent=1.0)
            bd.box(l)
            self.hold()

        with self.voice("v1_21"):
            alpha = np.arctan2(4, 3)
            arc = Arc(radius=0.55, start_angle=0, angle=alpha, arc_center=ax.c2p(0, 0), color=Q_COL)
            al = T(r"\alpha", color=Q_COL).scale(0.7).move_to(ax.c2p(0, 0) + 0.8 * np.array([np.cos(alpha / 2), np.sin(alpha / 2), 0]))
            self.play(Create(arc), FadeIn(al))
            bd.line(r"\vec r\cdot\hat n_1 = |\vec r|\,|\hat n_1|\cos\alpha", reason="definition of the dot product")
            bd.line(r"3 = (5)(1)\cos\alpha", reason="left side is the first component", indent=1.0)
            bd.line(r"\cos\alpha = \tfrac{3}{5} = 0.6", indent=1.0)
            l = bd.line(r"\alpha = \cos^{-1}(0.6) \approx 53.1^\circ", color=YELLOW, indent=1.0)
            bd.box(l)
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not hdr])))

        # ---- Example 2: dot and cross
        with self.voice("v1_22"):
            self.play(Transform(hdr, header("Example 2: dot and cross products")))
            given = T(r"a_{(\mathcal N)} = \begin{bmatrix}1\\2\\0\end{bmatrix},\qquad b_{(\mathcal N)} = \begin{bmatrix}0\\1\\3\end{bmatrix}").scale(0.8)
            given.to_edge(UP, buff=0.9)
            self.play(Write(given))
            bd = Board(self, left=-6.0, top=1.1, scale=0.75)
            bd.line(r"\vec a\cdot\vec b = a_1 b_1 + a_2 b_2 + a_3 b_3")
            bd.line(r"= (1)(0) + (2)(1) + (0)(3)", indent=1.0)
            l = bd.line(r"= 2", color=YELLOW, indent=1.0)
            bd.box(l)
            self.hold()

        with self.voice("v1_23"):
            bd.clear()
            bd = Board(self, left=-6.0, top=1.1, scale=0.75)
            bd.line(r"(\vec a\times\vec b)_1 = a_2 b_3 - a_3 b_2 = (2)(3) - (0)(1) = 6", rt=2.0)
            bd.line(r"(\vec a\times\vec b)_2 = a_3 b_1 - a_1 b_3 = (0)(0) - (1)(3) = -3", rt=2.0)
            bd.line(r"(\vec a\times\vec b)_3 = a_1 b_2 - a_2 b_1 = (1)(1) - (2)(0) = 1", rt=2.0)
            l = bd.line(r"(\vec a\times\vec b)_{(\mathcal N)} = \begin{bmatrix}6\\-3\\1\end{bmatrix}", color=YELLOW)
            bd.box(l)
            self.hold()

        with self.voice("v1_24"):
            chk = VGroup(
                T(r"(\vec a\times\vec b)\cdot\vec a = (6)(1) + (-3)(2) + (1)(0) = 0\ \checkmark", color=Q_COL),
                T(r"(\vec a\times\vec b)\cdot\vec b = (6)(0) + (-3)(1) + (1)(3) = 0\ \checkmark", color=Q_COL),
            ).scale(0.72).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(l, RIGHT, buff=0.8).shift(DOWN * 0.25)
            why = Tx("check: the answer must be perpendicular to both", color=REASON).scale(0.6).next_to(chk, DOWN, buff=0.3).align_to(chk, LEFT)
            self.play(FadeIn(why))
            self.play(Write(chk[0]), run_time=2.0)
            self.play(Write(chk[1]), run_time=2.0)
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not hdr])))

        # ---- Example 3: same arrow, two frames
        cam = Cam(phi=70, theta=28, scale=1.15, center=(-2.6, -0.9))
        D = Draw(cam)
        self.add(*cam.trackers())
        L = 2.5
        rv = np.array([1.6, 2.2, 1.7])
        Bm = euler321(np.radians(40), np.radians(-25), np.radians(30))
        with self.voice("v1_25"):
            self.play(Transform(hdr, header("Example 3: same arrow, two frames")))
            nf, nl = D.frame(np.eye(3), N_COL, L, [r"\hat n_1", r"\hat n_2", r"\hat n_3"])
            bf, bl = D.frame(Bm, B_COL, L, [r"\hat b_1", r"\hat b_2", r"\hat b_3"])
            r3 = D.arrow(ORIGIN, rv, R_COL, 6, k=0)
            rl = D.label(r"\vec r", rv * 1.1, R_COL, 0.9)
            self.add(nf, nl, bf, bl, r3, rl)
            self.play(*grow(*nf, r3), *show(*nl, rl), run_time=1.5)
            cn = T(r"r_{(\mathcal N)} = \begin{bmatrix}1.60\\2.20\\1.70\end{bmatrix}", color=N_COL).scale(0.75)
            cn.move_to(RIGHT * 2.2 + UP * 1.2)
            self.play(Write(cn))
            self.play(*grow(*bf), *show(*bl), run_time=1.5)
            rb = Bm @ rv
            cb = T(r"r_{(\mathcal B)} = \begin{bmatrix}%.2f\\%.2f\\%.2f\end{bmatrix}" % tuple(rb), color=B_COL).scale(0.75)
            cb.next_to(cn, RIGHT, buff=0.8)
            sh = []
            for i in range(3):
                q = rb[i] * Bm[i]
                sh += [D.line(ORIGIN, q, B_COL, 9, k=0), D.line(rv, q, B_COL, 2, dashed=True, k=0)]
            self.add(*sh, r3)
            self.play(*grow(*sh), run_time=1.5)
            self.play(Write(cb))
            nxt = Tx(r"How do we get from one column to the other?\\Next lesson: the direction cosine matrix.", color=YELLOW).scale(0.7)
            nxt.next_to(VGroup(cn, cb), DOWN, buff=0.8).to_edge(RIGHT, buff=0.4)
            cam.start_spin(self, 0.05)
            self.play(FadeIn(nxt))
            self.hold()
        cam.stop_spin()
        stuff = flat(nf, nl, bf, bl, r3, rl, *sh)
        self.play(*hide(*stuff), FadeOut(VGroup(cn, cb, nxt, hdr)))
        self.remove(*stuff)

        with self.voice("v1_26"):
            h, rows = recap(self, [
                r"A vector is an arrow: a length and a direction.",
                r"A frame: an origin plus three perpendicular, right-handed unit vectors.",
                r"Each component is a dot product with an axis: $x = \vec r\cdot\hat n_1$.",
                r"Dot product: $a_1b_1 + a_2b_2 + a_3b_3$.\quad Cross product: the determinant / $\tilde a\,b$.",
                r"The column $r_{(\mathcal N)}$ depends on the frame you choose.",
            ])
            for rrow in rows:
                self.play(FadeIn(rrow, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 5 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
