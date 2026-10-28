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

# Series-wide readability overrides (the viewer struggles with small, soft text; reviews found halos smearing math):
# 1. stress/strain hue: the default ACCENT (#95a2ff) is nearly LILAC (stiffness), so use a clearly different cyan.
ACCENT = "#36d6e7"


# 2. glow(m) draws a crisp rounded box behind m (faint fill, thin outline) instead of a blurred halo over glyphs.
def glow(m, color=None, buff=0.14):
    color = color or m.get_color()
    z = max(x.z_index for x in m.get_family())
    box = SurroundingRectangle(m, color=color, buff=buff, corner_radius=0.12, stroke_width=3,
                               fill_color=color, fill_opacity=0.10)
    m.set_z_index(z + 1)
    return box.set_z_index(z)


# 3. spotlight dims everything else but adds no halo, so the spotlit math stays sharp (unspot/wipe work as before).
def _spotlight(self, *mobs, color=None):
    c, w, _ = self._frame()
    scrim = FullScreenRectangle(stroke_width=0, fill_color=BG, fill_opacity=0.78)
    scrim.scale(w / config.frame_width).move_to(c).set_z_index(89)
    z = [(x, x.z_index) for m in mobs for x in m.get_family()]
    for m in mobs:
        m.set_z_index(90)
    self._spot = (scrim, [], z)
    self.lint_on = False
    return FadeIn(scrim)


VScene.spotlight = _spotlight


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


def spring(a, b, coils=5, amp=0.18, color=LILAC, label=None, size=40, lead=0.22):
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


def force(p, d=RIGHT, length=1.0, label=None, color=ROSE, tail=False, size=40):
    p, d = np.array(p, float), np.array(d, float)
    d = d / np.linalg.norm(d)
    s, e = (p - d * length, p) if tail else (p, p + d * length)
    g = VGroup(Arrow(s, e, buff=0, color=color, stroke_width=6, tip_length=0.22, max_tip_length_to_length_ratio=0.4))
    if label is not None:
        lab = M(label, size=size, color=color) if isinstance(label, str) else label
        lab.next_to(e if not tail else s, d if not tail else -d, buff=0.12)
        g.add(lab)
    return g


def disp(p, label="q", length=0.7, below=0.45, color=SKY, size=38):
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
    def __init__(self, xs, y=0.0, h=0.42, elem_labels=True, node_labels=None, size=38):
        super().__init__()
        self.elems, self.nodes, self.tags = VGroup(), VGroup(), VGroup()
        for i in range(len(xs) - 1):
            self.elems.add(bar(xs[i], xs[i + 1], y, h))
            if elem_labels:
                c = Circle(radius=0.26, color=INK2, stroke_width=2.5).move_to([(xs[i] + xs[i + 1]) / 2, y + h / 2 + 0.42, 0])
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


class two_spring_fig(VGroup):
    """The Episode 2 figure, identical in S08-S12: wall - k1 - node 1 - k2 - node 2, loads F1/F2 and q1/q2.
    two_spring_fig(left=(-6, 2.45), L=3.0, d1=0, d2=0, loads=True, disps=True, scale=1)
      d1, d2: extra node displacements (scene units) for a stretched state; rebuild with a new figure to animate.
    Parts: .wall .s1 .s2 .n1 .n2 .k1 .k2 (labels BELOW the springs' middles, size 40) .F1 .F2 (ROSE arrows starting 0.5
    above each node, pointing right, label at the tip, size 40) .q1 .q2 (SKY disp arrows under the nodes, size 40)."""
    def __init__(self, left=(-6, 2.45), L=3.0, d1=0.0, d2=0.0, loads=True, disps=True, scale=1.0):
        super().__init__()
        x0, y = left
        p0 = np.array([x0, y, 0.0])
        p1 = p0 + RIGHT * (L + d1)
        p2 = p0 + RIGHT * (2 * L + d2)
        self.wall = wall(p0, h=1.4)
        self.s1, self.s2 = spring(p0, p1), spring(p1, p2)
        self.n1, self.n2 = node(p1, r=0.1), node(p2, r=0.1)
        self.k1 = M("k_1", size=40, color=LILAC).next_to(self.s1, DOWN, buff=0.18)
        self.k2 = M("k_2", size=40, color=LILAC).next_to(self.s2, DOWN, buff=0.18)
        self.add(self.wall, self.s1, self.s2, self.n1, self.n2, self.k1, self.k2)
        if loads:
            self.F1 = force(p1 + UP * 0.5, length=0.9, label="F_1")
            self.F2 = force(p2 + UP * 0.5, length=0.9, label="F_2")
            self.add(self.F1, self.F2)
        if disps:
            self.q1 = disp(p0 + RIGHT * L, "q_1", size=40)
            self.q2 = disp(p0 + RIGHT * 2 * L, "q_2", size=40)
            self.add(self.q1, self.q2)
        self.scale(scale, about_point=p0)


# ---- HW 6 problem 1 figure (from S16), shared by S16-S22 so it looks the same in every scene ----
# hw_figure(at=ORIGIN, k2b_label=False) -> VGroup about 10.6 wide x 4.6 tall centred near `at`; scale/shift it as needed.
# Layout: wall face at x=-5.8; K1 on the top row (y=+0.9) from the wall to a rigid bar (x 0.9..1.4, 4 tall); bottom row
# (y=-1.1): K2 wall -> junction J (x=-2.6) -> second K2 (unlabeled unless k2b_label) -> bar; K3 on the middle row from
# the bar's right face to the outer node O (x=4.4). Loads (ROSE, labels 40): P1 on a short stem below J, P2 (y=+1.7)
# and P3 (y=-1.7) end on the bar's left face, P4 starts at O. SKY q1 under P1, q2 under the bar, q3 under O (labels 40).
# Parts: .wall .k1 .k2a .k2b .k3 .bar .J .O .stem .P[i] .Plab[i] .q[i] .klab[...] .pts; .rebuild_springs(dq1, dq2, dq3)
# returns new (k1, k2a, k2b, k3) springs for a displaced state.
HW_WALL_X, HW_BAR_X0, HW_BAR_X1, HW_J_X, HW_O_X = -5.8, 0.9, 1.4, -2.6, 4.4
HW_TOP_Y, HW_BOT_Y, HW_MID_Y, HW_BAR_H = 0.9, -1.1, 0.0, 4.0


def qarrow(p, tex, below=0.45, length=0.7):
    """A SKY displacement arrow drawn below p, with a readable label (the kit's disp label is small)."""
    a = Arrow(p + below * DOWN, p + below * DOWN + length * RIGHT, buff=0, color=SKY, stroke_width=5,
              max_tip_length_to_length_ratio=0.3)
    return VGroup(a, E(tex, size=40).next_to(a, RIGHT, buff=0.1))


def hw_figure(at=ORIGIN, k2b_label=False):
    o = np.array(at, dtype=float)
    P = lambda x, y: o + np.array([x, y, 0.0])
    pts = dict(w_top=P(HW_WALL_X, HW_TOP_Y), w_bot=P(HW_WALL_X, HW_BOT_Y), b_top=P(HW_BAR_X0, HW_TOP_Y),
               b_bot=P(HW_BAR_X0, HW_BOT_Y), b_mid=P(HW_BAR_X1, HW_MID_Y), J=P(HW_J_X, HW_BOT_Y),
               O=P(HW_O_X, HW_MID_Y))
    g = VGroup()
    g.pts = pts
    g.wall = wall(P(HW_WALL_X, 0), side=LEFT, h=HW_BAR_H)
    g.k1 = spring(pts["w_top"], pts["b_top"], coils=7)
    g.k2a = spring(pts["w_bot"], pts["J"], coils=5)
    g.k2b = spring(pts["J"], pts["b_bot"], coils=5)
    g.k3 = spring(pts["b_mid"], pts["O"], coils=5)
    g.bar = bar(HW_BAR_X0, HW_BAR_X1, h=HW_BAR_H).shift(o)
    g.J = node(pts["J"])
    g.O = node(pts["O"])
    lab = lambda tex, m: E(tex, size=40).next_to(m, UP, buff=0.12)
    g.klab = {"K1": lab("K_1", g.k1), "K2a": lab("K_2", g.k2a), "K3": lab("K_3", g.k3)}
    if k2b_label:
        g.klab["K2b"] = lab("K_2", g.k2b)
    # loads
    g.stem = Line(pts["J"], pts["J"] + 0.5 * DOWN, color=INK2, stroke_width=3)
    g.P = {1: force(pts["J"] + 0.5 * DOWN, RIGHT, length=0.8),
           2: force(P(HW_BAR_X0, 1.7), RIGHT, length=0.9, tail=True),
           3: force(P(HW_BAR_X0, -1.7), RIGHT, length=0.9, tail=True),
           4: force(pts["O"], RIGHT, length=0.9)}
    g.Plab = {1: E("P_1", size=40).next_to(g.P[1], RIGHT, buff=0.1),
              2: E("P_2", size=40).next_to(g.P[2], LEFT, buff=0.1),
              3: E("P_3", size=40).next_to(g.P[3], LEFT, buff=0.1),
              4: E("P_4", size=40).next_to(g.P[4], RIGHT, buff=0.1)}
    # displacements
    g.q = {1: qarrow(pts["J"] + 0.5 * DOWN, "q_1", below=0.5),
           2: qarrow(P((HW_BAR_X0 + HW_BAR_X1) / 2, -HW_BAR_H / 2), "q_2", below=0.4),
           3: qarrow(pts["O"], "q_3", below=0.45)}
    g.add(g.wall, g.k1, g.k2a, g.k2b, g.k3, g.bar, g.J, g.O, *g.klab.values(), g.stem,
          *g.P.values(), *g.Plab.values(), *g.q.values())

    def rebuild_springs(dq1=0.0, dq2=0.0, dq3=0.0):
        s = lambda d: d * RIGHT
        return (spring(pts["w_top"], pts["b_top"] + s(dq2), coils=7),
                spring(pts["w_bot"], pts["J"] + s(dq1), coils=5),
                spring(pts["J"] + s(dq1), pts["b_bot"] + s(dq2), coils=5),
                spring(pts["b_mid"] + s(dq2), pts["O"] + s(dq3), coils=5))
    g.rebuild_springs = rebuild_springs
    return g


# ---- Episode 7 stepped bar (from S47), shared by S47-S53 ----
def stepped_bar(x0=-6.0, x3=6.0, y=2.0, h1=1.4, h2=0.6, f1=0.37, f2=0.37):
    """The S47-S53 figure. Left wall face at x0, right wall face at x3, bar axis at height y.
    Element 1 (thick, h1) runs x0..x1, element 2 (thin, h2) x1..x2, the LILAC spring x2..x3.
    Returns VGroup(wl, e1, e2, sp, wr); extras (not in the group) as attributes:
    .x node x's, .p(i) node point, .nodes dots, .nums node numbers (row below the bar), .elabs
    "element 1/2" (a third row, below the q arrows, at element mids), .klab K over the spring, .load + .plab the ROSE P at the
    step, .dims two "500 mm" dimension lines above the bars, .qs SKY q_1, q_2 arrows (row under .nums)."""
    L = x3 - x0
    x1 = x0 + f1 * L
    x2 = x1 + f2 * L
    xs = [x0, x1, x2, x3]
    p = lambda i: np.array([xs[i], y, 0.0])
    g = VGroup()
    g.x, g.p = xs, p
    g.wl = wall(p(0), side=LEFT, h=h1 + 1.2)
    g.e1 = bar(x0, x1, y=y, h=h1)
    g.e2 = bar(x1, x2, y=y, h=h2)
    g.sp = spring(p(2), p(3), coils=6, amp=0.3)
    g.wr = wall(p(3), side=RIGHT, h=h1 + 1.2)
    g.add(g.wl, g.e1, g.e2, g.sp, g.wr)
    ya, yb, yc = y - h1 / 2 - 0.42, y - h1 / 2 - 1.0, y - h1 / 2 - 1.6   # rows below the bar
    g.nodes = VGroup(*[node(p(i), r=0.11).set_z_index(3) for i in range(4)])
    inset = [0.4, 0, 0, -0.4]                              # keep 0 and 3 clear of the wall faces
    g.nums = VGroup(*[T(str(i), size=42, weight=BOLD).move_to([xs[i] + inset[i], ya, 0]) for i in range(4)])
    g.elabs = VGroup(T("element 1", size=36, color=INK2).move_to([(x0 + x1) / 2, yc, 0]),
                     T("element 2", size=36, color=INK2).move_to([(x1 + x2) / 2, yc, 0]))
    g.klab = M("K", size=60, color=LILAC).move_to([(x2 + x3) / 2, y + 0.8, 0])
    g.load = force(np.array([x1, y + (h1 + h2) / 4, 0]), d=RIGHT, length=0.9)
    g.plab = E(r"P|=|7000\ \text{N}", size=54).next_to(g.load, UP, buff=0.12).align_to(g.load, LEFT)
    yd = y + h1 / 2 + 0.35
    def dim(a, b):
        ln = Line([a + 0.06, yd, 0], [b - 0.06, yd, 0], color=MUTED, stroke_width=3)
        ticks = VGroup(*[Line([xx, yd - 0.14, 0], [xx, yd + 0.14, 0], color=MUTED, stroke_width=3)
                         for xx in (a + 0.06, b - 0.06)])
        return VGroup(ln, ticks, T("500 mm", size=36, color=INK2).next_to(ln, UP, buff=0.12))
    g.dims = VGroup(dim(x0, x1), dim(x1, x2))
    def qa(i, tex):
        a = Arrow(np.array([xs[i], yb, 0]), np.array([xs[i] + 0.85, yb, 0]), buff=0, color=SKY,
                  stroke_width=6, max_tip_length_to_length_ratio=0.3)
        return VGroup(a, M(tex, size=60, color=SKY).next_to(a, RIGHT, buff=0.12))
    g.qs = VGroup(qa(1, "q_1"), qa(2, "q_2"))
    return g


# ---- facts (the full derivations are in solve.py) ----
assert (20 * 5 == 100) and (0.5 * 20 * 5**2 == 250) and (100 * 5 == 500)                 # one spring
assert np.allclose(np.linalg.solve([[60, -20], [-20, 20]], [40, 20]), [1.5, 2.5])           # two springs
assert np.allclose(np.linalg.solve([[42000, -14000], [-14000, 28000]], [7000, 0]), [0.2, 0.1])  # stepped bar
assert np.allclose(np.linalg.solve(1000 * np.array([[2, -1], [-1, 1]]), [-50, 50]), [0, 0.05])  # HW P2
