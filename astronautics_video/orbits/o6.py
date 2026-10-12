"""Part 6: velocity on the orbit - frames, v_r, v_theta, flight-path angle, hodograph."""
from ocommon import *  # noqa: F401,F403

ECC = 0.5
P = 1.5


class O6Concept(OLesson):
    def construct(self):
        orb = Orb(focus=(-3.0, -0.6), k=1.2)
        ell = orb.conic(P, ECC)
        th = ValueTracker(1.1)

        def pos():
            return orb.at(P, ECC, th.get_value())
        with self.voice("o6_01"):
            t = o_title(self, 6, "Velocity on the Orbit", "speed, direction and the flight-path angle")
            self.wait(1.2)
            self.play(FadeOut(t))
            hdr = header("Two frames at the focus")
            self.play(FadeIn(hdr))
            self.play(Create(ell), FadeIn(earth(orb.f, 0.15)))
            Lf = 1.6
            pa = Arrow(orb.f, orb.f + Lf * RIGHT, buff=0, color=P_COL, stroke_width=5, tip_length=0.18)
            qa = Arrow(orb.f, orb.f + Lf * UP, buff=0, color=Q_COL, stroke_width=5, tip_length=0.18)
            pl_ = T(r"\hat p", color=P_COL).scale(0.65).next_to(pa, DOWN, buff=0.1).shift(RIGHT * 0.6)
            ql_ = T(r"\hat q", color=Q_COL).scale(0.65).next_to(qa, LEFT, buff=0.1).shift(UP * 0.5)
            wl_ = Tx(r"$\hat w = \hat h$ out of the screen", color=H_COL).scale(0.5).next_to(orb.f, DL, buff=0.2)
            self.play(GrowArrow(pa), GrowArrow(qa), FadeIn(pl_), FadeIn(ql_), FadeIn(wl_))
            tag = Tx(r"perifocal frame $\mathcal P$: fixed;\\ $\hat p$ toward periapsis (along $\vec e$)", color=WHITE).scale(0.6).move_to([3.8, 2.2, 0])
            self.play(FadeIn(tag))
            self.hold()

        Lr = 1.2
        a_er = always_redraw(lambda: Arrow(orb.f, orb.f + Lr * orb.unit(th.get_value()), buff=0, color=ER_COL, stroke_width=5, tip_length=0.16))
        a_et = always_redraw(lambda: Arrow(orb.f, orb.f + Lr * orb.unit(th.get_value() + PI / 2), buff=0, color=ET_COL, stroke_width=5, tip_length=0.16))
        l_er = always_redraw(lambda: T(r"\hat e_r", color=ER_COL).scale(0.6).move_to(orb.f + (Lr + 0.3) * orb.unit(th.get_value())))
        l_et = always_redraw(lambda: T(r"\hat e_\theta", color=ET_COL).scale(0.6).move_to(orb.f + (Lr + 0.3) * orb.unit(th.get_value() + PI / 2)))
        ang = always_redraw(lambda: Arc(radius=0.55, start_angle=0, angle=th.get_value(), arc_center=orb.f, color=YELLOW))
        angl = always_redraw(lambda: T(r"\theta", color=YELLOW).scale(0.55).move_to(orb.f + 0.8 * orb.unit(th.get_value() / 2)))
        pl = always_redraw(lambda: planet(pos()))
        rline = always_redraw(lambda: DashedLine(orb.f, pos(), color=DIM))
        with self.voice("o6_02"):
            self.add(rline, pl)
            self.play(FadeIn(a_er), FadeIn(a_et), FadeIn(l_er), FadeIn(l_et), FadeIn(ang), FadeIn(angl))
            tag2 = Tx(r"orbital frame $\mathcal O$: $\{\hat e_r,\ \hat e_\theta,\ \hat e_h\}$\\rides with the satellite", color=WHITE).scale(0.6).next_to(tag, DOWN, buff=0.45)
            self.play(FadeIn(tag2))
            self.play(th.animate.set_value(2.6), run_time=3, rate_func=there_and_back)
            self.hold()

        with self.voice("o6_03"):
            self.play(FadeOut(VGroup(tag, tag2)))
            bd = Board(self, left=0.9, top=2.6, scale=0.78, buff=0.4)
            bd.line(r"\hat e_r = \cos\theta\,\hat p + \sin\theta\,\hat q", color=ER_COL)
            bd.line(r"\hat e_\theta = -\sin\theta\,\hat p + \cos\theta\,\hat q", color=ET_COL)
            m = mat([[r"\cos\theta", r"\sin\theta", "0"], [r"-\sin\theta", r"\cos\theta", "0"], ["0", "0", "1"]], scale=0.62)
            l = bd.line(None, mob=VGroup(T(r"C^{\mathcal{OP}} =").scale(0.75), m, T(r"= C_3(\theta)", color=YELLOW).scale(0.75)).arrange(RIGHT, buff=0.15))
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(pa, qa, pl_, ql_, wl_, ang, angl)))

        # ------------------------------------------------ v_theta and v_r
        with self.voice("o6_04"):
            self.play(Transform(hdr, header("The two velocity components")))
            bd = Board(self, left=0.9, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"\vec v = \dot r\,\hat e_r + r\dot\theta\,\hat e_\theta")
            bd.line(r"v_\theta = r\dot\theta = r\cdot\frac{h}{r^2} = \frac{h}{r}", color=ET_COL)
            self.hold()

        with self.voice("o6_05"):
            bd.line(r"v_\theta = \frac{h}{p}\,(1 + e\cos\theta)", color=ET_COL, indent=0.4, reason="$1/r$ from the orbit equation")
            l = bd.line(r"v_\theta = \frac{\mu}{h}\,(1 + e\cos\theta)", color=YELLOW, indent=0.4, reason="$h/p = \\mu/h$")
            bd.box(l)
            self.hold()
        bd.clear()

        with self.voice("o6_06"):
            bd = Board(self, left=0.9, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"v_r = \dot r = \frac{d}{dt}\Big(\frac{p}{1 + e\cos\theta}\Big) = \frac{p\,e\sin\theta}{(1 + e\cos\theta)^2}\,\dot\theta", color=ER_COL,
                    reason="chain rule", below=True)
            self.hold()

        with self.voice("o6_07"):
            bd.line(r"\dot\theta = \frac{h}{r^2} = \frac{h\,(1 + e\cos\theta)^2}{p^2}", indent=0.4)
            bd.line(r"v_r = \frac{h\,e\sin\theta}{p}", color=ER_COL, indent=0.4, reason="squares cancel")
            l = bd.line(r"v_r = \frac{\mu}{h}\,e\sin\theta", color=YELLOW, indent=0.4)
            bd.box(l)
            self.hold()

        def comps():
            t_ = th.get_value()
            k = 1.05
            return k * ECC * np.sin(t_), k * (1 + ECC * np.cos(t_))
        a_vr = always_redraw(lambda: Arrow(pos(), pos() + comps()[0] * orb.unit(th.get_value()), buff=0, color=ER_COL, stroke_width=4, tip_length=0.13))
        a_vt = always_redraw(lambda: Arrow(pos(), pos() + comps()[1] * orb.unit(th.get_value() + PI / 2), buff=0, color=ET_COL, stroke_width=4, tip_length=0.13))
        a_v = always_redraw(lambda: Arrow(pos(), pos() + comps()[0] * orb.unit(th.get_value()) + comps()[1] * orb.unit(th.get_value() + PI / 2),
                                          buff=0, color=VEL, stroke_width=6, tip_length=0.18))
        sgn = always_redraw(lambda: Tx(r"$v_r > 0$: climbing" if np.sin(th.get_value()) > 0.05 else
                                       (r"$v_r < 0$: falling" if np.sin(th.get_value()) < -0.05 else r"$v_r = 0$: an apsis"),
                                       color=ER_COL).scale(0.6).move_to([-3.4, -3.3, 0]))
        with self.voice("o6_08"):
            self.play(FadeOut(VGroup(a_er, a_et, l_er, l_et)))
            self.play(GrowArrow(a_v), FadeIn(a_vr), FadeIn(a_vt), FadeIn(sgn))
            self.play(th.animate.set_value(TAU + 0.05), run_time=max(3, self.left() - 1), rate_func=linear)
            self.hold()
        bd.clear()

        # ------------------------------------------------ flight-path angle
        def gamma():
            t_ = th.get_value()
            return np.arctan2(ECC * np.sin(t_), 1 + ECC * np.cos(t_))
        horiz = always_redraw(lambda: DashedLine(pos() - 0.8 * orb.unit(th.get_value() + PI / 2), pos() + 1.6 * orb.unit(th.get_value() + PI / 2), color=ET_COL))
        garc = always_redraw(lambda: Arc(radius=0.75, start_angle=th.get_value() + PI / 2, angle=-gamma() + 1e-4, arc_center=pos(), color=YELLOW, stroke_width=4))
        gtxt = always_redraw(lambda: VGroup(T(r"\gamma =", color=YELLOW).scale(0.65),
                                            DecimalNumber(np.degrees(gamma()), num_decimal_places=1, color=YELLOW, include_sign=True).scale(0.65),
                                            T(r"^\circ", color=YELLOW).scale(0.65)).arrange(RIGHT, buff=0.08).move_to([-3.4, 2.4, 0]))
        with self.voice("o6_09"):
            self.play(Transform(hdr, header("The flight-path angle")))
            self.play(th.animate.set_value(1.2), FadeOut(sgn), run_time=1.5)
            self.play(FadeOut(VGroup(a_vr, a_vt)), Create(horiz), FadeIn(garc))
            bd = Board(self, left=0.9, top=2.7, scale=0.8, buff=0.4)
            bd.line(r"\tan\gamma = \frac{v_r}{v_\theta}")
            l = bd.line(r"\tan\gamma = \frac{e\sin\theta}{1 + e\cos\theta}", color=YELLOW, reason="$\\mu/h$ cancels")
            bd.box(l)
            bd.line(r"h = r\,v\cos\gamma", indent=0.4)
            self.hold()

        with self.voice("o6_10"):
            self.add(gtxt)
            self.play(th.animate.set_value(1.2 + TAU), run_time=max(4, self.left() - 2), rate_func=linear)
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(horiz, garc, gtxt, rline)))
        self.remove(horiz, garc, gtxt)

        # ------------------------------------------------ hodograph
        with self.voice("o6_11"):
            self.play(Transform(hdr, header("The hodograph")))
            bd = Board(self, left=0.9, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"\vec v = v_r\,\hat e_r + v_\theta\,\hat e_\theta")
            l = bd.line(r"\vec v = \frac{\mu}{h}\Big[-\sin\theta\,\hat p + (e + \cos\theta)\,\hat q\Big]", color=YELLOW, reason="substitute $\\hat e_r,\\ \\hat e_\\theta$", below=True)
            self.hold()

        Ho = np.array([3.3, -2.0, 0])
        Hk = 1.0

        def vtip():
            t_ = th.get_value()
            return Ho + Hk * np.array([-np.sin(t_), ECC + np.cos(t_), 0])
        hv = always_redraw(lambda: Arrow(Ho, vtip(), buff=0, color=VEL, stroke_width=5, tip_length=0.15))
        htr = TracedPath(vtip, stroke_color=VEL, stroke_width=3)
        with self.voice("o6_12"):
            dot0 = Dot(Ho, color=WHITE, radius=0.05)
            self.play(FadeIn(dot0), GrowArrow(hv))
            self.add(htr)
            self.play(th.animate.set_value(1.2 + 2 * TAU), run_time=5, rate_func=linear)
            cen = Arrow(Ho, Ho + Hk * ECC * UP, buff=0, color=E_VEC, stroke_width=4, tip_length=0.12)
            rad = always_redraw(lambda: Arrow(Ho + Hk * ECC * UP, vtip(), buff=0, color=B_COL, stroke_width=3, tip_length=0.12))
            cl = T(r"\frac{e\mu}{h}", color=E_VEC).scale(0.5).next_to(cen, LEFT, buff=0.08)
            rl = T(r"\text{radius } \frac{\mu}{h}", color=B_COL).scale(0.5).move_to(Ho + Hk * (ECC + 1.0) * UP + RIGHT * 1.3)
            self.play(GrowArrow(cen), FadeIn(rad), FadeIn(cl), FadeIn(rl))
            self.play(th.animate.set_value(1.2 + 3 * TAU), run_time=max(3, min(6, self.left() - 1)), rate_func=linear)
            self.hold()

        with self.voice("o6_13"):
            self.play(th.animate.set_value(3 * TAU + 0.001), run_time=1.5)
            bd.clear()
            bd = Board(self, left=0.9, top=2.7, scale=0.78, buff=0.4)
            bd.line(r"v_p = \frac{\mu}{h}(1 + e),\qquad v_a = \frac{\mu}{h}(1 - e)", color=Q_COL)
            bd.line(r"\frac{v_p}{v_a} = \frac{1 + e}{1 - e} = \frac{r_a}{r_p}", color=Q_COL, reason="matches $r_p v_p = r_a v_a$")
            self.hold()
        bd.clear()

        with self.voice("o6_14"):
            bd = Board(self, left=0.9, top=2.7, scale=0.8, buff=0.42)
            bd.line(r"\dot\theta = \frac{h}{r^2} = \sqrt{\frac{\mu}{p^3}}\,(1 + e\cos\theta)^2", color=YELLOW, reason="$h = \\sqrt{\\mu p}$", below=True)
            self.play(th.animate.set_value(4 * TAU), run_time=4, rate_func=linear)
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("o6_15"):
            h, rows = recap(self, [
                r"$v_r = \dfrac{\mu}{h}\,e\sin\theta$, \quad $v_\theta = \dfrac{\mu}{h}\,(1 + e\cos\theta)$.",
                r"$\tan\gamma = \dfrac{e\sin\theta}{1 + e\cos\theta}$, \quad $h = r v\cos\gamma$.",
                r"$C^{\mathcal{OP}} = C_3(\theta)$: the orbital frame is the perifocal frame turned by $\theta$.",
                r"Hodograph: the velocity tips trace a circle of radius $\mu/h$, center shifted by $e\mu/h$.",
            ])
            for rr in rows:
                self.play(FadeIn(rr, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
