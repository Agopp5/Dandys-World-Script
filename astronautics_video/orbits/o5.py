"""Part 5: anatomy of the ellipse, energy and semi-major axis, vis-viva, period."""
from ocommon import *  # noqa: F401,F403

A, ECC = 2.4, 0.6
C = A * ECC
B = A * np.sqrt(1 - ECC ** 2)
P = A * (1 - ECC ** 2)


def brace_between(p0, p1, tex, color, direction, buff=0.1, scale=0.6):
    br = BraceBetweenPoints(p0, p1, direction=direction, color=color, buff=buff)
    lab = T(tex, color=color).scale(scale).next_to(br, direction, buff=0.08)
    return VGroup(br, lab)


class O5Concept(OLesson):
    def construct(self):
        with self.voice("o5_01"):
            t = o_title(self, 5, "Anatomy of an Ellipse", "geometry, energy, vis-viva and period")
            self.wait(1.2)
            self.play(FadeOut(t))
            hdr = header("Ellipse vocabulary")
            self.play(FadeIn(hdr))
            orb = Orb(focus=(-2.2, -0.4), k=1.0)
            ell = orb.conic(P, ECC)
            Fp = orb.f
            ctr = orb.P(-C, 0)
            F2 = orb.P(-2 * C, 0)
            axis = DashedLine(orb.P(-A - C - 0.2, 0), orb.P(A - C + 0.2, 0), color=DIM, stroke_width=2)
            self.play(Create(ell), Create(axis))
            sF = earth(Fp, 0.15)
            dots = VGroup(Dot(ctr, color=WHITE, radius=0.05), Dot(F2, color=DIM, radius=0.05))
            labs = VGroup(T("C").scale(0.55).next_to(ctr, DOWN, buff=0.1), T("F", color=EARTH).scale(0.55).next_to(Fp, DOWN, buff=0.22),
                          T("F'", color=DIM).scale(0.55).next_to(F2, DOWN, buff=0.1))
            self.play(FadeIn(sF), FadeIn(dots), FadeIn(labs))
            ba = brace_between(ctr + UP * 0.0, orb.P(A - C, 0), "a", YELLOW, UP, buff=0.05)
            ba.shift(UP * (B + 0.1))
            bline = DashedLine(ctr, ctr + UP * B, color=Q_COL)
            bl = T("b", color=Q_COL).scale(0.6).next_to(bline, LEFT, buff=0.08)
            cline = Line(ctr, Fp, color=V_COL, stroke_width=5)
            cl = T("c", color=V_COL).scale(0.6).next_to(cline, DOWN, buff=0.08).shift(UP * 0.0 + RIGHT * 0.25)
            pline = Line(Fp, orb.at(P, ECC, PI / 2), color=B_COL, stroke_width=4)
            pl = T("p", color=B_COL).scale(0.6).next_to(pline, RIGHT, buff=0.08)
            amark = DashedLine(orb.P(A - C, 0), orb.P(A - C, B + 0.1), color=DIM, stroke_width=1.5)
            cmark = DashedLine(ctr, ctr + UP * (B + 0.1), color=DIM, stroke_width=1.5)
            self.play(FadeIn(ba), Create(amark), Create(cmark))
            self.play(Create(bline), FadeIn(bl))
            self.play(Create(cline), FadeIn(cl))
            self.play(Create(pline), FadeIn(pl))
            self.hold()

        with self.voice("o5_02"):
            self.play(Transform(hdr, header("Size from the apsides")))
            rpl = Line(Fp, orb.P(A - C, 0), color=Q_COL, stroke_width=6).shift(DOWN * 0.12)
            ral = Line(orb.P(-A - C, 0), Fp, color=P_COL, stroke_width=6).shift(DOWN * 0.12)
            rpt = T("r_p", color=Q_COL).scale(0.55).next_to(rpl, DOWN, buff=0.08)
            rat = T("r_a", color=P_COL).scale(0.55).next_to(ral, DOWN, buff=0.08).shift(LEFT * 1.4)
            self.play(Create(rpl), Create(ral), FadeIn(rpt), FadeIn(rat))
            bd = Board(self, left=0.9, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"2a = r_p + r_a = \frac{p}{1+e} + \frac{p}{1-e}")
            self.hold()

        with self.voice("o5_03"):
            bd.line(r"= p\,\frac{(1 - e) + (1 + e)}{1 - e^2} = \frac{2p}{1 - e^2}", indent=0.5, reason="common denominator", below=True)
            l = bd.line(r"p = a\,(1 - e^2)", color=YELLOW)
            bd.box(l)
            self.hold()

        with self.voice("o5_04"):
            bd.line(r"r_p = a(1 - e),\qquad r_a = a(1 + e)", color=YELLOW)
            bd.line(r"a = \tfrac12\,(r_p + r_a)", reason="the mean distance")
            self.hold()

        with self.voice("o5_05"):
            bd.line(r"c = a - r_p = a - a(1 - e) = a\,e", color=V_COL)
            bd.line(r"e = c/a", indent=0.5, color=V_COL, reason="focus offset as a fraction of $a$")
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(rpl, ral, rpt, rat)))

        with self.voice("o5_06"):
            self.play(Transform(hdr, header("The semi-minor axis")))
            Bp = ctr + UP * B
            s1 = Line(Bp, Fp, color=YELLOW, stroke_width=5)
            s2 = Line(Bp, F2, color=YELLOW, stroke_width=5).set_opacity(0.6)
            s1l = T("a", color=YELLOW).scale(0.6).next_to(s1.get_center(), UR, buff=0.05)
            s2l = T("a", color=YELLOW).scale(0.6).next_to(s2.get_center(), UL, buff=0.05)
            bdot = Dot(Bp, color=Q_COL)
            self.play(FadeOut(ba), FadeOut(amark), FadeOut(cmark), FadeIn(bdot))
            self.play(Create(s1), Create(s2), FadeIn(s1l), FadeIn(s2l))
            ra = RightAngle(Line(ctr, Fp), Line(ctr, Bp), length=0.2, color=WHITE)
            self.play(Create(ra))
            bd = Board(self, left=0.9, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"\text{string: } |BF| + |BF'| = 2a\ \Rightarrow\ |BF| = a", reason="by symmetry", below=True)
            self.hold()

        with self.voice("o5_07"):
            bd.line(r"b^2 + c^2 = a^2:\quad b^2 + a^2e^2 = a^2")
            l = bd.line(r"b = a\sqrt{1 - e^2},\qquad p = \frac{b^2}{a}", color=YELLOW)
            bd.box(l)
            self.hold()
        bd.clear()

        with self.voice("o5_08"):
            self.play(Transform(hdr, header("Names of the apsides")))
            rows = [("body", "periapsis", "apoapsis"), ("Earth", "perigee", "apogee"), ("Sun", "perihelion", "aphelion"),
                    ("Moon", "perilune", "apolune"), ("Jupiter", "perijove", "apojove")]
            tab = VGroup(*[VGroup(*[Tx(c, color=(B_COL if i == 0 else WHITE)).scale(0.62) for c in row]) for i, row in enumerate(rows)])
            for row in tab:
                for j, c in enumerate(row):
                    c.move_to([1.9 + 1.9 * j, 0, 0])
            tab.arrange(DOWN, buff=0.35).move_to([3.8, 0.4, 0])
            for row in tab:
                for j, c in enumerate(row):
                    c.set_x(1.9 + 1.9 * j)
            ul = Line([0.9, 0, 0], [6.8, 0, 0], color=DIM).next_to(tab[0], DOWN, buff=0.15).set_x(3.85)
            self.play(FadeIn(tab[0]), Create(ul))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in tab[1:]], lag_ratio=0.3), run_time=2.5)
            self.hold()
        self.play(FadeOut(VGroup(tab, ul, bline, bl, cline, cl, pline, pl, ell, axis, sF, dots, labs, bdot, s1, s2, s1l, s2l, ra)))

        # ------------------------------------------------ energy = -mu/2a
        with self.voice("o5_09"):
            self.play(Transform(hdr, header("Energy depends only on $a$")))
            bd = Board(self, left=-6.5, top=2.7, scale=0.8, buff=0.42)
            bd.line(r"\mathcal E = \frac{v^2}{2} - \frac{\mu}{r}\ \ \text{is the same everywhere: use periapsis}")
            bd.line(r"h = r_p\,v_p", indent=0.6, reason="$\\gamma = 0$ at periapsis")
            self.hold()

        with self.voice("o5_10"):
            bd.line(r"h = \sqrt{\mu p} = \sqrt{\mu a(1 - e^2)}", indent=0.6, reason="$p = h^2/\\mu$")
            bd.line(r"v_p = \frac{h}{r_p} = \frac{\sqrt{\mu a(1 - e^2)}}{a(1 - e)}", indent=0.6)
            self.hold()

        with self.voice("o5_11"):
            bd.line(r"v_p^2 = \frac{\mu a(1 - e)(1 + e)}{a^2(1 - e)^2} = \frac{\mu\,(1 + e)}{a\,(1 - e)}", indent=0.6, color=YELLOW, reason="cancel $(1-e)$ and $a$")
            self.hold()

        with self.voice("o5_12"):
            bd.line(r"\mathcal E = \frac{\mu(1 + e)}{2a(1 - e)} - \frac{\mu}{a(1 - e)} = \frac{\mu}{a(1 - e)}\Big[\frac{1 + e}{2} - 1\Big] = \frac{\mu}{a(1 - e)}\cdot\frac{e - 1}{2}",
                    indent=0.6)
            self.hold()

        with self.voice("o5_13"):
            l = bd.line(r"\mathcal E = -\frac{\mu}{2a}", color=YELLOW, reason="no $e$ at all!")
            bd.box(l)
            self.hold()
        bd.clear()

        with self.voice("o5_14"):
            self.play(Transform(hdr, header("The vis-viva equation")))
            bd = Board(self, left=-6.5, top=2.7, scale=0.85, buff=0.45)
            bd.line(r"\frac{v^2}{2} - \frac{\mu}{r} = -\frac{\mu}{2a}")
            l = bd.line(r"v^2 = \mu\Big(\frac{2}{r} - \frac{1}{a}\Big)", color=YELLOW, reason="speed from $r$ and $a$ alone")
            bd.box(l)
            self.hold()

        with self.voice("o5_15"):
            rows = VGroup(T(r"\mathcal E < 0 \iff a > 0:\ \text{ellipse}"), T(r"\mathcal E = 0 \iff a \to \infty:\ \text{parabola}"),
                          T(r"\mathcal E > 0 \iff a < 0:\ \text{hyperbola}")).scale(0.75)
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -1.2, 0])
            for r_ in rows:
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)
            bd.items.add(rows)
            self.hold()
        bd.clear()

        # ------------------------------------------------ circular and escape speeds
        Ec = np.array([2.4, -0.5, 0])
        K = 1.25
        ep = earth(Ec, 0.3)
        L0 = Ec + K * LEFT
        with self.voice("o5_16"):
            self.play(Transform(hdr, header("Circular and escape speed")))
            bd = Board(self, left=-6.5, top=2.7, right=-0.3, scale=0.8, buff=0.45)
            bd.line(r"\text{circle: } r = a")
            l = bd.line(r"v_c^2 = \mu\Big(\frac{2}{r} - \frac{1}{r}\Big) = \frac{\mu}{r}", indent=0.4)
            l = bd.line(r"v_c = \sqrt{\mu/r}", color=YELLOW, indent=0.4, reason="LEO: about 7.7 km/s")
            self.play(FadeIn(ep))
            circ = Circle(radius=K, color=B_COL).move_to(Ec)
            self.play(Create(circ))
            self.hold()

        with self.voice("o5_17"):
            bd.line(r"\text{escape: } \mathcal E = 0")
            bd.line(r"\frac{v_{esc}^2}{2} = \frac{\mu}{r}\ \Rightarrow\ v_{esc} = \sqrt{2\mu/r} = \sqrt2\,v_c", indent=0.4, color=YELLOW)
            bd.line(r"\text{any direction (miss the planet!)}", indent=0.4, color=REASON)
            self.play(FadeOut(circ))
            self.hold()

        with self.voice("o5_18"):
            self.play(FadeIn(Dot(L0, color=WHITE)), GrowArrow(Arrow(L0, L0 + UP * 0.7, buff=0, color=VEL, stroke_width=5, tip_length=0.15)))
            speeds = [(0.8, P_COL, r"0.8\,v_c"), (1.0, B_COL, r"v_c"), (1.2, Q_COL, r"1.2\,v_c"), (np.sqrt(2), YELLOW, r"\sqrt2\,v_c"), (1.6, V_COL, r"1.6\,v_c")]
            leg = VGroup()
            for v, col, lab in speeds:
                p_, e_ = v * v, abs(v * v - 1)
                if v < 0.999:          # launch point is the apoapsis
                    crv = Orb(focus=Ec, k=K, rot=0.0).conic(p_, e_, PI, -PI, color=col, width=3.5)
                elif v < 1.001:
                    crv = Orb(focus=Ec, k=K).conic(1.0, 0.0, PI, -PI, color=col, width=3.5)
                elif e_ < 0.999:       # launch point is the periapsis
                    crv = Orb(focus=Ec, k=K, rot=PI).conic(p_, e_, 0.0, -TAU, color=col, width=3.5)
                elif e_ < 1.001:
                    crv = Orb(focus=Ec, k=K, rot=PI).conic(p_, 1.0, 0.0, -(PI - 0.75), color=col, width=3.5)
                else:
                    crv = Orb(focus=Ec, k=K, rot=PI).conic(p_, e_, 0.0, -(np.arccos(-1 / e_) - 0.25), color=col, width=3.5)
                lg = T(lab, color=col).scale(0.55)
                leg.add(lg)
                lg.move_to([5.9, 2.6 - 0.45 * len(leg), 0])
                self.play(Create(crv), FadeIn(lg), run_time=1.6)
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker) and m is not hdr])))

        # ------------------------------------------------ period
        orb = Orb(focus=(-2.5, -0.5), k=1.0)
        ell = orb.conic(P, ECC)
        Mt = ValueTracker(-PI + 1e-3)
        sweep = always_redraw(lambda: orb.sector(P, ECC, -PI + 1e-3, theta_from_M(Mt.get_value(), ECC), opacity=0.35))
        with self.voice("o5_19"):
            self.play(Transform(hdr, header("The period")))
            self.play(Create(ell), FadeIn(earth(orb.f, 0.15)))
            self.add(sweep)
            self.play(Mt.animate.set_value(PI - 1e-3), run_time=4, rate_func=linear)
            bd = Board(self, left=0.9, top=2.7, scale=0.8, buff=0.42)
            bd.line(r"\frac{dA}{dt} = \frac{h}{2}\ \Rightarrow\ \pi a b = \frac{h\,T}{2}")
            bd.line(r"T = \frac{2\pi a b}{h}", indent=0.5, color=YELLOW)
            self.hold()

        with self.voice("o5_20"):
            bd.line(r"T = \frac{2\pi\,a\cdot a\sqrt{1 - e^2}}{\sqrt{\mu a}\,\sqrt{1 - e^2}}", reason="$b$ and $h$; the roots cancel", below=True)
            l = bd.line(r"T = 2\pi\sqrt{\frac{a^3}{\mu}}", color=YELLOW)
            bd.box(l)
            self.hold()

        with self.voice("o5_21"):
            bd.line(r"T^2 = \frac{4\pi^2}{\mu}\,a^3", color=Q_COL, reason="Kepler III, with the constant")
            bd.line(r"n = \frac{2\pi}{T} = \sqrt{\frac{\mu}{a^3}}", color=B_COL, reason="mean motion")
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("o5_22"):
            h, rows = recap(self, [
                r"$p = a(1 - e^2)$, \ $r_p = a(1 - e)$, \ $r_a = a(1 + e)$, \ $c = ae$, \ $b = a\sqrt{1 - e^2}$.",
                r"$\mathcal E = -\mu/2a$ \ $\Rightarrow$ \ vis-viva: $v^2 = \mu\,(2/r - 1/a)$.",
                r"$v_c = \sqrt{\mu/r}$, \quad $v_{esc} = \sqrt{2\mu/r} = \sqrt2\,v_c$.",
                r"$T = 2\pi\sqrt{a^3/\mu}$, \quad $n = \sqrt{\mu/a^3}$.",
            ])
            for rr in rows:
                self.play(FadeIn(rr, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
