"""S01: the problem, a real wing section is too many shapes (BRIEF.md S01)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

# Geometry: the kit's two-spar wing, drawn wide and given a 1.5x vertical stretch so it fills the frame height
# (a schematic; the real section is thinner).
CEN = np.array([0.0, -0.3, 0.0])
STRETCH = 1.5
_outline, _pts, _front, _rear = wing_outline(width=12.6, center=(CEN[0], CEN[1]))
PTS = [CEN + (p - CEN) * np.array([1.0, STRETCH, 1.0]) for p in _pts]

# facts: the narration says "two spars" and "a row of stringers along the top and bottom"
assert len(PTS) == 14
assert sum(p[1] > CEN[1] for p in PTS) == 7 and sum(p[1] < CEN[1] for p in PTS) == 7
assert _front.get_center()[0] < _rear.get_center()[0]


def stringer_L(p, top, w=0.30, h=0.34):
    """An L-section stringer: one flange along the skin, one leg pointing into the section."""
    inward = DOWN if top else UP
    L = VMobject(stroke_color=INK, stroke_width=6)
    L.set_points_as_corners([p + RIGHT * w, p, p + inward * h])
    return L


def skin_piece(outline, x0, x1, top=True):
    """The stretch of the (already stretched) outline between x0 and x1 on the top or bottom skin."""
    a = outline.get_anchors()
    sel = [q for q in a if x0 <= q[0] <= x1 and ((q[1] > CEN[1]) == top)]
    sel.sort(key=lambda q: q[0])
    m = VMobject(stroke_color=ACCENT, stroke_width=12)
    m.set_points_as_corners(sel)
    return m


class S01_Hook(VScene):
    budget = 62

    def construct(self):
        outline = _outline.copy().stretch(STRETCH, 1, about_point=CEN).set_stroke(INK2, width=6)
        front = _front.copy().stretch(STRETCH, 1, about_point=CEN).set_stroke(INK2, width=7)
        rear = _rear.copy().stretch(STRETCH, 1, about_point=CEN).set_stroke(INK2, width=7)
        tops = [p for p in PTS if p[1] > CEN[1]]
        Ls = VGroup(*[stringer_L(p, p[1] > CEN[1]) for p in PTS])
        top_y = max(q[1] for q in outline.get_anchors())
        bot_y = min(q[1] for q in outline.get_anchors())

        # labels for the parts
        skin_pt = min((q for q in outline.get_anchors() if q[1] > CEN[1]), key=lambda q: abs(q[0] + 5.3))
        lab_skin = T("thin skin", size=32, color=INK2).move_to([-5.6, top_y + 0.75, 0])
        arr_skin = Arrow(lab_skin.get_bottom(), skin_pt, buff=0.1, color=MUTED, stroke_width=4)
        lab_str = T("stringers", size=32, color=INK).move_to([1.2, top_y + 0.75, 0])
        arr_str = VGroup(*[Arrow(lab_str.get_bottom(), tops[k] + UP * 0.08, buff=0.12, color=MUTED, stroke_width=4)
                           for k in (3, 4, 5)])
        lab_front = T("front spar", size=32, color=INK2).move_to([front.get_center()[0], bot_y - 0.5, 0])
        lab_rear = T("rear spar", size=32, color=INK2).move_to([rear.get_center()[0] + 0.4, bot_y - 0.5, 0])
        labels = VGroup(lab_skin, arr_skin, lab_str, arr_str, lab_front, lab_rear)

        self.beat("Here's a real wing section: a thin skin, two spars, and a row of stringers along the top and bottom.",
                  Create(outline), [Create(front), Create(rear), FadeIn(lab_front), FadeIn(lab_rear)],
                  [FadeIn(lab_skin), GrowArrow(arr_skin)],
                  LaggedStart(*[Create(L) for L in Ls], lag_ratio=0.12),
                  [FadeIn(lab_str), *[GrowArrow(a) for a in arr_str]],
                  w=(.2, .18, .12, .35, .15))

        # beat 2: each shape needs its own area and position, and so does the skin between them
        picks = [2, 7, 9]                                   # a top stringer, a bottom one, another top one
        qs = VGroup()
        for i in picks:
            p = PTS[i]
            top = p[1] > CEN[1]
            q = T("?", size=48, color=ACCENT, weight=BOLD)
            q.move_to(p + (UP if top else DOWN) * 0.55 + RIGHT * 0.12)
            qs.add(q)
        x0, x1 = PTS[4][0] + 0.32, PTS[6][0] - 0.02         # top skin between two stringers
        skin = skin_piece(outline, x0, x1, top=True)
        q_skin = T("?", size=48, color=ACCENT, weight=BOLD).move_to(
            [(x0 + x1) / 2, max(q[1] for q in skin.get_anchors()) + 0.55, 0])
        need = T("each one needs its own area and position", size=34, color=INK)
        need.move_to([0, -3.45, 0])

        def flag(L):
            return [L.animate.set_stroke(ACCENT, width=9)]

        with self.say("To find its bending stresses and shear flow, you'd need the area and position of every one of these shapes, and the skin between them.") as d:
            self.play(FadeOut(labels), run_time=.08 * d)
            for k, i in enumerate(picks):
                self.play(*flag(Ls[i]), FadeIn(qs[k], scale=1.4), run_time=.14 * d)
                if k == 0:
                    self.play(FadeIn(need, shift=UP * 0.2), run_time=.1 * d)
            self.play(Create(skin), FadeIn(q_skin, scale=1.4), run_time=.16 * d)
            self.play(*[L.animate.set_stroke(ACCENT, width=7) for j, L in enumerate(Ls) if j not in picks],
                      run_time=.16 * d)
            self.wait(.08 * d)

        # beat 3: every stringer shrinks to a boom (a dot); the skin is drawn thin
        dots = VGroup(*[Dot(p, radius=0.13, color=EMBER) for p in PTS])
        cap = T("idealized: same outline, booms and thin skin", size=34, color=INK).move_to([0, -3.45, 0])
        b_lab = T("booms", size=32, color=EMBER).move_to([1.2, top_y + 0.75, 0])
        b_arr = VGroup(*[Arrow(b_lab.get_bottom(), tops[k] + UP * 0.12, buff=0.12, color=EMBER, stroke_width=4)
                         for k in (3, 4, 5)])
        self.beat("That's a lot of bookkeeping. So we simplify the section in a way that keeps what matters.",
                  [FadeOut(qs), FadeOut(q_skin), FadeOut(skin), FadeOut(need)],
                  .1,
                  [*[Transform(Ls[i], dots[i]) for i in range(len(PTS))],
                   outline.animate.set_stroke(INK2, width=2.5),
                   front.animate.set_stroke(INK2, width=3), rear.animate.set_stroke(INK2, width=3)],
                  [FadeIn(b_lab), *[GrowArrow(a) for a in b_arr], FadeIn(cap, shift=UP * 0.2)],
                  .25,
                  )
        self.wipe()
