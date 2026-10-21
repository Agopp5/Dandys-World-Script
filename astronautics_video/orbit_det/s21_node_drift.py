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

        view = View(elev=20, azim=-60, scale=1.3, center=(-3.4, -0.5))
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
        i_arc = arc3(view, lambda: nhat(om()), lambda: np.cross(K3, nhat(om())), ii, 1.2, EMBER)
        i_lab = label3(view, "i", lambda: 1.5 * mhat(om(), ii() / 2), EMBER, 40)
        scene3d = VGroup(earth, ax3, equator, plane, orb, node_line, node_dot, om_arc, om_lab, i_arc, i_lab)

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
                      Create(om_arc), FadeIn(om_lab), Create(i_arc), FadeIn(i_lab), FadeIn(i_read),
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
