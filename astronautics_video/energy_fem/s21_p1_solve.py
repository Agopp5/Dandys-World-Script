"""S21: HW P1 solved by substitution (BRIEF.md S21)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# ---- facts: every step on screen, checked against a direct solve of the 3 by 3 system ----
def solve_p1(K1, K2, K3, P1, P2, P3, P4):
    Km = np.array([[2 * K2, -K2, 0], [-K2, K1 + K2 + K3, -K3], [0, -K3, K3]], float)
    return np.linalg.solve(Km, [P1, P2 + P3, P4])

_rng = np.random.default_rng(21)
for _ in range(6):
    K1, K2, K3, P1, P2, P3, P4 = _rng.uniform(1, 9, 7)
    q1, q2, q3 = solve_p1(K1, K2, K3, P1, P2, P3, P4)
    assert np.isclose(K3 * (q3 - q2), P4)                                  # beat 1
    assert np.isclose(-K2 * q1 + (K1 + K2) * q2, P2 + P3 + P4)             # beat 2
    assert np.isclose(K1 * q2 + K2 * (q2 - q1), P2 + P3 + P4)              # beat 3: K1 + second K2 hold the loads
    assert np.isclose(q1, (P1 + K2 * q2) / (2 * K2))                       # beat 4
    assert np.isclose(-K2 * q1, -P1 / 2 - K2 * q2 / 2)                     # beat 5
    assert np.isclose(K1 + K2 - K2 / 2, K1 + K2 / 2)                       # beat 6
    assert np.isclose((K1 + K2 / 2) * q2 - P1 / 2, P2 + P3 + P4)
    assert np.isclose((2 * K1 + K2) * q2 - P1, 2 * (P2 + P3 + P4))         # beat 7
    assert np.isclose(q2, (P1 + 2 * (P2 + P3 + P4)) / (2 * K1 + K2))
    assert np.isclose(q3, q2 + P4 / K3)                                    # beat 8
assert np.allclose(solve_p1(100, 100, 100, 30, 30, 30, 30), [0.5, 0.7, 1.0])

# ---- layout ----
Y1, Y2, Y3 = 2.55, 1.7, 0.85          # the system (top band)
S1, S2, S3 = -0.5, -1.75, -3.0        # working slots (bottom band)
XW = -0.3                             # x of '=' in the working lines


def at_eq(e, i_eq, x, y):
    """Move e so its '=' part (index i_eq) sits at (x, y)."""
    e.shift(np.array([x, y, 0]) - e[i_eq].get_center())
    return e


def fcol(part, spec):
    """Color glyph ranges of an unsplit part (a fraction: numerator glyphs, bar, denominator glyphs)."""
    for (a, b), c in spec:
        for g in part[a:b]:
            g.set_color(c)
    return part


def rbox(m, color=SKY):
    return SurroundingRectangle(m, color=color, buff=.22, corner_radius=.12, stroke_width=4)


def frac_q1(size=48):
    e = E(r"q_1|=|\frac{P_1+K_2 q_2}{2K_2}", size=size)
    fcol(e[2], [((0, 2), ROSE), ((3, 5), LILAC), ((5, 7), SKY), ((9, 11), LILAC)])
    return e


class S21_P1_Solve(VScene):
    budget = 265

    def construct(self):
        self.section("Solving by substitution")

        # the system from S20, '=' signs aligned
        r1 = E(r"2|K_2|q_1|-|K_2|q_2|=|P_1", size=48)
        r2 = E(r"-|K_2|q_1|+|(K_1+K_2+K_3)|\,q_2|-|K_3|q_3|=|P_2|+|P_3", size=48)
        r3 = E(r"-|K_3|q_2|+|K_3|q_3|=|P_4", size=48)
        paint(r2, {4: LILAC})
        x_eq = -5.75 + (r2[9].get_center()[0] - r2.get_left()[0])
        at_eq(r1, 6, x_eq, Y1); at_eq(r2, 9, x_eq, Y2); at_eq(r3, 6, x_eq, Y3)
        chips = VGroup(*[M(t, size=36, color=MUTED).move_to([-6.45, y, 0])
                         for t, y in [("(1)", Y1), ("(2)", Y2), ("(3)", Y3)]])
        sep = Line([-6.8, .3, 0], [6.8, .3, 0], color=HAIR, stroke_width=2)
        self.add(r1, r2, r3, chips, sep)

        # ---- beat 1: the plan; equation 3 regrouped ----
        plan = VGroup(*[VGroup(badge(i + 1), TX(s, size=34)).arrange(RIGHT, buff=.35) for i, s in enumerate([
            r"Use equation (3) to remove $q_3$",
            r"Use equation (1) to remove $q_1$",
            r"One equation is left: solve it for $q_2$"])]).arrange(DOWN, aligned_edge=LEFT, buff=.45)
        plan.move_to([0, -1.75, 0])
        r3b = E(r"K_3|(|q_3|-|q_2|)|=|P_4", size=48)
        at_eq(r3b, 6, x_eq, Y3)
        self.beat("Here's the plan: get rid of q three first, then q one, until one equation is left with q two "
                  "alone. Look at the third equation: K three times q three minus q two equals P four.",
                  LaggedStart(*[FadeIn(p, shift=RIGHT * .3) for p in plan], lag_ratio=.6),
                  Circumscribe(VGroup(r3, chips[2]), color=GOLD),
                  morph(r3, r3b, [(4, 0), (5, 2), (0, 3), (2, 4), (6, 6), (7, 7)]),
                  .2, w=(.45, .12, .23, .2))

        # ---- beat 2: add equations 2 and 3; the K3 terms cancel ----
        ra = E(r"-|K_2|q_1|+|(K_1+K_2)|\,q_2|-|K_3|(|q_3|-|q_2|)|=|P_2|+|P_3", size=48)
        paint(ra, {4: LILAC})
        at_eq(ra, 13, x_eq, S1)
        rb = E(r"+|K_3|(|q_3|-|q_2|)|=|P_4", size=48)
        rb.shift(ra[7].get_left() - rb[1].get_left() + DOWN * (S1 - (-1.35)))
        rb[7].set_x(ra[13].get_x()); rb[8].align_to(ra[14], LEFT)
        rule = Line(ra.get_left() + DOWN * 1.35 + LEFT * .1, ra.get_right() + DOWN * 1.35 + RIGHT * .1,
                    color=INK2, stroke_width=3).set_y(-1.88)
        rc = E(r"-|K_2|q_1|+|(K_1+K_2)|\,q_2|=|P_2|+|P_3|+|P_4", size=48)
        paint(rc, {4: LILAC})
        at_eq(rc, 6, ra[13].get_x(), -2.55)
        s_a = strike(VGroup(*ra[6:13]))
        s_b = strike(VGroup(*rb[0:7]))
        with self.say("Add it to the second equation. The K three terms cancel, and we're left with minus K two q "
                      "one, plus K one plus K two times q two, equals P two plus P three plus P four.") as d:
            r2c = r2.copy()
            self.add(r2c)
            self.play(FadeOut(plan), Indicate(r2, color=GOLD, scale_factor=1.05), run_time=.08 * d)
            self.play(*morph(r2c, ra, [(i, i) for i in range(8)] + [(8, 9), (9, 13), (10, 14), (11, 15), (12, 16)]),
                      run_time=.12 * d)
            self.play(*morph(r3b.copy(), rb, [(i, i + 1) for i in range(8)]), run_time=.12 * d)
            self.play(Create(s_a), Create(s_b), run_time=.14 * d)
            self.play(Create(rule), run_time=.06 * d)
            self.play(*[TransformFromCopy(ra[i], rc[i]) for i in range(6)], run_time=.16 * d)
            self.play(TransformFromCopy(ra[13], rc[6]), *[TransformFromCopy(ra[14 + i], rc[7 + i]) for i in range(3)],
                      FadeIn(rc[10]), TransformFromCopy(rb[8], rc[11]), run_time=.17 * d)
            g_rc = glow(rc, GOLD)
            self.play(FadeIn(g_rc), run_time=.1 * d)
            self.wait(.05 * d)

        # ---- beat 3: the physics: bar + outer node as one free body ----
        yT, yM, yB, xb, xj, xw, xo = -1.0, -1.95, -2.9, .4, -2.55, -5.4, 3.4
        wl = wall(np.array([xw, yM, 0]), side=LEFT, h=3.5)
        barm = Rectangle(width=.3, height=3.1, color=INK2, fill_color=SURFACE, fill_opacity=1,
                         stroke_width=3).move_to([xb, yM, 0])
        k1 = spring(np.array([xw, yT, 0]), np.array([xb - .15, yT, 0]), coils=6, amp=.22)
        k2a = spring(np.array([xw, yB, 0]), np.array([xj, yB, 0]), coils=4, amp=.22)
        k2b = spring(np.array([xj, yB, 0]), np.array([xb - .15, yB, 0]), coils=4, amp=.22)
        k3 = spring(np.array([xb + .15, yM, 0]), np.array([xo, yM, 0]), coils=4, amp=.22)
        lk1 = M("K_1", size=40, color=LILAC).next_to(k1, UP, buff=.12)
        lk2a = M("K_2", size=40, color=LILAC).next_to(k2a, DOWN, buff=.12)
        lk2b = M("K_2", size=40, color=LILAC).next_to(k2b, DOWN, buff=.12)
        lk3 = M("K_3", size=40, color=LILAC).next_to(k3, UP, buff=.12)
        nj, no = node(np.array([xj, yB, 0]), r=.11), node(np.array([xo, yM, 0]), r=.11)
        stem = Line([xj, yB, 0], [xj, yB + .55, 0], color=MUTED, stroke_width=3)
        f1 = force(np.array([xj, yB + .55, 0]), RIGHT, length=.9, label="P_1", size=38)
        f2 = force(np.array([xb + .15, -.65, 0]), RIGHT, length=1.1, label="P_2", size=38)
        f3 = force(np.array([xb + .15, -3.3, 0]), RIGHT, length=1.1, label="P_3", size=38)
        f4 = force(np.array([xo, yM, 0]), RIGHT, length=1.1, label="P_4", size=38)
        sketch = VGroup(wl, k1, k2a, k2b, k3, lk1, lk2a, lk2b, lk3, barm, nj, no, stem, f1, f2, f3, f4)
        fb = DashedVMobject(Rectangle(width=6.35, height=3.65).move_to([2.8, -1.95, 0]), num_dashes=70)
        fb.set_stroke(GOLD, 3)
        cut = VGroup(k1, lk1, k2b, lk2b)
        with self.say("That makes sense physically. It's the force balance of the bar together with the outer "
                      "point: the two springs on the bar's left side, K one and the second K two, hold P two, P "
                      "three and P four together.") as d:
            self.play(FadeOut(VGroup(ra, rb, rule, s_a, s_b, r2, r2c, g_rc)),
                      rc.animate.shift(np.array([x_eq, Y2, 0]) - rc[6].get_center()),
                      r3b.animate.set_opacity(.35), chips[2].animate.set_opacity(.35), run_time=.14 * d)
            self.play(FadeIn(sketch, lag_ratio=.05), run_time=.2 * d)
            self.play(Create(fb), run_time=.12 * d)
            self.play(Indicate(VGroup(f2, f3, f4), color=ROSE, scale_factor=1.08), run_time=.14 * d)
            gk = VGroup(glow(k1, LILAC), glow(k2b, LILAC))
            self.play(FadeIn(gk), Indicate(lk1), Indicate(lk2b),
                      Indicate(rc[4], color=LILAC), run_time=.18 * d)
            self.play(Circumscribe(VGroup(*rc[7:12]), color=ROSE), run_time=.14 * d)
            self.wait(.08 * d)
