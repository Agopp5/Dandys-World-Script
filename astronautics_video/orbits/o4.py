"""Part 4: the orbit equation from the eccentricity vector, and conic sections."""
from ocommon import *  # noqa: F401,F403

ECC = 0.5
P = 1.6


def cone_slice(m, z0=0.55, tan_a=0.7, H=2.2, n=400):
    """Polylines where the plane z = z0 + m x cuts the double cone x^2 + y^2 = (z tan a)^2."""
    segs, cur = [], []
    phis = np.linspace(-PI, PI, n)
    for nappe in (1, -1):
        cur = []
        for ph in phis:
            den = 1 - nappe * m * tan_a * np.cos(ph)
            ok = abs(den) > 1e-6
            if ok:
                z = z0 / den
                ok = (nappe * z > 0) and abs(z) <= H
            if ok:
                rho = abs(z) * tan_a
                cur.append(np.array([rho * np.cos(ph), rho * np.sin(ph), z]))
            elif cur:
                segs.append(cur)
                cur = []
        if cur:
            segs.append(cur)
    return [s for s in segs if len(s) > 2]


class O4Concept(OLesson):
    def construct(self):
        with self.voice("o4_01"):
            t = o_title(self, 4, "The Orbit Equation", "the eccentricity vector and conic sections")
            self.wait(1.5)
            self.play(FadeOut(t))
            hdr = header("Hunting for a third constant")
            self.play(FadeIn(hdr))
            goal = T(r"r(\theta) = \ ?", color=YELLOW).scale(1.0).shift(UP * 1.2)
            idea = T(r"\text{consider}\quad \vec v\times\vec h").scale(0.9).next_to(goal, DOWN, buff=0.7)
            self.play(Write(goal))
            self.play(FadeIn(idea))
            self.hold()
        self.play(FadeOut(VGroup(goal, idea)))

        with self.voice("o4_02"):
            self.play(Transform(hdr, header("A third conserved vector")))
            bd = Board(self, left=-6.5, top=2.7, scale=0.8, buff=0.42)
            bd.line(r"\frac{d}{dt}\big(\vec v\times\vec h\big) = \ddot{\vec r}\times\vec h + \vec v\times\underbrace{\dot{\vec h}}_{=\,\vec 0}", reason="product rule; $\\vec h$ is constant")
            bd.line(r"= -\frac{\mu}{r^3}\,\vec r\times\big(\vec r\times\vec v\big)", indent=0.6, reason="$\\ddot{\\vec r} = -\\mu\\vec r/r^3,\\ \\vec h = \\vec r\\times\\vec v$")
            self.hold()

        with self.voice("o4_03"):
            bd.line(r"\vec a\times(\vec b\times\vec c) = \vec b\,(\vec a\cdot\vec c) - \vec c\,(\vec a\cdot\vec b)", color=B_COL, reason="triple product identity")
            bd.line(r"\vec r\times(\vec r\times\vec v) = \vec r\,(\vec r\cdot\vec v) - \vec v\,(\vec r\cdot\vec r)", indent=0.6, reason="$\\vec a = \\vec b = \\vec r,\\ \\vec c = \\vec v$")
            self.hold()

        with self.voice("o4_04"):
            bd.line(r"= r\dot r\;\vec r - r^2\,\vec v", indent=0.6, reason="$\\vec r\\cdot\\vec v = r\\dot r,\\ \\vec r\\cdot\\vec r = r^2$")
            l = bd.line(r"\frac{d}{dt}\big(\vec v\times\vec h\big) = \mu\,\frac{r\,\vec v - \dot r\,\vec r}{r^2}", color=YELLOW, reason="multiply by $-\\mu/r^3$")
            self.hold()

        with self.voice("o4_05"):
            bd.line(r"\frac{d}{dt}\Big(\frac{\vec r}{r}\Big) = \frac{r\,\vec v - \dot r\,\vec r}{r^2}", color=YELLOW, reason="quotient rule: the same!")
            self.hold()

        with self.voice("o4_06"):
            bd.line(r"\frac{d}{dt}\Big(\vec v\times\vec h - \mu\,\frac{\vec r}{r}\Big) = \vec 0", color=Q_COL)
            l = bd.line(r"\vec v\times\vec h - \mu\,\frac{\vec r}{r} = \vec c = \text{constant}", color=YELLOW)
            bd.box(l)
            self.hold()
        bd.clear()

        with self.voice("o4_07"):
            self.play(Transform(hdr, header("Dot with $\\vec r$")))
            bd = Board(self, left=-6.5, top=2.7, scale=0.8, buff=0.42)
            bd.line(r"\vec r\cdot\vec c = \vec r\cdot\big(\vec v\times\vec h\big) - \mu\,\frac{\vec r\cdot\vec r}{r}")
            bd.line(r"\vec r\cdot(\vec v\times\vec h) = \vec h\cdot(\vec r\times\vec v) = \vec h\cdot\vec h = h^2", indent=0.6,
                    reason="cycle the triple product")
            l = bd.line(r"\vec r\cdot\vec c = h^2 - \mu r", color=YELLOW)
            self.hold()

        with self.voice("o4_08"):
            bd.line(r"r\,c\cos\theta = h^2 - \mu r", reason="$\\theta$: angle from $\\vec c$ to $\\vec r$")
            bd.line(r"r\,\big(\mu + c\cos\theta\big) = h^2", indent=0.6)
            self.hold()

        with self.voice("o4_09"):
            l = bd.line(r"r = \frac{h^2/\mu}{1 + (c/\mu)\cos\theta}", color=YELLOW, reason="the orbit equation")
            bd.box(l)
            self.hold()

        with self.voice("o4_10"):
            l = bd.line(r"r = \frac{p}{1 + e\cos\theta},\qquad p = \frac{h^2}{\mu},\quad e = \frac{c}{\mu}", color=V_COL,
                        reason="a conic section")
            self.hold()
        bd.clear()

        # ------------------------------------------- eccentricity vector picture
        orb = Orb(focus=(-2.6, -0.6), k=1.25)
        ell = orb.conic(P, ECC)
        e_ = earth(orb.f, 0.18)
        th = ValueTracker(0.6)
        L = 1.1

        def pos():
            return orb.at(P, ECC, th.get_value())

        O2 = np.array([2.2, -2.0, 0])

        def a1():
            t_ = th.get_value()
            return O2 + L * np.array([np.cos(t_) + ECC, np.sin(t_), 0])
        pl = always_redraw(lambda: planet(pos()))
        rv = always_redraw(lambda: Line(orb.f, pos(), color=WHITE, stroke_width=2.5))
        A1 = always_redraw(lambda: Arrow(O2, a1(), buff=0, color=VEL, stroke_width=5, tip_length=0.16))
        A2 = always_redraw(lambda: Arrow(a1(), O2 + L * ECC * RIGHT, buff=0, color=ER_COL, stroke_width=5, tip_length=0.16))
        EV2 = Arrow(O2, O2 + L * ECC * RIGHT, buff=0, color=E_VEC, stroke_width=8, tip_length=0.2)
        EV = Arrow(orb.f, orb.f + 1.2 * RIGHT, buff=0, color=E_VEC, stroke_width=8, tip_length=0.2)
        circ_hint = DashedVMobject(Circle(radius=L, color=DIM, stroke_width=2).move_to(O2 + L * ECC * RIGHT), num_dashes=40)
        with self.voice("o4_11"):
            self.play(Transform(hdr, header("The eccentricity vector")))
            self.play(Create(ell), FadeIn(e_))
            self.add(rv, pl)
            bd = Board(self, left=1.2, top=2.6, scale=0.8, buff=0.4)
            bd.line(r"\vec e = \frac{\vec v\times\vec h}{\mu} - \frac{\vec r}{r}", color=E_VEC, reason="$|\\vec e| = e$")
            l1 = T(r"\frac{\vec v\times\vec h}{\mu}", color=VEL).scale(0.6).move_to([4.6, 0.7, 0])
            l2 = T(r"-\frac{\vec r}{r}", color=ER_COL).scale(0.6).next_to(l1, RIGHT, buff=0.4)
            l3 = T(r"=\ \vec e", color=E_VEC).scale(0.6).next_to(l2, RIGHT, buff=0.3)
            self.play(FadeIn(Dot(O2, radius=0.04)), FadeIn(A1), FadeIn(A2), FadeIn(l1), FadeIn(l2), FadeIn(circ_hint))
            self.play(GrowArrow(EV2), FadeIn(l3))
            self.play(TransformFromCopy(EV2, EV))
            self.play(th.animate.set_value(0.6 + TAU), run_time=max(3, min(8, self.left() - 4)), rate_func=linear)
            peri = Tx("points to periapsis", color=E_VEC).scale(0.55).next_to(orb.at(P, ECC, 0), RIGHT, buff=0.15)
            self.play(FadeIn(peri))
            self.hold()

        ang = always_redraw(lambda: Arc(radius=0.55, start_angle=0, angle=th.get_value() % TAU, arc_center=orb.f, color=YELLOW))
        angl = always_redraw(lambda: T(r"\theta", color=YELLOW).scale(0.6).move_to(orb.f + 0.85 * orb.unit((th.get_value() % TAU) / 2)))
        with self.voice("o4_12"):
            self.play(FadeOut(VGroup(A1, A2, l1, l2, l3, EV2, circ_hint)), *[FadeOut(m) for m in self.mobjects if isinstance(m, Dot) and np.allclose(m.get_center(), O2)])
            self.play(FadeIn(ang), FadeIn(angl))
            bd.line(r"\theta:\ \text{true anomaly}\ \ (\text{HW: } f)", color=YELLOW, reason="measured from periapsis")
            self.play(th.animate.set_value(0.6 + TAU + 1.6), run_time=3)
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(ell, e_, rv, pl, EV, peri, ang, angl)))

        # ------------------------------------------- slicing a cone
        cam = Cam(phi=72, theta=-25, scale=1.05, center=(-2.8, -0.2))
        D = Draw(cam)
        self.add(*cam.trackers())
        tan_a, Hc = 0.7, 2.2
        gens = VGroup()
        for ph in np.linspace(0, TAU, 12, endpoint=False):
            d = np.array([tan_a * np.cos(ph), tan_a * np.sin(ph), 1.0])
            gens.add(D.line(-Hc * d, Hc * d, DIM, 1.5))
        rims = VGroup(*[D.curve(lambda t, z=z: np.array([Hc * tan_a * np.cos(t), Hc * tan_a * np.sin(t), z]), (0, TAU), DIM, 2)
                        for z in (-Hc, Hc)])
        axisl = D.line([0, 0, -Hc - 0.3], [0, 0, Hc + 0.3], DIM, 1.5, dashed=True)
        mt = ValueTracker(0.0)
        z0 = 0.55

        def plane_pts():
            m = mt.get_value()
            xs = np.array([-1.8, 1.8])
            if abs(m) > 1e-6:
                lo, hi = sorted([(-Hc - z0) / m, (Hc - z0) / m])
                xs = np.clip(xs, lo, hi)
            return [np.array([x, y, z0 + m * x]) for x, y in [(xs[0], -1.8), (xs[1], -1.8), (xs[1], 1.8), (xs[0], 1.8)]]
        plane = D.polygon(plane_pts, B_COL, 0.18)

        def slice_mob():
            g = VGroup()
            for seg in cone_slice(mt.get_value(), z0, tan_a, Hc):
                m = VMobject(stroke_color=YELLOW, stroke_width=5)
                m.set_points_as_corners([cam.p(q) for q in seg])
                g.add(m)
            return g
        curve = always_redraw(slice_mob)
        name = Tx("circle", color=YELLOW).scale(0.8).move_to([3.6, 1.6, 0])
        with self.voice("o4_13"):
            self.play(Transform(hdr, header("Why ``conic sections''?")))
            self.add(axisl, gens, rims)
            self.play(*[FadeIn(g) for g in gens], *[FadeIn(r) for r in rims], run_time=1.5)
            self.add(plane, curve)
            self.play(FadeIn(name))
            self.wait(1.5)
            self.play(mt.animate.set_value(0.6), Transform(name, Tx("ellipse", color=YELLOW).scale(0.8).move_to(name)), run_time=2.5)
            self.hold()

        with self.voice("o4_14"):
            self.play(mt.animate.set_value(1 / tan_a), Transform(name, Tx(r"parabola\\(parallel to the side)", color=YELLOW).scale(0.8).move_to(name)), run_time=3)
            self.wait(1.5)
            self.play(mt.animate.set_value(3.2), Transform(name, Tx(r"hyperbola\\(two branches)", color=YELLOW).scale(0.8).move_to(name)), run_time=3)
            cam.start_spin(self, 0.12)
            self.hold()
        cam.stop_spin()
        g3 = flat(gens, rims, axisl, plane)
        self.play(*hide(*g3), FadeOut(curve), FadeOut(name))
        self.remove(*g3, curve)

        # ------------------------------------------- the e sweep
        orb2 = Orb(focus=(-1.2, -0.3), k=0.9)
        et = ValueTracker(0.0)

        def conic_now(rmax=4.0, p_=1.5):
            e = et.get_value()
            if e < 1e-3 or p_ / (1 - e + 1e-9) <= rmax and e < 1:
                return orb2.conic(p_, e, color=YELLOW, width=4)
            lim = np.arccos(np.clip((p_ / rmax - 1) / e, -1, 1))
            return orb2.conic(p_, e, -lim, lim, color=YELLOW, width=4)
        cn = always_redraw(conic_now)
        e2 = earth(orb2.f, 0.16)
        enum = always_redraw(lambda: VGroup(T("e = ", color=WHITE).scale(0.8),
                                            DecimalNumber(et.get_value(), num_decimal_places=2, color=YELLOW).scale(0.8)).arrange(RIGHT, buff=0.1).move_to([4.6, 2.5, 0]))

        def kind():
            e = et.get_value()
            s = "circle" if e < 0.02 else ("ellipse" if e < 0.985 else ("parabola" if e < 1.015 else "hyperbola"))
            return Tx(s, color=B_COL).scale(0.75).move_to([4.6, 1.8, 0])
        kd = always_redraw(kind)
        table = VGroup(*[Tx(s).scale(0.55) for s in [r"$e = 0$: circle", r"$0 < e < 1$: ellipse", r"$e = 1$: parabola", r"$e > 1$: hyperbola"]])
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.6, -0.6, 0])
        with self.voice("o4_15"):
            self.play(Transform(hdr, header("Eccentricity decides the conic")))
            self.play(FadeIn(e2), FadeIn(cn), FadeIn(enum), FadeIn(kd))
            self.play(FadeIn(table))
            self.play(et.animate.set_value(0.6), run_time=3)
            self.play(et.animate.set_value(1.0), run_time=3)
            self.wait(0.8)
            self.play(et.animate.set_value(1.6), run_time=3)
            self.hold()
        self.play(FadeOut(VGroup(cn, e2, enum, kd, table)))
        self.remove(cn, enum, kd)

        # ------------------------------------------- focus and directrix
        orb3 = Orb(focus=(-2.6, -0.5), k=1.2)
        e3 = 0.5
        p3 = 1.6
        xd = p3 / e3
        el3 = orb3.conic(p3, e3)
        F3 = Dot(orb3.f, color=SUN, radius=0.08)
        Fl = T("F", color=SUN).scale(0.6).next_to(orb3.f, DOWN, buff=0.12)
        dline = DashedLine(orb3.P(xd, -2.2), orb3.P(xd, 2.2), color=V_COL)
        dlab = Tx("directrix", color=V_COL).scale(0.5).next_to(orb3.P(xd, -2.2), DOWN, buff=0.08)
        th3 = 2.0
        Q = orb3.at(p3, e3, th3)
        r3 = p3 / (1 + e3 * np.cos(th3))
        with self.voice("o4_16"):
            self.play(Transform(hdr, header("Focus and directrix")))
            self.play(Create(el3), FadeIn(F3), FadeIn(Fl))
            self.play(Create(dline), FadeIn(dlab))
            pd = DoubleArrow(orb3.f + 0.35 * DOWN * 0 + DOWN * 0.0, orb3.P(xd, 0), buff=0, color=V_COL, stroke_width=3, tip_length=0.12)
            pdl = T(r"p/e", color=V_COL).scale(0.55).next_to(pd, DOWN, buff=0.08)
            self.play(GrowFromCenter(pd), FadeIn(pdl))
            rq = Line(orb3.f, Q, color=WHITE, stroke_width=3)
            dq = DashedLine(Q, orb3.P(xd, r3 * np.sin(th3)), color=ET_COL)
            rql = T("r", color=WHITE).scale(0.6).next_to(rq.get_center(), DOWN, buff=0.1)
            dql = T("d", color=ET_COL).scale(0.6).next_to(dq.get_center(), UP, buff=0.1)
            self.play(FadeIn(Dot(Q, color=B_COL)), Create(rq), Create(dq), FadeIn(rql), FadeIn(dql))
            bd = Board(self, left=1.6, top=2.6, scale=0.8, buff=0.42)
            l = bd.line(r"r = e\,d", color=YELLOW, reason="every point of the conic")
            self.hold()

        with self.voice("o4_17"):
            bd.line(r"d = \frac{p}{e} - r\cos\theta", reason="horizontal distance")
            bd.line(r"r = e\Big(\frac{p}{e} - r\cos\theta\Big) = p - e\,r\cos\theta")
            l = bd.line(r"r\,(1 + e\cos\theta) = p", color=YELLOW, reason="same equation")
            bd.box(l)
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(dline, dlab, pd, pdl, rq, dq, rql, dql)), *[FadeOut(m) for m in self.mobjects if isinstance(m, Dot) and m is not F3])

        with self.voice("o4_18"):
            self.play(Transform(hdr, header("Three special points")))
            pts = [(0.0, Q_COL, r"r_p = \frac{p}{1+e}", RIGHT), (PI / 2, V_COL, r"r = p", UP), (PI, P_COL, r"r_a = \frac{p}{1-e}", DR)]
            for thp, col, tex, d in pts:
                qq = orb3.at(p3, e3, thp)
                ln = Line(orb3.f, qq, color=col, stroke_width=4)
                lb = T(tex, color=col).scale(0.6).next_to(qq, d, buff=0.15)
                self.play(Create(ln), FadeIn(Dot(qq, color=col)), FadeIn(lb), run_time=1.2)
            tags = VGroup(Tx(r"$\theta = 0$: periapsis", color=Q_COL), Tx(r"$\theta = 90^\circ$: semi-latus rectum", color=V_COL),
                          Tx(r"$\theta = 180^\circ$: apoapsis (ellipse)", color=P_COL)).scale(0.6)
            tags.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, 1.5, 0])
            self.play(FadeIn(tags))
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("o4_19"):
            h, rows = recap(self, [
                r"$\vec v\times\vec h - \mu\,\vec r/r = \vec c$ is constant.",
                r"Dot with $\vec r$: $r = \dfrac{p}{1 + e\cos\theta}$, with $p = h^2/\mu$ and $e = c/\mu$.",
                r"$\vec e = \vec v\times\vec h/\mu - \vec r/r$ points to periapsis; $\theta$ (or $f$) is the true anomaly.",
                r"$e = 0$ circle, $0<e<1$ ellipse, $e = 1$ parabola, $e > 1$ hyperbola.",
            ])
            for rr in rows:
                self.play(FadeIn(rr, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
