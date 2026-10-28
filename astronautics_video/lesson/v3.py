"""Lesson 3: Euler angles."""
from lcommon import *  # noqa: F401,F403


def axis_view(O, L, th, right_lab, up_lab, out_lab, new_right, new_up):
    """2D view looking down a rotation axis: two axes turning by th."""
    def v(i):
        t = th.get_value()
        return [np.array([np.cos(t), np.sin(t), 0]), np.array([-np.sin(t), np.cos(t), 0])][i]
    a1 = Arrow(O, O + L * RIGHT, buff=0, color=N_COL, stroke_width=4)
    a2 = Arrow(O, O + L * UP, buff=0, color=N_COL, stroke_width=4)
    l1 = T(right_lab, color=N_COL).scale(0.7).next_to(a1.get_end(), RIGHT, buff=0.1)
    l2 = T(up_lab, color=N_COL).scale(0.7).next_to(a2.get_end(), UP, buff=0.1)
    dot = VGroup(Circle(radius=0.12, color=WHITE, stroke_width=2), Dot(radius=0.035)).move_to(O)
    ol = T(out_lab, color=DIM).scale(0.55).next_to(O, DL, buff=0.15)
    b1 = always_redraw(lambda: Arrow(O, O + L * v(0), buff=0, color=B_COL, stroke_width=5))
    b2 = always_redraw(lambda: Arrow(O, O + L * v(1), buff=0, color=B_COL, stroke_width=5))
    bl1 = always_redraw(lambda: T(new_right, color=B_COL).scale(0.7).move_to(O + (L + 0.35) * v(0)))
    bl2 = always_redraw(lambda: T(new_up, color=B_COL).scale(0.7).move_to(O + (L + 0.35) * v(1)))
    arc = always_redraw(lambda: Arc(radius=0.7, angle=th.get_value() + 1e-4, arc_center=O, color=YELLOW))
    return VGroup(a1, a2, l1, l2, dot, ol), VGroup(b1, b2, bl1, bl2, arc)


class V3Concept(Lesson):
    def construct(self):
        with self.voice("v3_01"):
            card = title_card(self, 3, "Euler Angles", "describing an orientation with three angles")
            self.hold()
        self.play(FadeOut(card))

        with self.voice("v3_02"):
            hdr = header("Building blocks: single-axis rotations")
            self.play(FadeIn(hdr))
            c3 = T(r"C_3(\theta) = \begin{bmatrix}\cos\theta & \sin\theta & 0\\-\sin\theta & \cos\theta & 0\\0&0&1\end{bmatrix}").scale(0.8)
            c3.move_to(UP * 1.2)
            got = Tx("found in Lesson 2", color=Q_COL).scale(0.6).next_to(c3, DOWN, buff=0.3)
            self.play(Write(c3), FadeIn(got))
            todo = T(r"C_1(\theta) = \ ?\qquad C_2(\theta) = \ ?", color=YELLOW).scale(0.85).next_to(got, DOWN, buff=0.7)
            self.play(Write(todo))
            self.hold()
        self.play(FadeOut(VGroup(c3, got, todo)))

        # ---- C1
        th = ValueTracker(0)
        self.add(th)
        O = np.array([-4.6, -1.3, 0])
        fixed, moving = axis_view(O, 2.3, th, r"\hat n_2", r"\hat n_3", r"\hat n_1 = \hat b_1\ \text{(out)}", r"\hat b_2", r"\hat b_3")
        with self.voice("v3_03"):
            self.play(Transform(hdr, header("Rotation about axis 1: looking down $\\hat n_1$")))
            self.play(FadeIn(fixed))
            self.add(moving)
            self.play(th.animate.set_value(np.radians(32)), run_time=2.0)
            bd = Board(self, left=-1.0, top=2.3, scale=0.8)
            bd.line(r"\hat b_1 = \hat n_1 \ \Rightarrow\ \text{row 1} = [\,1,\ 0,\ 0\,]", reason="axis 1 does not move")
            bd.line(r"\hat b_2 = \cos\theta\,\hat n_2 + \sin\theta\,\hat n_3", reason="same picture as $\\hat b_1$ in $C_3$")
            bd.line(r"\hat b_3 = -\sin\theta\,\hat n_2 + \cos\theta\,\hat n_3", reason="same picture as $\\hat b_2$ in $C_3$")
            l = bd.line(r"C_1(\theta) = \begin{bmatrix}1&0&0\\0&\cos\theta&\sin\theta\\0&-\sin\theta&\cos\theta\end{bmatrix}", color=YELLOW)
            bd.box(l)
            self.hold()
        for m in moving:
            m.clear_updaters()
        bd.clear()
        self.play(FadeOut(fixed), FadeOut(moving))

        # ---- C2
        th.set_value(0)
        fixed, moving = axis_view(O, 2.3, th, r"\hat n_3", r"\hat n_1", r"\hat n_2 = \hat b_2\ \text{(out)}", r"\hat b_3", r"\hat b_1")
        with self.voice("v3_04"):
            self.play(Transform(hdr, header("Rotation about axis 2: looking down $\\hat n_2$")))
            self.play(FadeIn(fixed))
            self.add(moving)
            self.play(th.animate.set_value(np.radians(32)), run_time=2.0)
            bd = Board(self, left=-1.0, top=2.3, scale=0.8)
            bd.line(r"\hat b_2 = \hat n_2 \ \Rightarrow\ \text{row 2} = [\,0,\ 1,\ 0\,]", reason="axis 2 does not move")
            note = Tx(r"counterclockwise order seen from $+\hat n_2$:\\ $\hat n_3$ first, then $\hat n_1$ \ (because $\hat n_3\times\hat n_1 = \hat n_2$)",
                      color=YELLOW).scale(0.6)
            bd.line(mob=note)
            self.hold()

        with self.voice("v3_05"):
            bd.line(r"\hat b_3 = \cos\theta\,\hat n_3 + \sin\theta\,\hat n_1", reason="$\\hat n_3$ plays the role of axis 1")
            bd.line(r"\hat b_1 = -\sin\theta\,\hat n_3 + \cos\theta\,\hat n_1", reason="$\\hat n_1$ plays the role of axis 2")
            l = bd.line(r"C_2(\theta) = \begin{bmatrix}\cos\theta&0&-\sin\theta\\0&1&0\\\sin\theta&0&\cos\theta\end{bmatrix}", color=YELLOW)
            bd.box(l)
            warn = Tx(r"minus sign in the \emph{top-right} corner!", color=P_COL).scale(0.6).next_to(l, RIGHT, buff=0.4)
            self.play(FadeIn(warn))
            self.hold()
        for m in moving:
            m.clear_updaters()
        bd.clear()
        self.play(FadeOut(fixed), FadeOut(moving), FadeOut(warn))

        with self.voice("v3_06"):
            self.play(Transform(hdr, header("A pattern to remember")))
            m1 = mat([["1", "0", "0"], ["0", r"c", r"s"], ["0", r"-s", r"c"]], scale=0.8)
            m2 = mat([[r"c", "0", r"-s"], ["0", "1", "0"], [r"s", "0", r"c"]], scale=0.8)
            m3 = mat([[r"c", r"s", "0"], [r"-s", r"c", "0"], ["0", "0", "1"]], scale=0.8)
            labs = [T(r"C_1:"), T(r"C_2:"), T(r"C_3:")]
            grp = VGroup(*[VGroup(l_.scale(0.85), m_).arrange(RIGHT) for l_, m_ in zip(labs, (m1, m2, m3))]).arrange(RIGHT, buff=0.9)
            grp.move_to(UP * 0.8)
            self.play(LaggedStart(*[FadeIn(g) for g in grp], lag_ratio=0.3), run_time=2.0)
            key = Tx(r"$c=\cos\theta,\ s=\sin\theta$. \ The rotation axis gets a 1 and zeros in its row and column.", color=REASON).scale(0.6)
            key.next_to(grp, DOWN, buff=0.6)
            self.play(FadeIn(key))
            self.wait(1.5)
            for mm, k in ((m1, 7), (m3, 3)):
                self.play(Indicate(mm.get_entries()[k], color=P_COL, scale_factor=1.4))
            self.play(Indicate(m2.get_entries()[2], color=P_COL, scale_factor=1.4))
            rule = Tx(r"minus sign: below the diagonal for $C_1, C_3$;\ \ above it for $C_2$", color=P_COL).scale(0.7).next_to(key, DOWN, buff=0.4)
            self.play(Write(rule))
            self.hold()
        self.play(FadeOut(VGroup(grp, key, rule)))

        # ---- chaining
        with self.voice("v3_07"):
            self.play(Transform(hdr, header("Chaining rotations")))
            bd = Board(self, left=-5.0, top=2.2, scale=0.9, buff=0.5)
            bd.line(r"\{\hat p\} = C_{\mathcal{PA}}\,\{\hat a\}", reason="first rotation: A $\\to$ P")
            bd.line(r"\{\hat q\} = C_{\mathcal{QP}}\,\{\hat p\}", reason="second rotation: P $\\to$ Q")
            self.hold()

        with self.voice("v3_08"):
            bd.line(r"\{\hat q\} = C_{\mathcal{QP}}\,\big(C_{\mathcal{PA}}\,\{\hat a\}\big)", reason="substitute the first line")
            l = bd.line(r"C_{\mathcal{QA}} = C_{\mathcal{QP}}\;C_{\mathcal{PA}}", color=YELLOW)
            bd.box(l)
            note = Tx("newest rotation on the left", color=YELLOW).scale(0.7).next_to(l, RIGHT, buff=0.6)
            self.play(FadeIn(note))
            self.hold()
        bd.clear()
        self.play(FadeOut(note))

        # ---- 3-2-1 in 3D
        cam = Cam(phi=68, theta=28, scale=1.1, center=(-3.0, -0.9))
        D = Draw(cam)
        self.add(*cam.trackers())
        L = 2.4
        psi, tt, ph = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        self.add(psi, tt, ph)
        col = [P_COL]

        def M():
            return euler321(psi.get_value(), tt.get_value(), ph.get_value())
        A, al = D.frame(np.eye(3), N_COL, L, [r"\hat a_1", r"\hat a_2", r"\hat a_3"])
        act, _ = D.frame(M, lambda: col[0], L, width=6, k=1.0)
        for a in act:
            a.op.set_value(0)
        eqs = VGroup(T(r"\text{1. } \psi \text{ about } \hat a_3:\ C_{\mathcal{PA}} = C_3(\psi)", color=P_COL),
                     T(r"\text{2. } \theta \text{ about } \hat p_2:\ C_{\mathcal{QP}} = C_2(\theta)", color=Q_COL),
                     T(r"\text{3. } \phi \text{ about } \hat q_1:\ C_{\mathcal{BQ}} = C_1(\phi)", color=B_COL)
                     ).scale(0.7).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.6 + UP * 1.2)
        with self.voice("v3_09"):
            self.play(Transform(hdr, header("The 3-2-1 sequence: yaw, pitch, roll")))
            self.add(A, al, act)
            self.play(*grow(*A), *show(*al))
            self.play(*show(*act), run_time=0.4)
            self.play(psi.animate.set_value(0.6), tt.animate.set_value(-0.4), ph.animate.set_value(0.7), run_time=2.0)
            self.play(psi.animate.set_value(0), tt.animate.set_value(0), ph.animate.set_value(0), run_time=1.5)
            self.hold()

        arc_psi = D.arc([0, 0, 1], [1, 0, 0], psi.get_value, 1.1, YELLOW)
        with self.voice("v3_10"):
            self.add(arc_psi)
            self.play(psi.animate.set_value(np.radians(40)), Write(eqs[0]), run_time=2.5)
            self.hold()
        P = C3(np.radians(40))
        gP, pl = D.frame(P, P_COL, L, [r"\hat p_1", r"\hat p_2", None], width=3, k=1, label_op=1)
        arc_th = D.arc(P[1], P[0], tt.get_value, 1.1, YELLOW)
        with self.voice("v3_11"):
            col[0] = Q_COL
            self.add(gP, pl, arc_th)
            self.play(tt.animate.set_value(np.radians(30)), Write(eqs[1]), run_time=2.5)
            self.hold()
        Q = C2(np.radians(30)) @ P
        gQ, ql = D.frame(Q, Q_COL, L, [r"\hat q_1", None, r"\hat q_3"], width=3, k=1, label_op=1)
        arc_ph = D.arc(Q[0], Q[1], ph.get_value, 1.1, YELLOW)
        with self.voice("v3_12"):
            col[0] = B_COL
            self.add(gQ, ql, arc_ph)
            self.play(*[g.op.animate.set_value(0.3) for g in gP], *[m.op.animate.set_value(0.3) for m in pl])
            self.play(ph.animate.set_value(np.radians(35)), Write(eqs[2]), run_time=2.5)
            self.hold()

        with self.voice("v3_13"):
            chain = T(r"C_{\mathcal{BA}} = ", r"C_1(\phi)", r"\,C_2(\theta)", r"\,C_3(\psi)").scale(0.9)
            chain[1].set_color(B_COL)
            chain[2].set_color(Q_COL)
            chain[3].set_color(P_COL)
            chain.next_to(eqs, DOWN, buff=0.6)
            self.play(Write(chain), run_time=2.0)
            self.hold()
        stuff = flat(A, al, act, gP, pl, gQ, ql, arc_psi, arc_th, arc_ph)
        self.play(*hide(*stuff), FadeOut(eqs), chain.animate.to_edge(UP, buff=0.8))
        self.remove(*stuff)

        # ---- multiplying out
        with self.voice("v3_14"):
            self.play(Transform(hdr, header("Multiplying it out, step 1: $C_2(\\theta)\\,C_3(\\psi)$")))
            m2 = mat([[r"c\theta", "0", r"-s\theta"], ["0", "1", "0"], [r"s\theta", "0", r"c\theta"]], scale=0.75, color=Q_COL)
            m3 = mat([[r"c\psi", r"s\psi", "0"], [r"-s\psi", r"c\psi", "0"], ["0", "0", "1"]], scale=0.75, color=P_COL)
            res = mat([[r"c\theta\,c\psi", r"c\theta\,s\psi", r"-s\theta"], [r"-s\psi", r"c\psi", "0"],
                       [r"s\theta\,c\psi", r"s\theta\,s\psi", r"c\theta"]], scale=0.75, h_buff=1.9)
            for e in res.get_entries():
                e.set_opacity(0)
            prod = VGroup(m2, m3, T("=").scale(0.8), res).arrange(RIGHT, buff=0.3).move_to(UP * 0.6)
            abbr = Tx(r"shorthand: $c\theta = \cos\theta$, \ $s\psi = \sin\psi$, \dots", color=REASON).scale(0.55).next_to(prod, UP, buff=0.3)
            self.play(FadeIn(prod), FadeIn(abbr))
            work = Board(self, left=-6.0, top=-1.0, scale=0.7, buff=0.25)

            def fill(i, j, tex):
                e = res.get_entries()[3 * i + j]
                self.play(e.animate.set_opacity(1), run_time=0.7)
            h1 = rows_hl(m2, 0)
            self.play(Create(h1))
            for j, (w, t) in enumerate([(r"(c\theta)(c\psi) + 0 + (-s\theta)(0)", r"c\theta\,c\psi"),
                                        (r"(c\theta)(s\psi) + 0 + 0", r"c\theta\,s\psi"),
                                        (r"0 + 0 + (-s\theta)(1)", r"-s\theta")]):
                h2 = col_hl(m3, j)
                self.play(Create(h2), run_time=0.4)
                work.line(r"\text{row 1}\cdot\text{col %d}: " % (j + 1) + w + " = " + t, rt=1.0)
                fill(0, j, t)
                self.play(FadeOut(h2), run_time=0.3)
            self.play(FadeOut(h1))
            self.hold()

        with self.voice("v3_15"):
            work.clear()
            self.play(Create(rows_hl(m2, 1)))
            note = Tx(r"row 2 of $C_2$ is $[0,1,0]$: it copies row 2 of $C_3$", color=REASON).scale(0.6).move_to(DOWN * 1.4)
            self.play(FadeIn(note))
            for j, t in enumerate([r"-s\psi", r"c\psi", "0"]):
                fill(1, j, t)
            self.play(FadeOut(note))
            note2 = Tx(r"row 3 $[s\theta, 0, c\theta]$ times each column", color=REASON).scale(0.6).move_to(DOWN * 1.4)
            self.play(FadeIn(note2))
            for j, t in enumerate([r"s\theta\,c\psi", r"s\theta\,s\psi", r"c\theta"]):
                fill(2, j, t)
            self.hold()

        with self.voice("v3_16"):
            self.play(FadeOut(VGroup(m2, m3, abbr, note2)), *[FadeOut(m) for m in self.mobjects if isinstance(m, SurroundingRectangle)])
            M23 = VGroup(*prod[2:])
            self.play(Transform(hdr, header("Step 2: multiply by $C_1(\\phi)$ on the left")))
            m1 = mat([["1", "0", "0"], ["0", r"c\phi", r"s\phi"], ["0", r"-s\phi", r"c\phi"]], scale=0.7, color=B_COL)
            res2 = res.copy()
            grp = VGroup(m1, res2).arrange(RIGHT, buff=0.25).to_edge(UP, buff=1.6).shift(LEFT * 2.5)
            self.play(FadeOut(M23), FadeIn(grp))
            bd = Board(self, left=-6.3, top=-0.4, scale=0.66, buff=0.3)
            bd.line(r"\text{row 1} = [\,c\theta c\psi,\ \ c\theta s\psi,\ \ -s\theta\,]", reason="row 1 of $C_1$ is $[1,0,0]$")
            bd.line(r"\text{row 2} = c\phi\,(\text{row 2}) + s\phi\,(\text{row 3}) = [\,s\phi s\theta c\psi - c\phi s\psi,\ \ s\phi s\theta s\psi + c\phi c\psi,\ \ s\phi c\theta\,]")
            bd.line(r"\text{row 3} = -s\phi\,(\text{row 2}) + c\phi\,(\text{row 3}) = [\,c\phi s\theta c\psi + s\phi s\psi,\ \ c\phi s\theta s\psi - s\phi c\psi,\ \ c\phi c\theta\,]")
            full = T(r"C_{\mathcal{BA}} = \begin{bmatrix}"
                     r"c\theta\, c\psi & c\theta\, s\psi & -s\theta\\"
                     r"s\phi\, s\theta\, c\psi - c\phi\, s\psi & s\phi\, s\theta\, s\psi + c\phi\, c\psi & s\phi\, c\theta\\"
                     r"c\phi\, s\theta\, c\psi + s\phi\, s\psi & c\phi\, s\theta\, s\psi - s\phi\, c\psi & c\phi\, c\theta"
                     r"\end{bmatrix}", color=YELLOW).scale(0.62)
            self.wait(1.0)
            bd.clear()
            self.play(FadeOut(grp))
            full.scale_to_fit_width(10).move_to(DOWN * 0.5)
            self.play(Write(full), run_time=2.0)
            self.hold()
        self.play(FadeOut(chain), full.animate.scale_to_fit_width(9).to_edge(UP, buff=0.9).set_x(0))

        # ---- inverse problem
        with self.voice("v3_17"):
            self.play(Transform(hdr, header("Going backwards: from a DCM to the angles")))
            bd = Board(self, left=-5.5, top=0.9, scale=0.8, buff=0.38)
            bd.line(r"C_{13} = -\sin\theta", reason="top-right entry")
            l = bd.line(r"\theta = -\sin^{-1}(C_{13})", color=YELLOW, indent=0.8)
            self.hold()

        with self.voice("v3_18"):
            bd.line(r"\frac{C_{12}}{C_{11}} = \frac{\cos\theta\,\sin\psi}{\cos\theta\,\cos\psi} = \tan\psi",
                    reason="the $\\cos\\theta$ cancels (if $\\cos\\theta\\neq0$)")
            bd.line(r"\psi = \operatorname{atan2}(C_{12},\ C_{11})", color=YELLOW, indent=0.8,
                    reason="atan2 picks the right quadrant")
            self.hold()

        with self.voice("v3_19"):
            bd.line(r"\frac{C_{23}}{C_{33}} = \frac{\sin\phi\cos\theta}{\cos\phi\cos\theta} = \tan\phi\ \Rightarrow\ \phi = \operatorname{atan2}(C_{23},\ C_{33})",
                    color=YELLOW)
            self.hold()

        with self.voice("v3_20"):
            bd.clear()
            bd = Board(self, left=-5.5, top=0.9, scale=0.8)
            bd.line(r"\theta = 90^\circ:\quad \cos\theta = 0,\ \ \sin\theta = 1")
            bd.line(r"\text{row 1} = [\,0,\ 0,\ -1\,]", indent=0.8, reason="every $\\psi$ gives the same row")
            bd.line(r"\frac{C_{12}}{C_{11}} = \frac{0}{0}\ \ \Rightarrow\ \ \psi,\ \phi\ \text{not separately defined}", color=P_COL, indent=0.8)
            self.hold()
        bd.clear()
        self.play(FadeOut(full))

        # ---- gimbal lock in 3D
        cam2 = Cam(phi=68, theta=28, scale=1.1, center=(-2.8, -0.9))
        D2 = Draw(cam2)
        self.add(*cam2.trackers())
        psi.set_value(np.radians(30))
        tt.set_value(0)
        ph.set_value(np.radians(20))
        col[0] = B_COL
        A2, al2 = D2.frame(np.eye(3), N_COL, L, [r"\hat a_1", r"\hat a_2", r"\hat a_3"], k=1, label_op=1)
        act2, _ = D2.frame(M, B_COL, L, width=6, k=1)
        yaw = D2.line([0, 0, -3], [0, 0, 3], P_COL, 3, op=0)
        roll = D2.line(lambda: -3 * M()[0], lambda: 3 * M()[0], B_COL, 3, op=0)
        with self.voice("v3_21"):
            self.play(Transform(hdr, header("Gimbal lock")))
            self.add(A2, al2, act2, yaw, roll)
            labs = VGroup(Tx("yaw axis $\\hat a_3$", color=P_COL), Tx("roll axis $\\hat b_1$", color=B_COL)).scale(0.65)
            labs.arrange(DOWN, aligned_edge=LEFT)
            labs.move_to(UP * 2.0).set_x(1.4 + labs.width / 2)
            self.play(*show(yaw, roll), FadeIn(labs))
            thl = always_redraw(lambda: T(r"\theta = %d^\circ" % round(np.degrees(tt.get_value())), color=Q_COL).next_to(labs, DOWN, buff=0.4).align_to(labs, LEFT))
            self.add(thl)
            self.play(tt.animate.set_value(np.radians(90)), run_time=4.0)
            same = Tx(r"roll axis $\parallel$ yaw axis:\\yaw and roll spin about the same line", color=YELLOW).scale(0.6)
            same.next_to(thl, DOWN, buff=0.4).align_to(labs, LEFT)
            self.play(Write(same))
            self.play(psi.animate.increment_value(np.radians(35)), run_time=1.5)
            self.play(ph.animate.increment_value(np.radians(35)), run_time=1.5)
            undo = Tx(r"$+35^\circ$ yaw then $+35^\circ$ roll: back where we started.\\Only $\phi-\psi$ matters.", color=REASON).scale(0.6)
            undo.next_to(same, DOWN, buff=0.3).align_to(labs, LEFT)
            self.play(FadeIn(undo))
            self.hold()
        thl.clear_updaters()
        stuff = flat(A2, al2, act2, yaw, roll)
        self.play(*hide(*stuff), FadeOut(VGroup(labs, thl, same, undo)))
        self.remove(*stuff)

        with self.voice("v3_22"):
            self.play(Transform(hdr, header("Every sequence has a singularity")))
            asym = VGroup(Tx("Asymmetric", color=B_COL), Tx(r"1-2-3, 1-3-2, 2-1-3,\\2-3-1, 3-1-2, 3-2-1", color=DIM).scale(0.75),
                          T(r"\text{lock at } \theta_2 = \pm 90^\circ")).arrange(DOWN, buff=0.3)
            sym = VGroup(Tx("Symmetric", color=Q_COL), Tx(r"1-2-1, 1-3-1, 2-1-2,\\2-3-2, 3-1-3, 3-2-3", color=DIM).scale(0.75),
                         T(r"\text{lock at } \theta_2 = 0^\circ,\ 180^\circ")).arrange(DOWN, buff=0.3)
            VGroup(asym, sym).arrange(RIGHT, buff=2.0).move_to(UP * 0.3)
            self.play(FadeIn(asym, shift=UP * 0.2))
            self.wait(2.0)
            self.play(FadeIn(sym, shift=UP * 0.2))
            tot = Tx(r"$3\times2\times2 = 12$ sequences, all listed in your appendix", color=REASON).scale(0.65).to_edge(DOWN, buff=0.8)
            self.play(FadeIn(tot))
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))


class V3Examples(Lesson):
    def construct(self):
        with self.voice("v3_23"):
            hdr = header("Example 1: angles $\\to$ DCM $\\to$ angles")
            self.play(FadeIn(hdr))
            given = T(r"\psi = 30^\circ,\quad \theta = 20^\circ,\quad \phi = 10^\circ").scale(0.85).to_edge(UP, buff=0.9)
            self.play(Write(given))
            C = mat([["0.8138", "0.4698", "-0.3420"], ["-0.4410", "0.8826", "0.1632"], ["0.3785", "0.0180", "0.9254"]],
                    scale=0.8, h_buff=2.2)
            Cl = T(r"C_{\mathcal{BA}} = C_1(10^\circ)\,C_2(20^\circ)\,C_3(30^\circ) =").scale(0.75)
            grp = VGroup(Cl, C).arrange(RIGHT).next_to(given, DOWN, buff=0.5)
            self.play(Write(Cl))
            self.play(FadeIn(C))
            same = Tx("the same matrix we rebuilt in Lesson 2!", color=Q_COL).scale(0.65).next_to(grp, DOWN, buff=0.3)
            self.play(FadeIn(same))
            self.hold()

        with self.voice("v3_24"):
            self.play(FadeOut(same))
            self.play(Create(SurroundingRectangle(C.get_entries()[2], color=Q_COL, buff=0.08)))
            bd = Board(self, left=-5.5, top=-0.9, scale=0.75, buff=0.3)
            bd.line(r"\theta = -\sin^{-1}(C_{13}) = -\sin^{-1}(-0.3420) = 20^\circ\ \checkmark", color=Q_COL)
            self.hold()

        with self.voice("v3_25"):
            self.play(Create(SurroundingRectangle(VGroup(C.get_entries()[0], C.get_entries()[1]), color=P_COL, buff=0.08)))
            bd.line(r"\psi = \operatorname{atan2}(0.4698,\ 0.8138) = 30^\circ\ \checkmark", color=P_COL)
            self.play(Create(SurroundingRectangle(VGroup(C.get_entries()[5], C.get_entries()[8]), color=B_COL, buff=0.08)))
            bd.line(r"\phi = \operatorname{atan2}(0.1632,\ 0.9254) = 10^\circ\ \checkmark", color=B_COL)
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not hdr])))

        # ---- Example 2: ground station frame
        cam = Cam(phi=72, theta=-30, scale=1.0, center=(-4.0, -1.2))
        D = Draw(cam)
        self.add(*cam.trackers())
        Re = 1.7
        lat, lon = np.radians(28.6), np.radians(45)
        up = np.array([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)])
        east = np.array([-np.sin(lon), np.cos(lon), 0])
        north = np.cross(up, east)
        st = Re * up
        with self.voice("v3_26"):
            self.play(Transform(hdr, header("Example 2: pointing a ground-station dish")))
            earth = D.sphere(ORIGIN, Re, "#7FB3FF")
            nf, nl = D.frame(np.eye(3), N_COL, 2.6, [r"\hat n_1", r"\hat n_2", r"\hat n_3"], width=3, k=1, label_op=1)
            tf = VGroup(*[D.arrow(st, st + 0.9 * v, c, 5, k=0) for v, c in ((up, YELLOW), (east, Q_COL), (north, B_COL))])
            tl = VGroup(D.label(r"\hat t_1\ \text{up}", st + 1.15 * up, YELLOW, 0.55),
                        D.label(r"\hat t_2\ \text{east}", st + 1.2 * east, Q_COL, 0.55),
                        D.label(r"\hat t_3\ \text{north}", st + 1.15 * north + np.array([0, 0, 0.1]), B_COL, 0.55))
            self.add(earth, nf, nl, tf, tl)
            self.play(*grow(*tf), *show(*tl), run_time=1.5)
            rh = Tx(r"check: $\hat t_1\times\hat t_2 = \hat t_3$\ (up $\times$ east = north)", color=REASON).scale(0.6).move_to(RIGHT * 3.0 + UP * 2.4)
            self.play(FadeIn(rh))
            self.hold()

        with self.voice("v3_27"):
            bd = Board(self, left=-0.6, top=1.7, scale=0.75)
            bd.line(r"\text{1) about } \hat n_3 \text{ by } \theta+\lambda:\ \ C_{\mathcal{EN}} = C_3(\theta+\lambda)",
                    reason="$\\hat e_1$ now points at the station's meridian", below=True)
            self.hold()

        with self.voice("v3_28"):
            bd.line(r"\text{2) about } \hat e_2 \text{ by } -\phi:\ \ C_{\mathcal{TE}} = C_2(-\phi)",
                    reason="$C_2(-\\phi)$ tips $\\hat e_1$ up toward the pole: $\\hat t_1 = \\cos\\phi\\,\\hat e_1 + \\sin\\phi\\,\\hat e_3$", below=True)
            l = bd.line(r"C_{\mathcal{TN}} = C_2(-\phi)\;C_3(\theta+\lambda)", color=YELLOW, reason="newest rotation on the left")
            bd.box(l)
            self.hold()
        stuff = flat(earth, nf, nl, tf, tl)
        self.play(*hide(*stuff), FadeOut(rh))
        self.remove(*stuff)
        bd.clear()

        with self.voice("v3_29"):
            self.play(Transform(hdr, header("Kennedy Space Center: $\\phi = 28.6^\\circ$, \\ $\\theta+\\lambda = 45^\\circ$")))
            a = mat([["0.8780", "0", "0.4787"], ["0", "1", "0"], ["-0.4787", "0", "0.8780"]], scale=0.62, h_buff=2.0)
            b = mat([["0.7071", "0.7071", "0"], ["-0.7071", "0.7071", "0"], ["0", "0", "1"]], scale=0.62, h_buff=2.0)
            c = mat([["0.6208", "0.6208", "0.4787"], ["-0.7071", "0.7071", "0"], ["-0.3385", "-0.3385", "0.8780"]], scale=0.62, h_buff=2.0)
            la = T(r"C_2(-28.6^\circ)", color=Q_COL).scale(0.6).next_to(a, UP, buff=0.15)
            lb = T(r"C_3(45^\circ)", color=P_COL).scale(0.6).next_to(b, UP, buff=0.15)
            lc = T(r"C_{\mathcal{TN}}", color=YELLOW).scale(0.6).next_to(c, UP, buff=0.15)
            row = VGroup(VGroup(a, la), VGroup(b, lb), T("=").scale(0.7), VGroup(c, lc)).arrange(RIGHT, buff=0.3).to_edge(UP, buff=1.1)
            self.play(FadeIn(row[0]), FadeIn(row[1]))
            ex = T(r"\text{e.g. row 1, col 1: } (0.8780)(0.7071) + 0 + (0.4787)(0) = 0.6208", color=REASON).scale(0.6)
            ex.next_to(row, DOWN, buff=0.4)
            self.play(Create(rows_hl(a, 0)), Create(col_hl(b, 0)))
            self.play(Write(ex), run_time=1.5)
            self.play(FadeIn(row[2]), FadeIn(row[3]))
            self.hold()

        with self.voice("v3_30"):
            self.play(*[FadeOut(m) for m in self.mobjects if isinstance(m, SurroundingRectangle)], FadeOut(ex))
            bd = Board(self, left=-6.3, top=-0.3, scale=0.68, buff=0.3, ceiling=row.get_bottom()[1] - 0.05)
            bd.line(r"r_{(\mathcal N)} = [\,3539,\ 4530,\ 3592\,]^T\ \text{km}", reason="satellite")
            bd.line(r"C_{\mathcal{TN}}\,r_{(\mathcal N)} = [\,(0.6208)(3539) + (0.6208)(4530) + (0.4787)(3592),\ \ \dots\,]^T = [\,6728.9,\ 700.7,\ 422.5\,]^T")
            bd.line(r"\vec\rho_{(\mathcal T)} = [\,6728.9,\ 700.7,\ 422.5\,]^T - [\,6378,\ 0,\ 0\,]^T", reason="subtract the station: $R_\\oplus\\,\\hat t_1$")
            self.hold()

        with self.voice("v3_31"):
            l = bd.line(r"\vec\rho_{(\mathcal T)} = [\,350.9\ \text{up},\ \ 700.7\ \text{east},\ \ 422.5\ \text{north}\,]^T\ \text{km}", color=YELLOW)
            bd.line(r"\text{up} > 0\ \Rightarrow\ \text{above the horizon}", color=Q_COL, indent=0.6)
            self.hold()

        with self.voice("v3_32"):
            bd.line(r"|\vec\rho| = \sqrt{350.9^2 + 700.7^2 + 422.5^2} = 890.3\ \text{km}")
            bd.line(r"\text{elevation} = \sin^{-1}(350.9 / 890.3) \approx 23.2^\circ", color=YELLOW, indent=0.6)
            bd.line(r"\text{azimuth} = \operatorname{atan2}(\text{east},\ \text{north}) = \operatorname{atan2}(700.7,\ 422.5) \approx 58.9^\circ",
                    color=YELLOW, indent=0.6, reason="measured from north toward east")
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("v3_33"):
            h, rows = recap(self, [
                r"Single-axis DCMs $C_1, C_2, C_3$ are the building blocks (watch $C_2$'s sign).",
                r"Chain rotations with the newest on the left: $C_{\mathcal{BA}} = C_1(\phi)C_2(\theta)C_3(\psi)$.",
                r"Read angles back: $\theta = -\sin^{-1}C_{13}$, \ $\psi = \operatorname{atan2}(C_{12}, C_{11})$, \ $\phi = \operatorname{atan2}(C_{23}, C_{33})$.",
                r"Gimbal lock: at $\theta = \pm90^\circ$ (3-2-1) only $\phi-\psi$ is defined.",
            ])
            for rrow in rows:
                self.play(FadeIn(rrow, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
