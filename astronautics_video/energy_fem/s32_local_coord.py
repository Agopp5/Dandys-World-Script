"""S32: a coordinate inside one element (BRIEF.md S32)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: s = (x - x1)/l maps [x1, x2] onto [0, 1]; its inverse is x = x1 + s l, so dx = l ds
for x1, x2 in [(0.0, 500.0), (20.0, 40.0), (3.0, 7.5)]:
    l = x2 - x1
    s_of = lambda x: (x - x1) / l
    assert np.isclose(s_of(x1), 0) and np.isclose(s_of(x2), 1)
    assert np.isclose(s_of((x1 + x2) / 2), 0.5)                 # halfway along, s is one half
    for s in np.linspace(0, 1, 5):
        assert np.isclose(s_of(x1 + s * l), s)                  # x = x1 + s l inverts it
    assert np.isclose(((x1 + 0.6 * l) - (x1 + 0.5 * l)) / 0.1, l)   # dx / ds = l
# U over [0, L] splits into per-element integrals: check with u = x^2 on three equal pieces
_g = lambda a, b: (b ** 3 - a ** 3) / 3 * 4                     # integral of (u')^2 = 4 x^2
assert np.isclose(_g(0, 3), _g(0, 1) + _g(1, 2) + _g(2, 3))

XL, XR, YB, YR = -6.2, -0.9, 1.9, -0.3      # element ends (screen x), element y, ruler y
WID = XR - XL
EQX = 3.6                                    # centre of the right half (equations)


def rx(s):
    """screen x of local coordinate s"""
    return XL + s * WID


class S32_Local_Coord(VScene):
    budget = 153

    def construct(self):
        # ---- beat 1: the bar's energy splits element by element
        xs = [XL + WID * i / 3 for i in range(4)]
        fb = fem_bar(xs, y=YB, h=0.6)
        wl = wall(np.array([XL, YB, 0]), side=LEFT, h=1.6)
        ends = VGroup(M("0", size=36, color=INK2).move_to([XL, YB + 0.7, 0]),
                      M("L", size=36, color=INK2).move_to([XR, YB + 0.7, 0]))
        ulab = VGroup(*[M("U_%d" % (i + 1), size=44, color=MINT).move_to([(xs[i] + xs[i + 1]) / 2, YB - 0.85, 0])
                        for i in range(3)])
        ucm = {"U_1": MINT, "U_2": MINT, "U_3": MINT}
        e1 = E(r"U|=|\frac12\int_0^L EA\Big(\frac{du}{dx}\Big)^2 dx", size=48)
        e2 = E(r"U|=|\int_{\mathrm{el}\,1}\!\!\cdots|+|\int_{\mathrm{el}\,2}\!\!\cdots|+|\int_{\mathrm{el}\,3}\!\!\cdots",
               size=48)
        e3 = E(r"U|=|U_1|+|U_2|+|U_3", size=56, cmap=ucm)
        for e in (e1, e2, e3):
            fit(e, 6.3, 2)
        e1.move_to([EQX, 1.9, 0])
        e2.move_to([EQX, 0.1, 0])
        e3.move_to([EQX, -1.8, 0])
        sep = VGroup(*[DashedLine([xs[i], YB - 0.5, 0], [xs[i], YB + 0.5, 0], color=MUTED) for i in (1, 2)])
        self.beat("Why can we study one element alone? The bar's energy is an integral along the bar, and an "
                  "integral along the bar splits into one integral per element. Work out one element's energy, "
                  "and the bar's is just the sum.",
                  [FadeIn(fb), FadeIn(wl), FadeIn(ends)], Write(e1), .05,
                  [FadeIn(e2), Create(sep)], .05,
                  [Write(e3), LaggedStart(*[FadeIn(u, shift=.2 * DOWN) for u in ulab], lag_ratio=.3)],
                  Indicate(e3[2:]), .1)

        # ---- beat 2: lift out one element
        lone = bar(XL, XR, y=YB, h=0.6)
        n1, n2 = node(np.array([XL, YB, 0])), node(np.array([XR, YB, 0]))
        xl1 = M("x_1", size=44).move_to([XL, YB - 0.8, 0])
        xl2 = M("x_2", size=44).move_to([XR, YB - 0.8, 0])
        ya = YB + 0.85
        dim = VGroup(DoubleArrow([XL, ya, 0], [XR, ya, 0], buff=0, color=INK2, stroke_width=4,
                                 tip_length=.22, max_tip_length_to_length_ratio=.1),
                     Line([XL, ya - .2, 0], [XL, ya + .2, 0], color=INK2),
                     Line([XR, ya - .2, 0], [XR, ya + .2, 0], color=INK2))
        dlab = backed(M(r"l = x_2 - x_1", size=44)).move_to([(XL + XR) / 2, ya + 0.5, 0])
        others = [m for i, m in enumerate(fb.elems) if i != 1] + list(fb.nodes) + list(fb.tags)
        self.beat("So lift out one element. It starts at x one and ends at x two. Its length is l, x two minus "
                  "x one.",
                  [FadeOut(VGroup(e1, e2, e3, ulab, ends, wl, sep, *others))],
                  ReplacementTransform(fb.elems[1], lone), .05,
                  [FadeIn(n1), FadeIn(n2), FadeIn(xl1, shift=.2 * UP), FadeIn(xl2, shift=.2 * UP)], .05,
                  [GrowFromCenter(dim), FadeIn(dlab)], .1)

        # ---- beat 3: the element's own ruler s
        rl = Line([XL, YR, 0], [XR, YR, 0], color=LIME, stroke_width=7)
        svals = [0, .25, .5, .75, 1]
        stxt = ["0", "0.25", "0.5", "0.75", "1"]
        ticks = VGroup(*[Line([rx(v), YR - .17, 0], [rx(v), YR + .17, 0], color=LIME, stroke_width=5)
                         for v in svals])
        tlab = VGroup(*[M(t, size=36, color=INK).move_to([rx(v), YR - 0.6, 0]) for v, t in zip(svals, stxt)])
        sname = M("s", size=52, color=LIME).next_to(rl, LEFT, buff=.3)
        self.beat("Measuring from the global x is clumsy, so give the element its own ruler, called s. It runs "
                  "from zero at the left end to one at the right end, whatever the element's length.",
                  [Create(rl), FadeIn(sname)], LaggedStart(*[FadeIn(VGroup(t, b)) for t, b in zip(ticks, tlab)],
                                                           lag_ratio=.25),
                  [Indicate(tlab[0], color=LIME), Indicate(tlab[-1], color=LIME)], .1)

        # ---- beat 4: s = (x - x1)/l, and the midpoint has s = 1/2
        seq = E(r"s|=|\frac{x - x_1}{l}", size=56).move_to([EQX, 1.7, 0])
        xm = rx(.5)
        mline = DashedLine([xm, YB - 0.3, 0], [xm, YR, 0], color=MUTED)
        mdot = Dot([xm, YB, 0], radius=.1, color=INK)
        rdot = Dot([xm, YR, 0], radius=.12, color=LIME)
        half = M(r"s = \frac12", size=44, color=LIME).move_to([xm, YR - 1.55, 0])
        self.beat("The conversion is s equals x minus x one, over l. Halfway along the element, s is one half.",
                  Write(seq), .05, [FadeIn(mdot), Create(mline), FadeIn(rdot)],
                  [Indicate(tlab[2], color=LIME), FadeIn(half, shift=.2 * DOWN)], .15)

        # ---- beat 5: x = x1 + s l, so dx = l ds
        xeq = E(r"x|=|x_1|+|s|\,l", size=56).move_to([EQX, 0.0, 0])
        deq = E(r"dx|=|l\,|ds", size=60, cmap={"ds": LIME}).move_to([EQX, -1.9, 0])
        box = SurroundingRectangle(deq, color=INK2, buff=.25, corner_radius=.1)
        sv = ValueTracker(.5)
        ldot = always_redraw(lambda: Dot([rx(sv.get_value()), YB, 0], radius=.1, color=INK))
        lline = always_redraw(lambda: DashedLine([rx(sv.get_value()), YB - .3, 0], [rx(sv.get_value()), YR, 0],
                                                 color=MUTED))
        lrd = always_redraw(lambda: Dot([rx(sv.get_value()), YR, 0], radius=.12, color=LIME))
        s0, s1 = .5, .64
        bds = Brace(Line([rx(s0), YR - .9, 0], [rx(s1), YR - .9, 0]), DOWN, color=LIME, buff=.05)
        lds = M("ds", size=44, color=LIME).next_to(bds, DOWN, buff=.12)
        bdx = Brace(Line([rx(s0), YB - .32, 0], [rx(s1), YB - .32, 0]), DOWN, color=INK, buff=.05)
        ldx = M("dx", size=44).next_to(bdx, DOWN, buff=.1)
        with self.say("Flip it around: x equals x one plus s times l. So as s moves a tiny step d s, x moves l "
                      "times that. d x equals l d s. We'll need that inside integrals.") as d:
            self.play(Write(xeq), FadeOut(half), run_time=.2 * d)
            self.remove(mdot, mline, rdot)
            self.add(lline, ldot, lrd)
            self.play(Circumscribe(xeq[4]), run_time=.08 * d)
            self.play(sv.animate.set_value(s1), run_time=.14 * d)
            self.play(GrowFromCenter(bds), FadeIn(lds), run_time=.08 * d)
            self.play(GrowFromCenter(bdx), FadeIn(ldx), run_time=.08 * d)
            self.play(Write(deq), run_time=.16 * d)
            self.play(Create(box), FadeIn(glow(deq, LIME)), run_time=.1 * d)
            self.wait(.16 * d)
        self.wipe()
