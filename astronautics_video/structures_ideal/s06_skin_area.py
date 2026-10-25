"""S06: when the skin carries direct stress too (BRIEF.md S06). Rework of old/s03_skin_area.py."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

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

# picture geometry (scene units): the panel on the left, filling the height; algebra on the right
XL, XR = -5.9, -2.3            # boom 1, boom 2
BW = XR - XL                   # panel width b
Y0 = 0.55                      # panel centre line
TH = 0.26                      # drawn panel thickness
YB = Y0 + TH / 2               # base of the stress block
H1, H2 = 2.0, 0.8              # stress heights at boom 1 and boom 2 (sigma_1 > sigma_2)
YI = -3.05                     # idealized booms
XC = -1.25                     # left edge of the algebra column

# idealized booms drawn to scale: B_1, B_2 from the rule with sigma_2/sigma_1 = H2/H1
RAT = H2 / H1
B1s, B2s = (2 + RAT) / 6, (2 + 1 / RAT) / 6            # in units of t_D b
assert np.isclose(H1 * B1s + H2 * B2s, (H1 + H2) / 2)    # same total force as the panel (per unit t_D b)
F1, F2 = H1 * B1s, H2 * B2s                              # boom forces, drawn as arrow lengths
assert F1 > F2 > 0


def hgt(x):
    return H1 + (H2 - H1) * (x - XL) / BW


def note(s):
    return TX(s, size=32, color=MUTED)


def row(eq, s, buff=.16):
    return VGroup(eq, note(s)).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def column(*rows, buff=.42):
    g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    g.align_to(np.array([XC, 0, 0]), LEFT)
    g.align_to(np.array([0, 2.95, 0]), UP)
    return g


class S06_Skin_Area(VScene):
    budget = 179

    def construct(self):
        self.section("When the skin carries direct stress too")

        # ---- beat 1: the real panel ------------------------------------------------------
        plate = Rectangle(width=BW, height=TH, stroke_color=INK2, stroke_width=2,
                          fill_color=INK2, fill_opacity=.55).move_to(np.array([(XL + XR) / 2, Y0, 0]))
        bm1 = Dot(np.array([XL, Y0, 0]), radius=.2, color=EMBER).set_z_index(3)
        bm2 = Dot(np.array([XR, Y0, 0]), radius=.2, color=EMBER).set_z_index(3)
        n1 = T("1", size=36, color=INK2).next_to(bm1, DOWN, buff=.2)
        n2 = T("2", size=36, color=INK2).next_to(bm2, DOWN, buff=.2)
        tlab = M(r"t_D", size=44).next_to(plate, DOWN, buff=.22)
        bspan = span(np.array([XL, Y0 - 1.0, 0]), np.array([XR, Y0 - 1.0, 0]), r"b", off=0.0, size=44)

        self.beat("Sometimes the skin does carry real direct stress. Then we give its share to the booms at its two edges.",
                  [FadeIn(plate), FadeIn(tlab), FadeIn(bspan)], .12,
                  [GrowFromCenter(bm1), GrowFromCenter(bm2), FadeIn(n1), FadeIn(n2)],
                  [Indicate(bm1, color=EMBER, scale_factor=1.6), Indicate(bm2, color=EMBER, scale_factor=1.6)], .15,
                  w=(.3, .25, .3))

        # ---- beat 2: the linear stress ---------------------------------------------------
        block = Polygon(np.array([XL, YB, 0]), np.array([XL, YB + H1, 0]),
                        np.array([XR, YB + H2, 0]), np.array([XR, YB, 0]),
                        stroke_width=0, fill_color=GOLD, fill_opacity=.12)
        arrows = VGroup(*[Arrow(np.array([x, YB, 0]), np.array([x, YB + hgt(x), 0]), buff=0, color=GOLD,
                                stroke_width=5, max_tip_length_to_length_ratio=.14)
                          for x in np.linspace(XL, XR, 9)])
        top = Line(np.array([XL, YB + H1, 0]), np.array([XR, YB + H2, 0]), color=GOLD, stroke_width=3)
        s1lab = M(r"\sigma_1", size=46, color=GOLD).next_to(np.array([XL, YB + H1, 0]), LEFT, buff=.15)
        s2lab = M(r"\sigma_2", size=46, color=GOLD).next_to(np.array([XR, YB + H2, 0]), UP, buff=.18)

        self.beat("Say the stress is sigma one at boom one and sigma two at boom two, changing in a straight line between them.",
                  [Indicate(bm1, color=EMBER, scale_factor=1.4), FadeIn(s1lab)],
                  [Indicate(bm2, color=EMBER, scale_factor=1.4), FadeIn(s2lab)],
                  [FadeIn(block), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.12), Create(top)], .18,
                  w=(.2, .2, .4))

        # ---- beat 3: the idealized version -----------------------------------------------
        ib1 = Dot(np.array([XL, YI, 0]), radius=.4 * np.sqrt(B1s), color=EMBER).set_z_index(3)
        ib2 = Dot(np.array([XR, YI, 0]), radius=.4 * np.sqrt(B2s), color=EMBER).set_z_index(3)
        skin = DashedLine(np.array([XL, YI, 0]), np.array([XR, YI, 0]), color=INK2, stroke_width=3)
        fa1 = Arrow(np.array([XL, YI, 0]), np.array([XL, YI + 1.2, 0]), buff=0, color=GOLD,
                    stroke_width=7, max_tip_length_to_length_ratio=.3)
        fa2 = Arrow(np.array([XR, YI, 0]), np.array([XR, YI + 1.2 * F2 / F1, 0]), buff=0, color=GOLD,
                    stroke_width=7, max_tip_length_to_length_ratio=.3)
        f1lab = E(r"\sigma_1|B_1", size=44).next_to(fa1, RIGHT, buff=.18)
        f2lab = E(r"\sigma_2|B_2", size=44).next_to(fa2, LEFT, buff=.18)
        shear = note("skin: shear only").next_to(skin, DOWN, buff=.3)
        card = panel(VGroup(T("same total force", size=36), T("same moment", size=36)).arrange(DOWN, buff=.3))
        card.move_to(np.array([(XC + 6.8) / 2, -.6, 0]))
        ideal = VGroup(skin, ib1, ib2, fa1, fa2, f1lab, f2lab, shear)

        self.beat("The two booms must do exactly what the panel did: give the same total force, and the same moment.",
                  [Create(skin), GrowFromCenter(ib1), GrowFromCenter(ib2), FadeIn(shear)],
                  [GrowArrow(fa1), GrowArrow(fa2), FadeIn(f1lab), FadeIn(f2lab)], .1,
                  [FadeIn(card, shift=UP * .2)], .18, w=(.3, .3, .4))

        # ---- beat 4: split the stress block about boom 2 ---------------------------------
        rect = Polygon(np.array([XL, YB, 0]), np.array([XL, YB + H2, 0]), np.array([XR, YB + H2, 0]),
                       np.array([XR, YB, 0]), stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=.3)
        tri = Polygon(np.array([XL, YB + H2, 0]), np.array([XL, YB + H1, 0]), np.array([XR, YB + H2, 0]),
                      stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=.6)
        trilab = backed(E(r"\sigma_1|-|\sigma_2", size=36)).move_to(np.array([XL + .95, YB + H2 + .4, 0]))
        pivot = Circle(radius=.36, color=EMBER, stroke_width=4).move_to(bm2)
        pivlab = T("pivot", size=34, color=EMBER).next_to(pivot, RIGHT, buff=.12)

        self.beat("To find B one, take moments about boom two. Split the stress into a rectangle and a triangle.",
                  [FadeOut(card), Create(pivot), FadeIn(pivlab)], .12,
                  [FadeOut(block), arrows.animate.set_opacity(.2), FadeIn(rect)],
                  [FadeIn(tri), FadeIn(trilab)], .18, w=(.35, .3, .35))

        # ---- beat 5: the rectangle ------------------------------------------------------
        xr_ = XR - BW / 2              # rectangle resultant: b/2 from boom 2
        xt_ = XR - 2 * BW / 3          # triangle resultant: 2b/3 from boom 2
        assert np.isclose(xt_, XL + BW / 3)          # a triangle's centroid sits a third from its tall side
        mr = Dot(np.array([xr_, Y0, 0]), radius=.1, color=INK).set_z_index(4)
        mt = Dot(np.array([xt_, Y0, 0]), radius=.1, color=INK).set_z_index(4)
        lr = DashedLine(np.array([xr_, YB + H2 / 2, 0]), np.array([xr_, Y0, 0]), color=INK, stroke_width=3)
        lt = DashedLine(np.array([xt_, YB + H2 + (H1 - H2) / 3, 0]), np.array([xt_, Y0, 0]), color=INK, stroke_width=3)
        sr = span(np.array([xr_, Y0 - 1.6, 0]), np.array([XR, Y0 - 1.6, 0]), r"b/2", off=0.0, size=40)
        st = span(np.array([xt_, Y0 - 2.25, 0]), np.array([XR, Y0 - 2.25, 0]), r"2b/3", off=0.0, size=40)

        r1 = row(E(r"\sigma_2|\,t_D b|\cdot|\frac{b}{2}", size=48), "rectangle: force times arm")
        r2 = row(E(r"+|\frac{1}{2}(|\sigma_1|-|\sigma_2|)\,t_D b|\cdot|\frac{2}{3}b", size=48),
                 "triangle: force times arm")
        r3 = row(E(r"=|\sigma_1|B_1|\cdot|b", size=48), r"boom 1: force $\sigma_1 B_1$, arm $b$")
        column(r1, r2, r3)
        e1, e2, e3 = r1[0], r2[0], r3[0]

        with self.say("The rectangle's force is sigma two times t D times b. It acts at the middle, b over two from boom two.") as d:
            self.play(tri.animate.set_fill(opacity=.15).set_stroke(opacity=.3), trilab.animate.set_opacity(.3),
                      Indicate(rect, color=GOLD, scale_factor=1.04), run_time=.12 * d)
            self.play(Write(VGroup(*e1[0:2])), run_time=.2 * d)
            self.wait(.08 * d)
            self.play(Create(lr), GrowFromCenter(mr), run_time=.12 * d)
            self.play(FadeIn(sr), Write(VGroup(*e1[2:4])), FadeIn(r1[1]), run_time=.25 * d)
            self.wait(.15 * d)

        # ---- beat 6: the triangle -------------------------------------------------------
        with self.say("The triangle's force is one half times sigma one minus sigma two, times t D times b. "
                      "It acts two thirds of the way across, two b over three from boom two.") as d:
            self.play(tri.animate.set_fill(opacity=.6).set_stroke(opacity=1), trilab.animate.set_opacity(1),
                      rect.animate.set_fill(opacity=.12).set_stroke(opacity=.3), run_time=.1 * d)
            self.play(Write(VGroup(*e2[0:6])), run_time=.3 * d)
            self.wait(.06 * d)
            self.play(Create(lt), GrowFromCenter(mt), run_time=.12 * d)
            self.play(FadeIn(st), Write(VGroup(*e2[6:8])), FadeIn(r2[1]), run_time=.25 * d)
            self.wait(.12 * d)

        # ---- beat 7: equal to the boom's moment -----------------------------------------
        self.beat("Their moments add up to the moment of the boom force, sigma one B one, times b.",
                  [rect.animate.set_fill(opacity=.3).set_stroke(opacity=1)],
                  [Write(e3), Indicate(f1lab, color=EMBER, scale_factor=1.25),
                   Indicate(ib1, color=EMBER, scale_factor=1.5)],
                  [FadeIn(r3[1]), Indicate(bspan, color=INK)], .2, w=(.15, .5, .35))

        # ---- beat 8: solve for B_1 ------------------------------------------------------
        rA = row(E(r"B_1|=|\frac{t_D b}{2}\,|\frac{\sigma_2}{\sigma_1}|+|\frac{t_D b}{3}|\Big(1-|\frac{\sigma_2}{\sigma_1}|\Big)",
                   size=46), r"divide both sides by $\sigma_1 b$")
        rB = row(E(r"=|\frac{t_D b}{6}|\Big(|3|\frac{\sigma_2}{\sigma_1}|+2-2|\frac{\sigma_2}{\sigma_1}|\Big)", size=46),
                 "common denominator 6")
        rC = row(E(r"B_1|=|\frac{t_D b}{6}|\Big(2+|\frac{\sigma_2}{\sigma_1}|\Big)", size=52), "collect terms")
        for e, ks in [(rA[0], (3, 7)), (rB[0], (4, 6)), (rC[0], (4,))]:
            paint(e, {k: GOLD for k in ks})
        column(rA, rB, rC)
        boxC = SurroundingRectangle(rC[0], color=EMBER, buff=.2, stroke_width=4)
        old = VGroup(r1, r2, r3)

        with self.say("Divide both sides by sigma one times b, and collect terms. "
                      "You get B one equals t D b over six, times two plus sigma two over sigma one.") as d:
            self.play(Circumscribe(VGroup(*e3[1:4]), color=GOLD), run_time=.1 * d)
            self.play(FadeOut(old, shift=UP * .3), run_time=.06 * d)
            self.play(Write(rA), run_time=.2 * d)
            self.wait(.06 * d)
            self.play(Write(rB), run_time=.17 * d)
            self.wait(.05 * d)
            self.play(Write(rC), run_time=.22 * d)
            self.play(Create(boxC), FadeIn(glow(rC[0], EMBER)), Indicate(ib1, color=EMBER, scale_factor=1.5),
                      run_time=.1 * d)
        self.snap("boxed B_1")
        self.wait(2.0)

        # ---- B_2 by swapping 1 and 2 ----------------------------------------------------
        r6 = row(E(r"B_2|=|\frac{t_D b}{6}|\Big(2+|\frac{\sigma_1}{\sigma_2}|\Big)", size=52), "swap 1 and 2")
        paint(r6[0], {4: GOLD})
        keepC = VGroup(rC, boxC)
        stage = column(rC.copy(), r6, buff=.7)
        self.play(FadeOut(rA), FadeOut(rB), keepC.animate.shift(stage[0].get_center() - rC.get_center()),
                  *[m.animate.set_opacity(.25) for m in (sr, st, lr, lt, mr, mt, pivot, pivlab)], run_time=1.2)
        box6 = SurroundingRectangle(r6[0], color=EMBER, buff=.2, stroke_width=4)
        self.play(Write(r6), run_time=2.0)
        self.play(Create(box6), Indicate(ib2, color=EMBER, scale_factor=1.5), Indicate(f2lab, color=EMBER),
                  run_time=1.2)
        self.wait(3.0)
        self.wipe()
