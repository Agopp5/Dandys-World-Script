"""S31: elements and nodes (BRIEF.md S31)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: 3 elements, 4 nodes, 4 degrees of freedom; element i runs from node i to node i+1,
# so element 2 has u1 = q2 and u2 = q3.
XS = [-5.4, -2.8, -0.2, 2.4]           # node x positions on screen
YB = 0.3                               # bar centre line
H = 0.5                                # bar height
N_NODES, N_ELEMS = len(XS), len(XS) - 1
assert (N_NODES, N_ELEMS) == (4, 3)
ELEM2 = (2, 3)                         # element 2: global nodes (u1, u2) -> (q2, q3)
assert ELEM2 == (2, 2 + 1)
# exact bar under uniform f plus tip load P = f L / 2 (L = 1): u ~ (L x - x^2/2) + (L/2) x = 1.5 x - x^2/2
def g(t):
    return 1.5 * t - 0.5 * t ** 2
UMAX = 2.0                              # screen height of the tip value
QV = [UMAX * g(t) / g(1.0) for t in (0, 1 / 3, 2 / 3, 1)]
assert np.allclose(np.array(QV) / UMAX, [0, 4 / 9, 7 / 9, 1])


def p(x, y):
    return np.array([x, y, 0.0])


def darrow(x, y, length=0.6):
    """Small SKY displacement arrow starting at x, pointing +x."""
    return Arrow(p(x, y), p(x + length, y), buff=0, color=SKY, stroke_width=6,
                 max_tip_length_to_length_ratio=0.35)


def qlab(i):
    """Global displacement label under node i (1-based)."""
    x = XS[i - 1]
    a = darrow(x, YB - 0.62)
    l = M("q_%d" % i, size=44, color=SKY).next_to(a, DOWN, buff=0.12)
    return VGroup(a, l)


class S31_Discretize(VScene):
    budget = 156

    def construct(self):
        # ---- beat 1: wall, bar chopped into 3 elements, nodes ----
        wl = wall(p(XS[0], YB), side=LEFT, h=1.8)
        fb = fem_bar(XS, y=YB, h=H, elem_labels=False)
        tags = VGroup(*[VGroup(Circle(radius=0.3, color=INK2, stroke_width=3), T(str(i + 1), size=36))
                        .move_to(p((XS[i] + XS[i + 1]) / 2, YB + H / 2 + 0.45)) for i in range(3)])
        tip = force(p(XS[3], YB), d=RIGHT, length=1.2, color=ROSE)
        tip_l = M("P", size=44, color=ROSE).next_to(tip, UP, buff=0.12)
        load = VGroup(tip, tip_l)
        floads = VGroup(*[dist_load(XS[i] + 0.35, XS[i + 1] - 0.75, YB, n=3, d=RIGHT, color=ROSE)
                          for i in range(3)])
        f_l = M("f", size=40, color=ROSE).move_to(p(XS[0] + 0.45, YB + H / 2 + 0.45))

        el_t = T("element", size=40, color=INK).move_to(p((XS[1] + XS[2]) / 2, YB + 2.3))
        el_a = Arrow(el_t.get_bottom(), tags[1].get_top(), buff=0.12, color=INK2,
                     stroke_width=4)
        nd_t = T("nodes", size=40, color=INK).move_to(p(-1.5, YB - 2.2))
        nd_a = VGroup(*[Arrow(nd_t.get_top(), p(x, YB - 0.1), buff=0.15, color=INK2, stroke_width=3,
                              max_tip_length_to_length_ratio=0.08) for x in XS])
        self.beat("Take the bar fixed to a wall, and chop it into three pieces. Each piece is called an element. "
                  "The points where they join, and the two ends, are called nodes.",
                  [FadeIn(wl), FadeIn(fb), FadeIn(tags)], [FadeIn(load), FadeIn(floads), FadeIn(f_l)], .1,
                  [FadeIn(el_t), GrowArrow(el_a), Indicate(VGroup(fb.elems[1], tags[1]), color=LILAC)], .1,
                  [FadeIn(nd_t), LaggedStart(*[GrowArrow(a) for a in nd_a], lag_ratio=.2)],
                  w=(.25, .1, .3, .35))

        # ---- beat 2: q1..q4 under the nodes, 4 degrees of freedom ----
        qs = VGroup(*[qlab(i) for i in range(1, 5)])
        dof = T("4 degrees of freedom", size=44, color=INK).move_to(p(-0.6, YB - 2.55))
        dof[0].set_color(SKY)
        dof_g = glow(dof, SKY)
        dof_s = T("instead of infinitely many", size=32, color=MUTED).next_to(dof, DOWN, buff=0.2)
        self.beat("The displacements of the nodes, q one, q two, q three, q four, are our unknowns. Just four "
                  "numbers, instead of infinitely many. Each one is called a degree of freedom: a number the "
                  "structure is free to choose.",
                  [FadeOut(nd_t), FadeOut(nd_a)],
                  LaggedStart(*[FadeIn(q, shift=.2 * DOWN) for q in qs], lag_ratio=.5), .1,
                  [FadeIn(dof), FadeIn(dof_s)], FadeIn(dof_g),
                  w=(.08, .42, .22, .28))

        # ---- beat 3: straight lines between node values ----
        y0 = YB + 1.35
        base = Line(p(XS[0], y0), p(XS[3], y0), color=AXIS, stroke_width=2)
        pts = [p(x, y0 + v) for x, v in zip(XS, QV)]
        dots = VGroup(*[Dot(q, radius=0.09, color=SKY) for q in pts])
        sticks = VGroup(*[DashedLine(p(x, y0), q, color=MUTED, stroke_width=2) for x, q in zip(XS, pts)])
        broken = VMobject(color=SKY, stroke_width=6).set_points_as_corners(pts)
        u_l = M("u(x)", size=44, color=SKY).next_to(pts[3], RIGHT, buff=0.25)
        exact = dashed(ParametricFunction(lambda t: p(XS[0] + t * (XS[3] - XS[0]), y0 + UMAX * g(t) / g(1.0)),
                                          t_range=[0, 1], color=MUTED, stroke_width=3))
        exact.set_stroke(width=4, opacity=.8)
        plot = VGroup(base, exact, sticks, dots, broken, u_l)
        self.beat("Between the nodes, we assume the displacement is a straight line. So once we know the four "
                  "node values, we know u everywhere.",
                  [FadeOut(el_t), FadeOut(el_a), Create(base)], [Create(sticks), FadeIn(dots), Create(exact)],
                  Create(broken), FadeIn(u_l),
                  w=(.1, .25, .4, .25))

        # ---- beat 4: explode, equal end displacements at each gap, reassemble ----
        ends = VGroup(*[VGroup(Dot(p(XS[i], YB), radius=0.09, color=INK),
                               Dot(p(XS[i + 1], YB), radius=0.09, color=INK)) for i in range(3)])
        pieces = [VGroup(fb.elems[i], tags[i], ends[i], floads[i]) for i in range(3)]
        SH = [0.0, 1.0, 2.0]                     # how far each element slides right
        ya = YB - 0.62
        gaps = VGroup()
        for i in range(2):                       # gap between element i+1 and i+2: shared node q_{i+2}
            xr = XS[i + 1] + SH[i] - 0.55        # arrow ending at the right end of the left element
            xl = XS[i + 1] + SH[i + 1]           # arrow starting at the left end of the right element
            a1, a2 = darrow(xr, ya, 0.55), darrow(xl, ya, 0.55)
            l1 = M("q_%d" % (i + 2), size=40, color=SKY).next_to(a1, DOWN, buff=0.12)
            l2 = M("q_%d" % (i + 2), size=40, color=SKY).next_to(a2, DOWN, buff=0.12)
            gaps.add(VGroup(a1, a2, l1, l2))
        same = T("same end displacement", size=32, color=INK2).move_to(p(-0.6, YB - 2.3))
        fb.nodes.set_opacity(0)                  # shared node dots hide; each element shows its own end dots
        self.add(ends)
        with self.say("Neighbors share a node, so the displacement can't jump: the right end of element one "
                      "moves exactly as much as the left end of element two.") as d:
            self.play(FadeOut(plot), FadeOut(qs), FadeOut(dof), FadeOut(dof_s), FadeOut(dof_g), run_time=.08 * d)
            self.play(pieces[1].animate.shift(SH[1] * RIGHT), pieces[2].animate.shift(SH[2] * RIGHT),
                      load.animate.shift(SH[2] * RIGHT), run_time=.2 * d)
            self.play(FadeIn(gaps), FadeIn(same), run_time=.15 * d)
            self.play(Circumscribe(gaps[0], color=SKY), run_time=.25 * d)
            self.snap("exploded")
            self.wait(.05 * d)
            self.play(FadeOut(gaps), FadeOut(same), pieces[1].animate.shift(-SH[1] * RIGHT),
                      pieces[2].animate.shift(-SH[2] * RIGHT), load.animate.shift(-SH[2] * RIGHT),
                      run_time=.25 * d)
        self.remove(ends)
        fb.nodes.set_opacity(1)

        # ---- beat 5: element 2 lifted out; local u1, u2 = global q2, q3 ----
        LIFT = 2.4
        e2 = VGroup(bar(XS[1], XS[2], y=YB, h=H, color=LILAC), Dot(p(XS[1], YB), radius=0.1, color=INK),
                    Dot(p(XS[2], YB), radius=0.1, color=INK))
        u1 = M("u_1", size=44, color=SKY).move_to(p(XS[1], YB + LIFT + 0.75))
        u2 = M("u_2", size=44, color=SKY).move_to(p(XS[2], YB + LIFT + 0.75))
        e2_t = T("element 2", size=36, color=INK).next_to(p(XS[1], YB + LIFT), LEFT, buff=0.5)
        links = VGroup(*[Arrow(p(x, YB + LIFT - H / 2), p(x, YB + H / 2), buff=0.12, color=SKY, stroke_width=4,
                               max_tip_length_to_length_ratio=0.12) for x in (XS[1], XS[2])])
        qs2 = VGroup(qlab(2), qlab(3))
        eqs = VGroup(E(r"u_1|=|q_2", size=52), E(r"u_2|=|q_3", size=52)).arrange(RIGHT, buff=1.6)
        eqs.move_to(p(-1.5, YB - 2.6))
        self.beat("When we study one element on its own, we'll call its two end displacements u one and u two. "
                  "For element two, its u one is the bar's q two, and its u two is q three.",
                  FadeIn(e2), e2.animate.shift(LIFT * UP), [FadeIn(e2_t), FadeIn(u1), FadeIn(u2)], .1,
                  [GrowArrow(links[0]), GrowArrow(links[1]), FadeIn(qs2)], FadeIn(eqs[0]), FadeIn(eqs[1]),
                  w=(.05, .13, .2, .22, .2, .2))
        self.wait(1)
        self.wipe()
