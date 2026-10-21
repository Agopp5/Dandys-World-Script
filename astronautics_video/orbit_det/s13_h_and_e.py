"""S13: step two, angular momentum and eccentricity (BRIEF.md S13)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# ---- facts (Kluever Example 3.1) -------------------------------------------------------------
MU = 3.986e5
R0 = np.array([9031.5, -5316.9, -1647.2])
V0 = np.array([-2.8640, 5.1112, -5.0805])
r0n = np.linalg.norm(R0)
EN = V0 @ V0 / 2 - MU / r0n
A = -MU / (2 * EN)
H = np.cross(R0, V0)
HN = np.linalg.norm(H)
EV = np.cross(V0, H) / MU - R0 / r0n
EC = np.linalg.norm(EV)
E_CHECK = np.sqrt(1 + 2 * EN * HN ** 2 / MU ** 2)
RP, RA = A * (1 - EC), A * (1 + EC)
assert np.allclose(H, [35432, 50602, 30934], atol=1)
assert abs(HN - 69086) < 1
assert np.allclose(EV, [0.1903, 0.2718, -0.6627], atol=6e-5)
assert abs(EC - 0.7411) < 5e-5 and abs(E_CHECK - 0.7411) < 5e-5
assert abs(EN - (-7.5027)) < 1e-4
assert abs(RP - 6877) < 1 and abs(RA - 46250) < 1
assert abs((RP - 6378.137) - 500) < 1         # "just five hundred kilometers up"

# ---- drawn Molniya (not to scale: a = 3.0, e = 0.6), true orientation -----------------------
DA, DE = 3.0, 0.6
OM, INC, W = np.radians(145.0), np.radians(63.4), np.radians(270.0)
CM = cpn(OM, INC, W)
PH, QH, HH = CM[0], CM[1], CM[2]
assert np.allclose(PH, EV / EC, atol=2e-3) and np.allclose(HH, H / HN, atol=2e-3)
TH0 = np.radians(280.0)
P_SL = DA * (1 - DE ** 2)


def eci(xp, yp):
    return xp * PH + yp * QH


def pos(th):
    rr = P_SL / (1 + DE * np.cos(th))
    return eci(rr * np.cos(th), rr * np.sin(th))


VDIR = eci(-np.sin(TH0), DE + np.cos(TH0))
VDIR = VDIR / np.linalg.norm(VDIR)
R0D = pos(TH0)
PERI = pos(0.0)                               # a(1-e) = 1.2 along p-hat
assert np.isclose(np.linalg.norm(PERI), DA * (1 - DE))


def note(s):
    return T(s, size=26, color=MUTED)


class S13_h_and_e(VScene):
    budget = 135

    def construct(self):
        view = View(elev=18, azim=-40, scale=0.72, center=(-3.4, -1.3))
        earth = globe(view)
        ax = axes3(view, 1.8)
        orb = curve(view, lambda t: pos(t), 0, TAU, INK, width=3, R=1.0)
        r_arr = arrow3(view, ORIGIN * 0, R0D, INK)
        v_arr = arrow3(view, R0D, R0D + 1.1 * VDIR, ACCENT)
        r_lab = label3(view, r"\vec r_0", R0D * 1.12 + 0.25 * QH, INK, 34)
        v_lab = label3(view, r"\vec v_0", R0D + 1.25 * VDIR, ACCENT, 34)
        h_arr = arrow3(view, np.zeros(3), 2.6 * HH, LILAC)
        h_lab = label3(view, r"\vec h", 2.85 * HH, LILAC, 38)
        plane = disc3(view, PH, QH, 3.2, LILAC, 0.16)
        e_arr = arrow3(view, np.zeros(3), 1.0 * PH, ROSE)
        e_lab = label3(view, r"\vec e", 0.75 * PH + 0.35 * QH, ROSE, 38)
        e_ext = line3(view, 1.0 * PH, PERI, ROSE, dashed=True)
        peri = dot3(view, PERI, ROSE)
        peri_lab = label3(view, r"\text{perigee}", PERI + 0.55 * QH - 0.2 * PH, ROSE, 30)

        X = 3.75                               # right-column center
        # ---- beat 1: h = r x v
        h1 = E(r"\vec h|=|\vec r_0 \times \vec v_0", size=48)
        h2 = M(r"= (35{,}432,\ 50{,}602,\ 30{,}934)", size=40)
        h2u = M(r"\mathrm{km^2/s}", size=40, color=INK2)
        h3 = E(r"|\vec h|| = 69{,}086\ \mathrm{km^2/s}", size=44)
        paint(h3, {0: LILAC})
        hb = VGroup(h1, h2, h2u, h3).arrange(DOWN, buff=.32)
        fit(hb, 6.0, 4.0)
        hb.move_to([X, 1.6, 0])
        self.beat("Next, the angular momentum: h equals r cross v.",
                  [FadeIn(earth), FadeIn(ax), FadeIn(orb)], [FadeIn(r_arr), FadeIn(v_arr), FadeIn(r_lab), FadeIn(v_lab)],
                  Write(h1), FadeIn(h2), FadeIn(h2u),
                  [grow(h_arr), FadeIn(h_lab)], Write(h3),
                  w=(.12, .1, .14, .14, .06, .26, .18))

        # ---- beat 2: the orbit plane is perpendicular to h
        n2 = note("h is perpendicular to the orbit plane:\nit fixes the plane's tilt")
        n2.next_to(hb, DOWN, buff=.45)
        self.beat("h sticks straight out of the orbit plane, so it already pins down the plane's tilt. "
                  "We'll use that in a moment.",
                  [FadeIn(plane), FadeIn(n2)], Indicate(h_lab, color=LILAC), view.turn(25), .1,
                  w=(.3, .2, .4))

        # ---- beat 3: e vector; fold h into one boxed result
        hbox_eq = E(r"\vec h| = (35{,}432,\ 50{,}602,\ 30{,}934)", size=40)
        hbox = panel(hbox_eq, color=LILAC)
        hbox.move_to([X, 3.0, 0])
        e1 = E(r"\vec e|=|\frac{\vec v_0 \times \vec h}{\mu}|-|\frac{\vec r_0}{r_0}", size=48)
        e2 = M(r"= (0.1903,\ 0.2718,\ -0.6627)", size=42)
        eb = VGroup(e1, e2).arrange(DOWN, buff=.35)
        fit(eb, 6.0, 3.0)
        eb.next_to(hbox, DOWN, buff=.5)
        eb.set_x(X)
        self.beat("Now the eccentricity vector, from the last chapter: v cross h over mu, minus the unit vector along r.",
                  [FadeOut(n2), ReplacementTransform(hb, hbox)], Write(e1), FadeIn(e2),
                  [grow(e_arr), FadeIn(e_lab)],
                  w=(.2, .35, .2, .25))

        # ---- beat 4: |e| = 0.7411, points to perigee
        e3 = E(r"e|=|\,|\vec e|\,|=|0.7411", size=48)
        paint(e3, {2: ROSE})
        e3.next_to(eb, DOWN, buff=.45).set_x(X)
        n4 = note("points from the focus to the perigee")
        n4.next_to(e3, DOWN, buff=.3)
        self.beat("Its length is the eccentricity: zero point seven four one one. "
                  "And it points from the focus straight to the perigee.",
                  Write(e3), FadeIn(glow(e3[4], ROSE)), [Create(e_ext), FadeIn(peri), FadeIn(peri_lab), FadeIn(n4)],
                  Indicate(peri, color=ROSE),
                  w=(.25, .15, .35, .25))

        # ---- beat 5: second route, sqrt(1 + 2 E h^2 / mu^2)
        c1 = M(r"e = \sqrt{1 + \frac{2\,\mathcal{E}\,h^2}{\mu^2}}", size=46)
        c2 = M(r"= \sqrt{1 + \frac{2(-7.5027)(69{,}086)^2}{(398{,}600)^2}}", size=40)
        c3 = M(r"= 0.7411", size=46, color=GOOD)
        tick = T("agrees", size=30, color=GOOD)
        cb = VGroup(c1, c2, VGroup(c3, tick).arrange(RIGHT, buff=.35)).arrange(DOWN, buff=.35)
        fit(cb, 6.0, 4.2)
        ebox = panel(E(r"e| = 0.7411", size=40, cmap={"e": ROSE}), color=ROSE)
        ebox.move_to([X, 3.0, 0])
        cb.next_to(ebox, DOWN, buff=.5).set_x(X)
        n5 = note("from energy and h alone")
        n5.next_to(cb, DOWN, buff=.3)
        self.beat("Your notes give a second way to get the same number, from energy and h alone: "
                  "e equals the square root of one plus two E h squared over mu squared. It agrees.",
                  [FadeOut(hbox), FadeOut(eb), FadeOut(n4), ReplacementTransform(e3, ebox)],
                  [Write(c1), FadeIn(n5)], FadeIn(c2), [FadeIn(c3), FadeIn(tick)], Circumscribe(c3, color=GOOD),
                  w=(.15, .3, .25, .15, .15))

        # ---- beat 6: perigee and apogee radii
        a_ln = M(r"a = 26{,}563.6\ \mathrm{km}", size=40, color=INK2)
        p1 = M(r"r_p = a(1-e) = 6{,}877\ \mathrm{km}", size=44)
        p1n = note("about 500 km above the surface")
        p2 = M(r"r_a = a(1+e) = 46{,}250\ \mathrm{km}", size=44)
        p2n = note("about 39,870 km up")
        pb = VGroup(a_ln, p1, p1n, p2, p2n).arrange(DOWN, buff=.3)
        pb[2].shift(UP * .1)
        pb[4].shift(UP * .1)
        fit(pb, 6.0, 4.6)
        pb.next_to(ebox, DOWN, buff=.5).set_x(X)
        apo = dot3(view, pos(PI), INK2)
        apo_lab = label3(view, r"\text{apogee}", pos(PI) + 0.45 * QH, INK2, 30)
        self.beat("So the perigee radius is about six thousand eight hundred seventy seven kilometers, "
                  "just five hundred kilometers up, and the apogee is about forty six thousand two hundred "
                  "fifty kilometers away.",
                  [FadeOut(cb), FadeOut(n5), FadeIn(a_ln)], [Write(p1), Indicate(peri, color=ROSE)], FadeIn(p1n),
                  [Write(p2), FadeIn(apo), FadeIn(apo_lab)], FadeIn(p2n), .1,
                  w=(.1, .25, .12, .3, .13))
        self.wipe()
