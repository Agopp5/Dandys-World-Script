"""Part 3-4: Euler angles and angular velocity."""
from common import *  # noqa: F401,F403
from proj3d import Cam, Draw, grow, show, hide, flat


def overlay():
    return Rectangle(width=config.frame_width + 1, height=config.frame_height + 1,
                     fill_color=BG, fill_opacity=0.97, stroke_width=0)


def unfreeze_free(scene, *mobs):
    """Stop camera-driven updaters and fade mobjects out."""
    for m in mobs:
        m.clear_updaters()
    return [FadeOut(m) for m in mobs]


# =================================================================== Euler
class Euler(Scene2D):
    def construct(self):
        cam = Cam(phi=68, theta=28, scale=1.15, center=(-2.4, -0.7))
        D = Draw(cam)
        self.add(*cam.trackers())
        L = 2.4
        psi, th, ph = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        self.add(psi, th, ph)
        col = [P_COL]

        def M():
            return euler321(psi.get_value(), th.get_value(), ph.get_value())

        A, alabs = D.frame(np.eye(3), N_COL, L, [r"\hat a_1", r"\hat a_2", r"\hat a_3"])
        active, _ = D.frame(M, lambda: col[0], L, width=6, k=1.0)
        for a in active:
            a.op.set_value(0)

        hdr = Tx("Euler angles", color=B_COL).scale(0.9).to_corner(UR)
        with self.voice("euler_1"):
            self.add(A, alabs, active)
            self.play(Write(hdr))
            self.play(*grow(*A), *show(*alabs))
            claim = Tx(r"Any orientation $=$\\3 successive rotations").scale(0.75)
            claim.next_to(hdr, DOWN, buff=0.5).to_edge(RIGHT)
            self.play(Write(claim))
            self.play(*show(*active), run_time=0.5)
            self.play(psi.animate.set_value(0.7), th.animate.set_value(-0.5), ph.animate.set_value(0.8), run_time=2.5)
            self.play(psi.animate.set_value(0), th.animate.set_value(0), ph.animate.set_value(0), run_time=2.0)
            self.hold()

        eqs = VGroup(
            T(r"C_{\mathcal{PA}} = C_3(\psi)", color=P_COL),
            T(r"C_{\mathcal{QP}} = C_2(\theta)", color=Q_COL),
            T(r"C_{\mathcal{BQ}} = C_1(\phi)", color=B_COL),
        ).scale(0.85).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(hdr, DOWN, buff=1.4).to_edge(RIGHT, buff=1.0)

        # ---- stage 1: yaw psi about a3
        arc_psi = D.arc([0, 0, 1], [1, 0, 0], psi.get_value, 1.1, YELLOW)
        lab_psi = D.label(r"\psi", lambda: 1.4 * np.array([np.cos(psi.get_value() / 2), np.sin(psi.get_value() / 2), 0]),
                          YELLOW, 0.85)
        with self.voice("euler_2"):
            seq = T(r"3\text{-}2\text{-}1:\ \text{yaw, pitch, roll}").scale(0.8).next_to(hdr, DOWN, buff=0.5).to_edge(RIGHT, buff=1.0)
            self.play(FadeOut(claim), Write(seq))
            self.wait(2.0)
            self.add(arc_psi, lab_psi)
            self.play(*show(lab_psi), run_time=0.5)
            self.play(psi.animate.set_value(np.radians(40)), run_time=2.5)
            self.play(Write(eqs[0]))
            self.hold()
        P = C3(np.radians(40))
        ghostP, plabs = D.frame(P, P_COL, L, [r"\hat p_1", r"\hat p_2", None], width=4)

        # ---- stage 2: pitch theta about p2
        arc_th = D.arc(P[1], P[0], th.get_value, 1.1, YELLOW)
        lab_th = D.label(r"\theta", lambda: 1.4 * (np.cos(th.get_value() / 2) * P[0] - np.sin(th.get_value() / 2) * P[2]),
                         YELLOW, 0.85)
        with self.voice("euler_3"):
            col[0] = Q_COL
            self.add(ghostP, plabs, arc_th, lab_th)
            for g in ghostP:
                g.k.set_value(1)
                g.op.set_value(0.5)
            self.play(*show(*plabs), *show(lab_th), run_time=0.6)
            self.play(th.animate.set_value(np.radians(30)), run_time=2.5)
            self.play(Write(eqs[1]))
            self.hold()
        Q = C2(np.radians(30)) @ P
        ghostQ, qlabs = D.frame(Q, Q_COL, L, [r"\hat q_1", None, r"\hat q_3"], width=4)

        # ---- stage 3: roll phi about q1
        arc_ph = D.arc(Q[0], Q[1], ph.get_value, 1.1, YELLOW)
        lab_ph = D.label(r"\phi", lambda: 1.4 * (np.cos(ph.get_value() / 2) * Q[1] + np.sin(ph.get_value() / 2) * Q[2]),
                         YELLOW, 0.85)
        with self.voice("euler_4"):
            col[0] = B_COL
            self.add(ghostQ, qlabs, arc_ph, lab_ph)
            for g in ghostQ:
                g.k.set_value(1)
                g.op.set_value(0.5)
            self.play(*show(*qlabs), *show(lab_ph), *[g.op.animate.set_value(0.2) for g in ghostP],
                      *show(*plabs, to=0.35), run_time=0.6)
            self.play(ph.animate.set_value(np.radians(35)), run_time=2.5)
            self.play(Write(eqs[2]))
            self.hold()
        B = M()
        _, blabs = D.frame(B, B_COL, L, [r"\hat b_1", r"\hat b_2", r"\hat b_3"])
        self.add(blabs)
        self.play(*show(*blabs), run_time=0.5)

        # ---- the chain, on an overlay
        ov = overlay()
        with self.voice("euler_5"):
            self.play(FadeIn(ov), run_time=0.6)
            chain = T(r"\begin{bmatrix}\hat b_1\\\hat b_2\\\hat b_3\end{bmatrix} = ",
                      r"C_{\mathcal{BQ}}", r"C_{\mathcal{QP}}", r"C_{\mathcal{PA}}",
                      r"\begin{bmatrix}\hat a_1\\\hat a_2\\\hat a_3\end{bmatrix}").scale(0.85).to_edge(UP, buff=0.7)
            chain[1].set_color(B_COL)
            chain[2].set_color(Q_COL)
            chain[3].set_color(P_COL)
            cba = T(r"C_{\mathcal{BA}} = ", r"C_1(\phi)", r"\,C_2(\theta)", r"\,C_3(\psi)").scale(1.0)
            cba[1].set_color(B_COL)
            cba[2].set_color(Q_COL)
            cba[3].set_color(P_COL)
            cba.next_to(chain, DOWN, buff=0.6)
            mats = VGroup(
                T(r"C_1(\phi)=\begin{bmatrix}1&0&0\\0&\cos\phi&\sin\phi\\0&-\sin\phi&\cos\phi\end{bmatrix}", color=B_COL),
                T(r"C_2(\theta)=\begin{bmatrix}\cos\theta&0&-\sin\theta\\0&1&0\\\sin\theta&0&\cos\theta\end{bmatrix}", color=Q_COL),
                T(r"C_3(\psi)=\begin{bmatrix}\cos\psi&\sin\psi&0\\-\sin\psi&\cos\psi&0\\0&0&1\end{bmatrix}", color=P_COL),
            ).scale(0.6).arrange(RIGHT, buff=0.45).next_to(cba, DOWN, buff=0.9)
            self.play(Write(chain), run_time=1.8)
            self.wait(1.5)
            self.play(Write(cba), run_time=1.5)
            note = Tx(r"last rotation on the left", color=DIM).scale(0.6).next_to(cba, RIGHT, buff=0.4)
            self.play(FadeIn(note))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in mats], lag_ratio=0.4),
                      run_time=min(2.5, self.left()))
            self.hold()

        with self.voice("euler_6"):
            self.play(FadeOut(VGroup(chain, mats, note)), cba.animate.to_edge(UP, buff=0.6))
            count = T(r"3", r"\times", r"2", r"\times", r"2", r"= 12").scale(1.2).next_to(cba, DOWN, buff=0.7)
            subs = VGroup(*[Tx(t, color=DIM).scale(0.5) for t in ("1st axis", "2nd axis", "3rd axis")])
            for s_, i in zip(subs, (0, 2, 4)):
                s_.next_to(count[i], DOWN, buff=0.25)
            self.play(Write(count[0]), FadeIn(subs[0]))
            self.wait(0.8)
            self.play(Write(count[1:3]), FadeIn(subs[1]))
            self.wait(0.8)
            self.play(Write(count[3:]), FadeIn(subs[2]))
            sets = ["1-2-1", "1-2-3", "1-3-1", "1-3-2", "2-1-2", "2-1-3",
                    "2-3-1", "2-3-2", "3-1-2", "3-1-3", "3-2-1", "3-2-3"]
            grid = VGroup(*[Tx(x).scale(0.7) for x in sets]).arrange_in_grid(2, 6, buff=(0.6, 0.35))
            grid.next_to(count, DOWN, buff=1.0)
            grid[sets.index("3-2-1")].set_color(YELLOW)
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.1), run_time=min(2.0, self.left()))
            self.hold()

        with self.voice("euler_7"):
            self.play(FadeOut(VGroup(count, subs, grid)))
            full = T(r"C_{\mathcal{BA}} = \begin{bmatrix}"
                     r"c\theta\, c\psi & c\theta\, s\psi & -s\theta\\"
                     r"s\phi\, s\theta\, c\psi - c\phi\, s\psi & s\phi\, s\theta\, s\psi + c\phi\, c\psi & s\phi\, c\theta\\"
                     r"c\phi\, s\theta\, c\psi + s\phi\, s\psi & c\phi\, s\theta\, s\psi - s\phi\, c\psi & c\phi\, c\theta"
                     r"\end{bmatrix}").scale(0.72).next_to(cba, DOWN, buff=0.6)
            inv = VGroup(
                T(r"\theta = -\sin^{-1}(C_{13})", color=Q_COL),
                T(r"\psi = \operatorname{atan2}(C_{12},\, C_{11})", color=P_COL),
                T(r"\phi = \operatorname{atan2}(C_{23},\, C_{33})", color=B_COL),
            ).scale(0.75).arrange(RIGHT, buff=0.7).next_to(full, DOWN, buff=0.7)
            self.play(FadeOut(cba), Write(full), run_time=2.0)
            hl = SurroundingRectangle(pick_glyphs(full, 0.86, 0.97, 0.66, 1.0), color=YELLOW, buff=0.08)
            self.play(Create(hl))
            self.play(Write(inv[0]))
            self.play(Write(inv[1]), Write(inv[2]), run_time=min(2.0, self.left()))
            self.hold()

        # ---- gimbal lock
        with self.voice("euler_8"):
            gone = flat(ghostP, ghostQ, plabs, qlabs, blabs, lab_psi, lab_th, lab_ph, arc_psi, arc_th, arc_ph)
            self.play(FadeOut(VGroup(full, inv, hl, ov, eqs, seq)), *hide(*gone), run_time=0.8)
            self.remove(*gone)
            self.play(psi.animate.set_value(np.radians(30)), th.animate.set_value(0),
                      ph.animate.set_value(np.radians(20)), run_time=1.0)
            yaw_axis = D.line([0, 0, -3], [0, 0, 3], P_COL, 3, op=0)
            roll_axis = D.line(lambda: -3 * M()[0], lambda: 3 * M()[0], B_COL, 3, op=0)
            self.add(yaw_axis, roll_axis)
            ylab = Tx("yaw axis ($\\hat a_3$)", color=P_COL).scale(0.65)
            rlab = Tx("roll axis ($\\hat b_1$)", color=B_COL).scale(0.65)
            labs = VGroup(ylab, rlab).arrange(DOWN, aligned_edge=LEFT).next_to(hdr, DOWN, buff=0.5)
            labs.shift(RIGHT * (2.6 - labs.get_left()[0]))
            self.play(*show(yaw_axis, roll_axis), FadeIn(labs))
            thl = always_redraw(lambda: T(r"\theta = %d^\circ" % round(np.degrees(th.get_value())),
                                          color=Q_COL).scale(1.0).next_to(labs, DOWN, buff=0.5).align_to(labs, LEFT))
            self.add(thl)
            self.play(th.animate.set_value(np.radians(90)), run_time=4.0, rate_func=smooth)
            lock = Tx(r"gimbal lock", color=YELLOW).scale(1.0).next_to(thl, DOWN, buff=0.35).align_to(labs, LEFT)
            self.play(Write(lock))
            a1 = T(r"\psi \mathrel{+}= 40^\circ", color=P_COL).scale(0.8).next_to(lock, DOWN, buff=0.4).align_to(labs, LEFT)
            self.play(FadeIn(a1), psi.animate.increment_value(np.radians(40)), run_time=2.0)
            a2 = T(r"\phi \mathrel{+}= 40^\circ", color=B_COL).scale(0.8).next_to(a1, DOWN).align_to(labs, LEFT)
            self.play(FadeIn(a2), ph.animate.increment_value(np.radians(40)), run_time=2.0)
            only = T(r"\text{only } \phi-\psi \text{ matters}", color=YELLOW).scale(0.8).next_to(a2, DOWN, buff=0.4).align_to(labs, LEFT)
            self.play(Write(only), run_time=min(1.2, self.left()))
            self.hold()

        with self.voice("euler_9"):
            thl.clear_updaters()
            ov2 = overlay()
            self.play(FadeIn(ov2), FadeOut(VGroup(lock, a1, a2, only, labs, thl, hdr)), run_time=0.6)
            t1 = Tx(r"Every Euler angle set has a singularity").scale(0.9).to_edge(UP, buff=1.0)
            asym = VGroup(Tx(r"Asymmetric", color=B_COL), Tx(r"3-2-1, 1-2-3, 2-1-3, \dots", color=DIM).scale(0.8),
                          T(r"\theta_2 = \pm 90^\circ")).arrange(DOWN, buff=0.3)
            sym = VGroup(Tx(r"Symmetric", color=Q_COL), Tx(r"3-1-3, 1-2-1, 2-3-2, \dots", color=DIM).scale(0.8),
                         T(r"\theta_2 = 0^\circ,\ 180^\circ")).arrange(DOWN, buff=0.3)
            VGroup(asym, sym).arrange(RIGHT, buff=2.0).next_to(t1, DOWN, buff=1.0)
            tip = Tx(r"Pick the set whose singularity is far from your motion", color=YELLOW).scale(0.75)
            tip.to_edge(DOWN, buff=1.0)
            self.play(Write(t1))
            self.play(FadeIn(asym, shift=UP * 0.2))
            self.wait(2.0)
            self.play(FadeIn(sym, shift=UP * 0.2))
            self.wait(2.0)
            self.play(Write(tip), run_time=min(2.0, self.left()))
            self.hold()
        for m in self.mobjects:
            m.clear_updaters()
        self.play(FadeOut(Group(*self.mobjects)))


# ======================================================== Angular velocity
class AngularVelocity(Scene2D):
    def construct(self):
        cam = Cam(phi=70, theta=28, scale=1.15, center=(-2.4, -1.0))
        D = Draw(cam)
        self.add(*cam.trackers())
        L = 2.3
        ang = ValueTracker(0)
        rate = ValueTracker(0)
        ang.add_updater(lambda m, dt: m.increment_value(rate.get_value() * dt))
        self.add(ang, rate)

        N, nlabs = D.frame(np.eye(3), N_COL, L, [r"\hat n_1", r"\hat n_2", r"\hat n_3"])
        Bf, blabs = D.frame(lambda: C3(ang.get_value()), B_COL, L, [r"\hat b_1", r"\hat b_2", None], width=6)
        Bf.remove(Bf[2])
        hdr = Tx("Angular velocity", color=B_COL).scale(0.9).to_corner(UR)

        with self.voice("omega_1"):
            self.add(N, nlabs, Bf, blabs)
            self.play(Write(hdr))
            self.play(*grow(*N), *show(*nlabs))
            self.play(*grow(*Bf), *show(*blabs))
            self.play(rate.animate.set_value(0.6), run_time=1.5)
            self.hold()

        w_arrow = D.arrow(ORIGIN, lambda: [0, 0, 0.6 + 1.6 * rate.get_value()], W_COL, width=8, k=0)
        wl = D.label(r"\vec\omega^{\mathcal B/\mathcal N}", lambda: [0.0, 0.0, 1.0 + 1.6 * rate.get_value()], W_COL, 0.8)
        wl.add_updater(lambda m: m.shift(LEFT * 0.7))
        with self.voice("omega_2"):
            self.add(w_arrow, wl)
            self.play(*grow(w_arrow), *show(wl), *hide(nlabs[2]))
            e1 = T(r"\vec\omega^{\mathcal B/\mathcal N} = \dot\theta\,\hat n_3 = \dot\theta\,\hat b_3").scale(0.85)
            e1.next_to(hdr, DOWN, buff=0.6).to_edge(RIGHT)
            self.play(Write(e1))
            self.wait(1.0)
            e2 = VGroup(Tx("direction: the spin axis (right-hand rule)", color=DIM),
                        Tx("length: the spin rate", color=DIM)).arrange(DOWN, aligned_edge=LEFT)
            e2.scale(0.6).next_to(e1, DOWN, buff=0.4).to_edge(RIGHT)
            self.play(FadeIn(e2[0]))
            self.play(rate.animate.set_value(1.5), FadeIn(e2[1]), run_time=2.5)
            self.play(rate.animate.set_value(0.7), run_time=max(1.0, self.left() - 0.2))

        # ---- tip of a tilted basis vector sweeping a cone
        phi0 = np.radians(50)
        Lb = 2.4

        def bt():
            a = ang.get_value()
            return Lb * np.array([np.sin(phi0) * np.cos(a), np.sin(phi0) * np.sin(a), np.cos(phi0)])

        h = Lb * np.cos(phi0)
        with self.voice("omega_3"):
            self.play(*hide(*Bf, *blabs), FadeOut(e2), run_time=0.6)
            self.remove(*Bf, *blabs)
            bvec = D.arrow(ORIGIN, bt, B_COL, width=6, k=0)
            blab = D.label(r"\hat b_i", lambda: bt() * 1.13, B_COL, 0.85)
            circ = D.curve(lambda t: [Lb * np.sin(phi0) * np.cos(t), Lb * np.sin(phi0) * np.sin(t), h],
                           (0, TAU), B_COL, 2, n=90, k=0)
            circ.op.set_value(0.6)
            rad = D.line([0, 0, h], bt, YELLOW, 3, dashed=True, op=0)
            radl = D.label(r"\rho = \sin\phi", lambda: (np.array([0, 0, h]) + bt()) / 2 + np.array([0, 0, 0.35]), YELLOW, 0.65)
            phiarc = D.curve(lambda t: 0.95 * np.array([np.sin(t) * np.cos(ang.get_value()),
                                                        np.sin(t) * np.sin(ang.get_value()), np.cos(t)]),
                             (0, phi0), V_COL, 3, n=20, op=0)
            phil = D.label(r"\phi", lambda: 1.25 * np.array([np.sin(phi0 / 2) * np.cos(ang.get_value()),
                                                              np.sin(phi0 / 2) * np.sin(ang.get_value()),
                                                              np.cos(phi0 / 2)]), V_COL, 0.75)
            self.add(circ, bvec, blab, rad, radl, phiarc, phil)
            self.play(*grow(bvec), *show(blab))
            self.play(*grow(circ), run_time=1.5)
            self.play(*show(rad, radl, phiarc, phil))
            e3 = T(r"\left|{}^{\mathcal N}\tfrac{d}{dt}\hat b_i\right| = \rho\,|\vec\omega| = \sin\phi\,|\vec\omega|").scale(0.8)
            e3.next_to(e1, DOWN, buff=0.6).to_edge(RIGHT)
            self.wait(2.0)
            self.play(Write(e3), run_time=2.0)
            self.hold()

        with self.voice("omega_4"):
            vel = D.arrow(bt, lambda: bt() + 0.8 * np.cross([0, 0, 1.0], bt()), V_COL, width=6, k=0)
            self.add(vel)
            self.play(*grow(vel))
            perp = Tx(r"$\perp$ to both $\hat b_i$ and $\vec\omega$", color=V_COL).scale(0.7)
            perp.next_to(e3, DOWN, buff=0.4).to_edge(RIGHT)
            self.play(FadeIn(perp))
            self.wait(3.0)
            boxed = T(r"{}^{\mathcal N}\frac{d}{dt}\hat b_i = \vec\omega^{\mathcal B/\mathcal N}\times\hat b_i").scale(0.95)
            boxed = VGroup(boxed, SurroundingRectangle(boxed, color=YELLOW, buff=0.15)).next_to(perp, DOWN, buff=0.5).to_edge(RIGHT)
            self.play(Write(boxed), run_time=2.0)
            self.hold()

        # ---- adding angular velocities through the 3-2-1 chain
        psi, th, ph = np.radians(35), np.radians(30), np.radians(25)
        Pm = C3(psi)
        Qm = C2(th) @ Pm
        Bm = C1(ph) @ Qm
        with self.voice("omega_5"):
            gone = flat(bvec, blab, circ, rad, radl, phiarc, phil, vel, w_arrow, wl)
            self.play(*hide(*gone), FadeOut(VGroup(e1, e3, perp, boxed)), run_time=0.8)
            self.remove(*gone)
            rate.set_value(0)
            cam.start_spin(self, 0.1)
            ax_p3 = D.arrow(ORIGIN, 2.4 * Pm[2], P_COL, width=7, k=0)
            ax_q2 = D.arrow(ORIGIN, 2.4 * Qm[1], Q_COL, width=7, k=0)
            ax_b1 = D.arrow(ORIGIN, 2.4 * Bm[0], B_COL, width=7, k=0)
            l1 = D.label(r"\dot\psi\,\hat p_3", 2.8 * Pm[2] + np.array([0.3, 0, 0]), P_COL, 0.8)
            l2 = D.label(r"\dot\theta\,\hat q_2", 2.85 * Qm[1], Q_COL, 0.8)
            l3 = D.label(r"\dot\phi\,\hat b_1", 2.85 * Bm[0], B_COL, 0.8)
            self.add(ax_p3, ax_q2, ax_b1, l1, l2, l3)
            sumeq = T(r"\vec\omega^{\mathcal B/\mathcal A} = \vec\omega^{\mathcal B/\mathcal Q} + \vec\omega^{\mathcal Q/\mathcal P}"
                      r" + \vec\omega^{\mathcal P/\mathcal A}").scale(0.72)
            sumeq2 = T(r"=", r"\dot\psi\,\hat p_3", r"+", r"\dot\theta\,\hat q_2", r"+", r"\dot\phi\,\hat b_1").scale(0.85)
            sumeq2[1].set_color(P_COL)
            sumeq2[3].set_color(Q_COL)
            sumeq2[5].set_color(B_COL)
            VGroup(sumeq, sumeq2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(hdr, DOWN, buff=0.6).to_edge(RIGHT)
            self.play(Write(sumeq), run_time=2.0)
            self.wait(1.0)
            self.play(*grow(ax_p3), *show(l1), Write(sumeq2[:2]))
            self.play(*grow(ax_q2), *show(l2), Write(sumeq2[2:4]))
            self.play(*grow(ax_b1), *show(l3), Write(sumeq2[4:]), run_time=min(1.0, self.left()))
            self.hold()

        with self.voice("omega_6"):
            warn = Tx(r"these axes are \emph{not} perpendicular!", color=YELLOW).scale(0.7)
            warn.next_to(sumeq2, DOWN, buff=0.4).to_edge(RIGHT)
            self.play(Write(warn))
            wb = T(r"\omega_{(\mathcal B)} = \begin{bmatrix}\dot\phi - \dot\psi\sin\theta\\"
                   r"\dot\theta\cos\phi + \dot\psi\cos\theta\sin\phi\\"
                   r"-\dot\theta\sin\phi + \dot\psi\cos\theta\cos\phi\end{bmatrix}").scale(0.72)
            wb.next_to(warn, DOWN, buff=0.5).to_edge(RIGHT)
            self.wait(1.0)
            self.play(Write(wb), run_time=min(3.0, self.left()))
            self.hold()

        with self.voice("omega_7"):
            cam.stop_spin()
            ov = overlay()
            self.play(FadeIn(ov), FadeOut(VGroup(sumeq, sumeq2, warn, wb, hdr)), run_time=0.6)
            gyro = Tx(r"a gyro measures $\omega_{(\mathcal B)}$ \ $\Longrightarrow$ \ how do the angles evolve?", color=DIM)
            gyro.scale(0.7).to_edge(UP, buff=0.5)
            kde = T(r"\begin{bmatrix}\dot\psi\\\dot\theta\\\dot\phi\end{bmatrix} = ", r"\frac{1}{\cos\theta}",
                    r"\begin{bmatrix}0&\sin\phi&\cos\phi\\0&\cos\phi\cos\theta&-\sin\phi\cos\theta\\"
                    r"\cos\theta&\sin\phi\sin\theta&\cos\phi\sin\theta\end{bmatrix}",
                    r"\begin{bmatrix}\omega_1\\\omega_2\\\omega_3\end{bmatrix}").scale(0.75)
            kde.next_to(gyro, DOWN, buff=0.5)
            self.play(FadeIn(gyro))
            self.play(Write(kde), run_time=2.5)
            self.wait(1.0)
            hl = SurroundingRectangle(kde[1], color=P_COL, buff=0.08)
            self.play(Create(hl), kde[1].animate.set_color(P_COL))
            ax = Axes(x_range=[0, 90, 15], y_range=[0, 12, 4], x_length=6, y_length=2.6,
                      axis_config={"color": DIM, "include_tip": False},
                      x_axis_config={"numbers_to_include": [0, 30, 60, 90]}).next_to(kde, DOWN, buff=0.6)
            xl = T(r"\theta\ (\text{deg})", color=DIM).scale(0.6).next_to(ax.x_axis, RIGHT, buff=0.15)
            yl = T(r"1/\cos\theta", color=P_COL).scale(0.6).next_to(ax.y_axis, UP, buff=0.1)
            curve = ax.plot(lambda x: 1 / np.cos(np.radians(x)), x_range=[0, 85.2], color=P_COL)
            asym = DashedLine(ax.c2p(90, 0), ax.c2p(90, 12), color=YELLOW)
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(curve), run_time=2.0)
            self.play(Create(asym), run_time=min(1.0, self.left()))
            self.hold()
        for m in self.mobjects:
            m.clear_updaters()
        self.play(FadeOut(Group(*self.mobjects)))
