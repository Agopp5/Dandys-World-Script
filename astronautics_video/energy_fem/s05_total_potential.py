"""S05: total potential energy, a bowl (BRIEF.md S05)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: one spring, K = 20 N/mm, F = 100 N
K_, F_ = 20.0, 100.0
U_ = lambda q: 0.5 * K_ * q ** 2
W_ = lambda q: F_ * q
Pi_ = lambda q: U_(q) - W_(q)
assert np.isclose(0.5 * K_, 10) and np.isclose(F_, 100)
for qq, pv in [(0, 0), (3, -210), (5, -250), (7, -210), (10, 0)]:
    assert np.isclose(Pi_(qq), pv)
assert np.isclose(U_(5), 250) and np.isclose(W_(5), 500) and np.isclose(U_(5), W_(5) / 2)

CMAP = {"q^2": SKY}


def tank(center, color, frac, label):
    """Outline tank with an always_redraw fill whose height is frac() of the tank."""
    w, h = 1.5, 3.0
    shell = Rectangle(width=w, height=h, color=INK2, stroke_width=3).move_to(center)
    fill = always_redraw(lambda: Rectangle(width=w - 0.08, height=max(h * frac(), 1e-3) - 0.04 * (frac() > 0.02),
                                           stroke_width=0, fill_color=color, fill_opacity=0.85)
                         .move_to(shell.get_bottom() + 0.04 * UP, aligned_edge=DOWN))
    lab = M(label, size=48, color=color).next_to(shell, DOWN, buff=0.25)
    return VGroup(fill, shell, lab)


class S05_Total_Potential(VScene):
    budget = 165

    def construct(self):
        # ---- beat 1: hanging spring, U tank fills, W tank drains
        t = ValueTracker(0)
        sx, top = -5.0, 2.9
        ceil = VGroup(Line([sx - 0.9, top, 0], [sx + 0.9, top, 0], color=INK, stroke_width=4),
                      *[Line([x, top, 0], [x + 0.22, top + 0.25, 0], color=INK2, stroke_width=2)
                        for x in np.linspace(sx - 0.85, sx + 0.6, 7)])
        bot = lambda: np.array([sx, 0.9 - 1.6 * t.get_value(), 0])
        spr = always_redraw(lambda: spring(np.array([sx, top, 0]), bot()))
        mass = always_redraw(lambda: Square(0.85, color=INK2, fill_color=SURFACE, fill_opacity=1)
                             .move_to(bot() + 0.425 * DOWN))
        load = always_redraw(lambda: force(bot() + 0.85 * DOWN, d=DOWN, length=0.9, label="F"))
        fig = VGroup(ceil, spr, mass, load)
        tu = tank(np.array([-0.6, 0.7, 0]), MINT, lambda: 0.5 * t.get_value(), "U")
        tw = tank(np.array([3.8, 0.7, 0]), EMBER, lambda: 1 - t.get_value(), "W")
        nu = T("stored by the spring", 32, INK2).next_to(tu, DOWN, buff=0.15)
        nw = T("given up by the load", 32, INK2).next_to(tw, DOWN, buff=0.15)
        tot = E(r"U|-|W", size=60).move_to(np.array([1.6, 3.0, 0]))
        self.beat("Now combine them. As the spring stretches, it stores energy, U. And the weight gives energy up, "
                  "W. So the total energy of the whole system, spring plus load, is U minus W.",
                  [FadeIn(fig), FadeIn(tu), FadeIn(tw)], [FadeIn(nu), FadeIn(nw)],
                  t.animate(rate_func=linear).set_value(1), Write(tot), w=(.12, .1, .53, .25))
        for m in (spr, mass, load, tu[0], tw[0]):
            m.clear_updaters()

        # ---- beat 2: the definition, spotlit
        eq = E(r"\Pi|=|U|-|W", size=60).move_to(UP * 0.3)
        words = T("total potential is strain energy minus work potential", 32, INK2).next_to(eq, DOWN, buff=0.6)
        self.beat("This is the definition everything else rests on, so let it land. The total potential energy, "
                  "capital Pi, is strain energy minus work potential. Pi equals U minus W.",
                  [FadeOut(VGroup(fig, tu, tw, nu, nw))], ReplacementTransform(tot, eq[2:]), FadeIn(eq[:2]),
                  FadeIn(words), self.spotlight(eq), .3,
                  w=(.15, .15, .1, .15, .15), style="slower and deliberate, stressing the key words")

        # ---- beat 3: plug in the spring
        gen = E(r"\Pi|=|\tfrac12|K|q^2|-|F|q", size=60, cmap=CMAP).move_to(UP * 1.5)
        num = E(r"\Pi|=|10|q^2|-|100|q", size=60, cmap=CMAP).next_to(gen, DOWN, buff=0.7)
        vals = E(r"K|=|20|,\quad|F|=|100", size=40).next_to(num, DOWN, buff=0.7)
        self.beat("For our spring, that's one half K q squared, minus F q. With twenty and one hundred, Pi equals "
                  "ten q squared minus one hundred q.",
                  self.unspot(), [FadeOut(words), ReplacementTransform(eq, gen)], FadeIn(vals),
                  [Indicate(vals[2], color=LILAC), Indicate(vals[6], color=ROSE)], Write(num),
                  [Indicate(num[2], color=GOLD, scale_factor=1.3), Indicate(num[4], color=GOLD, scale_factor=1.3)],
                  w=(.08, .2, .12, .15, .2, .25))

        # ---- beat 4: the three curves
        ax = axes([0, 10, 1], [-300, 1000, 100], width=8.4, height=5.8, xlabel="q", ylabel="energy")
        ax.to_edge(LEFT, buff=0.9).shift(0.1 * DOWN)
        ticks = VGroup(*[M(str(v), size=26, color=MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.15)
                         for v in (500,)],
                       *[M(str(v), size=26, color=MUTED).next_to(ax.c2p(v, 0), UP + LEFT, buff=0.08)
                         for v in (5, 10)])
        cu = ax.plot(U_, x_range=[0, 10], color=MINT, stroke_width=5)
        cw = ax.plot(W_, x_range=[0, 10], color=EMBER, stroke_width=5)
        cp = ax.plot(Pi_, x_range=[0, 10], color=GOLD, stroke_width=6)
        lu = M(r"U", size=48, color=MINT).next_to(ax.c2p(8, U_(8)), DOWN + RIGHT, buff=0.15)
        lw = M(r"W", size=48, color=EMBER).next_to(ax.c2p(6, W_(6)), UP + LEFT, buff=0.15)
        lp = M(r"\Pi", size=48, color=GOLD).next_to(ax.c2p(5, Pi_(5)), DOWN, buff=0.2)
        unit = T("q in mm, energy in N mm", 30, MUTED)
        side = VGroup(num.copy(), E(r"\Pi|=|U|-|W", size=44)).arrange(DOWN, buff=0.5)
        side.to_edge(RIGHT, buff=0.6).shift(UP * 1.2)
        unit.to_corner(DR, buff=0.6)
        gap = ax.get_area(cu, x_range=[0, 10], bounded_graph=cw, color=GOLD, opacity=0.3)
        self.beat("Let's draw all three. U is the upward parabola. W is a straight line, rising. Subtract the line "
                  "from the parabola, and you get Pi: a bowl that dips below zero.",
                  [FadeOut(VGroup(gen, vals)), ReplacementTransform(num, side[0]), FadeIn(side[1]),
                   Create(ax), FadeIn(ticks), FadeIn(unit)],
                  [Create(cu), FadeIn(lu)], [Create(cw), FadeIn(lw)], FadeIn(gap),
                  [Create(cp), FadeIn(lp)], FadeOut(gap),
                  w=(.14, .17, .17, .14, .26, .12))

        # ---- beat 5: values on the bowl
        dots, cards = VGroup(), VGroup()
        for qq, side_dir in [(0, UP + RIGHT), (3, DOWN), (7, DOWN), (10, UP + LEFT)]:
            p = ax.c2p(qq, Pi_(qq))
            d = Dot(p, color=GOLD, radius=0.09)
            txt = M(r"%d" % round(Pi_(qq)), size=34, color=GOLD)
            c = panel(txt, color=GOLD).scale(0.95).next_to(d, side_dir, buff=0.2)
            dots.add(d)
            cards.add(c)
        cards[0].shift(0.2 * RIGHT)
        link = DashedLine(ax.c2p(3, -210), ax.c2p(7, -210), color=GOLD, stroke_width=3)
        sym = T("same height", 28, MUTED).next_to(link, UP, buff=0.12)
        self.beat("Look at a few values. At q equals zero, Pi is zero. At three, minus two hundred ten. At seven, "
                  "also minus two hundred ten. At ten, back to zero.",
                  [FadeOut(VGroup(cu, cw, lu, lw)), cp.animate.set_stroke(width=6)],
                  [FadeIn(dots[0], scale=2), FadeIn(cards[0])], [FadeIn(dots[1], scale=2), FadeIn(cards[1])],
                  [FadeIn(dots[2], scale=2), FadeIn(cards[2]), Create(link), FadeIn(sym)],
                  [FadeIn(dots[3], scale=2), FadeIn(cards[3])],
                  w=(.1, .2, .25, .25, .2))

        # ---- beat 6: predict
        self.predict("Where is the bottom of the bowl?",
                     "So where is the bottom of this bowl? Make a guess before we work it out.")
        self.wipe()
