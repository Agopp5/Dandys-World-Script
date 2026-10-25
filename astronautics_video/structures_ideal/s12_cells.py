"""S12: one shear flow per cell (BRIEF.md S12)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

# q_III has no series hue; this scene gives it SKY (generic shear flow) and the areas follow their cell's hue
CM = {"q_{III}": SKY, "A_I": MINT, "A_{II}": LIME, "A_{III}": SKY}

# a generic tapered three-cell wing box (mm), straight walls; webs at x = 0, 220, 420, 600
PTS = {"a1": (0, 250), "a2": (0, -250), "b1": (220, 260), "b2": (220, -260),
       "c1": (420, 220), "c2": (420, -220), "d1": (600, 160), "d2": (600, -160)}
WALLS = [("a1", "b1", 2), ("b1", "c1", 2), ("c1", "d1", 2),
         ("a2", "b2", 2), ("b2", "c2", 2), ("c2", "d2", 2),
         ("a1", "a2", 3), ("b1", "b2", 3), ("c1", "c2", 3), ("d1", "d2", 2.5)]
CELLS = [("a1", "b1", "b2", "a2"), ("b1", "c1", "c2", "b2"), ("c1", "d1", "d2", "c2")]


def shoelace(names):
    xy = np.array([PTS[n] for n in names], float)
    x, y = xy[:, 0], xy[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


# facts: each cell encloses a positive area, and every interior web is shared by exactly two cells
AREAS = [shoelace(c) for c in CELLS]
assert all(a > 0 for a in AREAS)
assert np.isclose(AREAS[0], 220 * (500 + 520) / 2)
edges = [frozenset(e) for c in CELLS for e in zip(c, c[1:] + c[:1])]
assert edges.count(frozenset(("b1", "b2"))) == 2 and edges.count(frozenset(("c1", "c2"))) == 2
# T = sum 2 A_R q_R: with all q_R equal to q, the box acts as one cell of area sum A_R
assert np.isclose(sum(2 * a * 1.0 for a in AREAS), 2 * shoelace(("a1", "b1", "c1", "d1", "d2", "c2", "b2", "a2")))


class S12_Cells(VScene):
    budget = 71

    def construct(self):
        sec = Section(PTS, WALLS, width=6.0, center=(-3.2, -0.3))
        walls = sec.draw()
        booms = sec.booms({n: 600 for n in PTS})
        tq = torque(np.array([1.6, 0.4, 0]), radius=1.0, color=LILAC, ccw=True, label="T")
        tnote = T("pure torque", size=28, color=MUTED).next_to(tq, DOWN, buff=.35)
        self.beat("Now twist a wing box with several cells. With no axial restraint, there's no direct stress, so the booms play no part at all.",
                  Create(walls), [FadeIn(booms), FadeIn(tq), FadeIn(tnote)], .15, FadeOut(booms), w=(.3, .3, .25))

        # cell polygons (faint fill, for the areas later) and their constant flows
        hues = [MINT, LIME, SKY]
        polys = VGroup(*[Polygon(*[sec.p(n) for n in c], stroke_width=0, fill_color=h, fill_opacity=0)
                         for c, h in zip(CELLS, hues)])
        centers = [np.mean([sec.p(n) for n in c], axis=0) for c in CELLS]
        qnames = [r"q_I", r"q_{II}", r"q_{III}"]
        flows = VGroup(*[cell_flow(ctr + UP * .75, radius=.5, color=h, ccw=True, label=qn)
                         for ctr, h, qn in zip(centers, hues, qnames)])
        shared = VGroup(flow(sec, "b2", "b1", 1.0, color=GOLD, frac=.45, off=.0),
                        flow(sec, "c2", "c1", 1.0, color=GOLD, frac=.45, off=.0))
        dl = VGroup(backed(M(r"q_I - q_{II}", size=30, color=GOLD)),
                    backed(M(r"q_{II} - q_{III}", size=30, color=GOLD)))
        dl[0].move_to(sec.mid("b1", "b2") + DOWN * 1.3)
        dl[1].move_to(sec.mid("c1", "c2") + DOWN * 1.3)
        self.add(polys)
        self.beat("Each cell carries its own constant shear flow. A wall shared by two cells carries the difference.",
                  LaggedStart(*[FadeIn(f) for f in flows], lag_ratio=.4), .1,
                  [Indicate(walls[7], color=GOLD), Indicate(walls[8], color=GOLD)],
                  [FadeIn(shared), FadeIn(dl)], w=(.45, .2, .25))

        # torque equation on the right
        eq = E(r"T|=|\sum_R|2|A_R|q_R", size=52)
        rows = VGroup(E(r"T|=|2|A_I|q_I", size=44, cmap=CM),
                      E(r"+|2|A_{II}|q_{II}", size=44, cmap=CM),
                      E(r"+|2|A_{III}|q_{III}", size=44, cmap=CM)).arrange(DOWN, buff=.35, aligned_edge=LEFT)
        rows[1].align_to(rows[0][2], LEFT).shift(LEFT * rows[1][0].width * 1.6)
        rows[2].align_to(rows[1], LEFT)
        alg = VGroup(eq, rows).arrange(DOWN, buff=.7)
        place(alg, "right")
        alg.shift(UP * .3)
        anote = TX(r"$A_R$ = area enclosed by cell $R$", size=26, color=MUTED).next_to(eq, DOWN, buff=.2)
        rows.next_to(anote, DOWN, buff=.45)
        alabels = VGroup(*[M(a, size=34, color=h).move_to(ctr + DOWN * .25)
                           for a, h, ctr in zip([r"A_I", r"A_{II}", r"A_{III}"], hues, centers)])
        self.beat("The torque is two times the area of each cell, times its shear flow, added up.",
                  [FadeOut(tq), FadeOut(tnote), Write(eq)],
                  [polys.animate.set_fill(opacity=.18), FadeIn(alabels), FadeIn(anote)],
                  LaggedStart(*[FadeIn(r, shift=.2 * LEFT) for r in rows], lag_ratio=.5),
                  w=(.3, .3, .4))

        box = SurroundingRectangle(rows, color=HAIR, buff=.2, corner_radius=.1)
        count = panel(VGroup(T("N unknowns, 1 equation", size=34, color=INK),
                             T("We need more equations.", size=30, color=MUTED)).arrange(DOWN, buff=.2))
        count.next_to(rows, DOWN, buff=.45)
        if count.get_bottom()[1] < -3.8:
            count.shift(UP * (-3.8 - count.get_bottom()[1]))
        self.beat("But that's one equation, and there's one unknown for every cell. We need more.",
                  [Create(box), *[Circumscribe(f, color=h, shape=Circle) for f, h in zip(flows, hues)]],
                  FadeIn(count, shift=.2 * UP), .1, Indicate(count[1], color=ACCENT), w=(.4, .3, .2))
        self.wipe()
