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

# on-screen arithmetic, with the rounded numbers exactly as shown
assert np.allclose(EV, [0.1903, 0.2718, -0.6627], atol=6e-5)
assert np.isclose(np.linalg.norm(EV), 0.7411, atol=6e-5)
assert np.allclose(H, [35432, 50602, 30934], atol=0.5)
assert np.isclose(np.linalg.norm(H), 69086, atol=0.5)
assert np.allclose(np.array([0.1903, 0.2718, -0.6627]) / 0.7411, [0.2568, 0.3668, -0.8942], atol=5e-5)
assert np.allclose(np.array([35432, 50602, 30934]) / 69086, [0.5129, 0.7324, 0.4478], atol=5e-5)
assert np.isclose(0.7324 * (-0.8942) - 0.4478 * 0.3668, -0.8192, atol=5e-5)     # q_x = h_y p_z - h_z p_y
assert np.isclose(0.4478 * 0.2568 - 0.5129 * (-0.8942), 0.5736, atol=5e-5)      # q_y = h_z p_x - h_x p_z
assert abs(0.5129 * 0.3668 - 0.7324 * 0.2568) < 6e-5                           # q_z = h_x p_y - h_y p_x ~ 0
assert abs(Q_HAT[2]) < 1e-5                                                    # unrounded: 0.0000

XR = 3.25         # center of the right-hand text column
LEFT_X = -0.25    # left edge of the long derivation lines
STACK_Y = (3.3, 2.5, 1.7)   # finished p-hat, h-hat, q-hat rows
WORK_Y = 0.4                # where each derivation happens


def vec_line(sym, row, color):
    """sym = ( a , b , c ) with the numbers in the vector's hue."""
    m = E(sym + r"|=|\big(|" + row[0] + "|,|" + row[1] + "|,|" + row[2] + r"|\big)", size=40)
    for k in (3, 5, 7):
        m[k].set_color(color)
    return m


def div_line(sym, row, mag, color):
    """sym = ( a , b , c ) / mag."""
    m = E(sym + r"|=|\big(|" + row[0] + "|,|" + row[1] + "|,|" + row[2] + r"|\big)|\,/\,|" + mag, size=40)
    for k in (3, 5, 7, 10):
        m[k].set_color(color)
    return m


class S14_Build_C(VScene):
    budget = 75

    def construct(self):
        self.section("Step three: build the rotation matrix")

        view = View(elev=22, azim=-15, scale=0.86, center=(-3.75, -1.3))
        earth = globe(view)
        ax = axes3(view, 3.0)
        orb = curve(view, orbit(3.0, 0.6, OM, INC, W), 0, 2 * np.pi, INK, width=3, R=1.0)
        L = 2.7
        a_p = arrow3(view, (0, 0, 0), L * P_HAT, ROSE)
        a_h = arrow3(view, (0, 0, 0), L * H_HAT, LILAC)
        a_q = arrow3(view, (0, 0, 0), L * Q_HAT, LIME)
        l_p = label3(view, r"\hat p", (L + 0.4) * P_HAT, ROSE, 40)
        l_h = label3(view, r"\hat h", (L + 0.4) * H_HAT, LILAC, 40)
        l_q = label3(view, r"\hat q", (L + 0.4) * Q_HAT, LIME, 40)
        work = [XR, WORK_Y, 0]

        # ---- p-hat: definition -> numbers -> unit vector, then it parks in the stack
        d_p = E(r"\hat p|=|\vec e|\,/\,|e", size=44).move_to(work)
        s_p = div_line(r"\hat p", ["0.1903", "0.2718", "-0.6627"], "0.7411", ROSE).move_to(work)
        n_p = vec_line(r"\hat p", ROWS[0], ROSE).move_to(work)
        w_p = T("unit vector toward perigee", size=26, color=MUTED).move_to([XR, WORK_Y - .8, 0])
        with self.say("Now build the perifocal frame from these two vectors. p hat is the eccentricity vector divided by its length.") as d:
            self.play(FadeIn(earth), FadeIn(ax), Create(orb), run_time=.2 * d)
            self.play(Write(d_p), grow(a_p), FadeIn(l_p), run_time=.16 * d)
            self.play(*morph(d_p, s_p, [(0, 0), (1, 1), (3, 9)]), run_time=.16 * d)
            self.wait(.12 * d)
            self.play(*morph(s_p, n_p, [(0, 0), (1, 1), (2, 2), (4, 4), (6, 6), (8, 8)]), run_time=.16 * d)
            self.play(FadeIn(w_p), run_time=.1 * d)
            self.wait(.1 * d)
        self.play(n_p.animate.move_to([XR, STACK_Y[0], 0]), FadeOut(w_p), run_time=.8)

        # ---- h-hat
        d_h = E(r"\hat h|=|\vec h|\,/\,|h", size=44).move_to(work)
        s_h = div_line(r"\hat h", [r"35{,}432", r"50{,}602", r"30{,}934"], r"69{,}086", LILAC).move_to(work)
        n_h = vec_line(r"\hat h", ROWS[2], LILAC).move_to(work)
        w_h = T("normal to the orbit plane", size=26, color=MUTED).move_to([XR, WORK_Y - .8, 0])
        with self.say("h hat is h divided by its length.") as d:
            self.play(Write(d_h), grow(a_h), FadeIn(l_h), run_time=.3 * d)
            self.play(*morph(d_h, s_h, [(0, 0), (1, 1), (3, 9)]), run_time=.3 * d)
            self.wait(.4 * d)
        self.play(*morph(s_h, n_h, [(0, 0), (1, 1), (2, 2), (4, 4), (6, 6), (8, 8)]), FadeIn(w_h), run_time=1.0)
        self.wait(.8)
        self.play(n_h.animate.move_to([XR, STACK_Y[1], 0]), FadeOut(w_h), run_time=.8)

        # ---- q-hat, one component at a time
        d_q = E(r"\hat q|=|\hat h|\times|\hat p", size=44).move_to([XR, WORK_Y + .1, 0])
        comp_src = [(r"q_x", "0.7324(-0.8942)", "0.4478(0.3668)", r"=|-0.8192"),
                    (r"q_y", "0.4478(0.2568)", "0.5129(-0.8942)", r"=|0.5736"),
                    (r"q_z", "0.5129(0.3668)", "0.7324(0.2568)", r"\approx|0")]
        comps, results = VGroup(), VGroup()
        for n, (lab, a, b, res) in enumerate(comp_src):
            y = WORK_Y - 1.0 - .95 * n
            c = E(lab + "|=|" + a + "|-|" + b, size=40)
            c.move_to([0, y, 0]).align_to([LEFT_X, 0, 0], LEFT)
            r = E(lab + "|" + res, size=40)
            r[2].set_color(LIME)
            r.move_to([0, y, 0]).align_to([LEFT_X, 0, 0], LEFT)
            comps.add(c)
            results.add(r)
        w_q = T("q_z is zero up to rounding", size=26, color=MUTED).next_to(results[2], RIGHT, buff=.5)
        n_q = vec_line(r"\hat q", ROWS[1], LIME).move_to([XR, STACK_Y[2], 0])
        with self.say("And q hat completes the right handed set: h hat cross p hat.") as d:
            self.play(Write(d_q), grow(a_q), FadeIn(l_q), run_time=.25 * d)
            for c in comps:
                self.play(Write(c), run_time=.22 * d)
            self.wait(.09 * d)
        self.play(*[a for c, r in zip(comps, results) for a in morph(c, r, [(0, 0), (1, 1)])], FadeIn(w_q),
                  run_time=1.0)
        self.snap("q components")
        self.wait(.7)
        self.play(ReplacementTransform(d_q[0], n_q[0]), FadeOut(d_q[1:]), FadeOut(w_q),
                  *[ReplacementTransform(r[2], n_q[k]) for r, k in zip(results, (3, 5, 7))],
                  *[FadeOut(r[:2]) for r in results],
                  *[FadeIn(n_q[k]) for k in (1, 2, 4, 6, 8)], run_time=1.2)

        # ---- stack the rows into C_PN
        # hand-built matrix: right-aligned columns so the minus signs never touch a neighbor
        cells = VGroup(*[M(x, size=40, color=col) for row, col in zip(ROWS, (ROSE, LIME, LILAC)) for x in row])
        cells.arrange_in_grid(rows=3, cols=3, buff=(.45, .38), col_alignments="rrr")
        ent = [cells[3 * r:3 * r + 3] for r in range(3)]

        def bracket(side):
            hgt, tick = cells.height + .3, .14
            x = cells.get_left()[0] - .2 if side < 0 else cells.get_right()[0] + .2
            y0, y1 = cells.get_center()[1] - hgt / 2, cells.get_center()[1] + hgt / 2
            pts = [[x - side * tick, y1, 0], [x, y1, 0], [x, y0, 0], [x - side * tick, y0, 0]]
            return VMobject(stroke_color=INK, stroke_width=3).set_points_as_corners(pts)

        brackets = VGroup(bracket(-1), bracket(1))
        mat = VGroup(cells, brackets)
        lhs = M(r"C_{PN}", "=", size=44)
        grp = VGroup(lhs, mat).arrange(RIGHT, buff=.25)
        grp.move_to([XR, 1.4, 0])
        moves = []
        for line, r in ((n_p, 0), (n_q, 1), (n_h, 2)):
            for j, k in enumerate((3, 5, 7)):
                moves.append(ReplacementTransform(line[k], ent[r][j]))
            moves.append(line[0].animate.move_to(lhs[0]).set_opacity(0))   # the three hats merge into C_PN
            moves += [FadeOut(line[k]) for k in (1, 2, 4, 6, 8)]
        self.beat("Stack them as rows, and that's C P N, with real numbers in it.",
                  moves,
                  [FadeIn(lhs), FadeIn(brackets)], .2, w=(.55, .25))

        # ---- the corner entry and the inclination
        c33 = ent[2][2]
        box = SurroundingRectangle(c33, color=EMBER, buff=.1)
        eq1 = E(r"\cos|i|=|C_{33}|=|0.4478", size=44).move_to([XR, -1.1, 0])
        eq2 = E(r"i|=|\arccos(0.4478)|=|63.4^\circ", size=44).move_to([XR, -2.5, 0])
        eq2[4].set_color(EMBER)
        arc = arc3(view, ARC_AXIS, K_HAT, INC, 2.0, EMBER)
        l_i = label3(view, "i", 2.4 * ARC_MID, EMBER, 40)
        with self.say("The corner entry is zero point four four seven eight. Its arc cosine is the inclination: sixty three point four degrees.") as d:
            self.play(Create(box), Indicate(c33, color=EMBER), run_time=.18 * d)
            self.play(Write(eq1), run_time=.2 * d)
            self.wait(.1 * d)
            self.play(Write(eq2), run_time=.2 * d)
            self.play(grow(arc), FadeIn(l_i), run_time=.17 * d)
            self.play(FadeIn(glow(eq2[4], EMBER)), Indicate(a_h), run_time=.15 * d)
        self.wipe()
