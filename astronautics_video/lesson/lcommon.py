"""Shared helpers for the step-by-step lesson series."""
import importlib.util
import json
import os
import sys

L_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(L_HERE))

from common import *  # noqa: F401,F403,E402
from proj3d import Cam, Draw, grow, show, hide, flat  # noqa: F401,E402

_spec = importlib.util.spec_from_file_location("lesson_narration", os.path.join(L_HERE, "narration.py"))
_narr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_narr)

L_AUDIO = os.path.join(L_HERE, "audio")
_mp = os.path.join(L_AUDIO, "manifest.json")
L_MANIFEST = json.load(open(_mp)) if os.path.exists(_mp) else {}
L_TEXT = {k: t for segs in _narr.SCRIPT.values() for k, t in segs}

REASON = "#8C8C9A"


class Lesson(VoiceMixin, Scene):
    narration_manifest = L_MANIFEST
    narration_text = L_TEXT
    narration_audio_dir = L_AUDIO
    narration_pad = 0.7


def mat(rows, color=WHITE, h_buff=1.25, v_buff=0.75, scale=0.75):
    """A Matrix of TeX strings whose entries/rows/columns can be addressed."""
    m = Matrix(rows, element_to_mobject=lambda e: T(e, color=color),
               h_buff=h_buff, v_buff=v_buff, bracket_h_buff=0.2)
    return m.scale(scale)


class Board:
    """A column of derivation lines. Each line can carry a grey reason on its
    right. The board scrolls up when it reaches the bottom."""

    def __init__(self, scene, left=-6.5, top=2.6, bottom=-3.6, right=6.9, scale=0.8, buff=0.38, ceiling=3.2):
        self.s = scene
        self.ceiling = ceiling
        self.left, self.top, self.bottom, self.right = left, top, bottom, right
        self.scale, self.buff = scale, buff
        self.items = VGroup()          # lines and their reasons
        self.lines = []

    def _place(self, m, indent=0.0, gap=None):
        if self.lines:
            m.next_to(self.lines[-1], DOWN, buff=self.buff if gap is None else gap)
        else:
            m.move_to([0, self.top, 0], aligned_edge=UP)
        m.align_to([self.left + indent, 0, 0], LEFT)

    def line(self, *tex, reason=None, indent=0.0, color=WHITE, rt=1.4, gap=None, mob=None,
             from_mob=None, scale=None, anim=True, below=False):
        m = mob if mob is not None else T(*tex, color=color).scale(scale or self.scale)
        max_w = self.right - self.left - indent - (3.2 if reason and not below else 0)
        if m.width > max_w:
            m.scale_to_fit_width(max_w)
        self._place(m, indent, gap)
        r = None
        if reason:
            r = Tx(reason, color=REASON).scale(0.52)
            r.next_to(m, RIGHT, buff=0.45)
            if below:
                r.next_to(m, DOWN, buff=0.12).align_to(m, LEFT)
            elif r.get_right()[0] > self.right:
                r.scale_to_fit_width(max(0.5, self.right - m.get_right()[0] - 0.5))
                r.next_to(m, RIGHT, buff=0.45)
        overflow = self.bottom - (r.get_bottom()[1] if (r is not None and below) else m.get_bottom()[1])
        if overflow > 0:
            shift = UP * (overflow + 0.1)
            m.shift(shift)
            if r:
                r.shift(shift)
            gone = [it for it in self.items if it.get_top()[1] + shift[1] > self.ceiling]
            keep = [it for it in self.items if it not in gone]
            self.s.play(*[it.animate.shift(shift) for it in keep], *[FadeOut(it, shift=shift) for it in gone], run_time=0.6)
            for it in gone:
                self.items.remove(it)
                self.s.remove(it)
        self.lines.append(VGroup(m, r) if (r is not None and below) else m)
        self.items.add(m)
        if anim:
            if from_mob is not None:
                self.s.play(TransformFromCopy(from_mob, m), run_time=rt)
            else:
                self.s.play(Write(m), run_time=rt)
            if r:
                self.s.play(FadeIn(r, shift=LEFT * 0.15), run_time=0.5)
        else:
            self.s.add(m)
            if r:
                self.s.add(r)
        if r:
            self.items.add(r)
        return m

    def box(self, m, color=YELLOW):
        b = SurroundingRectangle(m, color=color, buff=0.12)
        self.s.play(Create(b))
        self.items.add(b)
        return b

    def clear(self, rt=0.6):
        if len(self.items):
            members = list(self.items.submobjects)
            self.s.play(FadeOut(self.items), run_time=rt)
            self.s.remove(self.items, *members)
        self.items = VGroup()
        self.lines = []


def title_card(scene, number, title, sub):
    n = Tx(f"Lesson {number}", color=B_COL).scale(0.8)
    t = Tx(title).scale(1.35)
    st = Tx(sub, color=DIM).scale(0.7)
    g = VGroup(n, t, st).arrange(DOWN, buff=0.35)
    line = Line(LEFT * 3.5, RIGHT * 3.5, color=B_COL, stroke_width=2).next_to(t, DOWN, buff=0.18)
    st.next_to(line, DOWN, buff=0.3)
    grp = VGroup(n, t, line, st)
    scene.play(FadeIn(n, shift=DOWN * 0.2), Write(t), run_time=1.5)
    scene.play(Create(line), FadeIn(st), run_time=1.0)
    return grp


def header(text, color=B_COL):
    return Tx(text, color=color).scale(0.75).to_corner(UL, buff=0.35)


def recap(scene, items, title="Recap"):
    h = Tx(title, color=YELLOW).scale(1.0).to_edge(UP, buff=0.6)
    rows = VGroup(*[Tx(r"$\bullet$\ " + it).scale(0.72) for it in items])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(h, DOWN, buff=0.6)
    if rows.width > 12.5:
        rows.scale_to_fit_width(12.5)
    scene.play(Write(h))
    return h, rows


def rows_hl(matrix, i, color=B_COL):
    return SurroundingRectangle(matrix.get_rows()[i], color=color, buff=0.08)


def col_hl(matrix, j, color=Q_COL):
    return SurroundingRectangle(matrix.get_columns()[j], color=color, buff=0.08)
