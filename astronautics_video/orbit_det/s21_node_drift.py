"""S21: the node drifts (BRIEF.md S21)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# ---------------------------------------------------------------- facts
MU, RE, J2 = 3.986e5, 6378.137, 1.08263e-3
DEG_PER_DAY = 86400 * 180 / np.pi


def node_rate(alt_km, i_deg, e=0.0):
    """Omega-dot in deg/day for a circular (e=0) orbit at altitude alt_km."""
    a = RE + alt_km
    n = np.sqrt(MU / a ** 3)
    return -(3 * n * J2 * RE ** 2) / (2 * a ** 2 * (1 - e ** 2) ** 2) * np.cos(np.radians(i_deg)) * DEG_PER_DAY


def sso_incl(alt_km):
    k = -node_rate(alt_km, 0.0)                      # magnitude of the cos i coefficient
    return np.degrees(np.arccos(-(360 / 365.24) / k))


ISS_RATE = node_rate(400, 51.6)
assert np.isclose(ISS_RATE, -5.0, atol=0.05)          # "about five degrees per day", westward
assert np.isclose(node_rate(500, 90.0), 0.0, atol=1e-12)   # polar: no drift
assert node_rate(500, 98.0) > 0                       # retrograde: eastward
SSO_RATE = 360 / 365.24
assert np.isclose(SSO_RATE, 0.9856, atol=1e-4)        # once per year, about one degree per day
assert np.isclose(sso_incl(700), 98.2, atol=0.05)     # 700 km -> 98.2 deg
assert np.isclose(sso_incl(500), 97.4, atol=0.05) and np.isclose(sso_incl(800), 98.6, atol=0.05)

# ---------------------------------------------------------------- drawing helpers
RO = 2.4                       # drawn orbit radius (circular, not to scale: ISS / SSO are near-circular)
K3 = np.array([0.0, 0.0, 1.0])
I3 = np.array([1.0, 0.0, 0.0])
XR = 3.95                      # x of the right column


def nhat(Om):
    return np.array([np.cos(Om), np.sin(Om), 0.0])


def mhat(Om, i):               # h-hat x n-hat: in-plane direction 90 deg past the ascending node
    return np.array([-np.cos(i) * np.sin(Om), np.cos(i) * np.cos(Om), np.sin(i)])


class S21_Node_Drift(VScene):
    budget = 150

    def construct(self):
        Om = ValueTracker(70.0)        # degrees
        inc = ValueTracker(51.6)       # degrees
        om = lambda: np.radians(Om.get_value())
        ii = lambda: np.radians(inc.get_value())

        view = View(elev=18, azim=15, scale=1.3, center=(-3.4, -0.5))
        earth = globe(view)
        ax3 = axes3(view, 3.2)
        equator = curve(view, lambda t: (RO * np.cos(t), RO * np.sin(t), 0.0), 0, TAU, MUTED, width=2, R=1.0)
        plane = disc3(view, lambda: nhat(om()), lambda: mhat(om(), ii()), RO, INK2, 0.12)
        orb = curve(view, lambda t: RO * (np.cos(t) * nhat(om()) + np.sin(t) * mhat(om(), ii())),
                    0, TAU, INK, width=4, R=1.0)
        node_line = line3(view, lambda: -RO * nhat(om()), lambda: RO * nhat(om()), SKY, dashed=True)
        node_dot = dot3(view, lambda: RO * nhat(om()), SKY)
        om_arc = arc3(view, K3, I3, om, 1.5, SKY)
        om_lab = label3(view, r"\Omega", lambda: 1.95 * nhat(om() / 2), SKY, 40)
        i_arc = arc3(view, lambda: nhat(om()), lambda: np.cross(K3, nhat(om())), ii, 1.75, EMBER)
        i_lab = label3(view, "i", lambda: 2.1 * mhat(om(), ii() / 2), EMBER, 40)
        hhat = lambda: np.cross(nhat(om()), mhat(om(), ii()))
        h_arr = arrow3(view, np.zeros(3), lambda: 2.3 * hhat(), LILAC)
        h_lab = label3(view, r"\hat h", lambda: 2.65 * hhat(), LILAC, 40)
        scene3d = Group(earth, ax3, equator, plane, orb, node_line, node_dot, om_arc, om_lab, i_arc, i_lab, h_arr, h_lab)

        # live inclination readout (top left)
        i_num = DecimalNumber(51.6, num_decimal_places=1, unit=r"^{\circ}", font_size=44, color=EMBER)
        i_eq = M("i =", size=44, color=EMBER)
        i_read = VGroup(i_eq, i_num).arrange(RIGHT, buff=0.2).move_to([-5.4, 3.35, 0])
        i_num.add_updater(lambda m: m.set_value(inc.get_value()).next_to(i_eq, RIGHT, buff=0.2))

        # ------------------------------------------------ beat 1: the formula
        fml = E(r"\dot\Omega|=|-\frac{3\,n\,J_2\,R^2}{2\,a^2\,(1-e^2)^2}|\cos|i", size=46)
        paint(fml, {0: SKY})
        fml.move_to([XR, 2.75, 0])
        nline = E(r"n|=|\sqrt{\mu / a^3}", size=40).move_to([XR - 0.6, 1.35, 0])
        nnote = T("mean motion", size=26, color=MUTED).next_to(nline, RIGHT, buff=0.35)
        with self.say("The drift rate of the node is Omega dot equals minus three n J two R squared, over two a squared, times one minus e squared, squared, times cosine i.") as d:
            self.play(FadeIn(earth), FadeIn(ax3), Create(equator), run_time=0.12 * d)
            self.play(FadeIn(plane), Create(orb), FadeIn(node_line), FadeIn(node_dot),
                      Create(om_arc), FadeIn(om_lab), Create(i_arc), FadeIn(i_lab), FadeIn(i_read), FadeIn(h_arr), FadeIn(h_lab),
                      run_time=0.13 * d)
            self.play(Write(fml), run_time=0.45 * d)
            self.play(FadeIn(nline, shift=0.2 * UP), FadeIn(nnote), run_time=0.15 * d)

        # ------------------------------------------------ beat 2: cos i > 0 -> westward
        ghost = dot3(view, RO * nhat(np.radians(70.0)), MUTED)
        r1 = E(r"\cos|i|> 0|\;\Rightarrow\;|\dot\Omega|< 0", size=42)
        paint(r1, {4: SKY})
        r1.move_to([XR, -0.05, 0])
        r1n = T("prograde: the node slides westward", size=26, color=MUTED).next_to(r1, DOWN, buff=0.25)
        card_t = T("Space station, 400 km", size=30, color=INK2)
        card_e = E(r"\dot\Omega|\approx|-5.0^\circ\text{/day}", size=42)
        paint(card_e, {0: SKY})
        card = panel(VGroup(card_t, card_e).arrange(DOWN, buff=0.25)).move_to([XR, -2.45, 0])
        with self.say("Read the cosine i. For a prograde orbit, cosine i is positive, so Omega dot is negative: the node slides westward. For the space station, about five degrees per day.") as d:
            self.play(Circumscribe(VGroup(fml[3], fml[4]), color=EMBER), run_time=0.15 * d)
            self.play(Write(r1), run_time=0.15 * d)
            self.add(ghost)
            self.play(FadeIn(r1n), Om.animate.set_value(40.0), run_time=0.35 * d, rate_func=linear)
            self.play(FadeIn(card, shift=0.2 * UP), run_time=0.12 * d)
            g1 = glow(card_e, SKY)
            self.play(FadeIn(g1), run_time=0.1 * d)

        # ------------------------------------------------ beat 3: polar stops, retrograde reverses
        r2 = E(r"\cos|i|= 0|\;\Rightarrow\;|\dot\Omega|= 0", size=42)
        paint(r2, {4: SKY})
        r2.move_to([XR, -0.05, 0])
        r2n = T("polar: no drift at all", size=26, color=MUTED).next_to(r2, DOWN, buff=0.25)
        r3 = E(r"\cos|i|< 0|\;\Rightarrow\;|\dot\Omega|> 0", size=42)
        paint(r3, {4: SKY})
        r3.move_to([XR, -1.75, 0])
        r3n = T("retrograde: the node drifts eastward", size=26, color=MUTED).next_to(r3, DOWN, buff=0.25)
        old2 = [r1, r1n, card, g1]
        with self.say("For a polar orbit, cosine i is zero, and the node doesn't drift at all. For a retrograde orbit, it drifts eastward.") as d:
            self.play(*[FadeOut(m) for m in old2], run_time=0.08 * d)
            self.play(inc.animate.set_value(90.0), Om.animate(rate_func=rate_functions.ease_out_sine).set_value(30.0),
                      FadeIn(r2), run_time=0.3 * d)
            self.play(FadeIn(r2n), Indicate(r2[4], color=SKY), run_time=0.14 * d)
            self.play(inc.animate.set_value(98.0), Om.animate(rate_func=rate_functions.ease_in_sine).set_value(40.0),
                      FadeIn(r3), run_time=0.3 * d)
            self.play(FadeIn(r3n), run_time=0.1 * d)

        # ------------------------------------------------ beat 4: the Sun inset
        S = np.array([-3.3, -0.25, 0.0])
        RS, HALF, BETA = 2.6, 0.85, np.radians(55)
        lam0 = -0.42 * PI
        lam = ValueTracker(lam0)
        epos = lambda: S + RS * np.array([np.cos(lam.get_value()), np.sin(lam.get_value()), 0.0])
        udir = lambda ang: np.array([np.cos(ang), np.sin(ang), 0.0])
        sun = Dot(S, radius=0.34, color=GOLD)
        sun_g = glow(sun, GOLD)
        sun_l = T("Sun", size=28, color=GOLD).next_to(sun, DOWN, buff=0.25)
        path = DashedVMobject(Circle(radius=RS, color=MUTED, stroke_width=2).move_to(S), num_dashes=70)
        sunline = always_redraw(lambda: DashedLine(epos(), epos() + 1.25 * (S - epos()) / RS, color=GOLD,
                                                   stroke_width=3))
        fixed = always_redraw(lambda: DashedLine(epos() - HALF * udir(lam0 + PI + BETA),
                                                 epos() + HALF * udir(lam0 + PI + BETA), color=MUTED,
                                                 stroke_width=4))
        seg = always_redraw(lambda: Line(epos() - HALF * udir(lam.get_value() + PI + BETA),
                                         epos() + HALF * udir(lam.get_value() + PI + BETA), color=INK,
                                         stroke_width=7))
        ang = always_redraw(lambda: Arc(radius=0.5, start_angle=lam.get_value() + PI, angle=BETA,
                                        arc_center=epos(), color=GOLD, stroke_width=5))
        edot = always_redraw(lambda: Dot(epos(), radius=0.15, color=INK2))
        leg = VGroup(
            VGroup(Line(ORIGIN, 0.6 * RIGHT, color=INK, stroke_width=7), T("orbit plane, node drifting", size=26)),
            VGroup(DashedLine(ORIGIN, 0.6 * RIGHT, color=MUTED, stroke_width=4),
                   T("plane with no drift", size=26, color=MUTED)),
        )
        for row in leg:
            row.arrange(RIGHT, buff=0.25)
        leg.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL, buff=0.35)
        sun_scene = Group(path, sun_g, sun, sun_l, fixed, sunline, seg, ang, edot)

        s1 = E(r"\dot\Omega|=|+\frac{360^\circ}{365.24\ \text{days}}", size=42)
        paint(s1, {0: SKY})
        s1.move_to([XR, 1.15, 0])
        s2 = E(r"\approx|+0.9856^\circ\text{/day}", size=42).next_to(s1, DOWN, buff=0.45).align_to(s1[1], LEFT)
        s2n = T("once per year, eastward", size=26, color=MUTED).next_to(s2, DOWN, buff=0.25)
        old3 = [r2, r2n, r3, r3n, nline, nnote, i_read, ghost]
        with self.say("Engineers use that eastward drift on purpose. If the node turns exactly once per year, about one degree per day, the orbit plane keeps the same angle to the Sun all year.") as d:
            i_num.clear_updaters()
            self.play(FadeOut(scene3d), *[FadeOut(m) for m in old3], run_time=0.1 * d)
            self.play(FadeIn(path), FadeIn(sun_g), FadeIn(sun), FadeIn(sun_l), FadeIn(edot), FadeIn(sunline),
                      FadeIn(fixed), FadeIn(seg), FadeIn(ang), FadeIn(leg), run_time=0.14 * d)
            self.play(Write(s1), run_time=0.16 * d)
            self.play(lam.animate.set_value(lam0 + TAU), FadeIn(s2, run_time=0.1 * d),
                      FadeIn(s2n, run_time=0.1 * d), run_time=0.55 * d, rate_func=linear)

        # ------------------------------------------------ beat 5: sun synchronous, 98.2 deg at 700 km
        t5 = T("sun synchronous orbit", size=32, color=INK).move_to([XR, -1.45, 0])
        e5 = E(r"700\ \text{km}:|\quad|i|\approx|98.2^\circ", size=44).next_to(t5, DOWN, buff=0.35)
        paint(e5, {4: EMBER})
        n5 = T("same lighting every pass", size=30, color=GOLD).next_to(e5, DOWN, buff=0.3)
        with self.say("That's a sun synchronous orbit. At seven hundred kilometers, it needs an inclination of about ninety eight degrees.") as d:
            self.play(FadeIn(t5, shift=0.2 * UP), lam.animate(rate_func=linear).set_value(lam0 + TAU + 0.5 * PI),
                      run_time=0.3 * d)
            self.play(Write(e5), lam.animate(rate_func=linear).set_value(lam0 + TAU + 1.1 * PI), run_time=0.35 * d)
            g5 = glow(e5[4], EMBER)
            self.play(FadeIn(g5), FadeIn(n5), lam.animate(rate_func=linear).set_value(lam0 + TAU + 1.6 * PI),
                      run_time=0.3 * d)

        # ------------------------------------------------ beat 6: a, e, i only wiggle
        x_max = 6
        ax_a = axes([0, x_max, 1], [-1, 1, 1], width=6.0, height=3.8, xlabel="", ylabel="")
        ax_o = axes([0, x_max, 1], [-1, 1, 1], width=6.0, height=3.8, xlabel="", ylabel="")
        ax_a.move_to([-3.45, 0.3, 0])
        ax_o.move_to([3.45, 0.3, 0])
        f_a = lambda t: 0.22 * np.sin(4 * PI * t)                   # short-period wiggle, twice per orbit
        f_o = lambda t: 0.7 - 0.25 * t + 0.16 * np.sin(4 * PI * t)  # same wiggle on a steady downward trend
        c_a = ax_a.plot(f_a, x_range=[0, x_max, 0.02], color=INK, stroke_width=4)
        c_o = ax_o.plot(f_o, x_range=[0, x_max, 0.02], color=SKY, stroke_width=4)
        m_a = DashedLine(ax_a.c2p(0, 0), ax_a.c2p(x_max, 0), color=MUTED, stroke_width=3)
        m_o = DashedLine(ax_o.c2p(0, 0.7), ax_o.c2p(x_max, 0.7 - 0.25 * x_max), color=MUTED, stroke_width=3)
        yl_a = M("a", size=40).next_to(ax_a.c2p(0, 1), LEFT, buff=0.25)
        yl_o = M(r"\Omega", size=40, color=SKY).next_to(ax_o.c2p(0, 1), LEFT, buff=0.25)
        xl_a = M("t", size=40).next_to(ax_a.c2p(x_max, 0), DR, buff=0.12)
        xl_o = M("t", size=40).next_to(ax_o.c2p(x_max, 0), DR, buff=0.12)
        head = T("a, e and i only wiggle", size=36).move_to([0, 3.3, 0])
        cap_a = T("a: wiggles, no trend", size=30).next_to(ax_a, DOWN, buff=0.45)
        cap_o = VGroup(M(r"\Omega", size=40, color=SKY), T(": wiggles plus a steady drift", size=30)).arrange(RIGHT, buff=0.1).next_to(ax_o, DOWN, buff=0.45)
        note6 = T("schematic, t in orbits", size=26, color=MUTED).move_to([0, -3.55, 0])
        old4 = [sun_scene, leg, fml, s1, s2, s2n, t5, e5, g5, n5]
        with self.say("Meanwhile a, e and i don't drift. They only wiggle a little each orbit, like your notes sketch.") as d:
            self.play(*[FadeOut(m) for m in old4], run_time=0.1 * d)
            self.play(FadeIn(head), Create(ax_a), Create(ax_o), FadeIn(yl_a), FadeIn(yl_o), FadeIn(xl_a),
                      FadeIn(xl_o), run_time=0.15 * d)
            self.play(Create(m_a), Create(c_a), FadeIn(cap_a), run_time=0.3 * d, rate_func=linear)
            self.play(Create(m_o), Create(c_o), FadeIn(cap_o), FadeIn(note6), run_time=0.3 * d, rate_func=linear)
        self.wipe()
