"""S15: Step four, capital Omega two ways (BRIEF.md S15)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# ---- facts (Kluever Example 3.1), every number on screen is checked here ----
MU = 3.986e5
R0 = np.array([9031.5, -5316.9, -1647.2])
V0 = np.array([-2.8640, 5.1112, -5.0805])
H = np.cross(R0, V0)
EV = np.cross(V0, H) / MU - R0 / np.linalg.norm(R0)
P_HAT = EV / np.linalg.norm(EV)
H_HAT = H / np.linalg.norm(H)
Q_HAT = np.cross(H_HAT, P_HAT)
CPN = np.array([P_HAT, Q_HAT, H_HAT])
CPN_SHOWN = np.array([[0.2568, 0.3668, -0.8942], [-0.8192, 0.5736, 0.0], [0.5129, 0.7324, 0.4478]])
assert np.allclose(CPN, CPN_SHOWN, atol=1.5e-4)
OM = np.degrees(np.arctan2(CPN[2, 0], -CPN[2, 1]))          # atan2(C31, -C32)
assert abs(OM - 145.0) < 0.05
assert CPN_SHOWN[2, 0] > 0 and -CPN_SHOWN[2, 1] < 0            # second quadrant
INC = np.degrees(np.arccos(CPN[2, 2]))
assert abs(INC - 63.4) < 0.05
W = np.degrees(np.arctan2(CPN[0, 2], CPN[1, 2])) % 360          # little omega = 270
assert abs(W - 270) < 0.05
# third row = (sin i sin Om, -sin i cos Om, cos i)
si, ci = np.sin(np.radians(INC)), np.cos(np.radians(INC))
assert np.allclose(CPN[2], [si * np.sin(np.radians(OM)), -si * np.cos(np.radians(OM)), ci], atol=1e-9)
assert np.allclose(cpn(np.radians(OM), np.radians(INC), np.radians(W)), CPN, atol=1e-6)
# textbook route: n = K x h
N_VEC = np.cross([0.0, 0.0, 1.0], H)
assert np.allclose(N_VEC, [-50602, 35432, 0], atol=2)
N_MAG = np.linalg.norm(N_VEC)
assert abs(N_MAG - 61774) < 2
COS_OM, SIN_OM = N_VEC[0] / N_MAG, N_VEC[1] / N_MAG
assert abs(COS_OM - (-0.8192)) < 5e-5 and abs(SIN_OM - 0.5736) < 5e-5
assert abs(-50602 / 61774 - (-0.8192)) < 1e-4 and abs(35432 / 61774 - 0.5736) < 1e-4  # rounded inputs
assert abs(np.degrees(np.arctan2(SIN_OM, COS_OM)) - OM) < 1e-9
N_HAT = N_VEC / N_MAG
assert np.allclose(Q_HAT, N_HAT, atol=1e-4)                     # the coincidence (omega = 270)
# drawn Molniya (not to scale): a = 3.0, e = 0.6; it crosses the equator at r = p = a(1 - e^2)
A_DR, E_DR = 3.0, 0.6
P_DR = A_DR * (1 - E_DR ** 2)
f_orb = orbit(A_DR, E_DR, np.radians(OM), np.radians(INC), np.radians(W))
asc_pt = f_orb(np.radians((360 - W) % 360))                      # u = 0: theta = -omega
assert np.allclose(asc_pt, P_DR * N_HAT, atol=1e-3)
assert asc_pt.shape == (3,)

ZERO = np.array([0.0, 0.0, 0.0])
KZ = np.array([0.0, 0.0, 1.0])
IX = np.array([1.0, 0.0, 0.0])
JY = np.array([0.0, 1.0, 0.0])


class S15_Omega(VScene):
    budget = 139

    def construct(self):
        self.section("Step four: capital Omega, two ways")

        # ---------- beat 1: the bottom row of C_PN ----------
        mat = Matrix([["0.2568", "0.3668", "-0.8942"], ["-0.8192", "0.5736", "0"],
                      ["0.5129", "0.7324", "0.4478"]], h_buff=2.0).scale(.86)
        mat.set_color(INK)
        lhs = M(r"C_{PN} =", size=44)
        grp = VGroup(lhs, mat).arrange(RIGHT, buff=.25)
        tags = VGroup(*[M(t, size=40, color=c) for t, c in
                        [(r"\hat p", ROSE), (r"\hat q", LIME), (r"\hat h", LILAC)]])
        for t, row in zip(tags, mat.get_rows()):
            t.next_to(mat, RIGHT, buff=.3).set_y(row.get_y())
        block = VGroup(grp, tags).move_to([-2.75, 1.35, 0])
        ent = mat.get_entries()
        row_box = SurroundingRectangle(mat.get_rows()[2], color=LILAC, buff=.12)
        row_eq = M(r"\text{row 3} = \big(\sin i\,\sin\Omega,\ \ {-\sin i}\,\cos\Omega,\ \ \cos i\big)", size=40)
        fit(row_eq, 6.6, 1)
        row_eq.move_to([-3.5, -.55, 0])
        m31 = E(r"C_{31}|=|0.5129", size=40)
        m32 = E(r"-C_{32}|=|-0.7324", size=40)
        m31[2].set_color(SKY)
        m32[2].set_color(SKY)
        marks = VGroup(m31, m32).arrange(RIGHT, buff=.9).move_to([-3.5, -1.65, 0])
        b31 = SurroundingRectangle(ent[6], color=SKY, buff=.08)
        b32 = SurroundingRectangle(ent[7], color=SKY, buff=.08)
        self.beat("For capital Omega, take the first two entries of the bottom row. C three one is zero point five one two nine. C three two is zero point seven three two four, so minus C three two is negative.",
                  FadeIn(block), Create(row_box), FadeIn(row_eq), [Create(b31), FadeIn(m31)], .1,
                  [Create(b32), FadeIn(m32)], w=(.18, .12, .15, .25, .2))

        # ---------- beat 2: the unit circle picks the quadrant ----------
        O = np.array([3.8, .75, 0])
        Rc = 1.6
        ang = np.radians(OM)
        xax = Line(O + 2.1 * LEFT, O + 2.1 * RIGHT, color=AXIS, stroke_width=2)
        yax = Line(O + 2.0 * DOWN, O + 2.0 * UP, color=AXIS, stroke_width=2)
        circ = Circle(radius=Rc, color=MUTED, stroke_width=3).move_to(O)
        quad = Sector(radius=Rc, start_angle=PI / 2, angle=PI / 2, arc_center=O,
                      fill_color=SKY, fill_opacity=.16, stroke_width=0)
        P = O + Rc * np.array([np.cos(ang), np.sin(ang), 0])
        ray = Line(O, P, color=SKY, stroke_width=5)
        dot = Dot(P, color=SKY, radius=.1)
        arcO = Arc(radius=.55, start_angle=0, angle=ang, arc_center=O, color=SKY, stroke_width=4)
        labO = M(r"\Omega", size=40, color=SKY).move_to(O + .9 * np.array([np.cos(ang / 2), np.sin(ang / 2), 0]))
        dx = DashedLine(P, [P[0], O[1], 0], color=MUTED)
        dy = DashedLine(P, [O[0], P[1], 0], color=MUTED)
        sin_lab = M(r"\sin\Omega > 0", size=40).next_to(O + Rc * UP, UR, buff=.12)
        cos_lab = M(r"\cos\Omega < 0", size=40).next_to(O + Rc * LEFT, DOWN, buff=.25)
        q_lab = T("quadrant II", size=26, color=MUTED).next_to(O + Rc * UP, UL, buff=.12).shift(.3 * LEFT)
        atan = E(r"\Omega|=|\operatorname{atan2}(0.5129,\,-0.7324)|=|145.0^\circ", size=44)
        atan.set_color(SKY).move_to([0, -3.0, 0])
        self.beat("Positive sine, negative cosine. That's the second quadrant. atan two gives one hundred forty five degrees.",
                  [Create(xax), Create(yax), Create(circ)], [FadeIn(sin_lab), FadeIn(cos_lab)],
                  [FadeIn(quad), FadeIn(q_lab)], [Create(ray), FadeIn(dot), Create(dx), Create(dy),
                                                  Create(arcO), FadeIn(labO)],
                  Write(atan), w=(.12, .18, .2, .2, .3))

        # ---------- beat 3: the textbook route, n = K x h, in 3D ----------
        view = View(elev=34, azim=0, scale=.9, center=(-3.3, -1.7))
        g = globe(view)
        axs = axes3(view, 2.4)
        eqd = disc3(view, IX, JY, 2.6, MUTED, .1)
        orb = curve(view, f_orb, 0, TAU, INK, R=1.0)
        harr = arrow3(view, ZERO, 2.0 * H_HAT, LILAC)
        hlab = label3(view, r"\vec h", 2.3 * H_HAT, LILAC, 40)
        node = line3(view, -2.9 * N_HAT, 2.9 * N_HAT, SKY, dashed=True)
        asc = dot3(view, P_DR * N_HAT, SKY)
        narr = arrow3(view, ZERO, 2.7 * N_HAT, LIME)
        nlab = label3(view, r"\vec n", 3.05 * N_HAT, LIME, 40)

        chip = E(r"\Omega|=|145.0^\circ", size=40).set_color(SKY)
        chip_note = TX(r"from row 3 of $C_{PN}$", size=26, color=MUTED)
        chip_g = VGroup(chip, chip_note).arrange(RIGHT, buff=.35)
        eqn1 = E(r"\vec n|=|\hat K|\times|\vec h", size=44, cmap={r"\hat K": INK2})
        eqn2 = M(r"=\big(-50{,}602,\ 35{,}432,\ 0\big)", size=40)
        note = T("points to the ascending node", size=26, color=MUTED)
        col = VGroup(chip_g, eqn1, eqn2, note).arrange(DOWN, aligned_edge=LEFT, buff=.38)
        eqn2.shift(.4 * RIGHT)
        col.move_to([4.0, 1.75, 0])
        old = VGroup(block, row_box, row_eq, m31, m32, b31, b32, xax, yax, circ, quad, ray, dot,
                     arcO, labO, dx, dy, sin_lab, cos_lab, q_lab)
        self.beat("The textbook gets the same answer with the node vector: n equals K cross h. It points along the line of nodes, toward the ascending node.",
                  [FadeOut(old), ReplacementTransform(atan, chip), FadeIn(chip_note)],
                  [FadeIn(g), FadeIn(axs), FadeIn(eqd), FadeIn(orb), FadeIn(harr), FadeIn(hlab)],
                  Write(eqn1), FadeIn(eqn2),
                  [Create(node), grow(narr), FadeIn(nlab), FadeIn(asc)], FadeIn(note),
                  w=(.14, .16, .14, .12, .3, .14))

        # ---------- beat 4: cos and sin of Omega from n, arc in the equator ----------
        cos_eq = E(r"\cos\Omega|=|\frac{-50{,}602}{61{,}774}|=|-0.8192", size=40)
        sin_eq = E(r"\sin\Omega|=|\frac{35{,}432}{61{,}774}|=|0.5736", size=40)
        cs = VGroup(cos_eq, sin_eq).arrange(DOWN, aligned_edge=LEFT, buff=.35)
        cs.next_to(note, DOWN, buff=.5, aligned_edge=LEFT)
        nmag = T("divide by its length, 61,774", size=26, color=MUTED).next_to(cs, DOWN, buff=.3, aligned_edge=LEFT)
        tick = M(r"\checkmark", size=52, color=GOOD).next_to(chip, LEFT, buff=.25)
        arc_om = arc3(view, KZ, IX, ang, 1.55, SKY)
        mid = ang / 2
        arc_lab = label3(view, r"\Omega", 1.95 * np.array([np.cos(mid), np.sin(mid), 0]), SKY, 40)
        self.beat("Its components give cosine Omega equals minus zero point eight one nine two, and sine Omega equals zero point five seven three six. The same quadrant, the same one hundred forty five degrees.",
                  [FadeIn(cos_eq), FadeIn(nmag)], FadeIn(sin_eq), [grow(arc_om), FadeIn(arc_lab)],
                  [FadeIn(tick), Indicate(chip, color=SKY)], w=(.3, .25, .25, .2))

        # ---------- beat 5: q-hat lies on n-hat ----------
        qarr = arrow3(view, ZERO, 2.7 * Q_HAT, LIME)
        qlab = label3(view, r"\hat q = \hat n", 3.25 * Q_HAT + .35 * KZ, LIME, 40)
        qq = E(r"\hat q|=|\hat n", size=48, cmap={r"\hat n": LIME})
        why = E(r"\text{because }|\omega|=|270^\circ", size=40)
        qg = VGroup(qq, why).arrange(DOWN, aligned_edge=LEFT, buff=.35).move_to(cs, aligned_edge=UL)
        halo = glow(qq, LIME)
        self.beat("A fun coincidence: q hat equals the node direction here. That's not an accident; it happens because little omega turns out to be two seventy.",
                  [FadeOut(cs), FadeOut(nmag), FadeOut(nlab)],
                  [grow(qarr), FadeIn(qlab), FadeIn(qq)], [FadeIn(halo)], .1,
                  [FadeIn(why), FadeOut(halo)], w=(.12, .3, .15, .33))
        self.wipe()
