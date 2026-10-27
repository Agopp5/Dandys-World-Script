"""S12: the two-spring system as a matrix, with numbers (BRIEF.md S12)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts
k1, k2, F1, F2 = 40.0, 20.0, 40.0, 20.0
Kn = np.array([[k1 + k2, -k2], [-k2, k2]])
assert np.allclose(Kn, [[60, -20], [-20, 20]])
qs = np.linalg.solve(Kn, [F1, F2])
assert np.allclose(qs, [1.5, 2.5])
assert np.isclose((Kn[0, 0] + Kn[1, 0]), 40) and np.isclose(Kn[0, 1] + Kn[1, 1], 0)   # adding rows: q2 cancels
assert np.isclose(F1 + F2, 60) and np.isclose(60 / 40, 1.5)
assert np.isclose(20 * (qs[1] - 1.5), 20)
assert np.isclose(F2 / k2, 1.0) and np.isclose(qs[1] - qs[0], 1.0)


def mat(rows, color, curly=False, hb=1.5):
    m = Matrix(rows, left_bracket="\\{" if curly else "[", right_bracket="\\}" if curly else "]",
               h_buff=hb if not curly else 1.0)
    m.get_entries().set_color(color)
    m.get_brackets().set_color(INK)
    return m


def tick(m):
    return M(r"\checkmark", size=48, color=GOOD).next_to(m, RIGHT, buff=.3)


class S12_Two_Matrix(VScene):
    budget = 191

    def construct(self):
        # the two-spring figure, small at the top
        y0 = 2.75
        wp = np.array([-6.4, y0, 0])
        n1p = np.array([-3.8, y0, 0])
        n2p = np.array([-1.2, y0, 0])
        W0 = wall(wp, side=LEFT, h=1.2)
        sp1 = spring(wp, n1p, label="k_1")
        sp2 = spring(n1p, n2p, label="k_2")
        N1, N2 = node(n1p), node(n2p)
        f1 = force(n1p + UP * .95, RIGHT, length=.8, label="F_1")
        lead = Line(n1p, n1p + UP * .95, color=ROSE, stroke_width=2)
        f2 = force(n2p, RIGHT, length=.9, label="F_2")
        d1, d2 = disp(n1p, "q_1"), disp(n2p, "q_2")
        fig = VGroup(W0, sp1, sp2, lead, N1, N2, f1, f2, d1, d2)
        self.add(fig)

        # beat 1: equations -> matrix rows
        eq1 = E(r"(k_1+k_2)|q_1|-k_2|q_2|=|F_1", size=48)
        eq2 = E(r"-k_2|q_1|+k_2|q_2|=|F_2", size=48)
        paint(eq1, {0: LILAC, 2: LILAC})
        paint(eq2, {0: LILAC, 2: LILAC})
        eq1.move_to([0, 1.15, 0])
        eq2.move_to([0, .35, 0])
        eq2.shift((eq1[4].get_center()[0] - eq2[4].get_center()[0]) * RIGHT)

        Km = mat([["k_1+k_2", "-k_2"], ["-k_2", "k_2"]], LILAC)
        qv = mat([["q_1"], ["q_2"]], SKY, curly=True)
        es = M("=", size=48)
        Fv = mat([["F_1"], ["F_2"]], ROSE, curly=True)
        sym = VGroup(Km, qv, es, Fv).arrange(RIGHT, buff=.3).move_to([-.9, -.2, 0])   # beat-2 home
        Ke, qe, Fe = Km.get_entries(), qv.get_entries(), Fv.get_entries()
        box = SurroundingRectangle(Km, color=LILAC, buff=.15)
        box_lbl = T("stiffness matrix", size=36, color=LILAC).next_to(box, DOWN, buff=.25)
        echo = E(r"K|q|=|F", size=48).next_to(sym, RIGHT, buff=1.0)
        home = sym.get_center()
        sym.move_to([0, -1.75, 0])

        self.beat("Stack the two equations into one matrix equation. Row one is node one's balance; row two is node two's. Each equation's coefficients drop into its row.",
                  FadeIn(VGroup(eq1, eq2), shift=.2 * DOWN),
                  [FadeIn(Km.get_brackets()), FadeIn(qv.get_brackets()), FadeIn(Fv.get_brackets()), Write(es)],
                  [Indicate(eq1, color=INK, scale_factor=1.05),
                   TransformFromCopy(eq1[0], Ke[0]), TransformFromCopy(eq1[2], Ke[1]),
                   TransformFromCopy(eq1[1], qe[0]), TransformFromCopy(eq1[3], qe[1]),
                   TransformFromCopy(eq1[5], Fe[0])],
                  [Indicate(eq2, color=INK, scale_factor=1.05),
                   TransformFromCopy(eq2[0], Ke[2]), TransformFromCopy(eq2[2], Ke[3]),
                   TransformFromCopy(eq2[5], Fe[1])],
                  w=(.15, .12, .38, .35))

        # beat 2: the stiffness matrix
        self.beat("The matrix is called the stiffness matrix. Like K for one spring, it multiplies displacements and gives forces.",
                  [FadeOut(VGroup(eq1, eq2)), sym.animate.move_to(home)],
                  [Create(box), FadeIn(box_lbl)],
                  [FadeIn(echo, shift=.2 * LEFT), Indicate(Km, color=LILAC, scale_factor=1.04)],
                  w=(.25, .4, .35))

        # beat 3: numbers
        cards = VGroup(E(r"k_1|=|40\text{ N/mm}", size=36), E(r"k_2|=|20\text{ N/mm}", size=36),
                       E(r"F_1|=|40\text{ N}", size=36), E(r"F_2|=|20\text{ N}", size=36))
        cards.arrange_in_grid(2, 2, buff=(.5, .25), cell_alignment=LEFT)
        card = panel(cards).move_to([3.95, y0, 0])
        Nm = mat([["60", "-20"], ["-20", "20"]], LILAC, hb=1.15)
        qv2 = mat([["q_1"], ["q_2"]], SKY, curly=True)
        es2 = M("=", size=48)
        Fn = mat([["40"], ["20"]], ROSE, curly=True)
        num = VGroup(Nm, qv2, es2, Fn).arrange(RIGHT, buff=.3).move_to(home)
        Ne = Nm.get_entries()
        self.beat("Now numbers. k one is forty newtons per millimeter, k two is twenty. F one is forty newtons, F two is twenty. So the matrix is sixty, minus twenty, minus twenty, twenty.",
                  FadeIn(card, shift=.2 * LEFT),
                  [FadeOut(VGroup(box, box_lbl, echo)), ReplacementTransform(sym, num)],
                  LaggedStart(*[Indicate(Ne[i], color=LILAC, scale_factor=1.25) for i in range(4)], lag_ratio=.6),
                  .15,
                  w=(.45, .15, .25))

        # beat 4: checkpoint cue
        self.beat("Your turn: pause and do checkpoint two point one in your guide, and solve for q one and q two.",
                  Circumscribe(qv2, color=SKY), .5)
        self.checkpoint("2.1", "Solve the two-spring system for q1 and q2")

        # beat 5: solve by adding rows
        X0 = 4.1
        r1 = E(r"60|q_1|-20|q_2|=|40", size=48)
        r2 = E(r"-20|q_1|+20|q_2|=|20", size=48)
        paint(r1, {0: LILAC, 2: LILAC, 5: ROSE})
        paint(r2, {0: LILAC, 2: LILAC, 5: ROSE})

        def at_eq(m, y, k):            # put part k (the "=") at x = X0
            m.move_to([0, y, 0])
            m.shift((X0 - m[k].get_center()[0]) * RIGHT)
            return m

        at_eq(r1, 1.0, 4)
        at_eq(r2, .2, 4)
        plus = M("+", size=48).next_to(r2, LEFT, buff=.35)
        rule = Line([plus.get_left()[0], -.25, 0], [r1.get_right()[0], -.25, 0], color=INK2, stroke_width=3)
        sm = E(r"40|q_1|=|60", size=48)
        paint(sm, {0: LILAC, 3: ROSE})
        at_eq(sm, -.8, 2)
        q1r = E(r"q_1|=|1.5\text{ mm}", size=48)
        at_eq(q1r, -1.75, 1)
        g1 = glow(q1r, SKY)
        st1, st2 = strike(VGroup(r1[2], r1[3])), strike(VGroup(r2[2], r2[3]))
        q1_home = np.array([-4.2, -1.3, 0])
        q2_home = np.array([-4.2, -2.3, 0])

        r2b = E(r"20|(|q_2|-|1.5|)|=|20", size=48)
        paint(r2b, {0: LILAC, 4: SKY, 7: ROSE})
        at_eq(r2b, 1.0, 6)
        q2r = E(r"q_2|=|2.5\text{ mm}", size=48)
        at_eq(q2r, .1, 1)
        g2 = glow(q2r, SKY)

        with self.say("Add the two equations: the q two terms cancel, leaving forty q one equals sixty, so q one is one point five millimeters. Then the second equation: twenty times q two minus one point five equals twenty, so q two is two point five millimeters.") as d:
            self.play(num.animate.move_to([-3.95, .5, 0]), run_time=.05 * d)
            self.play(TransformFromCopy(VGroup(Ne[0], Ne[1], Fn.get_entries()[0]), r1),
                      TransformFromCopy(VGroup(Ne[2], Ne[3], Fn.get_entries()[1]), r2), run_time=.09 * d)
            self.play(Indicate(VGroup(r1[2], r1[3]), color=SKY), Indicate(VGroup(r2[2], r2[3]), color=SKY),
                      run_time=.07 * d)
            self.play(Create(st1), Create(st2), run_time=.05 * d)
            self.play(FadeIn(plus), Create(rule), Write(sm), run_time=.09 * d)
            self.play(Write(q1r), FadeIn(g1), run_time=.08 * d)
            self.snap("rows added")
            self.wait(.04 * d)
            self.play(FadeOut(VGroup(r1, st1, st2, plus, rule, sm)), r2.animate.shift(.8 * UP),
                      VGroup(g1, q1r).animate.move_to(q1_home), run_time=.07 * d)
            self.play(*morph(r2, r2b, [(2, 0), (3, 2), (4, 6), (5, 7)]),
                      Indicate(q1r[2], color=SKY), run_time=.13 * d)
            self.snap("second equation")
            self.wait(.1 * d)
            self.play(Write(q2r), FadeIn(g2), run_time=.09 * d)
            self.wait(.06 * d)
            self.play(VGroup(g2, q2r).animate.move_to(q2_home), FadeOut(r2b), run_time=.06 * d)

        # beat 6: Newton check
        xc = (wp[0] + n1p[0]) / 2
        cut = DashedLine([xc, y0 + .75, 0], [xc, y0 - .75, 0], color=ACCENT, stroke_width=4)
        L0 = E(r"F_1|+|F_2|=|60\text{ N}", size=48)
        L1 = E(r"\text{spring 1:}\ \ 60/40|=|1.5\text{ mm}", size=48)
        L2 = E(r"\text{spring 2:}\ \ 20/20|=|1.0\text{ mm}", size=48)
        L3 = E(r"q_2-q_1|=|2.5-1.5|=|1.0\text{ mm}", size=48)
        lines = VGroup(L0, L1, L2, L3).arrange(DOWN, buff=.42, aligned_edge=LEFT).move_to([2.9, -.3, 0])
        lines.align_to(np.array([-1.1, 0, 0]), LEFT)
        ticks = [tick(L) for L in (L1, L2, L3)]
        self.beat("Quick check with Newton. Cut through spring one: everything to its right carries forty plus twenty, sixty newtons, so it stretches sixty over forty, one point five. Spring two carries only F two, twenty, so it stretches one. Two point five minus one point five is one. It all agrees.",
                  [FadeOut(num), Create(cut), Indicate(VGroup(f1, f2), color=ROSE, scale_factor=1.15)],
                  Write(L0),
                  [Write(L1), Indicate(sp1, color=LILAC)],
                  [FadeIn(ticks[0])],
                  [Indicate(VGroup(f2, sp2), color=LILAC), Write(L2), FadeIn(ticks[1])],
                  [Write(L3), Indicate(VGroup(q1r, q2r), color=SKY)],
                  [FadeIn(ticks[2]), FadeIn(glow(L3, GOOD))],
                  .1,
                  w=(.12, .1, .18, .05, .2, .17, .1))
        self.wipe()
