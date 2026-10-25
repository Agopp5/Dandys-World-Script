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


