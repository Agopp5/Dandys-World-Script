"""Lesson 2: Direction cosine matrices."""
from lcommon import *  # noqa: F401,F403

BM = euler321(np.radians(35), np.radians(-20), np.radians(25))


def topview(O, L, th):
    """2D top view of N (grey) and B (blue) rotated by angle tracker th about n3."""
    def bvec(i):
        t = th.get_value()
        return [np.array([np.cos(t), np.sin(t), 0]), np.array([-np.sin(t), np.cos(t), 0])][i]
    n1 = Arrow(O, O + L * RIGHT, buff=0, color=N_COL, stroke_width=4)
    n2 = Arrow(O, O + L * UP, buff=0, color=N_COL, stroke_width=4)
    n1l = T(r"\hat n_1", color=N_COL).scale(0.75).next_to(n1.get_end(), RIGHT, buff=0.1)
    n2l = T(r"\hat n_2", color=N_COL).scale(0.75).next_to(n2.get_end(), UP, buff=0.1)
    dot3 = VGroup(Circle(radius=0.12, color=WHITE, stroke_width=2), Dot(radius=0.035)).move_to(O)
    l3 = T(r"\hat n_3 = \hat b_3\ (\text{out of page})", color=DIM).scale(0.5).next_to(O, DOWN, buff=0.25)
    b1 = always_redraw(lambda: Arrow(O, O + L * bvec(0), buff=0, color=B_COL, stroke_width=5))
    b2 = always_redraw(lambda: Arrow(O, O + L * bvec(1), buff=0, color=B_COL, stroke_width=5))
    b1l = always_redraw(lambda: T(r"\hat b_1", color=B_COL).scale(0.75).move_to(O + (L + 0.35) * bvec(0)))
    b2l = always_redraw(lambda: T(r"\hat b_2", color=B_COL).scale(0.75).move_to(O + (L + 0.35) * bvec(1)))
    arc = always_redraw(lambda: Arc(radius=0.8, start_angle=0, angle=th.get_value() + 1e-4, arc_center=O, color=YELLOW))
    arcl = always_redraw(lambda: T(r"\theta", color=YELLOW).scale(0.65).move_to(
        O + 1.05 * np.array([np.cos(th.get_value() / 2), np.sin(th.get_value() / 2), 0])))
    return VGroup(n1, n2, n1l, n2l, dot3, l3), VGroup(b1, b2, b1l, b2l, arc, arcl)


class V2Concept(Lesson):
    def construct(self):
        with self.voice("v2_01"):
            card = title_card(self, 2, "Direction Cosine Matrices", "converting components from one frame to another")
            self.hold()
        self.play(FadeOut(card))

        cam = Cam(phi=70, theta=28, scale=1.0, center=(-4.3, -1.2))
        D = Draw(cam)
        self.add(*cam.trackers())
        L = 2.4
        hdr = header("Each basis vector of B is a vector")
        with self.voice("v2_02"):
            self.play(FadeIn(hdr))
            nf, nl = D.frame(np.eye(3), N_COL, L, [r"\hat n_1", r"\hat n_2", r"\hat n_3"])
            bf, bl = D.frame(BM, B_COL, L, [r"\hat b_1", r"\hat b_2", r"\hat b_3"])
            self.add(nf, nl, bf, bl)
            self.play(*grow(*nf), *show(*nl), run_time=1.5)
            self.play(*grow(*bf), *show(*bl), run_time=1.5)
            note = Tx(r"$\mathcal N$ (grey) and $\mathcal B$ (blue)\\share the same origin", color=REASON).scale(0.65)
            note.move_to(RIGHT * 3.0 + UP * 2.4)
            self.play(FadeIn(note))
            self.hold()

        b1 = BM[0]
        with self.voice("v2_03"):
            self.play(FadeOut(note))
            sh = [D.line(ORIGIN, b1[i] * L * np.eye(3)[i], YELLOW, 9, k=0) for i in range(3)]
            dl = [D.line(L * b1, b1[i] * L * np.eye(3)[i], DIM, 2, dashed=True, k=0) for i in range(3)]
            self.add(*dl, *sh)
            bd = Board(self, left=-1.4, top=2.3, scale=0.78)
            bd.line(r"\hat b_1 = (\hat b_1\cdot\hat n_1)\,\hat n_1 + (\hat b_1\cdot\hat n_2)\,\hat n_2 + (\hat b_1\cdot\hat n_3)\,\hat n_3",
                    reason="components = dot products (Lesson 1)", below=True, rt=2.5)
            self.play(*grow(*dl), run_time=1.0)
            self.play(LaggedStart(*grow(*sh), lag_ratio=0.4), run_time=2.0)
            self.hold()

        with self.voice("v2_04"):
            bd.line(r"\hat b_2 = (\hat b_2\cdot\hat n_1)\,\hat n_1 + (\hat b_2\cdot\hat n_2)\,\hat n_2 + (\hat b_2\cdot\hat n_3)\,\hat n_3", rt=1.8)
            bd.line(r"\hat b_3 = (\hat b_3\cdot\hat n_1)\,\hat n_1 + (\hat b_3\cdot\hat n_2)\,\hat n_2 + (\hat b_3\cdot\hat n_3)\,\hat n_3", rt=1.8)
            self.hold()
        stuff = flat(nf, nl, bf, bl, *sh, *dl)
        self.play(*hide(*stuff), run_time=0.6)
        self.remove(*stuff)
        bd.clear()

        with self.voice("v2_05"):
            self.play(Transform(hdr, header("Three equations become one matrix equation")))
            eq = T(r"\begin{bmatrix}\hat b_1\\\hat b_2\\\hat b_3\end{bmatrix} =",
                   r"\begin{bmatrix}\hat b_1\!\cdot\!\hat n_1 & \hat b_1\!\cdot\!\hat n_2 & \hat b_1\!\cdot\!\hat n_3\\"
                   r"\hat b_2\!\cdot\!\hat n_1 & \hat b_2\!\cdot\!\hat n_2 & \hat b_2\!\cdot\!\hat n_3\\"
                   r"\hat b_3\!\cdot\!\hat n_1 & \hat b_3\!\cdot\!\hat n_2 & \hat b_3\!\cdot\!\hat n_3\end{bmatrix}",
                   r"\begin{bmatrix}\hat n_1\\\hat n_2\\\hat n_3\end{bmatrix}").scale(0.85).move_to(UP * 0.8)
            self.play(Write(eq), run_time=3.0)
            br = Brace(eq[1], DOWN, color=YELLOW)
            brl = T(r"C_{\mathcal{BN}}", color=YELLOW).next_to(br, DOWN, buff=0.1)
            name = Tx("the direction cosine matrix (DCM)", color=YELLOW).scale(0.65).next_to(brl, DOWN, buff=0.15)
            self.play(GrowFromCenter(br), Write(brl))
            self.play(FadeIn(name))
            self.hold()

        with self.voice("v2_06"):
            entry = T(r"C_{ij}", r"= \hat b_i\cdot\hat n_j", r"= |\hat b_i|\,|\hat n_j|\cos\theta_{ij}", r"= \cos\theta_{ij}").scale(0.85)
            entry.next_to(name, DOWN, buff=0.5)
            self.play(Write(entry[:2]))
            self.wait(1.0)
            self.play(Write(entry[2]))
            self.play(Write(entry[3]))
            why = Tx(r"$\theta_{ij}$ = angle between axis $\hat b_i$ and axis $\hat n_j$; both lengths are 1",
                     color=REASON).scale(0.55).next_to(entry, DOWN, buff=0.2)
            self.play(FadeIn(why))
            self.hold()
        self.play(FadeOut(VGroup(eq, br, brl, name, entry, why)))

        # ---- worked: rotation about n3 by theta, entry by entry
        th = ValueTracker(0)
        self.add(th)
        O = np.array([-4.3, -1.0, 0])
        Lr = 2.4
        fixed, moving = topview(O, Lr, th)
        t0 = np.radians(32)
        with self.voice("v2_07"):
            self.play(Transform(hdr, header("Example inside the concept: rotate by $\\theta$ about $\\hat n_3$")))
            self.play(FadeIn(fixed))
            self.add(moving)
            self.play(th.animate.set_value(t0), run_time=2.0)
            C = mat([[r"?", r"?", r"?"], [r"?", r"?", r"?"], [r"?", r"?", r"?"]], scale=0.8, h_buff=1.9)
            Cl = T(r"C_{\mathcal{BN}} =").scale(0.85)
            Cg = VGroup(Cl, C).arrange(RIGHT).move_to(RIGHT * 2.8 + UP * 1.5)
            self.play(FadeIn(Cg))
            rlab = VGroup(*[T(r"\hat b_%d" % (i + 1), color=B_COL).scale(0.6).next_to(C.get_rows()[i], LEFT, buff=0.15).shift(LEFT * 0.0)
                            for i in range(3)])
            clab = VGroup(*[T(r"\hat n_%d" % (j + 1), color=N_COL).scale(0.6).next_to(C.get_columns()[j], UP, buff=0.25)
                            for j in range(3)])
            rlab.next_to(C, LEFT, buff=1.3)
            for i in range(3):
                rlab[i].match_y(C.get_rows()[i])
            Cl.next_to(rlab, LEFT, buff=0.2)
            self.play(FadeIn(rlab), FadeIn(clab))
            self.hold()

        tip1 = O + Lr * np.array([np.cos(t0), np.sin(t0), 0])
        tip2 = O + Lr * np.array([-np.sin(t0), np.cos(t0), 0])
        notes = VGroup()

        def setentry(i, j, tex, color=WHITE):
            e = C.get_entries()[3 * i + j]
            new = T(tex, color=color).scale(0.8).move_to(e)
            self.play(Transform(e, new), run_time=0.8)

        with self.voice("v2_08"):
            hl = rows_hl(C, 0)
            self.play(Create(hl))
            n_ = Tx(r"angle($\hat b_1,\hat n_1$) $=\theta$ $\Rightarrow\cos\theta$", color=REASON).scale(0.55)
            n_.next_to(Cg, DOWN, buff=0.5).align_to(Cg, LEFT)
            notes.add(n_)
            self.play(FadeIn(n_))
            setentry(0, 0, r"\cos\theta")
            a2 = Arc(radius=0.55, start_angle=t0, angle=PI / 2 - t0, arc_center=O, color=V_COL)
            a2l = T(r"90^\circ\!-\!\theta", color=V_COL).scale(0.45).move_to(O + 0.95 * np.array([np.cos(1.2), np.sin(1.2), 0]) + RIGHT * 0.15)
            self.play(Create(a2), FadeIn(a2l))
            n_ = Tx(r"angle($\hat b_1,\hat n_2$) $=90^\circ-\theta$ $\Rightarrow\cos(90^\circ-\theta)=\sin\theta$", color=REASON).scale(0.55)
            n_.next_to(notes[-1], DOWN, buff=0.15).align_to(notes[-1], LEFT)
            notes.add(n_)
            self.play(FadeIn(n_))
            setentry(0, 1, r"\sin\theta")
            n_ = Tx(r"$\hat b_1\perp\hat n_3$ $\Rightarrow 0$", color=REASON).scale(0.55).next_to(notes[-1], DOWN, buff=0.15).align_to(notes[-1], LEFT)
            notes.add(n_)
            self.play(FadeIn(n_))
            setentry(0, 2, r"0")
            self.hold()

        with self.voice("v2_09"):
            self.play(FadeOut(a2), FadeOut(a2l), Transform(hl, rows_hl(C, 1)))
            a3 = Arc(radius=0.5, start_angle=0, angle=PI / 2 + t0, arc_center=O, color=V_COL)
            a3l = T(r"90^\circ\!+\!\theta", color=V_COL).scale(0.45).move_to(O + 0.85 * np.array([np.cos(1.0), np.sin(1.0), 0]) + RIGHT * 0.3)
            self.play(Create(a3), FadeIn(a3l))
            n_ = Tx(r"angle($\hat b_2,\hat n_1$) $=90^\circ+\theta$ $\Rightarrow\cos(90^\circ+\theta)=-\sin\theta$", color=REASON).scale(0.55)
            n_.next_to(notes[-1], DOWN, buff=0.15).align_to(notes[-1], LEFT)
            notes.add(n_)
            self.play(FadeIn(n_))
            setentry(1, 0, r"-\sin\theta")
            n_ = Tx(r"angle($\hat b_2,\hat n_2$) $=\theta$ $\Rightarrow\cos\theta$;\ \ $\hat b_2\perp\hat n_3\Rightarrow 0$", color=REASON).scale(0.55)
            n_.next_to(notes[-1], DOWN, buff=0.15).align_to(notes[-1], LEFT)
            notes.add(n_)
            self.play(FadeIn(n_))
            setentry(1, 1, r"\cos\theta")
            setentry(1, 2, r"0")
            self.hold()

        with self.voice("v2_10"):
            self.play(FadeOut(a3), FadeOut(a3l), Transform(hl, rows_hl(C, 2)))
            n_ = Tx(r"$\hat b_3=\hat n_3$ $\Rightarrow$ 0, 0, 1", color=REASON).scale(0.55).next_to(notes[-1], DOWN, buff=0.15).align_to(notes[-1], LEFT)
            notes.add(n_)
            self.play(FadeIn(n_))
            setentry(2, 0, "0")
            setentry(2, 1, "0")
            setentry(2, 2, "1")
            self.hold()

        with self.voice("v2_11"):
            self.play(FadeOut(hl))
            res = T(r"C_3(\theta) = \begin{bmatrix}\cos\theta & \sin\theta & 0\\-\sin\theta & \cos\theta & 0\\0 & 0 & 1\end{bmatrix}",
                    color=YELLOW).scale(0.85)
            res.move_to(Cg)
            self.play(FadeOut(rlab), FadeOut(clab), ReplacementTransform(Cg, res), run_time=1.5)
            self.play(Create(SurroundingRectangle(res, color=YELLOW, buff=0.15)))
            lab = Tx("rotation about the 3rd axis", color=YELLOW).scale(0.6).next_to(res, DOWN, buff=0.35)
            self.play(FadeOut(notes), FadeIn(lab))
            self.hold()
        for m in moving:
            m.clear_updaters()
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not hdr and not isinstance(m, ValueTracker)])))

        # ---- deriving r_(B) = C r_(N)
        with self.voice("v2_12"):
            self.play(Transform(hdr, header("Converting components: where $r_{(\\mathcal B)} = C_{\\mathcal{BN}}\\,r_{(\\mathcal N)}$ comes from")))
            goal = Tx(r"Know $r_{(\mathcal N)}$, want $r_{(\mathcal B)}$", color=YELLOW).scale(0.75).to_edge(UP, buff=1.0)
            self.play(FadeIn(goal))
            bd = Board(self, left=-6.0, top=1.9, scale=0.85, buff=0.45)
            bd.line(r"(r_{(\mathcal B)})_1 = \vec r\cdot\hat b_1", reason="a B component is a dot product with a B axis")
            self.hold()

        with self.voice("v2_13"):
            bd.line(r"= \hat b_1\cdot\Big(\sum_{j=1}^{3} r_j\,\hat n_j\Big)", indent=1.4,
                    reason=r"write $\vec r$ in $\mathcal N$ components: $r_j = (r_{(\mathcal N)})_j$")
            self.hold()

        with self.voice("v2_14"):
            bd.line(r"= \sum_{j=1}^{3} (\hat b_1\cdot\hat n_j)\, r_j", indent=1.4,
                    reason=r"dot product distributes; each $r_j$ is just a number")
            self.hold()

        with self.voice("v2_15"):
            bd.line(r"= C_{11}\,r_1 + C_{12}\,r_2 + C_{13}\,r_3", indent=1.4, reason=r"$\hat b_1\cdot\hat n_j = C_{1j}$")
            bd.line(r"= \begin{bmatrix}C_{11} & C_{12} & C_{13}\end{bmatrix}\begin{bmatrix}r_1\\r_2\\r_3\end{bmatrix}", indent=1.4,
                    reason=r"row 1 of $C$ times the column $r_{(\mathcal N)}$")
            self.hold()

        with self.voice("v2_16"):
            bd.clear()
            res = T(r"r_{(\mathcal B)} = C_{\mathcal{BN}}\; r_{(\mathcal N)}").scale(1.3)
            box = SurroundingRectangle(res, color=YELLOW, buff=0.25)
            every = Tx("every row works the same way", color=REASON).scale(0.65).next_to(box, DOWN, buff=0.3)
            self.play(Write(res), run_time=1.8)
            self.play(Create(box), FadeIn(every))
            self.hold()
        self.play(FadeOut(VGroup(res, box, every, goal)))

        # ---- orthogonality
        with self.voice("v2_17"):
            self.play(Transform(hdr, header("Why the inverse is just the transpose")))
            rows = T(r"C_{\mathcal{BN}} = \begin{bmatrix} \text{---}\ \hat b_1^{T}\ \text{---}\\ \text{---}\ \hat b_2^{T}\ \text{---}\\ \text{---}\ \hat b_3^{T}\ \text{---}\end{bmatrix}").scale(0.85)
            rl = Tx(r"each row = a $\mathcal B$ axis in $\mathcal N$ components", color=REASON).scale(0.6)
            VGroup(rows, rl).arrange(RIGHT, buff=0.5).to_edge(UP, buff=1.1)
            self.play(Write(rows), run_time=1.8)
            self.play(FadeIn(rl))
            cct = T(r"C\,C^{T} = \begin{bmatrix} \text{---}\ \hat b_1^{T}\ \text{---}\\ \text{---}\ \hat b_2^{T}\ \text{---}\\ \text{---}\ \hat b_3^{T}\ \text{---}\end{bmatrix}"
                    r"\begin{bmatrix} | & | & | \\ \hat b_1 & \hat b_2 & \hat b_3\\ | & | & | \end{bmatrix}").scale(0.8)
            cct.next_to(VGroup(rows, rl), DOWN, buff=0.5)
            self.play(Write(cct), run_time=2.0)
            self.hold()

        with self.voice("v2_18"):
            e1 = T(r"(C\,C^{T})_{ik} = \hat b_i\cdot\hat b_k = \begin{cases}1 & i = k\\ 0 & i\neq k\end{cases}").scale(0.8)
            e2 = T(r"C\,C^{T} = \begin{bmatrix}1&0&0\\0&1&0\\0&0&1\end{bmatrix} = I", color=YELLOW).scale(0.8)
            VGroup(e1, e2).arrange(RIGHT, buff=0.9).next_to(cct, DOWN, buff=0.5)
            self.play(Write(e1), run_time=2.0)
            self.wait(1.0)
            self.play(Write(e2), run_time=1.5)
            self.hold()

        with self.voice("v2_19"):
            self.play(FadeOut(VGroup(rows, rl, cct, e1)), e2.animate.to_edge(UP, buff=1.1))
            bd = Board(self, left=-4.5, top=1.6, scale=0.9)
            bd.line(r"C_{\mathcal{BN}}^{-1} = C_{\mathcal{BN}}^{T}", reason="multiply $C C^T = I$ by $C^{-1}$")
            l = bd.line(r"C_{\mathcal{NB}} = C_{\mathcal{BN}}^{T}", color=YELLOW)
            bd.line(r"r_{(\mathcal N)} = C_{\mathcal{BN}}^{T}\, r_{(\mathcal B)}", reason="going backwards: no inversion needed")
            self.hold()

        with self.voice("v2_20"):
            bd.line(r"\text{columns of } C_{\mathcal{BN}} = \hat n_j \text{ in } \mathcal B \text{ components}")
            bd.line(r"\det C_{\mathcal{BN}} = +1", reason=r"right-handed ($-1$ would be a mirror image)")
            self.hold()

        with self.voice("v2_21"):
            bd.clear()
            self.play(FadeOut(e2))
            nine = T(r"9", r"\text{ entries}").scale(1.0)
            c1 = T(r"-\,3", r"\quad |\hat b_i| = 1", color=Q_COL).scale(0.9)
            c2 = T(r"-\,3", r"\quad \hat b_i\cdot\hat b_k = 0\ (i\neq k)", color=Q_COL).scale(0.9)
            res = T(r"= 3", r"\ \text{independent numbers}", color=YELLOW).scale(1.0)
            col = VGroup(nine, c1, c2, res).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.2)
            for m in col:
                self.play(Write(m), run_time=1.2)
                self.wait(0.6)
            nxt = Tx("three angles $\\Rightarrow$ Euler angles, next lesson", color=REASON).scale(0.65).next_to(col, DOWN, buff=0.6)
            self.play(FadeIn(nxt))
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))


class V2Examples(Lesson):
    def construct(self):
        # ---- Example 1
        with self.voice("v2_22"):
            hdr = header("Example 1: converting a vector")
            self.play(FadeIn(hdr))
            given = Tx(r"$\mathcal B$ is rotated $30^\circ$ about $\hat n_3$, \quad $r_{(\mathcal N)} = [\,2,\ 1,\ 0\,]^T$. \quad Find $r_{(\mathcal B)}$.").scale(0.75)
            given.to_edge(UP, buff=0.9)
            self.play(Write(given), run_time=2.0)
            self.hold()

        with self.voice("v2_23"):
            vals = T(r"\cos 30^\circ \approx 0.866,\qquad \sin 30^\circ = 0.5", color=REASON).scale(0.7).next_to(given, DOWN, buff=0.4)
            self.play(FadeIn(vals))
            C = mat([["0.866", "0.5", "0"], ["-0.5", "0.866", "0"], ["0", "0", "1"]], scale=0.85, h_buff=1.5)
            r = mat([["2"], ["1"], ["0"]], scale=0.85)
            lhs = T(r"r_{(\mathcal B)} = ").scale(0.85)
            eq = VGroup(lhs, C, r).arrange(RIGHT, buff=0.25).move_to(LEFT * 2.5 + DOWN * 0.3)
            self.play(Write(lhs), FadeIn(C), run_time=1.5)
            self.play(FadeIn(r))
            self.hold()

        out = mat([["?"], ["?"], ["?"]], scale=0.85)
        eqs = T("=").scale(0.85)
        VGroup(eqs, out).arrange(RIGHT, buff=0.25).next_to(r, RIGHT, buff=0.25)
        work = VGroup()

        def row_step(i, tex, result):
            h1 = rows_hl(C, i)
            h2 = SurroundingRectangle(r, color=Q_COL, buff=0.08)
            self.play(Create(h1), Create(h2))
            w = T(tex).scale(0.7)
            if len(work):
                w.next_to(work[-1], DOWN, buff=0.3).align_to(work[-1], LEFT)
            else:
                w.next_to(eq, DOWN, buff=0.7).align_to(eq, LEFT)
            work.add(w)
            self.play(Write(w), run_time=2.0)
            e = out.get_entries()[i]
            self.play(Transform(e, T(result, color=YELLOW).scale(0.85).move_to(e)), FadeOut(h1), FadeOut(h2))

        with self.voice("v2_24"):
            self.play(FadeIn(eqs), FadeIn(out))
            row_step(0, r"\text{row 1: } (0.866)(2) + (0.5)(1) + (0)(0) = 2.232", "2.232")
            self.hold()

        with self.voice("v2_25"):
            row_step(1, r"\text{row 2: } (-0.5)(2) + (0.866)(1) + (0)(0) = -0.134", "-0.134")
            row_step(2, r"\text{row 3: } (0)(2) + (0)(1) + (1)(0) = 0", "0")
            self.hold()

        with self.voice("v2_26"):
            chk = VGroup(
                T(r"|r_{(\mathcal N)}| = \sqrt{2^2 + 1^2 + 0^2} = \sqrt5 \approx 2.236"),
                T(r"|r_{(\mathcal B)}| = \sqrt{2.232^2 + 0.134^2} \approx 2.236\ \checkmark", color=Q_COL),
            ).scale(0.62).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UR, buff=0.4).shift(DOWN * 1.6)
            why = Tx("rotating a frame never changes a length", color=REASON).scale(0.55).next_to(chk, UP, buff=0.25).align_to(chk, LEFT)
            self.play(FadeIn(why))
            self.play(Write(chk[0]), run_time=1.8)
            self.play(Write(chk[1]), run_time=1.8)
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not hdr])))

        # ---- Example 2: missing entries
        with self.voice("v2_27"):
            self.play(Transform(hdr, header("Example 2: rebuilding a DCM from partial data")))
            C = mat([["0.8138", "0.4698", "-0.3420"], ["a", "0.8826", "0.1632"], ["b", "c", "0.9254"]], scale=0.8, h_buff=2.3)
            for k in (3, 6, 7):
                C.get_entries()[k].set_color(YELLOW)
            Cl = T(r"C_{\mathcal{BN}} =").scale(0.8)
            Cg = VGroup(Cl, C).arrange(RIGHT).to_edge(UP, buff=0.9).shift(LEFT * 2.8)
            self.play(Write(Cl), FadeIn(C), run_time=1.5)
            tip = Tx(r"tools:\\rows are unit vectors\\rows are perpendicular\\$\hat b_3 = \hat b_1\times\hat b_2$", color=REASON).scale(0.6)
            tip.next_to(Cg, RIGHT, buff=0.6)
            self.play(FadeIn(tip))
            self.hold()

        with self.voice("v2_28"):
            self.play(Create(rows_hl(C, 1)))
            bd = Board(self, left=-6.3, top=0.6, scale=0.72, buff=0.3)
            bd.line(r"a^2 + 0.8826^2 + 0.1632^2 = 1", reason="row 2 is a unit vector")
            bd.line(r"a^2 = 1 - 0.7790 - 0.0266 = 0.1944", indent=0.8)
            bd.line(r"a = \pm\,0.441", indent=0.8, color=YELLOW)
            self.hold()

        with self.voice("v2_29"):
            bd.line(r"a=+0.441:\ (0.8138)(0.441) + (0.4698)(0.8826) + (-0.342)(0.1632) = 0.718 \neq 0", color=P_COL,
                    reason="row 1 $\\cdot$ row 2 must be 0")
            bd.line(r"a=-0.441:\ (0.8138)(-0.441) + (0.4698)(0.8826) + (-0.342)(0.1632) \approx 0\ \checkmark", color=Q_COL)
            e = C.get_entries()[3]
            self.play(Transform(e, T("-0.441", color=Q_COL).scale(0.8).move_to(e)))
            self.hold()

        with self.voice("v2_30"):
            bd.clear()
            bd = Board(self, left=-6.3, top=0.6, scale=0.72, buff=0.3)
            bd.line(r"\text{row 3} = \text{row 1}\times\text{row 2}", reason=r"$\hat b_3 = \hat b_1\times\hat b_2$ (right-handed)")
            bd.line(r"(0.4698)(0.1632) - (-0.342)(0.8826) = 0.3785", indent=0.8)
            bd.line(r"(-0.342)(-0.441) - (0.8138)(0.1632) = 0.0180", indent=0.8)
            bd.line(r"(0.8138)(0.8826) - (0.4698)(-0.441) = 0.9254", indent=0.8, reason="matches the given entry: a good check")
            e6, e7 = C.get_entries()[6], C.get_entries()[7]
            self.play(Transform(e6, T("0.3785", color=Q_COL).scale(0.8).move_to(e6)),
                      Transform(e7, T("0.0180", color=Q_COL).scale(0.8).move_to(e7)))
            self.hold()

        with self.voice("v2_31"):
            bd.clear()
            hl = SurroundingRectangle(C.get_entries()[1], color=YELLOW, buff=0.08)
            self.play(Create(hl))
            bd = Board(self, left=-5.0, top=0.3, scale=0.8)
            bd.line(r"\cos\theta_{\hat b_1,\hat n_2} = C_{12} = 0.4698", reason="entry (1,2) is that direction cosine")
            l = bd.line(r"\theta = \cos^{-1}(0.4698) \approx 62.0^\circ", color=YELLOW, indent=0.8)
            bd.box(l)
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not hdr])))

        # ---- Example 3: LVLH frame from r and v
        with self.voice("v2_32"):
            self.play(Transform(hdr, header("Example 3: building a frame from two vectors (LVLH)")))
            E = Circle(radius=0.8, color="#7FB3FF", fill_color="#16335C", fill_opacity=1).move_to(LEFT * 5.7 + UP * 0.6)
            sc = Dot(E.get_center() + RIGHT * 1.7, color=WHITE)
            rv = Arrow(E.get_center(), sc.get_center(), buff=0, color=R_COL)
            vv = Arrow(sc.get_center(), sc.get_center() + UP * 1.1, buff=0, color=Q_COL)
            rl = T(r"\vec r", color=R_COL).scale(0.7).next_to(rv, DOWN, buff=0.05)
            vl = T(r"\vec v", color=Q_COL).scale(0.7).next_to(vv, RIGHT, buff=0.05)
            self.play(FadeIn(E), GrowArrow(rv), FadeIn(sc), FadeIn(rl))
            self.play(GrowArrow(vv), FadeIn(vl))
            defs = VGroup(
                T(r"\hat t_1 = \frac{\vec r}{|\vec r|}"), T(r"\hat t_3 = \frac{\vec r\times\vec v}{|\vec r\times\vec v|}"),
                T(r"\hat t_2 = \hat t_3\times\hat t_1")).scale(0.75).arrange(RIGHT, buff=0.7).to_edge(UP, buff=1.0).shift(RIGHT * 1.4)
            for d_ in defs:
                self.play(Write(d_), run_time=1.2)
            self.hold()

        with self.voice("v2_33"):
            bd = Board(self, left=-3.0, top=1.4, scale=0.72, buff=0.32)
            bd.line(r"r_{(\mathcal N)} = [\,7000,\ 0,\ 0\,]^T\ \text{km},\quad v_{(\mathcal N)} = [\,0,\ 5,\ 5\,]^T\ \text{km/s}")
            bd.line(r"\hat t_1 = \tfrac{1}{7000}[\,7000,\ 0,\ 0\,]^T = [\,1,\ 0,\ 0\,]^T", color=YELLOW)
            self.hold()

        with self.voice("v2_34"):
            bd.line(r"\vec r\times\vec v = [\,0\cdot5 - 0\cdot5,\ \ 0\cdot0 - 7000\cdot5,\ \ 7000\cdot5 - 0\cdot0\,]^T",
                    reason="cross product formula (Lesson 1)")
            bd.line(r"= [\,0,\ -35000,\ 35000\,]^T", indent=0.8)
            bd.line(r"|\vec r\times\vec v| = 35000\sqrt2", indent=0.8)
            bd.line(r"\hat t_3 = [\,0,\ -\tfrac{1}{\sqrt2},\ \tfrac{1}{\sqrt2}\,]^T", color=YELLOW, indent=0.8)
            self.hold()

        with self.voice("v2_35"):
            bd.line(r"\hat t_2 = \hat t_3\times\hat t_1 = [\,0,\ \tfrac{1}{\sqrt2},\ \tfrac{1}{\sqrt2}\,]^T", color=YELLOW)
            res = T(r"C_{\mathcal{TN}} = \begin{bmatrix} 1 & 0 & 0\\ 0 & \tfrac{1}{\sqrt2} & \tfrac{1}{\sqrt2}\\ 0 & -\tfrac{1}{\sqrt2} & \tfrac{1}{\sqrt2}\end{bmatrix}",
                    color=YELLOW).scale(0.8)
            res.move_to([-5.0, -2.3, 0])
            rows_note = Tx(r"rows $=\hat t_1^T,\ \hat t_2^T,\ \hat t_3^T$", color=REASON).scale(0.55).next_to(res, RIGHT, buff=0.3)
            self.play(Write(res), run_time=2.0)
            self.play(FadeIn(rows_note))
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not hdr])))

        # ---- Example 4: ECI -> ECEF
        th = ValueTracker(0)
        self.add(th)
        O = np.array([-4.3, -1.0, 0])
        with self.voice("v2_36"):
            self.play(Transform(hdr, header("Example 4: a rotating frame (ECI $\\to$ ECEF)")))
            earth = Circle(radius=1.3, color="#7FB3FF", fill_color="#16335C", fill_opacity=1).move_to(O)
            n1 = Arrow(O, O + RIGHT * 2.5, buff=0, color=N_COL)
            n2 = Arrow(O, O + UP * 2.5, buff=0, color=N_COL)
            n1l = T(r"\hat n_1", color=N_COL).scale(0.7).next_to(n1.get_end(), RIGHT, buff=0.1)
            n2l = T(r"\hat n_2", color=N_COL).scale(0.7).next_to(n2.get_end(), UP, buff=0.1)
            e1 = always_redraw(lambda: Arrow(O, O + 2.2 * np.array([np.cos(th.get_value()), np.sin(th.get_value()), 0]), buff=0, color=B_COL, stroke_width=5))
            e2 = always_redraw(lambda: Arrow(O, O + 2.2 * np.array([-np.sin(th.get_value()), np.cos(th.get_value()), 0]), buff=0, color=B_COL, stroke_width=5))
            e1l = always_redraw(lambda: T(r"\hat e_1", color=B_COL).scale(0.7).move_to(O + 2.55 * np.array([np.cos(th.get_value()), np.sin(th.get_value()), 0])))
            e2l = always_redraw(lambda: T(r"\hat e_2", color=B_COL).scale(0.7).move_to(O + 2.55 * np.array([-np.sin(th.get_value()), np.cos(th.get_value()), 0])))
            arc = always_redraw(lambda: Arc(radius=0.6, angle=th.get_value() + 1e-4, arc_center=O, color=YELLOW))
            self.play(FadeIn(earth), GrowArrow(n1), GrowArrow(n2), FadeIn(n1l), FadeIn(n2l))
            self.add(e1, e2, e1l, e2l, arc)
            self.play(th.animate.set_value(0.7875), run_time=3.0)
            bd = Board(self, left=-1.0, top=2.3, scale=0.78)
            bd.line(r"\omega = 7.2921\times10^{-5}\ \text{rad/s}")
            bd.line(r"\text{angle at time } t:\ \ \omega t")
            l = bd.line(r"C_{\mathcal{EN}}(t) = C_3(\omega t)", color=YELLOW)
            self.hold()

        with self.voice("v2_37"):
            bd.line(r"t = 3\ \text{h} = 10800\ \text{s}\ \Rightarrow\ \omega t = 0.7875\ \text{rad} \approx 45.1^\circ")
            bd.line(r"C_3(0.7875) = \begin{bmatrix}0.7056 & 0.7086 & 0\\ -0.7086 & 0.7056 & 0\\ 0&0&1\end{bmatrix}", indent=0.6)
            bd.line(r"s_{(\mathcal E)} = C_3(0.7875)\,s_{(\mathcal N)},\qquad s_{(\mathcal N)} = [\,0.6,\ 0.8,\ 0\,]^T")
            bd.line(r"\text{row 1: } (0.7056)(0.6) + (0.7086)(0.8) = 0.990", indent=0.6)
            bd.line(r"\text{row 2: } (-0.7086)(0.6) + (0.7056)(0.8) = 0.139", indent=0.6)
            bd.line(r"s_{(\mathcal E)} = [\,0.990,\ 0.139,\ 0\,]^T", color=YELLOW, indent=0.6)
            self.hold()
        for m in (e1, e2, e1l, e2l, arc):
            m.clear_updaters()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("v2_38"):
            h, rows = recap(self, [
                r"$C_{\mathcal{BN}}$ is a table of direction cosines: $C_{ij} = \hat b_i\cdot\hat n_j$.",
                r"Its rows are the $\mathcal B$ axes written in $\mathcal N$ components.",
                r"Convert components with $r_{(\mathcal B)} = C_{\mathcal{BN}}\,r_{(\mathcal N)}$.",
                r"$C\,C^T = I$, so $C_{\mathcal{NB}} = C_{\mathcal{BN}}^T$ and $\det C = +1$.",
                r"Only 3 of the 9 entries are independent.",
            ])
            for rrow in rows:
                self.play(FadeIn(rrow, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 5 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
