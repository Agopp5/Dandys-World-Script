"""S07: the stationary principle (BRIEF.md S07)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the one-spring example (K = 20 N/mm, F = 100 N), Pi(q) = 10 q^2 - 100 q in N mm
K_S, F_S = 20.0, 100.0


def Pi(q):
    return 0.5 * K_S * q ** 2 - F_S * q


assert np.isclose(Pi(2), -160) and np.isclose(Pi(8), -160) and np.isclose(Pi(5), -250)
assert np.isclose(Pi(0), 0) and np.isclose(Pi(10), 0)
assert np.isclose(F_S / K_S, 5)                       # minimum at q = 5 mm: K q = F
assert np.isclose(K_S * 5 - F_S, 0)                   # dPi/dq = K q - F vanishes there
TRIALS = [(2, r"\Pi|=-160", LEFT), (8, r"\Pi|=-160", RIGHT), (5, r"\Pi|=-250", DOWN)]


def lock_icon(color=GOLD):
    body = RoundedRectangle(width=.44, height=.36, corner_radius=.06, fill_color=color, fill_opacity=1,
                            stroke_width=0)
    shackle = Arc(radius=.15, start_angle=0, angle=PI, color=color, stroke_width=7)
    shackle.next_to(body, UP, buff=-.02)
    hole = Dot(body.get_center(), radius=.05, color=BG)
    return VGroup(shackle, body, hole)


class S07_Principle(VScene):
    budget = 168

    def construct(self):
        # ---- left: the bowl Pi(q) -------------------------------------------------------------
        ax = axes([0, 10, 2], [-300, 50, 100], width=6, height=4.6, xlabel="q", ylabel=r"\Pi")
        ax.move_to([-3.5, -0.2, 0])
        bowl = ax.plot(Pi, x_range=[0, 10], color=GOLD, stroke_width=5)
        dots, tags, drops, ticks = {}, {}, {}, {}
        for q, tex, side in TRIALS:
            d = Dot(ax.c2p(q, 45), color=SKY, radius=0.11).set_z_index(5)
            dots[q] = d
            drops[q] = DashedLine(ax.c2p(q, 0), ax.c2p(q, Pi(q)), color=MUTED, stroke_width=2)
            tags[q] = E(tex, size=34).next_to(ax.c2p(q, Pi(q)), side, buff=0.4 if q == 5 else 0.2)
            ticks[q] = M(str(q), size=30, color=SKY).next_to(ax.c2p(q, 0), UP, buff=0.15)

        with self.say("Let's say what just happened in general. Imagine trying every stretch the spring could "
                      "possibly have: two millimeters, eight, five. Each one gives a value of Pi.") as d:
            self.play(Create(ax), run_time=.12 * d)
            self.play(Create(bowl), run_time=.13 * d)
            for q, _, _ in TRIALS:
                self.add(dots[q])
                self.play(dots[q].animate.move_to(ax.c2p(q, Pi(q))), Create(drops[q]), run_time=.12 * d)
                self.play(FadeIn(tags[q], shift=.1 * UP), FadeIn(ticks[q]), run_time=.08 * d)

        # ---- right: the principle in words --------------------------------------------------
        title = T("The stationary principle", size=42, color=GOLD, weight=BOLD).move_to([3.85, 3.2, 0])
        stmt = VGroup(
            T("Among all geometrically possible", size=32),
            T("displacements, the real one makes", size=32),
            VGroup(M(r"\Pi", size=40, color=GOLD), T("stationary, and for a stable", size=32)).arrange(RIGHT, buff=.15),
            T("structure, a minimum.", size=32),
            T("(minimum total potential energy)", size=30, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.2)
        fit(stmt, 6.0, 3.0)
        stmt.next_to(title, DOWN, buff=.45)
        halo = glow(dots[5], GOLD)
        self.beat("Here's the principle: among all the geometrically possible displacements, the real one is the "
                  "one that makes Pi stationary, and for a stable structure, a minimum. It's called the stationary "
                  "principle, or the principle of minimum total potential energy.",
                  [FadeIn(halo), Indicate(tags[5], color=GOLD)], Write(title),
                  LaggedStart(*[FadeIn(l, shift=.1 * UP) for l in stmt], lag_ratio=.5), w=(.15, .2, .65))

        # ---- the slope condition is force balance --------------------------------------------
        eq_a = M(r"\frac{d\Pi}{dq}=0", size=52)
        eq_a[0][1].set_fill(GOLD, 1).set_stroke(GOLD)
        eq_a[0][4].set_fill(SKY, 1).set_stroke(SKY)
        eq_b = E(r"K|q|=|F", size=52)
        same = M("=", size=72, color=ACCENT)
        pair = VGroup(eq_a, same, eq_b).arrange(RIGHT, buff=.6)
        pair.move_to([3.85, -1.9, 0])
        lab_a = T("bottom of the bowl", size=30, color=MUTED).next_to(eq_a, DOWN, buff=.3)
        lab_b = T("force balance", size=30, color=MUTED).next_to(eq_b, DOWN, buff=.3)
        lab_b.align_to(lab_a, UP)
        self.beat("Why should we believe it? Because, as you just saw, its slope condition is exactly force "
                  "balance. Minimizing Pi and balancing forces are the same thing.",
                  [Write(eq_a), FadeIn(lab_a)], [Write(eq_b), FadeIn(lab_b)], .05,
                  [FadeIn(same, scale=1.6), Circumscribe(pair, color=ACCENT)], w=(.3, .3, .35))

        # ---- geometrically possible: the wall end never moves ---------------------------------
        xw, xn, y1, y2 = 1.4, 4.4, 1.3, -1.5
        w1 = wall([xw, y1, 0], h=1.3)
        s1 = spring([xw, y1, 0], [xn, y1, 0], label="K")
        n1 = node([xn, y1, 0])
        f1 = force([xn, y1, 0], RIGHT, 1.0, label="F")
        d1 = disp([xn, y1, 0], label="q")
        good = VGroup(w1, s1, n1, f1, d1)
        lock = lock_icon().move_to([xw + .35, y1 + .75, 0])
        zero = M("0", size=40, color=SKY).move_to([xw + .3, y1 - .6, 0])

        shift = 0.8
        w2 = wall([xw, y2, 0], h=1.1)
        s2 = spring([xw + shift, y2, 0], [xn + shift, y2, 0])
        n2 = node([xn + shift, y2, 0])
        a2 = Arrow([xw, y2 - .5, 0], [xw + shift + .15, y2 - .5, 0], buff=0, color=SKY, stroke_width=5,
                   max_tip_length_to_length_ratio=.35)
        bad = VGroup(w2, s2, n2, a2)
        x2 = Cross(VGroup(s2, a2), stroke_color=BAD, stroke_width=8)
        nope = T("not allowed", size=32, color=BAD).next_to(VGroup(s2, n2, a2), DOWN, buff=.35)

        with self.say("Geometrically possible means the trial must respect the supports. The end bolted to the "
                      "wall never moves, so no trial is allowed to move it.") as d:
            self.play(FadeOut(stmt), FadeOut(pair), FadeOut(lab_a), FadeOut(lab_b), run_time=.1 * d)
            self.play(FadeIn(good), run_time=.15 * d)
            self.play(Flash([xw, y1, 0], color=GOLD, flash_radius=.45), FadeIn(lock, scale=1.4),
                      FadeIn(zero), run_time=.2 * d)
            self.wait(.05 * d)
            self.play(FadeIn(bad), run_time=.2 * d)
            self.play(Create(x2), FadeIn(nope), run_time=.2 * d)

        # ---- stationary = flat ----------------------------------------------------------------
        tangent = Line(ax.c2p(3.3, -250), ax.c2p(6.7, -250), color=ACCENT, stroke_width=6).set_z_index(4)
        flat = T("flat: slope zero", size=30, color=ACCENT).next_to(tangent, RIGHT, buff=.2)
        with self.say("Stationary means flat: the slope is zero. For a stable structure, the flat spot is the "
                      "bottom of a bowl, a minimum.") as d:
            self.play(Create(tangent), FadeIn(flat), run_time=.25 * d)
            self.play(self.spotlight(tangent, flat, dots[5], tags[5]), run_time=.2 * d)
            self.play(Indicate(tangent, color=GOLD, scale_factor=1.15), Flash(dots[5], color=GOLD),
                      run_time=.3 * d)

        self.wipe()
        kb_pi = E(r"\Pi|=|U|-|W|,\ \ \frac{d\Pi}{dq} = 0 \Rightarrow|K|q|=|F", size=48)
        kb_pi[5][2].set_fill(GOLD, 1).set_stroke(GOLD)
        kb_pi[5][5].set_fill(SKY, 1).set_stroke(SKY)
        kb = key_box(E(r"U|=|\tfrac12|K|q|^2", size=48), E(r"W|=|F|q", size=48), kb_pi, label="KEY IDEA")
        self.beat("So, stepping back: one spring, two routes. Balance forces, or minimize Pi equals U minus W. Next, "
                  "we'll see why the energy route wins when there are many springs.",
                  FadeIn(kb, shift=.2 * UP), .6, w=(.4,))
        self.wipe()
