"""Shared kit for the orbit-determination series: a fake-3D orbit view on top of mtk.

  View(elev=22, azim=-55, scale=1.0, center=(-3.2, -0.3))  camera; .elev .azim .scale are ValueTrackers
      .p(xyz) scene point   .depth(xyz) toward-viewer depth   .turn(d_azim) animation that orbits the camera
  globe(view, R=1.0)        shaded Earth (mtk SurfaceImage) that follows the camera
  curve(view, f, t0, t1, color, width=4, R=None)  3D curve f(t); parts hidden behind a globe of radius R are dimmed
  arrow3(view, a, b, color), line3(view, a, b, color, dashed=False), dot3(view, xyz, color)
  arc3(view, axis, u, angle, radius, color)   arc from direction u, turning right-handedly about axis
  disc3(view, u, v, radius, color, opacity)   a filled disc spanned by orthonormal u, v (an orbital plane)
  label3(view, tex, xyz, color, size)         MathTex pinned to a 3D point (screen-aligned)
  axes3(view, L)            I, J, K arrows with labels -> VGroup
  Every factory accepts callables for its geometry, so pieces can move with ValueTrackers.
  grow(m) / k-tracker: arrow3, curve and arc3 have .k (0..1 drawn fraction): self.play(m.k.animate.set_value(1)).

Orbit math (radians; C rows are p-hat, q-hat, h-hat written in ECI):
  C1(x), C3(x)  elementary rotations (course convention, rows = new axes in old)
  cpn(Om, i, w) = C3(w) @ C1(i) @ C3(Om)
  orbit(a, e, Om, i, w) -> f(theta) in ECI;  rv_perifocal(a, e, theta) -> (r_P, v_P)
Facts asserted at import: the Molniya numbers of Kluever Example 3.1.
"""
from mtk import *
import mtk.core as core
from mtk.view3d import SurfaceImage, sphere_grid, _cam

core.FONT = "Lato"   # Avenir Next is not installed here
MU = 3.986e5


def C1(x):
    c, s = np.cos(x), np.sin(x)
    return np.array([[1, 0, 0], [0, c, s], [0, -s, c]])


def C3(x):
    c, s = np.cos(x), np.sin(x)
    return np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])


def cpn(Om, i, w):
    return C3(w) @ C1(i) @ C3(Om)


def orbit(a, e, Om, i, w):
    C = cpn(Om, i, w)
    p = a * (1 - e * e)

    def f(t):
        r = p / (1 + e * np.cos(t))
        return r * (np.cos(t) * C[0] + np.sin(t) * C[1])
    return f


def rv_perifocal(a, e, th, mu=MU):
    p = a * (1 - e * e)
    h = np.sqrt(mu * p)
    r = p / (1 + e * np.cos(th))
    return np.array([r * np.cos(th), r * np.sin(th), 0.0]), mu / h * np.array([-np.sin(th), e + np.cos(th), 0.0])


# ---- facts: Kluever Example 3.1 (Molniya) ----
R0 = np.array([9031.5, -5316.9, -1647.2])
V0 = np.array([-2.8640, 5.1112, -5.0805])
_r, _v = np.linalg.norm(R0), np.linalg.norm(V0)
_E = _v ** 2 / 2 - MU / _r
_h = np.cross(R0, V0)
_e = np.cross(V0, _h) / MU - R0 / _r
assert np.isclose(-MU / (2 * _E), 26563.6, atol=0.5) and np.isclose(np.linalg.norm(_e), 0.7411, atol=1e-4)
_C = np.vstack([_e / np.linalg.norm(_e), np.cross(_h / np.linalg.norm(_h), _e / np.linalg.norm(_e)), _h / np.linalg.norm(_h)])
assert np.isclose(np.degrees(np.arccos(_C[2, 2])), 63.4, atol=0.05)
assert np.isclose(np.degrees(np.arctan2(_C[2, 0], -_C[2, 1])), 145.0, atol=0.05)
assert np.isclose(np.degrees(np.arctan2(_C[0, 2], _C[1, 2])), -90.0, atol=0.05)
assert R0 @ V0 < 0 and np.isclose(np.degrees(np.arccos(_e @ R0 / (np.linalg.norm(_e) * _r))), 80.0, atol=0.05)


def _v3(x):
    return np.asarray(x() if callable(x) else x, float)


class View:
    def __init__(self, elev=22, azim=-55, scale=1.0, center=(-3.2, -0.3)):
        self.elev, self.azim, self.scale = ValueTracker(elev), ValueTracker(azim), ValueTracker(scale)
        self.c = np.array([center[0], center[1], 0.0])

    def basis(self):
        return _cam(self.elev.get_value(), self.azim.get_value())

    def p(self, xyz):
        _, e1, e2 = self.basis()
        q = _v3(xyz)
        s = self.scale.get_value()
        return self.c + s * (np.dot(e1, q) * RIGHT + np.dot(e2, q) * UP)

    def depth(self, xyz):
        return float(np.dot(self.basis()[0], _v3(xyz)))

    def hidden(self, xyz, R):
        """Behind a globe of radius R at the origin?"""
        q = _v3(xyz)
        d, e1, e2 = self.basis()
        return np.dot(d, q) < 0 and np.hypot(np.dot(e1, q), np.dot(e2, q)) < R

    def turn(self, d_azim, run_time=4):
        return self.azim.animate(run_time=run_time, rate_func=smooth).increment_value(d_azim)


def globe(view, R=1.0, color="#2b6cb0"):
    g = SurfaceImage(sphere_grid(150), width=1.0, elev=view.elev.get_value(), azim=view.azim.get_value(),
                     base=color, lines=(6, 12), px=420)

    def upd(m):
        m.redraw(elev=view.elev.get_value(), azim=view.azim.get_value())
        m.set_width(2 * 1.05 * R * view.scale.get_value())
        m.move_to(view.p(ORIGIN))
    g.add_updater(upd)
    upd(g)
    return g


def _tracked(make, k=1.0):
    kt = ValueTracker(k)
    m = always_redraw(lambda: make(kt.get_value()))
    m.k = kt
    return m


def curve(view, f, t0, t1, color, width=4, R=None, n=160, k=1.0):
    def make(g):
        a, b = (t0() if callable(t0) else t0), (t1() if callable(t1) else t1)
        ts = np.linspace(a, a + max(g, 1e-4) * (b - a), n)
        pts = [f(t) for t in ts]
        out = VGroup()
        run, hid = [], None
        for q in pts:
            h = bool(R) and view.hidden(q, R)
            if hid is None or h == hid:
                run.append(view.p(q))
            else:
                run.append(view.p(q))
                out.add(_poly(run, color, width, hid))
                run = [view.p(q)]
            hid = h
        if len(run) > 1:
            out.add(_poly(run, color, width, hid))
        return out
    return _tracked(make, k)


def _poly(pts, color, width, hid):
    m = VMobject(stroke_color=color, stroke_width=width * (0.6 if hid else 1.0))
    m.set_points_smoothly(pts) if len(pts) > 2 else m.set_points_as_corners(pts)
    if hid:
        m.set_stroke(opacity=0.25)
    return m


def arrow3(view, a, b, color, width=5, tip=0.2, k=1.0):
    def make(g):
        s = _v3(a)
        e = s + max(g, 1e-3) * (_v3(b) - s)
        p0, p1 = view.p(s), view.p(e)
        if np.linalg.norm(p1 - p0) < 1e-3:
            p1 = p0 + 1e-3 * RIGHT
        return Arrow(p0, p1, buff=0, color=color, stroke_width=width, tip_length=tip,
                     max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=1000)
    return _tracked(make, k)


def line3(view, a, b, color, width=3, dashed=False, k=1.0):
    def make(g):
        s = _v3(a)
        e = s + max(g, 1e-3) * (_v3(b) - s)
        p0, p1 = view.p(s), view.p(e)
        if np.linalg.norm(p1 - p0) < 1e-3:
            p1 = p0 + 1e-3 * RIGHT
        return (DashedLine(p0, p1, color=color, stroke_width=width, dash_length=0.08) if dashed
                else Line(p0, p1, color=color, stroke_width=width))
    return _tracked(make, k)


def dot3(view, xyz, color, radius=0.07):
    return always_redraw(lambda: Dot(view.p(xyz), radius=radius, color=color))


def arc3(view, axis, u, angle, radius, color, width=4, k=1.0):
    def f(t):
        ax = _v3(axis)
        ax = ax / np.linalg.norm(ax)
        uu = _v3(u)
        uu = uu - ax * np.dot(uu, ax)
        uu = uu / np.linalg.norm(uu)
        return radius * (np.cos(t) * uu + np.sin(t) * np.cross(ax, uu))
    return curve(view, f, 0.0, lambda: float(angle() if callable(angle) else angle), color, width, n=40, k=k)


def disc3(view, u, v, radius, color, opacity=0.12, n=60):
    def make():
        uu, vv = _v3(u), _v3(v)
        pts = [view.p(radius * (np.cos(t) * uu + np.sin(t) * vv)) for t in np.linspace(0, TAU, n, endpoint=False)]
        return Polygon(*pts, stroke_width=1, stroke_color=color, stroke_opacity=0.4, fill_color=color,
                       fill_opacity=opacity)
    return always_redraw(make)


def label3(view, tex, xyz, color=INK, size=34):
    m = M(tex, size=size, color=color)
    m.add_updater(lambda x: x.move_to(view.p(xyz)))
    m.update()
    return m


def axes3(view, L=2.4, color=INK2):
    g = VGroup()
    for vec, name in ((RIGHT, r"\hat I"), (UP, r"\hat J"), (OUT, r"\hat K")):
        d = np.array([vec[0], vec[1], vec[2]], float)
        if name == r"\hat J":
            d = np.array([0, 1.0, 0])
        g.add(arrow3(view, ORIGIN, L * d, color, 4))
        g.add(label3(view, name, (L + 0.32) * d, color, 32))
    return g
