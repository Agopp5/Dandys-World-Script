"""Part 8: worked examples on closed orbits - HW 3 P3 and textbook 2.16, 2.17, 2.28, 2.32."""
from ocommon import *  # noqa: F401,F403

MU = 3.986e5
RE = 6378.0


def given(rows, at=(-4.4, 1.6), scale=0.58):
    c = num_card(rows, scale=scale)
    c.move_to([at[0], at[1], 0])
    return c


class O8Examples(OLesson):
    def construct(self):
        with self.voice("o8_01"):
            t = o_title(self, 8, "Worked Examples: Closed Orbits", "HW 3 Problem 3 and textbook 2.16, 2.17, 2.28, 2.32")
            self.wait(1.5)
            self.play(FadeOut(t))
            hdr = header("Constants used")
            self.play(FadeIn(hdr))
            c = VGroup(T(r"\mu_\oplus = 3.986\times10^5\ \text{km}^3/\text{s}^2"), T(r"R_\oplus = 6378\ \text{km}")).scale(0.85)
            c.arrange(DOWN, buff=0.45)
            self.play(FadeIn(c))
            self.hold()
        self.play(FadeOut(c))

        # ------------------------------------------------ HW 3 P3
        A, E = 2.0, 0.55
        Pp = A * (1 - E ** 2)
        Bb = A * np.sqrt(1 - E ** 2)
        orb = Orb(focus=(-3.2, -1.2), k=0.95)
        ell = orb.conic(Pp, E)
        ctr = orb.P(-A * E, 0)
        with self.voice("o8_02"):
            self.play(Transform(hdr, header("HW 3, Problem 3: three ellipse identities")))
            self.play(Create(ell), FadeIn(earth(orb.f, 0.13)))
            rpl = Line(orb.f, orb.P(A - A * E, 0), color=Q_COL, stroke_width=5)
            ral = Line(orb.P(-A - A * E, 0), orb.f, color=P_COL, stroke_width=5)
            rpt = T("r_p", color=Q_COL).scale(0.55).next_to(rpl, DOWN, buff=0.08)
            rat = T("r_a", color=P_COL).scale(0.55).next_to(ral, DOWN, buff=0.08)
            bl = DashedLine(ctr, ctr + UP * Bb * orb.k, color=B_COL)
            btx = T("b", color=B_COL).scale(0.55).next_to(bl, LEFT, buff=0.06)
            self.play(Create(rpl), Create(ral), FadeIn(rpt), FadeIn(rat), Create(bl), FadeIn(btx))
            bd = Board(self, left=-1.0, top=2.7, scale=0.78, buff=0.42)
            bd.line(r"r_p + r_a = a(1 - e) + a(1 + e) = 2a")
            l = bd.line(r"a = \tfrac12\,(r_p + r_a)\ \checkmark", color=YELLOW)
            self.hold()

        with self.voice("o8_03"):
            bd.line(r"r_p\,r_a = a^2(1 - e)(1 + e) = a^2(1 - e^2) = b^2", reason="$b = a\\sqrt{1 - e^2}$")
            l = bd.line(r"b = \sqrt{r_p\,r_a}\ \checkmark", color=YELLOW)
            self.hold()

        with self.voice("o8_04"):
            bd.line(r"p = \frac{b^2}{a} = \frac{r_p\,r_a}{\tfrac12(r_p + r_a)}")
            l = bd.line(r"p = \frac{2\,r_p\,r_a}{r_p + r_a}\ \checkmark", color=YELLOW)
            bd.box(l)
            self.hold()

        with self.voice("o8_05"):
            note = VGroup(Tx(r"Sheet prints $\dfrac{2r_pr_a}{r_p + r_a + a}$: the extra $a$ looks like a typo.", color=P_COL),
                          Tx(r"Circle check ($r_p = r_a = r$): \ $\dfrac{2r^2}{2r} = r$ \ \checkmark \qquad $\dfrac{2r^2}{3r} = \tfrac23 r$ \ $\times$", color=WHITE)).scale(0.58)
            note.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, -2.3, 0])
            self.play(FadeIn(note))
            self.hold()

        with self.voice("o8_06"):
            self.play(FadeOut(note))
            bd.line(r"\frac{1}{p} = \frac12\Big(\frac{1}{r_p} + \frac{1}{r_a}\Big)", color=Q_COL, reason="$p$ is the harmonic mean", below=True)
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker) and m is not hdr])))

        # ------------------------------------------------ 2.16
        Ec = np.array([-4.4, -1.3, 0])
        Rs = 1.15
        ep = Circle(radius=Rs, color=EARTH, fill_color="#16335C", fill_opacity=1).move_to(Ec)
        orb = Orb(focus=Ec, k=1.0, rot=PI * 0.75)
        rp_s, ra_s = 0.92, 1.75
        a_s, e_s = (rp_s + ra_s) / 2, (ra_s - rp_s) / (ra_s + rp_s)
        orbit = orb.conic(a_s * (1 - e_s ** 2), e_s, color=YELLOW, width=3)
        with self.voice("o8_07"):
            self.play(Transform(hdr, header("Problem 2.16: has it reached orbit?")))
            g = given([r"h_{bo} = 250\ \text{km}", r"v = 7.791\ \text{km/s}", r"\gamma = 4.5^\circ"], at=(-4.4, 2.0))
            self.play(FadeIn(g))
            self.play(FadeIn(ep))
            bd = Board(self, left=-1.6, top=2.7, scale=0.76, buff=0.4)
            bd.line(r"\text{plan: } \mathcal E \to a,\quad h \to p,\quad \text{then } e,\ r_p", color=B_COL)
            self.hold()

        with self.voice("o8_08"):
            bd.line(r"r = 6378 + 250 = 6628\ \text{km}")
            bd.line(r"\mathcal E = \frac{7.791^2}{2} - \frac{3.986\times10^5}{6628} = 30.35 - 60.14 = -29.79\ \tfrac{\text{km}^2}{\text{s}^2}",
                    reason="$< 0$: closed", below=True)
            bd.line(r"a = -\frac{\mu}{2\mathcal E} = 6690.4\ \text{km}", color=YELLOW)
            self.hold()

        with self.voice("o8_09"):
            bd.line(r"h = r v\cos\gamma = 6628\,(7.791)\cos 4.5^\circ = 51{,}480\ \tfrac{\text{km}^2}{\text{s}}")
            bd.line(r"p = h^2/\mu = 6648.6\ \text{km}", color=YELLOW)
            self.hold()

        with self.voice("o8_10"):
            bd.line(r"e = \sqrt{1 - p/a} = \sqrt{1 - \tfrac{6648.6}{6690.4}} = 0.0790", color=YELLOW, reason="from $p = a(1-e^2)$")
            self.hold()

        with self.voice("o8_11"):
            l = bd.line(r"r_p = a(1 - e) = 6161.8\ \text{km} < R_\oplus = 6378\ \text{km}", color=P_COL)
            bd.box(l, color=P_COL)
            self.play(Create(orbit), run_time=2)
            pp = orb.at(a_s * (1 - e_s ** 2), e_s, 0)
            x = Cross(stroke_width=4, scale_factor=0.12).move_to(pp).set_color(P_COL)
            lab = Tx(r"perigee $\approx$ 216 km\\underground (schematic)", color=P_COL).scale(0.5).next_to(ep, DOWN, buff=0.15)
            self.play(FadeIn(x), FadeIn(lab))
            no = Tx(r"Not a stable orbit: it re-enters and impacts.", color=YELLOW).scale(0.65).move_to([2.6, -3.3, 0])
            self.play(FadeIn(no))
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker) and m is not hdr])))

        # ------------------------------------------------ 2.17
        Ec = np.array([-3.9, -0.9, 0])
        k = 1.65 / 7178
        rA = 7178.0
        aB = 7954.9
        eB = (2 * aB - 2 * rA) / (2 * aB)
        pB = aB * (1 - eB ** 2)
        orb = Orb(focus=Ec, k=k)
        circA = Circle(radius=rA * k, color=B_COL, stroke_width=3).move_to(Ec)
        ellB = orb.conic(pB, eB, color=YELLOW, width=3)
        tt = ValueTracker(0.0)               # in units of B's period
        nA = 7 / 6 * TAU

        def posA():
            ang = -PI / 3 + nA * tt.get_value()
            return Ec + rA * k * np.array([np.cos(ang), np.sin(ang), 0])

        def posB():
            return orb.at(pB, eB, theta_from_M(TAU * tt.get_value(), eB))
        dA = always_redraw(lambda: Dot(posA(), color=B_COL, radius=0.09))
        dB = always_redraw(lambda: Dot(posB(), color=YELLOW, radius=0.09))
        lA = always_redraw(lambda: T("A", color=B_COL).scale(0.55).next_to(posA(), DL, buff=0.05))
        lB = always_redraw(lambda: T("B", color=YELLOW).scale(0.55).next_to(posB(), UR, buff=0.05))
        with self.voice("o8_12"):
            self.play(Transform(hdr, header("Problem 2.17: a rendezvous by timing")))
            self.play(FadeIn(earth(Ec, 0.3)), Create(circA), Create(ellB))
            self.play(FadeIn(dA), FadeIn(dB), FadeIn(lA), FadeIn(lB))
            sep = Arc(radius=0.75, start_angle=-PI / 3, angle=PI / 3, arc_center=Ec, color=WHITE)
            sepl = T(r"60^\circ").scale(0.5).next_to(sep, RIGHT, buff=0.05).shift(DOWN * 0.25)
            self.play(Create(sep), FadeIn(sepl))
            bd = Board(self, left=0.0, top=2.7, scale=0.76, buff=0.4)
            bd.line(r"h_A = 800\ \text{km circular};\quad B:\ h_p = 800\ \text{km}", reason="find $h_a$ of $B$", below=True)
            self.hold()

        with self.voice("o8_13"):
            self.play(FadeOut(VGroup(sep, sepl)))
            bd.line(r"a_B > r_A\ \Rightarrow\ T_B > T_A", reason="bigger orbit, longer period")
            bd.line(r"\text{in } T_B,\ A \text{ covers } 60^\circ + 360^\circ = 420^\circ")
            l = bd.line(r"T_B = \tfrac{420}{360}\,T_A = \tfrac76\,T_A", color=YELLOW)
            self.play(tt.animate.set_value(1.0), run_time=6, rate_func=linear)
            meet = Tx("they meet at perigee", color=Q_COL).scale(0.55).next_to(posB(), RIGHT, buff=0.3)
            self.play(FadeIn(meet))
            self.hold()

        with self.voice("o8_14"):
            self.play(FadeOut(meet))
            bd.line(r"r_A = 6378 + 800 = 7178\ \text{km}")
            bd.line(r"T_A = 2\pi\sqrt{r_A^3/\mu} = 6052.2\ \text{s} \approx 100.9\ \text{min}")
            bd.line(r"T_B = \tfrac76(6052.2) = 7061.0\ \text{s}", color=YELLOW)
            self.hold()

        with self.voice("o8_15"):
            bd.line(r"a_B = \Big[\mu\Big(\frac{T_B}{2\pi}\Big)^2\Big]^{1/3} = 7954.9\ \text{km}", reason="or $7178\\,(7/6)^{2/3}$")
            self.hold()

        with self.voice("o8_16"):
            bd.line(r"r_a = 2a_B - r_p = 2(7954.9) - 7178 = 8731.8\ \text{km}")
            l = bd.line(r"h_a = 8731.8 - 6378 \approx 2354\ \text{km}", color=YELLOW)
            bd.box(l)
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker) and m is not hdr])))

        # ------------------------------------------------ 2.28
        Ec = np.array([-0.2, -1.6, 0])
        k = 1.0 / 7000 * 0.62
        rp = 6678.0
        orb = Orb(focus=Ec, k=k, rot=PI)
        with self.voice("o8_17"):
            self.play(Transform(hdr, header("Problem 2.28: Chandra's transfer orbits")))
            ep2 = earth(Ec, RE * k)
            self.play(FadeIn(ep2))
            cols = [B_COL, YELLOW]
            curves = VGroup()
            for ha, col in zip((13200, 72000), cols):
                ra = RE + ha
                e_ = (ra - rp) / (ra + rp)
                a_ = (ra + rp) / 2
                curves.add(orb.conic(a_ * (1 - e_ ** 2), e_, color=col, width=3))
            self.play(Create(curves[0]), run_time=1.5)
            self.play(Create(curves[1]), run_time=2)
            labs = VGroup(Tx("orbit 1", color=B_COL).scale(0.5).next_to(curves[0], UP, buff=0.05),
                          Tx("orbit 2", color=YELLOW).scale(0.5).move_to([3.4, 0.75, 0]))
            self.play(FadeIn(labs))
            g = given([r"h_p = 300\ \text{km (both)}", r"h_{a,1} = 13{,}200\ \text{km}", r"h_{a,2} = 72{,}000\ \text{km}"], at=(4.5, 2.2))
            self.play(FadeIn(g))
            self.hold()
        self.play(FadeOut(VGroup(curves, labs, ep2)))

        with self.voice("o8_18"):
            bd = Board(self, left=-6.5, top=2.7, right=2.0, scale=0.76, buff=0.42)
            bd.line(r"a = \tfrac12\,(r_p + r_a)")
            bd.line(r"r_a - r_p = 2ae,\quad r_a + r_p = 2a\ \Rightarrow\ e = \frac{r_a - r_p}{r_a + r_p}")
            bd.line(r"T = 2\pi\sqrt{a^3/\mu}")
            self.hold()

        with self.voice("o8_19"):
            bd.line(r"\textbf{1: } r_p = 6678,\ r_a = 19{,}578\ \text{km}", color=B_COL)
            bd.line(r"a = 13{,}128\ \text{km},\quad e = 0.4913", color=B_COL, indent=0.4)
            bd.line(r"T = 14{,}970\ \text{s} = 4.16\ \text{h}", color=YELLOW, indent=0.4)
            self.hold()

        with self.voice("o8_20"):
            bd.line(r"\textbf{2: } r_a = 78{,}378\ \text{km}", color=V_COL)
            bd.line(r"a = 42{,}528\ \text{km},\quad e = 0.8430", color=V_COL, indent=0.4)
            bd.line(r"T = 87{,}282\ \text{s} = 24.24\ \text{h} \approx 1\ \text{day}", color=YELLOW, indent=0.4)
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker) and m is not hdr])))

        # ------------------------------------------------ 2.32
        mm, Rm = 4902.8, 1737.5
        h_, E_ = 3509.8, -0.886641
        a_ = -mm / (2 * E_)
        p_ = h_ ** 2 / mm
        e_ = np.sqrt(1 - p_ / a_)
        Mc = np.array([-3.4, -1.0, 0])
        k = 1.0 / 1300
        orb = Orb(focus=Mc, k=k)
        moon = Circle(radius=Rm * k, color=GREY_B, fill_color="#3A3A44", fill_opacity=1).move_to(Mc)
        with self.voice("o8_21"):
            self.play(Transform(hdr, header("Problem 2.32: Lunar Orbiter 1")))
            self.play(FadeIn(moon), Create(orb.conic(p_, e_, color=YELLOW, width=3)))
            g = given([r"h = 3509.8\ \text{km}^2/\text{s}", r"\mathcal E = -0.886641\ \text{km}^2/\text{s}^2",
                       r"\mu_{\text{Moon}} = 4902.8\ \text{km}^3/\text{s}^2", r"R_{\text{Moon}} = 1737.5\ \text{km}"], at=(-4.3, 2.4), scale=0.52)
            self.play(FadeIn(g))
            self.hold()

        with self.voice("o8_22"):
            bd = Board(self, left=-0.4, top=2.7, scale=0.74, buff=0.38)
            bd.line(r"a = -\frac{\mu}{2\mathcal E} = 2764.8\ \text{km}")
            bd.line(r"p = \frac{h^2}{\mu} = 2512.6\ \text{km}")
            bd.line(r"e = \sqrt{1 - p/a} = 0.3020", color=YELLOW)
            self.hold()

        with self.voice("o8_23"):
            bd.line(r"r_p = a(1 - e) = 1929.7\ \text{km}\ \to\ 192.2\ \text{km alt.}", color=Q_COL)
            bd.line(r"r_a = a(1 + e) = 3599.9\ \text{km}\ \to\ 1862.4\ \text{km alt.}", color=P_COL)
            self.hold()

        with self.voice("o8_24"):
            bd.line(r"v_p = h/r_p = 1.819\ \text{km/s},\qquad v_a = h/r_a = 0.975\ \text{km/s}", color=YELLOW)
            self.hold()

        with self.voice("o8_25"):
            th = np.radians(220)
            q = orb.at(p_, e_, th)
            er, et = orb.unit(th), orb.unit(th + PI / 2)
            vr, vt = mm / h_ * e_ * np.sin(th), mm / h_ * (1 + e_ * np.cos(th))
            s_ = 1.0
            self.play(FadeIn(Dot(q, color=WHITE)), Create(DashedLine(Mc, q, color=DIM)))
            self.play(GrowArrow(Arrow(q, q + s_ * vr * er, buff=0, color=ER_COL, stroke_width=5, tip_length=0.12)),
                      GrowArrow(Arrow(q, q + s_ * vt * et, buff=0, color=ET_COL, stroke_width=5, tip_length=0.15)))
            bd.line(r"\theta = 220^\circ:\quad \mu/h = 1.397\ \text{km/s}")
            bd.line(r"v_r = \tfrac{\mu}{h}\,e\sin\theta = -0.271\ \text{km/s}", color=ER_COL, indent=0.4, reason="falling toward perilune")
            bd.line(r"v_\theta = \tfrac{\mu}{h}(1 + e\cos\theta) = 1.074\ \text{km/s}", color=ET_COL, indent=0.4)
            self.hold()

        with self.voice("o8_26"):
            l = bd.line(r"T = 2\pi\sqrt{a^3/\mu} = 13{,}045\ \text{s} = 217.4\ \text{min}", color=YELLOW)
            bd.box(l)
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))
