"""S02: work under a growing force (BRIEF.md S02)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts
KV, QV = 20, 5                      # N/mm, mm
FV = KV * QV
assert FV == 100                    # F = K q
assert np.isclose(0.5 * KV * QV ** 2, 250)          # one half K q squared, N mm
_n = 1000                           # midpoint sum of K u du (exact for a straight line)
assert np.isclose(sum(KV * (i + .5) * QV / _n * QV / _n for i in range(_n)), 250)
assert np.isclose(0.5 * QV * FV, 250)               # half base times height


class S02_Work(VScene):
    budget = 214

    def construct(self):
        # ---------- beat 1: constant force, rectangle ----------
        GY = 0.9
        ground = Line([-6.6, GY, 0], [-0.6, GY, 0], color=INK2, stroke_width=3)
        box = Square(1.1, color=INK2, fill_color=SURFACE, fill_opacity=1).move_to([-5.0, GY + 0.55, 0])
        x0 = box.get_center()[0]
        push = always_redraw(lambda: force(box.get_left(), RIGHT, length=1.0, tail=True, label="F"))
        ax1 = axes((0, 4, 1), (0, 3, 1), width=4.6, height=2.8, xlabel="", ylabel="")
        ax1.move_to([3.6, 0.3, 0])
        ax1_lab = VGroup(T("distance", size=30, color=INK2).next_to(ax1.c2p(4, 0), DOWN, buff=.25),
                         T("force", size=30, color=INK2).next_to(ax1.c2p(0, 3), UP, buff=.2))
        flat = Line(ax1.c2p(0, 2), ax1.c2p(3.6, 2), color=ROSE, stroke_width=5)
        flat_lab = E("F", size=40).next_to(flat, UP, buff=0.15).align_to(flat, RIGHT)
        rect = always_redraw(lambda: Polygon(
            ax1.c2p(0, 0), ax1.c2p(max(box.get_center()[0] - x0, 1e-3), 0),
            ax1.c2p(max(box.get_center()[0] - x0, 1e-3), 2), ax1.c2p(0, 2),
            color=EMBER, stroke_width=2, fill_color=EMBER, fill_opacity=.45))
        with self.say("Start with work. When a constant force pushes something through a distance, it does "
                      "work: force times distance. On a graph of force against distance, that's the area of a "
                      "rectangle.") as d:
            self.play(FadeIn(ground), FadeIn(box), FadeIn(push), Create(ax1), FadeIn(ax1_lab), Create(flat), FadeIn(flat_lab),
                      run_time=.2 * d)
            self.add(rect)
            self.play(box.animate.shift(RIGHT * 3), run_time=.35 * d, rate_func=linear)
            rect.clear_updaters()
            push.clear_updaters()
            dist = span(np.array([x0, GY, 0]), np.array([x0 + 3, GY, 0]), "d", side=DOWN)
            fd = E(r"F|\cdot|d", size=44).move_to(Polygon(ax1.c2p(0, 0), ax1.c2p(3, 0), ax1.c2p(3, 2),
                                                          ax1.c2p(0, 2)).get_center())
            self.play(FadeIn(dist), run_time=.15 * d)
            self.play(Write(fd), Indicate(rect, color=EMBER, scale_factor=1.03), run_time=.2 * d)
            self.wait(.1 * d)
        beat1 = VGroup(ground, box, push, ax1, ax1_lab, flat, flat_lab, rect, dist, fd)

        # ---------- beat 2: the spring, force grows with stretch ----------
        SY, WX, REST, SC = 2.5, -6.2, -3.6, 2.2 / QV
        ut = ValueTracker(0.0)

        def npos():
            return np.array([REST + SC * ut.get_value(), SY, 0])

        wl = wall(np.array([WX, SY, 0]), side=LEFT, h=1.3)
        spr = always_redraw(lambda: spring(np.array([WX, SY, 0]), npos(), label="K"))
        nd = always_redraw(lambda: node(npos(), r=.11))
        pull = always_redraw(lambda: force(npos(), RIGHT, length=0.2 + 1.1 * ut.get_value() / QV))
        rest_tick = DashedLine([REST, SY - 0.35, 0], [REST, SY - 0.85, 0], color=MUTED)

        def stretch_arrow():
            v = ut.get_value()
            if v < 0.05:
                return VGroup()
            a = Arrow([REST, SY - 0.6, 0], [REST + SC * v, SY - 0.6, 0], buff=0, color=SKY, stroke_width=5,
                      max_tip_length_to_length_ratio=.3)
            return VGroup(a, E("u", size=36).next_to(a, RIGHT, buff=.12))
        sarr = always_redraw(stretch_arrow)

        ax = axes((0, 6, 1), (0, 120, 20), width=5.2, height=3.3, xlabel="", ylabel="")
        ax.move_to([-3.9, -1.3, 0])
        ax_lab = VGroup(E("u", size=40).next_to(ax.c2p(6, 0), RIGHT, buff=.2),
                        T("force", size=30, color=INK2).next_to(ax.c2p(0, 120), UP, buff=.2))

        def gpt():
            v = max(ut.get_value(), 1e-3)
            return ax.c2p(v, KV * v)
        gline = always_redraw(lambda: Line(ax.c2p(0, 0), gpt(), color=LILAC, stroke_width=6))
        gdot = always_redraw(lambda: Dot(gpt(), color=LILAC, radius=.1))
        with self.say("A spring is different. If you slam the full force on at once, the spring bounces around. "
                      "We want the slow, settled stretch, so we pull gently, and the force grows as the spring "
                      "stretches.") as d:
            self.play(FadeOut(beat1), run_time=.1 * d)
            self.play(FadeIn(wl), FadeIn(spr), FadeIn(nd), FadeIn(pull), FadeIn(rest_tick), Create(ax), FadeIn(ax_lab),
                      run_time=.2 * d)
            self.add(sarr, gline, gdot)
            self.wait(.15 * d)
            self.play(ut.animate.set_value(QV), run_time=.45 * d, rate_func=smooth)
            self.wait(.1 * d)
        for m in (spr, nd, pull, sarr, gline, gdot):
            m.clear_updaters()

        # ---------- beat 3: K u, q, F = K q ----------
        top = ax.c2p(QV, FV)
        ku = E("K|u", size=44).next_to(top, RIGHT, buff=.3).shift(DOWN * .5)
        vguide = DashedLine(ax.c2p(QV, 0), top, color=MUTED)
        hguide = DashedLine(ax.c2p(0, FV), top, color=MUTED)
        qlab = E("q", size=40).next_to(ax.c2p(QV, 0), DOWN, buff=.2)
        flab = E("F|=|K|q", size=44).next_to(ax.c2p(1.6, FV), UP, buff=.2)
        self.beat("At a stretch u, the force is K times u. It starts at zero and climbs in a straight line, up "
                  "to its full value at the final stretch q. That full value is F, which equals K q.",
                  [FadeIn(ku), Indicate(gline, color=LILAC)], .1,
                  [Create(vguide), FadeIn(qlab)], .1,
                  [Create(hguide), Write(flab)], w=(.3, .25, .25))

        # ---------- beat 4: thin strips ----------
        graph = ax.plot(lambda x: KV * x, x_range=[0, QV], color=LILAC)
        strips = ax.get_riemann_rectangles(graph, x_range=[0, QV], dx=QV / 20, color=MINT, fill_opacity=.45,
                                           stroke_width=1, stroke_color=BG)
        hi = strips[12]
        hi_box = hi.copy().set_fill(MINT, opacity=1).set_stroke(INK, 2)
        slab = E(r"K|u|\,du", size=44).move_to(ax.c2p(1.3, 78))
        sptr = Arrow(slab.get_bottom() + DOWN * .05, hi.get_top() + UP * .02, buff=.05, color=INK2,
                     stroke_width=3, max_tip_length_to_length_ratio=.2)
        self.beat("How much work does a force that keeps changing do? Chop the stretch into tiny steps d u. "
                  "Over one tiny step the force barely changes, so the work is force times d u: a thin strip.",
                  .25, LaggedStart(*[FadeIn(s) for s in strips], lag_ratio=.08), .1,
                  [FadeIn(hi_box), GrowArrow(sptr), Write(slab)], w=(.3, .35))

        # ---------- beat 5: strips merge into the triangle ----------
        tri = Polygon(ax.c2p(0, 0), ax.c2p(QV, 0), top, color=MINT, stroke_width=3, fill_color=MINT,
                      fill_opacity=.55)
        eq = E(r"\int_0^{q} K u\,du|=|\tfrac12|\,q|\cdot|Kq|=|\tfrac12 K q^2", size=46)
        paint(eq, {3: SKY, 5: ROSE, 7: MINT})
        fit(eq, 7.0, 1.5)
        eq.move_to([3.2, 0.0, 0])
        base = Line(ax.c2p(0, 0), ax.c2p(QV, 0), color=SKY, stroke_width=10)
        height = Line(ax.c2p(QV, 0), top, color=ROSE, stroke_width=10)
        with self.say("Add up all the strips, and you get the area under the force line. Here it's a triangle: "
                      "base q, height K q. Half base times height: one half K q squared. That's the integral of "
                      "K u d u, from zero to q.") as d:
            self.play(ReplacementTransform(VGroup(strips, hi_box), tri), FadeOut(slab), FadeOut(sptr),
                      run_time=.2 * d)
            self.play(FadeIn(eq[3]), ShowPassingFlash(base, time_width=.8), run_time=.12 * d)
            self.play(FadeIn(eq[4]), FadeIn(eq[5]), ShowPassingFlash(height, time_width=.8), run_time=.12 * d)
            self.play(FadeIn(eq[2]), Indicate(tri, color=MINT, scale_factor=1.03), run_time=.13 * d)
            self.play(Write(eq[6]), Write(eq[7]), run_time=.15 * d)
            self.play(Write(eq[0]), Write(eq[1]), run_time=.2 * d)
            self.wait(.08 * d)

        # ---------- beat 6: numbers ----------
        eq2 = E(r"\tfrac12|(20)|(5)^2|=|250\text{ N mm}", size=46)
        paint(eq2, {1: LILAC, 2: SKY, 4: MINT})
        fit(eq2, 7.0, 1.2)
        eq2.next_to(eq, DOWN, buff=.7)
        k_note = E(r"K|=|20\text{ N/mm}", size=40)
        paint(k_note, {2: LILAC})
        q_note = E(r"q|=|5\text{ mm}", size=40)
        paint(q_note, {2: SKY})
        notes = VGroup(k_note, q_note).arrange(RIGHT, buff=.7).next_to(eq, UP, buff=.6)
        self.beat("With numbers: K is twenty newtons per millimeter, and the final stretch is five millimeters. "
                  "One half, times twenty, times five squared, is two hundred fifty newton millimeters.",
                  FadeIn(k_note), FadeIn(q_note), Write(eq2[:4]), [Write(eq2[4]), FadeIn(glow(eq2[4], MINT))],
                  .25, w=(.2, .2, .25, .15))
        self.wipe()
