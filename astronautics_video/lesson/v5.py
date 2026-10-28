"""Lesson 5: The transport theorem."""
from lcommon import *  # noqa: F401,F403
from scenes_c import SpinningDisk, make_disk, vec, rot2  # noqa: E402

THEOREM = r"{}^{\mathcal N}\frac{d}{dt}\vec r = {}^{\mathcal B}\frac{d}{dt}\vec r + \vec\omega^{\mathcal B/\mathcal N}\times\vec r"


class V5Concept(Lesson):
    def construct(self):
        with self.voice("v5_01"):
            card = title_card(self, 5, "The Transport Theorem", "taking derivatives in a rotating frame")
            self.hold()
        self.play(FadeOut(card))

        ang = ValueTracker(0)
        w = 0.6
        self.add(ang)
        LC, RC = np.array([-3.5, -1.2, 0]), np.array([3.5, -1.2, 0])
        pb = np.array([1.3, 0.5, 0])
        with self.voice("v5_02"):
            hdr = header("A puzzle: is this vector changing?")
            self.play(FadeIn(hdr))
            ld = make_disk().move_to(LC)
            rd = SpinningDisk(RC, ang)
            lt = Tx("Riding on the disk", color=B_COL).scale(0.7).next_to(ld, UP, buff=0.25)
            rt = Tx("Standing on the ground", color=N_COL).scale(0.7).next_to(rd, UP, buff=0.25)
            lv = Arrow(LC, LC + pb, buff=0, color=R_COL, stroke_width=6)
            rv = always_redraw(lambda: vec(RC, rd.to_world(pb), R_COL, 6))
            self.play(FadeIn(ld), FadeIn(rd), FadeIn(lt), FadeIn(rt), GrowArrow(lv))
            self.add(rv)
            ang.add_updater(lambda m, dt: m.increment_value(w * dt))
            self.wait(2.0)
            l0 = T(r"\frac{d\vec r}{dt} = 0", color=B_COL).scale(0.8).next_to(ld, DOWN, buff=0.3)
            r0 = T(r"\frac{d\vec r}{dt} \neq 0", color=N_COL).scale(0.8).next_to(rd, DOWN, buff=0.3)
            self.play(Write(l0))
            self.wait(1.5)
            self.play(Write(r0))
            self.hold()

        with self.voice("v5_03"):
            both = Tx("Both are right!", color=YELLOW).scale(0.8).move_to(UP * 2.4)
            self.play(Write(both))
            nl0 = T(r"{}^{\mathcal B}\frac{d\vec r}{dt} = 0", color=B_COL).scale(0.8).move_to(l0)
            nr0 = T(r"{}^{\mathcal N}\frac{d\vec r}{dt} \neq 0", color=N_COL).scale(0.8).move_to(r0)
            self.play(Transform(l0, nl0), Transform(r0, nr0))
            key = Tx(r"the small letter says \emph{which frame} is watching", color=REASON).scale(0.6).next_to(both, DOWN, buff=0.25)
            self.play(FadeIn(key))
            self.hold()
        ang.clear_updaters()
        rv.clear_updaters()
        rd.clear_updaters()
        self.play(FadeOut(VGroup(ld, rd, lt, rt, lv, rv, l0, r0, both, key)))

        # ---- derivation
        with self.voice("v5_04"):
            self.play(Transform(hdr, header("Deriving the rule, one step at a time")))
            bd = Board(self, left=-6.3, top=2.4, scale=0.8, buff=0.4)
            bd.line(r"\vec r = r_1\,\hat b_1 + r_2\,\hat b_2 + r_3\,\hat b_3", reason="write $\\vec r$ in $\\mathcal B$ components")
            self.hold()

        with self.voice("v5_05"):
            bd.line(r"{}^{\mathcal B}\frac{d}{dt}\vec r = \dot r_1\,\hat b_1 + \dot r_2\,\hat b_2 + \dot r_3\,\hat b_3", color=B_COL,
                    reason="in $\\mathcal B$, the $\\hat b_i$ are fixed: only components change")
            self.hold()

        with self.voice("v5_06"):
            bd.line(r"{}^{\mathcal N}\frac{d}{dt}\vec r = \sum_i \Big(\dot r_i\,\hat b_i + r_i\,{}^{\mathcal N}\frac{d}{dt}\hat b_i\Big)",
                    reason="product rule on each (number $\\times$ vector)")
            self.hold()

        with self.voice("v5_07"):
            l = bd.line(r"= \underbrace{\sum_i \dot r_i\,\hat b_i}_{{}^{\mathcal B}\frac{d}{dt}\vec r} + \sum_i r_i\,{}^{\mathcal N}\frac{d}{dt}\hat b_i",
                        indent=1.6, reason="group the terms")
            self.hold()

        with self.voice("v5_08"):
            bd.line(r"= {}^{\mathcal B}\frac{d}{dt}\vec r + r_1(\vec\omega\times\hat b_1) + r_2(\vec\omega\times\hat b_2) + r_3(\vec\omega\times\hat b_3)",
                    indent=1.6, reason=r"Lesson 4: ${}^{\mathcal N}\tfrac{d}{dt}\hat b_i = \vec\omega\times\hat b_i$", below=True)
            self.hold()

        with self.voice("v5_09"):
            bd.line(r"= {}^{\mathcal B}\frac{d}{dt}\vec r + \vec\omega\times\underbrace{(r_1\hat b_1 + r_2\hat b_2 + r_3\hat b_3)}_{\vec r}",
                    indent=1.6, reason="cross product is linear: pull $\\vec\\omega$ out")
            self.hold()

        with self.voice("v5_10"):
            bd.clear()
            thm = T(THEOREM).scale(1.2)
            box = SurroundingRectangle(thm, color=YELLOW, buff=0.25)
            name = Tx("The transport theorem", color=YELLOW).scale(0.85).next_to(box, UP, buff=0.3)
            self.play(Write(thm), run_time=2.5)
            self.play(Create(box), FadeIn(name))
            self.hold()

        with self.voice("v5_11"):
            parts = VGroup(Tx(r"rate of change\\seen by $\mathcal N$", color=N_COL), Tx(r"rate of change\\seen by $\mathcal B$", color=B_COL),
                           Tx(r"$\mathcal B$ itself turning\\(transport term)", color=W_COL)).scale(0.6)
            xs = [thm.get_left()[0] + thm.width * 0.12, thm.get_left()[0] + thm.width * 0.47, thm.get_left()[0] + thm.width * 0.82]
            for p, x in zip(parts, xs):
                p.move_to([x, box.get_bottom()[1] - 0.7, 0])
                self.play(FadeIn(p, shift=UP * 0.2), run_time=0.8)
                self.wait(1.2)
            self.hold()
        self.play(FadeOut(VGroup(parts, name)), VGroup(thm, box).animate.scale(0.7).to_edge(UP, buff=0.25), FadeOut(hdr))

        # ---- pictures
        ang.set_value(0)
        rho = ValueTracker(1.3)
        self.add(rho)
        u = np.array([np.cos(0.5), np.sin(0.5), 0])
        p_body = lambda: rho.get_value() * u
        with self.voice("v5_12"):
            ld = make_disk().move_to(LC)
            rd = SpinningDisk(RC, ang)
            lt = Tx("Observer in $\\mathcal B$", color=B_COL).scale(0.7).next_to(ld, UP, buff=0.25)
            rt = Tx("Observer in $\\mathcal N$", color=N_COL).scale(0.7).next_to(rd, UP, buff=0.25)
            self.play(FadeIn(ld), FadeIn(rd), FadeIn(lt), FadeIn(rt))
            lp = always_redraw(lambda: Dot(LC + p_body(), color=R_COL, radius=0.09))
            rp = always_redraw(lambda: Dot(rd.to_world(p_body()), color=R_COL, radius=0.09))
            rr = always_redraw(lambda: vec(RC, rd.to_world(p_body()), R_COL, 4))
            wxr = always_redraw(lambda: vec(rd.to_world(p_body()), rd.to_world(p_body()) + 0.9 * w * rot2(np.cross([0, 0, 1], p_body()), ang.get_value()), W_COL, 5))
            trail = TracedPath(lambda: rd.to_world(p_body()), stroke_color=R_COL, stroke_width=2, stroke_opacity=0.5)
            self.add(trail, lp, rp, rr)
            ang.add_updater(lambda m, dt: m.increment_value(w * dt))
            lt0 = T(r"{}^{\mathcal B}\dot{\vec r} = 0", color=B_COL).scale(0.8).next_to(ld, DOWN, buff=0.3)
            rt0 = T(r"{}^{\mathcal N}\dot{\vec r} = 0 + \vec\omega\times\vec r", color=W_COL).scale(0.8).next_to(rd, DOWN, buff=0.3)
            self.wait(1.5)
            self.play(Write(lt0))
            self.add(wxr)
            self.play(FadeIn(wxr), Write(rt0))
            self.hold()

        with self.voice("v5_13"):
            self.play(FadeOut(lt0), FadeOut(rt0), run_time=0.5)
            rdot = 0.13
            rho.add_updater(lambda m, dt: m.set_value(min(1.85, m.get_value() + rdot * dt)))
            self.play(rho.animate.set_value(0.45), run_time=0.8)
            lv = always_redraw(lambda: vec(LC + p_body(), LC + p_body() + 3.5 * rdot * u, Q_COL, 5))
            rv2 = always_redraw(lambda: vec(rd.to_world(p_body()), rd.to_world(p_body()) + 3.5 * rdot * rot2(u, ang.get_value()), Q_COL, 5))
            tot = always_redraw(lambda: vec(rd.to_world(p_body()), rd.to_world(p_body()) + 3.5 * rdot * rot2(u, ang.get_value())
                                            + 0.9 * w * rot2(np.cross([0, 0, 1], p_body()), ang.get_value()), WHITE, 5))
            self.add(lv, rv2, tot)
            leq = T(r"{}^{\mathcal B}\dot{\vec r}\ \text{(sliding)}", color=Q_COL).scale(0.75).next_to(ld, DOWN, buff=0.3)
            req = T(r"{}^{\mathcal N}\dot{\vec r}", "=", r"{}^{\mathcal B}\dot{\vec r}", "+", r"\vec\omega\times\vec r").scale(0.8)
            req[2].set_color(Q_COL)
            req[4].set_color(W_COL)
            req.next_to(rd, DOWN, buff=0.3)
            self.play(FadeIn(lv), FadeIn(rv2), FadeIn(tot), Write(leq), Write(req), run_time=1.5)
            self.hold()
        for m_ in (lp, rp, rr, wxr, lv, rv2, tot, trail, rd, rho, ang):
            m_.clear_updaters()
        self.play(FadeOut(VGroup(ld, rd, lt, rt, lp, rp, rr, wxr, lv, rv2, tot, trail, leq, req)))

        with self.voice("v5_14"):
            h = Tx("A recipe that always works", color=YELLOW).scale(0.85).next_to(VGroup(thm, box), DOWN, buff=0.5)
            steps = VGroup(*[Tx(t).scale(0.7) for t in (
                r"1.\ Pick a frame where the vector is simple.",
                r"2.\ Write the vector in that frame's components.",
                r"3.\ Differentiate the components (the easy derivative).",
                r"4.\ Add $\vec\omega\times$ (the vector).",
                r"5.\ If needed, convert to another frame with a DCM.")]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
            steps.next_to(h, DOWN, buff=0.4)
            self.play(Write(h))
            for st in steps:
                self.play(FadeIn(st, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.3, (self.left() - 1.0) / 5 - 0.6))
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))


class V5Examples(Lesson):
    def construct(self):
        ang = ValueTracker(0)
        self.add(ang)
        C = np.array([-4.3, -0.9, 0])
        disk = SpinningDisk(C, ang, radius=1.9)
        pb = np.array([1.4, 0, 0])
        with self.voice("v5_15"):
            hdr = header("Example 1: a point on a spinning disk")
            self.play(FadeIn(hdr))
            self.play(FadeIn(disk))
            pt = always_redraw(lambda: Dot(disk.to_world(pb), color=R_COL, radius=0.1))
            self.add(pt)
            ang.add_updater(lambda m, dt: m.increment_value(0.4 * dt))
            bd = Board(self, left=-1.4, top=2.3, scale=0.8, buff=0.42)
            bd.line(r"\vec\omega = \omega\,\hat b_3\ (\text{const}),\qquad \vec r = R\,\hat b_1\ (R\ \text{const})", reason="step 1, 2")
            self.hold()

        with self.voice("v5_16"):
            bd.line(r"{}^{\mathcal B}\frac{d}{dt}\vec r = \dot R\,\hat b_1 = 0", reason="step 3: $R$ constant, $\\hat b_1$ fixed in $\\mathcal B$")
            self.hold()

        with self.voice("v5_17"):
            bd.line(r"\vec\omega\times\vec r = \omega\,\hat b_3\times R\,\hat b_1 = \omega R\,(\hat b_3\times\hat b_1)", reason="step 4")
            l = bd.line(r"{}^{\mathcal N}\vec v = \omega R\,\hat b_2", color=YELLOW, indent=1.2, reason="$\\hat b_3\\times\\hat b_1 = \\hat b_2$")
            bd.box(l)
            va = always_redraw(lambda: vec(disk.to_world(pb), disk.to_world(pb) + rot2(UP * 1.1, ang.get_value()), W_COL, 6))
            self.add(va)
            self.play(FadeIn(va))
            tan = Tx("tangent to the circle, size $\\omega R$", color=W_COL).scale(0.6).next_to(disk, DOWN, buff=0.25)
            self.play(FadeIn(tan))
            self.hold()
        for m_ in (pt, va, disk, ang):
            m_.clear_updaters()
        bd.clear()
        self.play(FadeOut(VGroup(disk, pt, va, tan)))

        # ---- telescoping arm
        ang.set_value(0)
        Lt = ValueTracker(0.8)
        self.add(Lt)
        C2_ = np.array([-4.3, -0.6, 0])

        def b1w():
            return np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0])
        body = always_redraw(lambda: Square(1.0, color=GREY_B, fill_color="#1B2233", fill_opacity=1).rotate(ang.get_value()).move_to(C2_))
        arm = always_redraw(lambda: Line(C2_, C2_ + Lt.get_value() * b1w(), color=GREY_A, stroke_width=8))
        mass = always_redraw(lambda: Square(0.22, color=YELLOW, fill_color=YELLOW, fill_opacity=1).rotate(ang.get_value()).move_to(C2_ + Lt.get_value() * b1w()))
        bax = always_redraw(lambda: VGroup(Arrow(C2_, C2_ + 0.9 * b1w(), buff=0, color=B_COL, stroke_width=4),
                                           Arrow(C2_, C2_ + 0.9 * rot2(UP, ang.get_value()), buff=0, color=B_COL, stroke_width=4)))
        with self.voice("v5_18"):
            self.play(Transform(hdr, header("Example 2: a telescoping arm on a spinning satellite")))
            self.add(body, arm, mass, bax)
            ang.add_updater(lambda m, dt: m.increment_value(0.35 * dt))
            Lt.add_updater(lambda m, dt: m.set_value(min(2.6, m.get_value() + 0.12 * dt)))
            given = VGroup(T(r"\vec\omega = \omega\,\hat b_3\ (\text{const})"), T(r"L(t) = L_0 + c\,t")).scale(0.75).arrange(DOWN, aligned_edge=LEFT)
            given.move_to(RIGHT * 2.0 + UP * 2.2)
            self.play(Write(given), run_time=2.0)
            self.hold()

        with self.voice("v5_19"):
            bd = Board(self, left=-1.4, top=1.2, scale=0.75, buff=0.36, ceiling=given.get_bottom()[1] - 0.1)
            bd.line(r"\vec r = L\,\hat b_1", reason="simple in $\\mathcal B$")
            bd.line(r"{}^{\mathcal B}\frac{d}{dt}\vec r = \dot L\,\hat b_1 = c\,\hat b_1", reason="only the length changes")
            self.hold()

        with self.voice("v5_20"):
            bd.line(r"\vec\omega\times\vec r = \omega\,\hat b_3\times L\,\hat b_1 = \omega L\,\hat b_2")
            l = bd.line(r"{}^{\mathcal N}\vec v = c\,\hat b_1 + \omega\,(L_0 + c\,t)\,\hat b_2", color=YELLOW)
            bd.box(l)
            self.hold()

        with self.voice("v5_21"):
            bd.line(r"\hat b_1 = \cos\omega t\,\hat n_1 + \sin\omega t\,\hat n_2,\quad \hat b_2 = -\sin\omega t\,\hat n_1 + \cos\omega t\,\hat n_2",
                    reason="rows of $C_3(\\omega t)$ (B started aligned with N)", below=True)
            self.hold()

        with self.voice("v5_22"):
            bd.line(r"v_1 = c\cos\omega t - \omega L\sin\omega t,\qquad v_2 = c\sin\omega t + \omega L\cos\omega t", color=YELLOW,
                    reason="substitute and collect $\\hat n_1$, $\\hat n_2$", below=True)
            self.hold()
        for m_ in (body, arm, mass, bax, ang, Lt):
            m_.clear_updaters()
        bd.clear()
        self.play(FadeOut(VGroup(body, arm, mass, bax, given)))

        with self.voice("v5_23"):
            self.play(Transform(hdr, header("Check it the hard way (directly in $\\mathcal N$)")))
            bd = Board(self, left=-6.0, top=2.3, scale=0.8, buff=0.42)
            bd.line(r"\vec r = L\cos\omega t\,\hat n_1 + L\sin\omega t\,\hat n_2", reason="$\\vec r = L\\,\\hat b_1$ written in $\\mathcal N$")
            bd.line(r"\frac{d}{dt}(L\cos\omega t) = \dot L\cos\omega t - L\,\omega\sin\omega t", reason="product rule + chain rule")
            bd.line(r"\frac{d}{dt}(L\sin\omega t) = \dot L\sin\omega t + L\,\omega\cos\omega t")
            ok = bd.line(r"\text{with } \dot L = c:\ \text{same as before}\ \checkmark", color=Q_COL)
            note = Tx("the transport theorem got there with much less work", color=REASON).scale(0.6).next_to(ok, RIGHT, buff=0.5)
            self.play(FadeIn(note))
            self.hold()
        bd.clear()
        self.play(FadeOut(note))

        with self.voice("v5_24"):
            self.play(Transform(hdr, header("Example 3: cylindrical coordinates")))
            O = np.array([-4.8, -1.7, 0])
            th0 = 0.6
            n1 = Arrow(O, O + RIGHT * 2.2, buff=0, color=N_COL, stroke_width=3)
            e1 = Arrow(O, O + 2.2 * np.array([np.cos(th0), np.sin(th0), 0]), buff=0, color=B_COL, stroke_width=4)
            e2 = Arrow(O, O + 1.4 * np.array([-np.sin(th0), np.cos(th0), 0]), buff=0, color=B_COL, stroke_width=4)
            labs = VGroup(T(r"\hat n_1", color=N_COL).scale(0.6).next_to(n1.get_end(), RIGHT, buff=0.05),
                          T(r"\hat e_1", color=B_COL).scale(0.6).next_to(e1.get_end(), UR, buff=0.05),
                          T(r"\hat e_2", color=B_COL).scale(0.6).next_to(e2.get_end(), UP, buff=0.05))
            pt = Dot(O + 1.6 * np.array([np.cos(th0), np.sin(th0), 0]), color=R_COL)
            arc = Arc(radius=0.6, angle=th0, arc_center=O, color=YELLOW)
            thl = T(r"\theta", color=YELLOW).scale(0.6).move_to(O + 0.85 * np.array([np.cos(th0 / 2), np.sin(th0 / 2), 0]))
            diag = VGroup(n1, e1, e2, labs, pt, arc, thl)
            self.play(FadeIn(diag))
            bd = Board(self, left=-2.0, top=2.3, scale=0.8, buff=0.42)
            bd.line(r"\vec r = R\,\hat e_1 + z\,\hat e_3,\qquad \vec\omega^{\mathcal E/\mathcal N} = \dot\theta\,\hat e_3")
            self.hold()

        with self.voice("v5_25"):
            bd.line(r"{}^{\mathcal E}\frac{d}{dt}\vec r = \dot R\,\hat e_1 + \dot z\,\hat e_3")
            bd.line(r"\vec\omega\times\vec r = \dot\theta\,\hat e_3\times(R\,\hat e_1 + z\,\hat e_3) = R\dot\theta\,\hat e_2",
                    reason="$\\hat e_3\\times\\hat e_1 = \\hat e_2$, \\ $\\hat e_3\\times\\hat e_3 = 0$", below=True)
            self.hold()

        with self.voice("v5_26"):
            l = bd.line(r"{}^{\mathcal N}\vec v = \dot R\,\hat e_1 + R\dot\theta\,\hat e_2 + \dot z\,\hat e_3", color=YELLOW)
            bd.box(l)
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("v5_27"):
            h, rows = recap(self, [
                r"A derivative of a vector depends on the observer (frame).",
                r"Transport theorem: ${}^{\mathcal N}\tfrac{d}{dt}\vec r = {}^{\mathcal B}\tfrac{d}{dt}\vec r + \vec\omega^{\mathcal B/\mathcal N}\times\vec r$.",
                r"Recipe: simple frame $\to$ components $\to$ easy derivative $\to$ add $\vec\omega\times\vec r$ $\to$ convert.",
            ])
            for rrow in rows:
                self.play(FadeIn(rrow, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 3 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
