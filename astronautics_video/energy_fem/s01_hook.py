"""S01: two ways to find a stretch (BRIEF.md S01)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the bowl drawn on the right is the series' one-spring example, Pi(q) = 10 q^2 - 100 q (K = 20, F = 100)
K_N, F_N = 20.0, 100.0
Q_STAR = F_N / K_N
assert np.isclose(Q_STAR, 5.0)                       # K q = F  ->  q = 5 mm


def Pi(q):
    return 0.5 * K_N * q ** 2 - F_N * q


assert np.allclose([Pi(q) for q in (0, 3, 5, 7, 10)], [0, -210, -250, -210, 0])
assert np.isclose(K_N * Q_STAR - F_N, 0.0)           # d Pi / d q = K q - F = 0 at the bottom: the same answer


def settle(t):
    """0 -> 1 with a damped overshoot: a spring that stretches and settles."""
    return 1 - (1 - t) * np.exp(-3 * t) * np.cos(3 * np.pi * t)


def roll(t):
    """0 -> 1 starting from rest, rocking a little before it stops: a ball rolling into a bowl."""
    s = t * t * (3 - 2 * t)
    return 1 - (1 - s) * np.exp(-2.5 * s) * np.cos(2.5 * np.pi * s)


# left half: the spring problem
WALL_X, SY = -6.3, 2.2            # wall face, spring line height
X0, STRETCH = -3.1, 0.8           # node at rest, drawn stretch (the q arrow has the same length)
# right half: the bowl, q from 0 to 10 across, Pi from -250 (bottom) to 0 (rims)
BX0, BXS, BY0, BH = 1.2, 0.48, 0.35, 2.6


def bx(q):
    return BX0 + BXS * q


def by(p):
    return BY0 + (p + 250.0) / 250.0 * BH


def bowl_pt(q, r=0.0):
    """Point on the bowl at q, lifted r along the normal (the ball's centre sits r above the curve)."""
    slope = (BH / 250.0) * (K_N * q - F_N) / BXS
    n = np.array([-slope, 1.0, 0.0]) / np.sqrt(1 + slope ** 2)
    return np.array([bx(q), by(Pi(q)), 0.0]) + r * n


class S01_Hook(VScene):
    budget = 166

    def construct(self):
        # ---------- beat 1: a spring, a wall, a force ----------
        xt = ValueTracker(X0)
        wl = wall(np.array([WALL_X, SY, 0]), side=LEFT, h=1.6)
        spr0 = spring(np.array([WALL_X, SY, 0]), np.array([X0, SY, 0]))
        spr = always_redraw(lambda: spring(np.array([WALL_X, SY, 0]), np.array([xt.get_value(), SY, 0])))
        nd = node(np.array([X0, SY, 0]), r=0.11)
        fa = force(np.array([X0 + 0.11, SY, 0]), d=RIGHT, length=1.3)
        fl = E("F", size=48).next_to(fa, RIGHT, buff=0.15)
        tip = VGroup(nd, fa, fl)
        tip.add_updater(lambda m: m.shift(RIGHT * (xt.get_value() - nd.get_center()[0])))
        klab = E("K", size=44)
        klab.add_updater(lambda m: m.move_to([(WALL_X + xt.get_value()) / 2, SY + 0.62, 0]))
        rest = DashedLine([X0, SY - 0.35, 0], [X0, SY - 0.95, 0], color=MUTED, dash_length=0.08)
        qd = disp(np.array([X0, SY, 0]), label="q", length=STRETCH, below=0.62)
        qd[2].scale(1.5).next_to(qd[1], DOWN, buff=0.1)

        with self.say("Here's a spring fixed to a wall, and a force pulling on its free end. How far does it "
                      "stretch? You already know one way to answer that.") as d:
            self.play(Create(wl), Create(spr0), FadeIn(nd), FadeIn(klab), run_time=0.22 * d)
            self.remove(spr0)
            self.add(spr)
            self.play(GrowFromPoint(VGroup(fa, fl), nd.get_center()), run_time=0.15 * d)
            self.add(tip)
            self.wait(0.05 * d)
            self.play(xt.animate(rate_func=settle).set_value(X0 + STRETCH), run_time=0.28 * d)
            self.play(Create(rest), FadeIn(qd, shift=RIGHT * 0.2), run_time=0.15 * d)
            self.wait(0.1 * d)

        # ---------- beat 2: free-body diagram of the node, then K q = F ----------
        FB = np.array([-3.6, -0.1, 0])
        n2 = node(FB, r=0.11)
        kq_arrow = force(FB + LEFT * 0.11, d=LEFT, length=1.4, color=LILAC)
        kq_lab = E("K|q", size=44).next_to(kq_arrow, LEFT, buff=0.18)
        f_arrow = force(FB + RIGHT * 0.11, d=RIGHT, length=1.4)
        f_lab = E("F", size=44).next_to(f_arrow, RIGHT, buff=0.18)
        eq = E("K|q|=|F", size=60).move_to([-3.6, -2.0, 0])
        self.beat("Balance the forces. The spring pulls back with stiffness times stretch, K times q. The load "
                  "pulls forward with F. At rest they're equal, so K q equals F.",
                  [Circumscribe(nd, shape=Circle, color=INK2), TransformFromCopy(nd, n2)],
                  [GrowFromPoint(kq_arrow, FB), FadeIn(kq_lab, shift=LEFT * 0.2), Indicate(spr, color=LILAC)],
                  [GrowFromPoint(f_arrow, FB), FadeIn(f_lab, shift=RIGHT * 0.2)],
                  .08, Write(eq), .1, w=(.14, .3, .18, .2))

        # ---------- beat 3: Newton's way vs a bowl of energy ----------
        newton = T("Newton's way", size=32, color=INK2).next_to(eq, DOWN, buff=0.35)
        divider = Line([0, 3.5, 0], [0, -3.5, 0], color=HAIR, stroke_width=2)
        bowl = ParametricFunction(lambda q: np.array([bx(q), by(Pi(q)), 0.0]), t_range=[0, 10],
                                  color=GOLD, stroke_width=6)
        energy = T("energy", size=36, color=GOLD).move_to([bx(5), 3.45, 0])
        qt = ValueTracker(0.0)
        R_BALL = 0.15
        ball = Dot(radius=R_BALL, color=SKY).move_to(bowl_pt(0, R_BALL))
        ball.add_updater(lambda m: m.move_to(bowl_pt(qt.get_value(), R_BALL)))
        self.beat("That's Newton's way. In this series you'll learn a second way, and it sounds completely "
                  "different. Instead of balancing forces, we'll write down a single number, an energy, and look "
                  "for the bottom of a bowl.",
                  [FadeIn(newton, shift=UP * 0.15), Circumscribe(eq, color=INK2)],
                  Create(divider), .14,
                  [Create(bowl), FadeIn(energy, shift=DOWN * 0.15), FadeIn(ball)],
                  qt.animate(rate_func=roll).set_value(Q_STAR), .03,
                  w=(.12, .13, .25, .33))

        # ---------- beat 4: same answer; the energy way grows into finite elements ----------
        drop = DashedLine(bowl_pt(Q_STAR), [bx(Q_STAR), -0.3, 0], color=SKY, dash_length=0.1)
        qlab = E("q", size=44).next_to(drop, DOWN, buff=0.12)
        fb = fem_bar(np.linspace(1.0, 6.2, 7), y=-1.6, elem_labels=False)
        fe = T("finite elements", size=36).next_to(fb, DOWN, buff=0.4)
        self.beat("Both ways give the same answer. But the energy way grows into something much bigger: the finite "
                  "element method, the tool behind nearly every structural simulation you'll ever run.",
                  [Create(drop), FadeIn(qlab, shift=DOWN * 0.15)],
                  [Indicate(eq[1], scale_factor=1.4), Indicate(qlab, scale_factor=1.4)],
                  .05,
                  LaggedStart(*[FadeIn(e, shift=DOWN * 0.15) for e in fb.elems], lag_ratio=0.25),
                  LaggedStart(*[GrowFromCenter(n) for n in fb.nodes], lag_ratio=0.15),
                  FadeIn(fe, shift=UP * 0.15), .12,
                  w=(.14, .14, .25, .12, .18))

        # ---------- beat 5: the road map and the practice guide ----------
        for m in (spr, tip, klab, ball):
            m.clear_updaters()
        old = VGroup(wl, spr, tip, klab, rest, qd, n2, kq_arrow, kq_lab, f_arrow, f_lab, eq, newton, divider,
                     bowl, energy, ball, drop, qlab, fb, fe)

        def stop(pic, *lines):
            frame = Rectangle(width=2.9, height=2.2, stroke_opacity=0, fill_opacity=0)
            words = VGroup(*[T(s, size=34) for s in lines]).arrange(DOWN, buff=0.15)
            body = VGroup(pic, words).arrange(DOWN, buff=0.4).move_to(frame)
            return panel(VGroup(frame, body))

        pic1 = VGroup(node(LEFT * 1.0), spring(LEFT * 1.0, RIGHT * 1.0, coils=4, amp=0.15), node(RIGHT * 1.0))
        pic2 = bar(-1.1, 1.1, y=0.0, h=0.36)
        pic3 = fem_bar(np.linspace(-1.1, 1.1, 5), y=0.0, h=0.36, elem_labels=False)
        p1 = stop(pic1, "springs", "HW 1")
        p2 = stop(pic2, "bars")
        p3 = stop(pic3, "finite elements", "HW 2")
        row = VGroup(p1, p2, p3).arrange(RIGHT, buff=0.75)
        fit(row, 13.0, 3.4)
        row.move_to(UP * 0.9)
        a1 = Arrow(p1.get_right(), p2.get_left(), buff=0.12, color=MUTED, stroke_width=4)
        a2 = Arrow(p2.get_right(), p3.get_left(), buff=0.12, color=MUTED, stroke_width=4)

        page = Polygon([-0.55, -0.75, 0], [0.55, -0.75, 0], [0.55, 0.42, 0], [0.22, 0.75, 0], [-0.55, 0.75, 0],
                       color=INK2, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
        fold = Polygon([0.22, 0.75, 0], [0.22, 0.42, 0], [0.55, 0.42, 0], color=INK2, stroke_width=3,
                       fill_color=HAIR, fill_opacity=1)
        rules = VGroup(*[Line([-0.35, y, 0], [0.35, y, 0], color=HAIR, stroke_width=3) for y in (-0.45, -0.6)])
        pdf_word = T("PDF", size=28, weight=BOLD, color=INK2).move_to([0, -0.05, 0])
        icon = VGroup(page, fold, rules, pdf_word)
        guide = T("practice guide", size=36)
        pdf = VGroup(icon, guide).arrange(RIGHT, buff=0.35).move_to(DOWN * 2.35)

        self.beat("Here's the plan: springs first, then your first homework problem, then bars and finite elements, "
                  "and your second homework problem. Along the way, the video will pause for you to try things in "
                  "your practice guide, a short PDF that goes with these videos.",
                  FadeOut(old),
                  FadeIn(p1, shift=UP * 0.2),
                  [GrowArrow(a1), FadeIn(p2, shift=UP * 0.2)],
                  [GrowArrow(a2), FadeIn(p3, shift=UP * 0.2)],
                  FadeIn(glow(p1, LILAC)), .04,
                  FadeIn(pdf, shift=UP * 0.2), .2,
                  w=(.06, .14, .1, .16, .1, .2))
        self.wipe()
