"""Shared styling, narration sync and geometry helpers for the scenes."""
import json
import os
from contextlib import contextmanager

import numpy as np
from manim import *  # noqa: F401,F403

from narration import SCRIPT

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(HERE, "audio")
_manifest_path = os.path.join(AUDIO_DIR, "manifest.json")
MANIFEST = json.load(open(_manifest_path)) if os.path.exists(_manifest_path) else {}
SEGMENT_TEXT = {k: t for segs in SCRIPT.values() for k, t in segs}

WORDS_PER_SEC = 2.8   # fallback pacing when audio has not been generated
PAD = 0.35            # breathing room after each narration clip

# ---------------------------------------------------------------- palette
BG = "#0E0E12"
N_COL = "#C8C8C8"     # inertial frame N (and A)
B_COL = "#58C4DD"     # body frame B  (3b1b blue)
P_COL = "#FC6255"     # intermediate frame P (red)
Q_COL = "#83C167"     # intermediate frame Q (green)
R_COL = "#FFD644"     # the vector r (yellow)
W_COL = "#FF9A3C"     # angular velocity omega (orange)
V_COL = "#E07BE0"     # derived quantities (pink/purple)
DIM = "#6B6B78"

config.background_color = BG

TEX = TexTemplate()
TEX.add_to_preamble(r"\usepackage{amsmath}\usepackage{amssymb}")


def T(*s, **kw):
    """MathTex with the project template."""
    kw.setdefault("tex_template", TEX)
    return MathTex(*s, **kw)


def Tx(*s, **kw):
    kw.setdefault("tex_template", TEX)
    return Tex(*s, **kw)


# ------------------------------------------------------- rotation helpers
def C1(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1, 0, 0], [0, c, s], [0, -s, c]])


def C2(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]])


def C3(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])


def euler321(psi, th, ph):
    """C_BA for a 3-2-1 sequence. Rows are b_i written in A components."""
    return C1(ph) @ C2(th) @ C3(psi)


# ---------------------------------------------------------- narration sync
class VoiceMixin:
    """Adds `with self.voice("seg_id"):` blocks that play a narration clip and
    pad the block so the next segment starts after the clip ends."""

    _seg_end = 0.0
    narration_manifest = MANIFEST
    narration_text = SEGMENT_TEXT
    narration_audio_dir = AUDIO_DIR
    narration_pad = PAD

    @contextmanager
    def voice(self, key):
        entry = self.narration_manifest.get(key)
        path = os.path.join(self.narration_audio_dir, entry["file"]) if entry else None
        if path and os.path.exists(path):
            dur = entry["duration"]
            self.add_sound(path)
        else:
            dur = len(self.narration_text[key].split()) / WORDS_PER_SEC
        start = self.renderer.time
        self._seg_end = start + dur + self.narration_pad
        yield dur
        rem = self._seg_end - self.renderer.time
        if rem > 1 / 30:
            self.wait(rem)

    def left(self, minimum=0.5):
        """Seconds left in the current narration segment."""
        return max(minimum, self._seg_end - self.renderer.time)

    def hold(self, minimum=0.1):
        """Wait out the rest of the current segment now."""
        self.wait(self.left(minimum))


class Scene2D(VoiceMixin, Scene):
    pass


class Scene3D(VoiceMixin, ThreeDScene):
    def hud(self, *mobs):
        """Register mobjects as fixed-in-frame (screen space) without adding them."""
        self.add_fixed_in_frame_mobjects(*mobs)
        self.remove(*mobs)
        return mobs[0] if len(mobs) == 1 else mobs

    def label3d(self, tex, pos_func, color, scale=0.75):
        lab = T(tex, color=color).scale(scale)
        lab.move_to(pos_func())
        self.add_fixed_orientation_mobjects(lab)
        self.remove(lab)
        lab.add_updater(lambda m: m.move_to(pos_func()))
        return lab


def arrow3d(start, end, color, thick=0.022):
    return Arrow3D(start=np.array(start, dtype=float), end=np.array(end, dtype=float),
                   color=color, thickness=thick, height=0.22, base_radius=0.065,
                   resolution=8)


def frame_arrows(M, color, length=2.4, origin=ORIGIN, thick=0.022):
    """Three arrows along the rows of M (basis vectors in world coordinates)."""
    o = np.array(origin, dtype=float)
    return VGroup(*[arrow3d(o, o + length * np.array(M[i]), color, thick) for i in range(3)])


def arc3d(axis, u, angle, radius, color, stroke=3):
    """Arc of `angle` radians starting at unit vector u, turning right-handedly about axis."""
    axis = np.array(axis, float) / np.linalg.norm(axis)
    u = np.array(u, float)
    u = u - axis * np.dot(u, axis)
    u /= np.linalg.norm(u)
    w = np.cross(axis, u)
    return ParametricFunction(
        lambda t: radius * (np.cos(t) * u + np.sin(t) * w),
        t_range=[0, angle, angle / 40 if angle else 0.01], color=color, stroke_width=stroke)


def bracket_column(values, fmt="{:.2f}", color=WHITE, scale=0.8):
    """A column vector of numbers as MathTex."""
    rows = r"\\".join(fmt.format(v) for v in values)
    return T(r"\begin{bmatrix}" + rows + r"\end{bmatrix}", color=color).scale(scale)


def live_column(funcs, color=WHITE, num_decimal_places=2, scale=0.8):
    """Column vector with live DecimalNumbers driven by funcs (list of callables)."""
    nums = VGroup(*[DecimalNumber(f(), num_decimal_places=num_decimal_places,
                                  include_sign=True, color=color).scale(scale)
                    for f in funcs])
    nums.arrange(DOWN, buff=0.22, aligned_edge=RIGHT)
    for n, f in zip(nums, funcs):
        n.add_updater(lambda m, f=f: m.set_value(f()))
    left = T("[", color=color).stretch_to_fit_height(nums.height + 0.3)
    right = T("]", color=color).stretch_to_fit_height(nums.height + 0.3)
    left.next_to(nums, LEFT, buff=0.12)
    right.next_to(nums, RIGHT, buff=0.12)
    return VGroup(left, nums, right)


def chapter_card(number, title):
    num = Tx(f"Part {number}", color=DIM).scale(0.8)
    t = Tx(title).scale(1.3)
    g = VGroup(num, t).arrange(DOWN, buff=0.3)
    line = Line(LEFT * 3, RIGHT * 3, color=B_COL, stroke_width=2).next_to(g, DOWN, buff=0.3)
    return VGroup(g, line)


def pick_glyphs(mob, x0, x1, y0, y1, max_h=0.45):
    """Glyphs of a Tex mobject whose centers fall in a fractional box of its bounds
    (fractions measured from left/bottom). Tall glyphs such as brackets are skipped."""
    l, r = mob.get_left()[0], mob.get_right()[0]
    b, t = mob.get_bottom()[1], mob.get_top()[1]
    out = VGroup()
    for g in mob.family_members_with_points():
        c = g.get_center()
        fx, fy = (c[0] - l) / (r - l), (c[1] - b) / (t - b)
        if x0 <= fx <= x1 and y0 <= fy <= y1 and g.height < max_h * mob.height:
            out.add(g)
    return out
