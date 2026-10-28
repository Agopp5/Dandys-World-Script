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

# beat 1 substitution (e components shown to 4 places, products from the exact e-vector)
assert np.allclose(np.round(EV, 4), [0.1903, 0.2718, -0.6627])
PROD = EV * R0
assert np.allclose(np.round(PROD, 1), [1718.9, -1445.3, 1091.5])
assert np.isclose(round(EV @ R0, 1), 1365.2)
assert np.isclose(round(np.linalg.norm(R0)), 10609)
assert np.isclose(round(ECC * np.linalg.norm(R0), 1), 7862.3)
assert np.isclose(round(1365.2 / 7862.3, 4), 0.1736)
# beat 4 substitution
assert np.allclose(np.round(R0 * V0), [-25866, -27176, 8369]) and -25866 - 27176 + 8369 == -44673

# ---------------- drawn geometry (not to scale: a = 3.0, e = 0.6) ----------------
DA, DE = 3.0, 0.6
DP = DA * (1 - DE ** 2)


def rad(th):
    return DP / (1 + DE * np.cos(th))


S2 = 1.0                                  # 2D plane: scene units per Earth radius
F2 = np.array([-1.7, -0.3, 0])            # focus (Earth) in the 2D view
CX = 3.95                                 # right column center (x from 1.0 to 6.9)


def p2(th, r=None):
    r = rad(th) if r is None else r
    return F2 + S2 * r * np.array([np.cos(th), np.sin(th), 0])


def vdir(th):
    v = np.array([-np.sin(th), DE + np.cos(th), 0])
    return v / np.linalg.norm(v)


def note(s, m, side=RIGHT):
    return T(s, 28, MUTED).next_to(m, side, buff=.35)


class S17_theta0(VScene):
    budget = 101

    def construct(self):
        self.section("Step six: where is the satellite?")

        # ---- beat 1: pure algebra, full width ----
        f0 = E(r"\cos|\theta_0|=|\frac{\vec e\cdot\vec r_0}{e\,r_0}", size=48).move_to([0, 2.45, 0])
        l1 = E(r"\vec e\cdot\vec r_0|=|0.1903(9031.5)+0.2718(-5316.9)+(-0.6627)(-1647.2)", size=40)
        l1.move_to([0, 1.0, 0])
        l2 = E(r"=|1{,}718.9-1{,}445.3+1{,}091.5|=|1{,}365.2", size=40)
        l2.next_to(l1, DOWN, buff=.45).align_to(l1[1], LEFT)
        n2 = note("multiply, then add", l2)
        l3 = E(r"e\,r_0|=|0.7411\times 10{,}609|=|7{,}862.3", size=40)
        l3.next_to(l2, DOWN, buff=.85).align_to(l1, LEFT)
        n3 = note("the two lengths", l3)
        l4 = E(r"\cos|\theta_0|=|\frac{1{,}365.2}{7{,}862.3}|=|0.1736", size=44)
        l4.next_to(l3, DOWN, buff=.75).align_to(l1, LEFT)
        n4 = note("divide", l4)
        self.beat("Last, the true anomaly. Its cosine is e dot r over e times r, which comes out to zero point one seven three six.",
                  Write(f0), Write(l1), [Write(l2), FadeIn(n2)], [Write(l3), FadeIn(n3)],
                  [Write(l4), FadeIn(n4)], Indicate(l4[5], color=GOLD),
                  w=(.17, .2, .17, .17, .17, .12))

        # ---- beat 2: fold to one boxed line; orbit plane with two candidates ----
        cb = E(r"\cos|\theta_0|=|0.1736", size=44).move_to([CX, 2.55, 0])
        cbox = SurroundingRectangle(cb, color=GOLD, buff=.18)
        earth2 = Circle(radius=0.45, color=SKY, fill_color=SKY, fill_opacity=.35, stroke_width=2).move_to(F2)
        ell = ParametricFunction(lambda t: p2(t), t_range=[0, TAU], color=INK, stroke_width=4)
        e2 = Arrow(F2, F2 + RIGHT * 2.1, buff=0, color=ROSE, stroke_width=5)
        e2l = M(r"\vec e", size=40, color=ROSE).next_to(e2.get_end(), UR, buff=.08)
        peri = Dot(p2(0), color=ROSE)
        peril = T("perigee", 28, ROSE).next_to(peri, DR, buff=.1)
        plane = VGroup(ell, earth2, e2, e2l, peri, peril)

        ta, tb = np.radians(80), np.radians(-80)
        da, db = Dot(p2(ta), color=INK, radius=.1), Dot(p2(tb), color=INK, radius=.1)
        la, lb = DashedLine(F2, p2(ta), color=INK2), DashedLine(F2, p2(tb), color=INK2)
        aa = Arc(radius=1.0, start_angle=0, angle=ta, arc_center=F2, color=GOLD, stroke_width=5)
        ab = Arc(radius=1.0, start_angle=0, angle=tb, arc_center=F2, color=GOLD, stroke_width=5)
        ta_l = TX(r"$80^\circ$ past perigee", size=30).next_to(da, LEFT, buff=.15)
        tb_l = TX(r"$80^\circ$ before perigee", size=30).next_to(db, LEFT, buff=.15)
        candA = VGroup(la, aa, da, ta_l)
        candB = VGroup(lb, ab, db, tb_l)

        eq2 = E(r"\arccos(0.1736)|=|80^\circ", size=44).move_to([CX, 1.2, 0])
        self.beat("Arc cosine says eighty degrees. But the satellite could be eighty degrees past perigee, or eighty degrees before it.",
                  [FadeOut(f0), FadeOut(l1), FadeOut(l2), FadeOut(l3), FadeOut(n2), FadeOut(n3), FadeOut(n4),
                   *morph(l4, cb, [(0, 0), (1, 1), (2, 2), (5, 3)]), Create(cbox)],
                  [FadeIn(plane), Write(eq2)],
                  [Create(la), Create(aa), FadeIn(da), FadeIn(ta_l)],
                  [Create(lb), Create(ab), FadeIn(db), FadeIn(tb_l)],
                  w=(.2, .25, .27, .28))

        self.beat("Which one is it?")
        self.checkpoint("4.3", "80 or 280? Then theta zero for your practice orbit")

        # ---- beat 4: r.v decides ----
        x0 = 1.15
        r1 = E(r"\vec r_0\cdot\vec v_0|=|9031.5(-2.8640)", size=40)
        r1.move_to([0, 1.45, 0]).align_to([x0, 0, 0], LEFT)
        r2 = E(r"+(-5316.9)(5.1112)", size=40).next_to(r1, DOWN, buff=.35).align_to(r1[2], LEFT)
        r3 = E(r"+(-1647.2)(-5.0805)", size=40).next_to(r2, DOWN, buff=.35).align_to(r1[2], LEFT)
        r4 = E(r"=|-25{,}866-27{,}176+8{,}369", size=40).next_to(r3, DOWN, buff=.45).align_to(r1, LEFT)
        r5 = E(r"=|-44{,}673\ \mathrm{km^2/s}|<0", size=40).next_to(r4, DOWN, buff=.45).align_to(r1, LEFT)
        rf = E(r"\vec r_0\cdot\vec v_0|=|-44{,}673\ \mathrm{km^2/s}|<0", size=40).move_to([CX, 1.2, 0])
        nt = VGroup(T("distance shrinking:", 30, MUTED), T("heading to perigee", 30, MUTED)).arrange(DOWN, buff=.12)
        nt.next_to(rf, DOWN, buff=.3)
        va = Arrow(p2(ta), p2(ta) + 1.0 * vdir(ta), buff=0, color=ACCENT, stroke_width=5)
        vb = Arrow(p2(tb), p2(tb) + 1.0 * vdir(tb), buff=0, color=ACCENT, stroke_width=5)
        vbl = M(r"\vec v_0", size=40, color=ACCENT).next_to(vb.get_end(), RIGHT, buff=.1)
        rb = Arrow(F2, p2(tb), buff=0, color=INK, stroke_width=5)
        a280 = Arc(radius=.7, start_angle=0, angle=np.radians(280), arc_center=F2, color=GOLD, stroke_width=6)
        a280l = M(r"\theta_0", size=40, color=GOLD).move_to(F2 + 1.1 * np.array([np.cos(np.radians(150)), np.sin(np.radians(150)), 0]))
        eq4 = E(r"\theta_0|=|360^\circ-80^\circ|=|280^\circ", size=48).move_to([CX, -1.6, 0])
        for m in (va, vb, vbl, rb, a280, a280l):
            m.set_z_index(2)
        steps = [[FadeOut(eq2), Write(r1)], [Write(r2)], [Write(r3)], [Write(r4)], [Write(r5)], "snap",
                 [FadeOut(r1), FadeOut(r2), FadeOut(r3), FadeOut(r4), *morph(r5, rf, [(0, 1), (1, 2), (2, 3)])],
                 [FadeIn(nt), GrowArrow(va), GrowArrow(vb), FadeIn(vbl)],
                 [candA.animate.set_opacity(.2), va.animate.set_opacity(.2), FadeOut(ab), FadeOut(lb), GrowArrow(rb),
                  Indicate(db, color=GOLD)],
                 [Write(eq4), Create(a280), FadeIn(a280l), db.animate.set_color(GOLD)],
                 [FadeIn(glow(eq4[4], GOLD))]]
        fr = iter((.08, .06, .06, .07, .07, .1, .12, .14, .22, .08))
        with self.say("Check r dot v. It's minus forty four thousand six hundred seventy three. Negative means the distance is shrinking: the satellite is falling toward perigee. So theta zero is three sixty minus eighty: two hundred eighty degrees.") as d:
            for st in steps:
                if st == "snap":
                    self.snap("r dot v worked out")
                    continue
                self.play(*st, run_time=next(fr) * d)
        self.wipe()

        # ---- beat 5: all six ----
        hd = T("Six elements from one measurement", 44).move_to([0, 2.85, 0])
        labs = [T("energy", 36, INK2), E(r"\vec h|,\ |\vec e", size=44), E(r"C_{PN}", size=44),
                E(r"\vec e\cdot\vec r_0|,\ |\vec r_0\cdot\vec v_0", size=40)]
        vals = [E(r"a|=|26{,}564\ \mathrm{km}", size=48), E(r"e|=|0.7411", size=48),
                E(r"i|=|63.4^\circ|,\quad|\Omega|=|145.0^\circ|,\quad|\omega|=|270^\circ", size=48),
                E(r"\theta_0|=|280^\circ", size=48)]
        rows = VGroup()
        for k, (lab, val) in enumerate(zip(labs, vals)):
            y = 1.55 - 1.3 * k
            lab.move_to([0, y, 0]).align_to([-2.3, 0, 0], RIGHT)
            ar = Arrow([-2.15, y, 0], [-1.15, y, 0], buff=0, color=MUTED, stroke_width=4)
            val.move_to([0, y, 0]).align_to([-0.95, 0, 0], LEFT)
            rows.add(VGroup(lab, ar, val))
        self.beat("And that's all six: a, e, i, capital Omega, little omega, and theta zero, from one measurement.",
                  FadeIn(hd), LaggedStart(*[FadeIn(r, shift=.2 * RIGHT) for r in rows], lag_ratio=.35),
                  .15, w=(.15, .7))
        self.wipe()
