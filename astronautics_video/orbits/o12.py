"""Part 12: HW 3 Problem 4 - classical orbital elements from two position vectors."""
from ocommon import *  # noqa: F401,F403

N_AX = "#C8C8C8"
NODE = "#FFD644"


def pqw(Om, inc, w):
    C = C3(w) @ C1(inc) @ C3(Om)
    return C[0], C[1], C[2]


def orbit_fn(Om, inc, w, e, p):
    ph, qh, _ = pqw(Om, inc, w)

    def f(t):
        r = p / (1 + e * np.cos(t))
        return r * (np.cos(t) * ph + np.sin(t) * qh)
    return f


def disc(center, u, v, R, n=48):
    return [center + R * (np.cos(t) * u + np.sin(t) * v) for t in np.linspace(0, TAU, n, endpoint=False)]


class O12Problem(OLesson):
    def construct(self):
        cam = Cam(phi=66, theta=-62, scale=1.15, center=(-3.4, -0.7))
        D = Draw(cam)
        self.add(*cam.trackers())

        with self.voice("o12_01"):
            t = o_title(self, 12, "HW 3, Problem 4: The Orbit in 3D", "classical orbital elements from two positions")
            self.wait(1.5)
            self.play(FadeOut(t))
            hdr = header("Orbits live in tilted planes")
            self.play(FadeIn(hdr))
            self.hold()

        # ------------------------------------------------ the inertial frame
        globe = D.sphere(ORIGIN, 0.45, EARTH)
        eq = D.polygon(disc(ORIGIN, np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), 2.5), B_COL, 0.12)
        nf, nl = D.frame(np.eye(3), N_AX, 2.6, [r"\hat n_1", r"\hat n_2", r"\hat n_3"])
        with self.voice("o12_02"):
            self.play(Transform(hdr, header("The geocentric equatorial frame")))
            self.add(eq, globe, nf, nl)
            self.play(FadeIn(globe), *grow(*nf), run_time=1.8)
            self.play(*show(*nl))
            notes = VGroup(Tx(r"$\hat n_1$: toward the vernal equinox"), Tx(r"$\hat n_3$: through the North Pole"),
                           Tx(r"the frame does not rotate")).scale(0.6)
            notes.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, 1.8, 0])
            self.play(FadeIn(notes))
            self.hold()
        self.play(FadeOut(notes))

        # generic orbit for the definitions
        Om, inc, w, e, p = np.radians(40), np.radians(38), np.radians(70), 0.3, 1.75
        ph, qh, wh = pqw(Om, inc, w)
        nhat = np.array([np.cos(Om), np.sin(Om), 0.0])
        orbit = D.curve(orbit_fn(Om, inc, w, e, p), (-PI, PI), YELLOW, 3.5, n=140, k=0)
        oplane = D.polygon(disc(ORIGIN, ph, qh, 2.6), YELLOW, 0.07)
        node = D.line(-2.7 * nhat, 2.7 * nhat, NODE, 2.5, dashed=True)
        asc = D.dot(lambda: orbit_fn(Om, inc, w, e, p)(-w), Q_COL, 0.08)
        ascl = D.label(r"\text{ascending node}", orbit_fn(Om, inc, w, e, p)(-w) + np.array([0.3, 0.5, -0.25]), Q_COL, 0.5)
        ha = D.arrow(ORIGIN, 2.0 * wh, H_COL, 5, k=0)
        hl = D.label(r"\vec h", 2.25 * wh, H_COL, 0.65)
        with self.voice("o12_03"):
            self.play(Transform(hdr, header("The line of nodes")))
            self.add(oplane, orbit, node, asc, ascl, ha, hl)
            self.play(*grow(orbit), run_time=2)
            self.play(*grow(ha), *show(hl))
            self.play(FadeIn(node), FadeIn(asc), *show(ascl))
            bd = Board(self, left=1.2, top=2.6, scale=0.78, buff=0.4)
            bd.line(r"\vec n = \hat n_3\times\vec h", color=NODE, reason="points to the ascending node")
            self.hold()

        Oa = D.arc([0, 0, 1], [1, 0, 0], Om, 1.25, B_COL, 4)
        Ol = D.label(r"\Omega", 1.5 * np.array([np.cos(Om / 2), np.sin(Om / 2), 0]), B_COL, 0.65)
        ia = D.arc(nhat, [0, 0, 1], inc, 1.15, V_COL, 4)
        il = D.label(r"i", 1.35 * (np.cos(inc / 2) * np.array([0, 0, 1.0]) + np.sin(inc / 2) * np.cross(nhat, [0, 0, 1.0])), V_COL, 0.65)
        with self.voice("o12_04"):
            self.play(Transform(hdr, header("Size, shape, tilt and swivel")))
            bd.line(r"a,\ e:\ \text{size and shape}")
            self.add(ia, il)
            self.play(*grow(ia), *show(il))
            bd.line(r"i:\ \angle(\hat n_3, \vec h)", color=V_COL, reason="inclination")
            self.add(Oa, Ol)
            self.play(*grow(Oa), *show(Ol))
            bd.line(r"\Omega:\ \hat n_1 \to \vec n\ \text{(in the equator)}", color=B_COL, reason="RAAN")
            self.hold()

        th = np.radians(55)
        sat = orbit_fn(Om, inc, w, e, p)(th)
        peri = orbit_fn(Om, inc, w, e, p)(0)
        pa = D.arrow(ORIGIN, peri, E_VEC, 4, k=0)
        wa = D.arc(wh, nhat, w, 0.85, Q_COL, 4)
        wl = D.label(r"\omega", 1.1 * (np.cos(w / 2) * nhat + np.sin(w / 2) * np.cross(wh, nhat)), Q_COL, 0.65)
        ta = D.arc(wh, ph, th, 0.6, ER_COL, 4)
        tl = D.label(r"f", 0.82 * (np.cos(th / 2) * ph + np.sin(th / 2) * qh), ER_COL, 0.6)
        sd = D.dot(sat, WHITE, 0.08)
        ra = D.line(ORIGIN, sat, WHITE, 2.5)
        with self.voice("o12_05"):
            self.add(pa, wa, wl)
            self.play(*grow(pa), *grow(wa), *show(wl))
            bd.line(r"\omega:\ \vec n \to \text{periapsis (in the orbit plane)}", color=Q_COL, reason="argument of periapsis", below=True)
            self.add(ra, sd, ta, tl)
            self.play(FadeIn(ra), FadeIn(sd), *grow(ta), *show(tl))
            bd.line(r"f:\ \text{periapsis} \to \text{satellite},\qquad u = \omega + f", color=ER_COL, reason="true anomaly; argument of latitude", below=True)
            cam.start_spin(self, 0.1)
            self.hold()
        cam.stop_spin()
        bd.clear()

        with self.voice("o12_06"):
            self.play(Transform(hdr, header("A 3-1-3 Euler sequence")))
            bd = Board(self, left=1.2, top=2.6, scale=0.78, buff=0.42)
            bd.line(r"\hat n_3 \text{ by } \Omega\ \to\ \text{node line by } i\ \to\ \vec h \text{ by } \omega", reason="three rotations", below=True)
            l = bd.line(r"C^{\mathcal{PN}} = C_3(\omega)\,C_1(i)\,C_3(\Omega)", color=YELLOW)
            bd.box(l)
            self.hold()
        bd.clear()

        with self.voice("o12_07"):
            self.play(Transform(hdr, header("Computing the angles")))
            bd = Board(self, left=1.2, top=2.6, scale=0.76, buff=0.4)
            bd.line(r"\cos i = h_3/h", color=V_COL, reason="$0 \\le i \\le 180^\\circ$")
            bd.line(r"\Omega:\ \text{from } (n_1, n_2)", color=B_COL, reason="use both signs (quadrant)")
            bd.line(r"u = \cos^{-1}\!\big(\hat n\cdot\hat r\big);\ \ r_3 < 0 \Rightarrow u = 360^\circ - u", color=Q_COL, reason="below the equator", below=True)
            self.hold()
        bd.clear()
        g_generic = flat(orbit, oplane, node, asc, ascl, ha, hl, Oa, Ol, ia, il, pa, wa, wl, ta, tl, sd, ra)
        self.play(*hide(*g_generic))
        self.remove(*g_generic)

        # ------------------------------------------------ the homework orbit
        Om2, inc2, w2, e2 = np.radians(45), np.radians(30), np.radians(345), 0.2
        RE_s = 0.45
        a2 = 3 * RE_s
        p2 = a2 * (1 - e2 ** 2)
        f1, f2 = np.radians(320), np.radians(85.6)
        o2 = orbit_fn(Om2, inc2, w2, e2, p2)
        ph2, qh2, wh2 = pqw(Om2, inc2, w2)
        n2 = np.array([np.cos(Om2), np.sin(Om2), 0.0])
        r1v, r2v = o2(f1), o2(f2)
        with self.voice("o12_08"):
            self.play(Transform(hdr, header("HW 3, Problem 4")))
            g = num_card([r"\vec r_1 = (14450.6,\ -1529.9,\ -6524.0)\ \text{km}",
                          r"\vec r_2 = (-6199.5,\ 14699.2,\ 8531.9)\ \text{km}",
                          r"p = 2.88\,R_e = 18{,}369.0\ \text{km}"], scale=0.55).move_to([3.7, 2.1, 0])
            self.play(FadeIn(g))
            r1a = D.arrow(ORIGIN, r1v, ER_COL, 5, k=0)
            r2a = D.arrow(ORIGIN, r2v, ET_COL, 5, k=0)
            r1l = D.label(r"\vec r_1", 1.15 * r1v, ER_COL, 0.6)
            r2l = D.label(r"\vec r_2", 1.15 * r2v, ET_COL, 0.6)
            self.add(r1a, r2a, r1l, r2l)
            self.play(*grow(r1a, r2a), *show(r1l, r2l), run_time=1.5)
            self.hold()

        h2a = D.arrow(ORIGIN, 1.9 * wh2, H_COL, 5, k=0)
        h2l = D.label(r"\hat h \parallel \vec r_1\times\vec r_2", 2.2 * wh2 + np.array([0.0, 0.0, 0.15]), H_COL, 0.55)
        with self.voice("o12_09"):
            self.add(h2a, h2l)
            self.play(*grow(h2a), *show(h2l))
            bd = Board(self, left=0.9, top=1.0, scale=0.74, buff=0.36, ceiling=1.3)
            bd.line(r"\hat h = \frac{\vec r_1\times\vec r_2}{|\vec r_1\times\vec r_2|} = (0.3536,\ -0.3536,\ 0.8660)", color=H_COL,
                    reason="short way: $\\Delta f < 180^\\circ$", below=True)
            self.hold()

        ia2 = D.arc(n2, [0, 0, 1], inc2, 1.1, V_COL, 4)
        with self.voice("o12_10"):
            self.add(ia2)
            self.play(*grow(ia2))
            l = bd.line(r"i = \cos^{-1}(0.8660) = 30^\circ", color=V_COL)
            self.hold()

        node2 = D.line(-2.4 * n2, 2.4 * n2, NODE, 2.5, dashed=True)
        Oa2 = D.arc([0, 0, 1], [1, 0, 0], Om2, 1.2, B_COL, 4)
        with self.voice("o12_11"):
            self.add(node2, Oa2)
            self.play(FadeIn(node2), *grow(Oa2))
            l = bd.line(r"\vec n = (-h_2,\ h_1,\ 0) = (0.3536,\ 0.3536,\ 0)\ \Rightarrow\ \Omega = 45^\circ", color=B_COL, reason="first quadrant", below=True)
            self.hold()
        bd.clear()

        orb2 = D.curve(o2, (-PI, PI), YELLOW, 3.5, n=140, k=0)
        with self.voice("o12_12"):
            self.add(orb2)
            self.play(*grow(orb2), run_time=1.8)
            bd = Board(self, left=0.9, top=1.0, scale=0.74, buff=0.36, ceiling=1.3)
            bd.line(r"r_1 = 15{,}928.7,\quad r_2 = 18{,}091.3\ \text{km}")
            bd.line(r"\cos\Delta f = \frac{\vec r_1\cdot\vec r_2}{r_1 r_2} = -0.5821\ \Rightarrow\ \Delta f = 125.60^\circ", color=YELLOW)
            self.hold()

        with self.voice("o12_13"):
            bd.line(r"e\cos f_1 = p/r_1 - 1 = 0.15320")
            bd.line(r"e\cos(f_1 + \Delta f) = p/r_2 - 1 = 0.01535")
            self.hold()

        with self.voice("o12_14"):
            bd.line(r"e\cos f_1\cos\Delta f - e\sin f_1\sin\Delta f = 0.01535", reason="expand", below=True)
            bd.line(r"e\sin f_1 = \frac{(0.15320)(-0.5821) - 0.01535}{0.8131} = -0.12855", color=YELLOW)
            self.hold()
        bd.clear()

        with self.voice("o12_15"):
            bd = Board(self, left=0.9, top=1.0, scale=0.74, buff=0.36, ceiling=1.3)
            bd.line(r"e = \sqrt{0.15320^2 + 0.12855^2} = 0.200", color=YELLOW)
            bd.line(r"f_1 = \text{atan2}(-0.12855,\ 0.15320) = -40^\circ = 320^\circ", color=ER_COL)
            bd.line(r"f_2 = 320^\circ + 125.6^\circ - 360^\circ = 85.6^\circ", color=ET_COL)
            self.hold()

        with self.voice("o12_16"):
            l = bd.line(r"a = \frac{p}{1 - e^2} = \frac{18{,}369.0}{0.96} = 19{,}134\ \text{km} = 3\,R_e", color=YELLOW)
            self.hold()
        bd.clear()

        peri2 = o2(0)
        pa2 = D.arrow(ORIGIN, peri2, E_VEC, 4, k=0)
        pl2 = D.label(r"\text{periapsis}", 1.25 * peri2, E_VEC, 0.5)
        with self.voice("o12_17"):
            self.add(pa2, pl2)
            self.play(*grow(pa2), *show(pl2))
            bd = Board(self, left=0.9, top=1.0, scale=0.74, buff=0.36, ceiling=1.3)
            bd.line(r"\cos u_1 = \hat n\cdot\hat r_1 = 0.5736\ \Rightarrow\ 55^\circ", reason="$r_{1,3} < 0$: below the equator", below=True)
            bd.line(r"u_1 = 360^\circ - 55^\circ = 305^\circ", color=Q_COL)
            l = bd.line(r"\omega = u_1 - f_1 = 305^\circ - 320^\circ = -15^\circ = 345^\circ", color=YELLOW)
            self.hold()

        with self.voice("o12_18"):
            bd.line(r"\text{check: } u_2 = 70.6^\circ,\ \ \omega = 70.6^\circ - 85.6^\circ = -15^\circ\ \checkmark", color=Q_COL)
            self.hold()
        bd.clear()

        with self.voice("o12_19"):
            bd = Board(self, left=0.9, top=1.0, scale=0.74, buff=0.36, ceiling=1.3)
            bd.line(r"f_1 = 320^\circ \in (180^\circ, 360^\circ):\ \gamma < 0", color=ER_COL, reason="heading to perigee: descending", below=True)
            bd.line(r"f_2 = 85.6^\circ \in (0, 180^\circ):\ \gamma > 0", color=ET_COL, reason="climbing to apogee: ascending", below=True)
            bd.line(r"\text{latitude: both northbound } (\cos u > 0)", color=REASON)
            self.hold()
        bd.clear()

        with self.voice("o12_20"):
            self.play(FadeOut(g))
            ans = VGroup(T(r"a = 3R_e = 19{,}134\ \text{km}"), T(r"e = 0.2"), T(r"i = 30^\circ"), T(r"\Omega = 45^\circ"),
                         T(r"\omega = 345^\circ"), T(r"f_1 = 320^\circ"), T(r"f_2 = 85.6^\circ")).scale(0.7)
            ans.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.8, 0.2, 0])
            box = SurroundingRectangle(ans, color=YELLOW, buff=0.25)
            self.play(LaggedStart(*[FadeIn(a_, shift=RIGHT * 0.2) for a_ in ans], lag_ratio=0.25), run_time=3)
            self.play(Create(box))
            cam.start_spin(self, 0.12)
            self.hold()
        cam.stop_spin()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))
