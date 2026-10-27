"""S20: the stiffness matrix of HW P1 (BRIEF.md S20)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the matrix is the Hessian of U (quadratic, so central differences are exact up to rounding)
_rng = np.random.default_rng(3)
for _ in range(5):
    K1, K2, K3 = _rng.uniform(10, 200, 3)

    def _U(q):
        q1, q2, q3 = q
        return .5 * K1 * q2**2 + .5 * K2 * q1**2 + .5 * K2 * (q2 - q1)**2 + .5 * K3 * (q3 - q2)**2

    H = np.zeros((3, 3))
    h = 1e-3
    I3 = np.eye(3)
    for i in range(3):
        for j in range(3):
            H[i, j] = (_U(h * I3[i] + h * I3[j]) - _U(h * I3[i] - h * I3[j])
                       - _U(-h * I3[i] + h * I3[j]) + _U(-h * I3[i] - h * I3[j])) / (4 * h * h)
    Kmat = np.array([[2 * K2, -K2, 0], [-K2, K1 + K2 + K3, -K3], [0, -K3, K3]])
    assert np.allclose(H, Kmat, rtol=1e-6, atol=1e-6)
    assert np.allclose(Kmat, Kmat.T)
# sanity numbers (all K = 100, all P = 30): q = (0.5, 0.7, 1.0) solves it
_K = np.array([[200, -100, 0], [-100, 300, -100], [0, -100, 100]])
assert np.allclose(_K @ np.array([.5, .7, 1.0]), [30, 60, 30])


def _figure():
    w = wall(ORIGIN, side=LEFT, h=2.4)
    s1 = spring(np.array([0, .7, 0]), np.array([2.6, .7, 0]), label="K_1")
    s2a = spring(np.array([0, -.7, 0]), np.array([1.3, -.7, 0]), coils=3, label="K_2")
    s2b = spring(np.array([1.3, -.7, 0]), np.array([2.6, -.7, 0]), coils=3, label="K_2")
    jn = node(np.array([1.3, -.7, 0]))
    rod = Rectangle(width=.2, height=2.2).move_to([2.7, 0, 0])
    rod.set_fill(SURFACE, 1).set_stroke(INK2, 2)
    s3 = spring(np.array([2.8, 0, 0]), np.array([4.2, 0, 0]), coils=3, label="K_3")
    n3 = node(np.array([4.2, 0, 0]))
    f1 = force(np.array([1.3, -1.15, 0]), RIGHT, length=.7, label="P_1")
    f2 = force(np.array([2.8, .9, 0]), RIGHT, length=.7, label="P_2")
    f3 = force(np.array([2.8, -.9, 0]), RIGHT, length=.7, label="P_3")
    f4 = force(np.array([4.2, 0, 0]), RIGHT, length=.7, label="P_4")
    fig = VGroup(w, s1, s2a, s2b, rod, s3, jn, n3, f1, f2, f3, f4)
    return fig, (s1, s2a, s2b, s3)


def _ent(s):
    return E(s, size=44)


class S20_P1_Matrix(VScene):
    budget = 73

    def construct(self):
        fig, (s1, s2a, s2b, s3) = _figure()
        fig.scale(.95).to_corner(UL, buff=.35)

        Kmx = Matrix([["2|K_2", "-|K_2", "0"],
                      ["-|K_2", "K_1|+|K_2|+|K_3", "-|K_3"],
                      ["0", "-|K_3", "K_3"]],
                     element_to_mobject=_ent, h_buff=3.3, v_buff=1.0)
        qv = Matrix([["q_1"], ["q_2"], ["q_3"]], element_to_mobject=_ent, v_buff=1.0,
                    left_bracket="\\{", right_bracket="\\}")
        Fv = Matrix([["P_1"], ["P_2|+|P_3"], ["P_4"]], element_to_mobject=_ent, v_buff=1.0,
                    left_bracket="\\{", right_bracket="\\}")
        eqs = M("=", size=48)
        eqn = VGroup(Kmx, qv, eqs, Fv).arrange(RIGHT, buff=.3)
        fit(eqn, 13, 3.6)
        eqn.move_to(DOWN * 1.5)
        ent = Kmx.get_entries()

        self.beat("Stack the three equations as a matrix.",
                  FadeIn(fig), Write(eqn), w=(.3, .7))

        # pattern card, top right
        pat = VGroup(M(r"\begin{bmatrix} +k & -k \\ -k & +k \end{bmatrix}", size=40),
                     T("spring between free nodes", size=30, color=INK2)).arrange(DOWN, buff=.2)
        card = panel(pat)
        card.to_corner(UR, buff=.35)
        pat2 = VGroup(M(r"+k", size=40, color=LILAC),
                      T("wall spring: one diagonal", size=30, color=INK2)).arrange(DOWN, buff=.25)
        pat2.move_to(card[1])
        paint(pat[0], {0: LILAC})

        def boxes(mobs):
            return VGroup(*[SurroundingRectangle(m, buff=.1, color=LILAC, stroke_width=3)
                            .set_fill(LILAC, .22) for m in mobs])

        groups = [
            (s2b, [ent[0], ent[1], ent[3], ent[4][2]]),
            (s3, [ent[4][4], ent[5], ent[7], ent[8]]),
            (s1, [ent[4][0]]),
            (s2a, [ent[0]]),
        ]
        with self.say("Check it against the pattern from last episode. Each spring adds plus k on the diagonal "
                      "of each free node it touches, and minus k between them. Springs tied to the wall only add "
                      "to one diagonal, because the wall's row and column are left out.") as d:
            self.play(FadeIn(card), run_time=.12 * d)
            self.wait(.04 * d)
            for n, (sp, mobs) in enumerate(groups):
                if n == 2:
                    self.play(FadeOut(pat), FadeIn(pat2), run_time=.05 * d)
                bx = boxes(mobs)
                g = glow(sp, LILAC)
                self.play(FadeIn(bx), FadeIn(g), run_time=.07 * d)
                self.snap("spring %d" % n)
                self.wait((.08 if n < 2 else .05) * d)
                self.play(FadeOut(bx), FadeOut(g), run_time=.03 * d)
            self.wait(.02 * d)

        mirror = DashedLine(ent[0].get_center() + (ent[0].get_center() - ent[8].get_center()) * .06,
                            ent[8].get_center() + (ent[8].get_center() - ent[0].get_center()) * .06,
                            color=INK2, stroke_width=4)
        sym = E(r"K|=|K^{T}", size=48).move_to(card)
        paint(sym, {2: LILAC})
        self.beat("And it's symmetric: each spring puts the same minus k in both of its off-diagonal spots. "
                  "Now let's solve it.",
                  [FadeOut(pat2), FadeOut(card), Create(mirror)],
                  [Indicate(ent[1], color=LILAC), Indicate(ent[3], color=LILAC)],
                  [Indicate(ent[5], color=LILAC), Indicate(ent[7], color=LILAC)],
                  FadeIn(sym), .2, w=(.25, .2, .2, .15))
        self.wipe()
