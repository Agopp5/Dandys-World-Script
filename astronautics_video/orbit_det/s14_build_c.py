"""S14: build C_PN from p-hat, q-hat, h-hat and read the inclination (BRIEF.md S14)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# ---------------------------------------------------------------- facts (Kluever Example 3.1)
MU = 3.986e5
R0 = np.array([9031.5, -5316.9, -1647.2])
V0 = np.array([-2.8640, 5.1112, -5.0805])
H = np.cross(R0, V0)
EV = np.cross(V0, H) / MU - R0 / np.linalg.norm(R0)
P_HAT = EV / np.linalg.norm(EV)
H_HAT = H / np.linalg.norm(H)
Q_HAT = np.cross(H_HAT, P_HAT)
assert np.allclose(P_HAT, [0.2568, 0.3668, -0.8942], atol=6e-4)
assert np.allclose(H_HAT, [0.5129, 0.7324, 0.4478], atol=6e-4)
assert np.allclose(Q_HAT, [-0.8192, 0.5736, 0.0000], atol=6e-4)
C_PN = np.array([P_HAT, Q_HAT, H_HAT])
assert np.isclose(np.linalg.det(C_PN), 1.0, atol=1e-6)          # right handed set
assert np.isclose(C_PN[2, 2], 0.4478, atol=6e-4)
INC = np.arccos(C_PN[2, 2])
assert np.isclose(np.degrees(np.arccos(0.4478)), 63.4, atol=0.05)
assert np.isclose(np.degrees(INC), 63.4, atol=0.05)
OM = np.arctan2(C_PN[2, 0], -C_PN[2, 1])                        # 145 deg
W = np.arctan2(C_PN[0, 2], C_PN[1, 2]) % (2 * np.pi)            # 270 deg
assert np.isclose(np.degrees(OM), 145.0, atol=0.1)
assert np.isclose(np.degrees(W), 270.0, atol=0.1)
assert np.allclose(cpn(OM, INC, W), C_PN, atol=2e-3)            # same matrix from the kit

ROWS = [["0.2568", "0.3668", "-0.8942"],
        ["-0.8192", "0.5736", "0.0000"],
        ["0.5129", "0.7324", "0.4478"]]
for row, vec in zip(ROWS, [P_HAT, Q_HAT, H_HAT]):
    assert np.allclose([float(s) for s in row], vec, atol=6e-4)

K_HAT = np.array([0.0, 0.0, 1.0])
ARC_AXIS = np.cross(K_HAT, H_HAT) / np.linalg.norm(np.cross(K_HAT, H_HAT))
HXY = np.array([H_HAT[0], H_HAT[1], 0.0]) / np.linalg.norm(H_HAT[:2])
ARC_MID = np.cos(INC / 2) * K_HAT + np.sin(INC / 2) * HXY

XR = 3.9          # center of the right-hand text column


def vec_line(sym, row, color):
    """sym = ( a , b , c ) with the numbers in the vector's hue."""
    m = E(sym + r"|=|\big(|" + row[0] + "|,|" + row[1] + "|,|" + row[2] + r"|\big)", size=40)
    for k in (3, 5, 7):
        m[k].set_color(color)
    return m


class S14_Build_C(VScene):
    budget = 75

    def construct(self):
        self.section("Step three: build the rotation matrix")

        view = View(elev=22, azim=-15, scale=0.8, center=(-3.2, -1.6))
        earth = globe(view)
        ax = axes3(view, 2.6)
        orb = curve(view, orbit(3.0, 0.6, OM, INC, W), 0, 2 * np.pi, INK, width=3, R=1.0)
        L = 2.2
        a_p = arrow3(view, (0, 0, 0), L * P_HAT, ROSE)
        a_h = arrow3(view, (0, 0, 0), L * H_HAT, LILAC)
        a_q = arrow3(view, (0, 0, 0), L * Q_HAT, LIME)
        l_p = label3(view, r"\hat p", (L + 0.4) * P_HAT, ROSE, 40)
        l_h = label3(view, r"\hat h", (L + 0.4) * H_HAT, LILAC, 40)
        l_q = label3(view, r"\hat q", (L + 0.4) * Q_HAT, LIME, 40)

        # right column: definition, then numbers, then a grey note
        y_p, y_h, y_q = 2.4, 0.4, -1.6
        d_p = E(r"\hat p|=|\vec e|\,/\,|e", size=44).move_to([XR, y_p, 0])
        n_p = vec_line(r"\hat p", ROWS[0], ROSE).move_to([XR, y_p, 0])
        w_p = T("unit vector toward perigee", size=26, color=MUTED).next_to(n_p, DOWN, buff=.2)

        self.beat("Now build the perifocal frame from these two vectors. p hat is the eccentricity vector divided by its length.",
                  [FadeIn(earth), FadeIn(ax), Create(orb)], Write(d_p), [grow(a_p), FadeIn(l_p)],
                  .1, morph(d_p, n_p, [(0, 0), (1, 1)]), FadeIn(w_p),
                  w=(.2, .15, .15, .25, .1))

        d_h = E(r"\hat h|=|\vec h|\,/\,|h", size=44).move_to([XR, y_h, 0])
        n_h = vec_line(r"\hat h", ROWS[2], LILAC).move_to([XR, y_h, 0])
        w_h = T("normal to the orbit plane", size=26, color=MUTED).next_to(n_h, DOWN, buff=.2)
        self.beat("h hat is h divided by its length.",
                  [Write(d_h), grow(a_h), FadeIn(l_h)], morph(d_h, n_h, [(0, 0), (1, 1)]),
                  FadeIn(w_h), w=(.35, .4, .25))

        d_q = E(r"\hat q|=|\hat h|\times|\hat p", size=44).move_to([XR, y_q, 0])
        n_q = vec_line(r"\hat q", ROWS[1], LIME).move_to([XR, y_q, 0])
        w_q = T("in the plane, 90 degrees past perigee", size=26, color=MUTED).next_to(n_q, DOWN, buff=.2)
        self.beat("And q hat completes the right handed set: h hat cross p hat.",
                  Write(d_q), [grow(a_q), FadeIn(l_q)], .05,
                  morph(d_q, n_q, [(0, 0), (1, 1)]), FadeIn(w_q), w=(.25, .25, .3, .15))

        # ---- stack the rows into C_PN
        mat = Matrix(ROWS, h_buff=1.75, v_buff=.85)
        mat.scale(40 / 48)
        for r, col in enumerate((ROSE, LIME, LILAC)):
            mat.get_rows()[r].set_color(col)
        lhs = M(r"C_{PN}", "=", size=44)
        grp = VGroup(lhs, mat).arrange(RIGHT, buff=.25)
        grp.move_to([3.6, 1.5, 0])
        ent = mat.get_rows()
        moves = []
        for line, r in ((n_p, 0), (n_q, 1), (n_h, 2)):
            for j, k in enumerate((3, 5, 7)):
                moves.append(ReplacementTransform(line[k], ent[r][j]))
            moves.append(line[0].animate.move_to(lhs[0]).set_opacity(0))   # the three hats merge into C_PN
            moves += [FadeOut(line[k]) for k in (1, 2, 4, 6, 8)]
        self.beat("Stack them as rows, and that's C P N, with real numbers in it.",
                  [FadeOut(w_p), FadeOut(w_h), FadeOut(w_q)], moves,
                  [FadeIn(lhs), FadeIn(mat.get_brackets())], .2, w=(.15, .45, .2))

        # ---- the corner entry and the inclination
        c33 = ent[2][2]
        box = SurroundingRectangle(c33, color=EMBER, buff=.1)
        eq1 = E(r"\cos|i|=|C_{33}|=|0.4478", size=44).move_to([XR, -1.0, 0])
        eq2 = E(r"i|=|\arccos(0.4478)|=|63.4^\circ", size=44).move_to([XR, -2.5, 0])
        eq2[4].set_color(EMBER)
        arc = arc3(view, ARC_AXIS, K_HAT, INC, 1.5, EMBER)
        l_i = label3(view, "i", 1.85 * ARC_MID, EMBER, 38)
        with self.say("The corner entry is zero point four four seven eight. Its arc cosine is the inclination: sixty three point four degrees.") as d:
            self.play(Create(box), Indicate(c33, color=EMBER), run_time=.18 * d)
            self.play(Write(eq1), run_time=.2 * d)
            self.wait(.1 * d)
            self.play(Write(eq2), run_time=.2 * d)
            self.play(grow(arc), FadeIn(l_i), run_time=.17 * d)
            self.play(FadeIn(glow(eq2[4], EMBER)), Indicate(a_h), run_time=.15 * d)
        self.wipe()
