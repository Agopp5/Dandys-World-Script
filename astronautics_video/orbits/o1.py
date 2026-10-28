"""Part 1: Kepler's three laws, the polar frame, and why the force is central."""
from ocommon import *  # noqa: F401,F403

A, ECC = 2.6, 0.6
C = A * ECC
P = A * (1 - ECC ** 2)
B = A * np.sqrt(1 - ECC ** 2)


class O1Concept(OLesson):
    def construct(self):
        with self.voice("o1_01"):
            t = o_title(self, 1, "Kepler's Laws", "from Tycho's data to a central force")
            self.hold()
        self.play(FadeOut(t))

        # ---------------------------------------------------------- first law
        orb = Orb(focus=(-1.6, -0.35), k=1.0)
        F2 = orb.P(-2 * C, 0)
        F1 = orb.P(0, 0)
        ctr = orb.P(-C, 0)

        def ell(u):  # point on the ellipse by its centre angle
            return ctr + np.array([A * np.cos(u), B * np.sin(u), 0])
        with self.voice("o1_02"):
            hdr = header("Kepler's first law (1609)")
            self.play(FadeIn(hdr))
            txt = Tx(r"The orbit of a planet is an \textbf{ellipse},\\with the Sun at one \textbf{focus}.").scale(0.7)
            txt.move_to([3.9, 2.2, 0])
            self.play(FadeIn(txt))
            pins = VGroup(Dot(F1, color=WHITE, radius=0.06), Dot(F2, color=WHITE, radius=0.06))
            self.play(FadeIn(pins))
            u = ValueTracker(0.01)
            pen = always_redraw(lambda: Dot(ell(u.get_value()), color=YELLOW, radius=0.07))
            s1 = always_redraw(lambda: Line(F1, ell(u.get_value()), color=Q_COL, stroke_width=3))
            s2 = always_redraw(lambda: Line(F2, ell(u.get_value()), color=P_COL, stroke_width=3))
            trace = always_redraw(lambda: ParametricFunction(ell, t_range=[0, u.get_value()], color=ORB, stroke_width=3))
            self.add(trace, s1, s2, pen)
            rule = T(r"r_1 + r_2 = 2a = \text{const}", color=WHITE).scale(0.75).move_to([3.9, 0.9, 0])
            rule[0][0:2].set_color(Q_COL)
            rule[0][3:5].set_color(P_COL)
            self.play(u.animate.set_value(TAU), FadeIn(rule, run_time=1.5), run_time=max(3, min(9, self.left() - 1)), rate_func=linear)
            self.hold()

        ellipse = orb.conic(P, ECC)
        with self.voice("o1_03"):
            self.remove(trace, pen)
            self.add(ellipse)
            self.play(FadeOut(VGroup(s1, s2)))
            s = sun(F1)
            self.play(FadeOut(pins[0]), FadeIn(s))
            vac = Tx("vacant focus", color=DIM).scale(0.55).next_to(F2, DOWN, buff=0.2)
            sl = Tx("Sun", color=SUN).scale(0.55).next_to(F1, DOWN, buff=0.3)
            self.play(FadeIn(vac), FadeIn(sl), pins[1].animate.set_color(DIM))
            cdot = Dot(ctr, color=DIM, radius=0.04)
            cl = Tx("center", color=DIM).scale(0.45).next_to(ctr, UP, buff=0.12)
            self.play(FadeIn(cdot), FadeIn(cl))
            near = Dot(orb.P(A - C, 0), color=Q_COL)
            far = Dot(orb.P(-A - C, 0), color=P_COL)
            nl = Tx("closest", color=Q_COL).scale(0.5).next_to(near, RIGHT, buff=0.12)
            fl = Tx("farthest", color=P_COL).scale(0.5).next_to(far, LEFT, buff=0.12)
            self.play(FadeIn(near), FadeIn(far), FadeIn(nl), FadeIn(fl))
            self.hold()
        self.play(FadeOut(VGroup(txt, rule, cdot, cl, nl, fl, near, far, vac)))

        # ---------------------------------------------------------- second law
        with self.voice("o1_04"):
            self.play(Transform(hdr, header("Kepler's second law (1609)")))
            txt = Tx(r"The Sun--planet line sweeps\\\textbf{equal areas in equal times}.").scale(0.7).move_to([3.9, 2.2, 0])
            self.play(FadeIn(txt))
            Mt = ValueTracker(-0.35)
            pl = always_redraw(lambda: planet(orb.at(P, ECC, theta_from_M(Mt.get_value(), ECC))))
            rad = always_redraw(lambda: Line(F1, orb.at(P, ECC, theta_from_M(Mt.get_value(), ECC)), color=WHITE, stroke_width=2))
            self.add(rad, pl)
            dM = 0.7

            def wedge(M0, color):
                th0, th1 = theta_from_M(M0, ECC), theta_from_M(M0 + dM, ECC)
                return orb.sector(P, ECC, th0, th1, color=color, opacity=0.45)
            w1 = wedge(-0.35, AREA)
            self.play(Mt.animate.set_value(-0.35 + dM), FadeIn(w1, run_time=2.5), run_time=2.5, rate_func=linear)
            self.play(Mt.animate.set_value(PI - 0.35), run_time=2.5, rate_func=linear)
            w2 = wedge(PI - 0.35, V_COL)
            self.play(Mt.animate.set_value(PI - 0.35 + dM), FadeIn(w2, run_time=2.5), run_time=2.5, rate_func=linear)
            eq = T(r"\text{Area}_1 = \text{Area}_2", color=WHITE).scale(0.75).move_to([3.9, 0.9, 0])
            eq[0][0:5].set_color(AREA)
            eq[0][6:].set_color(V_COL)
            self.play(Write(eq))
            fast = Tx("fast: short, wide", color=AREA).scale(0.5).next_to(w1, RIGHT, buff=0.15)
            slow = Tx("slow: long, thin", color=V_COL).scale(0.5).next_to(w2, UP, buff=0.1).shift(LEFT * 0.4)
            self.play(FadeIn(fast), FadeIn(slow))
            self.play(Mt.animate.set_value(TAU - 0.35), run_time=max(0.5, min(5, self.left() - 0.5)), rate_func=linear)
            self.hold()
        self.play(FadeOut(VGroup(txt, eq, fast, slow, w1, w2, rad, pl, ellipse, s, sl, pins[1])))

        # ---------------------------------------------------------- third law
        with self.voice("o1_05"):
            self.play(Transform(hdr, header("Kepler's third law (1619)")))
            txt = Tx(r"$T^2 \propto a^3$\quad (period squared $\propto$ mean distance cubed)").scale(0.7).to_edge(UP, buff=1.0)
            self.play(FadeIn(txt))
            ax = Axes(x_range=[-0.6, 1.2, 0.5], y_range=[-0.9, 1.7, 0.5], x_length=6.5, y_length=4.6,
                      axis_config={"color": DIM, "include_ticks": False}).shift(DOWN * 0.55 + LEFT * 0.8)
            xl = T(r"\log a", color=DIM).scale(0.6).next_to(ax.x_axis, DOWN, buff=0.15).align_to(ax.x_axis, RIGHT)
            yl = T(r"\log T", color=DIM).scale(0.6).next_to(ax.y_axis, LEFT, buff=0.15).align_to(ax.y_axis, UP)
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            data = [("Mercury", 0.387, 0.241), ("Venus", 0.723, 0.615), ("Earth", 1.0, 1.0),
                    ("Mars", 1.524, 1.881), ("Jupiter", 5.203, 11.86), ("Saturn", 9.537, 29.46)]
            dots = VGroup()
            for name, a, T_ in data:
                d = Dot(ax.c2p(np.log10(a), np.log10(T_)), color=YELLOW, radius=0.07)
                lb = Tx(name, color=WHITE).scale(0.42).next_to(d, RIGHT, buff=0.12)
                dots.add(VGroup(d, lb))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.3), run_time=2.5)
            ln = ax.plot(lambda x: 1.5 * x, x_range=[-0.55, 1.12], color=B_COL)
            sl = T(r"\text{slope} = \tfrac{3}{2}", color=B_COL).scale(0.65).move_to(ax.c2p(0.25, 1.15))
            self.play(Create(ln), FadeIn(sl), run_time=1.5)
            self.hold()
        self.play(FadeOut(VGroup(ax, xl, yl, dots, ln, sl, txt)))

        # ---------------------------------------------------------- polar frame
        with self.voice("o1_06"):
            self.play(Transform(hdr, header("Newton's question: why?")))
            q = Tx(r"Kepler: \emph{how} planets move.\\[4pt] Newton (1643--1727): \emph{why}.").scale(0.8)
            self.play(FadeIn(q))
            tool = Tx(r"Tool: polar coordinates, and a frame that rides with the planet", color=B_COL).scale(0.65).next_to(q, DOWN, buff=0.6)
            self.play(FadeIn(tool))
            self.hold()
        self.play(FadeOut(VGroup(q, tool)))

        orb = Orb(focus=(-2.2, -0.6), k=0.85)
        ellipse = orb.conic(P, ECC).set_stroke(opacity=0.5)
        sn = sun(orb.f)
        th = ValueTracker(1.05)

        def pos():
            return orb.at(P, ECC, th.get_value())

        def er():
            return orb.unit(th.get_value())

        def et():
            return orb.unit(th.get_value() + PI / 2)
        L = 1.1
        rvec = always_redraw(lambda: Arrow(orb.f, pos(), buff=0, color=WHITE, stroke_width=4, tip_length=0.2))
        a_er = always_redraw(lambda: Arrow(pos(), pos() + L * er(), buff=0, color=ER_COL, stroke_width=5, tip_length=0.18))
        a_et = always_redraw(lambda: Arrow(pos(), pos() + L * et(), buff=0, color=ET_COL, stroke_width=5, tip_length=0.18))
        l_er = always_redraw(lambda: T(r"\hat e_r", color=ER_COL).scale(0.6).move_to(pos() + (L + 0.3) * er()))
        l_et = always_redraw(lambda: T(r"\hat e_\theta", color=ET_COL).scale(0.6).move_to(pos() + (L + 0.3) * et()))
        e3 = always_redraw(lambda: VGroup(Circle(radius=0.11, color=H_COL, stroke_width=3).move_to(pos() - 0.35 * er() - 0.35 * et()),
                                          Dot(pos() - 0.35 * er() - 0.35 * et(), radius=0.035, color=H_COL)))
        l_e3 = always_redraw(lambda: T(r"\hat e_3", color=H_COL).scale(0.55).next_to(e3, DOWN, buff=0.08))
        pl = always_redraw(lambda: planet(pos()))
        with self.voice("o1_07"):
            self.play(Transform(hdr, header("A frame that rides with the planet")))
            self.play(FadeIn(sn), Create(ellipse))
            self.play(GrowArrow(rvec), FadeIn(pl))
            self.play(FadeIn(a_er), FadeIn(l_er))
            self.play(FadeIn(a_et), FadeIn(l_et))
            self.play(FadeIn(e3), FadeIn(l_e3))
            bd = Board(self, left=1.2, top=2.6, scale=0.8)
            bd.line(r"\vec r = r\,\hat e_r", color=WHITE, reason="$r = |\\vec r|$, the distance")
            self.hold()

        ang = always_redraw(lambda: Arc(radius=0.6, start_angle=0, angle=th.get_value(), arc_center=orb.f, color=YELLOW))
        ang_l = always_redraw(lambda: T(r"\theta", color=YELLOW).scale(0.6).move_to(orb.f + 0.85 * orb.unit(th.get_value() / 2)))
        axis = DashedLine(orb.f, orb.f + RIGHT * 2.2, color=DIM)
        with self.voice("o1_08"):
            self.play(Create(axis), FadeIn(ang), FadeIn(ang_l))
            self.play(th.animate.set_value(2.3), run_time=4, rate_func=there_and_back)
            bd.line(r"\vec\omega^{E/N} = \dot\theta\,\hat e_3", color=H_COL, reason="the polar frame $E$ turns at $\\dot\\theta$")
            self.hold()

        with self.voice("o1_09"):
            bd.line(r"\dot{\hat e}_r = \vec\omega\times\hat e_r = \dot\theta\,\hat e_3\times\hat e_r = \dot\theta\,\hat e_\theta",
                    color=ER_COL, reason="transport theorem", below=True)
            bd.line(r"\dot{\hat e}_\theta = \dot\theta\,\hat e_3\times\hat e_\theta = -\dot\theta\,\hat e_r", color=ET_COL)
            self.hold()

        # zoomed picture of a turning unit vector
        with self.voice("o1_10"):
            self.play(FadeOut(VGroup(rvec, a_er, a_et, l_er, l_et, e3, l_e3, pl, ang, ang_l, axis, ellipse, sn)))
            o = np.array([-4.6, -1.8, 0])
            R = 3.0
            t0, dt = 0.45, 0.32
            arc_bg = Arc(radius=R, start_angle=0.1, angle=1.2, arc_center=o, color=DIM, stroke_width=2)
            v0 = Arrow(o, o + R * np.array([np.cos(t0), np.sin(t0), 0]), buff=0, color=ER_COL, stroke_width=5)
            v1 = Arrow(o, o + R * np.array([np.cos(t0 + dt), np.sin(t0 + dt), 0]), buff=0, color=ER_COL, stroke_width=5).set_opacity(0.55)
            dth = Arc(radius=0.9, start_angle=t0, angle=dt, arc_center=o, color=YELLOW)
            dthl = T(r"d\theta", color=YELLOW).scale(0.6).move_to(o + 1.25 * np.array([np.cos(t0 + dt / 2), np.sin(t0 + dt / 2), 0]))
            tip0 = o + R * np.array([np.cos(t0), np.sin(t0), 0])
            tip1 = o + R * np.array([np.cos(t0 + dt), np.sin(t0 + dt), 0])
            move = Arrow(tip0, tip1, buff=0, color=ET_COL, stroke_width=5, tip_length=0.18)
            ml = Tx(r"length $\approx 1\cdot d\theta$,\\ along $\hat e_\theta$", color=ET_COL).scale(0.55).next_to(move, RIGHT, buff=0.15)
            one = T("1", color=ER_COL).scale(0.6).next_to(v0.get_center(), DOWN, buff=0.15)
            self.play(Create(arc_bg), GrowArrow(v0), FadeIn(one))
            self.play(TransformFromCopy(v0, v1), Create(dth), FadeIn(dthl))
            self.play(GrowArrow(move), FadeIn(ml))
            self.hold()
        self.play(FadeOut(VGroup(arc_bg, v0, v1, dth, dthl, move, ml, one)))
        bd.clear()

        # ---------------------------------------------------------- velocity
        self.add(ellipse, sn)
        self.play(FadeIn(VGroup(rvec, pl, a_er, a_et, l_er, l_et)))
        with self.voice("o1_11"):
            self.play(Transform(hdr, header("Velocity in polar form")))
            bd = Board(self, left=0.6, top=2.6, scale=0.8)
            bd.line(r"\vec v = \frac{d}{dt}\big(r\,\hat e_r\big) = \dot r\,\hat e_r + r\,\dot{\hat e}_r", reason="product rule")
            l = bd.line(r"\vec v = \dot r\,\hat e_r + r\dot\theta\,\hat e_\theta", color=YELLOW, reason="$\\dot{\\hat e}_r = \\dot\\theta\\,\\hat e_\\theta$")
            bd.box(l)
            self.hold()

        def vr_vt():
            t_ = th.get_value()
            r = P / (1 + ECC * np.cos(t_))
            hh = 1.0
            vr = hh / P * ECC * np.sin(t_)
            vt = hh / P * (1 + ECC * np.cos(t_))
            return vr * 1.6, vt * 1.6, r
        a_vr = always_redraw(lambda: Arrow(pos(), pos() + vr_vt()[0] * er(), buff=0, color=ER_COL, stroke_width=4, tip_length=0.15))
        a_vt = always_redraw(lambda: Arrow(pos(), pos() + vr_vt()[1] * et(), buff=0, color=ET_COL, stroke_width=4, tip_length=0.15))
        a_v = always_redraw(lambda: Arrow(pos(), pos() + vr_vt()[0] * er() + vr_vt()[1] * et(), buff=0, color=VEL, stroke_width=6, tip_length=0.2))
        with self.voice("o1_12"):
            self.play(FadeOut(VGroup(a_er, a_et, l_er, l_et)))
            self.play(GrowArrow(a_v))
            self.play(FadeIn(a_vr), FadeIn(a_vt))
            bd.line(r"\dot r:\ \text{radial velocity}", color=ER_COL, indent=0.4, reason="is the distance growing?")
            bd.line(r"r\dot\theta:\ \text{transverse velocity}", color=ET_COL, indent=0.4, reason="how fast it swings around")
            self.play(th.animate.set_value(3.6), run_time=5, rate_func=there_and_back)
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(a_v, a_vr, a_vt)))

        # ---------------------------------------------------------- areal velocity
        with self.voice("o1_13"):
            self.play(Transform(hdr, header("The second law, in vectors")))
            self.play(th.animate.set_value(2.25), run_time=1.5)
            t1 = th.get_value() + 0.45
            p0, p1 = pos(), orb.at(P, ECC, t1)
            tri = Polygon(orb.f, p0, p1, color=AREA, fill_opacity=0.4, stroke_width=2)
            dr = Arrow(p0, p1, buff=0, color=V_COL, stroke_width=5, tip_length=0.15)
            r1 = Arrow(orb.f, p1, buff=0, color=WHITE, stroke_width=3, tip_length=0.15).set_opacity(0.6)
            drl = T(r"\Delta\vec r", color=V_COL).scale(0.6).next_to(dr.get_center(), UR, buff=0.06)
            r1l = T(r"\vec r + \Delta\vec r", color=WHITE).scale(0.55).next_to(p1, UP, buff=0.12)
            rl = T(r"\vec r", color=WHITE).scale(0.6).next_to(rvec.get_center(), DR, buff=0.05)
            self.play(GrowArrow(dr), GrowArrow(r1), FadeIn(drl), FadeIn(r1l), FadeIn(rl))
            self.play(FadeIn(tri))
            ext = DashedLine(p0, p0 + 0.9 * (p0 - orb.f) / np.linalg.norm(p0 - orb.f), color=DIM)
            phi = Angle(Line(p0, p0 + (p0 - orb.f)), Line(p0, p1), radius=0.35, color=YELLOW)
            phil = T(r"\phi", color=YELLOW).scale(0.55).next_to(phi, UR, buff=0.04)
            self.play(Create(ext), Create(phi), FadeIn(phil))
            bd = Board(self, left=0.6, top=2.6, scale=0.8)
            bd.line(r"\Delta A = \tfrac12\,|\vec r|\,|\Delta\vec r|\sin\phi = \tfrac12\,\big|\vec r\times\Delta\vec r\big|",
                    color=AREA, reason="area of a triangle", below=True)
            self.hold()

        with self.voice("o1_14"):
            bd.line(r"\Delta A\;\hat e_3 = \tfrac12\,\vec r\times\Delta\vec r", reason="the cross product points along $\\hat e_3$")
            bd.line(r"\frac{dA}{dt}\,\hat e_3 = \tfrac12\,\vec r\times\vec v", color=YELLOW, reason="divide by $\\Delta t$, let $\\Delta t\\to 0$")
            self.hold()

        with self.voice("o1_15"):
            l = bd.line(r"\text{Kepler II:}\ \ \vec r\times\vec v = \text{constant vector}", color=Q_COL)
            bd.box(l, color=Q_COL)
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(tri, dr, r1, drl, r1l, rl, ext, phi, phil)))

        with self.voice("o1_16"):
            bd = Board(self, left=0.6, top=2.6, scale=0.8)
            bd.line(r"\vec r\times\vec v = r\,\hat e_r\times\big(\dot r\,\hat e_r + r\dot\theta\,\hat e_\theta\big)")
            bd.line(r"= r\dot r\,(\hat e_r\times\hat e_r) + r^2\dot\theta\,(\hat e_r\times\hat e_\theta)", indent=0.5,
                    reason="$\\hat e_r\\times\\hat e_r = 0,\\ \\hat e_r\\times\\hat e_\\theta = \\hat e_3$", below=True)
            l = bd.line(r"\vec r\times\vec v = r^2\dot\theta\;\hat e_3", color=YELLOW, reason="area rate $= \\tfrac12 r^2\\dot\\theta$")
            bd.box(l)
            self.hold()

        with self.voice("o1_17"):
            bd.line(r"\vec h = \vec r\times\vec v", color=H_COL, reason="specific angular momentum")
            bd.line(r"\vec H = \vec r\times m\vec v,\qquad \vec h = \vec H/m", indent=0.5, reason="specific = per unit mass")
            self.hold()
        bd.clear()

        with self.voice("o1_18"):
            self.play(Transform(hdr, header("What could change $\\vec H$?")))
            bd = Board(self, left=0.6, top=2.6, scale=0.8)
            bd.line(r"\frac{d\vec H}{dt} = \underbrace{\vec v\times m\vec v}_{=\,0} + \vec r\times m\vec a", reason="product rule")
            bd.line(r"\frac{d\vec H}{dt} = \vec r\times\vec F", indent=0.5, reason="Newton: $m\\vec a = \\vec F$")
            self.hold()

        with self.voice("o1_19"):
            bd.line(r"\text{Kepler II:}\ \ \vec H = \text{const}\ \Rightarrow\ \vec r\times\vec F = \vec 0", color=Q_COL)
            l = bd.line(r"\vec F \parallel \hat e_r:\ \text{a central force}", color=YELLOW)
            bd.box(l)
            forces = VGroup()
            for tt in np.linspace(0, TAU, 8, endpoint=False):
                q = orb.at(P, ECC, tt)
                d = (orb.f - q) / np.linalg.norm(orb.f - q)
                forces.add(VGroup(Dot(q, color=B_COL, radius=0.06), Arrow(q, q + 0.6 * d, buff=0, color=W_COL, stroke_width=4, tip_length=0.14)))
            self.play(FadeOut(VGroup(rvec, pl)), LaggedStart(*[FadeIn(f) for f in forces], lag_ratio=0.15), run_time=2)
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("o1_20"):
            h, rows = recap(self, [
                r"Kepler: ellipses with the Sun at a focus; equal areas in equal times; $T^2\propto a^3$.",
                r"The polar frame turns at $\dot\theta$: $\dot{\hat e}_r = \dot\theta\,\hat e_\theta$, $\dot{\hat e}_\theta = -\dot\theta\,\hat e_r$.",
                r"$\vec v = \dot r\,\hat e_r + r\dot\theta\,\hat e_\theta$.",
                r"Equal areas $\Rightarrow$ $\vec h = \vec r\times\vec v = r^2\dot\theta\,\hat e_3$ is constant $\Rightarrow$ the force is central.",
            ])
            for rr in rows:
                self.play(FadeIn(rr, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
