"""S11: two partial derivatives (BRIEF.md S11)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the two-spring numbers make both partials vanish, and the expanded / collected forms agree
k1, k2, F1, F2, q1, q2 = 40.0, 20.0, 40.0, 20.0, 1.5, 2.5
dPi1 = lambda a, b: k1 * a + k2 * (b - a) * (-1) - F1          # d Pi / d q1 (chain rule, inside derivative -1)
dPi2 = lambda a, b: k2 * (b - a) - F2                          # d Pi / d q2
assert np.isclose(dPi1(q1, q2), 0) and np.isclose(dPi2(q1, q2), 0)
Pi = lambda a, b: .5 * k1 * a ** 2 + .5 * k2 * (b - a) ** 2 - F1 * a - F2 * b
h = 1e-6
for a, b in [(0.3, -1.2), (2.0, 0.7), (q1, q2)]:
    assert np.isclose((Pi(a + h, b) - Pi(a - h, b)) / (2 * h), dPi1(a, b), atol=1e-4)
    assert np.isclose((Pi(a, b + h) - Pi(a, b - h)) / (2 * h), dPi2(a, b), atol=1e-4)
    assert np.isclose(dPi1(a, b), k1 * a - k2 * b + k2 * a - F1)               # expanded line
    assert np.isclose(dPi1(a, b) + F1, (k1 + k2) * a - k2 * b)                 # Newton row 1
    assert np.isclose(dPi2(a, b) + F2, -k2 * a + k2 * b)                       # Newton row 2

SQ = {"q_1^2": SKY, "(q_2-q_1)^2": SKY}
LX = -6.6          # left edge of the derivation column
ROW_A, ROW_B, ROW_C = 1.15, -0.1, -1.35


def good_frame(m):
    """GOOD frame (faint GOOD fill) around an equation: a Newton row or its energy twin, lit as a match."""
    return SurroundingRectangle(m, color=GOOD, stroke_width=4, buff=.08, corner_radius=.1,
                                fill_color=GOOD, fill_opacity=.1).set_z_index(-1)


def tick(eq, card):
    """check badge inside the Newton card's left padding, level with eq"""
    c = Circle(radius=.2, color=GOOD, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
    b = VGroup(c, M(r"\checkmark", size=30, color=GOOD).move_to(c))
    return b.move_to([card.get_left()[0] + .15 + .2, eq.get_y(), 0]).set_z_index(3)


class S11_Partials(VScene):
    budget = 223

    def construct(self):
        # Pi at the top: term groups 0 Pi, 1 =, 2-4 spring 1, 5 +, 6-8 spring 2, 9 -, 10-11 F1 q1, 12 -, 13-14 F2 q2
        pi = E(r"\Pi|=|\tfrac{1}{2}|k_1|q_1^2|+|\tfrac{1}{2}|k_2|(q_2-q_1)^2|-|F_1|q_1|-|F_2|q_2",
               size=46, cmap=SQ)
        t_s1, t_s2, t_f1, t_f2 = pi[2:5], pi[6:9], pi[9:12], pi[12:15]

        # Newton panel (the force balances from S09)
        # compact box at the top right, as S09 ends: title "Newton", two equations 0.3 apart
        n_title = T("Newton", size=32, color=INK2)
        N1 = E(r"(|k_1|+|k_2|)|q_1|-|k_2|q_2|=|F_1", size=40)
        N2 = E(r"-|k_2|q_1|+|k_2|q_2|=|F_2", size=40)
        eqs = VGroup(N1, N2).arrange(DOWN, buff=.3, aligned_edge=LEFT)
        body = VGroup(n_title, eqs).arrange(DOWN, buff=.25)
        PAD, LPAD = .25, .15 + .4 + .2           # left padding holds the check badges (buff .15 from the border)
        card = RoundedRectangle(width=body.width + PAD + LPAD, height=body.height + 2 * PAD, corner_radius=.15,
                                stroke_color=HAIR, stroke_width=2, fill_color=SURFACE, fill_opacity=1)
        card.move_to(body).shift(LEFT * (LPAD - PAD) / 2).set_z_index(-2)
        newton = VGroup(card, body)
        newton.shift(np.array([6.9, 3.8, 0]) - card.get_corner(UR))
        pi.next_to(card, LEFT, buff=.3).set_y(card.get_y() + .1)
        if pi.get_left()[0] < -6.85:
            fit(pi, card.get_left()[0] - .3 + 6.85, 1.2)
            pi.next_to(card, LEFT, buff=.3).set_y(card.get_y() + .1)

        # beat 1: the two stationarity conditions
        C1 = E(r"\frac{\partial \Pi}{\partial q_1}|=|0", size=48)
        C2 = E(r"\frac{\partial \Pi}{\partial q_2}|=|0", size=48)
        C1.move_to([-2.4, 0.7, 0]); C2.move_to([-2.4, -0.9, 0])
        self.beat("With two unknowns, stationary means: the partial derivative with respect to q one is zero, "
                  "and the partial derivative with respect to q two is zero.",
                  FadeIn(pi), FadeIn(newton), Write(C1), Write(C2), w=(.2, .2, .25, .25))

        # beat 2: d Pi / d q1 term by term
        # D1 parts: 0 dPi/dq1, 1 =, 2 k1, 3 q1, 4 +, 5 k2, 6 (, 7 q2, 8 -, 9 q1, 10 ), 11 cdot, 12 (-1),
        #           13 -, 14 F1, 15 =, 16 0
        D1 = E(r"\frac{\partial \Pi}{\partial q_1}|=|k_1|q_1|+|k_2|(|q_2|-|q_1|)|\cdot|(-1)|-|F_1|=|0", size=44)
        fit(D1, 8.6, 1.4)
        D1.move_to([0, ROW_A, 0], aligned_edge=LEFT).set_x(LX + D1.width / 2)
        with self.say("Take q one first. One half k one q one squared gives k one q one. For the second spring, "
                      "use the chain rule: two times one half is one, times k two times q two minus q one, "
                      "times the inside derivative.") as d:
            self.play(FadeOut(C2), ReplacementTransform(C1[0], D1[0]), ReplacementTransform(C1[1], D1[1]),
                      FadeOut(C1[2]), run_time=.1 * d)
            self.play(Indicate(t_s1, color=GOLD), run_time=.12 * d)
            self.play(TransformFromCopy(t_s1[1:3], D1[2:4]), run_time=.12 * d)
            self.wait(.06 * d)
            self.play(Indicate(t_s2, color=GOLD), run_time=.14 * d)
            self.play(Write(D1[4]), TransformFromCopy(t_s2[1], D1[5]), run_time=.12 * d)
            self.play(FadeIn(D1[6:11], shift=.1 * DOWN), run_time=.14 * d)
            self.play(Write(D1[11:13]), run_time=.1 * d)

        # beat 3: the inside derivative is minus one
        ring = SurroundingRectangle(D1[12], color=ACCENT, stroke_width=5, buff=.07, corner_radius=.12)
        inside = M(r"\frac{\partial (q_2-q_1)}{\partial q_1} = -1", size=36, color=ACCENT)
        inside.next_to(ring, DOWN, buff=.25)
        if inside.get_right()[0] > 1.9:
            inside.shift(LEFT * (inside.get_right()[0] - 1.9))
        self.beat("And the inside derivative, the derivative of q two minus q one with respect to q one, is minus "
                  "one. That minus sign is why our equations have minus signs between neighbors.",
                  Create(ring), FadeIn(inside, shift=.1 * UP), .25, Indicate(D1[12], color=ACCENT),
                  w=(.2, .2, .2))

        # beat 4: the load, then the expanded line
        X = E(r"k_1|q_1|-|k_2|q_2|+|k_2|q_1|-|F_1|=|0", size=44)
        X.move_to([0, ROW_B, 0]).set_x(D1[2].get_left()[0] + X.width / 2)
        with self.say("Then the load: F one q one gives F one, with a minus sign. Set it all to zero: k one q one, "
                      "minus k two q two, plus k two q one, minus F one, equals zero.") as d:
            self.play(Indicate(t_f1, color=GOLD), FadeOut(inside), run_time=.12 * d)
            self.play(TransformFromCopy(t_f1[0:2], D1[13:15]), run_time=.12 * d)
            self.play(Write(D1[15:17]), run_time=.1 * d)
            self.wait(.04 * d)
            self.play(TransformFromCopy(D1[2:4], X[0:2]), run_time=.12 * d)
            self.play(FadeIn(X[2:5], shift=.1 * DOWN), Indicate(D1[7], color=SKY), run_time=.13 * d)
            self.play(FadeIn(X[5:8], shift=.1 * DOWN), Indicate(D1[9], color=SKY), run_time=.13 * d)
            self.play(TransformFromCopy(D1[13:17], X[8:12]), run_time=.12 * d)

        # beat 5: collect, compare with Newton row 1
        G = E(r"(|k_1|+|k_2|)|q_1|-|k_2|q_2|=|F_1", size=44)
        G.move_to([0, ROW_C, 0]).set_x(X.get_left()[0] + G.width / 2)
        G_end = G.copy().scale(40 / 44).next_to(card, DOWN, buff=.3).align_to(N1, LEFT)
        with self.say("Group the q one terms and move F one across: k one plus k two, times q one, minus k two q "
                      "two, equals F one. Exactly Newton's first equation.") as d:
            self.play(Indicate(X[0:2], color=SKY), Indicate(X[5:8], color=SKY), run_time=.12 * d)
            self.play(FadeIn(G[0]), TransformFromCopy(X[0], G[1]), FadeIn(G[2]), TransformFromCopy(X[6], G[3]),
                      FadeIn(G[4]), TransformFromCopy(VGroup(X[1], X[7]), G[5]), run_time=.16 * d)
            self.play(TransformFromCopy(X[2:5], G[6:9]), run_time=.1 * d)
            self.play(Indicate(X[8:10], color=ROSE), run_time=.08 * d)
            self.play(FadeIn(G[9]), TransformFromCopy(X[9], G[10]), run_time=.12 * d)
            self.wait(.04 * d)
            self.play(G.animate.scale(40 / 44).move_to(G_end), run_time=.14 * d)
            self.play(FadeIn(good_frame(N1)), FadeIn(good_frame(G)), run_time=.12 * d)

        # beat 6: d Pi / d q2
        # D2 parts: 0 dPi/dq2, 1 =, 2 k2, 3 (, 4 q2, 5 -, 6 q1, 7 ), 8 -, 9 F2, 10 =, 11 0
        D2 = E(r"\frac{\partial \Pi}{\partial q_2}|=|k_2|(|q_2|-|q_1|)|-|F_2|=|0", size=44)
        D2.move_to([0, ROW_A, 0]).set_x(LX + D2.width / 2)
        H = E(r"-|k_2|q_1|+|k_2|q_2|=|F_2", size=44)
        H.move_to([0, ROW_B, 0]).set_x(D2[2].get_left()[0] + H.width / 2)
        note = T("No arrows drawn: only derivatives.", size=32, color=MUTED).move_to([-2.35, -2.75, 0])
        with self.say("Now q two. Only two terms contain it: the second spring gives k two times q two minus q one, "
                      "and the load gives minus F two. Set to zero and multiply out: minus k two q one plus k two q "
                      "two equals F two. Newton's second equation. We never drew an arrow.") as d:
            self.play(FadeOut(VGroup(D1, X, ring)), run_time=.07 * d)
            self.play(Write(D2[0:2]), run_time=.06 * d)
            self.play(Indicate(t_s2, color=GOLD), run_time=.08 * d)
            self.play(TransformFromCopy(t_s2[1:3], D2[2:8]), run_time=.1 * d)
            self.play(Indicate(t_f2, color=GOLD), run_time=.07 * d)
            self.play(TransformFromCopy(t_f2, D2[8:10]), run_time=.08 * d)
            self.play(Write(D2[10:12]), run_time=.06 * d)
            # H parts: 0 -, 1 k2, 2 q1, 3 +, 4 k2, 5 q2, 6 =, 7 F2
            self.play(TransformFromCopy(D2[5], H[0]), TransformFromCopy(D2[2], H[1]),
                      TransformFromCopy(D2[6], H[2]), run_time=.1 * d)
            self.play(FadeIn(H[3]), TransformFromCopy(D2[2], H[4]), TransformFromCopy(D2[4], H[5]),
                      run_time=.08 * d)
            self.play(FadeIn(H[6]), TransformFromCopy(D2[9], H[7]), run_time=.07 * d)
            H_end = H.copy().scale(40 / 44).next_to(G, DOWN, buff=.3).align_to(N1, LEFT)
            self.play(H.animate.scale(40 / 44).move_to(H_end), run_time=.1 * d)
            ticks = VGroup(tick(N1, card), tick(N2, card))
            self.play(FadeIn(good_frame(N2)), FadeIn(good_frame(H)), FadeIn(ticks, scale=1.4), run_time=.07 * d)
            self.play(FadeIn(note), run_time=.05 * d)
        self.wipe()
