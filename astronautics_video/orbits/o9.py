"""Part 9: worked examples on open trajectories - textbook 2.19, 2.20, 2.21, 2.22, 2.42."""
from ocommon import *  # noqa: F401,F403


def given(rows, at=(-4.4, 2.2), scale=0.56):
    c = num_card(rows, scale=scale)
    c.move_to([at[0], at[1], 0])
    return c


class O9Examples(OLesson):
    def clear_all(self, keep=()):
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker) and m not in keep])))

    def construct(self):
        with self.voice("o9_01"):
            t = o_title(self, 9, "Worked Examples: Escape Trajectories", "textbook 2.19, 2.20, 2.21, 2.22 and 2.42")
            self.hold()
        self.play(FadeOut(t))

        # ------------------------------------------------ 2.19
        Ec = np.array([-3.8, -1.2, 0])
        orb = Orb(focus=Ec, k=0.9)
        p19 = 1.6
        par = orb.conic(p19, 1.0, -2.2, 2.2, color=YELLOW, width=3.5)
        hdr = header("Problem 2.19: a parabola at 4000 km")
        with self.voice("o9_02"):
            self.play(FadeIn(hdr))
            self.play(FadeIn(earth(Ec, 0.35)), Create(par))
            th = np.radians(50)
            q = orb.at(p19, 1.0, th)
            self.play(FadeIn(Dot(q, color=WHITE)), Create(DashedLine(Ec, q, color=DIM)))
            g = given([r"h = 4000\ \text{km}", r"\gamma = 25^\circ", r"e = 1"], at=(-4.6, 2.3))
            self.play(FadeIn(g))
            bd = Board(self, left=-0.6, top=2.7, scale=0.78, buff=0.42)
            bd.line(r"r = 6378 + 4000 = 10{,}378\ \text{km}")
            self.hold()

        with self.voice("o9_03"):
            bd.line(r"v = \sqrt{2\mu/r} = \sqrt{\tfrac{2(3.986\times10^5)}{10{,}378}} = 8.765\ \text{km/s}", color=YELLOW, reason="parabola: escape speed", below=True)
            bd.line(r"\gamma = \theta/2\ \Rightarrow\ \theta = 2(25^\circ) = 50^\circ", color=YELLOW, reason="$\\gamma > 0$: moving away")
            self.hold()

        with self.voice("o9_04"):
            bd.line(r"p = r(1 + \cos\theta) = 17{,}049\ \text{km},\quad r_p = p/2 = 8524\ \text{km}", color=Q_COL, reason="a check", below=True)
            self.hold()
        bd.clear()
        self.clear_all()

        # ------------------------------------------------ 2.20
        Ec = np.array([-1.8, 0.0, 0])
        orb = Orb(focus=Ec, k=1.15e-4)
        k = orb.k
        with self.voice("o9_05"):
            hdr = header("Problem 2.20: approaching on a parabola")
            self.play(FadeIn(hdr))
            pp = 2 * 7178.0
            par = orb.conic(pp, 1.0, -2.12, 2.12, color=YELLOW, width=3.5)
            self.play(FadeIn(earth(Ec, 6378 * k)), Create(par))
            th = -np.radians(118.06)
            q = orb.at(pp, 1.0, th)
            vdir = (orb.at(pp, 1.0, th + 0.01) - orb.at(pp, 1.0, th - 0.01))
            vdir /= np.linalg.norm(vdir)
            self.play(FadeIn(Dot(q, color=WHITE)), GrowArrow(Arrow(q, q + 0.9 * vdir, buff=0, color=VEL, stroke_width=5, tip_length=0.15)))
            g = given([r"v = 5.423\ \text{km/s}", r"h_p = 800\ \text{km}", r"\text{approaching}"], at=(-5.3, 0.0))
            self.play(FadeIn(g))
            self.hold()

        with self.voice("o9_06"):
            bd = Board(self, left=-0.2, top=2.7, scale=0.78, buff=0.42)
            l = bd.line(r"v^2 = \frac{2\mu}{r}\ \Rightarrow\ r = \frac{2\mu}{v^2} = \frac{2(3.986\times10^5)}{5.423^2} = 27{,}107\ \text{km}", color=YELLOW, below=True,
                        reason="escape speed, backwards")
            self.hold()

        with self.voice("o9_07"):
            bd.line(r"p = 2r_p = 2(7178) = 14{,}356\ \text{km}")
            bd.line(r"1 + \cos\theta = p/r\ \Rightarrow\ \cos\theta = -0.4704")
            self.hold()

        with self.voice("o9_08"):
            bd.line(r"\theta = \pm118.06^\circ\ \to\ \theta = -118.06^\circ\ (241.94^\circ)", color=YELLOW, reason="approaching: $v_r < 0$")
            l = bd.line(r"\gamma = \theta/2 = -59.03^\circ", color=YELLOW)
            bd.box(l)
            self.hold()
        bd.clear()
        self.clear_all()

        # ------------------------------------------------ 2.21
        e21 = 1.3033
        Ec = np.array([-2.2, -0.6, 0])
        orb = Orb(focus=Ec, k=0.7)
        p_s = 1.0 * (1 + e21)          # schematic: r_p = 1 unit
        tinf = np.arccos(-1 / e21)
        hyp = orb.conic(p_s, e21, -1.95, 1.95, color=YELLOW, width=3.5)
        with self.voice("o9_09"):
            hdr = header("Problem 2.21: leaving Earth on a hyperbola")
            self.play(FadeIn(hdr))
            self.play(FadeIn(earth(Ec, 0.45)), Create(hyp))
            pq = orb.at(p_s, e21, 0)
            self.play(FadeIn(Dot(pq, color=Q_COL)), GrowArrow(Arrow(pq, pq + UP * 1.0, buff=0, color=VEL, stroke_width=5, tip_length=0.15)))
            pl = Tx(r"cutoff: $\gamma = 0$\\$\Rightarrow$ perigee", color=Q_COL).scale(0.5).next_to(pq, RIGHT, buff=0.15)
            self.play(FadeIn(pl))
            g = given([r"h = 200\ \text{km}", r"v = 11.814\ \text{km/s}", r"\gamma = 0"], at=(-5.3, 2.3))
            self.play(FadeIn(g))
            bd = Board(self, left=0.4, top=2.7, scale=0.76, buff=0.4)
            bd.line(r"r_p = 6578\ \text{km},\quad v_p = 11.814\ \text{km/s}")
            self.hold()

        with self.voice("o9_10"):
            bd.line(r"h = r_p v_p = 77{,}712\ \text{km}^2/\text{s},\quad p = h^2/\mu = 15{,}151\ \text{km}")
            l = bd.line(r"\text{(a) } e = \frac{p}{r_p} - 1 = 1.3033", color=YELLOW, reason="$> 1$: hyperbola")
            self.hold()

        with self.voice("o9_11"):
            bd.line(r"\mathcal E = \frac{11.814^2}{2} - \frac{\mu}{6578} = 69.79 - 60.60 = 9.189\ \tfrac{\text{km}^2}{\text{s}^2}", below=True, reason="positive, as it must be")
            l = bd.line(r"\text{(b) } v = \sqrt{2\big(\mathcal E + \mu/r\big)} = 4.514\ \text{km/s}", color=YELLOW, reason="$r = 400{,}000$ km", below=True)
            self.hold()
        bd.clear()

        with self.voice("o9_12"):
            far = orb.at(p_s, e21, 1.9)
            self.play(FadeIn(Dot(far, color=WHITE)))
            fl = Tx(r"$r = 400{,}000$ km\\(far along the arm)", color=WHITE).scale(0.5).next_to(far, RIGHT, buff=0.15)
            self.play(FadeIn(fl))
            bd = Board(self, left=0.4, top=2.7, scale=0.76, buff=0.4)
            bd.line(r"\text{(c) } \cos\gamma = \frac{h}{r v} = \frac{77{,}712}{400{,}000\,(4.514)} = 0.0430")
            bd.line(r"\gamma = 87.53^\circ", color=YELLOW, indent=0.4, reason="almost straight out")
            self.hold()

        with self.voice("o9_13"):
            bd.line(r"\text{(d) } \cos\theta = \frac{p/r - 1}{e} = -0.7382\ \Rightarrow\ \theta = 137.58^\circ", color=YELLOW)
            bd.line(r"\theta_\infty = \cos^{-1}(-1/e) = 140.11^\circ", indent=0.4, reason="just short of the asymptote")
            asy = DashedLine(Ec, Ec + 3.0 * orb.unit(tinf), color=V_COL)
            self.play(Create(asy))
            self.hold()

        with self.voice("o9_14"):
            l = bd.line(r"\text{(e) } v_\infty = \sqrt{2\mathcal E} = 4.287\ \text{km/s}", color=YELLOW, reason="$a = -\\mu/2\\mathcal E = -21{,}688$ km")
            bd.box(l)
            self.hold()
        bd.clear()
        self.clear_all()

        # ------------------------------------------------ 2.22
        e22, a22 = 1.4, -16900.0
        p22 = a22 * (1 - e22 ** 2)
        Ec = np.array([-3.0, -0.2, 0])
        orb = Orb(focus=Ec, k=0.8 / 6760)
        t22 = np.arccos(-1 / e22)
        with self.voice("o9_15"):
            hdr = header("Problem 2.22: a departure hyperbola")
            self.play(FadeIn(hdr))
            hyp = orb.conic(p22, e22, -1.85, 1.85, color=YELLOW, width=3.5)
            self.play(FadeIn(earth(Ec, 6378 * orb.k)), Create(hyp))
            g = given([r"e = 1.4", r"a = -16{,}900\ \text{km}"], at=(-5.6, -2.4))
            self.play(FadeIn(g))
            bd = Board(self, left=-0.2, top=2.7, scale=0.76, buff=0.4)
            bd.line(r"\text{(a) } r_p = a(1 - e) = (-16{,}900)(-0.4) = 6760\ \text{km}")
            l = bd.line(r"h_p = 382\ \text{km}", color=YELLOW, indent=0.4)
            self.hold()

        with self.voice("o9_16"):
            th = np.radians(100)
            q = orb.at(p22, e22, th)
            er, et = orb.unit(th), orb.unit(th + PI / 2)
            self.play(FadeIn(Dot(q, color=WHITE)), Create(DashedLine(Ec, q, color=DIM)),
                      GrowArrow(Arrow(q, q + 0.12 * 6.834 * er, buff=0, color=ER_COL, stroke_width=5, tip_length=0.13)),
                      GrowArrow(Arrow(q, q + 0.12 * 3.752 * et, buff=0, color=ET_COL, stroke_width=5, tip_length=0.13)))
            bd.line(r"\text{(b) } p = a(1 - e^2) = 16{,}224\ \text{km},\quad \mu/h = 4.957\ \text{km/s}", below=True)
            bd.line(r"v_r = \tfrac{\mu}{h}\,e\sin100^\circ = 6.834\ \text{km/s}", color=ER_COL, indent=0.4)
            bd.line(r"v_\theta = \tfrac{\mu}{h}(1 + e\cos100^\circ) = 3.752\ \text{km/s}", color=ET_COL, indent=0.4)
            self.hold()

        with self.voice("o9_17"):
            bd.line(r"\text{(c) } \theta_\infty = \cos^{-1}(-1/1.4) = 135.58^\circ", color=V_COL)
            l = bd.line(r"\text{(d) } \delta = 2\sin^{-1}(1/1.4) = 91.17^\circ", color=YELLOW, reason="$= 2\\theta_\\infty - 180^\\circ$ \\checkmark")
            bd.box(l)
            asy = DashedLine(Ec, Ec + 3.6 * orb.unit(t22), color=V_COL)
            self.play(Create(asy))
            self.hold()
        bd.clear()
        self.clear_all()

        # ------------------------------------------------ 2.42
        mj = 1.266865e8
        e42, a42 = 1.0172, -4.384e6
        rp42 = a42 * (1 - e42)
        Jc = np.array([-2.6, -0.6, 0])
        Rj = 71492.0
        k = 1.1 / Rj
        orb = Orb(focus=Jc, k=k, rot=0.0)
        t42 = np.arccos(-1 / e42)
        p42 = a42 * (1 - e42 ** 2)
        with self.voice("o9_18"):
            hdr = header("Problem 2.42: Juno at Jupiter")
            self.play(FadeIn(hdr))
            jup = VGroup(Circle(radius=Rj * k, color="#D9A066", fill_color="#5A3D22", fill_opacity=1).move_to(Jc),
                         *[Line(Jc + Rj * k * np.array([-np.sqrt(1 - y * y), y, 0]), Jc + Rj * k * np.array([np.sqrt(1 - y * y), y, 0]),
                                color="#D9A066", stroke_width=1.5) for y in (-0.5, -0.15, 0.25, 0.6)])
            self.play(FadeIn(jup))
            g = given([r"e = 1.0172", r"a = -4.384\times10^6\ \text{km}", r"\mu_J = 1.2669\times10^8\ \text{km}^3/\text{s}^2"], at=(4.4, -2.4), scale=0.52)
            self.play(FadeIn(g))
            hyp = orb.conic(p42, e42, -1.85, 1.85, color=YELLOW, width=3.5)
            self.play(Create(hyp), run_time=2)
            self.hold()

        with self.voice("o9_19"):
            bd = Board(self, left=0.2, top=2.7, scale=0.76, buff=0.42)
            bd.line(r"v_\infty = \sqrt{-\mu/a} = \sqrt{\tfrac{1.2669\times10^8}{4.384\times10^6}} = 5.376\ \text{km/s}", color=YELLOW)
            bd.line(r"r_p = a(1 - e) = 75{,}405\ \text{km}", color=YELLOW)
            bd.line(r"R_J = 71{,}492\ \text{km}:\ \text{only} \approx 3900\ \text{km above the clouds}", indent=0.4, color=REASON)
            self.hold()

        with self.voice("o9_20"):
            l = bd.line(r"\delta = 2\sin^{-1}(1/1.0172) \approx 159^\circ", color=V_COL, reason="nearly parabolic: a hairpin")
            self.hold()
        bd.clear()
        self.clear_all()
