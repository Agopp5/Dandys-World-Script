"""Part 3: constants of motion - angular momentum and energy."""
from ocommon import *  # noqa: F401,F403

A, ECC = 2.0, 0.5
P = A * (1 - ECC ** 2)


class O3Concept(OLesson):
    def construct(self):
        with self.voice("o3_01"):
            t = o_title(self, 3, "Constants of Motion", "angular momentum and energy")
            self.wait(1.5)
            self.play(FadeOut(t))
            hdr = header("Look for what never changes")
            self.play(FadeIn(hdr))
            eom = T(r"\ddot{\vec r} = -\frac{\mu}{r^3}\,\vec r").scale(1.1).shift(UP * 1.3)
            self.play(Write(eom))
            c1 = VGroup(RoundedRectangle(width=4.2, height=1.2, corner_radius=0.15, color=H_COL),
                        Tx(r"angular momentum $\vec h$", color=H_COL).scale(0.7))
            c2 = VGroup(RoundedRectangle(width=4.2, height=1.2, corner_radius=0.15, color=B_COL),
                        Tx(r"energy $\mathcal E$", color=B_COL).scale(0.7))
            VGroup(c1, c2).arrange(RIGHT, buff=0.8).shift(DOWN * 1.0)
            self.play(FadeIn(c1, shift=UP * 0.2), FadeIn(c2, shift=UP * 0.2))
            self.hold()
        self.play(FadeOut(VGroup(eom, c1, c2)))

        # ------------------------------------------------ h is constant
        with self.voice("o3_02"):
            self.play(Transform(hdr, header("Angular momentum")))
            bd = Board(self, left=-6.5, top=2.6, scale=0.82, buff=0.45)
            bd.line(r"\frac{d\vec h}{dt} = \frac{d}{dt}\big(\vec r\times\vec v\big) = \vec v\times\vec v + \vec r\times\ddot{\vec r}", reason="product rule")
            bd.line(r"= \vec 0 + \vec r\times\Big(-\frac{\mu}{r^3}\,\vec r\Big) = -\frac{\mu}{r^3}\,\big(\vec r\times\vec r\big) = \vec 0",
                    indent=0.6, reason="a vector crossed with itself is zero", below=True)
            self.hold()

        with self.voice("o3_03"):
            l = bd.line(r"\vec h = \vec r\times\vec v = \text{constant}", color=YELLOW, reason="magnitude \\emph{and} direction")
            bd.box(l)
            self.hold()
        bd.clear()

        # ------------------------------------------------ planar orbit (3D)
        cam = Cam(phi=62, theta=-50, scale=1.0, center=(-3.4, -0.6))
        D = Draw(cam)
        self.add(*cam.trackers())
        hn = np.array([0.25, -0.35, 0.9])
        hn = hn / np.linalg.norm(hn)
        u1 = np.cross(hn, [0, 0, 1.0])
        u1 /= np.linalg.norm(u1)
        u2 = np.cross(hn, u1)
        S = 0.85

        def orbit3(th):
            r = P / (1 + ECC * np.cos(th))
            return S * r * (np.cos(th) * u1 + np.sin(th) * u2)
        ctr = -S * A * ECC * u1
        corners = [ctr + S * (sx * 2.9 * u1 + sy * 2.2 * u2) for sx, sy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
        plane = D.polygon(corners, B_COL, 0.15)
        ocurve = D.curve(orbit3, (-PI, PI), ORB, 3, n=120, k=0)
        ha = D.arrow(ORIGIN, 2.2 * hn, H_COL, 6, k=0)
        hl = D.label(r"\vec h", 2.45 * hn, H_COL)
        th_r = 2.0
        rp_ = orbit3(th_r)
        vdir = orbit3(th_r + 0.01) - orbit3(th_r - 0.01)
        vdir = vdir / np.linalg.norm(vdir)
        ra = D.arrow(ORIGIN, rp_, WHITE, 5, k=0)
        va = D.arrow(rp_, rp_ + 1.2 * vdir, VEL, 5, k=0)
        rl = D.label(r"\vec r", rp_ * 0.55 + 0.25 * hn, WHITE)
        vl = D.label(r"\vec v", rp_ + 1.4 * vdir, VEL)
        foc = D.dot(ORIGIN, EARTH, 0.1)
        with self.voice("o3_04"):
            self.play(Transform(hdr, header("Every orbit is planar")))
            bd = Board(self, left=0.9, top=2.6, scale=0.8, buff=0.42)
            bd.line(r"\vec r\cdot\vec h = \vec r\cdot\big(\vec r\times\vec v\big) = 0", reason="$\\vec r\\times\\vec v \\perp \\vec r$", below=True)
            self.add(plane, ocurve, foc, ha, hl, ra, va, rl, vl)
            self.play(*grow(ha), *show(hl), run_time=1.2)
            self.play(*grow(ra, va), *show(rl, vl), run_time=1.2)
            self.play(*grow(ocurve), run_time=2)
            bd.line(r"\vec r \perp \vec h \text{ always}\ \Rightarrow\ \text{motion stays in one plane}", color=YELLOW, below=True)
            cam.start_spin(self, 0.15)
            self.hold()
        cam.stop_spin()
        g3 = flat(plane, ocurve, ha, hl, ra, va, rl, vl, foc)

        with self.voice("o3_05"):
            bd.line(r"|\vec h| = h = r^2\dot\theta = \text{const}", color=H_COL, reason="Kepler II, for any central force", below=True)
            self.hold()
        bd.clear()
        self.play(*hide(*g3))
        self.remove(*g3)

        # ------------------------------------------------ flight-path angle
        orb = Orb(focus=(-3.4, -0.7), k=1.15)
        ell = orb.conic(P, ECC)
        e_ = earth(orb.f)
        th0 = 1.4
        q = orb.at(P, ECC, th0)
        vr = ECC * np.sin(th0)
        vt = 1 + ECC * np.cos(th0)
        er, et = orb.unit(th0), orb.unit(th0 + PI / 2)
        vv = 1.3 * (vr * er + vt * et) / np.hypot(vr, vt) * 1.2
        rline = Line(orb.f, q, color=WHITE, stroke_width=3)
        horiz = DashedLine(q - 1.0 * et, q + 1.9 * et, color=ET_COL)
        hlab = Tx(r"local horizontal, $\hat e_\theta$", color=ET_COL).scale(0.48).next_to(q + 1.9 * et, UP, buff=0.08)
        varr = Arrow(q, q + vv, buff=0, color=VEL, stroke_width=6, tip_length=0.2)
        vlab = T(r"\vec v", color=VEL).scale(0.65).next_to(varr.get_end(), RIGHT, buff=0.1)
        g_ = np.arctan2(vr, vt)
        gam = Arc(radius=0.75, start_angle=th0 + PI / 2, angle=-g_, arc_center=q, color=YELLOW, stroke_width=4)
        gl = T(r"\gamma", color=YELLOW).scale(0.65).move_to(q + 1.0 * (et + vv / np.linalg.norm(vv)) / np.linalg.norm(et + vv / np.linalg.norm(vv)))
        with self.voice("o3_06"):
            self.play(Transform(hdr, header("The flight-path angle")))
            self.play(Create(ell), FadeIn(e_))
            self.play(Create(rline), FadeIn(planet(q)))
            self.play(Create(horiz), FadeIn(hlab))
            self.play(GrowArrow(varr), FadeIn(vlab))
            self.play(Create(gam), FadeIn(gl))
            bd = Board(self, left=0.9, top=2.6, scale=0.8, buff=0.42)
            bd.line(r"h = r\,v_\theta", reason="only $v_\\theta$ contributes to $\\vec r\\times\\vec v$")
            l = bd.line(r"h = r\,v\cos\gamma", color=YELLOW, reason="$v_\\theta = v\\cos\\gamma$")
            self.hold()

        with self.voice("o3_07"):
            pts = [(0.0, Q_COL, r"r_p,\ v_p"), (PI, P_COL, r"r_a,\ v_a")]
            marks = VGroup()
            for th, col, lab in pts:
                qq = orb.at(P, ECC, th)
                ve = (1 + ECC * np.cos(th)) * 0.9
                ar = Arrow(qq, qq + ve * orb.unit(th + PI / 2), buff=0, color=col, stroke_width=5, tip_length=0.15)
                lb = T(lab, color=col).scale(0.55).next_to(qq, RIGHT if th == 0 else LEFT, buff=0.15)
                marks.add(Dot(qq, color=col), ar, lb)
            self.play(FadeIn(marks))
            bd.line(r"\gamma = 0 \text{ at the apsides}", indent=0.4)
            l = bd.line(r"h = r_p\,v_p = r_a\,v_a", color=YELLOW, reason="fastest where closest")
            bd.box(l)
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(ell, e_, rline, horiz, hlab, varr, vlab, gam, gl, marks)),
                  *[FadeOut(m) for m in self.mobjects if isinstance(m, Dot)])

        # ------------------------------------------------ energy
        with self.voice("o3_08"):
            self.play(Transform(hdr, header("Energy")))
            bd = Board(self, left=-6.5, top=2.6, scale=0.82, buff=0.45)
            bd.line(r"T = \tfrac12 v^2 = \tfrac12\,\dot{\vec r}\cdot\dot{\vec r}", reason="kinetic energy per unit mass")
            bd.line(r"\dot T = \tfrac12\big(\ddot{\vec r}\cdot\dot{\vec r} + \dot{\vec r}\cdot\ddot{\vec r}\big) = \dot{\vec r}\cdot\ddot{\vec r}", indent=0.6, reason="product rule")
            self.hold()

        with self.voice("o3_09"):
            bd.line(r"\dot T = \dot{\vec r}\cdot\Big(-\frac{\mu}{r^3}\,\vec r\Big) = -\frac{\mu}{r^3}\,\big(\dot{\vec r}\cdot\vec r\big)", indent=0.6, reason="equation of motion")
            self.hold()

        with self.voice("o3_10"):
            bd.line(r"\vec r\cdot\dot{\vec r} = r\,\hat e_r\cdot\big(\dot r\,\hat e_r + r\dot\theta\,\hat e_\theta\big) = r\dot r", indent=0.6, reason="only the $\\hat e_r$ parts survive")
            l = bd.line(r"\dot T = -\frac{\mu}{r^2}\,\dot r", indent=0.6, color=YELLOW)
            self.hold()

        with self.voice("o3_11"):
            bd.line(r"\frac{d}{dt}\Big(\frac{\mu}{r}\Big) = -\frac{\mu}{r^2}\,\dot r", color=YELLOW, reason="chain rule: the same thing!")
            bd.line(r"\frac{d}{dt}\Big(T - \frac{\mu}{r}\Big) = 0", color=Q_COL)
            self.hold()

        with self.voice("o3_12"):
            l = bd.line(r"\mathcal E = \frac{v^2}{2} - \frac{\mu}{r} = \text{constant}", color=YELLOW, reason="specific mechanical energy")
            bd.box(l)
            bd.line(r"\frac{v^2}{2}:\ \text{kinetic},\qquad -\frac{\mu}{r}:\ \text{potential}", indent=0.6, color=B_COL, reason="both per unit mass")
            self.hold()
        bd.clear()

        # ------------------------------------------------ potential well
        ax = Axes(x_range=[0, 10, 2], y_range=[-2.2, 0.8, 1], x_length=8.5, y_length=5.0,
                  axis_config={"color": DIM, "include_ticks": False}).shift(LEFT * 1.6 + DOWN * 0.5)
        xl = T("r", color=DIM).scale(0.65).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = Tx(r"energy per unit mass", color=DIM).scale(0.5).next_to(ax.y_axis, UP, buff=0.1)
        mu = 2.0
        V = ax.plot(lambda r: -mu / r, x_range=[0.93, 10], color=P_COL, stroke_width=4)
        Vl = T(r"V(r) = -\frac{\mu}{r}", color=P_COL).scale(0.7).move_to(ax.c2p(7.0, -0.75))
        with self.voice("o3_13"):
            self.play(Transform(hdr, header("Why the minus sign? A potential well")))
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            zero = Tx(r"$V = 0$ at $r\to\infty$", color=DIM).scale(0.55).next_to(ax.c2p(8.6, 0), UP, buff=0.3)
            self.play(Create(V), FadeIn(Vl), FadeIn(zero), run_time=2)
            self.hold()

        Et = ValueTracker(-0.5)
        Eline = always_redraw(lambda: DashedLine(ax.c2p(0.2, Et.get_value()), ax.c2p(10, Et.get_value()), color=YELLOW))
        El = always_redraw(lambda: T(r"\mathcal E", color=YELLOW).scale(0.7).next_to(ax.c2p(10, Et.get_value()), RIGHT, buff=0.1))
        rr = ValueTracker(2.0)

        def gap():
            r = rr.get_value()
            top = max(Et.get_value(), -mu / r)
            return Line(ax.c2p(r, -mu / r), ax.c2p(r, top), color=B_COL, stroke_width=7)
        gp = always_redraw(gap)
        gpl = always_redraw(lambda: Tx("kinetic", color=B_COL).scale(0.5).next_to(gap(), RIGHT, buff=0.1))
        with self.voice("o3_14"):
            self.play(Create(Eline), FadeIn(El))
            self.play(FadeIn(gp), FadeIn(gpl))
            self.play(rr.animate.set_value(3.4), run_time=2)
            self.hold()

        with self.voice("o3_15"):
            rmax = mu / 0.5
            wall = Dot(ax.c2p(rmax, -0.5), color=YELLOW, radius=0.09)
            wl = Tx(r"$\mathcal E < 0$: turns back here\\(bound)", color=YELLOW).scale(0.5).next_to(wall, UP, buff=0.2)
            self.play(rr.animate.set_value(rmax), run_time=2)
            self.play(FadeIn(wall), FadeIn(wl))
            self.wait(1.0)
            self.play(FadeOut(VGroup(wall, wl)), Et.animate.set_value(0.35), rr.animate.set_value(6.0), run_time=2)
            esc = Tx(r"$\mathcal E \ge 0$: never meets the curve (escapes)", color=YELLOW).scale(0.5).next_to(ax.c2p(4.0, 0.35), UP, buff=0.15)
            self.play(FadeIn(esc))
            self.hold()

        with self.voice("o3_16"):
            self.play(FadeOut(esc), Et.animate.set_value(-0.5), rr.animate.set_value(1.6), run_time=1.5)
            climb = Tx("climbs: $V$ up, speed down", color=WHITE).scale(0.55).move_to(ax.c2p(5.5, -1.7))
            self.play(FadeIn(climb))
            self.play(rr.animate.set_value(3.9), run_time=3, rate_func=there_and_back)
            self.play(rr.animate.set_value(3.9), run_time=3, rate_func=there_and_back)
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("o3_17"):
            h, rows = recap(self, [
                r"$\dot{\vec h} = \vec r\times\ddot{\vec r} = \vec 0$: $\vec h = \vec r\times\vec v$ is constant.",
                r"So every orbit is planar, and $h = r^2\dot\theta = r v\cos\gamma = r_p v_p = r_a v_a$.",
                r"$\mathcal E = \dfrac{v^2}{2} - \dfrac{\mu}{r}$ is constant (potential zero at infinity).",
                r"$\mathcal E < 0$: bound.\quad $\mathcal E \ge 0$: can escape.",
            ])
            for rr_ in rows:
                self.play(FadeIn(rr_, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
