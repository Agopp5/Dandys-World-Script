"""Shared kit for the energy-methods / FEM series: springs, walls, bars, loads, drawn the same way in every scene.

  wall(p, side=LEFT, h=1.6)          hatched wall whose face is at point p (side = the side the hatching is on)
  spring(a, b, coils=5, amp=0.18, color=LILAC, label=None)   zigzag from a to b with straight leads; label above
  node(p, color=INK, r=0.08)         a junction dot
  force(p, d=RIGHT, length=1.0, label=None, color=ROSE, tail=False)
                                     load arrow starting at p (tail=True: arrow ends at p), TeX label at its tip
  disp(p, label="q", length=0.7, below=0.45, color=SKY)   small displacement arrow drawn below p, TeX label
  bar(x0, x1, y=0.0, h=0.42, color=INK2, fill=SURFACE)    a bar segment (an element) as a rectangle
  fem_bar(xs, y=0.0, h=0.42, elem_labels=True, node_labels=None)
                                     elements between consecutive xs; .elems[i], .nodes[i], .tags[i] (circled numbers)
  dist_load(x0, x1, y, n=7, d=RIGHT, color=ROSE, length=0.42)   a row of small arrows: a distributed load f
  coil_x(spring_mob)                 helper for agents that redraw a spring: rebuild with spring(a, b) instead
Facts asserted at import: the series' worked numbers (one spring, two springs, stepped bar, HW P2).
"""
from mtk import *
import mtk.core as core

core.FONT = "Lato"   # Avenir Next is not installed here


def wall(p, side=LEFT, h=1.6, color=INK2):
    """Hatched support with its face through p. side LEFT/RIGHT: a vertical wall (hatching on that side);
    side UP: a ceiling (face below, hatching above); side DOWN: a floor (face above, hatching below). h = face length."""
    p, side = np.array(p, float), np.array(side, float)
    along = RIGHT if abs(side[1]) > 0.5 else UP
    line = Line(p - along * h / 2, p + along * h / 2, color=color, stroke_width=4)
    g = VGroup(line)
    n = int(h / 0.2)
    for i in range(n + 1):
        a = p - along * h / 2 + along * i * h / n
        g.add(Line(a, a + side * 0.22 - along * 0.18, color=color, stroke_width=2))
    return g


def spring(a, b, coils=5, amp=0.18, color=LILAC, label=None, size=34, lead=0.22):
    a, b = np.array(a, float), np.array(b, float)
    d = b - a
    L = np.linalg.norm(d)
    u = d / L
    nrm = np.array([-u[1], u[0], 0])
    lead = min(lead, L * 0.2)
    pts = [a, a + u * lead]
    m = 2 * coils
    for i in range(1, m):
        t = lead + (L - 2 * lead) * i / m
        pts.append(a + u * t + nrm * amp * (1 if i % 2 else -1))
    pts += [b - u * lead, b]
    g = VGroup(VMobject(color=color, stroke_width=4).set_points_as_corners(pts))
    if label is not None:
        lab = M(label, size=size, color=color) if isinstance(label, str) else label
        lab.move_to((a + b) / 2 + nrm * (amp + 0.32))
        g.add(lab)
    return g


def node(p, color=INK, r=0.08):
    return Dot(np.array(p, float), radius=r, color=color)


def force(p, d=RIGHT, length=1.0, label=None, color=ROSE, tail=False, size=34):
    p, d = np.array(p, float), np.array(d, float)
    d = d / np.linalg.norm(d)
    s, e = (p - d * length, p) if tail else (p, p + d * length)
    g = VGroup(Arrow(s, e, buff=0, color=color, stroke_width=6, tip_length=0.22, max_tip_length_to_length_ratio=0.4))
    if label is not None:
        lab = M(label, size=size, color=color) if isinstance(label, str) else label
        lab.next_to(e if not tail else s, d if not tail else -d, buff=0.12)
        g.add(lab)
    return g


def disp(p, label="q", length=0.7, below=0.45, color=SKY, size=32):
    p = np.array(p, float) + DOWN * below
    arr = Arrow(p, p + RIGHT * length, buff=0, color=color, stroke_width=4, tip_length=0.16,
                max_tip_length_to_length_ratio=0.35)
    tick = Line(p + UP * 0.12, p + DOWN * 0.12, color=color, stroke_width=3)
    g = VGroup(tick, arr)
    if label is not None:
        g.add((M(label, size=size, color=color) if isinstance(label, str) else label).next_to(arr, DOWN, buff=0.08))
    return g


def bar(x0, x1, y=0.0, h=0.42, color=INK2, fill=SURFACE):
    return Rectangle(width=x1 - x0, height=h, color=color, stroke_width=3, fill_color=fill,
                     fill_opacity=1).move_to([(x0 + x1) / 2, y, 0])


class fem_bar(VGroup):
    def __init__(self, xs, y=0.0, h=0.42, elem_labels=True, node_labels=None, size=30):
        super().__init__()
        self.elems, self.nodes, self.tags = VGroup(), VGroup(), VGroup()
        for i in range(len(xs) - 1):
            self.elems.add(bar(xs[i], xs[i + 1], y, h))
            if elem_labels:
                c = Circle(radius=0.2, color=INK2, stroke_width=2.5).move_to([(xs[i] + xs[i + 1]) / 2, y + h / 2 + 0.38, 0])
                self.tags.add(VGroup(c, T(str(i + 1), size=size - 6, color=INK2).move_to(c)))
        for i, x in enumerate(xs):
            self.nodes.add(node([x, y, 0]))
        self.add(self.elems, self.tags, self.nodes)
        if node_labels:
            self.nlabels = VGroup(*[M(t, size=size, color=SKY).next_to(self.nodes[i], DOWN, buff=h / 2 + 0.12)
                                    for i, t in enumerate(node_labels)])
            self.add(self.nlabels)


def dist_load(x0, x1, y, n=7, d=RIGHT, color=ROSE, length=0.42):
    d = np.array(d, float)
    g = VGroup()
    for i in range(n):
        x = x0 + (x1 - x0) * (i + 0.5) / n
        s = np.array([x, y, 0]) - d * length / 2
        g.add(Arrow(s, s + d * length, buff=0, color=color, stroke_width=3.5, tip_length=0.13,
                    max_tip_length_to_length_ratio=0.4))
    return g


# ---- facts (the full derivations are in solve.py) ----
assert (20 * 5 == 100) and (0.5 * 20 * 5**2 == 250) and (100 * 5 == 500)                 # one spring
assert np.allclose(np.linalg.solve([[60, -20], [-20, 20]], [40, 20]), [1.5, 2.5])           # two springs
assert np.allclose(np.linalg.solve([[42000, -14000], [-14000, 28000]], [7000, 0]), [0.2, 0.1])  # stepped bar
assert np.allclose(np.linalg.solve(1000 * np.array([[2, -1], [-1, 1]]), [-50, 50]), [0, 0.05])  # HW P2
