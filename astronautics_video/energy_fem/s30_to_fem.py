"""S30: from one assumed shape to many pieces (BRIEF.md S30)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})


# facts: bar fixed at x = 0, uniform load f, no tip load. Displacement in units of f L^2 / (E A), xi = x / L.
def exact(xi):
    return xi - xi ** 2 / 2          # u = (f / EA)(L x - x^2 / 2)


def assumed(xi):
    return xi / 2                    # u = a x with a = f L / (2 E A)


assert np.isclose(exact(1.0), assumed(1.0))          # same tip: f L^2 / (2 E A)
assert np.isclose(assumed(0.5), 1 / 4)               # assumed middle: 1/4
assert np.isclose(exact(0.5), 3 / 8)                 # exact middle: 3/8
# broken line through the exact curve at the nodes (linear bar elements are nodally exact for this load)
for n_el in (4, 8):
    xs = np.linspace(0, 1, n_el + 1)
    mid = (xs[:-1] + xs[1:]) / 2
    gap = np.max(exact(mid) - (exact(xs[:-1]) + exact(xs[1:])) / 2)
    assert np.isclose(gap, 1 / (8 * n_el ** 2))      # chord error of a parabola: h^2 / 8 with u'' = -1


class S30_To_FEM(VScene):
    budget = 152

    def construct(self):
        ax = axes([0, 1, 0.25], [0, 0.5, 0.25], width=11, height=3.9, xlabel="x", ylabel="u")
        ax.move_to(DOWN * 1.35)
        X = lambda xi: ax.c2p(xi, 0)[0]
        yb = 2.35
        wl = wall(np.array([X(0), yb, 0]), side=LEFT, h=1.3)
        one = bar(X(0), X(1), y=yb, h=0.5)
        fl = dist_load(X(0) + 0.3, X(1) - 0.2, yb + 0.55, n=9, d=RIGHT)
        flab = M("f", size=40, color=ROSE).next_to(fl, RIGHT, buff=0.15)

        ex = dashed(ax.plot(exact, color=INK2, stroke_width=5))
        exlab = T("exact", size=34, color=INK2).next_to(ax.c2p(0.62, exact(0.62)), UL, buff=0.15)
        line = ax.plot(assumed, color=SKY, stroke_width=6)
        llab = M(r"u = a\,x", size=40, color=SKY).next_to(ax.c2p(0.7, assumed(0.7)), DR, buff=0.15)
        gap = Line(ax.c2p(0.5, assumed(0.5)), ax.c2p(0.5, exact(0.5)), color=BAD, stroke_width=7)
        miss = T("missed", size=32, color=BAD).next_to(gap, RIGHT, buff=0.15).shift(DOWN * 0.1)

        self.beat("So assumed shapes work, but one shape for the whole structure is hard to choose, "
                  "and our single straight line missed the curve inside the bar.",
                  [FadeIn(wl), FadeIn(one), FadeIn(fl), FadeIn(flab), Create(ax)],
                  [Create(ex), FadeIn(exlab)], [Create(line), FadeIn(llab)], [Create(gap), FadeIn(miss)],
                  Indicate(gap, color=BAD), w=(.2, .2, .2, .2, .2))

        # ---- beat 2: chop into 4 elements, one straight segment each
        def pts(vals):
            n = len(vals) - 1
            return [ax.c2p(i / n, v) for i, v in enumerate(vals)]

        xs4 = [X(i / 4) for i in range(5)]
        fb4 = fem_bar(xs4, y=yb, h=0.5)
        ex4 = [exact(i / 4) for i in range(5)]
        v = [ValueTracker(val) for val in ex4]
        broken = always_redraw(lambda: VMobject(color=SKY, stroke_width=7).set_points_as_corners(
            pts([t.get_value() for t in v])))
        dots = VGroup(*[Dot(ax.c2p(i / 4, ex4[i]), radius=0.1, color=SKY) for i in range(5)])
        for i, dt in enumerate(dots):
            dt.add_updater(lambda m, i=i: m.move_to(ax.c2p(i / 4, v[i].get_value())))
        dots.set_z_index(3)
        with self.say("Here's the way out, and it's the whole idea of finite elements. Chop the bar into short "
                      "pieces. In each piece, use the simplest shape there is, a straight line. "
                      "The pieces join at shared points.") as d:
            self.play(FadeOut(line), FadeOut(llab), FadeOut(gap), FadeOut(miss), run_time=.12 * d)
            self.play(FadeOut(one), FadeIn(fb4), run_time=.2 * d)
            self.play(Create(broken), run_time=.3 * d)
            self.play(FadeIn(dots[1:4], scale=1.6), run_time=.13 * d)
            self.play(Indicate(dots[1:4], color=GOLD, scale_factor=1.6), run_time=.17 * d)
        broken.set_z_index(2)

        # ---- beat 3: the unknowns q_1..q_4 at the joints; the broken line follows each one
        qlab = VGroup()
        for i in range(1, 5):
            lb = M("q_%d" % i, size=44, color=SKY)
            lb.add_updater(lambda m, i=i: m.next_to(ax.c2p(i / 4, v[i].get_value()), UL, buff=0.12))
            qlab.add(lb)
        dq = VGroup(*[disp(np.array([xs4[i], yb - 0.25, 0]), label="q_%d" % i, length=0.7, below=0.3)
                      for i in range(1, 5)])
        with self.say("And now the unknowns are just the displacements of those shared points: q one, q two, "
                      "q three, q four. A handful of numbers again, exactly like our springs.") as d:
            self.play(FadeIn(dq), run_time=.1 * d)
            for i in range(1, 5):
                self.play(FadeIn(qlab[i - 1]), v[i].animate.set_value(ex4[i] + 0.11),
                          run_time=.08 * d, rate_func=smooth)
                self.play(v[i].animate.set_value(ex4[i]), run_time=.08 * d)
            self.play(Indicate(qlab, color=GOLD), run_time=.18 * d)
            self.wait(.08 * d)

        # ---- beat 4: 8 elements hug the curve
        for m in [*qlab, *dots]:
            m.clear_updaters()
        xs8 = [X(i / 8) for i in range(9)]
        fb8 = fem_bar(xs8, y=yb, h=0.5, elem_labels=False)
        ex8 = [exact(i / 8) for i in range(9)]
        broken8 = VMobject(color=SKY, stroke_width=7).set_points_as_corners(pts(ex8)).set_z_index(2)
        dots8 = VGroup(*[Dot(p, radius=0.09, color=SKY) for p in pts(ex8)]).set_z_index(3)
        frozen = broken.copy().clear_updaters()
        self.remove(broken)
        self.add(frozen)
        note = T("8 elements", size=36, color=INK2).next_to(ax.c2p(0.92, 0.12), UP, buff=0)
        with self.say("Lots of short straight lines can follow any curve. And each piece is so simple that we "
                      "can work out its energy once, for good.") as d:
            self.play(FadeOut(qlab), FadeOut(dq), run_time=.12 * d)
            self.play(FadeOut(fb4), FadeIn(fb8), Transform(frozen, broken8), FadeOut(dots),
                      FadeIn(dots8), FadeIn(note), run_time=.35 * d)
            el = fb8.elems[3]
            self.play(Circumscribe(el, color=GOLD), Indicate(
                Line(ax.c2p(3 / 8, ex8[3]), ax.c2p(4 / 8, ex8[4]), color=GOLD, stroke_width=9)),
                run_time=.3 * d)
            self.wait(.23 * d)

        # ---- beat 5: key box
        u_eq = E(r"U|=|\tfrac12\int_0^L EA\Big(\frac{du}{dx}\Big)^2 dx", size=48)
        w_eq = E(r"W|=|P|\,|u|(L) + \int_0^L |f|\,|u|\,dx", size=48)
        p_eq = E(r"\text{assume a shape} \Rightarrow |\Pi| \text{ depends on a few numbers}", size=44)
        fig = [m for m in self.mobjects]
        with self.say("So, stepping back: the strain energy of a bar is one half the integral of E A times strain "
                      "squared. Assume a shape, and Pi becomes a bowl again. Next time: one element, worked out "
                      "completely.") as d:
            self.play(*[FadeOut(m) for m in fig], run_time=.1 * d)
            kb = key_box(u_eq, w_eq, p_eq, label="KEY IDEA")
            self.play(FadeIn(kb), run_time=.15 * d)
            self.play(Circumscribe(u_eq, color=MINT), run_time=.25 * d)
            self.play(Circumscribe(p_eq, color=GOLD), run_time=.25 * d)
            self.wait(.25 * d)
        self.wipe()
