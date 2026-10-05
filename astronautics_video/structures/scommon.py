"""Shared helpers for the AERSP 301 shear-of-beams lesson series."""
import importlib.util
import json
import os
import sys

S_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(S_HERE), "lesson"))

from lcommon import *  # noqa: F401,F403,E402

_spec = importlib.util.spec_from_file_location("structures_narration", os.path.join(S_HERE, "narration.py"))
_narr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_narr)
S_AUDIO = os.path.join(S_HERE, "audio")
_mp = os.path.join(S_AUDIO, "manifest.json")
S_MANIFEST = json.load(open(_mp)) if os.path.exists(_mp) else {}
S_TEXT = {k: t for segs in _narr.SCRIPT.values() for k, t in segs}

WALL = "#D9DCE3"
Q_FILL = "#E07BE0"      # shear-flow diagrams
LOAD = "#FF9A3C"        # applied loads
SC_COL = "#FFD644"      # shear centre


class SLesson(Lesson):
    narration_manifest = S_MANIFEST
    narration_text = S_TEXT
    narration_audio_dir = S_AUDIO


def s_title(scene, number, title, sub):
    n = Tx(f"AERSP 301 $\\cdot$ Shear of Beams $\\cdot$ Part {number}", color=B_COL).scale(0.75)
    t = Tx(title).scale(1.3)
    st = Tx(sub, color=DIM).scale(0.68)
    VGroup(n, t, st).arrange(DOWN, buff=0.35)
    line = Line(LEFT * 3.8, RIGHT * 3.8, color=B_COL, stroke_width=2).next_to(t, DOWN, buff=0.18)
    st.next_to(line, DOWN, buff=0.3)
    grp = VGroup(n, t, line, st)
    scene.play(FadeIn(n, shift=DOWN * 0.2), Write(t), run_time=1.5)
    scene.play(Create(line), FadeIn(st), run_time=1.0)
    return grp


class Sec:
    """Maps section coordinates (in units of a, h, ...) to the screen."""

    def __init__(self, origin, scale):
        self.o = np.array([origin[0], origin[1], 0.0])
        self.k = scale

    def P(self, x, y):
        return self.o + self.k * np.array([x, y, 0.0])

    def wall(self, p0, p1, tf=1.0, color=WALL):
        return Line(self.P(*p0), self.P(*p1), color=color, stroke_width=5 * tf, cap_style=CapStyleType.ROUND)

    def dot(self, x, y, color=WHITE, r=0.06):
        return Dot(self.P(x, y), color=color, radius=r)

    def label(self, tex, x, y, direction=UP, color=WHITE, scale=0.6, buff=0.12):
        return T(tex, color=color).scale(scale).next_to(self.P(x, y), direction, buff=buff)


def _frame(sec, p0, p1):
    a, b = sec.P(*p0), sec.P(*p1)
    tvec = (b - a) / np.linalg.norm(b - a)
    nvec = np.array([-tvec[1], tvec[0], 0.0])
    return a, b, tvec, nvec


def flow_fill(sec, p0, p1, qfun, scale, color=Q_FILL, side=1, n=40, opacity=0.35):
    """Shaded shear-flow diagram on one wall: offset |q|*scale along the wall normal.
    qfun takes the fraction u in [0,1] from p0 to p1. side=+1/-1 picks the normal."""
    a, b, tvec, nvec = _frame(sec, p0, p1)
    us = np.linspace(0, 1, n)
    base = [a + u * (b - a) for u in us]
    top = [base[i] + side * nvec * scale * qfun(us[i]) for i in range(n)]
    poly = Polygon(*(base + top[::-1]), stroke_width=0, fill_color=color, fill_opacity=opacity)
    edge = VMobject(stroke_color=color, stroke_width=2.5).set_points_smoothly(top)
    return VGroup(poly, edge)


def flow_arrows(sec, p0, p1, qfun, n=4, color=Q_FILL, length=0.4, side=0.0):
    """Arrows along a wall showing the direction of q (positive = p0 -> p1)."""
    a, b, tvec, nvec = _frame(sec, p0, p1)
    g = VGroup()
    for i in range(n):
        u = (i + 0.5) / n
        q = qfun(u)
        if abs(q) < 1e-6:
            continue
        c = a + u * (b - a) + side * nvec
        d = np.sign(q) * tvec * length / 2
        g.add(Arrow(c - d, c + d, buff=0, color=color, stroke_width=4, tip_length=0.15,
                    max_tip_length_to_length_ratio=0.5))
    return g


def load_arrow(start, end, label, color=LOAD, scale=0.7, direction=RIGHT):
    ar = Arrow(start, end, buff=0, color=color, stroke_width=6, tip_length=0.22)
    lab = T(label, color=color).scale(scale).next_to(ar.get_end(), direction, buff=0.1)
    return VGroup(ar, lab)


def dim_line(p0, p1, tex, offset, color=DIM, scale=0.55):
    """A dimension line offset from the segment p0-p1 with a centred label."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    off = np.array([offset[0], offset[1], 0.0])
    ln = DoubleArrow(p0 + off, p1 + off, buff=0, color=color, stroke_width=2, tip_length=0.12,
                     max_tip_length_to_length_ratio=0.2)
    lab = T(tex, color=color).scale(scale).move_to((p0 + p1) / 2 + off * 1.0 + normalize(off) * 0.25)
    return VGroup(ln, lab)
