"""S07: two cases you will use (BRIEF.md S07). Rework of old/s04_ratio.py, slowed down and enlarged."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# facts: B_1 = (t_D b / 6)(2 + sigma_2/sigma_1)
def boom(tD_b, ratio):
    return tD_b / 6 * (2 + ratio)
assert np.isclose(boom(1.0, 1.0), 1 / 2)        # ratio 1  -> t_D b / 2   (2 + 1 = 3, 3/6 = 1/2)
assert np.isclose(boom(1.0, -1.0), 1 / 6)       # ratio -1 -> t_D b / 6   (2 - 1 = 1)
assert np.isclose(boom(10 * 300, -1.0), 500)    # checkpoint 2.1: 10 x 300 / 6 = 500 mm^2
assert np.isclose(10 * 300 / 6, 500)

RATIO = {r"\frac{\sigma_2}{\sigma_1}": GOLD, r"\frac{\sigma_2}{\sigma_1}=1": GOLD,
         r"\frac{\sigma_2}{\sigma_1}=-1": GOLD, r"\sigma_2=-\sigma_1": GOLD}


def skin_picture(cx, cy, L=4.6):
    """Horizontal top skin at constant y: uniform stress block, booms at both ends, neutral axis below."""
    plate = Rectangle(width=L, height=0.14, fill_color=INK2, fill_opacity=1, stroke_width=0).move_to([cx, cy, 0])
    b1 = Dot([cx - L / 2, cy, 0], radius=0.18, color=EMBER)
    b2 = Dot([cx + L / 2, cy, 0], radius=0.18, color=EMBER)
    lb1 = E(r"B_1", size=42).next_to(b1, DOWN, buff=0.18)
    lb2 = E(r"B_2", size=42).next_to(b2, DOWN, buff=0.18)
    block = Rectangle(width=L, height=0.75, fill_color=GOLD, fill_opacity=0.28, stroke_color=GOLD,
                      stroke_width=3).next_to(plate, UP, buff=0)
    arrows = VGroup(*[Arrow([x, cy + 0.07, 0], [x, cy + 0.82, 0], buff=0, color=GOLD, stroke_width=4,
                            max_tip_length_to_length_ratio=0.3) for x in np.linspace(cx - L / 2 + 0.25, cx + L / 2 - 0.25, 7)])
    s1 = E(r"\sigma_1", size=44).next_to(block, UP, buff=0.12).align_to(block, LEFT)
    s2 = E(r"\sigma_2", size=44).next_to(block, UP, buff=0.12).align_to(block, RIGHT)
    na = DashedLine([cx - L / 2 - 0.3, cy - 1.2, 0], [cx + L / 2 + 0.3, cy - 1.2, 0], color=MUTED, stroke_width=3)
    nal = T("neutral axis", size=30, color=MUTED).next_to(na, DOWN, buff=0.1)
    return VGroup(plate, b1, b2, lb1, lb2, block, arrows, s1, s2, na, nal)


def web_picture(cx, cy, h=2.8, w=1.0, size=44):
    """Vertical web symmetric about the neutral axis: linear stress, +sigma at top, -sigma at bottom."""
    top, bot = np.array([cx, cy + h / 2, 0]), np.array([cx, cy - h / 2, 0])
    web = Rectangle(width=0.14, height=h, fill_color=INK2, fill_opacity=1, stroke_width=0).move_to([cx, cy, 0])
    b1 = Dot(top, radius=0.18, color=EMBER)
    b2 = Dot(bot, radius=0.18, color=EMBER)
    lb1 = E(r"B_1", size=42).next_to(b1, RIGHT, buff=0.2)
    lb2 = E(r"B_2", size=42).next_to(b2, LEFT, buff=0.2)
    tri_t = Polygon(top, top + LEFT * w, np.array([cx, cy, 0]), fill_color=GOLD, fill_opacity=0.28,
                    stroke_color=GOLD, stroke_width=3)
    tri_b = Polygon(bot, bot + RIGHT * w, np.array([cx, cy, 0]), fill_color=GOLD, fill_opacity=0.28,
                    stroke_color=GOLD, stroke_width=3)
    s1 = E(r"+\sigma_1", size=size).next_to(tri_t, LEFT, buff=0.12).align_to(tri_t, UP)
    s2 = E(r"\sigma_2=-\sigma_1", size=size, cmap=RATIO).next_to(tri_b, RIGHT, buff=0.12).align_to(tri_b, DOWN)
    na = DashedLine([cx - 1.9, cy, 0], [cx + 1.9, cy, 0], color=MUTED, stroke_width=3)
    nal = T("neutral axis", size=30, color=MUTED).next_to(np.array([cx - 0.2, cy, 0]), DL, buff=0.1)
    return VGroup(web, b1, b2, lb1, lb2, tri_t, tri_b, s1, s2, na, nal)


class S07_Ratio(VScene):
    budget = 145

    def construct(self):
        # ---- beat 1: the general formula, boxed, stays on top
        f = E(r"B_1|=|\frac{t_D b}{6}|\Big(2+|\frac{\sigma_2}{\sigma_1}|\Big)", size=52, cmap=RATIO)
        f.move_to([0, 3.15, 0])
        fbox = SurroundingRectangle(f, color=HAIR, buff=0.18, corner_radius=0.1)
        self.beat("So the boom area depends on the ratio of the two stresses. Two cases come up again and again.",
                  [Write(f), Create(fbox)], .1, Circumscribe(f[4], color=GOLD), .25, w=(.4, .25))

        # ---- beat 2: top skin, ratio one
        LX, RX = -3.55, 3.6
        skin = skin_picture(LX, 0.75)
        cap_s = T("top skin: same height, same stress", size=30, color=INK2).move_to([LX, -1.35, 0])
        r1 = E(r"\frac{\sigma_2}{\sigma_1}=1", size=46, cmap=RATIO).move_to([LX, -2.25, 0])
        e1 = E(r"B|=|\frac{t_D b}{6}|(2+1)|=|\frac{t_D b}{2}", size=46).move_to([LX, -3.35, 0])
        self.beat("First case: a top skin, in bending. Both of its edges are at the same height, so they have "
                  "the same stress. The ratio is one.",
                  [FadeIn(skin[:5]), FadeIn(skin[9:])], .1,
                  [GrowFromEdge(skin[5], DOWN), FadeIn(skin[6]), FadeIn(skin[7:9]), FadeIn(cap_s)], .1,
                  Write(r1), .15, w=(.25, .3, .2))

        # ---- beat 3: two plus one over six
        self.beat("Two plus one is three, and three over six is one half. Each boom gets t D b over two.",
                  Write(e1[:4]), .15, [Write(e1[4:]), FadeIn(glow(e1[5], EMBER))], .25,
                  w=(.3, .3))

        # ---- beat 4: web across the neutral axis, ratio minus one
        web = web_picture(RX, 0.55)
        cap_w = T("web: symmetric about the axis", size=30, color=INK2).move_to([RX, -1.35, 0])
        r2 = E(r"\frac{\sigma_2}{\sigma_1}=-1", size=46, cmap=RATIO).move_to([RX, -2.25, 0])
        e2 = E(r"B|=|\frac{t_D b}{6}|(2-1)|=|\frac{t_D b}{6}", size=46).move_to([RX, -3.35, 0])
        self.beat("Second case: a web that crosses the neutral axis, with its ends equally far above and below. "
                  "The stresses are equal and opposite. The ratio is minus one.",
                  [FadeIn(web[:5]), FadeIn(web[9:]), FadeIn(cap_w)], .1,
                  [FadeIn(web[5:7]), FadeIn(web[7:9])], .1, Write(r2), .15,
                  w=(.25, .25, .2))

        # ---- beat 5: two minus one
        self.beat("Two minus one is one. Each boom gets only t D b over six.",
                  Write(e2[:4]), .15, [Write(e2[4:]), FadeIn(glow(e2[5], EMBER))], .25,
                  w=(.3, .3))

        # ---- beat 6: your turn (a 300 mm web, 10 mm thick)
        cy, h = -0.5, 4.6
        big = web_picture(-2.4, cy, h=h, w=1.1)
        dim = DoubleArrow([-5.0, cy + h / 2, 0], [-5.0, cy - h / 2, 0], buff=0, color=INK2, stroke_width=3,
                          tip_length=0.22)
        dl = VGroup(E(r"b=300", size=44), M(r"\text{mm}", size=44)).arrange(DOWN, buff=0.15).next_to(dim, LEFT, buff=0.2)
        tl = E(r"t_D=10\ \text{mm}", size=44).move_to([-0.3, 1.0, 0])
        tarrow = Arrow(tl.get_left() + LEFT * 0.05, [-2.33, 0.6, 0], buff=0.1, color=INK2, stroke_width=3)
        keep = {f, fbox}
        old = Group(*[m for m in self.mobjects if m not in keep])
        self.beat("Your turn. Pause here and do checkpoint two point one in your guide.",
                  FadeOut(old), [FadeIn(big), GrowFromCenter(dim), FadeIn(dl)], [FadeIn(tl), GrowArrow(tarrow)], .15,
                  w=(.25, .35, .25))
        self.checkpoint("2.1", "A 300 mm web, 10 mm thick, in bending: area added?")

        # ---- beat 7: the answer
        a1 = E(r"B|=|\frac{t_D b}{6}", size=48).move_to([0, 1.2, 0]).align_to([1.9, 0, 0], LEFT)
        n1 = T("web: the ratio is minus one", size=30, color=MUTED).next_to(a1, DOWN, buff=0.15).align_to(a1, LEFT)
        a2 = E(r"=|\frac{10\times 300}{6}", size=48).next_to(n1, DOWN, buff=0.35)
        a2.align_to(a1[1], LEFT)
        a3 = E(r"=|500\ \text{mm}^2", size=52).next_to(a2, DOWN, buff=0.45)
        a3.align_to(a1[1], LEFT)
        a3[1].shift(RIGHT * 0.15)
        box = SurroundingRectangle(a3[1], color=EMBER, buff=0.12, corner_radius=0.08)
        n3 = T("added to each boom", size=30, color=MUTED).next_to(box, DOWN, buff=0.18).align_to(a1, LEFT)
        self.beat("Ten times three hundred, over six, is five hundred. So five hundred square millimeters go to "
                  "each boom. We'll use exactly this in the homework.",
                  [Write(a1), FadeIn(n1)], .08, Write(a2), .08, [Write(a3), Create(box)], .12,
                  [FadeIn(n3), Indicate(VGroup(big[1], big[2]), color=EMBER)], .15,
                  w=(.17, .17, .17, .14))
        self.wait(1.0)
        self.wipe()
