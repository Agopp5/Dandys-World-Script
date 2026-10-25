"""S03: when the skin carries direct stress too (BRIEF.md S03)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

# facts: the panel-to-boom rule, checked on arbitrary numbers
for tD, bb, s1, s2 in [(2.0, 150.0, 80.0, 30.0), (1.2, 90.0, -40.0, 55.0), (3.0, 200.0, 10.0, 10.0)]:
    # moments about boom 2: rectangle (sigma_2 t_D b at b/2) + triangle (1/2 (s1 - s2) t_D b at 2b/3) = s1 B1 b
    M2 = s2 * tD * bb * bb / 2 + 0.5 * (s1 - s2) * tD * bb * (2 / 3) * bb
    B1 = M2 / (s1 * bb)
    assert np.isclose(B1, tD * bb / 2 * s2 / s1 + tD * bb / 3 * (1 - s2 / s1))           # divided line
    assert np.isclose(B1, tD * bb / 6 * (3 * s2 / s1 + 2 - 2 * s2 / s1))                 # common denominator
    assert np.isclose(B1, tD * bb / 6 * (2 + s2 / s1))                                   # boxed result
    B2 = tD * bb / 6 * (2 + s1 / s2)                                                     # swap 1 and 2
    assert np.isclose(s1 * B1 + s2 * B2, tD * bb * (s1 + s2) / 2)                        # same total force
    assert np.isclose(s2 * B2 * bb, s1 * tD * bb * bb / 2 + 0.5 * (s2 - s1) * tD * bb * (2 / 3) * bb)  # moment about 1

# picture geometry (scene units): a short, narrow panel on the left so the algebra gets the width
XL, XR = -6.3, -2.9            # boom 1, boom 2
BW = XR - XL                   # panel width b
Y0 = 1.45                      # panel centre line
TH = 0.2                       # drawn panel thickness
YB = Y0 + TH / 2               # base of the stress block
H1, H2 = 1.25, 0.6             # stress heights at boom 1 and boom 2 (sigma_1 > sigma_2)
YI = -2.95                     # idealized booms
XC = -1.55                     # left edge of the algebra column


def hgt(x):
    return H1 + (H2 - H1) * (x - XL) / BW


def note(s):
    return TX(s, size=30, color=MUTED)


def row(eq, s, buff=.14):
    return VGroup(eq, note(s)).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def column(*rows):
    g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=.4)
    g.align_to(np.array([XC, 0, 0]), LEFT)
    g.align_to(np.array([0, 2.95, 0]), UP)
    return g



class S03_Skin_Area(VScene):
    budget = 97

    def construct(self):
        self.section("When the skin carries direct stress too")

        # ---- the real panel ------------------------------------------------------------
        panel = Rectangle(width=BW, height=TH, stroke_color=INK2, stroke_width=2,
                          fill_color=INK2, fill_opacity=.55).move_to(np.array([(XL + XR) / 2, Y0, 0]))
        bm1 = Dot(np.array([XL, Y0, 0]), radius=.17, color=EMBER).set_z_index(3)
        bm2 = Dot(np.array([XR, Y0, 0]), radius=.17, color=EMBER).set_z_index(3)
        n1 = T("1", size=30, color=INK2).next_to(bm1, DOWN, buff=.18)
        n2 = T("2", size=30, color=INK2).next_to(bm2, DOWN, buff=.18)
        tlab = M(r"t_D", size=40).next_to(bm2, RIGHT, buff=.2)
        bspan = span(np.array([XL, Y0 - .7, 0]), np.array([XR, Y0 - .7, 0]), r"b", off=0.0, size=40)

        block = Polygon(np.array([XL, YB, 0]), np.array([XL, YB + H1, 0]),
                        np.array([XR, YB + H2, 0]), np.array([XR, YB, 0]),
                        stroke_width=0, fill_color=GOLD, fill_opacity=.12)
        arrows = VGroup(*[Arrow(np.array([x, YB, 0]), np.array([x, YB + hgt(x), 0]), buff=0, color=GOLD,
                                stroke_width=4, max_tip_length_to_length_ratio=.16)
                          for x in np.linspace(XL, XR, 9)])
        top = Line(np.array([XL, YB + H1, 0]), np.array([XR, YB + H2, 0]), color=GOLD, stroke_width=3)
        s1lab = M(r"\sigma_1", size=42, color=GOLD).next_to(np.array([XL, YB + H1, 0]), LEFT, buff=.15)
        s2lab = M(r"\sigma_2", size=42, color=GOLD).next_to(np.array([XR, YB + H2, 0]), RIGHT, buff=.15)
        real = VGroup(block, arrows, top, panel, bm1, bm2, n1, n2, tlab, bspan, s1lab, s2lab)

        self.beat("Sometimes the skin does carry real direct stress. Then we add its share to the booms at its two edges.",
                  [FadeIn(panel), GrowFromCenter(bm1), GrowFromCenter(bm2), FadeIn(n1), FadeIn(n2),
                   FadeIn(tlab), FadeIn(bspan)], .1,
                  [FadeIn(block), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.1), Create(top),
                   FadeIn(s1lab), FadeIn(s2lab)], .1,
                  [Indicate(bm1, color=EMBER, scale_factor=1.6), Indicate(bm2, color=EMBER, scale_factor=1.6)],
                  w=(.3, .4, .3))

        # ---- the idealized version -----------------------------------------------------
        ib1 = Dot(np.array([XL, YI, 0]), radius=.24, color=EMBER).set_z_index(3)
        ib2 = Dot(np.array([XR, YI, 0]), radius=.2, color=EMBER).set_z_index(3)
        skin = DashedLine(np.array([XL, YI, 0]), np.array([XR, YI, 0]), color=INK2, stroke_width=2)
        fa1 = Arrow(np.array([XL, YI, 0]), np.array([XL, YI + .85, 0]), buff=0, color=GOLD, stroke_width=6,
                    max_tip_length_to_length_ratio=.3)
        fa2 = Arrow(np.array([XR, YI, 0]), np.array([XR, YI + .55, 0]), buff=0, color=GOLD, stroke_width=6,
                    max_tip_length_to_length_ratio=.3)
        f1lab = E(r"\sigma_1|B_1", size=40).next_to(fa1, RIGHT, buff=.15)
        f2lab = E(r"\sigma_2|B_2", size=40).next_to(fa2, LEFT, buff=.15)
        shear = note("skin: shear only").next_to(skin, DOWN, buff=.22)
        same = note("same force, same moment").move_to(np.array([(XL + XR) / 2, -1.6, 0]))
        ideal = VGroup(skin, ib1, ib2, fa1, fa2, f1lab, f2lab, shear)

        self.beat("The rule: the two booms must give the same force and the same moment as the panel.",
                  [Create(skin), GrowFromCenter(ib1), GrowFromCenter(ib2), FadeIn(shear)],
                  [GrowArrow(fa1), GrowArrow(fa2), FadeIn(f1lab), FadeIn(f2lab)], .1,
                  [FadeIn(same)], w=(.3, .35, .35))

        # ---- split the stress block ----------------------------------------------------
        rect = Polygon(np.array([XL, YB, 0]), np.array([XL, YB + H2, 0]), np.array([XR, YB + H2, 0]),
                       np.array([XR, YB, 0]), stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=.3)
        tri = Polygon(np.array([XL, YB + H2, 0]), np.array([XL, YB + H1, 0]), np.array([XR, YB + H2, 0]),
                      stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=.65)
        xr_ = XR - BW / 2              # rectangle resultant: b/2 from boom 2
        xt_ = XR - 2 * BW / 3          # triangle resultant: 2b/3 from boom 2
        assert np.isclose(xt_, XL + BW / 3)
        mr = Dot(np.array([xr_, Y0, 0]), radius=.09, color=INK).set_z_index(4)
        mt = Dot(np.array([xt_, Y0, 0]), radius=.09, color=INK).set_z_index(4)
        lr = DashedLine(np.array([xr_, YB + H2 / 2, 0]), np.array([xr_, Y0, 0]), color=INK, stroke_width=2)
        lt = DashedLine(np.array([xt_, YB + H2 + (H1 - H2) / 3, 0]), np.array([xt_, Y0, 0]), color=INK, stroke_width=2)
        sr = span(np.array([xr_, Y0 - 1.35, 0]), np.array([XR, Y0 - 1.35, 0]), r"b/2", off=0.0, size=38)
        st = span(np.array([xt_, Y0 - 2.0, 0]), np.array([XR, Y0 - 2.0, 0]), r"2b/3", off=0.0, size=38)

        r1 = row(E(r"\sigma_2|\,t_D b|\cdot|\frac{b}{2}", size=44), "rectangle: force times arm")
        r2 = row(E(r"+|\frac{1}{2}(|\sigma_1|-|\sigma_2|)\,t_D b|\cdot|\frac{2}{3}b", size=44),
                 "triangle: force times arm")
        column(r1, r2)

        with self.say("Take moments about boom two. The uniform part of the stress, sigma two, acts at the middle. "
                      "The triangle on top acts two thirds of the way across.") as d:
            self.play(FadeOut(same), Indicate(bm2, color=EMBER, scale_factor=1.8), run_time=.18 * d)
            self.play(FadeOut(block), arrows.animate.set_opacity(.25), FadeIn(rect), run_time=.1 * d)
            self.play(Create(lr), GrowFromCenter(mr), FadeIn(sr), Write(r1), run_time=.25 * d)
            self.wait(.08 * d)
            self.play(FadeIn(tri), run_time=.1 * d)
            self.play(Create(lt), GrowFromCenter(mt), FadeIn(st), Write(r2), run_time=.25 * d)
            self.wait(.04 * d)

        # ---- solve for B_1 -------------------------------------------------------------
        bal = row(E(r"\sigma_2|\,t_D b|\cdot|\frac{b}{2}|+|\frac{1}{2}(|\sigma_1|-|\sigma_2|)\,t_D b|\cdot|\frac{2}{3}b"
                    r"|=|\sigma_1|B_1|\,b", size=44), "moment balance about boom 2")
        r4 = row(E(r"B_1|=|\frac{t_D b}{2}|\,\frac{\sigma_2}{\sigma_1}|+|\frac{t_D b}{3}\Big(1-\frac{\sigma_2}{\sigma_1}\Big)",
                   size=44), r"divide both sides by $\sigma_1 b$")
        r4b = row(E(r"=|\frac{t_D b}{6}|\Big(3\frac{\sigma_2}{\sigma_1}+2-2\frac{\sigma_2}{\sigma_1}\Big)", size=44),
                  "common denominator 6")
        column(bal, r4, r4b)
        r5 = row(E(r"B_1|=|\frac{t_D b}{6}|\Big(2+\frac{\sigma_2}{\sigma_1}\Big)", size=48), "collect terms", buff=.34)
        r6 = row(E(r"B_2|=|\frac{t_D b}{6}|\Big(2+\frac{\sigma_1}{\sigma_2}\Big)", size=48), "swap 1 and 2", buff=.34)
        stage_c = column(r4b.copy(), r5, r6)
        box1 = SurroundingRectangle(r5[0], color=EMBER, buff=.18, stroke_width=3)
        box2 = SurroundingRectangle(r6[0], color=EMBER, buff=.18, stroke_width=3)
        be = bal[0]

        with self.say("Setting their moment equal to sigma one times B one times b, and dividing through, "
                      "gives B one equals t D b over six, times two plus sigma two over sigma one.") as d:
            self.play(ReplacementTransform(r1[0], VGroup(*be[0:4])), ReplacementTransform(r2[0], VGroup(*be[4:12])),
                      FadeOut(r1[1]), FadeOut(r2[1]), run_time=.1 * d)
            self.play(Write(VGroup(*be[12:16])), FadeIn(bal[1]), Indicate(f1lab, color=EMBER), run_time=.12 * d)
            self.play(Write(r4), run_time=.2 * d)
            self.play(Write(r4b), run_time=.18 * d)
            self.play(FadeOut(bal), FadeOut(r4), r4b.animate.move_to(stage_c[0]), run_time=.08 * d)
            self.play(Write(r5), Create(box1), run_time=.2 * d)
            g5 = glow(r5[0], EMBER)
            self.play(FadeIn(g5), Indicate(ib1, color=EMBER, scale_factor=1.5), run_time=.1 * d)
        self.wait(1)

        # ---- B_2 by symmetry -----------------------------------------------------------
        self.play(Write(r6), Create(box2), Indicate(ib2, color=EMBER, scale_factor=1.5), run_time=2.0)
        self.wait(2.5)
        self.wipe()
