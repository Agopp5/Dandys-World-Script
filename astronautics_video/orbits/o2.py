"""Part 2: from Kepler's ellipses to the inverse-square law, and the two-body problem."""
from ocommon import *  # noqa: F401,F403

A, ECC = 2.2, 0.55
P = A * (1 - ECC ** 2)


class O2Concept(OLesson):
    def construct(self):
        with self.voice("o2_01"):
            t = o_title(self, 2, "From Ellipses to Inverse-Square Gravity", "and the two-body problem")
            self.wait(1.5)
            self.play(FadeOut(t))
            hdr = header("Today's plan")
            self.play(FadeIn(hdr))
            items = VGroup(Tx(r"1.\ Kepler II $\Rightarrow$ the force is central \quad(done)", color=DIM),
                           Tx(r"2.\ Kepler I $\Rightarrow$ the force falls off as $1/r^2$"),
                           Tx(r"3.\ Kepler III $\Rightarrow$ one constant $\mu$ for every planet"),
                           Tx(r"4.\ The two-body problem")).scale(0.75)
            items.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
            for it in items:
                self.play(FadeIn(it, shift=RIGHT * 0.2), run_time=0.7)
            self.hold()
        self.play(FadeOut(items))

        # --------------------------------------------------- polar acceleration
        with self.voice("o2_02"):
            self.play(Transform(hdr, header("Acceleration in polar coordinates")))
            bd = Board(self, left=-6.5, top=2.7, scale=0.8, buff=0.42)
            bd.line(r"\vec a = \frac{d}{dt}\big(\dot r\,\hat e_r + r\dot\theta\,\hat e_\theta\big)")
            bd.line(r"= \underbrace{\ddot r\,\hat e_r + \dot r\,\dot{\hat e}_r}_{\text{from } \dot r\hat e_r}"
                    r" + \underbrace{\dot r\dot\theta\,\hat e_\theta + r\ddot\theta\,\hat e_\theta + r\dot\theta\,\dot{\hat e}_\theta}_{\text{from } r\dot\theta\hat e_\theta}",
                    indent=0.6, reason="product rule on each term")
            self.hold()

        with self.voice("o2_03"):
            bd.line(r"= \ddot r\,\hat e_r + \dot r\dot\theta\,\hat e_\theta + \dot r\dot\theta\,\hat e_\theta + r\ddot\theta\,\hat e_\theta - r\dot\theta^2\,\hat e_r",
                    indent=0.6, reason="$\\dot{\\hat e}_r = \\dot\\theta\\hat e_\\theta,\\ \\dot{\\hat e}_\\theta = -\\dot\\theta\\hat e_r$")
            self.hold()

        with self.voice("o2_04"):
            l = bd.line(r"\vec a = \big(\ddot r - r\dot\theta^2\big)\,\hat e_r + \big(2\dot r\dot\theta + r\ddot\theta\big)\,\hat e_\theta",
                        color=YELLOW, reason="collect $\\hat e_r$ and $\\hat e_\\theta$")
            bd.box(l)
            self.hold()

        with self.voice("o2_05"):
            bd.line(r"\frac{1}{r}\frac{d}{dt}\big(r^2\dot\theta\big) = \frac{1}{r}\big(2r\dot r\dot\theta + r^2\ddot\theta\big) = 2\dot r\dot\theta + r\ddot\theta",
                    color=ET_COL, reason="product rule")
            self.hold()

        with self.voice("o2_06"):
            bd.line(r"r^2\dot\theta = h = \text{const}\ \Rightarrow\ a_\theta = 0\ \checkmark", color=Q_COL, reason="consistent with a radial force")
            self.hold()
        bd.clear()

        # --------------------------------------------------- u = 1/r
        with self.voice("o2_07"):
            self.play(Transform(hdr, header("The radial equation")))
            bd = Board(self, left=-6.5, top=2.7, scale=0.8, buff=0.42)
            bd.line(r"f \equiv \frac{F}{m} = \ddot r - r\dot\theta^2", reason="force per unit mass, along $\\hat e_r$")
            bd.line(r"\dot\theta = \frac{h}{r^2}", indent=0.6, reason="from $h = r^2\\dot\\theta$")
            l = bd.line(r"f = \ddot r - \frac{h^2}{r^3}\qquad(1)", color=YELLOW)
            bd.box(l)
            self.hold()

        with self.voice("o2_08"):
            bd.line(r"u \equiv \frac{1}{r},\qquad \frac{d}{dt} = \dot\theta\,\frac{d}{d\theta},\qquad \dot\theta = h\,u^2",
                    color=B_COL, reason="trade time for angle")
            self.hold()

        with self.voice("o2_09"):
            bd.line(r"\dot r = -\frac{1}{u^2}\,\dot u = -\frac{1}{u^2}\,\big(h u^2\big)\,\frac{du}{d\theta} = -h\,\frac{du}{d\theta}",
                    reason="chain rule; the $u^2$ cancel")
            self.hold()

        with self.voice("o2_10"):
            bd.line(r"\ddot r = -h\,\frac{d}{dt}\Big(\frac{du}{d\theta}\Big) = -h\,\dot\theta\,\frac{d^2u}{d\theta^2} = -h^2u^2\,\frac{d^2u}{d\theta^2}",
                    reason="chain rule again")
            self.hold()

        with self.voice("o2_11"):
            l = bd.line(r"f = -h^2u^2\,u'' - h^2u^3 = -h^2u^2\,\big(u'' + u\big)\qquad(2)", color=YELLOW,
                        reason="any central force")
            bd.box(l)
            self.hold()
        bd.clear()

        # --------------------------------------------------- Kepler I -> 1/r^2
        orb = Orb(focus=(-3.6, -0.9), k=0.95)
        ell = orb.conic(P, ECC)
        sn = sun(orb.f)
        semi = Line(orb.f, orb.at(P, ECC, PI / 2), color=V_COL, stroke_width=4)
        semil = T("p", color=V_COL).scale(0.7).next_to(semi, LEFT, buff=0.1)
        th0 = 2.2
        q = orb.at(P, ECC, th0)
        rl = Line(orb.f, q, color=WHITE, stroke_width=3)
        rlab = T("r", color=WHITE).scale(0.6).next_to(rl.get_center(), DOWN, buff=0.1)
        ang = Arc(radius=0.45, start_angle=0, angle=th0, arc_center=orb.f, color=YELLOW)
        angl = T(r"\theta", color=YELLOW).scale(0.55).move_to(orb.f + 0.7 * orb.unit(th0 / 2))
        with self.voice("o2_12"):
            self.play(Transform(hdr, header("Kepler's first law in polar form")))
            self.play(Create(ell), FadeIn(sn))
            self.play(Create(rl), FadeIn(rlab), Create(ang), FadeIn(angl), FadeIn(planet(q)))
            self.play(Create(semi), FadeIn(semil))
            bd = Board(self, left=0.2, top=2.7, scale=0.8, buff=0.42)
            l = bd.line(r"r = \frac{p}{1 + e\cos\theta}", color=YELLOW, reason="$e$: eccentricity, $p$: semi-latus rectum", below=True)
            self.hold()

        with self.voice("o2_13"):
            bd.line(r"u = \frac{1 + e\cos\theta}{p}")
            bd.line(r"u' = -\frac{e}{p}\sin\theta,\qquad u'' = -\frac{e}{p}\cos\theta", indent=0.4)
            self.hold()

        with self.voice("o2_14"):
            l = bd.line(r"u'' + u = ", r"-\frac{e}{p}\cos\theta", r"+ \frac{1}{p}", r"+ \frac{e}{p}\cos\theta", indent=0.4)
            c1 = Line(l[1].get_corner(DL), l[1].get_corner(UR), color=P_COL, stroke_width=3)
            c2 = Line(l[3].get_corner(DL), l[3].get_corner(UR), color=P_COL, stroke_width=3)
            self.play(Create(c1), Create(c2))
            bd.items.add(c1, c2)
            bd.line(r"u'' + u = \frac{1}{p}", indent=0.4, color=Q_COL, reason="a constant!")
            self.hold()

        with self.voice("o2_15"):
            l = bd.line(r"f = -\frac{h^2}{p}\,u^2 = -\frac{h^2}{p}\cdot\frac{1}{r^2}", color=YELLOW, reason="inverse square, attractive")
            bd.box(l)
            fa = Arrow(q, q + 0.9 * (orb.f - q) / np.linalg.norm(orb.f - q), buff=0, color=W_COL, stroke_width=6)
            self.play(GrowArrow(fa))
            self.hold()
        bd.clear()

        # --------------------------------------------------- Kepler III -> mu
        with self.voice("o2_16"):
            self.play(Transform(hdr, header("Kepler's third law: one constant for all")))
            fill = orb.sector(P, ECC, -PI, PI, opacity=0.25)
            self.play(FadeIn(fill), FadeOut(VGroup(rl, rlab, ang, angl, fa)))
            bd = Board(self, left=0.2, top=2.7, scale=0.8, buff=0.42)
            bd.line(r"\frac{dA}{dt} = \frac{h}{2}", reason="Kepler II")
            bd.line(r"\pi a b = \frac{h\,T}{2}\ \Rightarrow\ h = \frac{2\pi a b}{T}", reason="one period sweeps the whole ellipse", below=True)
            self.hold()

        with self.voice("o2_17"):
            bd.line(r"\frac{h^2}{p} = \frac{4\pi^2a^2b^2}{T^2}\cdot\frac{a}{b^2}", reason="$p = b^2/a$")
            l = bd.line(r"\frac{h^2}{p} = \frac{4\pi^2\,a^3}{T^2}", color=YELLOW)
            self.hold()

        with self.voice("o2_18"):
            bd.line(r"\text{Kepler III: } \frac{a^3}{T^2} \text{ same for all planets}", color=Q_COL)
            l = bd.line(r"\mu \equiv \frac{h^2}{p}:\quad f = -\frac{\mu}{r^2},\qquad \ddot{\vec r} = -\frac{\mu}{r^3}\,\vec r", color=YELLOW,
                        reason="$\\mu$: gravitational parameter of the Sun", below=True)
            bd.box(l)
            self.hold()

        with self.voice("o2_19"):
            bd.line(r"\mu = G M,\qquad G = 6.674\times10^{-11}\ \tfrac{\text{m}^3}{\text{kg}\,\text{s}^2}", color=B_COL,
                    reason="Cavendish, 1798")
            bd.line(r"\vec F = -\frac{G M m}{r^2}\,\hat e_r", color=B_COL, reason="universal gravitation")
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(ell, sn, semi, semil, fill)), *[FadeOut(m) for m in self.mobjects if isinstance(m, Dot)])

        # --------------------------------------------------- two-body problem
        Mm, mm = 3.0, 1.0
        o = np.array([-5.6, -2.9, 0])
        axes = VGroup(Arrow(o, o + RIGHT * 1.4, buff=0, color=DIM, stroke_width=3),
                      Arrow(o, o + UP * 1.4, buff=0, color=DIM, stroke_width=3))
        tt = ValueTracker(0.0)
        e2, p2 = 0.45, 2.0
        drift = np.array([0.12, 0.05, 0])
        cm0 = np.array([-3.6, -0.6, 0])

        def rel(t):
            th = theta_from_M(t, e2)
            r = p2 / (1 + e2 * np.cos(th))
            return np.array([r * np.cos(th), r * np.sin(th), 0])

        def cm():
            return cm0 + drift * tt.get_value()

        def p1():
            return cm() - mm / (Mm + mm) * rel(tt.get_value())

        def p2_():
            return cm() + Mm / (Mm + mm) * rel(tt.get_value())
        b1 = always_redraw(lambda: Dot(p1(), radius=0.2, color=SUN))
        b2 = always_redraw(lambda: Dot(p2_(), radius=0.1, color=B_COL))
        r1a = always_redraw(lambda: Arrow(o, p1(), buff=0.0, color=P_COL, stroke_width=3, tip_length=0.15))
        r2a = always_redraw(lambda: Arrow(o, p2_(), buff=0.0, color=Q_COL, stroke_width=3, tip_length=0.15))
        ra = always_redraw(lambda: Arrow(p1(), p2_(), buff=0.1, color=WHITE, stroke_width=3, tip_length=0.15))
        l1 = always_redraw(lambda: T(r"M", color=SUN).scale(0.55).next_to(p1(), UP, buff=0.22))
        l2 = always_redraw(lambda: T(r"m", color=B_COL).scale(0.55).next_to(p2_(), UP, buff=0.12))
        lr1 = always_redraw(lambda: T(r"\vec r_1", color=P_COL).scale(0.55).move_to((o + p1()) / 2 + 0.25 * LEFT + 0.1 * UP))
        lr2 = always_redraw(lambda: T(r"\vec r_2", color=Q_COL).scale(0.55).move_to((o + p2_()) / 2 + 0.25 * DOWN + 0.1 * RIGHT))
        lr = always_redraw(lambda: T(r"\vec r", color=WHITE).scale(0.55).move_to((p1() + p2_()) / 2 + 0.25 * UP))
        with self.voice("o2_20"):
            self.play(Transform(hdr, header("The two-body problem")))
            self.play(FadeIn(axes))
            self.play(FadeIn(b1), FadeIn(b2), FadeIn(l1), FadeIn(l2))
            self.play(GrowArrow(r1a), GrowArrow(r2a), FadeIn(lr1), FadeIn(lr2))
            self.play(GrowArrow(ra), FadeIn(lr))
            bd = Board(self, left=0.2, top=2.7, scale=0.78, buff=0.42)
            bd.line(r"\vec r = \vec r_2 - \vec r_1")
            self.hold()

        with self.voice("o2_21"):
            bd.line(r"m\,\ddot{\vec r}_2 = -\frac{GMm}{r^3}\,\vec r", color=Q_COL)
            bd.line(r"M\,\ddot{\vec r}_1 = +\frac{GMm}{r^3}\,\vec r", color=P_COL, reason="equal and opposite")
            bd.line(r"M\,\ddot{\vec r}_1 + m\,\ddot{\vec r}_2 = \vec 0", reason="add")
            self.hold()

        cmd = always_redraw(lambda: VGroup(Cross(stroke_width=3, scale_factor=0.09).move_to(cm()).set_color(YELLOW)))
        cml = always_redraw(lambda: Tx("CM", color=YELLOW).scale(0.45).next_to(cm(), DOWN, buff=0.12))
        cmtrail = always_redraw(lambda: DashedLine(cm0, cm() + 1e-3 * RIGHT, color=YELLOW, stroke_width=2))
        tr1 = TracedPath(p1, stroke_color=SUN, stroke_width=2, stroke_opacity=0.5)
        tr2 = TracedPath(p2_, stroke_color=B_COL, stroke_width=2, stroke_opacity=0.5)
        with self.voice("o2_22"):
            bd.line(r"\vec r_{cm} = \frac{M\vec r_1 + m\vec r_2}{M + m}\ \Rightarrow\ \ddot{\vec r}_{cm} = \vec 0", color=YELLOW,
                    reason="the CM drifts at constant velocity", below=True)
            self.play(FadeOut(VGroup(r1a, r2a, lr1, lr2, lr, ra)), FadeIn(cmd), FadeIn(cml))
            self.add(cmtrail, tr1, tr2)
            self.play(tt.animate.set_value(2 * TAU), run_time=max(3, self.left() - 0.5), rate_func=linear)
            self.hold()

        with self.voice("o2_23"):
            bd.clear()
            bd = Board(self, left=0.2, top=2.7, scale=0.78, buff=0.42)
            bd.line(r"\ddot{\vec r}_2 = -\frac{GM}{r^3}\,\vec r,\qquad \ddot{\vec r}_1 = +\frac{Gm}{r^3}\,\vec r", reason="divide by each mass", below=True)
            bd.line(r"\ddot{\vec r} = \ddot{\vec r}_2 - \ddot{\vec r}_1 = -\frac{G(M + m)}{r^3}\,\vec r", reason="subtract")
            self.hold()

        with self.voice("o2_24"):
            l = bd.line(r"\ddot{\vec r} = -\frac{\mu}{r^3}\,\vec r,\qquad \mu = G(M + m)", color=YELLOW)
            bd.box(l)
            bd.line(r"m \ll M:\quad \mu \approx GM", indent=0.4, reason="satellites")
            self.play(FadeOut(VGroup(tr1, tr2, cmtrail)))
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("o2_25"):
            h, rows = recap(self, [
                r"$\vec a = (\ddot r - r\dot\theta^2)\,\hat e_r + (2\dot r\dot\theta + r\ddot\theta)\,\hat e_\theta$; the $\hat e_\theta$ part is $\tfrac1r\tfrac{d}{dt}(r^2\dot\theta) = 0$.",
                r"With $u = 1/r$: $f = -h^2u^2(u'' + u)$ for any central force.",
                r"Ellipse $r = p/(1 + e\cos\theta)$ gives $u'' + u = 1/p$, so $f = -\dfrac{h^2}{p}\dfrac{1}{r^2}$.",
                r"Kepler III: $h^2/p = 4\pi^2a^3/T^2 = \mu$ for every planet; $\mu = GM$.",
                r"Two bodies: the CM never accelerates, and $\ddot{\vec r} = -\mu\vec r/r^3$ with $\mu = G(M+m)$.",
            ])
            for rr in rows:
                self.play(FadeIn(rr, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 5 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
