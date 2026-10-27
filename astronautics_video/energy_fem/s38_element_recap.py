"""S38: one element, completely (BRIEF.md S38)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

EXTRA = {r"\Pi_e": GOLD, "u^{T}": SKY, "Q": ROSE}

# facts: everything this scene states, checked on random numbers
_rng = np.random.default_rng(38)
for _ in range(5):
    EA, l, c = _rng.uniform(1, 9, 3)
    u1, u2 = _rng.uniform(-2, 2, 2)
    uv = np.array([u1, u2])
    k = EA / l * np.array([[1, -1], [-1, 1]])
    # shape functions: u(s) = (1-s) u1 + s u2 hits u1 at s=0 and u2 at s=1, N1 + N2 = 1
    assert np.isclose((1 - 0) * u1 + 0 * u2, u1) and np.isclose((1 - 1) * u1 + 1 * u2, u2)
    # element energy: (1/2) EA/l (u2-u1)^2 = (1/2) u^T k u  (a spring with K = EA/l)
    s = np.linspace(0, 1, 2001)
    Ue_int = 0.5 * np.trapezoid(EA * ((u2 - u1) / l) ** 2 * l * np.ones_like(s), s)
    assert np.isclose(Ue_int, 0.5 * uv @ k @ uv)
    assert np.allclose(k.sum(axis=1), 0)
    # uniform load f = c: Q1 = Q2 = c l / 2
    Q1 = np.trapezoid(c * (1 - s) * l, s)
    Q2 = np.trapezoid(c * s * l, s)
    assert np.isclose(Q1, c * l / 2) and np.isclose(Q2, c * l / 2)
    Q = np.array([Q1, Q2])
    # d Pi_e / d u_i = (k u - Q)_i, so stationarity gives k u = Q
    Pi = lambda v: 0.5 * v @ k @ v - v @ Q
    h = 1e-6
    grad = np.array([(Pi(uv + h * e) - Pi(uv - h * e)) / (2 * h) for e in np.eye(2)])
    assert np.allclose(grad, k @ uv - Q, atol=1e-5)

X1, X2, YB = -5.6, -1.2, -1.0          # node positions and bar axis (left half of the frame)
RX = 3.7                               # centre of the right-hand column


class S38_Element_Recap(VScene):
    budget = 105

    def construct(self):
        p1, p2 = np.array([X1, YB, 0]), np.array([X2, YB, 0])

        # ---- beat 1: the element, u a straight line between its nodes
        rod = bar(X1, X2, y=YB, h=0.5)
        n1, n2 = node(p1, r=0.11), node(p2, r=0.11)
        top = YB + 0.25
        h1, h2 = 0.55, 2.45
        a1, a2 = np.array([X1, top + h1, 0]), np.array([X2, top + h2, 0])
        uline = Line(a1, a2, color=SKY, stroke_width=7)
        d1 = DashedLine(np.array([X1, top, 0]), a1, color=SKY, stroke_width=3)
        d2 = DashedLine(np.array([X2, top, 0]), a2, color=SKY, stroke_width=3)
        e1, e2 = Dot(a1, color=SKY, radius=0.1), Dot(a2, color=SKY, radius=0.1)
        lu1 = M("u_1", size=44, color=SKY).next_to(a1, UP, buff=0.2)
        lu2 = M("u_2", size=44, color=SKY).next_to(a2, UP, buff=0.2)
        lus = E(r"u|(|s|)", size=44).move_to(uline.get_center() + np.array([-0.55, 0.65, 0]))
        s0 = M("s=0", size=38, color=LIME).next_to(p1, DOWN, buff=0.5)
        s1 = M("s=1", size=38, color=LIME).next_to(p2, DOWN, buff=0.5)
        ys = YB - 2.0
        dim = DoubleArrow(np.array([X1, ys, 0]), np.array([X2, ys, 0]), buff=0, color=INK2,
                          stroke_width=3, tip_length=0.22)
        ll = M("l", size=44, color=INK).next_to(dim, DOWN, buff=0.15)
        plot = VGroup(d1, d2, uline, e1, e2, lu1, lu2, lus)

        eq_u = E(r"u|(|s|)|=|(1-|s|)|u_1|+|s|u_2", size=50).move_to([RX, 2.1, 0])
        fit(eq_u, 6.4, 1.2)

        self.beat("So, stepping back. An element is a short piece of bar whose displacement is a straight line between its two nodes.",
                  [FadeIn(rod), FadeIn(n1), FadeIn(n2), FadeIn(dim), FadeIn(ll)],
                  [FadeIn(s0), FadeIn(s1)],
                  [Create(d1), Create(d2), FadeIn(e1), FadeIn(e2), FadeIn(lu1), FadeIn(lu2)],
                  [Create(uline), FadeIn(lus)],
                  Write(eq_u), .15,
                  w=(.18, .1, .2, .2, .2))

        # ---- beat 2: the element is a spring; spread load -> two nodal forces
        spr = spring(p1, p2, coils=6, amp=0.32)
        lk = E(r"k|=|\frac{EA}{l}", size=44).move_to([(X1 + X2) / 2, YB + 1.25, 0])
        nd = 7
        xs = np.linspace(X1 + 0.3, X2 - 0.75, nd)
        spread = VGroup(*[Arrow(np.array([x, YB + 0.62, 0]), np.array([x + 0.48, YB + 0.62, 0]), buff=0,
                                color=ROSE, stroke_width=5, max_tip_length_to_length_ratio=0.4) for x in xs])
        lc = M("f = c", size=40, color=ROSE).next_to(spread, UP, buff=0.12)
        fL = Arrow(p1 + LEFT * 1.25, p1, buff=0, color=ROSE, stroke_width=7)
        fR = Arrow(p2, p2 + RIGHT * 1.25, buff=0, color=ROSE, stroke_width=7)
        lfL = M(r"\frac{cl}{2}", size=42, color=ROSE).next_to(fL, UP, buff=0.15)
        lfR = M(r"\frac{cl}{2}", size=42, color=ROSE).next_to(fR, UP, buff=0.15)

        eq_k = E(r"k|=|\frac{EA}{l}", size=50).move_to([RX, 0.4, 0])
        eq_Q = E(r"Q_1|=|Q_2|=|\frac{cl}{2}", size=50, cmap=EXTRA).move_to([RX, -1.4, 0])

        self.beat("Its stiffness is E A over l, exactly a spring. And a uniform spread load becomes two equal forces, c l over two, one at each node.",
                  [FadeOut(plot), FadeOut(s0), FadeOut(s1), ReplacementTransform(rod, spr)],
                  [FadeIn(lk), FadeIn(eq_k)], .08,
                  [LaggedStart(*[GrowArrow(a) for a in spread], lag_ratio=0.1), FadeIn(lc)],
                  [ReplacementTransform(VGroup(*spread[:nd // 2 + 1]), fL),
                   ReplacementTransform(VGroup(*spread[nd // 2 + 1:]), fR), FadeOut(lc)],
                  [FadeIn(lfL), FadeIn(lfR), FadeIn(eq_Q)], .15,
                  w=(.17, .15, .18, .17, .15))
        n1.set_z_index(3)
        n2.set_z_index(3)

        # ---- beat 3: element energy and its spring equation
        eq_pi = E(r"\Pi_e|=|\frac12|u^{T}|k|u|-|u^{T}|Q", size=52, cmap=EXTRA).move_to([RX, 1.6, 0])
        fit(eq_pi, 6.4, 1.4)
        eq_kq = E(r"k|u|=|Q", size=60, cmap=EXTRA).move_to([RX, -0.3, 0])
        note = T("one element alone", size=32, color=MUTED).next_to(eq_kq, DOWN, buff=0.45)
        with self.say("Its energy is one half u k u, minus u Q. Take a derivative for each end, and you'd get k times u equals Q: a spring equation, for one element. Next time, we join elements together, add up their energies, apply the supports, and solve a real problem.") as d:
            self.play(FadeOut(eq_u), FadeOut(eq_k), FadeOut(eq_Q), run_time=.05 * d)
            self.play(Write(eq_pi), run_time=.14 * d)
            self.wait(.04 * d)
            self.play(Indicate(n1, scale_factor=1.8, color=GOLD), Indicate(n2, scale_factor=1.8, color=GOLD),
                      run_time=.1 * d)
            self.play(TransformFromCopy(eq_pi[4], eq_kq[0]), TransformFromCopy(eq_pi[5], eq_kq[1]),
                      FadeIn(eq_kq[2]), TransformFromCopy(eq_pi[8], eq_kq[3]), run_time=.14 * d)
            halo = glow(eq_kq, LILAC)
            self.play(FadeIn(halo), FadeIn(note), run_time=.08 * d)
            self.wait(.1 * d)
            self.play(Circumscribe(note, color=MUTED), run_time=.15 * d)
            self.wait(.2 * d)

        # ---- beat 4: the summary card
        box = key_box(E(r"u|(|s|)|=|(1-|s|)|u_1|+|s|u_2", size=46),
                      E(r"k|=|\frac{EA}{l}|\begin{bmatrix}1&-1\\-1&1\end{bmatrix}", size=46),
                      E(r"Q_1|=|Q_2|=|\frac{cl}{2}|\quad (f = c)", size=46, cmap=EXTRA),
                      label="ONE ELEMENT")
        fit(box, 12.5, 7.0)
        box.move_to(ORIGIN + DOWN * 0.1)
        self.beat("Here's everything about one element in one place.",
                  [FadeOut(VGroup(spr, n1, n2, dim, ll, lk, fL, fR, lfL, lfR, eq_pi, eq_kq, halo, note))], FadeIn(box, shift=UP * 0.2), .4,
                  w=(.15, .3))
        self.wipe()
