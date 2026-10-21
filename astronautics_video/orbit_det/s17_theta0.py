"""S17: step six, the true anomaly theta0 (BRIEF.md S17)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# ---------------- facts (Kluever Example 3.1) ----------------
MU = 3.986e5
R0 = np.array([9031.5, -5316.9, -1647.2])
V0 = np.array([-2.8640, 5.1112, -5.0805])
H = np.cross(R0, V0)
EV = np.cross(V0, H) / MU - R0 / np.linalg.norm(R0)
ECC = np.linalg.norm(EV)
assert np.isclose(ECC, 0.7411, atol=1e-4)
COS_TH = EV @ R0 / (ECC * np.linalg.norm(R0))
assert np.isclose(COS_TH, 0.1736, atol=5e-5)
TH_ACOS = np.degrees(np.arccos(COS_TH))
assert abs(TH_ACOS - 80) < 0.05
RV = R0 @ V0
assert abs(RV - (-44673)) < 1 and RV < 0
TH0 = 360 - TH_ACOS
assert abs(TH0 - 280) < 0.05
EN = V0 @ V0 / 2 - MU / np.linalg.norm(R0)
A_KM = -MU / (2 * EN)
assert abs(A_KM - 26564) < 1
HH, PH = H / np.linalg.norm(H), EV / ECC
QH = np.cross(HH, PH)
CPN_N = np.array([PH, QH, HH])
INC = np.degrees(np.arccos(CPN_N[2, 2]))
OMG = np.degrees(np.arctan2(CPN_N[2, 0], -CPN_N[2, 1]))
ARGP = np.degrees(np.arctan2(CPN_N[0, 2], CPN_N[1, 2])) % 360
assert abs(INC - 63.4) < 0.05 and abs(OMG - 145.0) < 0.05 and abs(ARGP - 270) < 0.05
# in the perifocal frame r.v = (mu/h) e r sin(theta): negative exactly on the inbound half (180..360 deg)
assert np.sin(np.radians(280)) < 0 < np.sin(np.radians(80))

# ---------------- drawn geometry (not to scale: a = 3.0, e = 0.6) ----------------
DA, DE = 3.0, 0.6
DP = DA * (1 - DE ** 2)
ANG = np.radians([145.0, 63.43, 270.0])


def rad(th):
    return DP / (1 + DE * np.cos(th))


S2 = 1.15                                 # 2D plane: scene units per Earth radius
F2 = np.array([-1.0, -0.4, 0])           # focus (Earth) in the 2D view


def p2(th, r=None):
    r = rad(th) if r is None else r
    return F2 + S2 * r * np.array([np.cos(th), np.sin(th), 0])


def vdir(th):
    v = np.array([-np.sin(th), DE + np.cos(th), 0])
    return v / np.linalg.norm(v)


def col(m, y, w=4.7):
    fit(m, w, 1.3)
    m.move_to([4.55, y, 0])
    return m


class S17_theta0(VScene):
    budget = 101

    def construct(self):
        self.section("Step six: where is the satellite?")

        # ---- 3D: e and r0 ----
        view = View(elev=40, azim=30, scale=0.85, center=(-3.4, -1.5))
        f = orbit(DA, DE, *ANG)
        C = cpn(*ANG)
        ph, hh = C[0], C[2]
        o = np.zeros(3)
        pos = f(np.radians(280))
        earth = globe(view)
        orb = curve(view, f, 0, TAU, INK, R=1.0)
        e_arr = arrow3(view, o, 2.1 * ph, ROSE)
        e_lab = label3(view, r"\vec e", 2.35 * ph, ROSE, 40)
        r_arr = arrow3(view, o, pos, INK)
        r_lab = label3(view, r"\vec r_0", 1.45 * pos, INK, 40)
        ang = arc3(view, -hh, ph, np.radians(80), 1.35, GOLD)
        g3 = Group(earth, orb, e_arr, e_lab, r_arr, r_lab, ang)

        eq1 = col(E(r"\cos|\theta_0|=|\frac{\vec e\cdot\vec r_0}{e\,r_0}|=|0.1736", size=44), 1.9)
        self.beat("Last, the true anomaly. Its cosine is e dot r over e times r, which comes out to zero point one seven three six.",
                  [FadeIn(earth), grow(orb)], [grow(e_arr), FadeIn(e_lab), grow(r_arr), FadeIn(r_lab)],
                  Write(eq1[:4]), [Write(eq1[4:]), grow(ang)],
                  w=(.2, .2, .35, .25))

        # ---- 2D orbit plane: two candidates ----
        earth2 = Circle(radius=0.5, color=SKY, fill_color=SKY, fill_opacity=.35, stroke_width=2).move_to(F2)
        ell = ParametricFunction(lambda t: p2(t), t_range=[0, TAU], color=INK, stroke_width=4)
        e2 = Arrow(F2, F2 + RIGHT * 2.3, buff=0, color=ROSE, stroke_width=5)
        e2l = M(r"\vec e", size=40, color=ROSE).next_to(e2.get_end(), UR, buff=.08)
        peri = Dot(p2(0), color=ROSE)
        peril = T("perigee", 26, ROSE).next_to(peri, DR, buff=.1)
        plane = VGroup(ell, earth2, e2, e2l, peri, peril)

        ta, tb = np.radians(80), np.radians(-80)
        da, db = Dot(p2(ta), color=INK, radius=.1), Dot(p2(tb), color=INK, radius=.1)
        la, lb = DashedLine(F2, p2(ta), color=INK2), DashedLine(F2, p2(tb), color=INK2)
        aa = Arc(radius=1.15, start_angle=0, angle=ta, arc_center=F2, color=GOLD, stroke_width=5)
        ab = Arc(radius=1.15, start_angle=0, angle=tb, arc_center=F2, color=GOLD, stroke_width=5)
        ta_l = TX(r"$80^\circ$ past perigee", size=30).next_to(da, LEFT, buff=.15)
        tb_l = TX(r"$80^\circ$ before perigee", size=30).next_to(db, LEFT, buff=.15)
        candA = VGroup(la, aa, da, ta_l)
        candB = VGroup(lb, ab, db, tb_l)

        eq2 = col(E(r"\arccos(0.1736)|=|80^\circ", size=44), 0.75)
        self.beat("Arc cosine says eighty degrees. But the satellite could be eighty degrees past perigee, or eighty degrees before it.",
                  Write(eq2), [FadeOut(g3), FadeIn(plane)],
                  [Create(la), Create(aa), FadeIn(da), FadeIn(ta_l)],
                  [Create(lb), Create(ab), FadeIn(db), FadeIn(tb_l)],
                  w=(.25, .2, .27, .28))

        self.predict("80 degrees or 280 degrees? What could tell you?", "Which one is it?")

        # ---- r.v decides ----
        eq3 = col(E(r"\vec r_0\cdot\vec v_0|=|-44{,}673\ \mathrm{km^2/s}|<0", size=40), -0.45)
        note = T("distance shrinking: heading to perigee", 26, MUTED)
        fit(note, 4.7, .6).next_to(eq3, DOWN, buff=.2)
        va = Arrow(p2(ta), p2(ta) + 1.1 * vdir(ta), buff=0, color=ACCENT, stroke_width=5)
        vb = Arrow(p2(tb), p2(tb) + 1.1 * vdir(tb), buff=0, color=ACCENT, stroke_width=5)
        vbl = M(r"\vec v_0", size=40, color=ACCENT).next_to(vb.get_end(), RIGHT, buff=.1)
        rb = Arrow(F2, p2(tb), buff=0, color=INK, stroke_width=5)
        a280 = Arc(radius=.8, start_angle=0, angle=np.radians(280), arc_center=F2, color=GOLD, stroke_width=6)
        a280l = M(r"\theta_0", size=40, color=GOLD).move_to(F2 + 1.2 * np.array([np.cos(np.radians(150)), np.sin(np.radians(150)), 0]))
        eq4 = col(E(r"\theta_0|=|360^\circ-80^\circ|=|280^\circ", size=44), -2.3)
        for m in (va, vb, vbl, rb, a280, a280l):
            m.set_z_index(2)
        self.beat("Check r dot v. It's minus forty four thousand six hundred seventy three. Negative means the distance is shrinking: the satellite is falling toward perigee. So theta zero is three sixty minus eighty: two hundred eighty degrees.",
                  Write(eq3), [FadeIn(note), GrowArrow(va), GrowArrow(vb), FadeIn(vbl)],
                  [candA.animate.set_opacity(.2), va.animate.set_opacity(.2), FadeOut(ab), FadeOut(lb), GrowArrow(rb),
                   Indicate(db, color=GOLD)],
                  [Write(eq4), Create(a280), FadeIn(a280l), db.animate.set_color(GOLD)],
                  FadeIn(glow(eq4[4], GOLD)),
                  w=(.25, .17, .2, .28, .1))
        self.wipe()

        # ---- all six ----
        sh = sheet(T("Six elements from one measurement", 40), [
            ("energy", INK2, [E(r"a|=|26{,}564\ \mathrm{km}", size=50)]),
            ("h, e vector", ROSE, [E(r"e|=|0.7411", size=50)]),
            ("matrix C PN", ACCENT, [E(r"i|=|63.4^\circ|,\quad|\Omega|=|145.0^\circ|,\quad|\omega|=|270^\circ", size=50)]),
            ("dot products", GOLD, [E(r"\theta_0|=|280^\circ", size=50)]),
        ])
        self.beat("And that's all six: a, e, i, capital Omega, little omega, and theta zero, from one measurement.",
                  FadeIn(sh.head), LaggedStart(*[FadeIn(r, shift=.2 * RIGHT) for r in sh.rows], lag_ratio=.35),
                  .15, w=(.15, .7))
        self.wipe()
