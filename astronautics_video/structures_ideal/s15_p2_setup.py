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

COLS_X = [-6.35, -4.95, -3.55, -1.8, 0.35, 1.85]
ROWS_Y = [-0.75, -1.35, -1.95, -2.55, -3.15, -3.72]
DCM = {r"\delta_I": ACCENT, r"\delta_{II}": ACCENT, r"\delta_{25}": ACCENT, r"\delta_{16}": ACCENT,
       r"G_{\mathrm{ref}}": ACCENT, r"t^*": ACCENT}


class S15_P2_Setup(VScene):
    budget = 107

    def construct(self):
        head = self.section("HW P2: the two-cell box")

        # ---- the section, top of the frame
        sec = hw_twocell()
        sec = Section(sec.pts, sec.walls, width=9.4, center=(-1.2, 1.5))
        walls = sec.draw()
        booms = sec.booms({k: 300 for k in sec.pts})
        names = sec.names()
        cI = (sec.p(1) + sec.p(6) + sec.p(2) + sec.p(5)) / 4
        cII = (sec.p(2) + sec.p(5) + sec.p(3) + sec.p(4)) / 4
        labI = M(r"\mathrm{I}", size=48, color=MINT).move_to(cI)
        labII = M(r"\mathrm{II}", size=48, color=LIME).move_to(cII)
        tq = torque(np.array([5.55, 1.9, 0]), radius=0.6, color=LILAC, ccw=True, label="T")
        note1 = VGroup(TX(r"$T$ not given:", size=34), TX(r"solve per unit $T$", size=34)).arrange(DOWN, buff=.15)
        note1.move_to([5.6, 0.5, 0])

        self.beat("Here's the two cell wing box. The torque is counterclockwise, but the problem doesn't give its size, so we'll find each shear flow per unit of torque.",
                  [Create(walls), FadeIn(booms), FadeIn(names)], [FadeIn(labI), FadeIn(labII)],
                  Create(tq), .1, FadeIn(note1, shift=UP * .2), w=(.3, .15, .25, .2))

        # ---- boom areas: irrelevant in pure torsion
        bt = T("boom areas (HW table)", size=28, color=INK2)
        bl = E(r"B_1,\ B_2,\ \dots,\ B_6", size=44, cmap={r"B_1,\ B_2,\ \dots,\ B_6": EMBER})
        bn = VGroup(T("pure torsion: no direct stress,", size=26, color=MUTED),
                    T("so the booms carry nothing", size=26, color=MUTED)).arrange(DOWN, buff=.12)
        bcard = VGroup(bt, bl, bn).arrange(DOWN, buff=.35)
        fit(bcard, 6.5, 3.2)
        bcard.move_to([0, -2.2, 0])
        sk = strike(bl)
        self.beat("Notice the boom areas in the table. In pure torsion they don't matter at all.",
                  [FadeIn(bt), FadeIn(bl)], Indicate(booms, color=EMBER), [Create(sk), booms.animate.set_opacity(.2)],
                  FadeIn(bn), w=(.2, .25, .3, .25))

        # ---- the HW table (walls)
        hdr = VGroup(T("wall", size=30, color=INK2), M(r"L\ (\mathrm{mm})", size=34), M(r"t\ (\mathrm{mm})", size=34),
                     M(r"G\ (\mathrm{N/mm^2})", size=34), E(r"t^*|\ (\mathrm{mm})", size=34),
                     E(r"\delta", size=40))
        for m, x in zip(hdr, COLS_X):
            m.move_to([x, ROWS_Y[0], 0])
        rule = Line([-7.0, ROWS_Y[0] - .3, 0], [2.5, ROWS_Y[0] - .3, 0], color=HAIR, stroke_width=2)
        cells = []  # cells[r][c]
        for r, (lab, L, t, G) in enumerate(WALLS):
            y = ROWS_Y[r + 1]
            row = [M(lab, size=34, color=INK2), M(str(L), size=34), M(f"{t:.3f}", size=34),
                   M(r"27\,600" if G == G_REF else r"24\,200", size=34),
                   M(TSTAR_S[r], size=34, color=ACCENT), M(DELTA_S[r], size=34, color=ACCENT)]
            for m, x in zip(row, COLS_X):
                m.move_to([x, y, 0])
            cells.append(row)
        given = VGroup(*[m for row in cells for m in row[:4]])
        self.play(FadeOut(VGroup(bcard, sk)), FadeIn(hdr[:4]), Create(rule), FadeIn(given), run_time=1.2)

        # ---- reference G and t*
        g1 = E(r"G_{\mathrm{ref}}|=|27\,600", size=40, cmap=DCM)
        gn = T("webs keep their t", size=28, color=MUTED)
        t1 = E(r"t^*|=|\frac{24\,200}{27\,600}\,t", size=40, cmap=DCM)
        t2 = E(r"=|0.8768\,t", size=40)
        tn = T("skins 12, 56, 23, 45", size=28, color=MUTED)
        alg = VGroup(g1, gn, t1, t2, tn).arrange(DOWN, buff=.22)
        t2.align_to(t1[1], LEFT)
        fit(alg, 4.3, 3.6)
        alg.move_to([4.9, -2.2, 0])
        webs = VGroup(*[sec.walls_m[k] for k in [(6, 1), (2, 5), (3, 4)]])
        skins = VGroup(*[sec.walls_m[k] for k in [(1, 2), (5, 6), (2, 3), (4, 5)]])
        web_ts = VGroup(*[cells[r][4] for r in range(3)])
        skin_ts = VGroup(*[cells[r][4] for r in (3, 4)])
        self.beat("Take the reference G as twenty seven thousand six hundred. The webs keep their thickness. The skins, at twenty four thousand two hundred, are scaled by zero point eight seven seven.",
                  Write(g1), [FadeIn(hdr[4]), FadeIn(gn), Indicate(webs, color=ACCENT), FadeIn(web_ts)],
                  [Write(t1), Indicate(skins, color=ACCENT)], [Write(t2), FadeIn(skin_ts)], FadeIn(tn),
                  w=(.2, .25, .25, .2, .1))

        # ---- delta = L / t*
        dl1 = E(r"\delta|=|\int\frac{ds}{t^*}|=|\frac{L}{t^*}", size=40, cmap={r"\int\frac{ds}{t^*}": INK})
        dl2 = E(r"\delta_{16}|=|\frac{254}{1.625}|=|156.3", size=40, cmap=DCM)
        dalg = VGroup(dl1, dl2).arrange(DOWN, buff=.45)
        fit(dalg, 4.3, 3.4)
        dalg.move_to([4.9, -2.2, 0])
        dcol = [cells[r][5] for r in range(5)]
        self.play(FadeOut(alg), run_time=.6)
        self.beat("Now delta for each wall is its length over t star.",
                  [Write(dl1), FadeIn(hdr[5])], [Write(dl2), FadeIn(dcol[0])],
                  LaggedStart(*[FadeIn(m) for m in dcol[1:]], lag_ratio=.3), w=(.35, .35, .3))

        # ---- cell sums: keep wall + delta columns, sums on the right
        drop_cols = VGroup(*hdr[1:5], *[m for row in cells for m in row[1:5]])
        keep_d = VGroup(hdr[5], *dcol)
        rule2 = Line([-7.0, ROWS_Y[0] - .3, 0], [-3.9, ROWS_Y[0] - .3, 0], color=HAIR, stroke_width=2)
        cI_w = VGroup(*[sec.walls_m[k] for k in [(6, 1), (1, 2), (5, 6)]])
        cII_w = VGroup(*[sec.walls_m[k] for k in [(3, 4), (2, 3), (4, 5)]])
        spar = sec.walls_m[(2, 5)]
        s1 = E(r"\delta_I|=|156.3 + 2(806.4) + 199.8|=|1969.0", size=40, cmap=DCM)
        s1n = T("left web + top and bottom skins + spar", size=26, color=MUTED)
        s2 = E(r"\delta_{II}|=|165.6 + 2(1581.2) + 199.8|=|3527.8", size=40, cmap=DCM)
        s2n = T("right web + top and bottom skins + spar", size=26, color=MUTED)
        s3 = E(r"\delta_{25}|=|199.8", size=40, cmap=DCM)
        s3n = T("the shared spar alone", size=26, color=MUTED)
        sums = VGroup(VGroup(s1, s1n).arrange(DOWN, buff=.12, aligned_edge=LEFT),
                      VGroup(s2, s2n).arrange(DOWN, buff=.12, aligned_edge=LEFT),
                      VGroup(s3, s3n).arrange(DOWN, buff=.12, aligned_edge=LEFT)).arrange(DOWN, buff=.35, aligned_edge=LEFT)
        fit(sums, 9.8, 3.4)
        sums.move_to([2.0, -2.25, 0])
        self.play(FadeOut(dalg), FadeOut(drop_cols), ReplacementTransform(rule, rule2),
                  keep_d.animate.shift(LEFT * (COLS_X[5] - COLS_X[1])), run_time=1.2)
        with self.say("Around cell one: one nineteen sixty nine. Around cell two: thirty five twenty eight. The shared spar alone: one ninety nine point eight.") as d:
            self.play(cI_w.animate.set_color(MINT), spar.animate.set_color(GOLD), Write(s1[:2]), run_time=.12 * d)
            self.play(Write(s1[2:]), FadeIn(s1n), Indicate(VGroup(dcol[0], dcol[3], dcol[1]), color=MINT), run_time=.23 * d)
            self.play(cII_w.animate.set_color(LIME), Write(s2[:2]), run_time=.12 * d)
            self.play(Write(s2[2:]), FadeIn(s2n), Indicate(VGroup(dcol[2], dcol[4], dcol[1]), color=LIME), run_time=.23 * d)
            self.play(Write(s3), FadeIn(s3n), Indicate(spar, color=GOLD, scale_factor=1.0), run_time=.2 * d)
            self.wait(.1 * d)
        self.wipe()
