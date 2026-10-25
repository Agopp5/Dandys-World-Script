"""S16: solve the two-cell box for its shear flows (BRIEF.md S16)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

# ---- facts (HW P2, per unit torque, T in N mm) ----
A_I, A_II = 232_000, 258_000
d_I, d_II, d_25 = 1969.0, 3527.8, 199.8
assert np.isclose(156.3 + 2 * 806.4 + 199.8, d_I, atol=0.15)  # brief deltas are rounded
assert np.isclose(165.6 + 2 * 1581.2 + 199.8, d_II, atol=0.05)
# cross multiply: A_II (d_I q_I - d_25 q_II) = A_I (-d_25 q_I + d_II q_II)
cI = A_II * d_I + A_I * d_25            # coefficient of q_I
cII = A_I * d_II + A_II * d_25          # coefficient of q_II
assert np.isclose(A_II * d_I / 1e6, 508.00, atol=0.005) and np.isclose(A_I * d_25 / 1e6, 46.35, atol=0.005)
assert np.isclose(A_I * d_II / 1e6, 818.45, atol=0.005) and np.isclose(A_II * d_25 / 1e6, 51.55, atol=0.005)
assert np.isclose(cI / 1e6, 554.4, atol=0.05) and np.isclose(cII / 1e6, 870.0, atol=0.05)
ratio = cII / cI
assert np.isclose(ratio, 1.569, atol=5e-4) and np.isclose(ratio, 1.5694, atol=5e-5)
assert np.isclose(2 * A_I * 1.5694, 728_200, atol=5) and np.isclose(2 * A_II, 516_000)
k = 2 * A_I * ratio + 2 * A_II
assert np.isclose(k / 1e6, 1.244, atol=5e-4) and np.isclose(728_200 + 516_000, 1_244_200)
qII = 1 / k
qI = ratio * qII
assert np.isclose(qII * 1e6, 0.804, atol=5e-4) and np.isclose(qI * 1e6, 1.261, atol=5e-4)
# per 1 kN m = 1e6 N mm
assert np.isclose(qI * 1e6, 1.26, atol=5e-3) and np.isclose(qII * 1e6, 0.80, atol=5e-3)
assert np.isclose((qI - qII) * 1e6, 0.46, atol=5e-3) and np.isclose(1.26 - 0.80, 0.46)


def frac(num, den, size=44):
    """A fraction built from two E()'s, so the colored q's survive."""
    n, d = E(num, size=size), E(den, size=size)
    bar = Line(LEFT, RIGHT, stroke_width=3, color=INK).set_width(max(n.width, d.width) + 0.2)
    return VGroup(n, bar, d).arrange(DOWN, buff=0.16)


def note(s, size=28):
    return TX(s, size=size, color=MUTED)


def boxed(m, color):
    return VGroup(m, SurroundingRectangle(m, color=color, buff=0.18, stroke_width=3))


def cell_center(sec, names):
    return np.mean([sec.p(n) for n in names], axis=0)


class S16_P2_Solve(VScene):
    budget = 177

    def construct(self):
        # ---- the box (small, top-left) and its data card ----
        sec = hw_twocell(width=7.0, center=(-3.0, 2.45))
        walls = sec.draw()
        cI0, cII0 = cell_center(sec, [1, 2, 5, 6]), cell_center(sec, [2, 3, 4, 5])
        labI = T("I", size=40, color=MINT, weight=BOLD).move_to(cI0)
        labII = T("II", size=40, color=LIME, weight=BOLD).move_to(cII0)
        card = VGroup(
            E(r"A_I = 232\,000\ \text{mm}^2", size=32),
            E(r"A_{II} = 258\,000\ \text{mm}^2", size=32),
            E(r"\delta_I = 1969.0,\ \ \delta_{II} = 3527.8", size=32, cmap={r"\delta_I": ACCENT}),
            E(r"\delta_{25} = 199.8\ \text{(spar)}", size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for row in card[2:]:
            row.set_color(ACCENT)
        card = panel(card).move_to([4.3, 2.45, 0])
        self.add(walls, labI, labII, card)

        # ---- beat 1: the equal-twist equation ----
        f1 = frac(r"1969.0\,|q_I|-|199.8\,|q_{II}", r"2\,(232\,000)")
        f2 = frac(r"-199.8\,|q_I|+|3527.8\,|q_{II}", r"2\,(258\,000)")
        eq1 = VGroup(f1, E("=", size=44), f2).arrange(RIGHT, buff=0.35).move_to([0, -0.15, 0])
        tagI = T("cell I", size=28, color=MINT).next_to(f1, DOWN, buff=0.3)
        tagII = T("cell II", size=28, color=LIME).next_to(f2, DOWN, buff=0.3)
        n1 = note(r"each side is $G_{\rm REF}\,d\theta/dz$ of one cell: every cell twists the same",
                  size=28).move_to([0, -2.6, 0])
        self.beat("Equal twist: q one times nineteen sixty nine, minus q two times one ninety nine point eight, over two times two thirty two thousand, equals the same for cell two.",
                  Write(f1), [FadeIn(tagI), Indicate(card[1][0]), Indicate(labI)],
                  [Write(eq1[1]), Write(f2)], [FadeIn(tagII), Indicate(labII)], FadeIn(n1),
                  w=(.25, .15, .25, .15, .2))

        # ---- beat 2: cross multiply and collect ----
        lA = E(r"258\,000\,(1969.0\,|q_I|-|199.8\,|q_{II}|)|=|232\,000\,(-199.8\,|q_I|+|3527.8\,|q_{II}|)",
               size=40).move_to([0, 0.55, 0])
        nA = note(r"cross multiply: each side times the other cell's area (the 2s cancel)").next_to(lA, DOWN, buff=0.22)
        lB = E(r"(508.00 + 46.35)\times 10^{6}\,|q_I|=|(818.45 + 51.55)\times 10^{6}\,|q_{II}",
               size=40).move_to([0, -0.95, 0])
        nB = note(r"expand both brackets; every $q_I$ term to the left, every $q_{II}$ term to the right"
                  ).next_to(lB, DOWN, buff=0.22)
        lC = E(r"554.4\times 10^{6}\,|q_I|=|870.0\times 10^{6}\,|q_{II}", size=40)
        arr = E(r"\Longrightarrow", size=40)
        lD = boxed(E(r"q_I|=|1.569\,|q_{II}", size=44), MINT)
        rowC = VGroup(lC, arr, lD).arrange(RIGHT, buff=0.45).move_to([0, -2.5, 0])
        nC = note(r"divide both sides by $554.4\times 10^{6}$").next_to(lD, DOWN, buff=0.22)
        self.beat("Cross multiply and collect. That leaves five fifty four million q one equals eight hundred seventy million q two. So q one is one point five seven times q two.",
                  [FadeOut(tagI), FadeOut(tagII), FadeOut(n1), FadeTransform(eq1, lA)], FadeIn(nA),
                  [Write(lB), FadeIn(nB)], Write(lC), [Write(arr), Write(lD[0])],
                  [Create(lD[1]), FadeIn(nC)], w=(.15, .07, .2, .25, .18, .15))

        # ---- beat 3: the torque equation ----
        lDt = lD.copy().move_to([0, 0, 0]).to_edge(LEFT, buff=0.8).set_y(0.55)
        nDt = note(r"from equal twist").next_to(lDt, RIGHT, buff=0.35)
        t1 = E(r"T|=|2\,(232\,000)\,|q_I|+|2\,(258\,000)\,|q_{II}", size=40).move_to([0, -0.55, 0])
        nt1 = note(r"torque of the cells: $T = \sum 2A_R\,q_R$").next_to(t1, DOWN, buff=0.2)
        t2 = E(r"T|=|2\,(232\,000)(1.5694\,|q_{II}|)|+|516\,000\,|q_{II}", size=40).move_to([0, -1.75, 0])
        nt2 = note(r"substitute $q_I = 1.5694\,q_{II}$ (one more digit, so the rounding doesn't build up)"
                   ).next_to(t2, DOWN, buff=0.2)
        t3 = boxed(E(r"T|=|(728\,200 + 516\,000)\,|q_{II}|=|1.244\times 10^{6}\,|q_{II}", size=40), LILAC)
        t3.move_to([0, -3.15, 0])
        self.beat("Now the torque equation. T equals two times two thirty two thousand q one, plus two times two fifty eight thousand q two. Substituting, that's one point two four four million q two.",
                  [FadeOut(lA), FadeOut(nA), FadeOut(lB), FadeOut(nB), FadeOut(lC), FadeOut(arr), FadeOut(nC),
                   lD.animate.move_to(lDt)], FadeIn(nDt),
                  Write(t1), FadeIn(nt1), [Write(t2), FadeIn(nt2)], Write(t3[0]), Create(t3[1]),
                  w=(.12, .05, .25, .08, .22, .2, .08))

        # ---- beat 4: the two flows per unit torque ----
        t3t = t3.copy().move_to([0, 0.5, 0])
        q2 = boxed(E(r"q_{II}|=|\dfrac{T}{1.244\times 10^{6}}|=|0.804\times 10^{-6}\,|T", size=44), LIME)
        q1 = boxed(E(r"q_I|=|1.5694\,|q_{II}|=|1.261\times 10^{-6}\,|T", size=44), MINT)
        res = VGroup(q2, q1).arrange(DOWN, buff=0.4).move_to([0, -1.55, 0])
        nq = note(r"$T$ in N mm, so each $q$ comes out in N/mm", size=28).next_to(res, DOWN, buff=0.25)
        self.beat("So q two is zero point eight zero four times ten to the minus six, T. And q one is one point two six one times ten to the minus six, T.",
                  [FadeOut(t1), FadeOut(nt1), FadeOut(t2), FadeOut(nt2), FadeOut(lD), FadeOut(nDt),
                   t3.animate.move_to(t3t)],
                  Write(q2[0]), Create(q2[1]), Write(q1[0]), [Create(q1[1]), FadeIn(nq)],
                  w=(.12, .35, .08, .35, .1))

        # ---- beat 5: one kilonewton meter, drawn on the box ----
        big = hw_twocell(width=12.8, center=(0, 1.1))
        walls2 = big.draw()
        cI, cII = cell_center(big, [1, 2, 5, 6]), cell_center(big, [2, 3, 4, 5])
        arrI = VGroup(*[flow(big, a, b, 1.26, color=MINT) for a, b in [(1, 2), (5, 6), (6, 1)]])
        arrII = VGroup(*[flow(big, a, b, 0.80, color=LIME) for a, b in [(2, 3), (3, 4), (4, 5)]])
        cfI = cell_flow(cI + LEFT * 0.9, radius=0.42, color=MINT, ccw=True)
        cfII = cell_flow(cII + LEFT * 0.6, radius=0.42, color=LIME, ccw=True)
        vI = E(r"q_I = 1.26", size=40).next_to(cfI, RIGHT, buff=0.25)
        vII = E(r"q_{II} = 0.80", size=40).next_to(cfII, RIGHT, buff=0.25)
        spar = flow(big, 2, 5, 0.46, color=GOLD)
        vS = E(r"0.46", size=40, color=GOLD).next_to(spar, RIGHT, buff=0.15)
        tq = torque([-5.2, -2.0, 0], radius=0.5, color=LILAC, ccw=True, label=None)
        r1 = E(r"T|=|1\ \text{kN m}|=|10^{6}\ \text{N mm}", size=40).next_to(tq, RIGHT, buff=0.4)
        r2 = E(r"q_I|-|q_{II}|=|1.26|-|0.80|=|0.46\ \text{N/mm}", size=40)
        paint(r2, {0: MINT, 2: LIME, 4: MINT, 6: LIME, 8: GOLD})
        r2.move_to([0, -3.2, 0]).set_x(r1.get_center()[0] - 0.3)
        nS = note(r"the spar's share", size=28).next_to(r2, RIGHT, buff=0.35)
        self.beat("For a torque of one kilonewton meter: one point two six in cell one, zero point eight zero in cell two, and the spar carries the difference, zero point four six newtons per millimeter.",
                  [FadeOut(card), FadeOut(labI), FadeOut(labII), FadeOut(t3),
                   FadeOut(q1), FadeOut(q2), FadeOut(nq), ReplacementTransform(walls, walls2)],
                  [Create(tq), Write(r1)],
                  [LaggedStart(*[GrowArrow(a) if isinstance(a, Arrow) else FadeIn(a) for a in arrI]),
                   Create(cfI), Write(vI)],
                  [LaggedStart(*[FadeIn(a) for a in arrII]), Create(cfII), Write(vII)],
                  [FadeIn(spar), Write(vS), Write(r2), FadeIn(nS)],
                  w=(.15, .2, .22, .2, .23))

        # ---- beat 6: your turn ----
        self.beat("Your turn. Pause here and do checkpoint five point one: a two cell box with a real torque.",
                  Circumscribe(VGroup(vI, vII), color=ACCENT), Indicate(vS, color=GOLD), w=(.5, .5))
        self.checkpoint("5.1", "Practice two-cell box: T = 15 kN m")
        self.wipe()
