"""S12: step one, the semi major axis from energy (BRIEF.md S12)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# facts
MU = 3.986e5
RE = 6378.137
R0 = np.array([9031.5, -5316.9, -1647.2])
V0 = np.array([-2.8640, 5.1112, -5.0805])
r0 = np.linalg.norm(R0)
v0 = np.linalg.norm(V0)
assert np.isclose(r0, 10609.0, atol=0.5)
assert np.isclose(v0, 7.7549, atol=5e-5)
KE = v0 ** 2 / 2
PE = MU / r0
assert np.isclose(KE, 30.069, atol=5e-4)
assert np.isclose(PE, 37.572, atol=5e-4)
EN = KE - PE
assert np.isclose(EN, -7.5027, atol=5e-4) and EN < 0
A = -MU / (2 * EN)
assert np.isclose(A, 26563.6, atol=1.0)
assert round(A) == 26564
assert np.isclose(A / RE, 4.16, atol=5e-3)
T_H = 2 * np.pi * np.sqrt(A ** 3 / MU) / 3600
assert np.isclose(T_H, 11.97, atol=5e-3)

# drawn in Earth radii: r0 to scale (1.66 R_E); v0 only shows direction
RD = R0 / RE
VD = 1.5 * V0 / v0

# the true-scale Molniya orbit (Earth radii) for beat 5; r0 sits on it at theta = 280 deg
MOL = orbit(A / RE, 0.7411, np.radians(145.0), np.radians(63.4), np.radians(270.0))
assert np.allclose(MOL(np.radians(280.0)), RD, atol=.02)
APO = np.array(MOL(np.pi))
CEN = (np.array(MOL(0.0)) + APO) / 2
assert np.isclose(np.linalg.norm(APO - CEN), A / RE, atol=.01)


def measurement_card():
    r = M(r"\vec r_0 = (9031.5,\ -5316.9,\ -1647.2)\ \text{km}", size=30)
    v = M(r"\vec v_0 = (-2.8640,\ 5.1112,\ -5.0805)\ \text{km/s}", size=30, color=ACCENT)
    body = VGroup(r, v).arrange(DOWN, aligned_edge=LEFT, buff=.22)
    fit(body, 5.6, 2)
    card = panel(body)
    card.to_corner(UR, buff=.3)
    return card


class S12_Energy_a(VScene):
    budget = 107

    def construct(self):
        view = View(elev=60, azim=10, scale=1.5, center=(-3.6, -0.9))
        earth = globe(view)
        ax = axes3(view, 1.8)
        ar = arrow3(view, (0, 0, 0), tuple(RD), INK)
        av = arrow3(view, tuple(RD), tuple(RD + VD), ACCENT)
        lr = label3(view, r"\vec r_0", tuple(RD * 1.16), INK, 34)
        lv = label3(view, r"\vec v_0", tuple(RD + VD * 1.15), ACCENT, 34)
        card = measurement_card()
        X = card.get_left()[0] + .1   # left edge of the algebra column

        # 1. the measurement
        self.add(earth, ax)
        self.beat("Now the real job: start from one measurement and find all six elements. We'll use the textbook's example.",
                  FadeIn(card, shift=LEFT * .3), .1, Create(ar), Create(av), [FadeIn(lr), FadeIn(lv)],
                  w=(.3, .25, .2, .15))

        # 2. the lengths
        top = card.get_bottom()[1] - .35
        rl1 = M(r"|\vec r_0| = \sqrt{9031.5^2 + 5316.9^2 + 1647.2^2}", size=38)
        rl2 = M(r"= 10{,}609\ \text{km}", size=40)
        vl1 = M(r"|\vec v_0| = \sqrt{2.8640^2 + 5.1112^2 + 5.0805^2}", size=38, color=ACCENT)
        vl2 = M(r"= 7.7549\ \text{km/s}", size=40, color=ACCENT)
        lens = VGroup(rl1, rl2, vl1, vl2)
        for m in lens:
            fit(m, 7.0 - X, 1)
        rl1.next_to(np.array([X, top, 0]), DR, buff=0)
        rl2.next_to(rl1, DOWN, buff=.2).align_to(rl1, LEFT).shift(RIGHT * .6)
        vl1.next_to(rl2, DOWN, buff=.45).align_to(rl1, LEFT)
        vl2.next_to(vl1, DOWN, buff=.2).align_to(rl2, LEFT)
        self.beat("First, the lengths. The position vector is ten thousand six hundred nine kilometers long. The speed is seven point seven five five kilometers per second.",
                  [Write(rl1), Indicate(ar, color=INK, scale_factor=1.05)], Write(rl2), .1,
                  [Write(vl1), Indicate(av, color=ACCENT, scale_factor=1.05)], Write(vl2),
                  w=(.25, .15, .3, .2))

        # 3. the energy
        short = M(r"r_0 = 10{,}609\ \text{km},\quad", r"v_0 = 7.7549\ \text{km/s}", size=36)
        short[1].set_color(ACCENT)
        fit(short, 7.0 - X, 1)
        short.next_to(np.array([X, top, 0]), DR, buff=0)
        e1 = E(r"\mathcal{E}|=|\frac{v_0^2}{2}|-|\frac{\mu}{r_0}", size=50)
        e1[2].set_color(ACCENT)
        e1.next_to(short, DOWN, buff=.5).align_to(short, LEFT)
        e2 = M(r"= 30.069 - 37.572", size=44)
        e2.next_to(e1, DOWN, buff=.3).align_to(e1[1], LEFT)
        e3 = M(r"= -7.5027\ \text{km}^2/\text{s}^2", size=44)
        e3.next_to(e2, DOWN, buff=.3).align_to(e2, LEFT)
        why = T("negative: bound, an ellipse", size=32, color=GOOD)
        why.next_to(e3, DOWN, buff=.35).align_to(e1, LEFT)
        for m in (e1, e2, e3, why):
            fit(m, 7.0 - X, 2)
        self.beat("The energy is v squared over two, minus mu over r. That's minus seven point five zero three kilometers squared per second squared. Negative, so it's an ellipse.",
                  [ReplacementTransform(VGroup(rl1, rl2), short[0]), ReplacementTransform(VGroup(vl1, vl2), short[1])],
                  Write(e1), Write(e2), Write(e3), .1, FadeIn(why, shift=UP * .2),
                  w=(.12, .2, .18, .25, .2))

        # 4. semi major axis
        e_keep = M(r"\mathcal{E} = -7.5027\ \text{km}^2/\text{s}^2", size=40)
        fit(e_keep, 7.0 - X, 1)
        e_keep.next_to(short, DOWN, buff=.4).align_to(short, LEFT)
        a1 = E(r"a|=|-\frac{\mu}{2\mathcal{E}}", size=54)
        a1.next_to(e_keep, DOWN, buff=.5).align_to(short, LEFT)
        a2 = M(r"= 26{,}564\ \text{km}", size=54)
        a2.next_to(a1, RIGHT, buff=.25)
        box = SurroundingRectangle(VGroup(a1, a2), color=ACCENT, buff=.18, corner_radius=.08)
        self.beat("Energy gives the semi major axis directly: a equals minus mu over two E. That's twenty six thousand five hundred sixty four kilometers.",
                  [ReplacementTransform(VGroup(e1, e2, e3), e_keep), FadeOut(why)], Write(a1), .1,
                  Write(a2), Create(box),
                  w=(.15, .3, .3, .2))

        # 5. size and period
        s1 = M(r"a \approx 4.16\, R_E", size=44)
        s1.next_to(box, DOWN, buff=.45).align_to(short, LEFT)
        p1 = M(r"T = 2\pi\sqrt{a^3/\mu}", r"= 11.97\ \text{h}", size=44)
        p1.next_to(s1, DOWN, buff=.35).align_to(short, LEFT)
        for m in (s1, p1):
            fit(m, 7.0 - X, 1)
        mol = curve(view, MOL, 0, TAU, INK, width=3, R=1.0, k=0)
        semi = line3(view, tuple(CEN), tuple(APO), INK2, width=3, dashed=True, k=0)
        la = label3(view, "a", tuple((CEN + APO) / 2 + np.array([.5, 0, 0])), INK2, 40)
        self.add(mol, semi)
        with self.say("That's about four Earth radii, and a period of almost exactly twelve hours.") as d:
            self.play(view.scale.animate.set_value(.62), view.elev.animate.set_value(30),
                      FadeIn(s1, shift=UP * .2), run_time=.25 * d)
            self.play(mol.k.animate.set_value(1), run_time=.2 * d)
            self.play(semi.k.animate.set_value(1), FadeIn(la), Indicate(s1, color=INK), run_time=.2 * d)
            self.play(Write(p1[0]), run_time=.15 * d)
            self.play(Write(p1[1]), FadeIn(glow(p1[1], GOLD)), run_time=.15 * d)
            self.wait(.05 * d)
        self.wipe()
