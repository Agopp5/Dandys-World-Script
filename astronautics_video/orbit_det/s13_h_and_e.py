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
# component products of h = r0 x v0 (beat 1) and the two pieces of e (beat 3)
X0, Y0, Z0 = R0
VX, VY, VZ = V0
assert np.isclose(Y0 * VZ, 27012.5, atol=.05) and np.isclose(Z0 * VY, -8419.2, atol=.05)
assert np.isclose(Z0 * VX, 4717.6, atol=.05) and np.isclose(X0 * VZ, -45884.5, atol=.05)
assert np.isclose(X0 * VY, 46161.8, atol=.05) and np.isclose(Y0 * VX, 15227.6, atol=.05)
assert round(27012.5 + 8419.2) == 35432 and round(4717.6 + 45884.5) == 50602 and round(46161.8 - 15227.6) == 30934
assert abs(np.sqrt(35432 ** 2 + 50602 ** 2 + 30934 ** 2) - 69086) < 1
VXH = np.cross(V0, H) / MU
assert np.allclose(VXH, [1.0416, -0.2293, -0.8179], atol=6e-5)
assert abs(r0n - 10609) < 0.5
assert np.allclose(R0 / r0n, [0.8513, -0.5012, -0.1553], atol=6e-5)
assert np.allclose(VXH - R0 / r0n, EV) and np.allclose(EV, [0.1903, 0.2718, -0.6627], atol=6e-5)
assert abs(np.sqrt(0.1903 ** 2 + 0.2718 ** 2 + 0.6627 ** 2) - 0.7411) < 1e-4

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
        # el 25, azim -155 -> -140 (turn in beat 2): the orbit is seen ~60 deg off its normal, so it stays open
        # and the near-Earth pieces (r0, perigee, h) land apart; scale 1.45 fits apogee..globe in the frame height
        view = View(elev=25, azim=-155, scale=1.45, center=(-3.3, -1.75))
        earth = globe(view)
        KH = np.array([0.0, 0.0, 1.0])
        ax = VGroup(arrow3(view, np.zeros(3), 1.7 * np.array([1.0, 0, 0]), INK2),
                    arrow3(view, np.zeros(3), 1.7 * np.array([0, 1.0, 0]), INK2),
                    arrow3(view, np.zeros(3), 1.7 * KH, INK2),
                    label3(view, r"\hat K", 1.95 * KH - 0.25 * np.array([1.0, 0, 0]), INK2, 32))
        orb = curve(view, lambda t: pos(t), 0, TAU, INK, width=3, R=1.0)
        assert np.isclose(np.linalg.norm(R0D), P_SL / (1 + DE * np.cos(TH0)))   # r0 tip sits on the orbit
        r_arr = arrow3(view, np.zeros(3), R0D, INK)
        v_arr = arrow3(view, R0D, R0D + 1.0 * VDIR, ACCENT)                    # tangent at theta0 = 280 deg
        r_lab = label3(view, r"\vec r_0", R0D + 0.3 * R0D / np.linalg.norm(R0D) - 0.25 * KH, INK, 34)
        v_lab = label3(view, r"\vec v_0", R0D + 1.0 * VDIR - 0.35 * KH, ACCENT, 34)
        h_arr = arrow3(view, np.zeros(3), 2.4 * HH, LILAC)
        h_lab = label3(view, r"\vec h", 2.7 * HH, LILAC, 38)
        TS = np.linspace(0, TAU, 160)
        plane = always_redraw(lambda: Polygon(*[view.p(pos(t)) for t in TS], stroke_width=0,
                                              fill_color=LILAC, fill_opacity=0.12).set_z_index(-1))
        e_arr = arrow3(view, np.zeros(3), 1.0 * PH, ROSE)
        e_lab = label3(view, r"\vec e", 0.8 * PH + 1.2 * np.array([0, 1.0, 0]), ROSE, 38)
        e_ext = line3(view, 1.0 * PH, PERI, ROSE, dashed=True)
        peri = dot3(view, PERI, ROSE)
        peri_lab = label3(view, r"\text{perigee}", PERI - 0.42 * KH, ROSE, 34)

        X = 3.9                                # right-column center (column ~0.8 .. 7.0)
        CW = 6.15                              # column width: every line below is >= size 40 at this width

        # ---- beat 1: h = r x v, then each component worked out (silent holds let the viewer read)
        h1 = E(r"\vec h|=|\vec r_0 \times \vec v_0", size=48).move_to([X, 3.3, 0])
        hv = E(r"\vec h|=|(|35{,}432|,\ |50{,}602|,\ |30{,}934|)", size=40).move_to([X, 2.45, 0])
        comps = [
            (r"h_x = y\,v_z - z\,v_y", r"= (-5316.9)(-5.0805)", r"\quad - (-1647.2)(5.1112)",
             r"= 27{,}012.5 + 8{,}419.2 = 35{,}432"),
            (r"h_y = z\,v_x - x\,v_z", r"= (-1647.2)(-2.8640)", r"\quad - (9031.5)(-5.0805)",
             r"= 4{,}717.6 + 45{,}884.5 = 50{,}602"),
            (r"h_z = x\,v_y - y\,v_x", r"= (9031.5)(5.1112)", r"\quad - (-5316.9)(-2.8640)",
             r"= 46{,}161.8 - 15{,}227.6 = 30{,}934"),
        ]

        def work(lines):
            g = VGroup(*[M(s, size=40) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=.3)
            fit(g, CW, 4.2)
            return g.move_to([X, -0.1, 0])

        self.beat("Next, the angular momentum: h equals r cross v.",
                  [FadeIn(earth), FadeIn(ax), FadeIn(orb)], [FadeIn(r_arr), FadeIn(v_arr), FadeIn(r_lab), FadeIn(v_lab)],
                  Write(h1), [grow(h_arr), FadeIn(h_lab)], FadeIn(hv[0:3]), FadeIn(hv[4]), FadeIn(VGroup(hv[6], hv[8])),
                  w=(.15, .12, .2, .3, .08, .07, .08))
        for k, slot in enumerate((3, 5, 7)):
            wk = work(comps[k])
            self.play(LaggedStart(*[FadeIn(m, shift=.1 * DOWN) for m in wk], lag_ratio=.6), run_time=2.2)
            self.wait(1.2)
            self.snap("h component %d" % (k + 1))
            self.play(TransformFromCopy(wk[3], hv[slot]), FadeOut(wk), run_time=.8)
        hm = VGroup(M(r"h = |\vec h| = \sqrt{h_x^2 + h_y^2 + h_z^2}", size=40),
                    M(r"= \sqrt{35{,}432^2 + 50{,}602^2 + 30{,}934^2}", size=40),
                    M(r"= 69{,}086\ \mathrm{km^2/s}", size=40)).arrange(DOWN, aligned_edge=LEFT, buff=.3)
        fit(hm, CW, 3.0)
        hm.move_to([X, 0.6, 0])
        h3 = M(r"h = |\vec h| = 69{,}086\ \mathrm{km^2/s}", size=40).move_to([X, 1.55, 0])
        hb = VGroup(h1, hv, h3)

        # ---- beat 2: the orbit plane is perpendicular to h
        n2 = note("h is perpendicular to the orbit plane:\nit fixes the plane's tilt")
        n2.move_to([X, -1.9, 0])
        self.beat("h sticks straight out of the orbit plane, so it already pins down the plane's tilt. "
                  "We'll use that in a moment.",
                  [FadeIn(plane), FadeIn(n2), FadeIn(hm[0])], [view.turn(15), FadeIn(hm[1])], FadeIn(hm[2]), .1,
                  [FadeOut(hm[:2]), ReplacementTransform(hm[2], h3), Indicate(h_lab, color=LILAC)],
                  w=(.25, .3, .1, .25))

        # ---- beat 3: e vector, its two pieces first; fold h into one boxed result
        e1 = E(r"\vec e|=|\frac{\vec v_0 \times \vec h}{\mu}|-|\frac{\vec r_0}{r_0}", size=48)
        pa = VGroup(M(r"\frac{\vec v_0 \times \vec h}{\mu}", size=40),
                    M(r"= (1.0416,\ -0.2293,\ -0.8179)", size=40)).arrange(DOWN, aligned_edge=LEFT, buff=.2)
        pb_ = VGroup(M(r"\frac{\vec r_0}{r_0} = \frac{(9031.5,\ -5316.9,\ -1647.2)}{10{,}609}", size=40),
                     M(r"= (0.8513,\ -0.5012,\ -0.1553)", size=40)).arrange(DOWN, aligned_edge=LEFT, buff=.2)
        e2 = E(r"\vec e|=|(0.1903,\ 0.2718,\ -0.6627)", size=40)
        en = note("difference of the two pieces")
        eb = VGroup(e1, pa, pb_, VGroup(e2, en).arrange(DOWN, buff=.15)).arrange(DOWN, buff=.32)
        fit(eb, CW, 7.4)
        eb.move_to([X, 0, 0])
        self.beat("Now the eccentricity vector, from the last chapter: v cross h over mu, minus the unit vector along r.",
                  [FadeOut(n2), FadeOut(hb)], Write(e1), FadeIn(pa), FadeIn(pb_),
                  [FadeIn(e2), FadeIn(en), grow(e_arr), FadeIn(e_lab)],
                  w=(.12, .2, .2, .2, .28))
        self.wait(2.5)
        self.snap("e pieces")
        e2_top = e2.copy().move_to([X, 3.2, 0])
        self.play(FadeOut(e1), FadeOut(pa), FadeOut(pb_), FadeOut(en), e2.animate.move_to(e2_top), run_time=1.0)

        # ---- beat 4: e = |e| = sqrt(...) = 0.7411, points to perigee
        e3 = VGroup(M(r"e = |\vec e|", size=40),
                    M(r"= \sqrt{0.1903^2 + 0.2718^2 + 0.6627^2}", size=40),
                    M(r"= 0.7411", size=44)).arrange(DOWN, aligned_edge=LEFT, buff=.3)
        paint(e3[0], {0: ROSE})
        fit(e3, CW, 3.0)
        e3.next_to(e2, DOWN, buff=.45).set_x(X)
        eglow = glow(e3[2], ROSE)
        n4 = note("points from the focus to the perigee")
        n4.next_to(e3, DOWN, buff=.35)
        self.beat("Its length is the eccentricity: zero point seven four one one. "
                  "And it points from the focus straight to the perigee.",
                  FadeIn(e3[0]), FadeIn(e3[1]), [Write(e3[2]), FadeIn(eglow)],
                  [Create(e_ext), FadeIn(peri), FadeIn(peri_lab), FadeIn(n4)],
                  Indicate(peri, color=ROSE),
                  w=(.12, .18, .2, .3, .2))

        # ---- beat 5: second route, sqrt(1 + 2 E h^2 / mu^2)
        c1 = M(r"e = \sqrt{1 + \frac{2\,\mathcal{E}\,h^2}{\mu^2}}", size=46)
        c2 = M(r"= \sqrt{1 + \frac{2(-7.5027)(69{,}086)^2}{(398{,}600)^2}}", size=40)
        c3 = M(r"= 0.7411", size=46, color=GOOD)
        tick = T("agrees", size=30, color=GOOD)
        cb = VGroup(c1, c2, VGroup(c3, tick).arrange(RIGHT, buff=.35)).arrange(DOWN, buff=.35)
        fit(cb, 5.8, 4.2)
        ebox = panel(E(r"e| = 0.7411", size=40, cmap={"e": ROSE}), color=ROSE)
        ebox.move_to([X, 3.0, 0])
        cb.next_to(ebox, DOWN, buff=.5).set_x(X)
        n5 = note("from energy and h alone")
        n5.next_to(cb, DOWN, buff=.3)
        self.beat("Your notes give a second way to get the same number, from energy and h alone: "
                  "e equals the square root of one plus two E h squared over mu squared. It agrees.",
                  [FadeOut(e2), FadeOut(e3[:2]), FadeOut(n4), FadeOut(eglow), ReplacementTransform(e3[2], ebox)],
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
        fit(pb, 5.8, 4.6)
        pb.next_to(ebox, DOWN, buff=.5).set_x(X)
        apo = dot3(view, pos(PI), INK2)
        apo_lab = label3(view, r"\text{apogee}", pos(PI) + 0.4 * KH, INK2, 34)
        self.beat("So the perigee radius is about six thousand eight hundred seventy seven kilometers, "
                  "just five hundred kilometers up, and the apogee is about forty six thousand two hundred "
                  "fifty kilometers away.",
                  [FadeOut(cb), FadeOut(n5), FadeIn(a_ln)], [Write(p1), Indicate(peri, color=ROSE)], FadeIn(p1n),
                  [Write(p2), FadeIn(apo), FadeIn(apo_lab)], FadeIn(p2n), .1,
                  w=(.1, .25, .12, .3, .13))
        self.wipe()
