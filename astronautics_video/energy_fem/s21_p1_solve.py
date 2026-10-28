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
        r2 = E(r"-|K_2|q_1|+|(K_1+K_2+K_3)|q_2|-|K_3|q_3|=|P_2|+|P_3", size=48)
        r3 = E(r"-|K_3|q_2|+|K_3|q_3|=|P_4", size=48)
        paint(r2, {4: LILAC})
        x_eq = -5.75 + (r2[9].get_center()[0] - r2.get_left()[0])
        at_eq(r1, 6, x_eq, Y1); at_eq(r2, 9, x_eq, Y2); at_eq(r3, 6, x_eq, Y3)
        chips = VGroup(*[M(t, size=36, color=MUTED).move_to([-6.45, y, 0])
                         for t, y in [("(1)", Y1), ("(2)", Y2), ("(3)", Y3)]])
        sep = Line([-6.8, .3, 0], [6.8, .3, 0], color=HAIR, stroke_width=2)
        self.add(r1, r2, r3, chips, sep)

        # ---- beat 1: the plan; equation 3 regrouped ----
        plan = VGroup(*[VGroup(badge(i + 1), TX(s, size=40)).arrange(RIGHT, buff=.35) for i, s in enumerate([
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
                  .2, w=(.45, .12, .23))

        # ---- beat 2: add equations 2 and 3; the K3 terms cancel ----
        ra = E(r"-|K_2|q_1|+|(K_1+K_2)|q_2|-|K_3|(|q_3|-|q_2|)|=|P_2|+|P_3", size=48)
        paint(ra, {4: LILAC})
        at_eq(ra, 13, x_eq, S1)
        rb = E(r"+|K_3|(|q_3|-|q_2|)|=|P_4", size=48)
        rb.shift(ra[7].get_left() - rb[1].get_left() + DOWN * (S1 - (-1.35)))
        rb[7].set_x(ra[13].get_x()); rb[8].align_to(ra[14], LEFT)
        rule = Line(ra.get_left() + DOWN * 1.35 + LEFT * .1, ra.get_right() + DOWN * 1.35 + RIGHT * .1,
                    color=INK2, stroke_width=3).set_y(-1.88)
        rc = E(r"-|K_2|q_1|+|(K_1+K_2)|q_2|=|P_2|+|P_3|+|P_4", size=48)
        paint(rc, {4: LILAC})
        at_eq(rc, 6, ra[13].get_x(), -2.55)
        s_a = strike(VGroup(*ra[6:13]))
        s_b = strike(VGroup(*rb[0:7]))
        with self.say("Add it to the second equation. The K three terms cancel, and we're left with minus K two q "
                      "one, plus K one plus K two times q two, equals P two plus P three plus P four.") as d:
            self.play(FadeOut(plan), Indicate(r2, color=GOLD, scale_factor=1.05), run_time=.08 * d)
            self.play(*morph(r2, ra, [(i, i) for i in range(8)] + [(8, 9), (9, 13), (10, 14), (11, 15), (12, 16)]),
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
        sketch = hw_figure(k2b_label=True)            # the shared HW 6 P1 figure (same as S16-S22)
        sketch.scale(.85).move_to([0, -1.85, 0])
        k1, k2b, lk1, lk2b = sketch.k1, sketch.k2b, sketch.klab["K1"], sketch.klab["K2b"]
        body = VGroup(sketch.bar, sketch.O, sketch.k3, sketch.klab["K3"],
                      *[sketch.P[i] for i in (2, 3, 4)], *[sketch.Plab[i] for i in (2, 3, 4)])
        fb = DashedVMobject(SurroundingRectangle(body, buff=.15), num_dashes=80).set_stroke(INK2, 3)
        loads = VGroup(*[sketch.P[i] for i in (2, 3, 4)], *[sketch.Plab[i] for i in (2, 3, 4)])
        with self.say("That makes sense physically. It's the force balance of the bar together with the outer "
                      "point: the two springs on the bar's left side, K one and the second K two, hold P two, P "
                      "three and P four together.") as d:
            self.play(FadeOut(VGroup(ra, rb, rule, s_a, s_b, g_rc)),
                      rc.animate.shift(np.array([x_eq, Y2, 0]) - rc[6].get_center()),
                      r3b.animate.set_opacity(.35), chips[2].animate.set_opacity(.35), run_time=.14 * d)
            self.play(FadeIn(sketch, lag_ratio=.05), run_time=.2 * d)
            self.play(Create(fb), run_time=.12 * d)
            self.play(Indicate(loads, color=ROSE, scale_factor=1.08), run_time=.14 * d)
            gk = VGroup(glow(k1, LILAC), glow(k2b, LILAC))
            self.play(FadeIn(gk), Indicate(lk1), Indicate(lk2b),
                      Indicate(rc[4], color=LILAC), run_time=.18 * d)
            self.play(Circumscribe(VGroup(*rc[7:12]), color=ROSE), run_time=.14 * d)
            self.wait(.08 * d)

        # ---- beat 4: q1 from equation 1 ----
        qa = frac_q1()
        at_eq(qa, 1, XW, S1)
        self.beat("From the first equation, q one equals P one plus K two q two, all over two K two.",
                  [FadeOut(VGroup(sketch, fb, gk)), Circumscribe(VGroup(r1, chips[0]), color=GOLD)],
                  [TransformFromCopy(r1[2], qa[0]), Write(qa[1:])], .3, w=(.3, .4))

        # ---- beat 5: substitute into the new second equation ----
        qb = E(r"-|K_2|q_1|=|-\tfrac12|P_1|-|\tfrac12|K_2|q_2", size=48)
        at_eq(qb, 3, XW, S2)
        self.beat("Substitute. Minus K two times q one is minus one half P one, minus one half K two q two.",
                  Indicate(VGroup(*rc[0:3]), color=GOLD),
                  [*[TransformFromCopy(rc[i], qb[i]) for i in range(3)], FadeIn(qb[3])],
                  Write(VGroup(*qb[4:])), .25, w=(.15, .25, .35))

        # ---- beat 6: collect the q2 terms ----
        qc = E(r"(K_1+K_2|-\tfrac12 K_2)|q_2|=|(K_1+\tfrac12 K_2)|q_2", size=48)
        paint(qc, {0: LILAC, 1: LILAC, 4: LILAC})
        at_eq(qc, 3, XW, S2)
        qd = E(r"(K_1+\tfrac12 K_2)|q_2|-|\tfrac12|P_1|=|P_2|+|P_3|+|P_4", size=48)
        paint(qd, {0: LILAC})
        at_eq(qd, 5, XW, S3)
        with self.say("So the q two terms are K one plus K two, minus one half K two, which is K one plus one half "
                      "K two. The equation becomes: K one plus one half K two, times q two, minus one half P one, "
                      "equals P two plus P three plus P four.") as d:
            self.play(FadeOut(qa), qb.animate.shift(UP * (S1 - S2)), run_time=.1 * d)
            self.play(Indicate(rc[4], color=LILAC), Indicate(VGroup(*qb[6:10]), color=LILAC), run_time=.1 * d)
            self.play(TransformFromCopy(rc[4], qc[0]), TransformFromCopy(VGroup(*qb[6:9]), qc[1]),
                      TransformFromCopy(qb[9], qc[2]), run_time=.14 * d)
            self.play(Write(VGroup(*qc[3:])), run_time=.1 * d)
            g_qc = glow(qc[4], LILAC)
            self.play(FadeIn(g_qc), run_time=.06 * d)
            self.play(TransformFromCopy(VGroup(*qc[4:6]), VGroup(*qd[0:2])),
                      TransformFromCopy(qb[4], VGroup(qd[2], qd[3])), TransformFromCopy(qb[5], qd[4]),
                      run_time=.2 * d)
            self.play(*[TransformFromCopy(rc[6 + i], qd[5 + i]) for i in range(6)], run_time=.16 * d)
            self.wait(.14 * d)

        # ---- beat 7: times two, solve for q2 ----
        qx = E(r"(2K_1+K_2)|q_2|-|P_1|=|2(|P_2|+|P_3|+|P_4|)", size=48)
        paint(qx, {0: LILAC})
        at_eq(qx, 4, XW, -1.35)
        x2 = M(r"\times 2", size=36, color=MUTED).next_to(qx, LEFT, buff=.6)
        q2r = E(r"q_2|=|\frac{P_1+2(P_2+P_3+P_4)}{2K_1+K_2}", size=52)
        fcol(q2r[2], [((0, 2), ROSE), ((5, 7), ROSE), ((8, 10), ROSE), ((11, 13), ROSE),
                      ((16, 18), LILAC), ((19, 21), LILAC)])
        at_eq(q2r, 1, XW, -2.65)
        b2 = rbox(q2r)
        g2 = glow(q2r, SKY)
        with self.say("Multiply through by two and solve. q two equals P one, plus two times the sum of P two, P "
                      "three and P four, all over two K one plus K two.") as d:
            self.play(FadeOut(VGroup(qb, qc, g_qc)), qd.animate.shift(UP * (-.35 - S3)), run_time=.12 * d)
            self.play(FadeIn(x2, shift=RIGHT * .2), TransformFromCopy(VGroup(*qd[0:2]), VGroup(*qx[0:2])),
                      TransformFromCopy(qd[2], qx[2]), TransformFromCopy(qd[4], qx[3]),
                      TransformFromCopy(qd[5], qx[4]), *[TransformFromCopy(qd[6 + i], qx[6 + i]) for i in range(5)],
                      FadeIn(qx[5]), FadeIn(qx[11]), run_time=.22 * d)
            self.play(Write(q2r), run_time=.3 * d)
            self.play(Create(b2), FadeIn(g2), run_time=.14 * d)
            self.wait(.22 * d)

        # ---- beat 8: back-substitute for q1 and q3 ----
        q1r = frac_q1()
        q1r.move_to([-3.6, -.9, 0])
        q3r = E(r"q_3|=|q_2|+|\frac{P_4}{K_3}", size=48)
        fcol(q3r[4], [((0, 2), ROSE), ((3, 5), LILAC)])
        q3r.move_to([3.6, -.9, 0])
        b1, b3 = rbox(q1r), rbox(q3r)
        top = VGroup(q2r, b2, g2)
        note = T("put q2 in for a formula in the loads alone", size=32, color=MUTED).move_to([0, -2.9, 0])
        with self.say("Then q one is P one plus K two q two, over two K two, and q three is q two plus P four over "
                      "K three.") as d:
            self.play(FadeOut(VGroup(r1, rc, r3b, chips, sep, qd, qx, x2)),
                      top.animate.move_to([0, 1.9, 0]), run_time=.16 * d)
            a1 = Arrow(b2.get_bottom() + LEFT * 1.2, b1.get_top() + UP * .25, color=MUTED, buff=.1,
                       stroke_width=4, max_tip_length_to_length_ratio=.15)
            a3 = Arrow(b2.get_bottom() + RIGHT * 1.2, b3.get_top() + UP * .25, color=MUTED, buff=.1,
                       stroke_width=4, max_tip_length_to_length_ratio=.15)
            self.play(Write(q1r), GrowArrow(a1), run_time=.22 * d)
            self.play(Create(b1), run_time=.08 * d)
            self.play(Write(q3r), GrowArrow(a3), run_time=.22 * d)
            self.play(Create(b3), run_time=.08 * d)
            self.play(FadeIn(note, shift=UP * .2), run_time=.12 * d)
            self.wait(.12 * d)
        self.wipe()
