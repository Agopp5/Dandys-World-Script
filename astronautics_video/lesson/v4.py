"""Lesson 4: Angular velocity."""
from lcommon import *  # noqa: F401,F403


class V4Concept(Lesson):
    def construct(self):
        with self.voice("v4_01"):
            card = title_card(self, 4, "Angular Velocity", "how fast is a frame turning, and about which axis?")
            self.hold()
        self.play(FadeOut(card))

        # ---- simplest case, top view
        th = ValueTracker(0)
        rate = ValueTracker(0.0)
        th.add_updater(lambda m, dt: m.increment_value(rate.get_value() * dt))
        self.add(th, rate)
        O = np.array([-4.2, -1.0, 0])
        L = 2.3

        def bv(i):
            t = th.get_value()
            return [np.array([np.cos(t), np.sin(t), 0]), np.array([-np.sin(t), np.cos(t), 0])][i]
        n1 = Arrow(O, O + L * RIGHT, buff=0, color=N_COL, stroke_width=4)
        n2 = Arrow(O, O + L * UP, buff=0, color=N_COL, stroke_width=4)
        n1l = T(r"\hat n_1", color=N_COL).scale(0.7).next_to(n1.get_end(), RIGHT, buff=0.1)
        n2l = T(r"\hat n_2", color=N_COL).scale(0.7).next_to(n2.get_end(), UP, buff=0.1)
        dot3 = VGroup(Circle(radius=0.12, color=WHITE, stroke_width=2), Dot(radius=0.035)).move_to(O)
        l3 = T(r"\hat n_3 = \hat b_3\ (\text{out of page})", color=DIM).scale(0.5).next_to(O, DOWN, buff=0.3)
        b1 = always_redraw(lambda: Arrow(O, O + L * bv(0), buff=0, color=B_COL, stroke_width=5))
        b2 = always_redraw(lambda: Arrow(O, O + L * bv(1), buff=0, color=B_COL, stroke_width=5))
        b1l = always_redraw(lambda: T(r"\hat b_1", color=B_COL).scale(0.7).move_to(O + (L + 0.35) * bv(0)))
        b2l = always_redraw(lambda: T(r"\hat b_2", color=B_COL).scale(0.7).move_to(O + (L + 0.35) * bv(1)))
        arc = always_redraw(lambda: Arc(radius=0.7, angle=(th.get_value() % TAU) + 1e-4, arc_center=O, color=YELLOW))
        with self.voice("v4_02"):
            hdr = header("The simplest rotation")
            self.play(FadeIn(hdr))
            self.play(FadeIn(VGroup(n1, n2, n1l, n2l, dot3, l3)))
            self.add(b1, b2, b1l, b2l, arc)
            self.play(rate.animate.set_value(0.5), run_time=1.0)
            rd = always_redraw(lambda: T(r"\theta(t) = %.2f\ \text{rad},\quad \dot\theta = %.2f\ \text{rad/s}"
                                         % (th.get_value() % TAU, rate.get_value())).scale(0.75).move_to(RIGHT * 2.8 + UP * 2.3))
            self.add(rd)
            self.hold()

        with self.voice("v4_03"):
            d = T(r"\vec\omega^{\mathcal B/\mathcal N} = \dot\theta\,\hat n_3").scale(1.0).move_to(RIGHT * 2.8 + UP * 1.1)
            self.play(Write(d))
            pts = VGroup(Tx(r"direction: the spin axis (right-hand rule:\\fingers curl with the turning, thumb = $\vec\omega$)"),
                         Tx(r"length: the spin rate $\dot\theta$")).scale(0.6).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            pts.next_to(d, DOWN, buff=0.4)
            self.play(FadeIn(pts[0]))
            self.wait(1.5)
            self.play(FadeIn(pts[1]))
            out = Tx(r"turning counterclockwise $\Rightarrow$ $\vec\omega$ points out of the page", color=W_COL).scale(0.55)
            out.next_to(pts, DOWN, buff=0.35)
            self.play(FadeIn(out))
            self.hold()

        with self.voice("v4_04"):
            n = T(r"\vec\omega^{\mathcal B/\mathcal N}", r"\ :\ \text{frame } \mathcal B \text{ as seen from frame } \mathcal N").scale(0.7)
            n2_ = T(r"\vec\omega^{\mathcal N/\mathcal B} = -\,\vec\omega^{\mathcal B/\mathcal N}", color=YELLOW).scale(0.8)
            VGroup(n, n2_).arrange(DOWN, buff=0.35).next_to(out, DOWN, buff=0.45)
            self.play(Write(n))
            self.play(Write(n2_))
            self.hold()
        self.play(FadeOut(VGroup(d, pts, out, n, n2_)), FadeOut(rd))
        self.remove(rd)

        # ---- derivative of b1 from components
        vel = always_redraw(lambda: Arrow(O + L * bv(0), O + L * bv(0) + 1.1 * bv(1), buff=0, color=V_COL, stroke_width=5))
        with self.voice("v4_05"):
            self.play(Transform(hdr, header("How fast does $\\hat b_1$ move, as seen in $\\mathcal N$?")))
            self.add(vel)
            self.play(FadeIn(vel))
            q = T(r"{}^{\mathcal N}\frac{d}{dt}\hat b_1 = \ ?", color=V_COL).move_to(RIGHT * 2.6 + UP * 2.3)
            self.play(Write(q))
            self.hold()

        with self.voice("v4_06"):
            bd = Board(self, left=-0.9, top=1.5, scale=0.78, buff=0.4)
            bd.line(r"\hat b_1 = \cos\theta\,\hat n_1 + \sin\theta\,\hat n_2", reason="row 1 of $C_3(\\theta)$")
            bd.line(r"{}^{\mathcal N}\frac{d}{dt}\hat b_1 = -\dot\theta\sin\theta\,\hat n_1 + \dot\theta\cos\theta\,\hat n_2",
                    reason="chain rule; $\\hat n_1,\\hat n_2$ are fixed in $\\mathcal N$", below=True)
            self.hold()

        with self.voice("v4_07"):
            bd.line(r"= \dot\theta\,\big(-\sin\theta\,\hat n_1 + \cos\theta\,\hat n_2\big)", indent=0.8, reason="factor out $\\dot\\theta$")
            l = bd.line(r"= \dot\theta\,\hat b_2", indent=0.8, color=V_COL, reason="that bracket is row 2 of $C_3$: $\\hat b_2$")
            bd.box(l, V_COL)
            self.hold()

        with self.voice("v4_08"):
            bd.line(r"\vec\omega\times\hat b_1 = \dot\theta\,\hat b_3\times\hat b_1 = \dot\theta\,\hat b_2", color=Q_COL,
                    reason="$\\hat b_3\\times\\hat b_1 = \\hat b_2$ (right-handed)")
            ok = Tx(r"they match \checkmark", color=Q_COL).scale(0.8).next_to(bd.lines[-1], DOWN, buff=0.35).align_to(bd.lines[-1], LEFT)
            self.play(Write(ok))
            self.hold()
        for m_ in (b1, b2, b1l, b2l, arc, vel):
            m_.clear_updaters()
        bd.clear()
        self.play(FadeOut(VGroup(n1, n2, n1l, n2l, dot3, l3, b1, b2, b1l, b2l, arc, vel, q, ok)))
        rate.set_value(0)

        # ---- general geometric argument (3D)
        cam = Cam(phi=60, theta=28, scale=1.25, center=(-3.8, -1.9))
        D = Draw(cam)
        self.add(*cam.trackers())
        ang = ValueTracker(0)
        sp = ValueTracker(0)
        ang.add_updater(lambda m, dt: m.increment_value(sp.get_value() * dt))
        self.add(ang, sp)
        phi0 = np.radians(50)
        Lb = 2.4
        h = Lb * np.cos(phi0)

        def bt():
            a = ang.get_value()
            return Lb * np.array([np.sin(phi0) * np.cos(a), np.sin(phi0) * np.sin(a), np.cos(phi0)])
        w_ar = D.arrow(ORIGIN, [0, 0, 2.9], W_COL, 7, k=0)
        wl = D.label(r"\vec\omega", [0.0, 0.0, 3.2], W_COL, 0.8)
        bvec = D.arrow(ORIGIN, bt, B_COL, 6, k=0)
        bl = D.label(r"\hat b", lambda: bt() * 1.12, B_COL, 0.8)
        circ = D.curve(lambda t: [Lb * np.sin(phi0) * np.cos(t), Lb * np.sin(phi0) * np.sin(t), h], (0, TAU), B_COL, 2, n=90, k=0)
        rad = D.line([0, 0, h], bt, YELLOW, 3, dashed=True, op=0)
        radl = D.label(r"\rho = \sin\phi", lambda: (np.array([0, 0, h]) + bt()) / 2 + np.array([0, 0, 0.3]), YELLOW, 0.6)
        phiarc = D.curve(lambda t: 0.9 * np.array([np.sin(t) * np.cos(ang.get_value()), np.sin(t) * np.sin(ang.get_value()), np.cos(t)]),
                         (0, phi0), V_COL, 3, n=20, op=0)
        phil = D.label(r"\phi", lambda: 1.15 * np.array([np.sin(phi0 / 2) * np.cos(ang.get_value()),
                                                          np.sin(phi0 / 2) * np.sin(ang.get_value()), np.cos(phi0 / 2)]), V_COL, 0.7)
        with self.voice("v4_09"):
            self.play(Transform(hdr, header("Why it's always $\\vec\\omega\\times\\hat b$: a picture")))
            self.add(circ, w_ar, wl, bvec, bl)
            self.play(*grow(w_ar, bvec), *show(wl, bl))
            self.play(sp.animate.set_value(0.5), *grow(circ), run_time=2.0)
            self.add(phiarc, phil)
            self.play(*show(phiarc, phil))
            self.hold()

        with self.voice("v4_10"):
            self.add(rad, radl)
            self.play(*show(rad, radl))
            bd = Board(self, left=0.2, top=2.3, scale=0.75, buff=0.4)
            bd.line(r"\text{radius of the circle: } \rho = |\hat b|\sin\phi = \sin\phi")
            bd.line(r"\text{in time } \Delta t \text{ the frame turns } |\vec\omega|\,\Delta t")
            bd.line(r"\text{arc length} = \rho\,|\vec\omega|\,\Delta t = \sin\phi\,|\vec\omega|\,\Delta t", reason="arc = radius $\\times$ angle", below=True)
            l = bd.line(r"\text{speed} = \frac{\text{arc}}{\Delta t} = \sin\phi\,|\vec\omega|", color=YELLOW)
            self.hold()

        with self.voice("v4_11"):
            vv = D.arrow(bt, lambda: bt() + 0.8 * np.cross([0, 0, 1.0], bt()), V_COL, 6, k=0)
            self.add(vv)
            self.play(*grow(vv))
            bd.line(r"\text{direction: tangent to the circle} \perp \hat b,\ \perp \vec\omega")
            bd.line(r"|\vec\omega\times\hat b| = |\vec\omega|\,(1)\sin\phi", reason="same size, same direction", indent=0.6)
            l = bd.line(r"{}^{\mathcal N}\frac{d}{dt}\hat b_i = \vec\omega^{\mathcal B/\mathcal N}\times\hat b_i", color=YELLOW, scale=0.95)
            bd.box(l)
            self.hold()
        sp.set_value(0)
        stuff = flat(circ, w_ar, wl, bvec, bl, rad, radl, phiarc, phil, vv)
        bd.clear()
        self.play(*hide(*stuff))
        self.remove(*stuff)

        # ---- addition through a chain
        with self.voice("v4_12"):
            self.play(Transform(hdr, header("Angular velocities add through a chain of frames")))
            chainpic = VGroup(*[Tx(t) for t in (r"$\mathcal N$", r"$\mathcal A$", r"$\mathcal B$")]).arrange(RIGHT, buff=2.2).move_to(UP * 1.8)
            arrs = VGroup(Arrow(chainpic[0].get_right(), chainpic[1].get_left(), color=DIM),
                          Arrow(chainpic[1].get_right(), chainpic[2].get_left(), color=DIM))
            la = T(r"\vec\omega^{\mathcal A/\mathcal N}", color=W_COL).scale(0.7).next_to(arrs[0], UP, buff=0.1)
            lb = T(r"\vec\omega^{\mathcal B/\mathcal A}", color=W_COL).scale(0.7).next_to(arrs[1], UP, buff=0.1)
            self.play(FadeIn(chainpic), GrowArrow(arrs[0]), GrowArrow(arrs[1]), FadeIn(la), FadeIn(lb))
            add = T(r"\vec\omega^{\mathcal B/\mathcal N} = \vec\omega^{\mathcal B/\mathcal A} + \vec\omega^{\mathcal A/\mathcal N}", color=YELLOW).scale(0.95)
            add.next_to(chainpic, DOWN, buff=0.8)
            self.play(Write(add), run_time=2.0)
            self.hold()
        self.play(FadeOut(VGroup(chainpic, arrs, la, lb, add)))

        with self.voice("v4_13"):
            self.play(Transform(hdr, header("For 3-2-1 Euler angles: $\\mathcal A\\to\\mathcal P\\to\\mathcal Q\\to\\mathcal B$")))
            bd = Board(self, left=-6.0, top=2.3, scale=0.8, buff=0.4)
            bd.line(r"\vec\omega^{\mathcal B/\mathcal A} = \vec\omega^{\mathcal B/\mathcal Q} + \vec\omega^{\mathcal Q/\mathcal P} + \vec\omega^{\mathcal P/\mathcal A}")
            bd.line(r"= \dot\phi\,\hat b_1 + \dot\theta\,\hat q_2 + \dot\psi\,\hat p_3", indent=1.4,
                    reason="each step is one rotation about one axis")
            self.hold()

        with self.voice("v4_14"):
            bd.line(r"\text{need } \hat q_2 \text{ and } \hat p_3 \text{ in } \mathcal B \text{ components}", color=YELLOW,
                    reason="$\\hat b_1$ is already a $\\mathcal B$ axis")
            self.hold()

        with self.voice("v4_15"):
            bd.line(r"\hat q_2 = \cos\phi\,\hat b_2 - \sin\phi\,\hat b_3", reason="column 2 of $C_1(\\phi)$: $\\hat q_2$ in $\\mathcal B$ components")
            self.hold()

        with self.voice("v4_16"):
            bd.line(r"\hat p_3 = -\sin\theta\,\hat q_1 + \cos\theta\,\hat q_3", reason="column 3 of $C_2(\\theta)$")
            bd.line(r"\hat q_1 = \hat b_1,\qquad \hat q_3 = \sin\phi\,\hat b_2 + \cos\phi\,\hat b_3", indent=0.8, reason="columns 1 and 3 of $C_1(\\phi)$")
            bd.line(r"\hat p_3 = -\sin\theta\,\hat b_1 + \cos\theta\sin\phi\,\hat b_2 + \cos\theta\cos\phi\,\hat b_3", indent=0.8, color=YELLOW,
                    reason="substitute")
            self.hold()

        with self.voice("v4_17"):
            bd.clear()
            bd = Board(self, left=-6.0, top=2.3, scale=0.8, buff=0.42)
            bd.line(r"\vec\omega = \dot\phi\,\hat b_1 + \dot\theta(\cos\phi\,\hat b_2 - \sin\phi\,\hat b_3)"
                    r" + \dot\psi(-\sin\theta\,\hat b_1 + \cos\theta\sin\phi\,\hat b_2 + \cos\theta\cos\phi\,\hat b_3)")
            bd.line(r"\omega_1 = \dot\phi - \dot\psi\sin\theta", color=B_COL, indent=0.8, reason="collect the $\\hat b_1$ terms")
            bd.line(r"\omega_2 = \dot\theta\cos\phi + \dot\psi\cos\theta\sin\phi", color=B_COL, indent=0.8, reason="collect the $\\hat b_2$ terms")
            bd.line(r"\omega_3 = -\dot\theta\sin\phi + \dot\psi\cos\theta\cos\phi", color=B_COL, indent=0.8, reason="collect the $\\hat b_3$ terms")
            self.hold()

        with self.voice("v4_18"):
            bd.clear()
            fwd = T(r"\begin{bmatrix}\omega_1\\\omega_2\\\omega_3\end{bmatrix} = "
                    r"\begin{bmatrix}-\sin\theta & 0 & 1\\ \cos\theta\sin\phi & \cos\phi & 0\\ \cos\theta\cos\phi & -\sin\phi & 0\end{bmatrix}"
                    r"\begin{bmatrix}\dot\psi\\\dot\theta\\\dot\phi\end{bmatrix}").scale(0.75).move_to(UP * 1.6)
            self.play(Write(fwd), run_time=2.5)
            g = Tx(r"gyro measures $\omega$ $\Rightarrow$ we need the angle rates to integrate", color=REASON).scale(0.6).next_to(fwd, DOWN, buff=0.35)
            self.play(FadeIn(g))
            inv = T(r"\begin{bmatrix}\dot\psi\\\dot\theta\\\dot\phi\end{bmatrix} = ", r"\frac{1}{\cos\theta}",
                    r"\begin{bmatrix}0 & \sin\phi & \cos\phi\\ 0 & \cos\phi\cos\theta & -\sin\phi\cos\theta\\ \cos\theta & \sin\phi\sin\theta & \cos\phi\sin\theta\end{bmatrix}",
                    r"\begin{bmatrix}\omega_1\\\omega_2\\\omega_3\end{bmatrix}").scale(0.72).next_to(g, DOWN, buff=0.45)
            self.play(Write(inv), run_time=3.0)
            self.hold()

        with self.voice("v4_19"):
            self.play(inv[1].animate.set_color(P_COL), Create(SurroundingRectangle(inv[1], color=P_COL, buff=0.08)))
            ax = Axes(x_range=[0, 90, 15], y_range=[0, 12, 4], x_length=4.5, y_length=1.3,
                      axis_config={"color": DIM, "include_tip": False},
                      x_axis_config={"numbers_to_include": [0, 30, 60, 90]}).next_to(inv, DOWN, buff=0.4)
            curve = ax.plot(lambda x: 1 / np.cos(np.radians(x)), x_range=[0, 85.2], color=P_COL)
            yl = T(r"1/\cos\theta", color=P_COL).scale(0.55).next_to(ax.y_axis, UP, buff=0.05)
            self.play(Create(ax), FadeIn(yl))
            self.play(Create(curve), run_time=2.0)
            lk = Tx(r"$\theta\to90^\circ$: rates blow up\\(gimbal lock again)", color=P_COL).scale(0.6).next_to(ax, LEFT, buff=0.6)
            self.play(FadeIn(lk))
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))


class V4Examples(Lesson):
    def construct(self):
        cam = Cam(phi=72, theta=-25, scale=1.0, center=(-4.2, -1.3))
        D = Draw(cam)
        self.add(*cam.trackers())
        rot = ValueTracker(0)
        rot.add_updater(lambda m, dt: m.increment_value(0.25 * dt))
        self.add(rot)
        Re = 1.8
        lat = np.radians(28.6)
        site = lambda: Re * np.array([np.cos(lat) * np.cos(rot.get_value() + 0.3), np.cos(lat) * np.sin(rot.get_value() + 0.3), np.sin(lat)])
        earth = D.sphere(ORIGIN, Re, "#7FB3FF", rot=lambda: rot.get_value())
        w_ar = D.arrow(ORIGIN, [0, 0, 2.9], W_COL, 7, k=0)
        wl = D.label(r"\vec\omega", [0.0, 0.0, 3.2], W_COL, 0.8)
        sdot = D.dot(site, YELLOW, 0.07)
        with self.voice("v4_20"):
            hdr = header("Example 1: the spinning Earth")
            self.play(FadeIn(hdr))
            self.add(earth, w_ar, wl, sdot)
            self.play(*grow(w_ar), *show(wl))
            bd = Board(self, left=-1.2, top=2.3, scale=0.78)
            bd.line(r"\text{one turn (relative to the stars)} = 86164\ \text{s}", reason="a sidereal day")
            l = bd.line(r"|\vec\omega| = \frac{2\pi}{86164\ \text{s}} = 7.2921\times10^{-5}\ \text{rad/s}", color=W_COL)
            self.hold()

        vv = D.arrow(site, lambda: site() + 0.9 * np.cross([0, 0, 1.0], site()) / np.linalg.norm(site()[:2]), Q_COL, 6, k=0)
        with self.voice("v4_21"):
            self.add(vv)
            self.play(*grow(vv))
            bd.line(r"\vec v = {}^{\mathcal E}\dot{\vec r} + \vec\omega\times\vec r = \vec 0 + \vec\omega\times\vec r", reason="point fixed on Earth")
            bd.line(r"|\vec v| = \omega\,R\cos(\text{latitude})", color=Q_COL, indent=0.8, reason="$\\omega\\times$ (distance from the spin axis)")
            bd.line(r"\text{direction: due east}", indent=0.8)
            self.hold()

        with self.voice("v4_22"):
            bd.clear()
            bd = Board(self, left=-1.2, top=2.3, scale=0.72, buff=0.35)
            bd.line(r"\omega R_\oplus = (7.2921\times10^{-5})(6378\ \text{km}) = 0.4651\ \text{km/s}")
            bd.line(r"\text{Kennedy } (28.6^\circ):\ 0.4651\cos 28.6^\circ = 0.408\ \text{km/s}", indent=0.4)
            bd.line(r"\text{Wallops } (37.9^\circ):\ 0.4651\cos 37.9^\circ = 0.367\ \text{km/s}", indent=0.4)
            bd.line(r"\text{Alc\^antara } (2.3^\circ\text{S}):\ 0.4651\cos 2.3^\circ = 0.465\ \text{km/s}", indent=0.4)
            self.hold()

        with self.voice("v4_23"):
            chart = BarChart([408, 367, 465], bar_names=["Kennedy", "Wallops", "Alcantara"], y_range=[0, 500, 100],
                             y_length=2.0, x_length=4, bar_colors=[B_COL, B_COL, Q_COL],
                             x_axis_config={"font_size": 22}, y_axis_config={"font_size": 22})
            chart.next_to(bd.lines[-1], DOWN, buff=0.5).align_to(bd.lines[0], LEFT)
            self.play(Create(chart), run_time=1.5)
            lab = Tx(r"free eastward boost (m/s):\\ biggest at the equator", color=Q_COL).scale(0.55).next_to(chart, RIGHT, buff=0.3)
            self.play(FadeIn(lab))
            self.hold()
        rot.clear_updaters()
        stuff = flat(earth, w_ar, wl, sdot, vv)
        bd.clear()
        self.play(*hide(*stuff), FadeOut(VGroup(chart, lab)))
        self.remove(*stuff)

        with self.voice("v4_24"):
            self.play(Transform(hdr, header("Example 2: Euler rates $\\to$ angular velocity")))
            given = VGroup(T(r"\psi = 30^\circ,\ \ \theta = 20^\circ,\ \ \phi = 10^\circ"),
                           T(r"\dot\psi = 1,\ \ \dot\theta = 2,\ \ \dot\phi = 3\ \ \text{deg/s}")).scale(0.8).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.95)
            self.play(Write(given), run_time=2.0)
            self.hold()

        with self.voice("v4_25"):
            bd = Board(self, left=-6.2, top=1.8, scale=0.78, buff=0.42)
            bd.line(r"\omega_1 = \dot\phi - \dot\psi\sin\theta = 3 - (1)\sin20^\circ = 3 - 0.342 = 2.658\ \text{deg/s}")
            self.hold()

        with self.voice("v4_26"):
            bd.line(r"\omega_2 = \dot\theta\cos\phi + \dot\psi\cos\theta\sin\phi = 2\cos10^\circ + \cos20^\circ\sin10^\circ")
            bd.line(r"= 1.970 + 0.163 = 2.133\ \text{deg/s}", indent=1.2)
            self.hold()

        with self.voice("v4_27"):
            bd.line(r"\omega_3 = -\dot\theta\sin\phi + \dot\psi\cos\theta\cos\phi = -2\sin10^\circ + \cos20^\circ\cos10^\circ")
            bd.line(r"= -0.347 + 0.925 = 0.578\ \text{deg/s}", indent=1.2)
            l = bd.line(r"\omega_{(\mathcal B)} = [\,2.658,\ \ 2.133,\ \ 0.578\,]^T\ \text{deg/s}", color=YELLOW)
            bd.box(l)
            self.hold()

        with self.voice("v4_28"):
            note = Tx(r"not $[1, 2, 3]$: the rates act about tilted, non-perpendicular axes,\\so they mix when written in $\mathcal B$",
                      color=REASON).scale(0.65).next_to(l, DOWN, buff=0.4).align_to(l, LEFT)
            self.play(FadeIn(note))
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("v4_29"):
            h, rows = recap(self, [
                r"$\vec\omega$ points along the spin axis; its length is the spin rate.",
                r"Every basis vector of a rotating frame obeys ${}^{\mathcal N}\tfrac{d}{dt}\hat b_i = \vec\omega\times\hat b_i$.",
                r"Angular velocities add through a chain: $\vec\omega^{\mathcal B/\mathcal N} = \vec\omega^{\mathcal B/\mathcal A} + \vec\omega^{\mathcal A/\mathcal N}$.",
                r"Euler rates $\leftrightarrow\ \vec\omega$ through a matrix that is singular at gimbal lock.",
            ])
            for rrow in rows:
                self.play(FadeIn(rrow, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
