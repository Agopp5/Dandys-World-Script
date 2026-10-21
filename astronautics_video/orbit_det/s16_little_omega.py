"""S16: step five, little omega from the third column of C_PN (BRIEF.md S16)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# ---- facts (Kluever Example 3.1, full-precision state vector) ----
MU = 3.986e5
R0 = np.array([9031.5, -5316.9, -1647.2])
V0 = np.array([-2.8640, 5.1112, -5.0805])
H = np.cross(R0, V0)
EV = np.cross(V0, H) / MU - R0 / np.linalg.norm(R0)
NV = np.cross([0, 0, 1], H)
assert np.allclose(EV, [0.1903, 0.2718, -0.6627], atol=6e-5)
assert np.isclose(np.linalg.norm(EV), 0.7411, atol=5e-5)
assert np.allclose(NV, [-50602, 35432, 0], atol=1)
COSW = NV @ EV / (np.linalg.norm(NV) * np.linalg.norm(EV))
assert round(COSW, 5) == 0.00001                       # "essentially zero"
assert np.isclose(np.degrees(np.arccos(COSW)), 90, atol=1e-3)   # arccos alone gives 90 ...
C13, C23 = -0.8942, 0.0
assert np.isclose(EV[0] / np.linalg.norm(EV), 0.2568, atol=1e-4)
assert np.isclose(EV[2] / np.linalg.norm(EV), C13, atol=1e-4)
assert np.isclose(np.degrees(np.arctan2(C13, C23)), -90)
assert np.isclose(np.degrees(np.arctan2(C13, C23)) + 360, 270)
assert EV[2] < 0 and np.isclose(EV[2], -0.6627, atol=5e-5)   # ... e_Z < 0 picks 270
CPN = [["0.2568", "0.3668", "-0.8942"], ["-0.8192", "0.5736", "0"], ["0.5129", "0.7324", "0.4478"]]

# drawn Molniya (not to scale): a = 3.0, e = 0.6, Omega = 145, i = 63.4, omega = 270
A_D, E_D = 3.0, 0.6
OM, INC, W = np.radians(145.0), np.radians(63.4), np.radians(270.0)
CD = cpn(OM, INC, W)
assert np.allclose(CD[0], [0.2568, 0.3668, -0.8942], atol=2e-3)
PHAT, HHAT = CD[0], CD[2]
NHAT = np.array([np.cos(OM), np.sin(OM), 0.0])
F = orbit(A_D, E_D, OM, INC, W)
PERI, APO = F(0.0), F(np.pi)
assert PERI[2] < 0 and APO[2] > 0                       # perigee south, apogee north
assert np.allclose(PERI / np.linalg.norm(PERI), PHAT, atol=1e-6)
R_ASC = A_D * (1 - E_D ** 2) / (1 + E_D * np.cos(np.pi / 2))   # theta = 90 deg is the node (u = 0)
ASC = R_ASC * NHAT
assert np.allclose(F(np.radians(90.0)), ASC, atol=1e-6)


class S16_omega(VScene):
    budget = 115

    def construct(self):
        hdr = self.section("Step five: little omega")

        # ---- 3D picture on the left ----
        view = View(elev=20, azim=20, scale=0.94, center=(-3.6, -1.75))
        eq_disc = disc3(view, (1, 0, 0), (0, 1, 0), 2.6, INK2, opacity=0.10)
        earth = globe(view)
        orb = curve(view, F, 0, TAU, INK, R=1.0)
        node_line = line3(view, -2.6 * NHAT, 2.6 * NHAT, SKY, dashed=True)
        asc = dot3(view, ASC, SKY)
        asc_lbl = label3(view, r"\text{node}", ASC + 0.35 * NHAT + np.array([0, 0, -0.6]), SKY, 36)
        peri = dot3(view, PERI, ROSE, radius=0.09)
        apo = dot3(view, APO, INK2)
        pic = Group(eq_disc, earth, orb, node_line, asc, asc_lbl, peri, apo)

        # ---- C_PN with its third column ----
        mat = Matrix(CPN, h_buff=1.85, v_buff=0.75,
                     element_to_mobject=lambda s: MathTex(s, font_size=40, color=INK))
        lhs = M(r"C_{PN}=", size=40)
        cblock = VGroup(lhs, mat).arrange(RIGHT, buff=.2)
        lhs.next_to(mat, UP, buff=.12).align_to(mat, LEFT)
        fit(cblock, 6.6, 3.1)
        cblock.move_to([3.3, 2.05, 0])
        col3 = mat.get_columns()[2]
        colbox = SurroundingRectangle(col3, color=MINT, buff=.12, corner_radius=.08)
        e13, e23 = mat.get_entries()[2], mat.get_entries()[5]
        t13 = E(r"C_{13}|=|-0.8942", size=40)
        t23 = E(r"C_{23}|=|0", size=40)
        for t in (t13, t23):
            paint(t, {0: MINT, 2: MINT})
        VGroup(t13, t23).arrange(RIGHT, buff=.9).next_to(cblock, DOWN, buff=.4).set_x(3.3)
        self.beat("Little omega uses the third column: C one three is minus zero point eight nine four two, and C two three is zero.",
                  [FadeIn(pic), FadeIn(cblock)], Create(colbox),
                  [e13.animate.set_color(MINT), FadeIn(t13)],
                  [e23.animate.set_color(MINT), FadeIn(t23)], w=(.25, .2, .3, .25))

        # ---- atan2 ----
        l1 = E(r"\omega|=|\operatorname{atan2}(-0.8942,\ 0)", size=42)
        l2 = E(r"=|-90^\circ", size=42)
        l3 = E(r"\omega|=|-90^\circ+360^\circ|=|270^\circ", size=42)
        paint(l3, {4: MINT})
        for m in (l1, l2, l3):
            fit(m, 6.4, 1)
        l1.move_to([3.3, -0.75, 0])
        l2.next_to(l1, DOWN, buff=.35).align_to(l1[1], LEFT)
        l3.next_to(l2, DOWN, buff=.4).set_x(3.3)
        why = T("add 360 degrees", size=26, color=MUTED).next_to(l3, DOWN, buff=.2)
        self.beat("atan two of a negative number and zero is minus ninety degrees. Add three sixty: little omega is two hundred seventy degrees.",
                  Write(l1), Write(l2), .1, [Write(l3), FadeIn(why)], FadeIn(g1 := glow(l3[4], MINT)), w=(.3, .2, .25, .15))

        # fold: one boxed result, then the textbook route
        res = E(r"\omega|=|270^\circ", size=40)
        paint(res, {2: MINT})
        res_note = T("from the matrix", size=30, color=MUTED)
        res_card = panel(VGroup(res, res_note).arrange(RIGHT, buff=.3), color=MINT)
        res_card.move_to([3.3, 2.55, 0])
        k1 = E(r"\cos|\omega|=|\dfrac{\vec n\cdot\vec e}{n\,e}", size=42)
        tint(k1[3], [((0, 2), LIME), ((3, 5), ROSE), ((6, 7), LIME), ((7, 8), ROSE)])
        k2 = E(r"=|0.00001|\approx|0", size=42)
        k3 = E(r"\omega|=|90^\circ\ \text{or}\ 270^\circ\,?", size=42)
        for m in (k1, k2, k3):
            fit(m, 6.4, 1.4)
        k1.move_to([3.3, 0.85, 0])
        k2.next_to(k1, DOWN, buff=.3).align_to(k1[2], LEFT)
        k3.next_to(k2, DOWN, buff=.45).set_x(3.3)
        why2 = T("arccos can't tell which", size=26, color=MUTED).next_to(k3, DOWN, buff=.2)
        clear = [FadeOut(VGroup(cblock, colbox, t13, t23, l1, l2, l3, why, g1)), FadeIn(res_card)]
        self.beat("The textbook route: the cosine of omega is n dot e over n e, which is essentially zero. So omega is ninety or two seventy. Arc cosine can't tell which.",
                  clear, Write(k1), Write(k2), .1, [Write(k3), FadeIn(why2)], w=(.15, .3, .2, .25))

        # ---- e_Z decides ----
        drop_pt = np.array([PERI[0], PERI[1], 0.0])
        e_arrow = arrow3(view, (0, 0, 0), PERI, ROSE)
        e_lbl = label3(view, r"\vec e", PERI + 0.75 * NHAT + np.array([0, 0, 0.1]), ROSE, 44)
        drop = line3(view, PERI, drop_pt, ROSE, dashed=True)
        foot = dot3(view, drop_pt, MUTED, radius=0.05)
        p_lbl = label3(view, r"\text{perigee}", PERI - 1.3 * NHAT + np.array([0, 0, -0.55]), ROSE, 36)
        j1 = E(r"e_Z|=|-0.6627|<|0", size=42)
        paint(j1, {0: ROSE, 2: ROSE})
        j2 = E(r"\Rightarrow|\omega|=|270^\circ", size=44)
        paint(j2, {3: MINT})
        fit(j1, 6.4, 1); fit(j2, 6.4, 1)
        j1.move_to([3.3, 0.4, 0])
        j2.next_to(j1, DOWN, buff=.5)
        why3 = T("perigee below the equator", size=26, color=MUTED).next_to(j2, DOWN, buff=.2)
        self.beat("Look at the eccentricity vector's K component: minus zero point six six two seven. Perigee is below the equator, so it's two seventy.",
                  [FadeOut(VGroup(k1, k2, why2)), k3.animate.next_to(res_card, DOWN, buff=.3)],
                  [grow(e_arrow), FadeIn(e_lbl)], Write(j1),
                  [Create(drop), FadeIn(foot), FadeIn(p_lbl), Flash(peri, color=ROSE)],
                  [Write(j2), FadeIn(why3), FadeIn(glow(j2[3], MINT))], w=(.12, .2, .23, .2, .25))

        # ---- the omega arc in the orbit plane ----
        w_arc = arc3(view, HHAT, NHAT, W, 1.4, MINT, width=6)
        mid = np.cos(W / 2) * NHAT + np.sin(W / 2) * np.cross(HHAT, NHAT)
        w_lbl = label3(view, r"\omega", 2.0 * mid, MINT, 44)
        a_lbl = label3(view, r"\text{apogee}", APO - 1.9 * NHAT + np.array([0, 0, 0.1]), INK2, 36)
        self.beat("That matches the picture: perigee at the very bottom of the orbit, apogee high over the north.",
                  grow(w_arc), FadeIn(w_lbl),
                  [Indicate(peri, color=ROSE), FadeIn(a_lbl), Indicate(apo, color=INK)], .1, w=(.4, .15, .35))
        self.wipe()
