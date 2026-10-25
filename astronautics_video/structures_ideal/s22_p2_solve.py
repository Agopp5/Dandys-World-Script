"""S22: solve the two-cell box for its shear flows (BRIEF.md S22). Rework of old/s16_p2_solve.py."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# ---- facts (HW P2, per unit torque, T in N mm) ----
A_I, A_II = 232_000, 258_000
d_I, d_II, d_25 = 1969.0, 3527.8, 199.8
assert np.isclose(156.3 + 2 * 806.4 + 199.8, d_I, atol=0.15)  # brief deltas are rounded
assert np.isclose(165.6 + 2 * 1581.2 + 199.8, d_II, atol=0.05)
# cross multiply: A_II (d_I q_I - d_25 q_II) = A_I (-d_25 q_I + d_II q_II)
cI = A_II * d_I + A_I * d_25            # coefficient of q_I
cII = A_I * d_II + A_II * d_25          # coefficient of q_II
assert np.isclose(cI / 1e6, 554.4, atol=0.05) and np.isclose(cII / 1e6, 870.0, atol=0.05)
ratio = cII / cI
assert np.isclose(ratio, 1.569, atol=5e-4) and np.isclose(ratio, 1.5694, atol=5e-5)
assert np.isclose(round(ratio, 2), 1.57)
assert np.isclose(2 * A_I * 1.5694, 728_200, atol=5) and np.isclose(2 * A_II, 516_000)
k = 2 * A_I * ratio + 2 * A_II
assert np.isclose(k / 1e6, 1.244, atol=5e-4) and np.isclose(728_200 + 516_000, 1_244_200)
qII = 1 / k
qI = ratio * qII
assert np.isclose(qII * 1e6, 0.804, atol=5e-4) and np.isclose(qI * 1e6, 1.261, atol=5e-4)
# per 1 kN m = 1e6 N mm
assert np.isclose(qI * 1e6, 1.26, atol=5e-3) and np.isclose(qII * 1e6, 0.80, atol=5e-3)
assert np.isclose((qI - qII) * 1e6, 0.46, atol=5e-3) and np.isclose(1.26 - 0.80, 0.46)


def frac(num, den, size=48):
    """A fraction built from two E()'s, so the colored q's survive."""
    n, d = E(num, size=size), E(den, size=size)
    bar = Line(LEFT, RIGHT, stroke_width=3, color=INK).set_width(max(n.width, d.width) + 0.2)
    return VGroup(n, bar, d).arrange(DOWN, buff=0.16)


def note(s, size=30):
    return TX(s, size=size, color=MUTED)


def boxed(m, color):
    return VGroup(m, SurroundingRectangle(m, color=color, buff=0.2, stroke_width=3))


def cell_center(sec, names):
    return np.mean([sec.p(n) for n in names], axis=0)


def ccw_arc(center, radius=0.55, color=MINT):
    """A circular arrow that unmistakably turns counterclockwise (positive angle; head at the top pointing left)."""
    arc = Arc(radius=radius, start_angle=-PI, angle=1.5 * PI, color=color, stroke_width=6)
    arc.add_tip(tip_length=0.3, tip_width=0.3)
    arc.get_tip().set_fill(color, 1).set_stroke(color, 1)
    return arc.move_to(center)


class S22_P2_Solve(VScene):
    budget = 222

    def construct(self):
        # ---- data card across the top ----
        colA = VGroup(E(r"A_I = 232\,000\ \text{mm}^2", size=38),
                      E(r"A_{II} = 258\,000\ \text{mm}^2", size=38)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        colD = VGroup(E(r"\delta_I = 1969.0,\ \ \delta_{II} = 3527.8", size=38, color=ACCENT),
                      E(r"\delta_{25} = 199.8\ \text{(spar)}", size=38, color=ACCENT)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        card = panel(VGroup(colA, colD).arrange(RIGHT, buff=0.9, aligned_edge=UP))
        card.to_edge(UP, buff=0.25)
        self.add(card)

        # ---- beat 1: cell one's rate of twist ----
        f1 = frac(r"1969.0\,|q_I|-|199.8\,|q_{II}", r"2\,(232\,000)")
        f2 = frac(r"-199.8\,|q_I|+|3527.8\,|q_{II}", r"2\,(258\,000)")
        eqs = E("=", size=48)
        eq1 = VGroup(f1, eqs, f2).arrange(RIGHT, buff=0.35).move_to([0, -0.2, 0])
        tagI = T("cell I's twist rate", size=34, color=MINT).next_to(f1, DOWN, buff=0.4)
        tagII = T("cell II's twist rate", size=34, color=LIME).next_to(f2, DOWN, buff=0.4)
        n1 = note(r"each side is $G_{\rm REF}\,d\theta/dz$ of one cell: every cell twists the same").move_to([0, -3.1, 0])
        self.beat("First equation, equal twist. Cell one's rate: q one times nineteen sixty nine, minus q two times one ninety nine point eight, over two times two hundred thirty two thousand.",
                  .1, [Write(f1[0][0]), Write(f1[0][1]), Indicate(colD[0])],
                  [Write(f1[0][2:]), Indicate(colD[1])],
                  [Create(f1[1]), Write(f1[2]), Indicate(colA[0])], FadeIn(tagI), .18,
                  w=(.25, .22, .2, .08))

        # ---- beat 2: equals cell two's rate ----
        self.beat("That must equal cell two's rate: minus q one times one ninety nine point eight, plus q two times thirty five twenty eight, over two times two hundred fifty eight thousand.",
                  Write(eqs), [Write(f2[0][:2]), Indicate(colD[1])], [Write(f2[0][2:]), Indicate(colD[0])],
                  [Create(f2[1]), Write(f2[2]), Indicate(colA[1])], [FadeIn(tagII), FadeIn(n1)], .2,
                  w=(.1, .2, .2, .2, .1))

        # ---- beat 3: cross multiply and collect ----
        lA = E(r"258\,000\,(1969.0\,|q_I|-|199.8\,|q_{II}|)|=|232\,000\,(-199.8\,|q_I|+|3527.8\,|q_{II}|)",
               size=44)
        fit(lA, 13.4, 1)
        lA.move_to([0, 1.2, 0])
        nA = note(r"cross multiply: each side times the other cell's area (the 2s cancel)").next_to(lA, DOWN, buff=0.25)
        lC = E(r"554.4\times 10^{6}\,|q_I|=|870.0\times 10^{6}\,|q_{II}", size=50).move_to([0, -0.75, 0])
        nC = note(r"collect: every $q_I$ term to the left, every $q_{II}$ term to the right").next_to(lC, DOWN, buff=0.25)
        lD = boxed(E(r"q_I|=|1.569\,|q_{II}", size=54), MINT).move_to([0, -2.85, 0])
        self.beat("Cross multiply and collect. Five hundred fifty four million q one equals eight hundred seventy million q two. So q one is one point five seven times q two.",
                  [FadeOut(tagI), FadeOut(tagII), FadeOut(n1), FadeTransform(eq1, lA)], FadeIn(nA), .06,
                  [Write(lC), FadeIn(nC)], .1, Write(lD[0]), Create(lD[1]), .18,
                  w=(.14, .06, .24, .16, .06))

        # ---- beat 4: the torque equation ----
        lDt = lD.copy().scale(0.9).move_to([-4.2, 1.15, 0])
        nDt = note(r"from equal twist").next_to(lDt, RIGHT, buff=0.4)
        t1 = E(r"T|=|2\,(232\,000)\,|q_I|+|2\,(258\,000)\,|q_{II}", size=50).move_to([0, -0.35, 0])
        nt1 = note(r"torque of the cells: $T = \sum 2A_R\,q_R$").next_to(t1, DOWN, buff=0.25)
        self.beat("Second equation, the torque. T equals two times two hundred thirty two thousand times q one, plus two times two hundred fifty eight thousand times q two.",
                  [FadeOut(lA), FadeOut(nA), FadeOut(lC), FadeOut(nC), Transform(lD, lDt)], FadeIn(nDt),
                  [Write(t1[0:2]), FadeIn(nt1)], [Write(t1[2:4]), Indicate(colA[0])],
                  [Write(t1[4:]), Indicate(colA[1])], .2,
                  w=(.12, .06, .2, .22, .22))

        # ---- beat 5: substitute ----
        t2 = E(r"T|=|(728\,200|+|516\,000)\,|q_{II}", size=50).move_to([0, -1.75, 0])
        nt2 = note(r"$2\,(232\,000)(1.5694) = 728\,200$ (one more digit, so rounding doesn't build up)",
                   size=30).next_to(t2, DOWN, buff=0.22)
        t3 = boxed(E(r"T|=|1.244\times 10^{6}\,|q_{II}", size=54), LILAC).move_to([0, -3.35, 0])
        self.beat("Substitute q one. That gives T equals one point two four four million times q two.",
                  [Indicate(lD, color=MINT), Indicate(t1[2], color=MINT), FadeOut(nt1)], [Write(t2), FadeIn(nt2)],
                  .08, Write(t3[0]), Create(t3[1]), .15, w=(.14, .3, .25, .08))
        self.wait(1.0)

        # ---- beat 6: the two flows per unit torque ----
        q2 = boxed(E(r"q_{II}|=|\dfrac{T}{1.244\times 10^{6}}|=|0.804\times 10^{-6}\,|T", size=50), LIME)
        q1 = boxed(E(r"q_I|=|1.5694\,|q_{II}|=|1.261\times 10^{-6}\,|T", size=50), MINT)
        res = VGroup(q2, q1).arrange(DOWN, buff=0.45).move_to([0, -0.85, 0])
        nq = note(r"$T$ in N mm, so each $q$ comes out in N/mm").next_to(res, DOWN, buff=0.3)
        self.beat("So q two is zero point eight zero four times ten to the minus six, T. And q one is one point two six one times ten to the minus six, T, with T in newton millimeters.",
                  [FadeOut(t1), FadeOut(t2), FadeOut(lD), FadeOut(nDt), FadeOut(t3)],
                  Write(q2[0]), Create(q2[1]), .1, Write(q1[0]), Create(q1[1]), FadeIn(nq), .15,
                  w=(.08, .26, .06, .26, .06, .08))

        # ---- beat 7: one kilonewton meter, drawn on the box ----
        big = hw_twocell(width=12.8, center=(0, 1.0))
        walls2 = big.draw()
        cI0, cII0 = cell_center(big, [1, 2, 5, 6]), cell_center(big, [2, 3, 4, 5])
        arrI = VGroup(*[flow(big, a, b, 1.26, color=MINT) for a, b in [(1, 2), (5, 6), (6, 1)]])
        arrII = VGroup(*[flow(big, a, b, 0.80, color=LIME) for a, b in [(2, 3), (3, 4), (4, 5)]])
        cfI = ccw_arc(cI0 + LEFT * 1.2, color=MINT)
        cfII = ccw_arc(cII0 + LEFT * 1.0, color=LIME)
        vI = E(r"q_I = 1.26", size=44).next_to(cfI, RIGHT, buff=0.25)
        vII = E(r"q_{II} = 0.80", size=44).next_to(cfII, RIGHT, buff=0.25)
        spar = flow(big, 2, 5, 0.46, color=GOLD)
        vS = E(r"0.46", size=44, color=GOLD).next_to(spar, RIGHT, buff=0.12)
        tq = ccw_arc([-5.7, -2.2, 0], radius=0.45, color=LILAC)
        r1 = E(r"T|=|1\ \text{kN m}|=|10^{6}\ \text{N mm}", size=46).next_to(tq, RIGHT, buff=0.35)
        r2 = E(r"q_I|-|q_{II}|=|1.26|-|0.80|=|0.46\ \text{N/mm}", size=46)
        paint(r2, {0: MINT, 2: LIME, 4: MINT, 6: LIME, 8: GOLD})
        r2.move_to([-0.9, -3.3, 0])
        nS = note(r"the spar's share").next_to(r2, RIGHT, buff=0.35)
        self.beat("For a torque of one kilonewton meter: one point two six in cell one, zero point eight zero in cell two, and the spar carries the difference, zero point four six newtons per millimeter.",
                  [FadeOut(card), FadeOut(q1), FadeOut(q2), FadeOut(nq), Create(walls2)],
                  [Create(tq), Write(r1)], .05,
                  [LaggedStart(*[FadeIn(a) for a in arrI]), Create(cfI), Write(vI)], .05,
                  [LaggedStart(*[FadeIn(a) for a in arrII]), Create(cfII), Write(vII)], .05,
                  [FadeIn(spar), Write(vS), Write(r2), FadeIn(nS)], .1,
                  w=(.12, .15, .18, .17, .19))

        # ---- beat 8: your turn ----
        self.beat("Your turn. Pause here and do checkpoint six point one: a two cell box with a real torque.",
                  Circumscribe(VGroup(vI, vII), color=ACCENT), Indicate(vS, color=GOLD), .2, w=(.4, .4))
        self.checkpoint("6.1", "Practice two-cell box: T = 15 kN m")
        self.wipe()
