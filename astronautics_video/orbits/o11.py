"""Part 11: HW 3 Problem 2 - time on an orbit, Kepler's equation via the auxiliary circle."""
from ocommon import *  # noqa: F401,F403

A, ECC = 1.5, 2 / 3                  # AU
P = A * (1 - ECC ** 2)
B = A * np.sqrt(1 - ECC ** 2)
K = 1.55                              # screen units per AU
TH1 = np.arccos(-0.25)


class O11Problem(OLesson):
    def construct(self):
        ctr = np.array([-3.4, -0.5, 0])
        F = ctr + K * A * ECC * RIGHT
        orb = Orb(focus=F, k=K)
        ell = orb.conic(P, ECC)

        def on_ell(E):
            return ctr + K * np.array([A * np.cos(E), B * np.sin(E), 0])

        def on_circ(E):
            return ctr + K * A * np.array([np.cos(E), np.sin(E), 0])

        with self.voice("o11_01"):
            t = o_title(self, 11, "HW 3, Problem 2: Time on an Orbit", "Kepler's equation from the auxiliary circle")
            self.wait(1.2)
            self.play(FadeOut(t))
            hdr = header("HW 3, Problem 2")
            self.play(FadeIn(hdr))
            self.play(Create(ell), FadeIn(sun(F, 0.13)))
            g = num_card([r"r_p = 0.5\ \text{AU}", r"r_a = 2.5\ \text{AU}", r"\text{time with } r < 1\ \text{AU}\ ?"], scale=0.6).move_to([4.0, 1.8, 0])
            self.play(FadeIn(g))
            self.hold()
        self.play(FadeOut(g))

        with self.voice("o11_02"):
            bd = Board(self, left=0.9, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"a = \tfrac12(0.5 + 2.5) = 1.5\ \text{AU}")
            bd.line(r"e = \frac{r_a - r_p}{r_a + r_p} = \frac{2}{3}")
            bd.line(r"p = a(1 - e^2) = 1.5\cdot\tfrac59 = \tfrac56\ \text{AU}")
            self.hold()

        au = DashedVMobject(Circle(radius=K, color=B_COL, stroke_width=2.5).move_to(F), num_dashes=50)
        aul = Tx("1 AU", color=B_COL).scale(0.5).next_to(F + K * DOWN, DOWN, buff=0.08)
        x1, x2 = orb.at(P, ECC, TH1), orb.at(P, ECC, -TH1)
        with self.voice("o11_03"):
            self.play(Create(au), FadeIn(aul))
            bd.line(r"1 = \frac{5/6}{1 + \tfrac23\cos\theta}\ \Rightarrow\ \cos\theta = -\tfrac14")
            l = bd.line(r"\theta = \pm104.48^\circ", color=YELLOW)
            inside = orb.conic(P, ECC, -TH1, TH1, color=YELLOW, width=6)
            self.play(FadeIn(Dot(x1, color=YELLOW)), FadeIn(Dot(x2, color=YELLOW)), Create(inside))
            self.hold()
        bd.clear()

        sect = orb.sector(P, ECC, -TH1, TH1, color=AREA, opacity=0.45)
        with self.voice("o11_04"):
            wrong = T(r"\frac{208.96^\circ}{360^\circ}\ ?", color=P_COL).scale(0.8).move_to([3.6, 2.0, 0])
            self.play(FadeIn(wrong))
            cr = Cross(wrong, stroke_color=P_COL, stroke_width=5)
            self.play(Create(cr))
            why = Tx(r"time $\propto$ swept \emph{area}, not angle", color=AREA).scale(0.7).next_to(wrong, DOWN, buff=0.5)
            self.play(FadeIn(sect), FadeIn(why))
            self.hold()
        self.play(FadeOut(VGroup(wrong, cr, why, sect, au, aul)), *[FadeOut(m) for m in self.mobjects if isinstance(m, Dot)])
        self.remove(inside)

        # ---------------------------------------------------------------- auxiliary circle
        circ = Circle(radius=K * A, color=DIM, stroke_width=2.5).move_to(ctr)
        with self.voice("o11_05"):
            self.play(Transform(hdr, header("Kepler's trick: the auxiliary circle")))
            cdot = Dot(ctr, color=WHITE, radius=0.05)
            cl = T("C").scale(0.5).next_to(ctr, DL, buff=0.05)
            self.play(Create(circ), FadeIn(cdot), FadeIn(cl))
            sq = circ.copy().set_color(YELLOW)
            self.add(sq)
            self.play(sq.animate.stretch(B / A, 1, about_point=ctr), run_time=2.5)
            self.play(FadeOut(sq))
            sl = Tx(r"ellipse $=$ circle squashed\\vertically by $b/a$", color=YELLOW).scale(0.6).move_to([3.8, 2.2, 0])
            self.play(FadeIn(sl))
            self.hold()
        self.play(FadeOut(sl))

        E0 = 1.15
        Pp, Qp = on_ell(E0), on_circ(E0)
        with self.voice("o11_06"):
            pd = Dot(Pp, color=B_COL)
            qd = Dot(Qp, color=YELLOW)
            pl = T("P", color=B_COL).scale(0.55).next_to(Pp, DR, buff=0.05)
            ql = T("Q", color=YELLOW).scale(0.55).next_to(Qp, UR, buff=0.05)
            vl = DashedLine(Pp, Qp, color=WHITE)
            foot = DashedLine(Pp, np.array([Pp[0], ctr[1], 0]), color=DIM)
            cq = Line(ctr, Qp, color=YELLOW, stroke_width=3)
            Ea = Arc(radius=0.55, start_angle=0, angle=E0, arc_center=ctr, color=YELLOW)
            El = T("E", color=YELLOW).scale(0.6).move_to(ctr + 0.8 * np.array([np.cos(E0 / 2), np.sin(E0 / 2), 0]))
            axisl = DashedLine(ctr + LEFT * K * A, ctr + RIGHT * K * A, color=DIM, stroke_width=2)
            self.play(Create(axisl), FadeIn(pd), FadeIn(pl))
            self.play(Create(vl), FadeIn(qd), FadeIn(ql))
            self.play(Create(cq), Create(Ea), FadeIn(El))
            bd = Board(self, left=0.9, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"Q = (a\cos E,\ a\sin E)", color=YELLOW, reason="from the center")
            bd.line(r"P = (a\cos E,\ b\sin E)", color=B_COL, reason="squashed by $b/a$")
            self.hold()

        with self.voice("o11_07"):
            fl = Line(F, Pp, color=WHITE, stroke_width=3)
            fdl = T("r", color=WHITE).scale(0.55).next_to(fl.get_center(), RIGHT, buff=0.08)
            self.play(Create(fl), FadeIn(fdl), FadeIn(Dot(F, color=SUN, radius=0.07)))
            bd.line(r"\text{from } F:\ \big(a(\cos E - e),\ b\sin E\big)", reason="$F$ is $ae$ from the center")
            bd.line(r"r^2 = a^2(\cos E - e)^2 + a^2(1 - e^2)\sin^2 E", reason="$b^2 = a^2(1 - e^2)$", below=True)
            self.hold()

        with self.voice("o11_08"):
            bd.line(r"= a^2\big(1 - 2e\cos E + e^2\cos^2 E\big) = a^2(1 - e\cos E)^2", indent=0.4, reason="$\\sin^2 + \\cos^2 = 1$", below=True)
            l = bd.line(r"r = a\,(1 - e\cos E)", color=YELLOW)
            bd.box(l)
            self.hold()
        bd.clear()

        with self.voice("o11_09"):
            bd = Board(self, left=0.9, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"r\cos\theta = a(\cos E - e)", reason="horizontal coordinate")
            l = bd.line(r"\cos E = \frac{e + \cos\theta}{1 + e\cos\theta}", color=YELLOW, reason="true $\\to$ eccentric anomaly")
            bd.box(l)
            self.hold()
        bd.clear()

        # ---------------------------------------------------------------- areas
        peri = ctr + K * A * RIGHT

        def circ_region():
            pts = [F] + [on_circ(t_) for t_ in np.linspace(0, E0, 40)]
            return Polygon(*pts, stroke_width=1.5, color=YELLOW, fill_opacity=0.3)

        def ell_region():
            pts = [F] + [on_ell(t_) for t_ in np.linspace(0, E0, 40)]
            return Polygon(*pts, stroke_width=1.5, color=AREA, fill_opacity=0.45)
        cr_, er_ = circ_region(), ell_region()
        with self.voice("o11_10"):
            self.play(Transform(hdr, header("Swept area, via the circle")))
            self.play(FadeOut(VGroup(fl, fdl)), FadeIn(cr_))
            self.play(TransformFromCopy(cr_, er_))
            bd = Board(self, left=0.9, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"\text{area}_{\text{ellipse}} = \frac{b}{a}\;\text{area}_{\text{circle}}", reason="squashing scales every area")
            self.hold()

        with self.voice("o11_11"):
            pie = Sector(radius=K * A, angle=E0, start_angle=0, arc_center=ctr, color=Q_COL, fill_opacity=0.3, stroke_width=1.5)
            trig = Polygon(ctr, F, Qp, color=P_COL, fill_opacity=0.45, stroke_width=2)
            self.play(FadeOut(er_), FadeIn(pie))
            self.play(FadeIn(trig))
            bd.line(r"\text{pie slice} = \tfrac12 a^2 E", color=Q_COL)
            bd.line(r"\text{triangle } CFQ = \tfrac12\,(ae)(a\sin E)", color=P_COL)
            l = bd.line(r"\text{circle region} = \frac{a^2}{2}\,(E - e\sin E)", color=YELLOW)
            self.hold()

        with self.voice("o11_12"):
            self.play(FadeOut(VGroup(pie, trig)), FadeIn(er_))
            l = bd.line(r"\text{swept area} = \frac{ab}{2}\,(E - e\sin E)", color=AREA, reason="times $b/a$")
            bd.box(l, color=AREA)
            self.hold()
        bd.clear()

        with self.voice("o11_13"):
            bd = Board(self, left=0.9, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"t - t_p = \frac{\text{area}}{\pi a b}\,T = \frac{ab(E - e\sin E)/2}{\pi a b}\,T", reason="equal areas, equal times", below=True)
            bd.line(r"t - t_p = \frac{T}{2\pi}\,(E - e\sin E)", color=YELLOW)
            self.hold()

        with self.voice("o11_14"):
            bd.line(r"M \equiv \frac{2\pi}{T}(t - t_p) = n\,(t - t_p)", reason="mean anomaly: grows steadily")
            l = bd.line(r"M = E - e\sin E", color=YELLOW, reason="Kepler's equation")
            bd.box(l)
            self.hold()

        with self.voice("o11_15"):
            chain = T(r"\theta\ \longrightarrow\ E\ \longrightarrow\ M\ \longrightarrow\ t", color=B_COL).scale(0.8)
            chain.move_to([3.9, -2.6, 0])
            self.play(Write(chain))
            back = Tx(r"($t \to \theta$ needs iteration)", color=REASON).scale(0.55).next_to(chain, DOWN, buff=0.2)
            self.play(FadeIn(back))
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker) and m is not hdr])))

        # ---------------------------------------------------------------- the probe
        E1 = PI / 3
        with self.voice("o11_16"):
            self.play(Transform(hdr, header("Back to the probe")))
            au2 = DashedVMobject(Circle(radius=K, color=B_COL, stroke_width=2.5).move_to(F), num_dashes=50)
            self.play(FadeIn(orb.conic(P, ECC)), FadeIn(sun(F, 0.13)), FadeIn(au2), Create(Circle(radius=K * A, color=DIM, stroke_width=2.5).move_to(ctr)))
            Q1, Q2 = on_circ(E1), on_circ(-E1)
            p1d, p2d = Dot(on_ell(E1), color=YELLOW), Dot(on_ell(-E1), color=YELLOW)
            self.play(FadeIn(p1d), FadeIn(p2d), Create(DashedLine(on_ell(E1), Q1, color=WHITE)), Create(Line(ctr, Q1, color=YELLOW)),
                      Create(Arc(radius=0.5, start_angle=0, angle=E1, arc_center=ctr, color=YELLOW)))
            bd = Board(self, left=0.9, top=2.7, scale=0.76, buff=0.38)
            bd.line(r"1 = 1.5\big(1 - \tfrac23\cos E\big)\ \Rightarrow\ \cos E = \tfrac12")
            l = bd.line(r"E = 60^\circ = \pi/3", color=YELLOW)
            bd.line(r"\text{check: } \frac{\tfrac23 - \tfrac14}{1 - \tfrac16} = \frac{5/12}{5/6} = \frac12\ \checkmark", color=Q_COL)
            self.hold()

        with self.voice("o11_17"):
            bd.line(r"M = E - e\sin E = \frac{\pi}{3} - \frac23\cdot\frac{\sqrt3}{2}")
            l = bd.line(r"M = 1.0472 - 0.5774 = 0.4698\ \text{rad}", color=YELLOW)
            self.hold()

        with self.voice("o11_18"):
            self.play(FadeIn(orb.sector(P, ECC, -TH1, TH1, color=AREA, opacity=0.45)))
            l = bd.line(r"\text{fraction} = \frac{2M}{2\pi} = \frac{M}{\pi} = 0.1496", color=AREA, reason="about 15\\% of the time")
            self.hold()
        bd.clear()

        with self.voice("o11_19"):
            bd = Board(self, left=0.9, top=2.7, scale=0.76, buff=0.4)
            bd.line(r"T = a^{3/2}\ \text{yr} = 1.5^{3/2} = 1.837\ \text{yr}", reason="1 AU $\\leftrightarrow$ 1 year")
            bd.line(r"T = 671.0\ \text{days}", indent=0.5, color=YELLOW, reason="same as $2\\pi\\sqrt{a^3/\\mu_\\odot}$")
            self.hold()

        with self.voice("o11_20"):
            l = bd.line(r"t_{r<1\,\text{AU}} = 0.1496\times671.0 \approx 100\ \text{days} \approx 0.275\ \text{yr}", color=YELLOW)
            bd.box(l)
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("o11_21"):
            h, rows = recap(self, [
                r"Time is proportional to swept area (Kepler II), not to angle.",
                r"Auxiliary circle: $r = a(1 - e\cos E)$, \ $\cos E = \dfrac{e + \cos\theta}{1 + e\cos\theta}$.",
                r"Swept area $= \tfrac{ab}{2}(E - e\sin E)$ \ $\Rightarrow$ \ Kepler's equation $M = E - e\sin E$, \ $M = n(t - t_p)$.",
                r"HW 3 P2: $E = 60^\circ$, $M = 0.4698$, about 100 days per orbit inside 1 AU.",
            ])
            for rr in rows:
                self.play(FadeIn(rr, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
