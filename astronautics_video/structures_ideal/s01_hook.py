"""S01: the problem, a real wing section is too many shapes (BRIEF.md S01)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# Geometry: the kit's two-spar wing, drawn wide and given a 1.5x vertical stretch so it fills the frame height
# (a schematic; the real section is thinner).
CEN = np.array([0.0, -0.3, 0.0])
STRETCH = 1.5
_outline, _pts, _front, _rear = wing_outline(width=12.6, center=(CEN[0], CEN[1]))
PTS = [CEN + (p - CEN) * np.array([1.0, STRETCH, 1.0]) for p in _pts]

# facts: the narration says "two spars" and "a row of stringers along the top and the bottom"
assert len(PTS) == 14
assert sum(p[1] > CEN[1] for p in PTS) == 7 and sum(p[1] < CEN[1] for p in PTS) == 7
assert _front.get_center()[0] < _rear.get_center()[0]


def stringer_L(p, top, w=0.34, h=0.38):
    """An L-section stringer: one flange along the skin, one leg pointing into the section."""
    inward = DOWN if top else UP
    L = VMobject(stroke_color=INK, stroke_width=6)
    L.set_points_as_corners([p + RIGHT * w, p, p + inward * h])
    return L


def airfoil(width, center, color=INK2, sw=4):
    """A copy of the (stretched) wing outline, `width` units wide, centred at `center`: for the sliced-wing inset."""
    a = _outline.copy().stretch(STRETCH, 1, about_point=CEN).set_stroke(color, width=sw)
    a.scale(width / 12.6).move_to(np.array([center[0], center[1], 0.0]))
    return a


def tip(m, side):
    """The leading (side=-1) or trailing (side=+1) edge point of an airfoil copy."""
    a = np.array(m.get_anchors())
    return a[np.argmax(side * a[:, 0])]


class S01_Hook(VScene):
    budget = 101

    def construct(self):
        # ---- beat 1: a wing, sliced like a loaf of bread; the cut face becomes the big section ----
        root = airfoil(5.6, (-3.2, -2.2), sw=5).set_fill(SURFACE, opacity=1)
        wtip = airfoil(3.2, (3.4, 2.0), sw=4)
        le = Line(tip(root, -1), tip(wtip, -1), color=INK2, stroke_width=4)
        te = Line(tip(root, 1), tip(wtip, 1), color=INK2, stroke_width=4)
        wing = VGroup(le, te, wtip, root)
        cut = airfoil(4.4, (0.1, -0.1), color=ACCENT, sw=6)
        span_lab = T("span", size=34, color=MUTED).next_to(te.point_from_proportion(0.75), RIGHT, buff=0.35)
        cut_lab = T("cut face", size=34, color=ACCENT).next_to(cut, LEFT, buff=0.5).shift(UP * 0.3)

        outline = _outline.copy().stretch(STRETCH, 1, about_point=CEN).set_stroke(INK2, width=6)
        front = _front.copy().stretch(STRETCH, 1, about_point=CEN).set_stroke(INK2, width=7)
        rear = _rear.copy().stretch(STRETCH, 1, about_point=CEN).set_stroke(INK2, width=7)

        with self.say("Here's a slice through a real wing. It's called a cross section: imagine cutting the wing like a loaf of bread, and looking at the cut face.") as d:
            self.play(Create(root), Create(wtip), Create(le), Create(te), FadeIn(span_lab), run_time=.16 * d)
            self.wait(.06 * d)
            self.play(Create(cut), run_time=.14 * d)
            self.play(cut.animate.set_fill(ACCENT, opacity=0.35), FadeIn(cut_lab), run_time=.1 * d)
            self.snap("the cut face")
            self.wait(.12 * d)
            face = cut.copy()
            self.play(FadeOut(wing), FadeOut(span_lab), FadeOut(cut_lab), FadeOut(cut),
                      ReplacementTransform(face, outline), run_time=.2 * d)
            self.wait(.16 * d)

        # ---- beat 2: name the parts, one at a time ----
        tops = [p for p in PTS if p[1] > CEN[1]]
        Ls = VGroup(*[stringer_L(p, p[1] > CEN[1]) for p in PTS])
        top_y = max(q[1] for q in outline.get_anchors())
        bot_y = min(q[1] for q in outline.get_anchors())
        skin_pt = min((q for q in outline.get_anchors() if q[1] > CEN[1]), key=lambda q: abs(q[0] + 5.3))
        lab_skin = T("thin skin", size=36, color=INK2).move_to([-5.4, top_y + 0.7, 0])
        arr_skin = Arrow(lab_skin.get_bottom(), skin_pt, buff=0.1, color=MUTED, stroke_width=4)
        lab_front = T("front spar", size=36, color=INK2).move_to([front.get_center()[0], bot_y - 0.5, 0])
        lab_rear = T("rear spar", size=36, color=INK2).move_to([rear.get_center()[0] + 0.4, bot_y - 0.5, 0])
        lab_str = T("stringers", size=36, color=INK).move_to([1.2, top_y + 0.7, 0])
        arr_str = VGroup(*[Arrow(lab_str.get_bottom(), tops[k] + UP * 0.08, buff=0.12, color=MUTED, stroke_width=4)
                           for k in (3, 4, 5)])
        labels = VGroup(lab_skin, arr_skin, lab_str, arr_str, lab_front, lab_rear)

        self.beat("It has a thin outer skin, two spars that run along the wing, and a row of small stiffeners called stringers along the top and the bottom.",
                  [FadeIn(lab_skin), GrowArrow(arr_skin), Indicate(outline, color=ACCENT, scale_factor=1.0)],
                  .05,
                  [Create(front), Create(rear), FadeIn(lab_front), FadeIn(lab_rear)],
                  .05,
                  LaggedStart(*[Create(L) for L in Ls], lag_ratio=0.12),
                  [FadeIn(lab_str), *[GrowArrow(a) for a in arr_str]],
                  .15,
                  w=(.2, .25, .35, .2))

        # ---- beat 3: every shape needs its own area and position ----
        picks = [2, 4, 9, 11]                               # two top stringers, two bottom ones
        qs = VGroup()
        for i in picks:
            p = PTS[i]
            top = p[1] > CEN[1]
            q = T("?", size=56, color=ACCENT, weight=BOLD)
            q.move_to(p + (UP if top else DOWN) * 0.6 + RIGHT * 0.15)
            qs.add(q)
        need = T("each shape: its own area and position", size=36, color=INK).move_to([0, -0.3, 0])
        need = backed(need)
        note = T("a lot of bookkeeping", size=34, color=MUTED).next_to(need, DOWN, buff=0.3)

        with self.say("To find the stresses in it, you'd need the area and position of every one of these little shapes. That's a lot of bookkeeping.") as d:
            self.play(FadeOut(labels), run_time=.08 * d)
            for k, i in enumerate(picks):
                self.play(Ls[i].animate.set_stroke(ACCENT, width=9), FadeIn(qs[k], scale=1.4), run_time=.09 * d)
            self.play(FadeIn(need, shift=UP * 0.2), run_time=.1 * d)
            self.play(*[L.animate.set_stroke(ACCENT, width=8) for j, L in enumerate(Ls) if j not in picks],
                      run_time=.14 * d)
            self.wait(.08 * d)
            self.play(FadeIn(note, shift=UP * 0.15), run_time=.08 * d)
            self.wait(.16 * d)

        # ---- beat 4: every stringer shrinks to a dot; the simplified section; two homework problems ----
        dots = VGroup(*[Dot(p, radius=0.14, color=EMBER) for p in PTS])
        cap = T("the simplified section", size=36, color=INK).move_to([0, top_y + 0.7, 0])
        hw1 = panel(T("homework problem 1", size=34, color=INK))
        hw2 = panel(T("homework problem 2", size=34, color=INK))
        hws = VGroup(hw1, hw2).arrange(RIGHT, buff=0.8).move_to([0, bot_y - 0.65, 0])

        self.beat("So in this lesson, we'll learn a way to simplify the section, and then use it to solve both of your homework problems.",
                  [FadeOut(qs), FadeOut(need), FadeOut(note)],
                  .05,
                  [*[Transform(Ls[i], dots[i]) for i in range(len(PTS))],
                   outline.animate.set_stroke(INK2, width=2.5),
                   front.animate.set_stroke(INK2, width=3), rear.animate.set_stroke(INK2, width=3)],
                  FadeIn(cap, shift=DOWN * 0.2),
                  .1,
                  LaggedStart(FadeIn(hw1, shift=UP * 0.2), FadeIn(hw2, shift=UP * 0.2), lag_ratio=0.5),
                  .2,
                  w=(.15, .4, .15, .3))
        self.wipe()
