"""S01: the problem, six numbers you can't picture (BRIEF.md S01)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# ---------------------------------------------------------------- facts (Kluever Example 3.1)
MU = 3.986e5
R0 = np.array([9031.5, -5316.9, -1647.2])          # km
V0 = np.array([-2.8640, 5.1112, -5.0805])          # km/s
r0n, v0n = np.linalg.norm(R0), np.linalg.norm(V0)
assert np.isclose(r0n, 10609.0, atol=0.5) and np.isclose(v0n, 7.7549, atol=1e-3)
EN = v0n ** 2 / 2 - MU / r0n
A_KM = -MU / (2 * EN)
assert np.isclose(EN, -7.5027, atol=1e-3) and round(A_KM) == 26564
H = np.cross(R0, V0)
hn = np.linalg.norm(H)
assert np.isclose(hn, 69086, rtol=1e-4)
EV = np.cross(V0, H) / MU - R0 / r0n
ECC = np.linalg.norm(EV)
assert np.isclose(ECC, 0.7411, atol=2e-4) and np.isclose(np.sqrt(1 + 2 * EN * hn ** 2 / MU ** 2), ECC, atol=1e-4)
P_HAT, H_HAT = EV / ECC, H / hn
Q_HAT = np.cross(H_HAT, P_HAT)
CPN = np.array([P_HAT, Q_HAT, H_HAT])              # rows p-hat, q-hat, h-hat in ECI
INC = np.degrees(np.arccos(CPN[2, 2]))
RAAN = np.degrees(np.arctan2(CPN[2, 0], -CPN[2, 1])) % 360
ARGP = np.degrees(np.arctan2(CPN[0, 2], CPN[1, 2])) % 360
cos_t0 = EV @ R0 / (ECC * r0n)
assert R0 @ V0 < 0                                 # heading toward perigee: theta0 in (180, 360)
TH0 = 360 - np.degrees(np.arccos(cos_t0))
assert round(INC, 1) == 63.4 and round(RAAN) == 145 and round(ARGP) == 270 and round(TH0) == 280
assert np.isclose(ECC, 0.741, atol=5e-4)


def rv_eci(th):
    """Exact two-body state (km, km/s) of the real Molniya at true anomaly th (rad)."""
    p = A_KM * (1 - ECC ** 2)
    r = p / (1 + ECC * np.cos(th))
    rP = r * np.array([np.cos(th), np.sin(th), 0.0])
    vP = np.sqrt(MU / p) * np.array([-np.sin(th), ECC + np.cos(th), 0.0])
    return CPN.T @ rP, CPN.T @ vP


def mean_from_theta(th, e=ECC):
    E_ = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(th / 2), np.sqrt(1 + e) * np.cos(th / 2))
    return E_ - e * np.sin(E_)


def theta_from_mean(Mv, e=ECC):
    """Kepler's equation by Newton from E = pi (converges for every M in [0, 2 pi))."""
    m = Mv % TAU
    E_ = np.pi
    for _ in range(25):
        E_ -= (E_ - e * np.sin(E_) - m) / (1 - e * np.cos(E_))
    return (2 * np.arctan2(np.sqrt(1 + e) * np.sin(E_ / 2), np.sqrt(1 - e) * np.cos(E_ / 2))) % TAU


TH0_R = np.radians(TH0)
M0 = mean_from_theta(TH0_R) % TAU
assert np.isclose(theta_from_mean(M0), TH0_R)
_r, _v = rv_eci(TH0_R)
assert np.allclose(_r, R0, atol=2.0) and np.allclose(_v, V0, atol=2e-3)   # round trip matches the measurement

FS = 44                                            # readout digit size


def column(label_tex, vals, nd, widest, unit):
    """Column vector of live DecimalNumbers (right-aligned), brackets sized for the widest value it will show."""
    nums = VGroup(*[DecimalNumber(v, num_decimal_places=nd, font_size=FS, color=INK, edge_to_fix=RIGHT)
                    for v in vals]).arrange(DOWN, aligned_edge=RIGHT, buff=0.2)
    W = DecimalNumber(widest, num_decimal_places=nd, font_size=FS).width
    xR = nums.get_right()[0]
    xL = xR - W
    top, bot = nums.get_top()[1] + 0.15, nums.get_bottom()[1] - 0.15
    lb = VMobject(stroke_color=INK, stroke_width=3).set_points_as_corners(
        [[xL - 0.08, top, 0], [xL - 0.22, top, 0], [xL - 0.22, bot, 0], [xL - 0.08, bot, 0]])
    rb = VMobject(stroke_color=INK, stroke_width=3).set_points_as_corners(
        [[xR + 0.08, top, 0], [xR + 0.22, top, 0], [xR + 0.22, bot, 0], [xR + 0.08, bot, 0]])
    lab = M(label_tex + "=", size=46).next_to(lb, LEFT, buff=0.18)
    un = M(r"\text{" + unit + "}", size=34, color=MUTED).next_to(rb, RIGHT, buff=0.15)
    g = VGroup(lab, lb, nums, rb, un)
    g.nums = nums
    return g


class S01_Hook(VScene):
    budget = 120

    def construct(self):
        # ------------------------------------------------ 3D view (left two thirds)
        view = View(elev=22, azim=62, scale=1.0, center=(-3.0, -1.6))  # looks roughly down h-hat: the ellipse reads open
        earth = globe(view)
        ax3 = axes3(view, 2.2)
        Om, inc, w = np.radians(RAAN), np.radians(INC), np.radians(ARGP)
        f = orbit(3.0, 0.6, Om, inc, w)            # drawn Molniya (not to scale), same orientation
        mt = ValueTracker(M0)                      # mean anomaly: uniform in time, so Kepler's timing is real

        def th():
            return theta_from_mean(mt.get_value())

        def sat():
            return np.array(f(th()), dtype=float)

        def vvec():
            t = th()
            d = np.array(f(t + 1e-3), dtype=float) - np.array(f(t - 1e-3), dtype=float)
            return d / np.linalg.norm(d) * 0.12 * np.linalg.norm(rv_eci(t)[1])

        r_arr = arrow3(view, lambda: np.zeros(3), sat, INK)
        v_arr = arrow3(view, sat, lambda: sat() + vvec(), ACCENT)
        r_arr.k.set_value(0)
        v_arr.k.set_value(0)
        sat_dot = dot3(view, sat, INK)
        r_lab = label3(view, r"\vec r", lambda: 0.55 * sat() + np.array([0, 0, 0.4]), INK, 36)
        v_lab = label3(view, r"\vec v", lambda: sat() + 1.25 * vvec(), ACCENT, 36)
        path = curve(view, f, 0, TAU, INK, width=4, R=1.0)

        # ------------------------------------------------ right: the measurement
        rcol = column(r"\vec r_0", R0, 1, -46250.0, "km").move_to(RIGHT * 4.3 + UP * 1.55)
        vcol = column(r"\vec v_0", V0, 3, -10.000, "km/s").move_to(RIGHT * 4.3 + DOWN * 1.55)
        vcol.shift(RIGHT * (rcol[1].get_left()[0] - vcol[1].get_left()[0]))   # brackets line up

        with self.say("A tracking station measures a satellite and radios down six numbers: three for its position, and three for its velocity.") as d:
            self.play(FadeIn(earth), FadeIn(ax3), run_time=0.2 * d)
            self.add(r_arr)
            self.play(Write(rcol), r_arr.k.animate.set_value(1), FadeIn(sat_dot), FadeIn(r_lab), run_time=0.3 * d)
            self.wait(0.05 * d)
            self.add(v_arr)
            self.play(Write(vcol), v_arr.k.animate.set_value(1), FadeIn(v_lab), run_time=0.3 * d)

        qs = VGroup(*[T("?", size=80, color=ACCENT, weight=BOLD) for _ in range(3)])
        for q, p in zip(qs, [(-6.0, 2.4, 0), (-0.9, 2.2, 0), (-5.4, -2.8, 0)]):
            q.move_to(p)
        self.beat("Here they are. Can you tell what this orbit looks like? Is it round or stretched? Tilted or flat? Where is the satellite in its loop?",
                  Indicate(VGroup(rcol.nums, vcol.nums), color=ACCENT, scale_factor=1.08), .1,
                  GrowFromCenter(qs[0]), .1, GrowFromCenter(qs[1]), .15, GrowFromCenter(qs[2]))

        # live readouts: every component of r and v follows the moving satellite
        for k in range(3):
            rcol.nums[k].add_updater(lambda m, k=k: m.set_value(rv_eci(th())[0][k]))
            vcol.nums[k].add_updater(lambda m, k=k: m.set_value(rv_eci(th())[1][k]))
        self.beat("Worse, as the satellite moves, all six numbers keep changing.",
                  mt.animate(rate_func=linear).set_value(M0 + 0.55))

        # ------------------------------------------------ the same orbit, six better numbers
        rows = VGroup(
            E(r"a|=|26{,}564\ \text{km}", size=48),
            E(r"e|=|0.741", size=48, cmap={"e": ROSE}),
            E(r"i|=|63.4^\circ", size=48),
            E(r"\Omega|=|145^\circ", size=48),
            E(r"\omega|=|270^\circ", size=48),
        )
        hues = [INK, ROSE, EMBER, SKY, MINT]
        for row, hue in zip(rows, hues):
            row[0].set_color(hue)
            row[2].set_color(hue)
        th_lab = E(r"\theta_0|=", size=48)
        th_num = DecimalNumber(round(TH0), num_decimal_places=0, unit=r"^\circ", font_size=FS + 2, color=GOLD,
                               edge_to_fix=LEFT)
        th_row = VGroup(th_lab[0], th_lab[1], th_num)
        th_num.next_to(th_lab, RIGHT, buff=0.2)
        rows.add(th_row)
        for row in rows:                           # line up the = signs
            row.arrange(RIGHT, buff=0.2)
        rows.arrange(DOWN, buff=0.32)
        eq_x = rows[0][1].get_center()[0]
        for row in rows:
            row.shift(RIGHT * (eq_x - row[1].get_center()[0]))
        rows.move_to(RIGHT * 4.5 + UP * 1.0)

        with self.say("Now here is the same orbit, described by a different set of six numbers.") as d:
            self.play(FadeOut(qs), FadeIn(path), mt.animate(rate_func=linear).set_value(M0 + TAU),
                      run_time=0.55 * d)
            for m in [*rcol.nums, *vcol.nums]:
                m.clear_updaters()
            olds = [*rcol.nums, *vcol.nums]
            self.play(*[ReplacementTransform(olds[k], rows[k][2]) for k in range(6)],
                      *[FadeOut(m) for m in (rcol[0], rcol[1], rcol[3], rcol[4], vcol[0], vcol[1], vcol[3], vcol[4])],
                      *[FadeIn(VGroup(r[0], r[1])) for r in rows], run_time=0.4 * d)

        th_new = E(r"\theta", size=48)[0].move_to(th_lab[0], aligned_edge=RIGHT)
        th_num.add_updater(lambda m: m.set_value(round(np.degrees(th())) % 360))
        with self.say("Five of them never change. Only the last one moves, like the hand of a clock. And every one of them has a picture you can see.") as d:
            glows = VGroup(*[glow(rows[k], hues[k]) for k in range(5)])
            self.play(LaggedStart(*[FadeIn(g) for g in glows], lag_ratio=0.2), run_time=0.25 * d)
            self.play(ReplacementTransform(th_lab[0], th_new), run_time=0.06 * d)
            self.play(mt.animate(rate_func=linear).set_value(M0 + TAU + 1.0), run_time=0.4 * d)
            self.play(LaggedStart(*[Indicate(r[0], color=h, scale_factor=1.3) for r, h in zip(rows, hues + [GOLD])],
                                  lag_ratio=0.25), Indicate(path, color=INK2, scale_factor=1.0), run_time=0.24 * d)
        th_num.clear_updaters()

        chips = VGroup(chip("meaning", ACCENT), chip("r, v to elements", ACCENT), chip("elements to r, v", ACCENT)).scale(1.35)
        chips.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(rows, DOWN, buff=0.55).align_to(rows, LEFT)
        self.beat("This lesson is about those six numbers: what each one means, how to get them from a measurement, and how to go back.",
                  .2, FadeIn(chips[0], shift=0.2 * UP), .15, FadeIn(chips[1], shift=0.2 * UP), .15,
                  FadeIn(chips[2], shift=0.2 * UP))
        self.wipe()
