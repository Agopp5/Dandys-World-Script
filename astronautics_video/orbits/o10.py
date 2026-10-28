"""Part 10: HW 3 Problem 1 - the velocity frame: DCM, angular velocity, angular acceleration."""
from ocommon import *  # noqa: F401,F403

A, ECC = 2.2, 0.5
P = A * (1 - ECC ** 2)
F0 = np.radians(132)
BETA = np.arctan2(ECC * np.sin(F0), 1 + ECC * np.cos(F0))
IN_COL, IV_COL = "#FF9A3C", VEL


class O10Problem(OLesson):
    def construct(self):
        orb = Orb(focus=(-1.6, -0.6), k=1.0)
        ell = orb.conic(P, ECC)
        q = orb.at(P, ECC, F0)
        L = 1.15

        def arrow(ang, col):
            return Arrow(q, q + L * orb.unit(ang), buff=0, color=col, stroke_width=5, tip_length=0.16)

        def lab(tex, ang, col, d=0.3):
            return T(tex, color=col).scale(0.58).move_to(q + (L + d) * orb.unit(ang))
        ar, at = arrow(F0, ER_COL), arrow(F0 + PI / 2, ET_COL)
        av, an = arrow(F0 + PI / 2 - BETA, IV_COL), arrow(F0 - BETA, IN_COL)
        lr, lt = lab(r"\hat i_r", F0, ER_COL), lab(r"\hat i_\theta", F0 + PI / 2, ET_COL)
        lv, ln = lab(r"\hat i_v", F0 + PI / 2 - BETA, IV_COL), lab(r"\hat i_n", F0 - BETA, IN_COL)
        pe = Arrow(orb.f, orb.f + 1.2 * RIGHT, buff=0, color=P_COL, stroke_width=4, tip_length=0.14)
        pq = Arrow(orb.f, orb.f + 1.2 * UP, buff=0, color=Q_COL, stroke_width=4, tip_length=0.14)
        pel = T(r"\hat i_e", color=P_COL).scale(0.55).next_to(pe, RIGHT, buff=0.08)
        pql = T(r"\hat i_p", color=Q_COL).scale(0.55).next_to(pq, UP, buff=0.08)
        rl = Line(orb.f, q, color=WHITE, stroke_width=2.5)
        fa = Arc(radius=0.45, start_angle=0, angle=F0, arc_center=orb.f, color=YELLOW)
        fl = T("f", color=YELLOW).scale(0.6).move_to(orb.f + 0.7 * orb.unit(F0 / 2))

        with self.voice("o10_01"):
            t = o_title(self, 10, "HW 3, Problem 1: The Velocity Frame", "its DCM, angular velocity and angular acceleration")
            self.wait(1.2)
            self.play(FadeOut(t))
            hdr = header("HW 3, Problem 1")
            self.play(FadeIn(hdr))
            self.play(Create(ell), FadeIn(earth(orb.f, 0.14)))
            self.play(GrowArrow(pe), GrowArrow(pq), FadeIn(pel), FadeIn(pql))
            self.play(Create(rl), Create(fa), FadeIn(fl), FadeIn(Dot(q, color=WHITE, radius=0.06)))
            self.play(GrowArrow(ar), GrowArrow(at), FadeIn(lr), FadeIn(lt))
            self.play(GrowArrow(av), GrowArrow(an), FadeIn(lv), FadeIn(ln))
            task = VGroup(Tx(r"$\mathcal V = \{\hat i_n, \hat i_v, \hat i_h\}$, \ $\mathcal O = \{\hat i_r, \hat i_\theta, \hat i_h\}$"),
                          Tx(r"$\bullet$ \ $C^{\mathcal{VO}}(e, f)$"),
                          Tx(r"$\bullet$ \ $\vec\omega^{\mathcal V/\mathcal P}$ and $\vec\alpha^{\mathcal V/\mathcal P}$")).scale(0.62)
            task.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 1.6, 0])
            self.play(FadeIn(task))
            self.hold()
        self.play(FadeOut(task))

        hz = DashedLine(q - 0.8 * orb.unit(F0 + PI / 2), q + 1.5 * orb.unit(F0 + PI / 2), color=ET_COL, stroke_width=2)
        b1 = Arc(radius=0.75, start_angle=F0 + PI / 2, angle=-BETA, arc_center=q, color=YELLOW, stroke_width=4)
        b2 = Arc(radius=0.75, start_angle=F0, angle=-BETA, arc_center=q, color=YELLOW, stroke_width=4)
        bl1 = T(r"\beta", color=YELLOW).scale(0.55).move_to(q + 1.0 * orb.unit(F0 + PI / 2 - BETA / 2))
        bl2 = T(r"\beta", color=YELLOW).scale(0.55).move_to(q + 1.0 * orb.unit(F0 - BETA / 2))
        with self.voice("o10_02"):
            self.play(Create(b1), FadeIn(bl1))
            bd = Board(self, left=0.6, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"\beta = \gamma", color=YELLOW, reason="the flight-path angle: from $\\hat i_\\theta$ up to $\\vec v$")
            self.play(Create(b2), FadeIn(bl2))
            self.hold()

        with self.voice("o10_03"):
            bd.line(r"\hat i_v = \sin\beta\,\hat i_r + \cos\beta\,\hat i_\theta", color=IV_COL, reason="tips toward $\\hat i_r$ while climbing")
            bd.line(r"\hat i_n = \cos\beta\,\hat i_r - \sin\beta\,\hat i_\theta", color=IN_COL, reason="$\\perp \\hat i_v$, with $\\hat i_n\\times\\hat i_v = \\hat i_h$", below=True)
            self.hold()

        with self.voice("o10_04"):
            bd.line(r"\hat i_n\times\hat i_v = (\cos^2\beta + \sin^2\beta)\,\hat i_r\times\hat i_\theta = \hat i_h\ \checkmark", color=Q_COL)
            self.hold()

        with self.voice("o10_05"):
            m = mat([[r"\cos\beta", r"-\sin\beta", "0"], [r"\sin\beta", r"\cos\beta", "0"], ["0", "0", "1"]], scale=0.6)
            row = VGroup(T(r"C^{\mathcal{VO}} =").scale(0.72), m, T(r"= C_3(-\beta)", color=YELLOW).scale(0.72)).arrange(RIGHT, buff=0.15)
            bd.line(None, mob=row, reason="rows: $\\mathcal V$ axes in $\\mathcal O$", below=True)
            self.hold()
        bd.clear()

        # tan(beta) triangle
        with self.voice("o10_06"):
            bd = Board(self, left=0.6, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"\tan\beta = \frac{v_r}{v_\theta} = \frac{e\sin f}{1 + e\cos f}")
            o_ = np.array([1.4, -2.6, 0])
            W, H = 3.0, 1.35
            tri = Polygon(o_, o_ + RIGHT * W, o_ + RIGHT * W + UP * H, color=WHITE, stroke_width=3)
            adj = T(r"1 + e\cos f", color=ET_COL).scale(0.55).next_to(tri, DOWN, buff=0.1)
            opp = T(r"e\sin f", color=ER_COL).scale(0.55).next_to(o_ + RIGHT * W + UP * H / 2, RIGHT, buff=0.1)
            ang = Arc(radius=0.6, start_angle=0, angle=np.arctan2(H, W), arc_center=o_, color=YELLOW)
            angl = T(r"\beta", color=YELLOW).scale(0.55).move_to(o_ + 0.85 * np.array([np.cos(0.2), np.sin(0.2), 0]))
            self.play(Create(tri), FadeIn(adj), FadeIn(opp), Create(ang), FadeIn(angl))
            self.hold()

        with self.voice("o10_07"):
            hyp = T(r"k", color=YELLOW).scale(0.6).next_to(tri.get_center() + UP * 0.25 + LEFT * 0.3, UL, buff=0.0)
            self.play(FadeIn(hyp))
            bd.line(r"k^2 = (1 + e\cos f)^2 + e^2\sin^2 f")
            bd.line(r"= 1 + 2e\cos f + e^2\cos^2 f + e^2\sin^2 f", indent=0.5)
            l = bd.line(r"k = \sqrt{1 + 2e\cos f + e^2}", color=YELLOW, indent=0.5)
            self.hold()

        with self.voice("o10_08"):
            self.play(FadeOut(VGroup(tri, adj, opp, ang, angl, hyp)))
            bd.line(r"\sin\beta = \frac{e\sin f}{k},\qquad \cos\beta = \frac{1 + e\cos f}{k}")
            m = mat([[r"1 + e\cos f", r"-e\sin f", "0"], [r"e\sin f", r"1 + e\cos f", "0"], ["0", "0", "k"]], scale=0.56, h_buff=1.9)
            row = VGroup(T(r"C^{\mathcal{VO}} = \frac{1}{k}").scale(0.72), m).arrange(RIGHT, buff=0.15)
            l = bd.line(None, mob=row, reason="$e = 0$: identity \\checkmark", below=True)
            bd.box(l)
            self.hold()
        bd.clear()

        # ---------------------------------------------------------------- omega
        with self.voice("o10_09"):
            self.play(Transform(hdr, header("Angular velocity of $\\mathcal V$ relative to $\\mathcal P$")))
            bd = Board(self, left=0.6, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"\vec\omega^{\mathcal V/\mathcal P} = \vec\omega^{\mathcal V/\mathcal O} + \vec\omega^{\mathcal O/\mathcal P}", reason="addition rule")
            bd.line(r"\vec\omega^{\mathcal O/\mathcal P} = \dot f\,\hat i_h,\qquad \vec\omega^{\mathcal V/\mathcal O} = -\dot\beta\,\hat i_h", indent=0.4)
            self.hold()

        with self.voice("o10_10"):
            l = bd.line(r"\vec\omega^{\mathcal V/\mathcal P} = (\dot f - \dot\beta)\,\hat i_h", color=YELLOW)
            na = Arc(radius=0.7, start_angle=0, angle=F0 - BETA, arc_center=orb.f, color=IN_COL, stroke_width=4)
            ref = DashedLine(orb.f, orb.f + 1.8 * orb.unit(F0 - BETA), color=IN_COL)
            nl = T(r"f - \beta", color=IN_COL).scale(0.55).move_to(orb.f + 1.05 * orb.unit((F0 - BETA) / 2) + 0.1 * UP)
            self.play(Create(ref), Create(na), FadeIn(nl))
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(na, ref, nl)))

        with self.voice("o10_11"):
            bd = Board(self, left=0.6, top=2.7, scale=0.76, buff=0.38)
            bd.line(r"\frac{d}{dt}\big(\tan\beta\big) = \sec^2\beta\;\dot\beta", reason="left side")
            bd.line(r"\frac{d}{dt}\Big(\frac{e\sin f}{1 + e\cos f}\Big) = \frac{d}{df}\Big(\cdots\Big)\,\dot f", reason="right side")
            self.hold()

        with self.voice("o10_12"):
            bd.line(r"= \frac{e\cos f\,(1 + e\cos f) - e\sin f\,(-e\sin f)}{(1 + e\cos f)^2}\,\dot f", indent=0.4, reason="quotient rule", below=True)
            bd.line(r"= \frac{e\,(e + \cos f)}{(1 + e\cos f)^2}\,\dot f", indent=0.4)
            self.hold()

        with self.voice("o10_13"):
            bd.line(r"\sec^2\beta = \frac{k^2}{(1 + e\cos f)^2}", reason="$1/\\cos^2\\beta$")
            l = bd.line(r"\dot\beta = \frac{e\,(e + \cos f)}{k^2}\,\dot f", color=YELLOW)
            self.hold()
        bd.clear()

        with self.voice("o10_14"):
            bd = Board(self, left=0.6, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"\dot f - \dot\beta = \dot f\,\frac{k^2 - e^2 - e\cos f}{k^2}")
            bd.line(r"= \dot f\,\frac{1 + e\cos f}{k^2}", indent=0.5, reason="$k^2 = 1 + 2e\\cos f + e^2$")
            self.hold()

        with self.voice("o10_15"):
            bd.line(r"\dot f = \sqrt{\mu/p^3}\,(1 + e\cos f)^2", reason="from Part 6")
            l = bd.line(r"\vec\omega^{\mathcal V/\mathcal P} = \sqrt{\frac{\mu}{p^3}}\;\frac{(1 + e\cos f)^3}{1 + 2e\cos f + e^2}\;\hat i_h", color=YELLOW)
            bd.box(l)
            bd.line(r"\sqrt{\mu/p^3} = n/(1 - e^2)^{3/2}", indent=0.5, color=REASON, reason="a constant of the orbit")
            self.hold()

        with self.voice("o10_16"):
            bd.line(r"e = 0:\ \ \omega = \sqrt{\mu/r^3} = n\ \checkmark", color=Q_COL, reason="turns with the orbit")
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker) and m is not hdr])))

        # ---------------------------------------------------------------- alpha
        with self.voice("o10_17"):
            self.play(Transform(hdr, header("Angular acceleration")))
            bd = Board(self, left=-6.5, top=2.7, scale=0.8, buff=0.42)
            bd.line(r"\vec\alpha^{\mathcal V/\mathcal P} = \frac{d\omega}{dt}\,\hat i_h = \sqrt{\frac{\mu}{p^3}}\;g'(f)\,\dot f\;\hat i_h",
                    reason="$\\hat i_h$ is fixed in both frames")
            bd.line(r"g(f) = \frac{(1 + e\cos f)^3}{k^2},\qquad k^2 = 1 + 2e\cos f + e^2", indent=0.6)
            self.hold()

        with self.voice("o10_18"):
            bd.line(r"g' = \frac{3(1 + e\cos f)^2(-e\sin f)\,k^2 - (1 + e\cos f)^3(-2e\sin f)}{k^4}", indent=0.6, reason="quotient rule")
            bd.line(r"= \frac{-e\sin f\,(1 + e\cos f)^2\,\big[\,3k^2 - 2(1 + e\cos f)\,\big]}{k^4}", indent=0.6, reason="factor")
            self.hold()

        with self.voice("o10_19"):
            bd.line(r"3k^2 - 2(1 + e\cos f) = 3 + 6e\cos f + 3e^2 - 2 - 2e\cos f = 1 + 4e\cos f + 3e^2", indent=0.6, color=B_COL)
            self.hold()

        with self.voice("o10_20"):
            l = bd.line(r"\vec\alpha^{\mathcal V/\mathcal P} = -\frac{\mu}{p^3}\;\frac{e\sin f\,(1 + e\cos f)^4\,(1 + 4e\cos f + 3e^2)}{(1 + 2e\cos f + e^2)^2}\;\hat i_h",
                        color=YELLOW, reason="multiply by $\\sqrt{\\mu/p^3}$ and $\\dot f$", below=True)
            bd.box(l)
            self.hold()
        bd.clear()

        # plots
        e = 0.5
        fs = np.linspace(0, TAU, 400)
        wv = (1 + e * np.cos(fs)) ** 3 / (1 + 2 * e * np.cos(fs) + e * e)
        av_ = -e * np.sin(fs) * (1 + e * np.cos(fs)) ** 4 * (1 + 4 * e * np.cos(fs) + 3 * e * e) / (1 + 2 * e * np.cos(fs) + e * e) ** 2
        amax = float(np.max(np.abs(av_))) * 1.15
        with self.voice("o10_21"):
            ax1 = Axes(x_range=[0, TAU, PI / 2], y_range=[0, 1.8, 0.5], x_length=9, y_length=2.4,
                       axis_config={"color": DIM, "include_ticks": False}).move_to([0.4, 1.3, 0])
            ax2 = Axes(x_range=[0, TAU, PI / 2], y_range=[-amax, amax, 0.5], x_length=9, y_length=2.6,
                       axis_config={"color": DIM, "include_ticks": False}).move_to([0.4, -1.9, 0])
            l1 = T(r"\omega\,/\sqrt{\mu/p^3}", color=YELLOW).scale(0.55).next_to(ax1, LEFT, buff=0.15)
            l2 = T(r"\alpha\,/(\mu/p^3)", color=V_COL).scale(0.55).next_to(ax2, LEFT, buff=0.15)
            c1 = ax1.plot_line_graph(fs, wv, add_vertex_dots=False, line_color=YELLOW, stroke_width=4)
            c2 = ax2.plot_line_graph(fs, av_, add_vertex_dots=False, line_color=V_COL, stroke_width=4)
            ticks = VGroup(*[T(s, color=DIM).scale(0.45).next_to(ax2.c2p(x, -amax), DOWN, buff=0.1)
                             for x, s in [(0, "0"), (PI, r"180^\circ"), (TAU, r"360^\circ")]])
            fx = T("f", color=DIM).scale(0.55).next_to(ax2.c2p(TAU, -amax), RIGHT, buff=0.15)
            et = Tx(r"$e = 0.5$", color=WHITE).scale(0.6).to_corner(UR, buff=0.4)
            self.play(Create(ax1), Create(ax2), FadeIn(l1), FadeIn(l2), FadeIn(ticks), FadeIn(fx), FadeIn(et))
            self.play(Create(c1), Create(c2), run_time=3)
            zs = VGroup(*[Dot(ax2.c2p(x, 0), color=WHITE, radius=0.06) for x in (0, PI, TAU)])
            self.play(FadeIn(zs))
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("o10_22"):
            h, rows = recap(self, [
                r"$\mathcal V$ is $\mathcal O$ turned by $-\beta$ about $\hat i_h$, with $\beta = \gamma$: \ $C^{\mathcal{VO}} = C_3(-\beta)$.",
                r"$\sin\beta = e\sin f/k$, \ $\cos\beta = (1 + e\cos f)/k$, \ $k = \sqrt{1 + 2e\cos f + e^2}$.",
                r"$\omega^{\mathcal V/\mathcal P} = \dot f - \dot\beta = \sqrt{\mu/p^3}\,(1 + e\cos f)^3/k^2$.",
                r"$\alpha^{\mathcal V/\mathcal P} = -\dfrac{\mu}{p^3}\,\dfrac{e\sin f\,(1+e\cos f)^4(1 + 4e\cos f + 3e^2)}{k^4}$.",
            ])
            for rr in rows:
                self.play(FadeIn(rr, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
