"""S18: writing Pi for HW P1 (BRIEF.md S18)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the U and W written here make Pi stationary at the HW P1 sanity solution
# (all K = 100 N/mm, all P = 30 N -> q1 = 0.5, q2 = 0.7, q3 = 1.0 mm)
def _pi(q, K1=100., K2=100., K3=100., P1=30., P2=30., P3=30., P4=30.):
    q1, q2, q3 = q
    U = .5 * K1 * q2 ** 2 + .5 * K2 * q1 ** 2 + .5 * K2 * (q2 - q1) ** 2 + .5 * K3 * (q3 - q2) ** 2
    W = P1 * q1 + (P2 + P3) * q2 + P4 * q3
    return U - W

_q = np.array([.5, .7, 1.0])
for _i in range(3):
    _h = np.zeros(3); _h[_i] = 1e-6
    assert abs((_pi(_q + _h) - _pi(_q - _h)) / 2e-6) < 1e-5
assert np.isclose((30 + 2 * 90) / (2 * 100 + 100), .7)


def build(terms, size=44, cmap=None):
    """E() from a list of terms (each a list of TeX pieces); returns (eq, [VGroup per term])."""
    flat = [p for t in terms for p in t]
    eq = E("|".join(flat), size=size, cmap=cmap)
    groups, i = [], 0
    for t in terms:
        groups.append(VGroup(*eq[i:i + len(t)]))
        i += len(t)
    return eq, groups


class S18_P1_Pi(VScene):
    budget = 113

    def construct(self):
        # ---- stretch table (from S17), built at its final top-left spot ----
        head = VGroup(T("spring", size=30, color=MUTED), T("stretch", size=30, color=MUTED))
        rows_src = [("K_1", "q_2"), ("K_2", "q_1"), ("K_2", r"q_2|-|q_1"), ("K_3", r"q_3|-|q_2")]
        rows = [(E(a, size=40), E(b, size=40)) for a, b in rows_src]
        head[0].move_to(ORIGIN, aligned_edge=LEFT)
        head[1].move_to(1.5 * RIGHT, aligned_edge=LEFT)
        for i, (a, b) in enumerate(rows):
            y = -.72 * (i + 1) - .1
            a.move_to(np.array([.15, y, 0]), aligned_edge=LEFT)
            b.move_to(np.array([1.5, y, 0]), aligned_edge=LEFT)
        rule = Line(head.get_corner(DL) + .12 * DOWN, head.get_corner(DR) + .12 * DOWN + .6 * RIGHT,
                    color=HAIR, stroke_width=2)
        tab = VGroup(head, rule, *[VGroup(a, b) for a, b in rows])
        card = panel(tab)
        card.to_corner(UL, buff=.35)
        card.generate_target()
        card.scale(1.35).move_to(.2 * UP)

        # ---- U, two lines on the right ----
        UT = [["U"], ["="], [r"\tfrac12", "K_1", "q_2^2"], ["+"], [r"\tfrac12", "K_2", "q_1^2"], ["+"],
              [r"\tfrac12", "K_2", "(", "q_2", "-", "q_1", ")^2"], ["+"],
              [r"\tfrac12", "K_3", "(", "q_3", "-", "q_2", ")^2"]]
        u, ug = build(UT, size=46, cmap={"q_2^2": SKY, "q_1^2": SKY})
        line1 = VGroup(*ug[0:5])
        line2 = VGroup(*ug[5:9])
        line2.next_to(line1, DOWN, buff=.35, aligned_edge=LEFT)
        line2.shift((ug[2].get_left()[0] - line2.get_left()[0] - .45) * RIGHT)
        fit(u, 8.0, 2.2)
        u.move_to(np.array([-1.3, 3.5, 0]), aligned_edge=UL)

        # ---- W ----
        WT = [["W"], ["="], ["P_1", "q_1"], ["+"], ["(", "P_2", "+", "P_3", ")", "q_2"], ["+"], ["P_4", "q_3"]]
        w, wg = build(WT, size=46)
        # (W is placed below U once U moves to the top left in beat 3)
        u_tgt = u.copy().move_to(np.array([-6.6, 3.5, 0]), aligned_edge=UL)
        w.move_to(np.array([-6.6, u_tgt.get_bottom()[1] - .4 - w.height / 2, 0]), aligned_edge=LEFT)

        # ---- Pi (right of W) and the three slots (where the figure was) ----
        pi = E(r"\Pi|=|U|-|W", size=52)
        pi.move_to(np.array([w.get_right()[0] + 1.1, w.get_y(), 0]), aligned_edge=LEFT)
        assert pi.get_right()[0] < 6.6
        slots = VGroup()
        for k in ("1", "2", "3"):
            lab = E(r"\partial|\Pi|/|\partial|q_" + k, size=44)
            box = DashedVMobject(RoundedRectangle(width=2.2, height=1.0, corner_radius=.12,
                                                  color=HAIR, stroke_width=2.5), num_dashes=32)
            zero = M("=0", size=44)
            row = VGroup(box, zero).arrange(RIGHT, buff=.2)
            slots.add(VGroup(lab, row).arrange(DOWN, buff=.25))
        slots.arrange(RIGHT, buff=.7)
        fit(slots, 13.0, 3.0)
        slots.move_to(np.array([0, -1.7, 0]))

        # ---- the shared HW P1 figure, bottom, 0.5 clear of the frame (scale .9 keeps labels at 36) ----
        fig = hw_figure()
        fig.scale(.9).set_x(0).to_edge(DOWN, buff=.5)
        assert fig.get_left()[0] >= -6.6 and fig.get_right()[0] <= 6.6
        assert fig.get_top()[1] < w.get_bottom()[1] - .1
        load = {i: VGroup(fig.P[i], fig.Plab[i]) for i in (1, 2, 3, 4)}

        def pulse(m, s=1.18):
            return m.animate(rate_func=there_and_back).scale(s)

        # ---- beat 1: table shrinks, each row flies into a term ----
        with self.say("Now the strain energy: one half, stiffness, times stretch squared, "
                      "for each spring, all added up.") as d:
            self.play(FadeIn(card), run_time=.12 * d)
            self.play(MoveToTarget(card), run_time=.18 * d)
            self.play(FadeIn(ug[0]), FadeIn(ug[1]), run_time=.08 * d)
            for i, gi in enumerate((2, 4, 6, 8)):
                a, b = rows[i]
                g = ug[gi]
                anims = [FadeIn(g[0], shift=.1 * DOWN), TransformFromCopy(a, g[1]),
                         TransformFromCopy(b, VGroup(*g[2:]))]
                if gi > 2:
                    anims.append(FadeIn(ug[gi - 1]))
                self.play(*anims, run_time=.13 * d)

        # ---- beat 2: read the sum, a box walks term by term (and row by row) ----
        with self.say("U equals one half K one q two squared, plus one half K two q one squared, plus one half "
                      "K two, q two minus q one, squared, plus one half K three, q three minus q two, squared.") as d:
            bx = SurroundingRectangle(ug[2], color=MUTED, buff=.09, corner_radius=.08)
            rx = SurroundingRectangle(VGroup(*rows[0]), color=MUTED, buff=.08, corner_radius=.08)
            self.play(Indicate(ug[0], color=MINT), run_time=.08 * d)
            self.play(Create(bx), Create(rx), run_time=.12 * d)
            self.wait(.08 * d)
            for i, gi in enumerate((4, 6, 8)):
                self.play(Transform(bx, SurroundingRectangle(ug[gi], color=MUTED, buff=.09, corner_radius=.08)),
                          Transform(rx, SurroundingRectangle(VGroup(*rows[i + 1]), color=MUTED, buff=.08,
                                                             corner_radius=.08)), run_time=.1 * d)
                self.wait((.1 if i < 2 else .14) * d)
            self.play(FadeOut(bx), FadeOut(rx), run_time=.06 * d)

        # ---- beat 3: W; each load pulses with its term as it is named ----
        with self.say("The work potential: each load times the displacement of the point it's on. P one acts at "
                      "q one. P two and P three both act on the bar, at q two. P four acts at q three.") as d:
            self.play(FadeOut(card), u.animate.move_to(u_tgt), run_time=.1 * d)
            self.play(FadeIn(fig), FadeIn(wg[0]), FadeIn(wg[1]), run_time=.12 * d)
            self.wait(.16 * d)
            self.play(FadeIn(wg[2]), run_time=.05 * d)
            self.play(pulse(load[1]), pulse(fig.q[1]), pulse(wg[2]), run_time=.1 * d)
            self.play(FadeIn(wg[3]), FadeIn(wg[4]), run_time=.06 * d)
            self.play(pulse(load[2]), pulse(load[3]), pulse(VGroup(*wg[4][0:5])), run_time=.11 * d)
            self.play(pulse(fig.q[2]), pulse(wg[4][5]), run_time=.09 * d)
            self.play(FadeIn(wg[5]), FadeIn(wg[6]), run_time=.05 * d)
            self.play(pulse(load[4]), pulse(fig.q[3]), pulse(wg[6]), run_time=.11 * d)

        # ---- beat 4: Pi = U - W, three unknowns, three slots ----
        with self.say("And Pi is U minus W. Three unknowns, so we'll take three partial derivatives "
                      "and set each one to zero.") as d:
            self.play(FadeIn(pi[0]), FadeIn(pi[1]), TransformFromCopy(ug[0], pi[2]), FadeIn(pi[3]),
                      TransformFromCopy(wg[0], pi[4]), run_time=.2 * d)
            self.play(FadeIn(glow(pi[0], GOLD)), run_time=.08 * d)
            self.play(*[pulse(fig.q[i], 1.3) for i in (1, 2, 3)], run_time=.16 * d)
            self.play(FadeOut(fig), run_time=.1 * d)
            self.play(LaggedStart(*[FadeIn(s, shift=.15 * UP) for s in slots], lag_ratio=.35), run_time=.3 * d)
        self.wait(1.0)
        self.wipe()
