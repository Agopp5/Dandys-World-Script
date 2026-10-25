"""S18: several cells, one shear flow per cell (BRIEF.md S18; rework of old/s12_cells.py)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# cell III's flow is SKY (series rule); the areas follow their cell's hue
CM = {"q_{III}": SKY, "A_I": MINT, "A_{II}": LIME, "A_{III}": SKY}

# a generic tapered three-cell wing box (mm), straight walls; webs at x = 0, 220, 420, 600
PTS = {"a1": (0, 300), "a2": (0, -300), "b1": (220, 310), "b2": (220, -310),
       "c1": (420, 260), "c2": (420, -260), "d1": (600, 190), "d2": (600, -190)}
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
assert np.isclose(AREAS[0], 220 * (600 + 620) / 2)
edges = [frozenset(e) for c in CELLS for e in zip(c, c[1:] + c[:1])]
assert edges.count(frozenset(("b1", "b2"))) == 2 and edges.count(frozenset(("c1", "c2"))) == 2
# T = sum 2 A_R q_R: with all q_R equal to q, the box acts as one cell of area sum A_R
assert np.isclose(sum(2 * a * 1.0 for a in AREAS), 2 * shoelace(("a1", "b1", "c1", "d1", "d2", "c2", "b2", "a2")))


class S18_Cells(VScene):
    budget = 87

    def construct(self):
        sec = Section(PTS, WALLS, width=6.0, center=(-3.2, -0.3))
        walls = sec.draw()
        booms = sec.booms({n: 600 for n in PTS})
        tq = torque(np.array([3.6, 0.6, 0]), radius=1.2, color=LILAC, ccw=True, label="T")
        tnote = T("pure torque", size=34, color=MUTED).next_to(tq, DOWN, buff=.4)
        bnote = T("no bending stress: booms play no part", size=30, color=MUTED).next_to(tnote, DOWN, buff=.35)
        self.beat("Real wings often have several cells side by side. With pure torque, there's no bending stress, so the booms don't matter at all.",
                  Create(walls), FadeIn(booms), .1, [FadeIn(tq), FadeIn(tnote)], .1,
                  [FadeOut(booms), FadeIn(bnote)], .15, w=(.22, .1, .1, .18, .1, .15, .15))

        # cell polygons (faint fill, for the areas later) and their constant flows
        hues = [MINT, LIME, SKY]
        polys = VGroup(*[Polygon(*[sec.p(n) for n in c], stroke_width=0, fill_color=h, fill_opacity=0)
                         for c, h in zip(CELLS, hues)])
        centers = [np.mean([sec.p(n) for n in c], axis=0) for c in CELLS]
        qnames = [r"q_I", r"q_{II}", r"q_{III}"]
        flows = VGroup(*[VGroup(cell_flow(ctr + UP * 1.0, radius=.62, color=h, ccw=True),
                                M(qn, size=44, color=h).move_to(ctr + UP * 1.0))
                         for ctr, h, qn in zip(centers, hues, qnames)])
        self.add(polys)
        self.beat("Each cell still carries its own constant shear flow: q one, q two, q three.",
                  .25, FadeIn(flows[0]), .05, FadeIn(flows[1]), .05, FadeIn(flows[2]), .2,
                  w=(.25, .14, .05, .14, .05, .14, .23))

        # shared webs: both cells' flows run on them, opposite ways (ccw cells: up on the left cell's right wall)
        def pair(a, b, c_left, c_right):
            lo, hi = sec.p(b) + UP * .9, sec.p(a) + DOWN * .9
            up = Arrow(lo + LEFT * .22, hi + LEFT * .22, buff=0, color=c_left, stroke_width=5)
            dn = Arrow(hi + RIGHT * .22, lo + RIGHT * .22, buff=0, color=c_right, stroke_width=5)
            return VGroup(up, dn)
        pairs = VGroup(pair("b1", "b2", MINT, LIME), pair("c1", "c2", LIME, SKY))
        shared = VGroup(flow(sec, "b2", "b1", 1.0, color=GOLD, frac=.45, off=.0),
                        flow(sec, "c2", "c1", 1.0, color=GOLD, frac=.45, off=.0))
        dl = VGroup(backed(M(r"q_I - q_{II}", size=40, color=GOLD)),
                    backed(M(r"q_{II} - q_{III}", size=40, color=GOLD)))
        dl[0].move_to(sec.mid("b1", "b2") + DOWN * 1.3)
        dl[1].move_to(sec.mid("c1", "c2") + DOWN * 2.2)
        self.beat("A wall shared by two cells has both flows on it, in opposite directions. So it carries the difference.",
                  [Indicate(walls[7], color=GOLD), Indicate(walls[8], color=GOLD)],
                  [GrowArrow(a) for p in pairs for a in p], .15,
                  [ReplacementTransform(pairs[0], shared[0]), ReplacementTransform(pairs[1], shared[1])],
                  FadeIn(dl), .15, w=(.15, .2, .15, .15, .15, .2))

        # torque equation on the right
        eq = E(r"T|=|\sum_R|2|A_R|q_R", size=52)
        rows = VGroup(E(r"T|=|2|A_I|q_I", size=48, cmap=CM),
                      E(r"+|2|A_{II}|q_{II}", size=48, cmap=CM),
                      E(r"+|2|A_{III}|q_{III}", size=48, cmap=CM)).arrange(DOWN, buff=.35, aligned_edge=LEFT)
        rows[1].align_to(rows[0][2], LEFT).shift(LEFT * rows[1][0].width * 1.6)
        rows[2].align_to(rows[1], LEFT)
        anote = VGroup(M(r"A_R", size=44, color=MUTED), T("= area enclosed by cell R", size=30, color=MUTED))
        anote.arrange(RIGHT, buff=.2)
        alg = VGroup(eq, anote, rows).arrange(DOWN, buff=.45)
        alg.move_to(np.array([3.6, 0, 0])).to_edge(UP, buff=.5)
        alabels = VGroup(*[M(a, size=44, color=h).move_to(ctr + DOWN * .15)
                           for a, h, ctr in zip([r"A_I", r"A_{II}", r"A_{III}"], hues, centers)])
        self.beat("The torque is the sum of two A q for every cell.",
                  [FadeOut(tq), FadeOut(tnote), FadeOut(bnote)], Write(eq), .1,
                  [polys.animate.set_fill(opacity=.18), FadeIn(alabels), FadeIn(anote)], .1,
                  LaggedStart(*[FadeIn(r, shift=.2 * LEFT) for r in rows], lag_ratio=.5), .15,
                  w=(.08, .17, .08, .17, .08, .3, .12))

        box = SurroundingRectangle(rows, color=HAIR, buff=.2, corner_radius=.1)
        count = panel(VGroup(T("N unknowns, 1 equation", size=36, color=INK),
                             T("We need more equations.", size=32, color=MUTED)).arrange(DOWN, buff=.2))
        count.next_to(rows, DOWN, buff=.45)
        if count.get_bottom()[1] < -3.8:
            count.shift(UP * (-3.8 - count.get_bottom()[1]))
        self.beat("But that's only one equation, and there's one unknown shear flow for every cell. We need more equations.",
                  Create(box), .05, LaggedStart(*[Circumscribe(f, color=h, shape=Circle) for f, h in zip(flows, hues)],
                                                lag_ratio=.4), .05,
                  FadeIn(count, shift=.2 * UP), Indicate(count[1][1], color=ACCENT), .15,
                  w=(.12, .05, .3, .05, .15, .15, .18))
        self.wipe()
