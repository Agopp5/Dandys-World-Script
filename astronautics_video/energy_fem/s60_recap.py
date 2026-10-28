"""S60: recap, the whole road (BRIEF.md S60)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the bowl of panel 1 is Episode 1's spring, K = 20 N/mm, F = 100 N: Pi(q) = 10 q^2 - 100 q
def Pi1(q):
    return 10 * q ** 2 - 100 * q
assert np.isclose(Pi1(0), 0) and np.isclose(Pi1(10), 0) and np.isclose(Pi1(5), -250)
_qs = np.linspace(0, 10, 1001)
assert np.isclose(_qs[np.argmin(Pi1(_qs))], 5)                      # the bottom of the bowl is q = 5 mm
# panel 2's block matrix [[k1 + k2, -k2], [-k2, k2]] with Episode 2's numbers gives q1 = 1.5, q2 = 2.5
assert np.allclose(np.linalg.solve([[40 + 20, -20], [-20, 20]], [40, 20]), [1.5, 2.5])
# panel 3's sketch: bar fixed at x = 0 under a uniform load f (E A = f = L = 1). Exact u = x - x^2/2.
# Three linear elements (k = E A / l = 3, nodal loads c l / 2 = 1/6) land exactly on it at the nodes.
_q = np.linalg.solve(3 * np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 1]]), np.array([2, 2, 1]) / 6)
_xn = np.array([1, 2, 3]) / 3
assert np.allclose(_q, _xn - _xn ** 2 / 2)
assert np.allclose((_xn - _xn ** 2 / 2) / 0.5, 2 * _xn - _xn ** 2)  # drawn as H (2 xi - xi^2), tip = H

SL, SR = np.array([-3.6, -0.375, 0]), np.array([3.6, -0.375, 0])   # the two panel slots
PW, PH, SHIFT = 6.5, 6.75, 7.2


def card_at(c):
    return RoundedRectangle(width=PW, height=PH, corner_radius=0.22, stroke_color=HAIR,
                            stroke_width=2.5, fill_opacity=0).move_to(c)


def num(n, size=40, r=0.3, color=INK):
    c = Circle(radius=r, stroke_color=color, stroke_width=3)
    return VGroup(c, M(str(n), size=size, color=color).move_to(c))


def badge_at(n, c):
    return num(n).move_to([c[0] - PW / 2 + 0.5, c[1] + PH / 2 - 0.5, 0])


def tag_at(s, c):
    t = T(s, size=36, color=GOOD)
    g = VGroup(SurroundingRectangle(t, buff=0.15, corner_radius=0.12, color=GOOD, stroke_width=2.5), t)
    return g.move_to([c[0] + PW / 2 - 0.25 - g.width / 2, c[1] + PH / 2 - 0.5, 0])


def step_row(i, words, tex=None):
    g = VGroup(num(i, size=36, r=0.26), T(words, size=38))
    if tex:
        g.add(E(tex, size=44))
    return g.arrange(RIGHT, buff=0.28)


class S60_Recap(VScene):
    budget = 145

    def construct(self):
        # ---- the road: four milestones across the top ----
        names = ["One spring", "Springs", "Elements", "Recipe"]
        items = [VGroup(num(i + 1, size=36, r=0.26), T(n, size=36)).arrange(RIGHT, buff=0.18)
                 for i, n in enumerate(names)]
        seps = [M(r"\rightarrow", size=36, color=MUTED) for _ in range(3)]
        road = VGroup(items[0], seps[0], items[1], seps[1], items[2], seps[2], items[3])
        road.arrange(RIGHT, buff=0.22).move_to([0, 3.5, 0])
        for i, it in enumerate(items):
            it.set_color(INK if i == 0 else MUTED)

        def road_to(cur):
            return [it.animate.set_color(INK if i == cur else (INK2 if i < cur else MUTED))
                    for i, it in enumerate(items)]

        conn = Arrow([-0.34, SL[1], 0], [0.34, SL[1], 0], buff=0, color=INK2, stroke_width=6,
                     max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)

        # ---- panel 1: one spring, one bowl ----
        cx = SL[0]
        card1, b1 = card_at(SL), badge_at(1, SL)
        eq1 = E(r"\Pi|=|U|-|W", size=56).move_to([cx + 0.65, 2.05, 0])
        ax = Axes(x_range=[0, 10.6, 5], y_range=[-270, 30, 100], x_length=3.7, y_length=3.3, tips=False,
                  axis_config={"color": AXIS, "include_ticks": False, "stroke_width": 2})
        ax.move_to([cx + 0.8, -0.85, 0])
        lq = E("q", size=44).next_to(ax.c2p(10.6, 0), RIGHT, buff=0.15)
        lP = E(r"\Pi", size=44).next_to(ax.c2p(0, 30), UP, buff=0.15)
        bowl = ax.plot(Pi1, x_range=[0, 10], color=GOLD, stroke_width=5)
        note1 = T("the real displacement", size=32, color=MUTED).next_to(ax.c2p(5, -250), DOWN, buff=0.35)
        qt = ValueTracker(0.5)
        top = np.array([cx - 2.3, 1.3, 0])
        ceil = wall(top, side=UP, h=0.9)

        def hang():
            L = 0.85 + 0.14 * qt.get_value()          # the weight drops as q grows
            end = top + DOWN * L
            blk = Rectangle(width=0.7, height=0.5, stroke_color=INK2, stroke_width=3, fill_color=SURFACE,
                            fill_opacity=1).next_to(end, DOWN, buff=0)
            return VGroup(spring(top, end, coils=5, amp=0.17), blk,
                          force(blk.get_bottom(), d=DOWN, length=0.65, label="F"),
                          E("K", size=40).next_to(top + DOWN * L / 2, RIGHT, buff=0.32))
        icon = always_redraw(hang)
        dot = always_redraw(lambda: Dot(ax.c2p(qt.get_value(), Pi1(qt.get_value())), radius=0.1,
                                        color=INK).set_z_index(3))
        drop = always_redraw(lambda: DashedLine(ax.c2p(qt.get_value(), 0),
                                                ax.c2p(qt.get_value(), Pi1(qt.get_value())),
                                                color=SKY, stroke_width=3))
        qdot = always_redraw(lambda: Dot(ax.c2p(qt.get_value(), 0), radius=0.07, color=SKY))
        p1 = VGroup(card1, b1, eq1, ax, lq, lP, bowl, note1, ceil, icon, drop, qdot, dot)

        self.beat("Let's step back and look at the whole road. We started with one spring and one idea: the "
                  "real displacement makes Pi, strain energy minus work potential, as small as possible.",
                  FadeIn(road, lag_ratio=0.15),
                  [Create(card1), FadeIn(b1), FadeIn(ceil), FadeIn(icon)],
                  [Write(eq1), Create(ax), FadeIn(lq), FadeIn(lP), Create(bowl), FadeIn(dot), FadeIn(drop),
                   FadeIn(qdot)],
                  Indicate(eq1[2], color=MINT, scale_factor=1.3),
                  Indicate(eq1[4], color=EMBER, scale_factor=1.3),
                  qt.animate.set_value(5),
                  FadeIn(note1), .04,
                  w=(.16, .16, .2, .1, .1, .18, .06))
        for m in (icon, dot, drop, qdot):
            m.clear_updaters()

        # ---- panel 2: many springs, one matrix ----
        cx = SR[0]
        card2, b2, tag2 = card_at(SR), badge_at(2, SR), tag_at("Homework Problem 1", SR)
        fig = two_spring_fig(left=(cx - 2.75, 1.2), L=2.0, disps=False)   # q labels would collide with k2
        bridge = E(r"\partial|\Pi|/\partial|q_i|=|0", size=48, cmap={"q_i": SKY}).move_to([cx, -0.3, 0])
        Kmat = Matrix([["k_1|+|k_2", "-|k_2"], ["-|k_2", "k_2"]], h_buff=1.75, v_buff=0.95,
                      element_to_mobject=lambda s: E(s, size=48), element_alignment_corner=ORIGIN)
        Kmat.get_brackets().set_color(INK)
        ents = Kmat.get_entries()
        Keq = VGroup(E("K|=", size=48), Kmat).arrange(RIGHT, buff=0.25).move_to([cx, -2.05, 0])
        p2 = VGroup(card2, b2, tag2, fig, bridge, Keq)

        def ind(m):
            return Indicate(m, color=INK, scale_factor=1.2)

        self.beat("For many springs, that idea gave one equation per unknown, and a stiffness matrix built from "
                  "little blocks. That's how you solved problem one.",
                  [GrowArrow(conn), Create(card2), FadeIn(b2), FadeIn(fig), *road_to(1)],
                  Write(bridge),
                  Write(Keq),
                  [ind(fig.s1), ind(fig.k1), ind(ents[0][0])],
                  [ind(fig.s2), ind(fig.k2), ind(ents[0][2]), ind(ents[1]), ind(ents[2]), ind(ents[3])],
                  FadeIn(tag2, shift=UP * 0.2), .12,
                  w=(.2, .14, .2, .1, .12, .12))

        # ---- panel 3: a bar, cut into pieces that are springs ----
        card3, b3 = card_at(SR), badge_at(3, SR)
        x0, x1, yp, H, yb = cx - 2.6, cx + 2.2, -0.35, 1.1, -1.3
        Lb = x1 - x0
        ueq = E(r"U|=|\frac12 \int_0^L EA \Big(\frac{du}{dx}\Big)^2 dx", size=48).move_to([cx + 0.35, 1.75, 0])
        base = Line([x0, yp, 0], [x1, yp, 0], color=AXIS, stroke_width=2)
        exact = dashed(ParametricFunction(lambda t: np.array([x0 + Lb * t, yp + H * (2 * t - t * t), 0]),
                                          t_range=[0, 1], color=MUTED, stroke_width=3)).set_stroke(MUTED, 3)
        line1 = Line([x0, yp, 0], [x1, yp + H, 0], color=SKY, stroke_width=5)     # one assumed shape, u = a x
        xs = [x0 + Lb * k / 3 for k in range(4)]
        pts = [np.array([x, yp + H * (2 * t - t * t), 0]) for t, x in zip([0, 1 / 3, 2 / 3, 1], xs)]
        poly = VMobject(stroke_color=SKY, stroke_width=5).set_points_as_corners(pts)  # straight on each piece
        pdots = VGroup(*[Dot(p, radius=0.07, color=SKY) for p in pts]).set_z_index(3)
        ulab = E("u|(x)", size=40).next_to(pts[-1], RIGHT, buff=0.15)
        bar3 = bar(x0, x1, y=yb)
        wall3 = wall([x0, yb, 0], side=LEFT, h=1.0)
        fem3 = fem_bar(xs, y=yb)
        for nd in fem3.nodes:
            nd.set_z_index(3)
        springs3 = [spring([xs[i], yb, 0], [xs[i + 1], yb, 0], coils=4, amp=0.2) for i in range(3)]
        keq = VGroup(T("each piece:", size=36, color=INK2), E(r"k|=|\frac{EA}{l}", size=56))
        keq.arrange(RIGHT, buff=0.3).move_to([cx, -2.85, 0])

        self.beat("For a bar, we found its strain energy, and the trick of assuming a shape. Finite elements use "
                  "the simplest shape, a straight line, on many short pieces. Each piece is just a spring, E A "
                  "over l.",
                  [FadeOut(p1, shift=LEFT * 2), p2.animate.shift(LEFT * SHIFT).fade(0.5), *road_to(2),
                   Create(card3), FadeIn(b3)],
                  [FadeIn(wall3), FadeIn(bar3), Write(ueq)], .03,
                  [Create(base), Create(exact), Create(line1), FadeIn(ulab)], .03,
                  [FadeIn(fem3), FadeOut(bar3), Transform(line1, poly), FadeIn(pdots, lag_ratio=0.3)], .05,
                  [*[Transform(fem3.elems[i], springs3[i]) for i in range(3)], *[FadeOut(t) for t in fem3.tags]],
                  Write(keq), .07,
                  w=(.1, .12, .14, .2, .14, .12))
        p3 = VGroup(card3, b3, ueq, base, exact, line1, pdots, ulab, wall3, *fem3.elems, *fem3.nodes, keq)

        # ---- panel 4: the recipe, on the homework bar ----
        card4, b4, tag4 = card_at(SR), badge_at(4, SR), tag_at("Homework Problem 2", SR)
        x0, yf = cx - 2.5, 1.35
        wall4 = wall([x0, yf, 0], side=LEFT, h=1.0)
        fem4 = fem_bar([x0, x0 + 2.0, x0 + 4.0], y=yf, elem_labels=False)
        dist4 = dist_load(x0 + 0.15, x0 + 3.85, yf - 0.55, n=8, d=LEFT)
        flab = E("f", size=40).move_to([x0 + 4.25, yf - 0.55, 0])
        P1f = force([x0 + 2.0, yf + 0.5, 0], d=RIGHT, length=0.8, label="P_1")
        P2f = force([x0 + 4.0, yf + 0.5, 0], d=RIGHT, length=0.8, label="P_2")
        fig4 = VGroup(wall4, fem4, dist4, flab, P1f, P2f)
        rows = VGroup(step_row(1, "Assemble", r"K|,\;|F"), step_row(2, "Remove the supports"),
                      step_row(3, "Solve", "K|q|=|F"), step_row(4, "Find the stresses", r"\sigma"),
                      step_row(5, "Removed rows give", "R"))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([cx, -1.65, 0])
        rows.align_to(np.array([cx - 2.8, 0, 0]), LEFT)
        p4 = VGroup(card4, b4, tag4, fig4, rows)

        def rin(r):
            return FadeIn(r, shift=RIGHT * 0.3)

        self.beat("Then the recipe, five steps: assemble, remove the supports, solve, find the stresses, and use "
                  "the removed rows for the reactions. That's how you solved problem two.",
                  [FadeOut(p2, shift=LEFT * 2), p3.animate.shift(LEFT * SHIFT).fade(0.5), *road_to(3),
                   Create(card4), FadeIn(b4), FadeIn(fig4)],
                  rin(rows[0]), rin(rows[1]), rin(rows[2]), rin(rows[3]), rin(rows[4]), .1,
                  FadeIn(tag4, shift=UP * 0.2), .16,
                  w=(.16, .07, .1, .06, .1, .1, .15))

        # ---- the one thing to remember ----
        fin = E(r"\Pi|=|U|-|W|\ \Rightarrow\ |K|q|=|F", size=60)
        card5 = panel(fin).move_to([0, -0.2, 0])
        note5 = T("next in your slides: the rotated bar element, for trusses", size=32,
                  color=MUTED).next_to(card5, DOWN, buff=0.6)
        self.beat("If you remember one thing, make it this: finite elements are the energy method, applied to a "
                  "structure cut into pieces simple enough to handle.",
                  [FadeOut(p3, shift=LEFT * 2), FadeOut(p4), FadeOut(conn),
                   *[it.animate.set_color(INK) for it in items]],
                  FadeIn(card5, scale=0.9),
                  self.spotlight(card5), .2,
                  [self.unspot(), FadeIn(note5)], .24,      # lift the dim so the MUTED note stays readable
                  w=(.12, .2, .1, .14),
                  style="slower and deliberate, stressing the key words")
        self.wipe()
