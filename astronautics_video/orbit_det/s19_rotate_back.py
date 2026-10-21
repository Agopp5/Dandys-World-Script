"""S19: step two, rotate the perifocal r and v back into ECI (BRIEF.md S19)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# ---- facts: Kluever Example 3.1, rebuilt from the measured state vector ----
MU = 3.986e5
R0 = np.array([9031.5, -5316.9, -1647.2])
V0 = np.array([-2.8640, 5.1112, -5.0805])
HV = np.cross(R0, V0)
H = np.linalg.norm(HV)
EV = np.cross(V0, HV) / MU - R0 / np.linalg.norm(R0)
ECC = np.linalg.norm(EV)
EN = V0 @ V0 / 2 - MU / np.linalg.norm(R0)
A_KM = -MU / (2 * EN)
PH, HH = EV / ECC, HV / H
QH = np.cross(HH, PH)
CPN = np.array([PH, QH, HH])
TH0 = 2 * np.pi - np.arccos(EV @ R0 / (ECC * np.linalg.norm(R0)))     # r0.v0 < 0: heading to perigee
assert R0 @ V0 < 0 and np.isclose(np.degrees(TH0), 280, atol=0.1)
assert np.isclose(round(A_KM), 26564) and np.isclose(ECC, 0.7411, atol=1e-4)
I_DEG = np.degrees(np.arccos(CPN[2, 2]))
OM_DEG = np.degrees(np.arctan2(CPN[2, 0], -CPN[2, 1]))
W_DEG = np.degrees(np.arctan2(CPN[0, 2], CPN[1, 2])) % 360
assert np.isclose(I_DEG, 63.4, atol=.05) and np.isclose(OM_DEG, 145.0, atol=.05) and np.isclose(W_DEG, 270, atol=.05)
P_KM = A_KM * (1 - ECC ** 2)
R_KM = P_KM / (1 + ECC * np.cos(TH0))
RP = np.array([R_KM * np.cos(TH0), R_KM * np.sin(TH0), 0])
VP = MU / H * np.array([-np.sin(TH0), ECC + np.cos(TH0), 0])
assert np.allclose(RP, [1842, -10448, 0], atol=1.0)
assert np.allclose(VP, [5.682, 5.278, 0], atol=1e-3)
RN, VN = CPN.T @ RP, CPN.T @ VP
assert np.allclose(RN, [9031, -5317, -1647], atol=1.0)            # shown rounded to the km
assert np.allclose(VN, [-2.864, 5.111, -5.081], atol=1e-3)
assert np.allclose(RN, R0, atol=1e-6) and np.allclose(VN, V0, atol=1e-9)   # the round trip closes
# the transpose really is the inverse (rows orthonormal)
assert np.allclose(CPN.T @ CPN, np.eye(3), atol=1e-9)

# ---- drawn geometry (not to scale): Molniya drawn with a = 3.0, e = 0.6 ----
AD, ED = 3.0, 0.6
PD = AD * (1 - ED ** 2)
OM, INC, W = np.radians(145.0), np.radians(I_DEG), np.radians(270.0)
O3 = np.zeros(3)


def col(m, y=0.0):
    """Right-hand column: x in [0.7, 6.9], shrink only if needed."""
    fit(m, 6.1, 7.3)
    return m.move_to([3.8, y, 0])


def kepler_theta(M, e=ECC):
    """Kepler's equation M = E - e sin E by Newton from E = pi (converges for every M, e < 1)."""
    M = M % TAU
    E_ = np.pi
    for _ in range(30):
        E_ = E_ - (E_ - e * np.sin(E_) - M) / (1 - e * np.cos(E_))
    return 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E_ / 2), np.sqrt(1 - e) * np.cos(E_ / 2))


E0 = 2 * np.arctan2(np.sqrt(1 - ECC) * np.sin(TH0 / 2), np.sqrt(1 + ECC) * np.cos(TH0 / 2))
M0 = (E0 - ECC * np.sin(E0)) % TAU
assert np.isclose(np.cos(kepler_theta(M0)), np.cos(TH0)) and np.isclose(np.sin(kepler_theta(M0)), np.sin(TH0))


class S19_Rotate_Back(VScene):
    budget = 148

    def construct(self):
        view = View(elev=65, azim=25, scale=1.0, center=(-3.6, -1.9))
        s = ValueTracker(0.0)        # 0: perifocal page lying flat, 1: rotated into place
        Mt = ValueTracker(M0)        # mean anomaly drives the satellite

        def Cs():
            k = s.get_value()
            return cpn(k * OM, k * INC, k * W)

        def rpd(th):
            r = PD / (1 + ED * np.cos(th))
            return r * np.cos(th), r * np.sin(th)

        def P3(th):
            x, y = rpd(th)
            C = Cs()
            return x * C[0] + y * C[1]

        def th():
            return kepler_theta(Mt.get_value())

        def sat():
            return P3(th())

        def vtip():
            t = th()
            C = Cs()
            vx, vy = -np.sin(t), ED + np.cos(t)
            k = 0.75 / np.hypot(vx, vy)
            return sat() + k * (vx * C[0] + vy * C[1])

        earth = globe(view)
        ax = axes3(view, 1.8)
        plane = disc3(view, lambda: Cs()[0], lambda: Cs()[1], 2.3, MUTED, 0.14)
        orb = curve(view, P3, 0, TAU, INK, width=4, R=1.0)
        pA = arrow3(view, O3, lambda: 1.5 * Cs()[0], ROSE)
        qA = arrow3(view, O3, lambda: 1.5 * Cs()[1], LIME)
        hA = arrow3(view, O3, lambda: 1.5 * Cs()[2], LILAC)
        pL = label3(view, r"\hat p", lambda: 1.75 * Cs()[0], ROSE, 36)
        qL = label3(view, r"\hat q", lambda: 1.75 * Cs()[1], LIME, 36)
        hL = label3(view, r"\hat h", lambda: 1.75 * Cs()[2], LILAC, 36)

        # ---- beat 1: the transpose ----
        mat = MobjectMatrix([[M(r"\hat p^{\,T}", size=44, color=ROSE)],
                             [M(r"\hat q^{\,T}", size=44, color=LIME)],
                             [M(r"\hat h^{\,T}", size=44, color=LILAC)]])
        mat.get_brackets().set_color(INK)
        rows = VGroup(M(r"C_{PN}=", size=44), mat).arrange(RIGHT, buff=.2)
        eq1 = E(r"\vec r_N|=|C_{PN}^T|\,\vec r_P", size=50)
        note1 = VGroup(T("rows are the frame's axes,", size=27, color=MUTED),
                       T("so the transpose undoes it", size=27, color=MUTED)).arrange(DOWN, buff=.12)
        col1 = VGroup(rows, eq1, note1).arrange(DOWN, buff=.55)
        col(col1)
        with self.say("Step two: rotate into E C I. The rows of C P N are p hat, q hat and h hat, so going back uses the transpose.") as d:
            self.play(FadeIn(earth), FadeIn(ax), FadeIn(plane), FadeIn(orb), run_time=.12 * d)
            self.play(grow(pA), grow(qA), FadeIn(VGroup(pL, qL)), run_time=.1 * d)
            self.play(s.animate.set_value(1), view.elev.animate.set_value(22), Write(rows), run_time=.43 * d)
            self.play(Write(eq1), grow(hA), FadeIn(hL), run_time=.15 * d)
            self.play(FadeIn(note1), Indicate(eq1[2]), run_time=.15 * d)

        # ---- beat 2: tip to tail ----
        def xr():
            return rpd(th())[0] * Cs()[0]

        a1 = arrow3(view, O3, xr, ROSE)
        a2 = arrow3(view, xr, sat, LIME)
        rA = arrow3(view, O3, sat, INK)
        sdot = dot3(view, sat, GOLD)
        rL = label3(view, r"\vec r", lambda: 0.55 * sat() - 0.4 * np.cross(Cs()[2], sat() / np.linalg.norm(sat())), INK, 36)
        eq1t = eq1.copy()
        l1 = E(r"\vec r_N|=|1842\,|\hat p", size=44)
        l2 = E(r"+\,(-10{,}448)\,|\hat q", size=44)
        note2 = T("added tip to tail in ECI", size=27, color=MUTED)
        col2 = VGroup(eq1t, l1, l2, note2).arrange(DOWN, buff=.45)
        l2.align_to(l1[2], LEFT)
        col(col2)
        with self.say("In words: r is its p component times p hat, plus its q component times q hat. The transpose just adds those arrows in E C I coordinates.") as d:
            self.play(FadeOut(rows), FadeOut(note1), Transform(eq1, eq1t), FadeOut(VGroup(qA, qL)),
                      run_time=.15 * d)
            self.play(Write(l1), grow(a1), run_time=.25 * d)
            self.play(Write(l2), grow(a2), run_time=.25 * d)
            self.play(grow(rA), FadeIn(sdot), FadeIn(rL), FadeIn(note2), run_time=.2 * d)

        # ---- beat 3: multiply it out ----
        vA = arrow3(view, sat, vtip, ACCENT)
        vL = label3(view, r"\vec v", lambda: vtip() + 0.35 * (vtip() - sat()) / np.linalg.norm(vtip() - sat()), ACCENT, 36)
        rres = M(r"=\begin{bmatrix}9031\\-5317\\-1647\end{bmatrix}\,\mathrm{km}", size=42)
        veq = E(r"\vec v_N|=|C_{PN}^T|\,\vec v_P", size=46)
        vres = M(r"=\begin{bmatrix}-2.864\\5.111\\-5.081\end{bmatrix}\,\mathrm{km/s}", size=42)
        eq1u = eq1.copy()
        col3 = VGroup(eq1u, rres, veq, vres).arrange(DOWN, buff=.3)
        col(col3)
        with self.say("Multiply it out, and we get nine thousand thirty one, minus five thousand three hundred seventeen, minus one thousand six hundred forty seven kilometers. The velocity comes out minus two point eight six four, five point one one one, minus five point zero eight one.") as d:
            self.play(FadeOut(VGroup(l1, l2, note2)), FadeOut(VGroup(a1, a2)), Transform(eq1, eq1u),
                      run_time=.1 * d)
            self.play(Write(rres), run_time=.4 * d)
            self.play(Write(veq), grow(vA), FadeIn(vL), run_time=.15 * d)
            self.play(Write(vres), run_time=.3 * d)

        # ---- beat 4: the round trip closes ----
        hd1 = T("rotated back", size=28, color=MUTED)
        hd2 = T("measured", size=28, color=MUTED)
        rc = M(r"\begin{bmatrix}9031\\-5317\\-1647\end{bmatrix}", size=40)
        rm = M(r"\begin{bmatrix}9031.5\\-5316.9\\-1647.2\end{bmatrix}", size=40)
        vc = M(r"\begin{bmatrix}-2.864\\5.111\\-5.081\end{bmatrix}", size=40)
        vm = M(r"\begin{bmatrix}-2.8640\\5.1112\\-5.0805\end{bmatrix}", size=40)
        rlab = VGroup(M(r"\vec r", size=44), T("km", size=26, color=MUTED)).arrange(DOWN, buff=.1)
        vlab = VGroup(M(r"\vec v", size=44, color=ACCENT), T("km/s", size=26, color=MUTED)).arrange(DOWN, buff=.1)
        ck1 = M(r"\checkmark", size=48, color=GOOD)
        ck2 = M(r"\checkmark", size=48, color=GOOD)
        grid = VGroup(VGroup(VMobject(), hd1, hd2, VMobject()),
                      VGroup(rlab, rc, rm, ck1), VGroup(vlab, vc, vm, ck2))
        xs = [0, 1.35, 3.75, 5.5]
        for k, row in enumerate(grid):
            for j, m in enumerate(row):
                m.move_to([xs[j], -k * 2.1, 0])
        hd2.move_to([xs[2], -0.75, 0])
        hd1.move_to([xs[1], -0.75, 0])
        col(grid)
        with self.say("Those are exactly the measured r and v we started from. The round trip closes.") as d:
            self.play(FadeOut(VGroup(eq1, veq)),
                      ReplacementTransform(rres, rc), ReplacementTransform(vres, vc),
                      FadeIn(VGroup(rlab, vlab, hd1)), run_time=.3 * d)
            self.play(FadeIn(VGroup(hd2, rm, vm), shift=LEFT * .3), run_time=.25 * d)
            self.play(FadeIn(ck1, scale=1.5), FadeIn(ck2, scale=1.5), run_time=.2 * d)

        # ---- beat 5: propagate with frozen elements ----
        frozen = VGroup(
            T("frozen", size=28, color=MUTED),
            E(r"a|=26{,}564\ \mathrm{km}\qquad|e|=0.741", size=38),
            E(r"i|=63.4^\circ\quad|\Omega|=145^\circ\quad|\omega|=270^\circ", size=38),
        ).arrange(DOWN, buff=.22)
        card = panel(frozen)
        thr = readout(r"\theta =", lambda: np.degrees(th()) % 360, digits=1)
        thr.set_color(GOLD).scale(1.3)
        n0 = T("Kepler's equation", size=34)
        n2 = M(r"\vec r_P,\ \vec v_P", size=48)
        n3 = M(r"\vec r,\ \vec v", size=48)
        chain = VGroup(n0, thr, n2, n3).arrange(DOWN, buff=.6)
        arrs = VGroup(*[Arrow(chain[k].get_bottom(), chain[k + 1].get_top(), buff=.1, color=MUTED,
                              stroke_width=4) for k in range(3)])
        cT = M(r"C_{PN}^T", size=42).next_to(arrs[2], RIGHT, buff=.2)
        flow = VGroup(chain, arrs, cT)
        col5 = VGroup(card, flow).arrange(DOWN, buff=.4)
        col(col5)
        thr.clear_updaters()
        thr_live = readout(r"\theta =", lambda: np.degrees(th()) % 360, digits=1)
        thr_live.set_color(GOLD).scale(1.3).move_to(thr)
        thr_live.add_updater(lambda m: m.move_to(thr))
        with self.say("And here's why elements are worth the trouble. To move the satellite forward in time, five numbers stay frozen. Only theta advances, using Kepler's equation. Then one rotation gives r and v again.") as d:
            self.play(FadeOut(grid), FadeOut(VGroup(rL, vL)), FadeIn(card), run_time=.12 * d)
            self.play(Circumscribe(card, color=MUTED), run_time=.18 * d)
            self.play(FadeIn(n0), GrowArrow(arrs[0]), FadeIn(thr_live), run_time=.12 * d)
            self.play(Mt.animate.set_value(M0 + TAU),
                      LaggedStart(GrowArrow(arrs[1]), FadeIn(n2), GrowArrow(arrs[2]), FadeIn(cT), FadeIn(n3),
                                  lag_ratio=.35),
                      run_time=.5 * d, rate_func=linear)
            self.play(Indicate(cT), run_time=.08 * d)
        self.wipe()
