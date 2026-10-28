"""S28: how good is the assumed straight-line shape? (BRIEF.md S28)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts, in units of f L^2 / EA with xi = x / L
xi = np.linspace(0, 1, 401)
exact = xi - xi ** 2 / 2                      # u_exact = (f/EA)(L x - x^2/2)
guess = xi / 2                                # u = a x, a = f L / (2 EA)  ->  a x = (1/2) xi
assert np.allclose(np.gradient(exact, xi, edge_order=2), 1 - xi, atol=1e-9)   # strain f(L - x)/EA
assert np.isclose(exact[-1], 1 / 2) and np.isclose(guess[-1], 1 / 2)   # tip: f L^2 / (2 EA), both
assert np.isclose(0.5 - 0.5 ** 2 / 2, 3 / 8) and np.isclose(0.5 / 2, 1 / 4)   # middle: 3/8 vs 1/4
assert np.all(guess[1:-1] < exact[1:-1])      # the line is low everywhere inside

LX = -3.55     # centre of the left half
RX = 3.6       # centre of the right half
UCM = {r"u_{\text{exact}}": SKY, r"u_{\text{line}}": SKY, r"u_{\text{exact}}(L)": SKY,
       r"u_{\text{line}}(L)": SKY, r"u_{\text{line}}(\tfrac{L}{2})": SKY,
       r"u_{\text{exact}}(\tfrac{L}{2})": SKY}


def rib_outline(x0, chord, t=0.34, m=0.06, p=0.4, n=80):
    """A cambered, thick airfoil outline (a wing rib), as points."""
    b = np.linspace(0, np.pi, n)
    xs = (1 - np.cos(b)) / 2
    yt = 5 * t * (0.2969 * np.sqrt(xs) - 0.1260 * xs - 0.3516 * xs ** 2 + 0.2843 * xs ** 3 - 0.1036 * xs ** 4)
    yc = np.where(xs < p, m / p ** 2 * (2 * p * xs - xs ** 2), m / (1 - p) ** 2 * (1 - 2 * p + 2 * p * xs - xs ** 2))
    up = [np.array([x0 + chord * x, chord * (c + y), 0]) for x, c, y in zip(xs, yc, yt)]
    lo = [np.array([x0 + chord * x, chord * (c - y), 0]) for x, c, y in zip(xs, yc, yt)]
    return up + lo[::-1][1:-1], (lambda x: chord * (m / p ** 2 * (2 * p * x - x * x) if x < p else
                                              m / (1 - p) ** 2 * (1 - 2 * p + 2 * p * x - x * x))), \
        (lambda x: chord * 5 * t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3
                                    - 0.1036 * x ** 4))


class S28_Compare_Exact(VScene):
    budget = 170

    def construct(self):
        # ---------- the bar with a cut at x ----------
        y0 = 0.4
        xa, xb, xc = -6.5, -0.7, -3.3
        wl = wall(np.array([xa, y0, 0]), side=LEFT, h=1.8)
        br = bar(xa, xb, y=y0, h=0.8)
        ld = dist_load(xa + 0.2, xb - 0.1, y0 + 0.8, n=9, d=RIGHT, length=0.5)
        fl = M("f", size=52, color=ROSE).move_to([(xa + xc) / 2, y0 + 1.45, 0])
        sketch = VGroup(wl, br, ld, fl)
        cut = DashedLine([xc, y0 - 1.0, 0], [xc, y0 + 1.4, 0], color=INK, stroke_width=4)
        outer = Rectangle(width=xb - xc, height=0.8, stroke_color=ROSE, stroke_width=6,
                          fill_color=ROSE, fill_opacity=0.18).move_to([(xb + xc) / 2, y0, 0])
        b_out = Brace(Line([xc, y0 - 0.4, 0], [xb, y0 - 0.4, 0]), DOWN, color=INK2)
        l_out = E(r"f|(L-x)", size=52).next_to(b_out, DOWN, buff=0.15)
        b_x = Brace(Line([xa, y0 - 0.4, 0], [xc, y0 - 0.4, 0]), DOWN, color=INK2)
        l_x = M("x", size=52).next_to(b_x, DOWN, buff=0.15)
        cutgrp = VGroup(cut, outer, b_out, l_out, b_x, l_x)

        eps = E(r"\varepsilon|=|\frac{f(L-x)}{EA}", size=56).move_to([RX, 1.5, 0])
        paint(eps, {2: INK})
        uex = E(r"u_{\text{exact}}|=|\frac{f}{EA}\Big(Lx - \frac{x^2}{2}\Big)", size=52, cmap=UCM)
        fit(uex, 6.6, 2)
        uex.move_to([RX, -0.6, 0])

        # ---------- the plot: u in units of f L^2 / EA ----------
        ax = Axes(x_range=[0, 1.08, 0.5], y_range=[0, 0.62, 0.125], x_length=6.2, y_length=5.5,
                  axis_config={"color": AXIS, "stroke_width": 3, "include_ticks": True, "tip_length": 0.22})
        ax.move_to([LX + 0.3, -0.45, 0])
        xt = VGroup(*[M(s, size=44, color=INK2).next_to(ax.c2p(v, 0), DOWN, buff=0.22)
                      for s, v in [("0", 0), ("L/2", 0.5), ("L", 1)]])
        xl = M("x", size=44).next_to(ax.c2p(1.08, 0), RIGHT, buff=0.15)
        yl = VGroup(M("u", size=52, color=SKY), M(r"\Big[\frac{fL^2}{EA}\Big]", size=44, color=INK2))
        yl.arrange(RIGHT, buff=0.15).next_to(ax.c2p(0, 0.62), UP, buff=0.15).shift(RIGHT * 0.6)
        frame_ax = VGroup(ax, xt, xl, yl)
        ex = ax.plot(lambda t: t - t * t / 2, x_range=[0, 1], color=SKY, stroke_width=7)
        ex_lab = M(r"u_{\text{exact}}", size=50, color=SKY).next_to(ax.c2p(0.3, 0.29), UL, buff=0.05)

        with self.say("How good is that guess? This simple bar has an exact answer. Cut it at x: the piece beyond "
                      "the cut carries f times L minus x, so the strain there is f times L minus x, over E A. "
                      "Integrate that, and you get u of x equals f over E A, times L x minus x squared over two.") as d:
            # intro ~0.20 of the line, the cut ~0.25, the strain ~0.19, the integral ~0.36
            self.play(FadeIn(sketch), run_time=.08 * d)
            self.wait(.12 * d)
            self.play(Create(cut), FadeIn(outer), run_time=.08 * d)
            self.play(GrowFromCenter(b_x), FadeIn(l_x), run_time=.05 * d)
            self.play(GrowFromCenter(b_out), Write(l_out), run_time=.08 * d)
            self.wait(.04 * d)
            self.snap("cut")
            self.play(Write(eps), run_time=.1 * d)
            self.wait(.09 * d)
            self.play(Write(uex), run_time=.12 * d)
            self.play(FadeOut(sketch), FadeOut(cutgrp), Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl),
                      run_time=.07 * d)
            self.play(Create(ex), FadeIn(ex_lab), run_time=.1 * d)
            self.wait(.03 * d)

        # ---------- beat 2: the straight line meets the curve at the tip ----------
        ln = dashed(ax.plot(lambda t: t / 2, x_range=[0, 1], color=SKY, stroke_width=6))
        ln_lab = M("u = ax", size=50, color=SKY).next_to(ax.c2p(0.78, 0.39), DR, buff=0.12)
        tip = Dot(ax.c2p(1, 0.5), radius=0.11, color=SKY)
        tip_tick = M(r"\frac{1}{2}", size=44, color=INK2).next_to(ax.c2p(0, 0.5), LEFT, buff=0.18)
        tip_guide = DashedLine(ax.c2p(0, 0.5), ax.c2p(1, 0.5), color=MUTED, stroke_width=2.5)
        t1 = E(r"u_{\text{exact}}(L)|=|\frac{fL^2}{2EA}", size=52, cmap=UCM)
        t2 = E(r"u_{\text{line}}(L)|=|aL|=|\frac{fL^2}{2EA}", size=52, cmap=UCM)
        t1.move_to([RX, 0.9, 0])
        t2.next_to(t1, DOWN, buff=0.7)
        t2.shift((t1[1].get_x() - t2[1].get_x()) * RIGHT)
        tips = VGroup(t1, t2)
        tips.shift((RX - tips.get_center()[0]) * RIGHT)
        g1, g2 = glow(t1[2], SKY), glow(t2[4], SKY)
        self.beat("At the tip, the exact answer is f L squared over two E A. Exactly what our straight line gave.",
                  FadeOut(eps), uex.animate.move_to([RX, 2.6, 0]),
                  [Create(ln), FadeIn(ln_lab)], [FadeIn(tip), Create(tip_guide), FadeIn(tip_tick), Write(t1)],
                  Write(t2), [FadeIn(g1), FadeIn(g2)], .15,
                  w=(.08, .12, .2, .2, .15, .1))

        # ---------- beat 3: checkpoint ----------
        mid_guide = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, 0.58), color=MUTED, stroke_width=3)
        self.beat("Your turn: pause and do checkpoint four point one in your guide. Compare the two at the "
                  "middle of the bar.", .3, Create(mid_guide), Indicate(xt[1], color=SKY, scale_factor=1.3), .2)
        self.checkpoint("4.1", "Assumed u = a x: compare u at the middle with exact")

        # ---------- beat 4: the gap at the middle ----------
        p_ln, p_ex = ax.c2p(0.5, 0.25), ax.c2p(0.5, 0.375)
        d_ln = Dot(p_ln, radius=0.1, color=SKY)
        d_ex = Dot(p_ex, radius=0.1, color=SKY)
        v_ln = M(r"\frac{1}{4}", size=48, color=SKY).move_to(p_ln + RIGHT * 0.55 + DOWN * 0.3)
        v_ex = M(r"\frac{3}{8}", size=48, color=SKY).move_to(p_ex + LEFT * 0.6 + UP * 0.75)
        gap = DoubleArrow(p_ln, p_ex, buff=0.12, color=BAD, stroke_width=5, tip_length=0.2,
                          max_tip_length_to_length_ratio=0.3).shift(LEFT * 0.28)
        area = ax.get_area(ex, x_range=(0, 1), bounded_graph=ax.plot(lambda t: t / 2, x_range=[0, 1]),
                           color=BAD, opacity=0.3)
        m1 = E(r"u_{\text{line}}(\tfrac{L}{2})|=|\frac{1}{4}\,\frac{fL^2}{EA}", size=50, cmap=UCM)
        m2 = E(r"u_{\text{exact}}(\tfrac{L}{2})|=|\frac{3}{8}\,\frac{fL^2}{EA}", size=50, cmap=UCM)
        m1.move_to([RX, 2.1, 0])
        m2.next_to(m1, DOWN, buff=0.6)
        m2.shift((m1[1].get_x() - m2[1].get_x()) * RIGHT)
        VGroup(m1, m2).shift((RX - VGroup(m1, m2).get_center()[0]) * RIGHT)
        n1 = T("Too low everywhere inside the bar", size=36, color=BAD).move_to([RX, -1.2, 0])
        fit(n1, 6.4, 1)
        n2 = T("Tip match: a coincidence, not a rule", size=36, color=MUTED)
        fit(n2, 6.4, 1)
        n2.next_to(n1, DOWN, buff=0.45)
        self.beat("At the middle, the straight line gives one quarter f L squared over E A. The exact answer is "
                  "three eighths. The line sits too low everywhere inside the bar. The tip matching was a lucky "
                  "coincidence, not a rule.",
                  [FadeOut(uex), FadeOut(t1), FadeOut(t2), FadeOut(g1), FadeOut(g2), FadeOut(tip_guide), FadeOut(tip_tick)],
                  [FadeIn(d_ln), FadeIn(v_ln), Write(m1)], .05,
                  [FadeIn(d_ex), FadeIn(v_ex), Write(m2)], GrowFromCenter(gap),
                  [FadeIn(area), FadeIn(n1)], .05,
                  [Circumscribe(tip, color=SKY, shape=Circle), FadeIn(n2)], .1,
                  w=(.05, .2, .2, .1, .22, .15))

        # ---------- beat 5: a real structure ----------
        pts, camber, half = rib_outline(0.0, 6.6)
        rib = Polygon(*pts, color=INK2, stroke_width=4, fill_color=SURFACE, fill_opacity=1)
        holes = VGroup()
        for c in (0.2, 0.42, 0.63, 0.81):
            r = 0.55 * half(c)
            holes.add(Circle(radius=r, color=INK2, stroke_width=3, fill_color=BG, fill_opacity=1)
                      .move_to([6.6 * c, camber(c), 0]))
        spar = VGroup(*[Line([6.6 * c, camber(c) - half(c) * 0.92, 0], [6.6 * c, camber(c) + half(c) * 0.92, 0],
                             color=INK2, stroke_width=5) for c in (0.3, 0.72)])
        ribg = VGroup(rib, holes, spar)
        fit(ribg, 6.5, 4).move_to([RX - 0.05, -0.6, 0])
        qm = T("?", size=130, color=INK, weight=BOLD).move_to([RX + 2.2, 2.0, 0])
        rib_lab = T("a wing rib", size=40, color=MUTED).next_to(ribg, DOWN, buff=0.35)
        s1 = T("Assumed shapes are approximate.", size=40)
        s2 = T("Better shape, better answer.", size=40)
        s3 = T("One good shape for a whole", size=40, color=INK2)
        s4 = T("real structure? Hard.", size=40, color=INK2)
        notes = VGroup(s1, s2, s3, s4).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        s3.shift(DOWN * 0.3)
        s4.shift(DOWN * 0.3)
        fit(notes, 6.5, 6)
        notes.move_to([LX, 0, 0])
        figure = VGroup(ax, xt, xl, yl, ex, ex_lab, ln, ln_lab, tip, mid_guide, d_ln, d_ex, v_ln, v_ex, gap, area)
        self.beat("That's the honest truth about assumed shapes: they're approximate. A better shape gives a "
                  "better answer. But choosing one good shape for a whole real structure is hard.",
                  [FadeOut(figure), FadeOut(m1), FadeOut(m2), FadeOut(n1), FadeOut(n2)], FadeIn(s1), .05,
                  FadeIn(s2), .05, [FadeIn(s3), FadeIn(s4), DrawBorderThenFill(rib), FadeIn(rib_lab)],
                  [FadeIn(holes), Create(spar)], FadeIn(qm, scale=0.5), .15,
                  w=(.08, .12, .15, .22, .1, .1))
        self.wipe()
