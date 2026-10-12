"""Shared helpers for the AERSP 309 two-body orbital mechanics series."""
import importlib.util
import json
import os
import sys

O_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(O_HERE), "lesson"))

from lcommon import *  # noqa: F401,F403,E402

_spec = importlib.util.spec_from_file_location("orbits_narration", os.path.join(O_HERE, "narration.py"))
_narr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_narr)
O_AUDIO = os.path.join(O_HERE, "audio")
_mp = os.path.join(O_AUDIO, "manifest.json")
O_MANIFEST = json.load(open(_mp)) if os.path.exists(_mp) else {}
O_TEXT = {k: t for segs in _narr.SCRIPT.values() for k, t in segs}

SUN = "#FFC94D"
EARTH = "#4A90D9"
ORB = "#D9DCE3"         # orbit curves
AREA = "#58C4DD"        # swept areas
VEL = "#FC6255"         # velocity arrows
ER_COL = "#FFD644"      # e_r
ET_COL = "#83C167"      # e_theta
H_COL = "#FF9A3C"       # h / e_3
E_VEC = "#E07BE0"       # eccentricity vector


class OLesson(Lesson):
    narration_manifest = O_MANIFEST
    narration_text = O_TEXT
    narration_audio_dir = O_AUDIO


def o_title(scene, number, title, sub):
    n = Tx(f"AERSP 309 $\\cdot$ Two-Body Orbital Mechanics $\\cdot$ Part {number}", color=B_COL).scale(0.72)
    t = Tx(title).scale(1.25)
    st = Tx(sub, color=DIM).scale(0.66)
    VGroup(n, t, st).arrange(DOWN, buff=0.35)
    line = Line(LEFT * 4.0, RIGHT * 4.0, color=B_COL, stroke_width=2).next_to(t, DOWN, buff=0.18)
    st.next_to(line, DOWN, buff=0.3)
    grp = VGroup(n, t, line, st)
    scene.play(FadeIn(n, shift=DOWN * 0.2), Write(t), run_time=1.5)
    scene.play(Create(line), FadeIn(st), run_time=1.0)
    return grp


# ------------------------------------------------------------- orbit maths
def kepler_E(M, e, tol=1e-12):
    """Solve M = E - e sin E (elliptic)."""
    E = M if e < 0.8 else np.pi
    for _ in range(60):
        dE = (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
        E -= dE
        if abs(dE) < tol:
            break
    return E


def theta_from_M(M, e):
    """True anomaly for mean anomaly M on an ellipse (continuous in M)."""
    k = np.floor((M + np.pi) / TAU)
    Mr = M - k * TAU
    E = kepler_E(Mr, e)
    th = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    return th + k * TAU


def M_from_theta(th, e):
    E = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(th / 2), np.sqrt(1 + e) * np.cos(th / 2))
    return E - e * np.sin(E)


class Orb:
    """Screen mapping for an orbit drawn in its perifocal plane: focus at `focus`,
    periapsis along +x (or rotated by `rot`), lengths multiplied by `k`."""

    def __init__(self, focus=ORIGIN, k=1.0, rot=0.0):
        self.f = np.array([focus[0], focus[1], 0.0])
        self.k = k
        self.rot = rot

    def P(self, x, y):
        c, s = np.cos(self.rot), np.sin(self.rot)
        return self.f + self.k * np.array([c * x - s * y, s * x + c * y, 0.0])

    def at(self, p, e, th):
        r = p / (1 + e * np.cos(th))
        return self.P(r * np.cos(th), r * np.sin(th))

    def conic(self, p, e, th0=None, th1=None, color=ORB, width=3, n=200):
        if th0 is None:
            if e < 1:
                th0, th1 = -PI, PI
            else:
                lim = np.arccos(-1 / e) - 0.06 if e > 1 else PI - 0.25
                th0, th1 = -lim, lim
        ths = np.linspace(th0, th1, n)
        m = VMobject(stroke_color=color, stroke_width=width)
        m.set_points_smoothly([self.at(p, e, t) for t in ths])
        return m

    def sector(self, p, e, th0, th1, color=AREA, opacity=0.4, n=60):
        pts = [self.f] + [self.at(p, e, t) for t in np.linspace(th0, th1, n)]
        return Polygon(*pts, stroke_width=1.5, stroke_color=color, fill_color=color, fill_opacity=opacity)

    def unit(self, th):
        c, s = np.cos(self.rot + th), np.sin(self.rot + th)
        return np.array([c, s, 0.0])


def sun(pos, r=0.16):
    glow = VGroup(*[Dot(pos, radius=r * (1 + 0.5 * i), color=SUN, fill_opacity=0.18 / (i + 1)) for i in range(4)])
    return VGroup(glow, Dot(pos, radius=r, color=SUN))


def earth(pos, r=0.22):
    return VGroup(Circle(radius=r, color=EARTH, fill_color="#16335C", fill_opacity=1, stroke_width=2.5).move_to(pos),
                  Arc(radius=r * 0.6, start_angle=0.4, angle=1.6, color=EARTH, stroke_width=1.5).move_to(pos + 0.03 * UP))


def planet(pos, color=B_COL, r=0.08):
    return Dot(pos, radius=r, color=color)


def vlabel(tex, color, scale=0.6):
    return T(tex, color=color).scale(scale)


def num_card(rows, scale=0.6, color=WHITE):
    """A small boxed list of given data."""
    g = VGroup(*[T(r, color=color).scale(scale) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    box = SurroundingRectangle(g, color=DIM, buff=0.18, corner_radius=0.08)
    return VGroup(box, g)
