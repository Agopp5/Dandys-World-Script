"""Shared kit for the structural-idealization / multi-cell-torsion series: thin-walled cross-sections on top of mtk.

  sec = Section(pts, walls, width=6.0, center=(-3.2, -0.3))
      pts: {name: (x_mm, y_mm)}  walls: [(a, b, t_mm), ...]  (mm are scaled so the section is `width` units wide)
      sec.p(name) scene point     sec.mid(a, b) wall midpoint     sec.inward(a, b) unit normal toward the centroid
      sec.draw(color=INK2, t_scale=1.0) -> VGroup of walls (stroke width grows with thickness), sec.walls_m[(a, b)]
      sec.booms(areas, color=EMBER, r0=0.07, k=0.0028) -> VGroup of dots, radius r0 + k*sqrt(B); sec.boom_m[name]
      sec.names(color=INK2, size=30) -> VGroup of boom numbers placed just outside the section
  flow(sec, a, b, q, color=SKY, label=None, size=30, frac=0.6, off=0.28)
      arrow along wall a->b (reversed when q < 0), offset `off` toward the inside, with an optional TeX label
  cell_flow(center, radius=0.55, color=MINT, ccw=True, label=None)   circular arrow for a cell's constant shear flow
  torque(center, radius=0.6, color=LILAC, ccw=True, label="T")        curved torque arrow
  Presets (exact HW / slide geometry, in mm):
      channel()  the slide's 4-boom channel (B = 300 mm^2, 200 x 400)
      hw_box()   HW P1: 500 x 300 box, booms 1..4 clockwise from top-left; skins 10 mm, left web 10 mm, right web 8 mm
      hw_twocell() HW P2: booms 1..6 as in the figure (1 bottom-left, 6 top-left, 2/5 spar, 3/4 right);
                   straight walls drawn through the boom points (the real skins are slightly curved)
      wing_outline(n_stringers=14) -> (outline VMobject, list of stringer points) a two-spar wing for the hook
Facts asserted at import: HW P1 boom areas 4000 / 3556 mm^2 and shear centre 224.8 mm; HW P2 per-unit-torque flows.
"""
from mtk import *
import mtk.core as core

core.FONT = "Lato"   # Avenir Next is not installed here


class Section:
    def __init__(self, pts, walls, width=6.0, center=(-3.2, -0.3)):
        self.pts, self.walls = dict(pts), list(walls)
        xs = [v[0] for v in pts.values()]
        ys = [v[1] for v in pts.values()]
        self.s = width / max(1e-9, (max(xs) - min(xs)))
        self.c0 = np.array([(max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2])
        self.center = np.array([center[0], center[1], 0.0])
        self.walls_m, self.boom_m = {}, {}

    def p(self, name):
        x, y = (np.array(self.pts[name]) - self.c0) * self.s
        return self.center + np.array([x, y, 0.0])

    def mid(self, a, b):
        return (self.p(a) + self.p(b)) / 2

    def centroid(self):
        return sum(self.p(k) for k in self.pts) / len(self.pts)

    def inward(self, a, b):
        d = self.p(b) - self.p(a)
        n = np.array([-d[1], d[0], 0.0])
        n /= np.linalg.norm(n)
        if np.dot(self.centroid() - self.mid(a, b), n) < 0:
            n = -n
        return n

    def draw(self, color=INK2, t_scale=1.0):
        g = VGroup()
        for a, b, t in self.walls:
            m = Line(self.p(a), self.p(b), color=color, stroke_width=max(1.5, 1.6 * t * t_scale))
            self.walls_m[(a, b)] = m
            g.add(m)
        return g

    def booms(self, areas, color=EMBER, r0=0.07, k=0.0028):
        g = VGroup()
        for name, B in areas.items():
            d = Dot(self.p(name), radius=r0 + k * np.sqrt(B), color=color)
            self.boom_m[name] = d
            g.add(d)
        return g

    def names(self, color=INK2, size=30, off=0.38):
        g = VGroup()
        c = self.centroid()
        for name in self.pts:
            d = self.p(name) - c
            d = d / (np.linalg.norm(d) + 1e-9)
            g.add(T(str(name), size=size, color=color).move_to(self.p(name) + off * d))
        return g


def flow(sec, a, b, q, color=SKY, label=None, size=30, frac=0.6, off=0.28):
    pa, pb = sec.p(a), sec.p(b)
    if q < 0:
        pa, pb = pb, pa
    m = (pa + pb) / 2 + off * sec.inward(a, b)
    d = pb - pa
    d /= np.linalg.norm(d)
    L = frac * np.linalg.norm(sec.p(b) - sec.p(a))
    arr = Arrow(m - d * L / 2, m + d * L / 2, buff=0, color=color, stroke_width=5, tip_length=0.22,
                max_tip_length_to_length_ratio=0.35)
    g = VGroup(arr)
    if label is not None:
        lab = M(label, size=size, color=color) if isinstance(label, str) else label
        lab.move_to(m + 0.38 * sec.inward(a, b))
        g.add(lab)
    return g


def cell_flow(center, radius=0.55, color=MINT, ccw=True, label=None, size=34):
    c = np.array([center[0], center[1], 0.0])
    arc = Arc(radius=radius, start_angle=-PI / 2 if ccw else PI / 2, angle=(1.6 * PI) * (1 if ccw else -1),
              arc_center=c, color=color, stroke_width=5)
    arc.add_tip(tip_length=0.2)
    g = VGroup(arc)
    if label is not None:
        g.add((M(label, size=size, color=color) if isinstance(label, str) else label).move_to(c))
    return g


def torque(center, radius=0.6, color=LILAC, ccw=True, label="T", size=40):
    c = np.array([center[0], center[1], 0.0])
    arc = Arc(radius=radius, start_angle=PI / 6 if ccw else 5 * PI / 6, angle=(2 * PI / 3) * (1 if ccw else -1),
              arc_center=c, color=color, stroke_width=6)
    arc.add_tip(tip_length=0.24)
    g = VGroup(arc)
    if label:
        g.add(M(label, size=size, color=color).next_to(arc, UP, buff=0.1))
    return g


# ---- presets ----
def channel(**kw):
    pts = {1: (200, 200), 2: (0, 200), 3: (0, -200), 4: (200, -200)}
    return Section(pts, [(1, 2, 2), (2, 3, 2), (3, 4, 2)], **kw)


def hw_box(**kw):
    pts = {1: (0, 150), 2: (500, 150), 3: (500, -150), 4: (0, -150)}
    return Section(pts, [(1, 2, 10), (2, 3, 8), (3, 4, 10), (4, 1, 10)], **kw)


def hw_twocell(**kw):
    pts = {1: (0, -127), 6: (0, 127), 2: (635, -203), 5: (635, 203), 3: (1398, -101), 4: (1398, 101)}
    walls = [(1, 2, 0.915), (2, 3, 0.559), (3, 4, 1.220), (4, 5, 0.559), (5, 6, 0.915), (6, 1, 1.625), (2, 5, 2.032)]
    return Section(pts, walls, **kw)


def wing_outline(n_stringers=14, width=6.5, center=(0, 0)):
    """A two-spar wing section (nose left): returns (outline VMobject, stringer points, front spar, rear spar)."""
    t = np.linspace(0, 1, 120)
    xs = 1 - np.cos(t * PI / 2)          # cluster points at the nose
    thick = 0.12 * (2.97 * np.sqrt(xs) - 1.26 * xs - 3.52 * xs**2 + 2.84 * xs**3 - 1.0 * xs**4)
    top = [np.array([x * width - width / 2 + center[0], y * width + center[1], 0]) for x, y in zip(xs, thick)]
    bot = [np.array([x * width - width / 2 + center[0], -y * width + center[1], 0]) for x, y in zip(xs, thick)]
    out = VMobject(color=INK, stroke_width=4).set_points_smoothly(top + bot[::-1][1:])

    def at(x, side):
        k = int(np.argmin(np.abs(xs - x)))
        return top[k] if side > 0 else bot[k]
    st = [at(x, s) for x in np.linspace(0.12, 0.7, n_stringers // 2) for s in (1, -1)]
    fs = Line(at(0.15, 1), at(0.15, -1), color=INK, stroke_width=4)
    rs = Line(at(0.7, 1), at(0.7, -1), color=INK, stroke_width=4)
    return out, st, fs, rs


# ---- facts: the HW answers (asserted at import, so a wrong edit fails fast) ----
def _box_shear_centre(W, H, tt, tb, tl, tr, aL, aR):
    BL = aL + tt * W / 6 * 3 + tl * H / 6
    BR = aR + tt * W / 6 * 3 + tr * H / 6
    P = {1: (0, H / 2), 2: (W, H / 2), 3: (W, -H / 2), 4: (0, -H / 2)}
    B = {1: BL, 2: BR, 3: BR, 4: BL}
    Ixx = sum(B[k] * P[k][1] ** 2 for k in P)
    ws = [(1, 2, tt), (2, 3, tr), (3, 4, tb), (4, 1, tl)]
    qb, q = {}, 0.0
    for a, b, t in ws:
        if a != 1:
            q -= B[a] * P[a][1] / Ixx
        qb[(a, b)] = q
    L = {(a, b): np.hypot(P[b][0] - P[a][0], P[b][1] - P[a][1]) / t for a, b, t in ws}
    qs0 = -sum(qb[k] * L[k] for k in L) / sum(L.values())
    xi = sum((qb[(a, b)] + qs0) * (P[a][0] * P[b][1] - P[a][1] * P[b][0]) for a, b, t in ws)
    return BL, BR, Ixx, qs0, xi


_hw = _box_shear_centre(500, 300, 10, 10, 10, 8, 1000, 656)
assert _hw[0] == 4000 and _hw[1] == 3556 and np.isclose(_hw[2], 340.02e6) and np.isclose(_hw[4], 224.76, atol=0.01)
