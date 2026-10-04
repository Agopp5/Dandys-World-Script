"""Part 5-6: transport theorem, the UFO example, acceleration, outro."""
from common import *  # noqa: F401,F403
from proj3d import Cam, Draw, grow, show, hide, flat


def rot2(v, a):
    c, s = np.cos(a), np.sin(a)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0.0])


def make_disk(radius=1.9, stripes=8, axes=True):
    g = VGroup(Circle(radius=radius, color=GREY_B, stroke_width=3, fill_color="#1B2233", fill_opacity=1))
    for k in range(stripes):
        a = TAU * k / stripes
        g.add(Line(ORIGIN, radius * np.array([np.cos(a), np.sin(a), 0]), color="#2E3850", stroke_width=2))
    if axes:
        g.add(Arrow(ORIGIN, RIGHT * (radius * 0.75), buff=0, color=B_COL, stroke_width=4, tip_length=0.18))
        g.add(Arrow(ORIGIN, UP * (radius * 0.75), buff=0, color=B_COL, stroke_width=4, tip_length=0.18))
    return g


class SpinningDisk(VGroup):
    """A disk drawn about `center` that rotates with tracker `angle`."""

    def __init__(self, center, angle, radius=1.9, **kw):
        super().__init__(**kw)
        self.ctr = np.array(center)
        self.angle = angle
        self.base = make_disk(radius).move_to(self.ctr)
        self.add(self.base)
        self._last = 0.0
        self.add_updater(self._spin)

    def _spin(self, m):
        a = self.angle.get_value()
        self.base.rotate(a - self._last, about_point=self.ctr)
        self._last = a

    def to_world(self, v_body):
        return self.ctr + rot2(v_body, self.angle.get_value())


def vec(start, end, color, width=5, tip=0.18):
    s, e = np.array(start), np.array(end)
    if np.linalg.norm(e - s) < 1e-3:
        e = s + RIGHT * 1e-3
    return Arrow(s, e, buff=0, color=color, stroke_width=width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=1000)


TRANSPORT = r"{}^{\mathcal N}\frac{d}{dt}\vec r = {}^{\mathcal B}\frac{d}{dt}\vec r + \vec\omega^{\mathcal B/\mathcal N}\times\vec r"


# =============================================================== Transport
class Transport(Scene2D):
    def construct(self):
        with self.voice("trans_1"):
            hdr = Tx("The transport theorem", color=B_COL).scale(0.9).to_edge(UP, buff=0.3)
            q = T(r"\frac{d}{dt}\vec r", r"\ =\ ?").scale(1.6)
            self.play(Write(hdr))
            self.play(Write(q), run_time=1.5)
            self.hold()

        with self.voice("trans_2"):
            ea = T(r"\vec r = r_1\,\hat b_1 + r_2\,\hat b_2 + r_3\,\hat b_3").scale(0.9).next_to(hdr, DOWN, buff=0.4)
            self.play(FadeOut(q), Write(ea))
            eb = T(r"\frac{d}{dt}\vec r =", r"\sum_i \dot r_i\,\hat b_i", r"+", r"\sum_i r_i\,\frac{d}{dt}\hat b_i").scale(0.95)
            eb.next_to(ea, DOWN, buff=0.45)
            self.play(Write(eb), run_time=2.0)
            b1 = Brace(eb[1], DOWN, color=Q_COL)
            b1l = Tx("components change", color=Q_COL).scale(0.6).next_to(b1, DOWN, buff=0.1).shift(LEFT * 0.7)
            self.play(GrowFromCenter(b1), FadeIn(b1l))
            self.wait(1.0)
            b2 = Brace(eb[3], DOWN, color=W_COL)
            b2l = Tx("basis vectors change?", color=W_COL).scale(0.6).next_to(b2, DOWN, buff=0.1).shift(RIGHT * 0.7)
            self.play(GrowFromCenter(b2), FadeIn(b2l))
            self.hold()

        with self.voice("trans_3"):
            lbox = VGroup(Tx("Riding along in $\\mathcal B$", color=B_COL).scale(0.75),
                          T(r"{}^{\mathcal B}\frac{d}{dt}\hat b_i = 0").scale(0.85),
                          T(r"\Rightarrow\ {}^{\mathcal B}\frac{d}{dt}\vec r = \sum_i \dot r_i\,\hat b_i").scale(0.85)
                          ).arrange(DOWN, buff=0.3)
            rbox = VGroup(Tx("Watching from $\\mathcal N$", color=N_COL).scale(0.75),
                          T(r"{}^{\mathcal N}\frac{d}{dt}\hat b_i = \vec\omega^{\mathcal B/\mathcal N}\times\hat b_i").scale(0.85),
                          Tx("(the axes are spinning)", color=DIM).scale(0.6)).arrange(DOWN, buff=0.3)
            VGroup(lbox, rbox).arrange(RIGHT, buff=1.5).to_edge(DOWN, buff=0.45)
            lfr = SurroundingRectangle(lbox, color=B_COL, buff=0.25, corner_radius=0.1)
            rfr = SurroundingRectangle(rbox, color=N_COL, buff=0.25, corner_radius=0.1)
            self.play(Create(lfr), FadeIn(lbox[0]))
            self.play(Write(lbox[1]))
            self.wait(1.0)
            self.play(Write(lbox[2]))
            self.wait(1.5)
            self.play(Create(rfr), FadeIn(rbox[0]))
            self.play(Write(rbox[1]), FadeIn(rbox[2]), run_time=min(2.0, self.left()))
            self.hold()

        with self.voice("trans_4"):
            self.play(FadeOut(VGroup(ea, eb, b1, b1l, b2, b2l, lbox, rbox, lfr, rfr)))
            l1 = T(r"{}^{\mathcal N}\frac{d}{dt}\vec r", r"= {}^{\mathcal B}\frac{d}{dt}\vec r + \sum_i r_i\,(\vec\omega\times\hat b_i)").scale(0.9)
            l2 = T(r"= {}^{\mathcal B}\frac{d}{dt}\vec r + \vec\omega\times", r"\sum_i r_i\,\hat b_i").scale(0.9)
            l1.next_to(hdr, DOWN, buff=0.8)
            l2.next_to(l1, DOWN, buff=0.4).align_to(l1[1], LEFT)
            self.play(Write(l1), run_time=2.0)
            self.play(Write(l2), run_time=1.5)
            br = Brace(l2[1], DOWN, color=R_COL)
            brl = T(r"\vec r", color=R_COL).next_to(br, DOWN, buff=0.1)
            self.play(GrowFromCenter(br), FadeIn(brl))
            final = T(TRANSPORT).scale(1.15)
            frame = SurroundingRectangle(final, color=YELLOW, buff=0.25)
            tag = Tx("Transport theorem", color=YELLOW).scale(0.8).next_to(frame, DOWN, buff=0.2)
            VGroup(final, frame, tag).next_to(brl, DOWN, buff=0.5)
            self.play(Write(final), run_time=2.0)
            self.play(Create(frame), FadeIn(tag), run_time=min(1.2, self.left()))
            self.hold()
        theorem = VGroup(final, frame)

        # ---- two observers of the same disk
        ang = ValueTracker(0)
        w = 0.6
        rho = ValueTracker(1.3)
        self.add(ang, rho)
        LC, RC = np.array([-3.5, -1.3, 0]), np.array([3.5, -1.3, 0])
        p_body = lambda: rho.get_value() * np.array([np.cos(0.5), np.sin(0.5), 0])
        with self.voice("trans_5"):
            self.play(FadeOut(VGroup(l1, l2, br, brl, tag)), theorem.animate.scale(0.7).to_edge(UP, buff=0.25),
                      FadeOut(hdr))
            ldisk = make_disk().move_to(LC)
            rdisk = SpinningDisk(RC, ang)
            lt = Tx("Riding along in $\\mathcal B$", color=B_COL).scale(0.7).next_to(ldisk, UP, buff=0.25)
            rt = Tx("Watching from $\\mathcal N$", color=N_COL).scale(0.7).next_to(rdisk, UP, buff=0.25)
            wsym = VGroup(Circle(radius=0.11, color=W_COL, stroke_width=3), Dot(radius=0.035, color=W_COL)).move_to(RC)
            wlab = T(r"\vec\omega", color=W_COL).scale(0.6).next_to(wsym, DL, buff=0.05)
            self.play(FadeIn(ldisk), FadeIn(rdisk), FadeIn(lt), FadeIn(rt), FadeIn(wsym), FadeIn(wlab))
            lp = always_redraw(lambda: Dot(LC + p_body(), color=R_COL, radius=0.09))
            rp = always_redraw(lambda: Dot(rdisk.to_world(p_body()), color=R_COL, radius=0.09))
            rr = always_redraw(lambda: vec(RC, rdisk.to_world(p_body()), R_COL, 4))
            trail = TracedPath(lambda: rdisk.to_world(p_body()), stroke_color=R_COL, stroke_width=2, stroke_opacity=0.5)
            self.add(trail, lp, rp, rr)
            ang.add_updater(lambda m, dt: m.increment_value(w * dt))
            ltxt = T(r"{}^{\mathcal B}\dot{\vec r} = 0", color=B_COL).scale(0.8).next_to(ldisk, DOWN, buff=0.3)
            self.wait(2.5)
            self.play(Write(ltxt))
            wxr = always_redraw(lambda: vec(rdisk.to_world(p_body()),
                                            rdisk.to_world(p_body()) + 0.9 * w * rot2(np.cross([0, 0, 1], p_body()), ang.get_value()),
                                            W_COL, 5))
            rtxt = T(r"{}^{\mathcal N}\dot{\vec r} = \vec\omega\times\vec r", color=W_COL).scale(0.8).next_to(rdisk, DOWN, buff=0.3)
            self.wait(2.0)
            self.add(wxr)
            self.play(FadeIn(wxr), Write(rtxt))
            self.hold()

        with self.voice("trans_6"):
            self.play(FadeOut(ltxt), FadeOut(rtxt), run_time=0.5)
            rdot = 0.13
            rho.add_updater(lambda m, dt: m.set_value(min(1.85, m.get_value() + rdot * dt)))
            self.play(rho.animate.set_value(0.45), run_time=0.8)
            u = np.array([np.cos(0.5), np.sin(0.5), 0])
            lv = always_redraw(lambda: vec(LC + p_body(), LC + p_body() + 3.5 * rdot * u, Q_COL, 5))
            rv = always_redraw(lambda: vec(rdisk.to_world(p_body()), rdisk.to_world(p_body()) + 3.5 * rdot * rot2(u, ang.get_value()), Q_COL, 5))
            tot = always_redraw(lambda: vec(rdisk.to_world(p_body()), rdisk.to_world(p_body())
                                            + 3.5 * rdot * rot2(u, ang.get_value())
                                            + 0.9 * w * rot2(np.cross([0, 0, 1], p_body()), ang.get_value()), WHITE, 5))
            self.add(lv, rv, tot)
            leq = T(r"{}^{\mathcal B}\dot{\vec r}", r"\ \text{(sliding)}", color=Q_COL).scale(0.75).next_to(ldisk, DOWN, buff=0.3)
            req = T(r"{}^{\mathcal N}\dot{\vec r}", "=", r"{}^{\mathcal B}\dot{\vec r}", "+", r"\vec\omega\times\vec r").scale(0.8)
            req[2].set_color(Q_COL)
            req[4].set_color(W_COL)
            req.next_to(rdisk, DOWN, buff=0.3)
            self.play(FadeIn(lv), FadeIn(rv), FadeIn(tot), Write(leq), Write(req), run_time=1.5)
            self.hold()
            rho.clear_updaters()

        with self.voice("trans_7"):
            for m in (lp, rp, rr, wxr, lv, rv, tot, trail, rdisk):
                m.clear_updaters()
            ang.clear_updaters()
            self.play(FadeOut(VGroup(ldisk, rdisk, lt, rt, wsym, wlab, lp, rp, rr, trail, wxr, lv, rv, tot, leq, req)))
            pts = VGroup(
                Tx(r"$\bullet$ Works for \emph{any} vector: positions, velocities, momenta, \dots"),
                Tx(r"$\bullet$ Pick the frame where the vector looks simplest"),
                Tx(r"$\bullet$ Take the easy derivative there"),
                Tx(r"$\bullet$ Let ", r"$\vec\omega\times\vec r$", r" handle the rest"),
            ).scale(0.8).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(theorem, DOWN, buff=0.8)
            pts[3][1].set_color(W_COL)
            for p in pts:
                self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.3, (self.left() - 1.0) / 4 - 0.6))
            self.hold()

        with self.voice("trans_8"):
            self.play(FadeOut(pts))
            # small top-view diagram of the rotating frame E
            O = np.array([-4.6, -1.6, 0])
            th0 = 0.6
            n1 = Arrow(O, O + RIGHT * 2.2, buff=0, color=N_COL, stroke_width=3)
            n1l = T(r"\hat n_1", color=N_COL).scale(0.6).next_to(n1.get_end(), RIGHT, buff=0.05)
            e1 = Arrow(O, O + 2.2 * np.array([np.cos(th0), np.sin(th0), 0]), buff=0, color=B_COL, stroke_width=4)
            e2 = Arrow(O, O + 1.4 * np.array([-np.sin(th0), np.cos(th0), 0]), buff=0, color=B_COL, stroke_width=4)
            e1l = T(r"\hat e_1", color=B_COL).scale(0.6).next_to(e1.get_end(), UR, buff=0.05)
            e2l = T(r"\hat e_2", color=B_COL).scale(0.6).next_to(e2.get_end(), UP, buff=0.05)
            pt = Dot(O + 1.6 * np.array([np.cos(th0), np.sin(th0), 0]), color=R_COL)
            Rl = T("R", color=R_COL).scale(0.6).next_to(pt, DOWN, buff=0.12)
            tharc = Arc(radius=0.6, angle=th0, arc_center=O, color=YELLOW)
            thl = T(r"\theta", color=YELLOW).scale(0.6).move_to(O + 0.85 * np.array([np.cos(th0 / 2), np.sin(th0 / 2), 0]))
            diag = VGroup(n1, n1l, e1, e2, e1l, e2l, pt, Rl, tharc, thl)
            z3 = T(r"\hat e_3 = \hat n_3\ \text{out of page}", color=DIM).scale(0.5).next_to(O, DOWN, buff=0.35)
            diag.add(z3)
            self.play(FadeIn(diag))
            s1 = T(r"\vec r = R\,\hat e_1 + z\,\hat e_3,\qquad \vec\omega^{\mathcal E/\mathcal N} = \dot\theta\,\hat e_3").scale(0.75)
            s2 = T(r"{}^{\mathcal N}\dot{\vec r}", r"=", r"\dot R\,\hat e_1 + \dot z\,\hat e_3", r"+",
                   r"\dot\theta\,\hat e_3\times(R\,\hat e_1 + z\,\hat e_3)").scale(0.75)
            s2[2].set_color(B_COL)
            s2[4].set_color(W_COL)
            s3 = T(r"= \dot R\,\hat e_1 + R\dot\theta\,\hat e_2 + \dot z\,\hat e_3").scale(0.85)
            col = VGroup(s1, s2, s3).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 1.6 + DOWN * 0.9)
            self.play(Write(s1), run_time=1.8)
            self.wait(1.2)
            self.play(Write(s2), run_time=2.0)
            self.wait(1.5)
            self.play(Write(s3), run_time=1.5)
            fr = SurroundingRectangle(s3, color=YELLOW)
            hard = T(r"\text{vs. }(\dot R\cos\theta - \dot\theta R\sin\theta)\hat n_1 + (\dot R\sin\theta + \dot\theta R\cos\theta)\hat n_2 + \dot z\,\hat n_3",
                     color=DIM).scale(0.55).next_to(col, DOWN, buff=0.45)
            self.play(Create(fr), FadeIn(hard))
            self.hold()
        self.play(FadeOut(Group(*self.mobjects)))


# ===================================================================== UFO
class UFO(Scene2D):
    def construct(self):
        cam = Cam(phi=72, theta=-25, scale=1.05, center=(2.7, -0.7))
        D = Draw(cam)
        self.add(*cam.trackers())
        Re, Ru = 2.0, 2.45
        lat = np.radians(40.8)
        L0 = np.radians(35 + 282.1)
        rot = ValueTracker(-1.2)
        spin = ValueTracker(0.25)
        rot.add_updater(lambda m, dt: m.increment_value(spin.get_value() * dt))
        self.add(rot, spin)

        def U(r=Ru):
            a = L0 + rot.get_value()
            return r * np.array([np.cos(lat) * np.cos(a), np.cos(lat) * np.sin(a), np.sin(lat)])

        earth = D.sphere(ORIGIN, Re, "#7FB3FF", rot=lambda: rot.get_value())
        N, nlabs = D.frame(np.eye(3), N_COL, 3.3, [r"\hat n_1", r"\hat n_2", r"\hat n_3"], width=3, k=1, label_op=1)
        site = D.dot(lambda: U(Re), YELLOW, 0.06)
        ufo = D.dot(U, "#9EE6C0", 0.1)
        ulab = D.label("U", lambda: U() + np.array([0, 0, 0.3]), "#9EE6C0", 0.7, op=1)
        hdr = Tx("Back to the UFO", color=B_COL).scale(0.9).to_corner(UL)

        with self.voice("ufo_1"):
            self.add(earth, N, nlabs, site, ufo, ulab)
            self.play(FadeIn(hdr))
            facts = VGroup(
                T(r"R_\oplus + h = 6370 + 80 = 6450\ \text{km}"),
                T(r"\phi = 40.8^\circ\ \text{N}"),
                T(r"\lambda = 282.1^\circ,\quad \theta = 35^\circ"),
                T(r"|\vec\omega_{\mathcal E/\mathcal N}| = 7.29\times10^{-5}\ \text{rad/s}", color=W_COL),
            ).scale(0.7).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(hdr, DOWN, buff=0.5, aligned_edge=LEFT)
            fixed = Tx("fixed in the Earth frame $\\mathcal E$", color=DIM).scale(0.6)
            fixed.next_to(facts, DOWN, buff=0.4, aligned_edge=LEFT)
            for f in facts[:3]:
                self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.7)
                self.wait(1.0)
            self.play(FadeIn(fixed))
            dur = self.left() - 0.2
            # slow the spin so the globe arrives at the sighting orientation (rot = 0)
            spin.set_value(1.2 / dur * 1.0)
            self.wait(dur)
            spin.set_value(0)
            rot.clear_updaters()
            rot.set_value(0)

        with self.voice("ufo_2"):
            r_ar = D.arrow(ORIGIN, U, R_COL, width=6, k=0)
            proj = lambda: np.array([U()[0], U()[1], 0])
            pline = D.line(U, proj, DIM, 2, dashed=True, op=0)
            eqline = D.line(ORIGIN, proj, DIM, 2, dashed=True, op=0)
            a_lat = D.arc(lambda: np.cross(proj(), [0, 0, 1]), proj, lat, 1.0, YELLOW)
            a_lon = D.arc([0, 0, 1], [1, 0, 0], L0 - TAU, 0.8, V_COL)
            l_lat = D.label(r"\phi", lambda: 1.25 * (np.cos(lat / 2) * proj() / np.linalg.norm(proj())
                                                     + np.array([0, 0, np.sin(lat / 2)])), YELLOW, 0.7)
            l_lon = D.label(r"\theta+\lambda", lambda: 1.25 * np.array([np.cos((L0 - TAU) / 2), np.sin((L0 - TAU) / 2), 0]), V_COL, 0.6)
            self.add(r_ar, pline, eqline, a_lat, a_lon, l_lat, l_lon)
            self.play(*grow(r_ar), *show(pline, eqline))
            self.play(*show(l_lat, l_lon))
            eq = T(r"\vec r_{(\mathcal N)} = (R_\oplus + h)\begin{bmatrix}\cos\phi\cos(\theta+\lambda)\\"
                   r"\cos\phi\sin(\theta+\lambda)\\ \sin\phi\end{bmatrix}"
                   r"= \begin{bmatrix}3577\\-3324\\4215\end{bmatrix}\text{km}").scale(0.62)
            eq.next_to(hdr, DOWN, buff=0.5, aligned_edge=LEFT)
            self.play(FadeOut(facts), FadeOut(fixed))
            self.play(Write(eq), run_time=3.0)
            self.hold()

        with self.voice("ufo_3"):
            w_ar = D.arrow(ORIGIN, [0, 0, 3.0], W_COL, width=8, k=0)
            wl = D.label(r"\vec\omega", [0.0, 0.0, 3.35], W_COL, 0.8)
            v_ar = D.arrow(U, lambda: U() + 0.55 * np.cross([0, 0, 1.0], U()), Q_COL, width=6, k=0)
            vl = D.label(r"\vec v", lambda: U() + 0.62 * np.cross([0, 0, 1.0], U()) + np.array([0, 0, 0.25]), Q_COL, 0.8)
            self.add(w_ar, wl, v_ar, vl)
            self.play(*grow(w_ar), *show(wl), *hide(nlabs[2]))
            veq = T(r"\vec v = \underbrace{{}^{\mathcal E}\dot{\vec r}}_{0} + \vec\omega\times\vec r"
                    r"= \begin{bmatrix}242.3\\260.7\\0\end{bmatrix}\text{m/s}").scale(0.62)
            veq.next_to(eq, DOWN, buff=0.45, aligned_edge=LEFT)
            vmag = T(r"|\vec v| = \omega (R_\oplus+h)\cos\phi \approx 356\ \text{m/s, due east}", color=Q_COL).scale(0.62)
            vmag.next_to(veq, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(Write(veq), run_time=2.5)
            self.play(*grow(v_ar), *show(vl))
            self.play(Write(vmag), run_time=1.5)
            # let the Earth turn again so the velocity can be seen
            circle = D.curve(lambda t: Ru * np.array([np.cos(lat) * np.cos(t), np.cos(lat) * np.sin(t), np.sin(lat)]),
                             (0, TAU), Q_COL, 2, n=90, op=0)
            self.add(circle)
            rot.add_updater(lambda m, dt: m.increment_value(0.3 * dt))
            self.play(*show(circle, to=0.5))
            self.hold()

        with self.voice("ufo_4"):
            a_ar = D.arrow(U, lambda: U() - 0.4 * np.array([U()[0], U()[1], 0]), P_COL, width=6, k=0)
            al = D.label(r"\vec a", lambda: U() - 0.45 * np.array([U()[0], U()[1], 0]) + np.array([0, 0, -0.3]), P_COL, 0.8)
            self.add(a_ar, al)
            self.play(*grow(a_ar), *show(al))
            aeq = T(r"\vec a = \vec\omega\times(\vec\omega\times\vec r) = \begin{bmatrix}-0.0190\\0.0177\\0\end{bmatrix}\text{m/s}^2").scale(0.62)
            aeq.next_to(vmag, DOWN, buff=0.45, aligned_edge=LEFT)
            amag = T(r"|\vec a| = \omega^2 (R_\oplus+h)\cos\phi \approx 0.026\ \text{m/s}^2", color=P_COL).scale(0.62)
            amag.next_to(aeq, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(Write(aeq), run_time=2.5)
            self.wait(2.0)
            self.play(Write(amag), run_time=1.5)
            inward = Tx("points toward Earth's spin axis", color=DIM).scale(0.55).next_to(amag, DOWN, buff=0.2, aligned_edge=LEFT)
            self.play(FadeIn(inward), run_time=min(1.0, self.left()))
            self.hold()
        for m in self.mobjects:
            m.clear_updaters()
        self.play(FadeOut(Group(*self.mobjects)))


# ============================================================ Acceleration
class Acceleration(Scene2D):
    def construct(self):
        hdr = Tx("Acceleration", color=B_COL).scale(0.9).to_edge(UP, buff=0.3)
        with self.voice("acc_1"):
            self.play(Write(hdr))
            l1 = T(r"\vec v = {}^{\mathcal N}\frac{d}{dt}\vec r = {}^{\mathcal B}\dot{\vec r} + \vec\omega\times\vec r").scale(0.85)
            l1.next_to(hdr, DOWN, buff=0.5)
            self.play(Write(l1), run_time=2.0)
            self.wait(1.5)
            l2 = T(r"{}^{\mathcal N}\frac{d}{dt}\vec v = ",
                   r"{}^{\mathcal B}\frac{d}{dt}\Big({}^{\mathcal B}\dot{\vec r} + \vec\omega\times\vec r\Big)",
                   r"+", r"\vec\omega\times\Big({}^{\mathcal B}\dot{\vec r} + \vec\omega\times\vec r\Big)").scale(0.8)
            l2.next_to(l1, DOWN, buff=0.5)
            self.play(Write(l2), run_time=3.0)
            self.hold()

        with self.voice("acc_2"):
            l3 = T(r"= {}^{\mathcal B}\ddot{\vec r}", r"+", r"\dot{\vec\omega}\times\vec r", r"+",
                   r"\vec\omega\times{}^{\mathcal B}\dot{\vec r}", r"+", r"\vec\omega\times{}^{\mathcal B}\dot{\vec r}",
                   r"+", r"\vec\omega\times(\vec\omega\times\vec r)").scale(0.8)
            l3.next_to(l2, DOWN, buff=0.5)
            self.play(Write(l3), run_time=2.5)
            self.play(l3[4].animate.set_color(V_COL), l3[6].animate.set_color(V_COL))
            self.play(Indicate(l3[4], color=V_COL), Indicate(l3[6], color=V_COL), run_time=min(1.2, self.left()))
            self.hold()

        with self.voice("acc_3"):
            fin = T(r"{}^{\mathcal N}\ddot{\vec r} =", r"{}^{\mathcal B}\ddot{\vec r}", r"+", r"\dot{\vec\omega}\times\vec r", r"+",
                    r"2\,\vec\omega\times{}^{\mathcal B}\dot{\vec r}", r"+", r"\vec\omega\times(\vec\omega\times\vec r)").scale(1.0)
            fin.next_to(hdr, DOWN, buff=0.6)
            self.play(FadeOut(VGroup(l1, l2)), ReplacementTransform(l3, fin), run_time=1.5)
            self.hold()

        def tag(part, text, color):
            b = Brace(fin[part], DOWN, color=color, buff=0.1)
            t = Tx(text, color=color).scale(0.6).next_to(b, DOWN, buff=0.1)
            return VGroup(b, t)

        ang = ValueTracker(0)
        w = ValueTracker(0.4)
        self.add(ang, w)
        ang.add_updater(lambda m, dt: m.increment_value(w.get_value() * dt))
        C = np.array([0, -1.9, 0])
        disk = SpinningDisk(C, ang, radius=1.5)
        pb = np.array([1.1, 0, 0])

        with self.voice("acc_4"):
            t1 = tag(1, "relative", B_COL)
            self.play(fin[1].animate.set_color(B_COL), GrowFromCenter(t1[0]), FadeIn(t1[1]))
            self.wait(2.5)
            t2 = tag(3, "tangential", Q_COL)
            self.play(fin[3].animate.set_color(Q_COL), GrowFromCenter(t2[0]), FadeIn(t2[1]))
            self.play(FadeIn(disk))
            p = always_redraw(lambda: Dot(disk.to_world(pb), color=R_COL))
            tan = always_redraw(lambda: vec(disk.to_world(pb), disk.to_world(pb) + 0.9 * rot2(UP, ang.get_value()), Q_COL))
            spin_up = Tx("spinning up", color=Q_COL).scale(0.6).next_to(disk, RIGHT, buff=0.4)
            self.add(p, tan)
            self.play(FadeIn(spin_up), w.animate.set_value(2.0), run_time=max(1.0, self.left() - 0.2), rate_func=linear)

        with self.voice("acc_5"):
            t4 = tag(7, "centripetal", P_COL)
            tan.clear_updaters()
            self.play(fin[7].animate.set_color(P_COL), GrowFromCenter(t4[0]), FadeIn(t4[1]), FadeOut(tan), FadeOut(spin_up),
                      w.animate.set_value(1.0))
            cen = always_redraw(lambda: vec(disk.to_world(pb), disk.to_world(0.25 * pb), P_COL))
            inw = Tx("always inward", color=P_COL).scale(0.6).next_to(disk, RIGHT, buff=0.4)
            self.add(cen)
            self.play(FadeIn(cen), FadeIn(inw))
            self.hold()

        with self.voice("acc_6"):
            t3 = tag(5, "Coriolis", V_COL)
            self.play(fin[5].animate.set_color(V_COL), GrowFromCenter(t3[0]), FadeIn(t3[1]))
            only = Tx(r"needs motion \emph{within} the rotating frame", color=V_COL).scale(0.6).next_to(disk, RIGHT, buff=0.4)
            self.play(FadeOut(inw), FadeIn(only))
            self.hold()
        tags = VGroup(t1, t2, t3, t4)

        # ---- frictionless puck: straight in N, curved on the disk
        with self.voice("acc_7"):
            for m in (p, cen, disk):
                m.clear_updaters()
            self.play(FadeOut(VGroup(disk, p, cen, only)), FadeOut(tags),
                      VGroup(fin).animate.scale(0.75).next_to(hdr, DOWN, buff=0.3))
            ang.set_value(0)
            w.set_value(0.75)
            LC, RC = np.array([-3.5, -1.3, 0]), np.array([3.5, -1.3, 0])
            frozen = ValueTracker(0)
            ldisk = SpinningDisk(LC, ang)
            rdisk = make_disk().move_to(RC)
            lt = Tx("Inertial view ($\\mathcal N$)", color=N_COL).scale(0.7).next_to(ldisk, UP, buff=0.25)
            rt = Tx("Riding the disk ($\\mathcal B$)", color=B_COL).scale(0.7).next_to(rdisk, UP, buff=0.25)
            self.play(FadeIn(ldisk), FadeIn(rdisk), FadeIn(lt), FadeIn(rt))
            t = ValueTracker(0)
            p0, v0 = np.array([-1.7, -0.6, 0]), np.array([0.5, 0.13, 0])
            pos_n = lambda: p0 + v0 * t.get_value()
            pos_b = lambda: rot2(pos_n(), -0.75 * t.get_value())
            ang.clear_updaters()
            ang.add_updater(lambda m: m.set_value(0.75 * t.get_value()))
            puck_l = always_redraw(lambda: Dot(LC + pos_n(), color=YELLOW, radius=0.1))
            puck_r = always_redraw(lambda: Dot(RC + pos_b(), color=YELLOW, radius=0.1))
            tr_l = TracedPath(lambda: LC + pos_n(), stroke_color=YELLOW, stroke_width=3)
            tr_r = TracedPath(lambda: RC + pos_b(), stroke_color=YELLOW, stroke_width=3)
            self.add(tr_l, tr_r, puck_l, puck_r, t)
            dur = min(7.0, self.left() - 4.0)
            self.play(t.animate.set_value(7.0), run_time=dur, rate_func=linear)
            l_note = Tx("straight line", color=YELLOW).scale(0.6).next_to(ldisk, DOWN, buff=0.3)
            r_note = Tx("curves, with no force acting", color=YELLOW).scale(0.6).next_to(rdisk, DOWN, buff=0.3)
            self.play(FadeIn(l_note), FadeIn(r_note))
            self.hold()

        # ---- merry-go-round (lecture example)
        with self.voice("acc_8"):
            for m in (puck_l, puck_r, tr_l, tr_r, ldisk, ang):
                m.clear_updaters()
            self.play(FadeOut(VGroup(ldisk, rdisk, lt, rt, puck_l, puck_r, tr_l, tr_r, l_note, r_note)))
            ang.set_value(0)
            wr = 0.5
            ang.add_updater(lambda m, dt: m.increment_value(wr * dt))
            MC = np.array([-4.0, -1.2, 0])
            mgr = SpinningDisk(MC, ang, radius=2.1)
            R = ValueTracker(0.9)
            self.add(R)
            person = always_redraw(lambda: Dot(mgr.to_world(np.array([R.get_value(), 0, 0])), color=YELLOW, radius=0.11))
            mt = Tx("merry-go-round", color=DIM).scale(0.6).next_to(mgr, UP, buff=0.2)
            self.play(FadeIn(mgr), FadeIn(mt))
            self.add(person)
            m1 = T(r"\vec r = R\,\hat b_1,\qquad \vec\omega^{\mathcal B/\mathcal N} = \dot\theta\,\hat b_3\ \ (\text{const})").scale(0.7)
            m2 = T(r"\frac{\vec F}{m} =", r"\ddot R\,\hat b_1", r"+", r"2\dot\theta\,\hat b_3\times\dot R\,\hat b_1", r"+",
                   r"\dot\theta\,\hat b_3\times(\dot\theta\,\hat b_3\times R\,\hat b_1)").scale(0.7)
            m2[1].set_color(B_COL)
            m2[3].set_color(V_COL)
            m2[5].set_color(P_COL)
            m3 = T(r"\frac{\vec F}{m} = (\ddot R - \dot\theta^2 R)\,\hat b_1 + 2\dot\theta\dot R\,\hat b_2").scale(0.85)
            colm = VGroup(m1, m2, m3).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 2.3 + DOWN * 0.6)
            self.play(Write(m1), run_time=2.0)
            self.wait(1.5)
            self.play(Write(m2), run_time=3.0)
            self.wait(1.0)
            box = SurroundingRectangle(m3, color=YELLOW)
            self.play(Write(m3), run_time=2.0)
            self.play(Create(box), run_time=min(1.0, self.left()))
            self.hold()

        with self.voice("acc_9"):
            inward = always_redraw(lambda: vec(mgr.to_world(np.array([R.get_value(), 0, 0])),
                                               mgr.to_world(np.array([R.get_value() * (1 - 0.6), 0, 0])), P_COL))
            stand = T(r"\text{standing: } \tfrac{\vec F}{m} = -\dot\theta^2 R\,\hat b_1", color=P_COL).scale(0.7)
            stand.next_to(colm, DOWN, buff=0.5).align_to(colm, LEFT)
            self.add(inward)
            self.play(FadeIn(inward), Write(stand))
            self.wait(2.0)
            walking = ValueTracker(0)
            self.add(walking)
            side = always_redraw(lambda: vec(mgr.to_world(np.array([R.get_value(), 0, 0])),
                                             mgr.to_world(np.array([R.get_value(), 1.1 * walking.get_value(), 0])), V_COL))
            walk = T(r"\text{walking out: } + 2\dot\theta\dot R\,\hat b_2", r"\ \ \text{(Coriolis)}", color=V_COL).scale(0.7)
            walk.next_to(stand, DOWN, buff=0.3).align_to(stand, LEFT)
            self.add(side)
            self.play(walking.animate.set_value(1.0), Write(walk), run_time=1.0)
            self.play(R.animate.set_value(1.95), run_time=max(1.0, self.left() - 0.3), rate_func=linear)

        # ---- polar coordinates and the door to orbital mechanics
        with self.voice("acc_10"):
            for m in (mgr, person, inward, side, ang):
                m.clear_updaters()
            self.play(FadeOut(VGroup(mgr, person, inward, side, mt, colm, box, stand, walk, fin)))
            p1 = T(r"\vec r = r\,\hat e_r,\qquad \vec\omega^{\mathcal E/\mathcal N} = \dot\theta\,\hat e_3").scale(0.75)
            p2 = T(r"\vec a = ", r"(\ddot r - r\dot\theta^2)", r"\,\hat e_r + ", r"(2\dot r\dot\theta + r\ddot\theta)", r"\,\hat e_\theta").scale(0.85)
            p2[1].set_color(P_COL)
            p2[3].set_color(Q_COL)
            pc = VGroup(p1, p2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(hdr, DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
            self.play(Write(p1), run_time=1.5)
            self.play(Write(p2), run_time=2.5)
            k2 = T(r"(2\dot r\dot\theta + r\ddot\theta) = \tfrac{1}{r}\tfrac{d}{dt}(r^2\dot\theta) = 0"
                   r"\ \Rightarrow\ h = r^2\dot\theta = \text{const}", color=Q_COL).scale(0.65)
            k2l = Tx("Kepler's 2nd law: equal areas in equal times", color=DIM).scale(0.55)
            k1 = T(r"\ddot r - r\dot\theta^2 = -\frac{\mu}{r^2}\ \Rightarrow\ r = \frac{p}{1+e\cos\theta}", color=P_COL).scale(0.65)
            k1l = Tx("conic sections: ellipses", color=DIM).scale(0.55)
            kc = VGroup(k2, k2l, k1, k1l).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(pc, DOWN, buff=0.6).align_to(pc, LEFT)
            # orbit on the right
            a_, e_ = 1.8, 0.5
            F = np.array([4.4, -1.0, 0])
            b_ = a_ * np.sqrt(1 - e_ ** 2)
            ell = Ellipse(width=2 * a_, height=2 * b_, color=GREY_B).move_to(F + RIGHT * a_ * e_)
            sun = Dot(F, color=YELLOW, radius=0.12)

            def P(M):
                E = M
                for _ in range(30):
                    E = E - (E - e_ * np.sin(E) - M) / (1 - e_ * np.cos(E))
                return F + np.array([a_ * (np.cos(E) - e_), b_ * np.sin(E), 0])

            ell.move_to(F + LEFT * a_ * e_)
            Mt = ValueTracker(0)
            planet = always_redraw(lambda: Dot(P(Mt.get_value()), color=B_COL, radius=0.1))
            self.play(Create(ell), FadeIn(sun))
            self.add(Mt, planet)
            self.play(Write(k2), FadeIn(k2l), run_time=1.5)

            def wedge(M0, M1, color):
                pts = [F] + [P(m) for m in np.linspace(M0, M1, 30)]
                return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=0.45)
            w1 = wedge(-0.45, 0.45, Q_COL)
            w2 = wedge(PI - 0.45, PI + 0.45, Q_COL)
            self.play(FadeIn(w1), FadeIn(w2))
            self.play(Write(k1), FadeIn(k1l), run_time=1.5)
            self.play(Mt.animate.set_value(2 * TAU), run_time=max(1.0, self.left() - 0.3), rate_func=linear)
        planet.clear_updaters()
        self.play(FadeOut(Group(*self.mobjects)))


# =================================================================== Outro
class Outro(Scene2D):
    def construct(self):
        with self.voice("outro_1"):
            items = VGroup(
                VGroup(Tx("Vector", color=R_COL), Tx("an arrow")),
                VGroup(Tx("Frame", color=N_COL), Tx("a way of casting its shadows")),
                VGroup(Tx("DCM", color=B_COL), T(r"r_{(\mathcal B)} = C_{\mathcal{BN}}\,r_{(\mathcal N)}")),
                VGroup(Tx("Euler angles", color=Q_COL), T(r"C_{\mathcal{BA}} = C_1(\phi)\,C_2(\theta)\,C_3(\psi)")),
                VGroup(Tx("Angular velocity", color=W_COL), T(r"{}^{\mathcal N}\tfrac{d}{dt}\hat b_i = \vec\omega\times\hat b_i")),
            )
            for it in items:
                it[0].scale(0.8)
                it[1].scale(0.75)
            for it in items:
                it.arrange(RIGHT, buff=0.6)
            items.arrange(DOWN, buff=0.45)
            for it in items:
                it[0].align_to(items, LEFT)
                it[1].move_to(np.array([1.5, it.get_center()[1], 0]), aligned_edge=LEFT)
            items.move_to(ORIGIN)
            each = (self.left() - 0.5) / 5
            for it in items:
                self.play(FadeIn(it, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.1, each - 0.6))

        with self.voice("outro_2"):
            self.play(FadeOut(items))
            thm = T(TRANSPORT).scale(1.25)
            fr = SurroundingRectangle(thm, color=YELLOW, buff=0.3)
            self.play(Write(thm), run_time=2.0)
            self.play(Create(fr))
            once = T(r"\text{once} \Rightarrow \vec v", color=Q_COL).scale(0.9)
            twice = T(r"\text{twice} \Rightarrow \vec a = {}^{\mathcal B}\ddot{\vec r} + \dot{\vec\omega}\times\vec r"
                      r" + 2\vec\omega\times{}^{\mathcal B}\dot{\vec r} + \vec\omega\times(\vec\omega\times\vec r)",
                      color=P_COL).scale(0.8)
            VGroup(once, twice).arrange(DOWN, buff=0.4).next_to(fr, DOWN, buff=0.7)
            self.wait(3.0)
            self.play(FadeIn(once, shift=UP * 0.2))
            self.play(FadeIn(twice, shift=UP * 0.2))
            self.hold()

        with self.voice("outro_3"):
            self.play(FadeOut(VGroup(thm, fr, once, twice)), run_time=0.6)
            title = Tx("Same arrow. Different observers.").scale(1.2)
            self.play(Write(title), run_time=1.5)
            self.hold()
        self.play(FadeOut(title), run_time=1.0)
        self.wait(0.5)
