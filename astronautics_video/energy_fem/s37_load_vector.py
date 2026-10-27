"""S37: the element load vector (BRIEF.md S37)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: integral of (1 - s) and of s over 0..1 are one half; uniform f = c gives Q1 = Q2 = c l / 2
_s = np.linspace(0, 1, 200001)
_trap = getattr(np, "trapezoid", None) or np.trapz
assert np.isclose(_trap(1 - _s, _s), 0.5)
assert np.isclose(_trap(_s, _s), 0.5)
_c, _l = -5.0, 20.0                               # HW P2 element: c = -5 lb/in, l = 20 in
_Q1 = _trap(_c * (1 - _s) * _l, _s)
_Q2 = _trap(_c * _s * _l, _s)
assert np.isclose(_Q1, _c * _l / 2) and np.isclose(_Q2, _c * _l / 2)
assert np.isclose(_Q1 + _Q2, _c * _l)             # half the element's total load c l to each node
assert np.isclose(_c * _l / 2, -50)

X1, X2, YB, HB = -4.5, 4.5, 1.9, 0.6               # element ends, bar centre height, bar height
WE = {"W_e": EMBER, "c": ROSE, "l": INK}


class S37_Load_Vector(VScene):
    budget = 167

    def construct(self):
        # ---- the element figure (top half) ----
        el = bar(X1, X2, y=YB, h=HB)
        n1, n2 = node([X1, YB, 0], r=0.11), node([X2, YB, 0], r=0.11)
        load = dist_load(X1 + 0.35, X2 - 0.55, YB + HB / 2 + 0.38, n=9, d=RIGHT, length=0.62)
        f_lab = M(r"f", size=44, color=ROSE).move_to([0, YB + HB / 2 + 1.0, 0])
        s0 = M(r"s=0", size=36, color=LIME).move_to([X1, YB + HB / 2 + 1.0, 0])
        s1 = M(r"s=1", size=36, color=LIME).move_to([X2, YB + HB / 2 + 1.0, 0])
        d1 = Arrow([X1, YB - 0.62, 0], [X1 + 0.8, YB - 0.62, 0], buff=0, color=SKY, stroke_width=6,
                   max_tip_length_to_length_ratio=0.3)
        d2 = Arrow([X2, YB - 0.62, 0], [X2 + 0.8, YB - 0.62, 0], buff=0, color=SKY, stroke_width=6,
                   max_tip_length_to_length_ratio=0.3)
        u1l = M(r"u_1", size=40, color=SKY).next_to(d1, DOWN, buff=0.12)
        u2l = M(r"u_2", size=40, color=SKY).next_to(d2, DOWN, buff=0.12)
        ly = YB - 0.95
        lline = Line([X1 + 1.2, ly, 0], [X2 - 0.4, ly, 0], color=MUTED, stroke_width=3)
        lticks = VGroup(*[Line([x, ly - 0.15, 0], [x, ly + 0.15, 0], color=MUTED, stroke_width=3)
                          for x in (X1 + 1.2, X2 - 0.4)])
        l_lab = backed(M(r"l", size=40).move_to(lline))
        span_l = VGroup(lline, lticks, l_lab)
        fig = VGroup(el, load, n1, n2, f_lab, s0, s1, d1, d2, u1l, u2l, span_l)

        # ---- beat 1: the work integral ----
        eq1 = E(r"W_e|=|\int_0^1|f|\big[|(1-s)|u_1|+|s|u_2|\big]|l\,ds", size=50, cmap=WE)
        eq1.move_to([0, -1.6, 0])
        self.beat("Last piece: the work potential of a spread-out load f on one element. It's the integral of f times u, d x. Put in our u and d x equals l d s.",
                  [FadeIn(el), FadeIn(n1), FadeIn(n2), FadeIn(d1), FadeIn(d2), FadeIn(u1l), FadeIn(u2l),
                   FadeIn(span_l), FadeIn(s0), FadeIn(s1)],
                  [LaggedStart(*[GrowArrow(a) for a in load], lag_ratio=0.1), FadeIn(f_lab)],
                  Write(eq1), Circumscribe(eq1[4:10], color=SKY), Circumscribe(eq1[10], color=LIME),
                  w=(.12, .15, .3, .2, .2))

        # ---- beat 2: split into u1 Q1 + u2 Q2 ----
        lhs = E(r"W_e|=", size=52, cmap=WE)
        t1 = E(r"u_1|Q_1", size=52)
        pl = M(r"+", size=52)
        t2 = E(r"u_2|Q_2", size=52)
        t1.move_to([-2.4, -0.55, 0]); t2.move_to([3.4, -0.55, 0]); pl.move_to([0.5, -0.55, 0])
        lhs.next_to(t1, LEFT, buff=0.3)
        def1 = E(r"Q_1|=|\int_0^1|f|(1-s)|l\,ds", size=42).move_to([-2.4, -2.25, 0])
        def2 = E(r"Q_2|=|\int_0^1|f|s|l\,ds", size=42).move_to([3.4, -2.25, 0])
        br1 = Brace(t1, DOWN, buff=0.15, color=INK2)
        br2 = Brace(t2, DOWN, buff=0.15, color=INK2)
        with self.say("Split it in two. The part multiplying u one is the integral of f times one minus s times l. Call it Q one. The part multiplying u two is the integral of f times s times l. Call it Q two.") as d:
            self.play(ReplacementTransform(eq1[0], lhs[0]), ReplacementTransform(eq1[1], lhs[1]),
                      FadeTransform(VGroup(*eq1[2:]), VGroup(t1, pl, t2)), run_time=.16 * d)
            self.play(Indicate(t1[0], color=SKY), GrowFromCenter(br1), run_time=.12 * d)
            self.play(Write(def1), run_time=.2 * d)
            self.play(Indicate(def1[0], color=ROSE), Indicate(t1[1], color=ROSE), run_time=.1 * d)
            self.play(Indicate(t2[0], color=SKY), GrowFromCenter(br2), run_time=.12 * d)
            self.play(Write(def2), run_time=.18 * d)
            self.play(Indicate(def2[0], color=ROSE), Indicate(t2[1], color=ROSE), run_time=.1 * d)

        # ---- beat 3: the element load vector ----
        vec = M(r"\begin{Bmatrix} Q_1 \\ Q_2 \end{Bmatrix}", size=56, color=ROSE).move_to([0, -1.6, 0])
        vbox = SurroundingRectangle(vec, color=ROSE, buff=0.22, stroke_width=4)
        vlab = T("element load vector", size=36, color=INK).next_to(vbox, DOWN, buff=0.25)
        vcard = VGroup(vec, vbox, vlab)
        qa1 = Arrow([X1 - 1.3, YB, 0], [X1, YB, 0], buff=0, color=ROSE, stroke_width=7,
                    max_tip_length_to_length_ratio=0.25)
        qa2 = Arrow([X2, YB, 0], [X2 + 1.3, YB, 0], buff=0, color=ROSE, stroke_width=7,
                    max_tip_length_to_length_ratio=0.25)
        q1l = M(r"Q_1", size=40, color=ROSE).next_to(qa1, UP, buff=0.12)
        q2l = M(r"Q_2", size=40, color=ROSE).next_to(qa2, UP, buff=0.12)
        s0.generate_target(); s0.target.next_to(n1, UP, buff=0.9).shift(RIGHT * 0.45)
        s1.generate_target(); s1.target.next_to(n2, UP, buff=0.9).shift(LEFT * 0.45)
        self.beat("Q one and Q two together are called the element load vector. They're the forces at the two nodes that do the same work as the spread-out load.",
                  [FadeOut(VGroup(lhs, t1, pl, t2, br1, br2, def1, def2)), MoveToTarget(s0), MoveToTarget(s1)],
                  [FadeIn(vec), Create(vbox)], FadeIn(vlab, shift=UP * 0.2),
                  [GrowArrow(qa1), GrowArrow(qa2), FadeIn(q1l), FadeIn(q2l)],
                  [Indicate(load, color=ROSE), Indicate(VGroup(qa1, qa2), color=ROSE)],
                  w=(.15, .2, .15, .25, .25))

        # ---- beat 4: f constant = c ----
        fc = M(r"f=c", size=44, color=ROSE).move_to(f_lab)
        eqQ1 = E(r"Q_1|=|c\,l\int_0^1(1-s)\,ds|=|\frac{cl}{2}", size=48, cmap=WE)
        eqQ2 = E(r"Q_2|=|c\,l\int_0^1 s\,ds|=|\frac{cl}{2}", size=48, cmap=WE)
        eqQ1.move_to([2.0, -0.75, 0])
        eqQ2.move_to([2.0, -2.6, 0])
        eqQ2.align_to(eqQ1, LEFT)
        with self.say("Now take the common case, f constant, equal to c. The integral of one minus s from zero to one is one half, and so is the integral of s. So Q one and Q two are both c l over two.") as d:
            self.play(ReplacementTransform(f_lab, fc), vcard.animate.scale(0.9).move_to([-4.6, -1.7, 0]),
                      FadeOut(VGroup(qa1, qa2, q1l, q2l)), run_time=.16 * d)
            self.play(Write(eqQ1[:3]), run_time=.14 * d)
            self.play(Circumscribe(eqQ1[2], color=LIME), run_time=.12 * d)
            self.play(Write(eqQ2[:3]), run_time=.14 * d)
            self.play(Circumscribe(eqQ2[2], color=LIME), run_time=.12 * d)
            self.play(Write(eqQ1[3:]), Write(eqQ2[3:]), run_time=.16 * d)
            self.play(FadeIn(glow(eqQ1[4], ROSE)), FadeIn(glow(eqQ2[4], ROSE)), run_time=.1 * d)
            self.wait(.06 * d)

        # ---- beat 5: total c l, half to each node ----
        tot = M(r"\text{total } c\,l", size=44, color=ROSE).move_to(fc)
        left_arrows = [a for a in load if a.get_center()[0] < 0]
        right_arrows = [a for a in load if a.get_center()[0] >= 0]
        big1 = Arrow([X1 - 1.6, YB, 0], [X1, YB, 0], buff=0, color=ROSE, stroke_width=14,
                     max_tip_length_to_length_ratio=0.3)
        big2 = Arrow([X2, YB, 0], [X2 + 1.6, YB, 0], buff=0, color=ROSE, stroke_width=14,
                     max_tip_length_to_length_ratio=0.3)
        h1 = M(r"\frac{cl}{2}", size=48, color=ROSE).next_to(big1, UP, buff=0.18)
        h2 = M(r"\frac{cl}{2}", size=48, color=ROSE).next_to(big2, UP, buff=0.18)
        with self.say("In plain words: the element carries a total load of c times l, and half of it goes to each end node.") as d:
            self.play(ReplacementTransform(fc, tot), Indicate(load, color=ROSE), run_time=.25 * d)
            self.play(FadeOut(VGroup(s0, s1)), run_time=.08 * d)
            self.play(*[a.animate.scale(0.3).move_to([X1 - 0.8, YB, 0]).set_opacity(0) for a in left_arrows],
                      *[a.animate.scale(0.3).move_to([X2 + 0.8, YB, 0]).set_opacity(0) for a in right_arrows],
                      GrowArrow(big1), GrowArrow(big2), run_time=.3 * d)
            self.play(FadeIn(h1, shift=DOWN * 0.2), FadeIn(h2, shift=DOWN * 0.2),
                      Circumscribe(eqQ1[4], color=ROSE), Circumscribe(eqQ2[4], color=ROSE), run_time=.2 * d)
            self.wait(.17 * d)
        self.wipe()
