"""S05: turn two, the inclination (BRIEF.md S05)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# generic drawn orbit (not to scale): a = 2.4, e = 0.5, Omega = 50 deg, omega not applied yet (that is S06)
A, ECC = 2.4, 0.5
OM = np.radians(50)
I0 = np.radians(40)
IX = np.array([1.0, 0, 0])
KZ = np.array([0, 0, 1.0])
NHAT = np.array([np.cos(OM), np.sin(OM), 0])      # node line (ascending node direction)
MHAT = np.cross(KZ, NHAT)                         # in the equator, 90 deg east of the node


def rot(v, axis, ang):
    """Rodrigues: turn v right-handedly about the unit axis by ang."""
    k = axis / np.linalg.norm(axis)
    return v * np.cos(ang) + np.cross(k, v) * np.sin(ang) + k * np.dot(k, v) * (1 - np.cos(ang))


def hhat(i):
    return np.array([np.sin(i) * np.sin(OM), -np.sin(i) * np.cos(OM), np.cos(i)])


def vel(f, t, dt=1e-5):
    return (f(t + dt) - f(t - dt)) / (2 * dt)


# facts
_f = orbit(A, ECC, OM, I0, 0)
assert np.allclose(cpn(OM, I0, 0)[2], hhat(I0))               # third row of C_PN = h-hat
assert np.allclose(cpn(OM, I0, 0)[0], NHAT)                   # omega = 0: periapsis on the node line
assert np.allclose(rot(KZ, NHAT, I0), hhat(I0))               # K turned about the node line by i is h-hat
assert np.allclose(rot(MHAT, NHAT, I0), cpn(OM, I0, 0)[1])    # the equator turned by i is the orbit plane
assert np.isclose(np.degrees(np.arccos(hhat(I0) @ KZ)), 40)   # i is the angle between K and h
assert np.allclose(_f(0), A * (1 - ECC) * NHAT)               # ascending node at r = 1.2
assert np.allclose(_f(np.pi), -A * (1 + ECC) * NHAT)          # descending node at r = 3.6
assert vel(_f, 0)[2] > 0 and vel(_f, np.pi)[2] < 0            # north at the ascending node, south at descending
for _deg, _sign in [(40, 1), (150, -1)]:                      # prograde h_K > 0 (east), retrograde h_K < 0 (west)
    _g = orbit(A, ECC, OM, np.radians(_deg), 0)
    assert np.sign(np.cross(_g(1.0), vel(_g, 1.0))[2]) == _sign
    assert np.sign(vel(_g, np.pi) @ (-MHAT)) == _sign         # eastward at the descending node is -MHAT
assert np.isclose(np.cos(np.radians(90)), 0, atol=1e-12)      # polar: h in the equator plane
assert 0 <= np.degrees(np.arccos(-1)) <= 180                  # arccos range: 0 to 180 deg


class S05_Turn_i(VScene):
    budget = 147

    def construct(self):
        view = View(azim=-15, scale=.92, center=(-2.9, -0.3))
        it = ValueTracker(0.0)              # inclination (rad)
        th = ValueTracker(-np.pi / 2)       # satellite true anomaly (rad)

        def ii():
            return max(it.get_value(), 1e-3)

        def orb(t):
            return orbit(A, ECC, OM, it.get_value(), 0)(t)

        def ph():
            return cpn(OM, it.get_value(), 0)[0]

        def qh():
            return cpn(OM, it.get_value(), 0)[1]

        def hh():
            return cpn(OM, it.get_value(), 0)[2]

        # --- the Omega-turned orbit, still in the equator ---
        eq_disc = disc3(view, IX, np.array([0, 1.0, 0]), 3.9, MUTED, .12)
        pl_disc = disc3(view, ph, qh, 3.7, INK, .09)
        earth = globe(view)
        ax = axes3(view, 2.8)
        node_line = line3(view, -4.3 * NHAT, 4.3 * NHAT, SKY, dashed=True)
        om_arc = arc3(view, KZ, IX, OM, 1.2, SKY)
        om_lab = label3(view, r"\Omega", rot(IX, KZ, OM / 2) * 1.55, SKY, 34)
        path = always_redraw(lambda: curve(view, orbit(A, ECC, OM, it.get_value(), 0), 0, TAU, INK, R=1.0))
        sat = dot3(view, lambda: orb(th.get_value()), INK)
        i_arc = arc3(view, NHAT, MHAT, ii, 2.0, EMBER)
        i_lab = label3(view, "i", lambda: rot(MHAT, NHAT, ii() / 2) * 2.35, EMBER, 36)
        setup = Group(eq_disc, pl_disc, earth, ax, node_line, om_arc, om_lab, path, sat)

        col1 = VGroup(T("Turn two", size=30, color=MUTED), E(r"C_1(|i|)", size=52),
                      T("tilt about the line of nodes", size=28)).arrange(DOWN, buff=.35)
        place(col1, "right")

        self.beat("Turn two: tilt the orbit about the line of nodes, by the inclination, i.",
                  [FadeIn(setup), FadeIn(col1[0])], [FadeIn(i_arc), FadeIn(i_lab), Write(col1[1])],
                  it.animate.set_value(I0), FadeIn(col1[2]), w=(.15, .15, .55, .15))

        # --- two equator crossings per lap ---
        with self.say("Now the orbit plane and the equator cross along the line of nodes. "
                      "Each lap, the satellite crosses the equator twice.") as d:
            self.play(Indicate(col1[2], color=SKY), run_time=.25 * d)
            self.play(th.animate.set_value(0), run_time=.2 * d, rate_func=linear)
            self.play(Flash(view.p(orb(0)), color=GOLD, flash_radius=.35), run_time=.1 * d)
            self.play(th.animate.set_value(np.pi), run_time=.25 * d, rate_func=linear)
            self.play(Flash(view.p(orb(np.pi)), color=GOLD, flash_radius=.35), run_time=.1 * d)
            self.play(th.animate.set_value(1.5 * np.pi), run_time=.1 * d, rate_func=linear)

        # --- ascending and descending node ---
        dim_sky = interpolate_color(ManimColor(SKY), ManimColor(BG), .5).to_hex()
        asc = dot3(view, lambda: orb(0), SKY)
        dsc = dot3(view, lambda: orb(np.pi), dim_sky)
        asc_lab = label3(view, r"\text{ascending node}", 2.9 * NHAT + np.array([0, 0, -.4]), SKY, 28)
        dsc_lab = label3(view, r"\text{descending node}", -3.6 * NHAT + np.array([0, 0, .95]), dim_sky, 28)
        dsc_card = backed(dsc_lab)
        om_glow = VGroup(glow(om_arc, SKY), glow(om_lab, SKY))
        self.beat("Where it crosses heading north is the ascending node. Where it crosses heading south is "
                  "the descending node. Now you can see why Omega is measured to the ascending node.",
                  [FadeIn(asc), FadeIn(asc_lab), FadeOut(col1)], .15, [FadeIn(dsc), FadeIn(dsc_card)], .15,
                  FadeIn(om_glow), w=(.2, .2, .3))

        # --- i is also the angle between K and h ---
        h_arr = arrow3(view, ORIGIN, lambda: 2.6 * hh(), LILAC)
        h_lab = label3(view, r"\vec h", lambda: 2.95 * hh(), LILAC, 36)
        kh_arc = arc3(view, NHAT, KZ, ii, 1.7, EMBER)
        kh_lab = label3(view, "i", lambda: rot(KZ, NHAT, ii() / 2) * 2.05, EMBER, 36)
        h_arr.k.set_value(0)
        kh_arc.k.set_value(0)

        eq_cos = E(r"\cos|i|=|\hat K|\cdot|\hat h|", size=48)
        rd_lab = E(r"i|=", size=48)
        num = DecimalNumber(40, num_decimal_places=0, font_size=48, color=INK)
        degs = M(r"^\circ", size=48)
        rd = VGroup(rd_lab, num, degs).arrange(RIGHT, buff=.12)
        rng = E(r"0^\circ \le|i|\le 180^\circ", size=44)
        col2 = VGroup(eq_cos, rd, rng).arrange(DOWN, buff=.6)
        place(col2, "right")
        num.add_updater(lambda m: m.set_value(np.degrees(it.get_value())).next_to(rd_lab, RIGHT, buff=.12))
        degs.add_updater(lambda m: m.next_to(num, RIGHT, buff=.05).align_to(num, UP))

        self.beat("The inclination is also the angle between K and the angular momentum vector h, which sticks "
                  "straight out of the orbit plane.",
                  [FadeOut(om_glow), FadeOut(asc_lab), FadeOut(dsc_card)],
                  [FadeIn(h_arr), FadeIn(h_lab), h_arr.k.animate.set_value(1)],
                  [FadeIn(kh_arc), FadeIn(kh_lab), kh_arc.k.animate.set_value(1)], Write(eq_cos),
                  w=(.1, .3, .3, .3))

        self.beat("Inclination only runs from zero to one hundred eighty degrees.",
                  FadeIn(rd), Write(rng), w=(.4, .6))

        # --- prograde, polar, retrograde ---
        def row(tex, words):
            return VGroup(E(tex, size=40), T(words, size=28)).arrange(RIGHT, buff=.3)

        rows = VGroup(row(r"i|<|90^\circ", "prograde: eastward"),
                      row(r"i|=|90^\circ", "polar: over both poles"),
                      row(r"i|>|90^\circ", "retrograde: westward")).arrange(DOWN, buff=.4, aligned_edge=LEFT)
        fit(rows, 5.6, 3.0)
        rows.next_to(rd, DOWN, buff=.6)
        rows.set_x(rd.get_x())
        motion = arrow3(view, lambda: orb(np.pi - .3), lambda: orb(np.pi + .3), ACCENT)
        spin = arrow3(view, -2.2 * NHAT + .45 * MHAT, -2.2 * NHAT - .45 * MHAT, INK2)
        spin_lab = label3(view, r"\text{Earth's spin}", -2.2 * NHAT + np.array([0, 0, -.45]), INK2, 26)

        with self.say("Below ninety, the satellite travels eastward, the same way the Earth spins. That's a "
                      "prograde orbit. At exactly ninety, it passes over both poles: a polar orbit. Above "
                      "ninety, it travels westward: retrograde.") as d:
            self.play(view.elev.animate.set_value(62), FadeOut(eq_cos), FadeOut(rng), FadeOut(dsc),
                      FadeIn(motion), FadeIn(spin), FadeIn(spin_lab), FadeOut(kh_lab), run_time=.14 * d)
            self.play(FadeIn(rows[0]), run_time=.1 * d)
            self.snap("prograde")
            self.wait(.22 * d)
            self.play(it.animate.set_value(np.pi / 2), run_time=.16 * d)
            self.play(FadeIn(rows[1]), run_time=.08 * d)
            self.snap("polar")
            self.wait(.1 * d)
            self.play(it.animate.set_value(np.radians(150)), run_time=.12 * d)
            self.play(FadeIn(rows[2]), run_time=.06 * d)
            self.wait(.02 * d)

        summ = VGroup(VGroup(E("i", size=44), T("how steeply the plane tilts", size=28)).arrange(RIGHT, buff=.3),
                      VGroup(E(r"\Omega", size=44), T("which way the tilt faces", size=28)).arrange(RIGHT, buff=.3)
                      ).arrange(DOWN, buff=.45, aligned_edge=LEFT)
        fit(summ, 5.6, 2.4)
        summ.next_to(rd, DOWN, buff=.7)
        summ.set_x(rd.get_x())
        self.beat("So i says how steeply the plane is tilted, and Omega says which way the tilt faces.",
                  [view.elev.animate.set_value(22), it.animate.set_value(I0), FadeOut(rows), FadeOut(motion),
                   FadeOut(spin), FadeOut(spin_lab), FadeIn(dsc), FadeIn(kh_lab)],
                  FadeIn(summ[0]), FadeIn(summ[1]),
                  [FadeIn(glow(i_arc, EMBER)), FadeIn(glow(kh_arc, EMBER)), FadeIn(glow(om_arc, SKY)),
                   FadeIn(glow(om_lab, SKY))], w=(.3, .2, .2, .3))
        self.wipe()
