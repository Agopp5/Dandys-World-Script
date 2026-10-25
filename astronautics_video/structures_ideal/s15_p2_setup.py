"""S15: set up the HW P2 two-cell box (BRIEF.md S15)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

# facts: HW P2 data (lengths mm, thicknesses mm, G in N/mm^2)
G_REF, G_SKIN = 27600, 24200
RATIO = G_SKIN / G_REF
assert np.isclose(RATIO, 0.8768, atol=5e-5)
WALLS = [  # label, length, t, G
    (r"16", 254, 1.625, G_REF),
    (r"25", 406, 2.032, G_REF),
    (r"34", 202, 1.220, G_REF),
    (r"12,\ 56", 647, 0.915, G_SKIN),
    (r"23,\ 45", 775, 0.559, G_SKIN),
]
TSTAR = [t * G / G_REF for _, _, t, G in WALLS]
DELTA = [L / ts for (_, L, _, _), ts in zip(WALLS, TSTAR)]
TSTAR_S = ["1.625", "2.032", "1.220", "0.8023", "0.4901"]
DELTA_S = ["156.3", "199.8", "165.6", "806.4", "1581.2"]
for v, s in zip(TSTAR, TSTAR_S):
    assert abs(v - float(s)) < 6e-5
for v, s in zip(DELTA, DELTA_S):
    assert abs(v - float(s)) < 0.051
d16, d25, d34, d12, d23 = DELTA
dI, dII = d16 + 2 * d12 + d25, d34 + 2 * d23 + d25
assert abs(dI - 1969.0) < 0.06 and abs(dII - 3527.8) < 0.06
# the rounded table entries sum to 1968.9 / 3527.8; the exact sums (above) round to 1969.0 / 3527.8
assert abs(156.3 + 2 * 806.4 + 199.8 - 1969.0) < .15 and np.isclose(165.6 + 2 * 1581.2 + 199.8, 3527.8)

X4 = [-6.0, -4.1, -2.0, 0.1]          # four table columns
ROWS_Y = [-0.22, -0.92, -1.62, -2.32, -3.02, -3.72]
BOOMS = {1: 1290, 6: 1290, 2: 1936, 5: 1936, 3: 645, 4: 645}   # HW P2 boom areas, mm^2 (irrelevant in torsion)
DCM = {r"\delta_I": ACCENT, r"\delta_{II}": ACCENT, r"\delta_{25}": ACCENT, r"\delta_{16}": ACCENT,
       r"G_{\mathrm{ref}}": ACCENT, r"t^*": ACCENT}
NUM, HEAD = 38, 34


def at(m, c, r):
    return m.move_to([X4[c], ROWS_Y[r], 0])


class S15_P2_Setup(VScene):
    budget = 107

    def construct(self):
        head = self.section("HW P2: the two-cell box")

        # ---- the section, top of the frame
        sec = hw_twocell()
        sec = Section(sec.pts, sec.walls, width=8.0, center=(-1.8, 1.97))
        walls = sec.draw()
        booms = sec.booms(BOOMS)
        names = sec.names()
        cI = (sec.p(1) + sec.p(6) + sec.p(2) + sec.p(5)) / 4
        cII = (sec.p(2) + sec.p(5) + sec.p(3) + sec.p(4)) / 4
        labI = M(r"\mathrm{I}", size=48, color=MINT).move_to(cI)
        labII = M(r"\mathrm{II}", size=48, color=LIME).move_to(cII)
        tq = torque(np.array([5.4, 2.35, 0]), radius=0.6, color=LILAC, ccw=True, label="T")
        note1 = VGroup(TX(r"$T$ not given:", size=34), TX(r"solve per unit $T$", size=34)).arrange(DOWN, buff=.15)
        note1.move_to([5.4, 1.0, 0])

        self.beat("Here's the two cell wing box. The torque is counterclockwise, but the problem doesn't give its size, so we'll find each shear flow per unit of torque.",
                  [Create(walls), FadeIn(booms), FadeIn(names)], [FadeIn(labI), FadeIn(labII)],
                  Create(tq), .1, FadeIn(note1, shift=UP * .2), w=(.3, .15, .25, .2))

        # ---- boom areas from the HW table: irrelevant in pure torsion
        bt = T("boom areas from the HW table", size=30, color=INK2)
        blines = VGroup(E(r"B_1|=|B_6|=|1290\ \mathrm{mm^2}", size=40, cmap={"B_6": EMBER}),
                        E(r"B_2|=|B_5|=|1936\ \mathrm{mm^2}", size=40, cmap={"B_5": EMBER}),
                        E(r"B_3|=|B_4|=|645\ \mathrm{mm^2}", size=40, cmap={"B_3": EMBER, "B_4": EMBER}))
        blines.arrange(DOWN, buff=.22, aligned_edge=LEFT)
        bn = T("pure torsion: no direct stress, so the booms carry nothing", size=28, color=MUTED)
        bcard = VGroup(bt, blines, bn).arrange(DOWN, buff=.28)
        fit(bcard, 12.5, 4.0)
        bcard.move_to([-0.3, -1.95, 0])
        sk = VGroup(*[strike(m) for m in blines])
        self.beat("Notice the boom areas in the table. In pure torsion they don't matter at all.",
                  [FadeIn(bt), FadeIn(blines)], Indicate(booms, color=EMBER), [Create(sk), booms.animate.set_opacity(.2)],
                  FadeIn(bn), w=(.2, .25, .3, .25))

        # ---- table 1: wall | t | G | t*
        cells = {}  # (key, r) -> mobject, r = 0..4
        for r, (lab, L, t, G) in enumerate(WALLS):
            cells["w", r] = at(M(lab, size=NUM, color=INK2), 0, r + 1)
            cells["t", r] = at(M(f"{t:.3f}", size=NUM), 1, r + 1)
            cells["G", r] = at(M(r"27\,600" if G == G_REF else r"24\,200", size=NUM), 2, r + 1)
            cells["ts", r] = at(M(TSTAR_S[r], size=NUM, color=ACCENT), 3, r + 1)
            cells["L", r] = at(M(str(L), size=NUM), 1, r + 1)
            cells["d", r] = at(M(DELTA_S[r], size=NUM, color=ACCENT), 3, r + 1)
        col = lambda k: VGroup(*[cells[k, r] for r in range(5)])
        h_w = at(T("wall", size=HEAD, color=INK2), 0, 0)
        h_t = at(M(r"t\ (\mathrm{mm})", size=HEAD), 1, 0)
        h_G = at(M(r"G\ (\mathrm{N/mm^2})", size=HEAD), 2, 0)
        h_ts = at(E(r"t^*|\ (\mathrm{mm})", size=HEAD), 3, 0)
        h_L = at(M(r"L\ (\mathrm{mm})", size=HEAD), 1, 0)
        h_d = at(E(r"\delta", size=HEAD + 6), 3, 0)
        rule = Line([-7.0, ROWS_Y[0] - .36, 0], [1.0, ROWS_Y[0] - .36, 0], color=HAIR, stroke_width=2)
        self.play(FadeOut(VGroup(bcard, sk)), FadeIn(VGroup(h_w, h_t, h_G)), Create(rule),
                  FadeIn(VGroup(col("w"), col("t"), col("G"))), run_time=1.2)

        # ---- reference G and t*
        g1 = E(r"G_{\mathrm{ref}}|=|27\,600", size=44, cmap=DCM)
        gn = T("webs keep their t", size=30, color=MUTED)
        t1 = E(r"t^*|=|\frac{24\,200}{27\,600}\,t", size=44, cmap=DCM)
        t2 = E(r"=|0.8768\,t", size=44)
        tn = T("skins 12, 56, 23, 45", size=30, color=MUTED)
        alg = VGroup(g1, gn, t1, t2, tn).arrange(DOWN, buff=.25)
        t2.align_to(t1[1], LEFT)
        fit(alg, 5.0, 4.1)
        alg.move_to([4.3, -1.9, 0])
        webs = VGroup(*[sec.walls_m[k] for k in [(6, 1), (2, 5), (3, 4)]])
        skins = VGroup(*[sec.walls_m[k] for k in [(1, 2), (5, 6), (2, 3), (4, 5)]])
        web_ts = VGroup(*[cells["ts", r] for r in range(3)])
        skin_ts = VGroup(*[cells["ts", r] for r in (3, 4)])
        self.beat("Take the reference G as twenty seven thousand six hundred. The webs keep their thickness. The skins, at twenty four thousand two hundred, are scaled by zero point eight seven seven.",
                  Write(g1), [FadeIn(h_ts), FadeIn(gn), Indicate(webs, color=ACCENT), FadeIn(web_ts)],
                  [Write(t1), Indicate(skins, color=ACCENT)], [Write(t2), FadeIn(skin_ts)], FadeIn(tn),
                  w=(.2, .25, .25, .2, .1))

        # ---- table 2: wall | L | t* | delta
        dl1 = E(r"\delta|=|\int\frac{ds}{t^*}|=|\frac{L}{t^*}", size=44, cmap={r"\int\frac{ds}{t^*}": INK})
        dl2 = E(r"\delta_{16}|=|\frac{254}{1.625}|=|156.3", size=44, cmap=DCM)
        dalg = VGroup(dl1, dl2).arrange(DOWN, buff=.5)
        fit(dalg, 5.0, 3.8)
        dalg.move_to([4.3, -1.9, 0])
        ts_move = VGroup(h_ts, col("ts"))
        self.play(FadeOut(alg), FadeOut(VGroup(h_t, h_G, col("t"), col("G"))),
                  ts_move.animate.shift(LEFT * (X4[3] - X4[2])), run_time=.9)
        self.beat("Now delta for each wall is its length over t star.",
                  [FadeIn(VGroup(h_L, col("L"))), Write(dl1), FadeIn(h_d)], [Write(dl2), FadeIn(cells["d", 0])],
                  LaggedStart(*[FadeIn(cells["d", r]) for r in range(1, 5)], lag_ratio=.3), w=(.35, .35, .3))

        # ---- cell sums: keep wall + delta columns, sums on the right
        dcol = [cells["d", r] for r in range(5)]
        keep_d = VGroup(h_d, *dcol)
        rule2 = Line([-7.0, ROWS_Y[0] - .36, 0], [-3.2, ROWS_Y[0] - .36, 0], color=HAIR, stroke_width=2)
        cI_w = VGroup(*[sec.walls_m[k] for k in [(6, 1), (1, 2), (5, 6)]])
        cII_w = VGroup(*[sec.walls_m[k] for k in [(3, 4), (2, 3), (4, 5)]])
        spar = sec.walls_m[(2, 5)]
        s1 = E(r"\delta_I|=|156.3 + 2(806.4) + 199.8|=|1969.0", size=40, cmap=DCM)
        s1n = T("left web + top and bottom skins + spar", size=28, color=MUTED)
        s2 = E(r"\delta_{II}|=|165.6 + 2(1581.2) + 199.8|=|3527.8", size=40, cmap=DCM)
        s2n = T("right web + top and bottom skins + spar", size=28, color=MUTED)
        s3 = E(r"\delta_{25}|=|199.8", size=40, cmap=DCM)
        s3n = T("the shared spar alone", size=28, color=MUTED)
        sums = VGroup(VGroup(s1, s1n).arrange(DOWN, buff=.12, aligned_edge=LEFT),
                      VGroup(s2, s2n).arrange(DOWN, buff=.12, aligned_edge=LEFT),
                      VGroup(s3, s3n).arrange(DOWN, buff=.12, aligned_edge=LEFT)).arrange(DOWN, buff=.35, aligned_edge=LEFT)
        fit(sums, 9.6, 4.0)
        sums.move_to([2.1, -1.95, 0])
        self.play(FadeOut(dalg), FadeOut(VGroup(h_L, col("L"), ts_move)), ReplacementTransform(rule, rule2),
                  keep_d.animate.shift(LEFT * (X4[3] - X4[1])), run_time=1.2)
        with self.say("Around cell one: one nineteen sixty nine. Around cell two: thirty five twenty eight. The shared spar alone: one ninety nine point eight.") as d:
            self.play(cI_w.animate.set_color(MINT), spar.animate.set_color(GOLD), Write(s1[:2]), run_time=.12 * d)
            self.play(Write(s1[2:]), FadeIn(s1n), Indicate(VGroup(dcol[0], dcol[3], dcol[1]), color=MINT), run_time=.23 * d)
            self.play(cII_w.animate.set_color(LIME), Write(s2[:2]), run_time=.12 * d)
            self.play(Write(s2[2:]), FadeIn(s2n), Indicate(VGroup(dcol[2], dcol[4], dcol[1]), color=LIME), run_time=.23 * d)
            self.play(Write(s3), FadeIn(s3n), Indicate(spar, color=GOLD, scale_factor=1.0), run_time=.2 * d)
            self.wait(.1 * d)
        self.wipe()
