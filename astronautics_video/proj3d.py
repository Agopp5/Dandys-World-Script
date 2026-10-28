"""A lightweight 3D look for 2D Manim scenes.

Manim's surface-based 3D objects (Arrow3D, Sphere) are very slow to rasterize
with the Cairo renderer. Here every 3D object is an ordinary 2D VMobject whose
points are recomputed from a simple perspective camera on every frame, which
renders orders of magnitude faster and lets equations live in normal screen
space.
"""
from common import *  # noqa: F401,F403


def cv(c):
    return c() if callable(c) else c


def val(x):
    return np.array(x() if callable(x) else x, dtype=float)


def fade(m, o):
    """Scale stroke and fill opacity of every part (open curves stay unfilled)."""
    if o < 0.999:
        for sm in m.family_members_with_points():
            sm.set_stroke(opacity=sm.get_stroke_opacity() * o)
            sm.set_fill(opacity=sm.get_fill_opacity() * o)
    return m


class Cam:
    def __init__(self, phi=68, theta=28, scale=1.0, center=ORIGIN, focal=16.0):
        self.phi = ValueTracker(np.radians(phi))
        self.theta = ValueTracker(np.radians(theta))
        self.scale = ValueTracker(scale)
        self.cx = ValueTracker(center[0])
        self.cy = ValueTracker(center[1])
        self.focal = focal
        self._spin = None

    # camera basis ---------------------------------------------------------
    def basis(self):
        ph, th = self.phi.get_value(), self.theta.get_value()
        d = np.array([np.sin(ph) * np.cos(th), np.sin(ph) * np.sin(th), np.cos(ph)])
        r = np.array([-np.sin(th), np.cos(th), 0.0])
        u = np.cross(d, r)
        return d, r, u

    def depth(self, pt):
        d, _, _ = self.basis()
        return float(np.dot(val(pt), d))

    def p(self, pt):
        pt = val(pt)
        d, r, u = self.basis()
        k = self.focal / (self.focal - np.dot(pt, d))
        s = self.scale.get_value() * k
        return np.array([self.cx.get_value() + s * np.dot(pt, r),
                         self.cy.get_value() + s * np.dot(pt, u), 0.0])

    def trackers(self):
        return [self.phi, self.theta, self.scale, self.cx, self.cy]

    def start_spin(self, scene, rate=0.1):
        self.stop_spin()
        self._spin = lambda m, dt: m.increment_value(rate * dt)
        self.theta.add_updater(self._spin)
        scene.add(self.theta)

    def stop_spin(self):
        if self._spin:
            self.theta.remove_updater(self._spin)
            self._spin = None


class Draw:
    """Factory for camera-driven mobjects. Each has `.k` (grow 0..1) and
    `.op` (opacity 0..1) ValueTrackers that animations can drive."""

    def __init__(self, cam):
        self.cam = cam

    def _wrap(self, make, k=1.0, op=1.0):
        kt, ot = ValueTracker(k), ValueTracker(op)
        m = always_redraw(lambda: fade(make(kt.get_value()), ot.get_value()))
        m.k, m.op = kt, ot
        return m

    def arrow(self, start, end, color, width=5, tip=0.2, k=1.0, op=1.0):
        cam = self.cam

        def make(g):
            s = val(start)
            e = s + g * (val(end) - s)
            a, b = cam.p(s), cam.p(e)
            if np.linalg.norm(b - a) < 1e-3:
                b = a + RIGHT * 1e-3
            return Arrow(a, b, buff=0, color=cv(color), stroke_width=width, tip_length=tip,
                         max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=1000)
        return self._wrap(make, k, op)

    def line(self, start, end, color, width=3, dashed=False, k=1.0, op=1.0):
        cam = self.cam

        def make(g):
            s = val(start)
            e = s + g * (val(end) - s)
            a, b = cam.p(s), cam.p(e)
            if np.linalg.norm(b - a) < 1e-3:
                b = a + RIGHT * 1e-3
            if dashed:
                return DashedLine(a, b, color=cv(color), stroke_width=width, dash_length=0.08)
            return Line(a, b, color=cv(color), stroke_width=width)
        return self._wrap(make, k, op)

    def curve(self, func, t_range, color, width=3, n=60, k=1.0, op=1.0):
        """func(t) -> 3D point; t_range may be a callable returning (t0, t1)."""
        cam = self.cam

        def make(g):
            t0, t1 = t_range() if callable(t_range) else t_range
            t1 = t0 + g * (t1 - t0)
            ts = np.linspace(t0, t1, n) if abs(t1 - t0) > 1e-6 else np.array([t0, t0 + 1e-6])
            m = VMobject(stroke_color=cv(color), stroke_width=width)
            m.set_points_smoothly([cam.p(func(t)) for t in ts])
            return m
        return self._wrap(make, k, op)

    def polygon(self, pts_func, color, fill_opacity=0.3, op=1.0):
        cam = self.cam

        def make(g):
            pts = [cam.p(q) for q in val(pts_func)]
            return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=fill_opacity * g)
        return self._wrap(make, 1.0, op)

    def dot(self, pos, color, radius=0.07, op=1.0):
        cam = self.cam
        return self._wrap(lambda g: Dot(cam.p(pos), radius=radius * max(g, 1e-3), color=color), 1.0, op)

    def label(self, tex, pos, color=WHITE, scale=0.75, op=0.0, mob=None):
        cam = self.cam
        m = mob if mob is not None else T(tex, color=color).scale(scale)
        ot = ValueTracker(op)
        m.op = ot
        m.add_updater(lambda x: x.move_to(cam.p(pos)).set_opacity(ot.get_value()))
        m.update()
        return m

    def frame(self, M, color, length=2.4, names=None, width=5, origin=ORIGIN, k=0.0, label_op=0.0):
        """Three arrows along rows of M (callable or array) with optional labels."""
        o = val(origin)
        arrows = VGroup(*[self.arrow(o, (lambda i=i: o + length * val(M)[i]), color, width, k=k)
                          for i in range(3)])
        labels = VGroup()
        if names:
            for i, nm in enumerate(names):
                if nm:
                    labels.add(self.label(nm, (lambda i=i: o + (length + 0.32) * val(M)[i]), color, op=label_op))
        return arrows, labels

    def arc(self, axis, u, angle, radius, color, width=3):
        """Arc starting at u, turning right-handedly about axis by angle (callables ok)."""
        def f(t):
            ax = val(axis)
            ax = ax / np.linalg.norm(ax)
            uu = val(u)
            uu = uu - ax * np.dot(uu, ax)
            uu = uu / np.linalg.norm(uu)
            w = np.cross(ax, uu)
            return radius * (np.cos(t) * uu + np.sin(t) * w)
        return self.curve(f, lambda: (0.0, float(val(angle)) + 1e-4), color, width, n=30)

    def sphere(self, center, R, color, rot=lambda: 0.0, n_lat=7, n_lon=12, fill="#13294B",
               width=1.6, tilt=None):
        """Wireframe globe; rot() spins it about the world z axis. Back lines are hidden."""
        cam = self.cam
        c = val(center)

        def make(g):
            d, _, _ = cam.basis()
            grp = VGroup()
            ctr = cam.p(c)
            rad = np.linalg.norm(cam.p(c + R * np.cross(d, [0, 0, 1]) / max(1e-6, np.linalg.norm(np.cross(d, [0, 0, 1])))) - ctr) \
                if abs(d[2]) < 0.999 else np.linalg.norm(cam.p(c + R * np.array([1, 0, 0])) - ctr)
            grp.add(Circle(radius=rad, color=color, stroke_width=2.5, fill_color=fill, fill_opacity=1).move_to(ctr))
            a0 = rot()
            curves = []
            for i in range(1, n_lat):
                lat = -PI / 2 + PI * i / n_lat
                curves.append([c + R * np.array([np.cos(lat) * np.cos(t), np.cos(lat) * np.sin(t), np.sin(lat)])
                               for t in np.linspace(0, TAU, 73)])
            for j in range(n_lon):
                lon = a0 + TAU * j / n_lon
                curves.append([c + R * np.array([np.cos(t) * np.cos(lon), np.cos(t) * np.sin(lon), np.sin(t)])
                               for t in np.linspace(-PI / 2, PI / 2, 37)])
            for pts in curves:
                run = []
                for q in pts:
                    if np.dot(q - c, d) > 0:
                        run.append(cam.p(q))
                    else:
                        if len(run) > 1:
                            grp.add(VMobject(stroke_color=color, stroke_width=width, stroke_opacity=0.55)
                                    .set_points_as_corners(run))
                        run = []
                if len(run) > 1:
                    grp.add(VMobject(stroke_color=color, stroke_width=width, stroke_opacity=0.55)
                            .set_points_as_corners(run))
            return grp
        return self._wrap(make, 1.0, 1.0)


def grow(*mobs, to=1.0):
    return [m.k.animate.set_value(to) for m in mobs]


def show(*mobs, to=1.0):
    return [m.op.animate.set_value(to) for m in mobs]


def hide(*mobs):
    return [m.op.animate.set_value(0.0) for m in mobs]


def flat(*groups):
    out = []
    for g in groups:
        if hasattr(g, "op"):
            out.append(g)
        else:
            out.extend(flat(*g.submobjects))
    return out
