"""Lesson 6: Acceleration in rotating frames."""
from lcommon import *  # noqa: F401,F403
from scenes_c import SpinningDisk, make_disk, vec, rot2  # noqa: E402

BRD = r"{}^{\mathcal B}\dot{\vec r}"
BRDD = r"{}^{\mathcal B}\ddot{\vec r}"


class V6Concept(Lesson):
    def construct(self):
        with self.voice("v6_01"):
            card = title_card(self, 6, "Acceleration in Rotating Frames", "relative, tangential, Coriolis, and centripetal")
            self.hold()
        self.play(FadeOut(card))

        with self.voice("v6_02"):
            hdr = header("Start from the velocity")
            self.play(FadeIn(hdr))
            bd = Board(self, left=-6.0, top=2.3, scale=0.85, buff=0.45)
            bd.line(r"\vec v = {}^{\mathcal N}\frac{d}{dt}\vec r = {}^{\mathcal B}\frac{d}{dt}\vec r + \vec\omega\times\vec r", reason="transport theorem (Lesson 5)")
            short = VGroup(T(BRD + r" \equiv {}^{\mathcal B}\frac{d}{dt}\vec r"), T(BRDD + r" \equiv {}^{\mathcal B}\frac{d^2}{dt^2}\vec r")).scale(0.75)
            short.arrange(RIGHT, buff=1.0)
            bd.line(mob=short, reason="shorthand", indent=0.6)
            bd.line(r"\vec v = " + BRD + r" + \vec\omega\times\vec r", color=YELLOW)
            self.hold()

        with self.voice("v6_03"):
            bd.line(r"\vec a = {}^{\mathcal N}\frac{d}{dt}\vec v = \underbrace{{}^{\mathcal N}\frac{d}{dt}\big(" + BRD +
                    r"\big)}_{\text{term 1}} + \underbrace{{}^{\mathcal N}\frac{d}{dt}\big(\vec\omega\times\vec r\big)}_{\text{term 2}}",
                    reason="derivative of a sum")
            self.hold()

        with self.voice("v6_04"):
            bd.clear()
            self.play(Transform(hdr, header("Term 1: the transport theorem applied to $^{\\mathcal B}\\dot{\\vec r}$")))
            bd = Board(self, left=-6.0, top=2.3, scale=0.85, buff=0.45)
            bd.line(r"{}^{\mathcal N}\frac{d}{dt}\big(" + BRD + r"\big) = {}^{\mathcal B}\frac{d}{dt}\big(" + BRD + r"\big) + \vec\omega\times" + BRD,
                    reason="it's just another vector")
            l1 = bd.line(r"\text{term 1} = " + BRDD + r" + \vec\omega\times" + BRD, color=B_COL)
            bd.box(l1, B_COL)
            self.hold()

        with self.voice("v6_05"):
            self.play(Transform(hdr, header("Term 2: product rule for a cross product")))
            bd.line(r"{}^{\mathcal N}\frac{d}{dt}\big(\vec\omega\times\vec r\big) = \Big({}^{\mathcal N}\frac{d}{dt}\vec\omega\Big)\times\vec r + \vec\omega\times\Big({}^{\mathcal N}\frac{d}{dt}\vec r\Big)",
                    reason="keep the order of each cross product", below=True)
            self.hold()

        with self.voice("v6_06"):
            bd.line(r"{}^{\mathcal N}\frac{d}{dt}\vec\omega = {}^{\mathcal B}\frac{d}{dt}\vec\omega + \underbrace{\vec\omega\times\vec\omega}_{0} \equiv \dot{\vec\omega}",
                    reason="same in both frames")
            bd.line(r"{}^{\mathcal N}\frac{d}{dt}\vec r = \vec v = " + BRD + r" + \vec\omega\times\vec r", reason="we already know this")
            self.hold()

        with self.voice("v6_07"):
            l2 = bd.line(r"\text{term 2} = \dot{\vec\omega}\times\vec r + \vec\omega\times" + BRD + r" + \vec\omega\times(\vec\omega\times\vec r)",
                         color=Q_COL, reason="substitute and distribute")
            bd.box(l2, Q_COL)
            self.hold()

        with self.voice("v6_08"):
            bd.clear()
            self.play(Transform(hdr, header("Add the two terms")))
            full = T(r"\vec a = ", BRDD, r" + ", r"\vec\omega\times" + BRD, r" + ", r"\dot{\vec\omega}\times\vec r", r" + ",
                     r"\vec\omega\times" + BRD, r" + ", r"\vec\omega\times(\vec\omega\times\vec r)").scale(0.95).move_to(UP * 1.5)
            t1 = Brace(VGroup(full[1], full[3]), UP, color=B_COL)
            t2 = Brace(VGroup(full[5], full[9]), DOWN, color=Q_COL)
            t1l = Tx("term 1", color=B_COL).scale(0.6).next_to(t1, UP, buff=0.1)
            t2l = Tx("term 2", color=Q_COL).scale(0.6).next_to(t2, DOWN, buff=0.1)
            self.play(Write(full), run_time=3.0)
            self.play(GrowFromCenter(t1), FadeIn(t1l), GrowFromCenter(t2), FadeIn(t2l))
            self.wait(1.0)
            self.play(full[3].animate.set_color(V_COL), full[7].animate.set_color(V_COL))
            self.play(Indicate(full[3], color=V_COL), Indicate(full[7], color=V_COL))
            twice = Tx(r"the same term appears twice", color=V_COL).scale(0.65).next_to(t2l, DOWN, buff=0.3)
            self.play(FadeIn(twice))
            self.hold()

        with self.voice("v6_09"):
            self.play(FadeOut(VGroup(t1, t2, t1l, t2l, twice)))
            fin = T(r"{}^{\mathcal N}\ddot{\vec r} = ", BRDD, r" + ", r"\dot{\vec\omega}\times\vec r", r" + ", r"2\,\vec\omega\times" + BRD,
                    r" + ", r"\vec\omega\times(\vec\omega\times\vec r)").scale(1.05).move_to(UP * 0.4)
            self.play(TransformMatchingTex(full, fin), run_time=2.0)
            box = SurroundingRectangle(fin, color=YELLOW, buff=0.25)
            self.play(Create(box))
            self.hold()

        def tag(i, text, color, direction=DOWN):
            b = Brace(fin[i], direction, color=color, buff=0.15)
            t = Tx(text, color=color).scale(0.6).next_to(b, direction, buff=0.1)
            return VGroup(b, t)

        with self.voice("v6_10"):
            self.play(FadeOut(box), fin.animate.move_to(UP * 1.5))
            g1 = tag(1, r"relative:\\seen riding in $\mathcal B$", B_COL)
            self.play(fin[1].animate.set_color(B_COL), GrowFromCenter(g1[0]), FadeIn(g1[1]))
            self.hold()

        with self.voice("v6_11"):
            g2 = tag(3, r"tangential (Euler):\\spin rate changing", Q_COL, UP)
            self.play(fin[3].animate.set_color(Q_COL), GrowFromCenter(g2[0]), FadeIn(g2[1]))
            self.hold()

        with self.voice("v6_12"):
            g3 = tag(5, r"Coriolis:\\moving relative to $\mathcal B$", V_COL)
            self.play(fin[5].animate.set_color(V_COL), GrowFromCenter(g3[0]), FadeIn(g3[1]))
            self.hold()

        with self.voice("v6_13"):
            g4 = tag(7, r"centripetal", P_COL, UP)
            self.play(fin[7].animate.set_color(P_COL), GrowFromCenter(g4[0]), FadeIn(g4[1]))
            bd = Board(self, left=-5.5, top=-0.5, scale=0.78, buff=0.32)
            bd.line(r"\vec r = R\,\hat b_1,\quad \vec\omega = \omega\,\hat b_3:\qquad \vec\omega\times\vec r = \omega R\,(\hat b_3\times\hat b_1) = \omega R\,\hat b_2")
            bd.line(r"\vec\omega\times(\vec\omega\times\vec r) = \omega\,\hat b_3\times\omega R\,\hat b_2 = \omega^2 R\,(\hat b_3\times\hat b_2)",
                    indent=0.6)
            l = bd.line(r"= -\,\omega^2 R\,\hat b_1", color=P_COL, indent=0.6, reason="$\\hat b_3\\times\\hat b_2 = -\\hat b_1$: inward, size $\\omega^2R$")
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(g1, g2, g3, g4)), fin.animate.scale(0.75).to_edge(UP, buff=0.9))

        # ---- Coriolis puck
        ang = ValueTracker(0)
        self.add(ang)
        with self.voice("v6_14"):
            self.play(Transform(hdr, header("The Coriolis effect, made visible")))
            LC, RC = np.array([-3.5, -1.4, 0]), np.array([3.5, -1.4, 0])
            ldisk = SpinningDisk(LC, ang)
            rdisk = make_disk().move_to(RC)
            lt = Tx("Seen from above ($\\mathcal N$)", color=N_COL).scale(0.7).next_to(ldisk, UP, buff=0.25)
            rt = Tx("Seen riding the disk ($\\mathcal B$)", color=B_COL).scale(0.7).next_to(rdisk, UP, buff=0.25)
            self.play(FadeIn(ldisk), FadeIn(rdisk), FadeIn(lt), FadeIn(rt))
            t = ValueTracker(0)
            self.add(t)
            p0, v0 = np.array([-1.7, -0.6, 0]), np.array([0.5, 0.13, 0])
            pos_n = lambda: p0 + v0 * t.get_value()
            pos_b = lambda: rot2(pos_n(), -0.75 * t.get_value())
            ang.add_updater(lambda m: m.set_value(0.75 * t.get_value()))
            puck_l = always_redraw(lambda: Dot(LC + pos_n(), color=YELLOW, radius=0.1))
            puck_r = always_redraw(lambda: Dot(RC + pos_b(), color=YELLOW, radius=0.1))
            tr_l = TracedPath(lambda: LC + pos_n(), stroke_color=YELLOW, stroke_width=3)
            tr_r = TracedPath(lambda: RC + pos_b(), stroke_color=YELLOW, stroke_width=3)
            self.add(tr_l, tr_r, puck_l, puck_r)
            self.play(t.animate.set_value(7.0), run_time=min(9.0, self.left() - 4.0), rate_func=linear)
            n1 = Tx("straight line: no force", color=YELLOW).scale(0.6).next_to(ldisk, DOWN, buff=0.3)
            n2 = Tx("curves: Coriolis + centripetal", color=YELLOW).scale(0.6).next_to(rdisk, DOWN, buff=0.3)
            self.play(FadeIn(n1), FadeIn(n2))
            self.hold()
        for m_ in (puck_l, puck_r, tr_l, tr_r, ldisk, ang):
            m_.clear_updaters()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))


class V6Examples(Lesson):
    def construct(self):
        ang = ValueTracker(0)
        Lt = ValueTracker(0.7)
        self.add(ang, Lt)
        C = np.array([-4.4, -0.8, 0])

        def b1w():
            return np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0])

        def tip():
            return C + Lt.get_value() * b1w()
        body = always_redraw(lambda: Square(1.0, color=GREY_B, fill_color="#1B2233", fill_opacity=1).rotate(ang.get_value()).move_to(C))
        arm = always_redraw(lambda: Line(C, tip(), color=GREY_A, stroke_width=8))
        mass = always_redraw(lambda: Square(0.22, color=YELLOW, fill_color=YELLOW, fill_opacity=1).rotate(ang.get_value()).move_to(tip()))
        with self.voice("v6_15"):
            hdr = header("Example 1: the telescoping arm, acceleration")
            self.play(FadeIn(hdr))
            self.add(body, arm, mass)
            ang.add_updater(lambda m, dt: m.increment_value(0.35 * dt))
            Lt.add_updater(lambda m, dt: m.set_value(min(1.8, m.get_value() + 0.08 * dt)))
            given = T(r"\vec r = L\,\hat b_1,\qquad \vec\omega = \omega\,\hat b_3\ (\text{const})").scale(0.8).move_to(RIGHT * 2.2 + UP * 2.3)
            self.play(Write(given))
            self.hold()

        with self.voice("v6_16"):
            bd = Board(self, left=-1.6, top=1.5, scale=0.78, buff=0.38)
            bd.line(r"\text{relative: } " + BRDD + r" = \ddot L\,\hat b_1", color=B_COL)
            bd.line(r"\text{tangential: } \dot{\vec\omega}\times\vec r = \vec 0", color=Q_COL, reason="$\\omega$ is constant")
            self.hold()

        with self.voice("v6_17"):
            bd.line(r"\text{Coriolis: } 2\,\omega\,\hat b_3\times\dot L\,\hat b_1 = 2\omega\dot L\,\hat b_2", color=V_COL,
                    reason="$\\hat b_3\\times\\hat b_1 = \\hat b_2$")
            self.hold()

        with self.voice("v6_18"):
            bd.line(r"\text{centripetal: } -\,\omega^2 L\,\hat b_1", color=P_COL, reason="as shown in the concept video")
            self.hold()

        with self.voice("v6_19"):
            l = bd.line(r"\vec a = (\ddot L - \omega^2 L)\,\hat b_1 + 2\omega\dot L\,\hat b_2", color=YELLOW)
            bd.box(l)
            bd.line(r"L = L_0 + ct:\ \ \vec a = -\,\omega^2 L\,\hat b_1 + 2\omega c\,\hat b_2", indent=0.6, reason="$\\dot L = c,\\ \\ddot L = 0$")
            inward = always_redraw(lambda: vec(tip(), tip() - 0.5 * Lt.get_value() * b1w(), P_COL, 5))
            side = always_redraw(lambda: vec(tip(), tip() + 0.8 * rot2(UP, ang.get_value()), V_COL, 5))
            self.add(inward, side)
            self.play(FadeIn(inward), FadeIn(side))
            push = Tx("the arm must push the mass sideways", color=V_COL).scale(0.6).next_to(body, DOWN, buff=1.6)
            self.play(FadeIn(push))
            self.hold()
        for m_ in (body, arm, mass, inward, side, ang, Lt):
            m_.clear_updaters()
        bd.clear()
        self.play(FadeOut(VGroup(body, arm, mass, inward, side, given, push)))

        # ---- polar coordinates
        with self.voice("v6_20"):
            self.play(Transform(hdr, header("Example 2: polar coordinates, the door to orbital mechanics")))
            S = np.array([-6.2, -2.4, 0])
            th0 = 0.7
            sun = Dot(S, color=YELLOW, radius=0.15)
            P = S + 2.0 * np.array([np.cos(th0), np.sin(th0), 0])
            planet = Dot(P, color=B_COL, radius=0.12)
            rr = Arrow(S, P, buff=0.1, color=R_COL, stroke_width=4)
            er = Arrow(P, P + 0.9 * np.array([np.cos(th0), np.sin(th0), 0]), buff=0, color=B_COL, stroke_width=4)
            et = Arrow(P, P + 0.9 * np.array([-np.sin(th0), np.cos(th0), 0]), buff=0, color=B_COL, stroke_width=4)
            erl = T(r"\hat e_r", color=B_COL).scale(0.6).next_to(er.get_end(), UR, buff=0.05)
            etl = T(r"\hat e_\theta", color=B_COL).scale(0.6).next_to(et.get_end(), UP, buff=0.05)
            arc = Arc(radius=0.7, angle=th0, arc_center=S, color=YELLOW)
            tl = T(r"\theta", color=YELLOW).scale(0.6).move_to(S + 0.95 * np.array([np.cos(th0 / 2), np.sin(th0 / 2), 0]))
            ref = DashedLine(S, S + RIGHT * 2.4, color=DIM)
            diag = VGroup(ref, rr, sun, planet, er, et, erl, etl, arc, tl)
            self.play(FadeIn(diag))
            bd = Board(self, left=-1.6, top=2.3, scale=0.78, buff=0.36)
            bd.line(r"\vec r = r\,\hat e_r,\qquad \vec\omega^{\mathcal E/\mathcal N} = \dot\theta\,\hat e_3")
            self.hold()

        with self.voice("v6_21"):
            bd.line(r"\text{relative: } \ddot r\,\hat e_r", color=B_COL)
            bd.line(r"\text{tangential: } \ddot\theta\,\hat e_3\times r\,\hat e_r = r\ddot\theta\,\hat e_\theta", color=Q_COL, reason="$\\hat e_3\\times\\hat e_r = \\hat e_\\theta$")
            bd.line(r"\text{Coriolis: } 2\dot\theta\,\hat e_3\times\dot r\,\hat e_r = 2\dot r\dot\theta\,\hat e_\theta", color=V_COL)
            self.hold()

        with self.voice("v6_22"):
            bd.line(r"\text{centripetal: } \dot\theta\,\hat e_3\times(r\dot\theta\,\hat e_\theta) = -\,r\dot\theta^2\,\hat e_r", color=P_COL,
                    reason="$\\hat e_3\\times\\hat e_\\theta = -\\hat e_r$")
            self.hold()

        with self.voice("v6_23"):
            l = bd.line(r"\vec a = (\ddot r - r\dot\theta^2)\,\hat e_r + (r\ddot\theta + 2\dot r\dot\theta)\,\hat e_\theta", color=YELLOW)
            bd.box(l)
            self.hold()
        bd.clear()

        with self.voice("v6_24"):
            bd = Board(self, left=-1.6, top=2.3, scale=0.78, buff=0.4)
            bd.line(r"\text{gravity is along } \hat e_r \ \Rightarrow\ r\ddot\theta + 2\dot r\dot\theta = 0")
            bd.line(r"r\ddot\theta + 2\dot r\dot\theta = \frac{1}{r}\frac{d}{dt}\big(r^2\dot\theta\big)", reason="check with the product rule")
            l = bd.line(r"\Rightarrow\ h = r^2\dot\theta = \text{constant}", color=Q_COL, reason="specific angular momentum")
            kep = Tx("Kepler's 2nd law: equal areas in equal times", color=Q_COL).scale(0.65)
            bd.line(mob=kep, indent=0.6)
            self.hold()

        with self.voice("v6_25"):
            bd.line(r"\ddot r - r\dot\theta^2 = -\frac{\mu}{r^2}", color=P_COL, reason="radial part = gravity")
            bd.line(r"\Rightarrow\ r(\theta) = \frac{p}{1 + e\cos\theta}\quad \text{(conic sections: ellipses)}", color=P_COL, indent=0.6)
            self.play(FadeOut(diag))
            a_, e_ = 1.5, 0.5
            b_ = a_ * np.sqrt(1 - e_ ** 2)
            F = np.array([-4.6, -1.6, 0])
            ell = Ellipse(width=2 * a_, height=2 * b_, color=GREY_B).move_to(F + LEFT * a_ * e_)

            def Pm(M):
                E = M
                for _ in range(30):
                    E = E - (E - e_ * np.sin(E) - M) / (1 - e_ * np.cos(E))
                return F + np.array([a_ * (np.cos(E) - e_), b_ * np.sin(E), 0])
            Mt = ValueTracker(0)
            self.add(Mt)
            pl = always_redraw(lambda: Dot(Pm(Mt.get_value()), color=B_COL, radius=0.09))
            sunD = Dot(F, color=YELLOW, radius=0.12)
            wed = lambda M0, M1: Polygon(*([F] + [Pm(m) for m in np.linspace(M0, M1, 30)]), stroke_width=0, fill_color=Q_COL, fill_opacity=0.45)
            self.play(Create(ell), FadeIn(sunD))
            self.add(pl)
            self.play(FadeIn(wed(-0.5, 0.5)), FadeIn(wed(PI - 0.5, PI + 0.5)))
            self.play(Mt.animate.set_value(2 * TAU), run_time=max(1.0, self.left() - 0.3), rate_func=linear)
        pl.clear_updaters()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("v6_26"):
            h, rows = recap(self, [
                r"Apply the transport theorem twice, using the product rule.",
                r"The term $\vec\omega\times{}^{\mathcal B}\dot{\vec r}$ appears twice: that's the factor 2 in Coriolis.",
                r"${}^{\mathcal N}\ddot{\vec r} = {}^{\mathcal B}\ddot{\vec r} + \dot{\vec\omega}\times\vec r + 2\vec\omega\times{}^{\mathcal B}\dot{\vec r} + \vec\omega\times(\vec\omega\times\vec r)$",
                r"relative \ $+$ \ tangential \ $+$ \ Coriolis \ $+$ \ centripetal",
            ])
            for rrow in rows:
                self.play(FadeIn(rrow, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
