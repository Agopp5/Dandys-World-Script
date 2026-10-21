"""S09: the direction cosine matrix C_PN (BRIEF.md S09)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# facts ---------------------------------------------------------------------------------------------
OM, INC, W = np.radians(50), np.radians(40), np.radians(60)      # generic orientation, episode 2
CG = cpn(OM, INC, W)
P_HAT, Q_HAT, H_HAT = CG[0], CG[1], CG[2]
I_HAT, J_HAT, K_HAT = np.eye(3)
assert np.allclose(CG, C3(W) @ C1(INC) @ C3(OM))
assert np.allclose(CG @ CG.T, np.eye(3))                          # rows are orthonormal unit vectors
assert np.isclose(np.linalg.det(CG), 1.0)
assert np.allclose(np.cross(P_HAT, Q_HAT), H_HAT)                 # right-handed triad
# each entry is a dot product = direction cosine
for r_, v_ in enumerate((P_HAT, Q_HAT, H_HAT)):
    for c_, a_ in enumerate((I_HAT, J_HAT, K_HAT)):
        assert np.isclose(CG[r_, c_], v_ @ a_)
ALPHA = np.arccos(P_HAT @ I_HAT)                                  # angle between p-hat and I
assert 0 < ALPHA < np.pi
# the course's elementary rotations (rows = new axes in old)
x_ = .7
assert np.allclose(C3(x_), [[np.cos(x_), np.sin(x_), 0], [-np.sin(x_), np.cos(x_), 0], [0, 0, 1]])
assert np.allclose(C1(x_), [[1, 0, 0], [0, np.cos(x_), np.sin(x_)], [0, -np.sin(x_), np.cos(x_)]])
assert np.allclose(C3(x_) @ K_HAT, K_HAT) and np.allclose(C1(x_) @ I_HAT, I_HAT)   # the turn axis stays put
N_HAT = np.array([np.cos(OM), np.sin(OM), 0.0])                   # node line, Omega from I about K
assert np.isclose(N_HAT @ H_HAT, 0)
assert np.isclose(np.degrees(np.arccos(H_HAT @ K_HAT)), 40)       # tilt i about the node line

XR = 3.75                      # right-column center


class S09_DCM(VScene):
    budget = 145

    def construct(self):
        view = View(elev=22, azim=-110, scale=.95, center=(-3.6, -0.2))
        earth = globe(view)
        ax = axes3(view, 2.3)
        orb = curve(view, orbit(2.4, .5, OM, INC, W), 0, 2 * PI, INK, width=3, R=1.0)
        L = 2.0
        pa = arrow3(view, ORIGIN, L * P_HAT, ROSE)
        qa = arrow3(view, ORIGIN, L * Q_HAT, LIME)
        ha = arrow3(view, ORIGIN, L * H_HAT, LILAC)
        pl = label3(view, r"\hat p", (L + .3) * P_HAT, ROSE, 34)
        ql = label3(view, r"\hat q", (L + .3) * Q_HAT, LIME, 34)
        hl = label3(view, r"\hat h", (L + .3) * H_HAT, LILAC, 34)
        triad = VGroup(pa, qa, ha, pl, ql, hl)
        for a in (pa, qa, ha):
            a.k.set_value(0)

        # the matrix: rows are p-hat, q-hat, h-hat in I, J, K components
        vecs = [r"\hat p", r"\hat q", r"\hat h"]
        axs = [r"\hat I", r"\hat J", r"\hat K"]
        ents = [[E(v + r"|\cdot|" + a, size=40) for a in axs] for v in vecs]
        mat = MobjectMatrix(ents, h_buff=1.75, v_buff=.85)
        lhs = E(r"C_{PN}|=", size=40)
        tags = VGroup(*[E(r"\leftarrow|" + v, size=40) for v in vecs])
        mblock = VGroup(lhs, mat).arrange(RIGHT, buff=.2)
        for t, row in zip(tags, mat.get_rows()):
            t.next_to(mat, RIGHT, buff=.2).set_y(row.get_y())
        mgroup = VGroup(mblock, tags)
        fit(mgroup, 6.2, 3.2)
        mgroup.move_to([XR, .9, 0])
        rows = mat.get_rows()

        with self.say("That's exactly what a direction cosine matrix stores. Write p hat, q hat and h hat in their I, J, K components, and stack them as rows. That stack is C P N.") as d:
            gl = glow(lhs[0], ACCENT)
            self.play(FadeIn(earth), FadeIn(ax), Create(orb), run_time=.12 * d)
            self.add(pa, qa, ha)
            self.play(pa.k.animate.set_value(1), qa.k.animate.set_value(1), ha.k.animate.set_value(1),
                      FadeIn(VGroup(pl, ql, hl)), run_time=.12 * d)
            self.play(FadeIn(lhs), FadeIn(mat.get_brackets()), run_time=.08 * d)
            for row, tag, arr in zip(rows, tags, (pa, qa, ha)):
                self.play(FadeIn(row, shift=.2 * RIGHT), FadeIn(tag), Indicate(arr, scale_factor=1.0),
                          run_time=.15 * d)
            self.wait(.06 * d)
            self.play(Circumscribe(mgroup, color=ACCENT), FadeIn(gl), run_time=.12 * d)
            self.wait(.05 * d)

        # beat 2: one entry is a cosine
        e00 = ents[0][0]
        box = SurroundingRectangle(e00, color=ACCENT, buff=.08)
        cosl = E(r"\hat p|\cdot|\hat I|=|\cos\alpha", size=40)
        cosl[4].set_color(ACCENT)
        val = M(r"\cos\alpha = %.3f" % (P_HAT @ I_HAT), size=32, color=MUTED)
        VGroup(cosl, val).arrange(DOWN, buff=.25).move_to([XR, -1.75, 0])
        axis = np.cross(I_HAT, P_HAT)
        axis = axis / np.linalg.norm(axis)
        arc = arc3(view, axis, I_HAT, ALPHA, 1.35, ACCENT)
        arc.k.set_value(0)
        self.add(arc)
        mid = np.cos(ALPHA / 2) * I_HAT + np.sin(ALPHA / 2) * np.cross(axis, I_HAT)
        al = label3(view, r"\alpha", 1.65 * mid, ACCENT, 34)
        others = VGroup(qa, ha, ql, hl, orb)
        self.beat("Each entry is a dot product, the cosine of the angle between one perifocal axis and one E C I axis.",
                  Create(box), [FadeOut(others), Indicate(ax[0], color=ACCENT)],
                  [arc.k.animate.set_value(1), FadeIn(al)], Write(cosl), FadeIn(val), w=(.12, .2, .25, .28, .15))

        # beat 3: three turns, three badges
        self.play(FadeOut(VGroup(mgroup, gl, box, cosl, val, arc, al)), FadeIn(others), run_time=.8)
        node = line3(view, -2.2 * N_HAT, 2.2 * N_HAT, SKY, dashed=True)
        specs = [(1, r"\Omega", SKY, "about K"), (2, "i", EMBER, "about the node line"),
                 (3, r"\omega", MINT, r"about h")]
        brows = VGroup()
        for n, sym, col, words in specs:
            b = badge(n)
            s = E(sym, size=44)
            head = VGroup(b, s).arrange(RIGHT, buff=.2)
            brows.add(VGroup(head, T(words, 28, color=INK2)).arrange(RIGHT, buff=.35))
        brows.arrange(DOWN, buff=.45, aligned_edge=LEFT).move_to([XR, .3, 0])
        k_arrow = ax[2] if len(ax) > 2 else ax
        with self.say("Because we built the orientation with three turns, Omega about K, then i about the node line, then omega about h, the matrix is a product of three simple rotations.") as d:
            self.wait(.08 * d)
            self.play(FadeIn(brows[0], shift=.2 * UP), Indicate(k_arrow, color=SKY), run_time=.17 * d)
            self.play(FadeIn(brows[1], shift=.2 * UP), Create(node), run_time=.17 * d)
            self.play(FadeIn(brows[2], shift=.2 * UP), Indicate(ha, color=LILAC), Indicate(hl), run_time=.17 * d)
            self.wait(.13 * d)
            self.play(Circumscribe(brows, color=ACCENT), run_time=.2 * d)
            self.wait(.08 * d)

        # beat 4: the product, read right to left
        prod = E(r"C_{PN}|=|C_3(|\omega|)\,|C_1(|i|)\,|C_3(|\Omega|)", size=46)
        fit(prod, 6.0, 1.0)
        prod.move_to([XR, 2.6, 0])
        fac = [VGroup(prod[2], prod[3], prod[4]), VGroup(prod[5], prod[6], prod[7]), VGroup(prod[8], prod[9], prod[10])]
        heads = [brows[k][0] for k in range(3)]
        words = VGroup(*[brows[k][1] for k in range(3)])
        targets = {2: fac[0], 1: fac[1], 0: fac[2]}       # badge 1 (Omega) sits under the rightmost factor
        moves = [heads[k].animate.next_to(targets[k], DOWN, buff=.25) for k in range(3)]
        rl = Arrow(fac[2].get_right() + 1.25 * DOWN, fac[0].get_left() + 1.25 * DOWN, buff=0, color=MUTED,
                   stroke_width=4, max_tip_length_to_length_ratio=.08)
        rl_lab = T("read right to left", 26, color=MUTED).next_to(rl, DOWN, buff=.12)
        with self.say("C P N equals C three of little omega, times C one of i, times C three of capital Omega. Read it right to left: first the Omega turn, then the tilt, then the spin in the plane.") as d:
            self.play(FadeOut(words), Write(prod), run_time=.3 * d)
            self.play(*moves, run_time=.14 * d)
            self.play(GrowArrow(rl), FadeIn(rl_lab), run_time=.1 * d)
            self.play(Indicate(fac[2], color=SKY), Indicate(heads[0]), run_time=.14 * d)
            self.play(Indicate(fac[1], color=EMBER), Indicate(heads[1]), Indicate(node, color=EMBER), run_time=.14 * d)
            self.play(Indicate(fac[0], color=MINT), Indicate(heads[2]), run_time=.14 * d)
            self.wait(.04 * d)

        # beat 5: the elementary rotations written out
        c3m = E(r"C_3(x)|=|\begin{bmatrix} \cos x & \sin x & 0\\ -\sin x & \cos x & 0\\ 0 & 0 & 1 \end{bmatrix}", size=34)
        c1m = E(r"C_1(x)|=|\begin{bmatrix} 1 & 0 & 0\\ 0 & \cos x & \sin x\\ 0 & -\sin x & \cos x \end{bmatrix}", size=34)
        mats = VGroup(c3m, c1m).arrange(DOWN, buff=.35, aligned_edge=LEFT)
        fit(mats, 5.6, 3.4)
        mats.move_to([XR, -1.95, 0])
        with self.say("These are the same elementary rotations from the kinematics lessons. C three turns about the third axis. C one turns about the first.") as d:
            self.play(FadeOut(rl_lab), run_time=.04 * d)
            self.play(Write(c3m), run_time=.2 * d)
            self.play(Write(c1m), run_time=.2 * d)
            self.wait(.06 * d)
            self.play(Circumscribe(c3m[2], color=ACCENT), Indicate(k_arrow, color=ACCENT), run_time=.22 * d)
            self.play(Circumscribe(c1m[2], color=ACCENT), Indicate(ax[0], color=ACCENT), run_time=.22 * d)
            self.wait(.06 * d)
        self.wipe()
