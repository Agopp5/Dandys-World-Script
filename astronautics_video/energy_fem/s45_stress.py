"""S45: stresses in the three-element column: a staircase (BRIEF.md S45)."""
from efem import *
from fractions import Fraction as Fr
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# ---- facts -------------------------------------------------------------------------------------------
# nodal displacements in units of rho g L^2 / (2E) (from S43/S44)
Q = [Fr(0), Fr(-5, 9), Fr(-8, 9), Fr(-1)]
# sigma_e = E (q_b - q_a) / (L/3) = (q_b - q_a) * (rho g L^2 / 2E) * E * 3 / L = (q_b - q_a) * 3/2 * rho g L
SIG = [(Q[i + 1] - Q[i]) * Fr(3, 2) for i in range(3)]
assert Q[1] - Q[0] == Fr(-5, 9)
assert SIG == [Fr(-5, 6), Fr(-1, 2), Fr(-1, 6)]
assert Fr(-8, 9) + Fr(5, 9) == Fr(-3, 9)


def exact(x):                      # exact stress / (rho g L) = -(1 - x/L)
    return -(1 - x)


assert exact(0) == -1 and exact(1) == 0
MIDS = [Fr(1, 6), Fr(1, 2), Fr(5, 6)]
for i, m in enumerate(MIDS):
    assert exact(m) == SIG[i]          # each step equals the exact line at its element's middle


def u_exact(x):                    # exact u / (rho g L^2 / 2E) = (x/L)(x/L - 2)
    return x * (x - 2)


assert [u_exact(Fr(k, 3)) for k in range(4)] == Q
# six elements (nodes exact again): sigma = (u_b - u_a) * 6/2 rho g L, equal to exact at each middle
SIX = [(u_exact(Fr(k + 1, 6)) - u_exact(Fr(k, 6))) * 3 for k in range(6)]
assert SIX == [exact(Fr(2 * k + 1, 12)) for k in range(6)]

SIGC = {r"\sigma_1": ACCENT, r"\sigma_2": ACCENT, r"\sigma_3": ACCENT}
RX = 3.6                            # centre of the right half


class S45_Stress(VScene):
    budget = 232

    def construct(self):
        # ---- the column, left half: three elements, nodal q in units of rho g L^2 / 2E ----
        cx = -4.6
        ys = [-2.55, -0.8, 0.95, 2.7]
        elems = VGroup(*[Rectangle(width=0.8, height=ys[i + 1] - ys[i], color=INK2, stroke_width=3,
                                   fill_color=SURFACE, fill_opacity=1).move_to([cx, (ys[i] + ys[i + 1]) / 2, 0])
                         for i in range(3)])
        ground = wall(np.array([cx, ys[0], 0]), side=DOWN, h=1.8)
        dots = VGroup(*[node([cx, y, 0], r=0.1) for y in ys])
        tags = VGroup(*[badge(i + 1).scale(1.15).move_to([cx - 0.95, (ys[i] + ys[i + 1]) / 2, 0])
                        for i in range(3)])
        qtex = [r"0", r"-\frac59", r"-\frac89", r"-1"]
        qlab = VGroup(*[E(r"q_%d|=|%s" % (i + 1, qtex[i]), size=44).next_to(dots[i], RIGHT, buff=0.75)
                        for i in range(4)])
        qlab[0].shift(0.3 * UP)
        unit = TX(r"$q$ in units of $\rho g L^2/2E$", size=36, color=INK2)
        unit.next_to(ground, DOWN, buff=0.3).set_x(cx + 1.2)
        col = VGroup(ground, elems, dots, tags, qlab, unit)

        # ---- beat 1: the stress formula ----
        gen = E(r"\sigma|=|E\,\frac{q_{\text{top}} - q_{\text{bottom}}}{l}", size=52).move_to([RX, 1.4, 0])
        top_lab = T("top", 32, MUTED).next_to(qlab[1], RIGHT, buff=0.35)
        bot_lab = T("bottom", 32, MUTED).next_to(qlab[0], RIGHT, buff=0.35)
        self.beat("Now stress. In each element, sigma is E times strain, and the strain is the change in displacement over the length: q of the top node minus q of the bottom node, over l.",
                  FadeIn(col), Write(gen), .1, [FadeIn(top_lab), FadeIn(bot_lab), elems[0].animate.set_fill(ACCENT, 0.25)],
                  w=(.3, .4, .25))

        # ---- beat 2: element one, one step at a time ----
        l1 = E(r"q_2|-|q_1|=|-\frac59\,\frac{\rho g L^2}{2E}", size=48).move_to([RX, 2.2, 0])
        l2 = E(r"\sigma_1|=|E\cdot\frac{3}{L}\cdot\Big(-\frac59\,\frac{\rho g L^2}{2E}\Big)", size=48, cmap=SIGC)
        fit(l2, 6.6, 2)
        l2.move_to([RX, 0.3, 0])
        l3 = E(r"\sigma_1|=|-\frac56\,\rho g L", size=56, cmap=SIGC).move_to([RX, -1.7, 0])
        with self.say("Element one: q two minus q one is minus five ninths, times rho g L squared over two E. Divide by L over three, multiply by E: minus five sixths rho g L.") as d:
            self.play(FadeOut(gen), FadeOut(top_lab), FadeOut(bot_lab), Indicate(qlab[1]), Indicate(qlab[0]),
                      run_time=.12 * d)
            self.play(Write(l1), run_time=.25 * d)
            self.play(Write(l2), run_time=.28 * d)
            halo = glow(l3, ACCENT)
            self.play(Write(l3), FadeIn(halo), run_time=.2 * d)
            self.wait(.15 * d)

        # ---- beat 3: checkpoint ----
        res1 = l3
        self.beat("Your turn: pause and do checkpoint six point two in your guide. Find the stress in element two.",
                  [FadeOut(l1), FadeOut(l2), FadeOut(halo)],
                  [res1.animate.scale(52 / 56).move_to([RX, 2.4, 0]),
                   elems[0].animate.set_fill(SURFACE, 1), elems[1].animate.set_fill(ACCENT, 0.25)],
                  [Indicate(qlab[2]), Indicate(qlab[1])], w=(.3, .35, .35))
        self.checkpoint("6.2", "Column under its own weight: the stress in element 2")

        # ---- beat 4: elements two and three ----
        d2 = E(r"q_3|-|q_2|=|-\frac89+\frac59|=|-\frac39", size=48).move_to([RX, 0.8, 0])
        res2 = E(r"\sigma_2|=|-\frac12\,\rho g L", size=52, cmap=SIGC).move_to([RX, 0.8, 0])
        res3 = E(r"\sigma_3|=|-\frac16\,\rho g L", size=52, cmap=SIGC).move_to([RX, -0.8, 0])
        self.beat("Element two: minus eight ninths plus five ninths is minus three ninths. The stress is minus one half rho g L. And element three, minus one sixth rho g L.",
                  Write(d2), .05, ReplacementTransform(d2, res2),
                  [elems[1].animate.set_fill(SURFACE, 1), elems[2].animate.set_fill(ACCENT, 0.25)],
                  Write(res3), w=(.3, .27, .1, .3))
        res = VGroup(res1, res2, res3)

        # ---- beat 5: the plot, left half ----
        ax = Axes(x_range=[0, 1, 1], y_range=[-1.2, 0, 1], x_length=4.9, y_length=5.6, tips=False,
                  axis_config=dict(color=AXIS, stroke_width=3, include_ticks=False))
        ax.move_to([-3.25, -0.75, 0])
        ticks = VGroup(*[Line(ax.c2p(Fr(k, 6), 0), ax.c2p(Fr(k, 6), 0) + 0.14 * UP, color=AXIS, stroke_width=3)
                         for k in range(1, 7)],
                       *[Line(ax.c2p(0, y), ax.c2p(0, y) + 0.14 * LEFT, color=AXIS, stroke_width=3)
                         for y in (-1, -0.5)])
        xt = VGroup(*[M(t, size=40, color=INK2).next_to(ax.c2p(v, 0), UP, buff=0.25)
                      for t, v in ((r"1/3", Fr(1, 3)), (r"2/3", Fr(2, 3)), (r"1", 1))])
        yt = VGroup(M(r"-1", size=40, color=INK2).next_to(ax.c2p(0, -1), LEFT, buff=0.2),
                    M(r"-1/2", size=40, color=INK2).next_to(ax.c2p(0, -0.5), LEFT, buff=0.2))
        xl = M(r"x/L", size=40, color=INK).next_to(ax.c2p(1, 0), RIGHT, buff=0.25)
        yl = E(r"\sigma|\,/\,\rho g L", size=40).next_to(ax.c2p(0, 0), UP, buff=1.05).align_to(ax, LEFT)
        frame_ax = VGroup(ax, ticks, xt, yt, xl, yl)

        def stairs(vals, width=9):
            n = len(vals)
            flats = VGroup(*[Line(ax.c2p(Fr(k, n), v), ax.c2p(Fr(k + 1, n), v), color=ACCENT, stroke_width=width)
                             for k, v in enumerate(vals)])
            risers = VGroup(*[DashedLine(ax.c2p(Fr(k + 1, n), vals[k]), ax.c2p(Fr(k + 1, n), vals[k + 1]),
                                         color=ACCENT, stroke_width=3, stroke_opacity=0.6) for k in range(n - 1)])
            return VGroup(flats, risers)

        st3 = stairs(SIG)
        ex = DashedLine(ax.c2p(0, -1), ax.c2p(1, 0), color=INK2, stroke_width=5, dash_length=0.16)
        leg_fem = VGroup(Line(ORIGIN, 0.6 * RIGHT, color=ACCENT, stroke_width=9),
                         T("FEM, 3 elements", 36, INK))
        leg_fem[1].next_to(leg_fem[0], RIGHT, buff=0.2)
        leg_ex = VGroup(DashedLine(ORIGIN, 0.6 * RIGHT, color=INK2, stroke_width=5, dash_length=0.12),
                        T("exact", 36, INK))
        leg_ex[1].next_to(leg_ex[0], RIGHT, buff=0.2)
        legend = VGroup(leg_fem, leg_ex).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        legend.move_to([RX, -3.0, 0])
        self.beat("Plot them. Each element's stress is a flat step, because its strain is constant. The exact stress is a straight line, from minus rho g L at the base to zero at the top.",
                  [FadeOut(col), Create(frame_ax)],
                  [Create(st3[0][0]), Indicate(res1)], [Create(st3[0][1]), Indicate(res2)],
                  [Create(st3[0][2]), Indicate(res3)], [FadeIn(st3[1]), FadeIn(leg_fem)],
                  [Create(ex), FadeIn(leg_ex)], [Flash(ax.c2p(0, -1), color=INK2), Flash(ax.c2p(1, 0), color=INK2)],
                  w=(.14, .1, .1, .1, .08, .28, .2))

        # ---- beat 6: where they meet ----
        mids = VGroup(*[Dot(ax.c2p(m, exact(m)), radius=0.12, color=INK).set_z_index(5) for m in MIDS])
        rings = VGroup(*[Circle(radius=0.28, color=INK, stroke_width=4).move_to(d) for d in mids])
        mlab = VGroup(*[M(t, size=40, color=INK).next_to(r, DR, buff=0.02)
                        for t, r in zip((r"1/6", r"1/2", r"5/6"), rings)])
        p1 = ax.c2p(MIDS[0], SIG[0])
        z_fem = E(r"\text{step}|=|-\frac56", size=36, cmap={r"\text{step}": ACCENT})
        z_fem.next_to(ax.c2p(Fr(1, 12), SIG[0]), UP, buff=0.3)
        z_ex = E(r"\text{exact at }\frac16|=|-\frac56", size=36)
        z_ex.next_to(p1, DOWN, buff=1.0).shift(1.6 * RIGHT)
        zl = VGroup(backed(z_fem), backed(z_ex)).set_z_index(6)
        fr = self.camera.frame
        with self.say("Look closely at where they meet. At x over L equal to one sixth, the middle of element one, the exact stress is minus five sixths rho g L: exactly the step's value. Each step crosses the line right at its element's middle.") as d:
            self.play(LaggedStart(*[AnimationGroup(FadeIn(m), FadeIn(dt), Create(r))
                                    for m, dt, r in zip(mlab, mids, rings)], lag_ratio=.4),
                      run_time=.2 * d)
            self.play(fr.animate.scale(0.55).move_to(p1 + 0.9 * RIGHT + 0.1 * DOWN), FadeOut(legend), run_time=.15 * d)
            self.play(FadeIn(zl[0]), Indicate(st3[0][0], color=ACCENT), run_time=.15 * d)
            self.play(FadeIn(zl[1]), Indicate(ex, color=INK), run_time=.15 * d)
            self.snap("zoomed: -5/6 on both")
            self.wait(.15 * d)
            self.play(fr.animate.scale(1 / 0.55).move_to(ORIGIN), FadeOut(zl), FadeIn(legend), run_time=.1 * d)
            self.play(*[Flash(dt, color=INK) for dt in mids], run_time=.1 * d)

        # ---- beat 7: the second question answered; finer steps ----
        card = panel(T("Where is the stress highest?", size=36))
        card.move_to([RX + 0.35, 1.0, 0])
        tick = M(r"\checkmark", size=48, color=GOOD).next_to(card, RIGHT, buff=0.15)
        over = tick.get_right()[0] - 6.85
        if over > 0:
            card.shift(over * LEFT)
            tick.shift(over * LEFT)
        qans = VGroup(T("At the base: it holds", 32, INK), T("up the whole weight", 32, INK))
        qans.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(card, DOWN, buff=0.35).align_to(card, LEFT)
        note1 = T("Stress is the slope of the", 30, INK2)
        note2 = T("straight-line guess:", 30, INK2)
        note3 = T("one order rougher than u", 30, INK2)
        notes = VGroup(note1, note2, note3).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(qans, DOWN, buff=0.4).align_to(card, LEFT)
        base_dot = Dot(ax.c2p(0, -1), radius=0.14, color=GOOD).set_z_index(6)
        base_lab = TX(r"largest compression: $|\sigma| = \rho g L$", size=36)
        base_lab.next_to(base_dot, RIGHT, buff=0.3).shift(0.4 * DOWN)
        st6 = stairs(SIX)
        leg6 = T("FEM, 6 elements", 36, INK).move_to(leg_fem[1], aligned_edge=LEFT)
        self.beat("That answers our second question: the stress is highest at the base, where the column holds up its whole weight. And stresses are rougher than displacements, because they come from the slope of the straight-line guess. More elements, finer steps.",
                  [FadeOut(res), FadeOut(mlab), FadeOut(rings), FadeOut(mids), FadeIn(card)],
                  [FadeIn(base_dot, scale=2), Flash(base_dot, color=GOOD), FadeIn(base_lab), Write(tick),
                   FadeIn(qans)], .1,
                  FadeIn(notes, shift=0.2 * UP), .05,
                  [ReplacementTransform(st3, st6), ReplacementTransform(leg_fem[1], leg6)], .1,
                  w=(.12, .15, .25, .2))
        self.wipe()
