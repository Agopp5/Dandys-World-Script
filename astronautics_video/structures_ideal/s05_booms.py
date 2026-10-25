"""S05: booms carry the direct stress (BRIEF.md S05). Rework of old/s02_booms.py."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# facts: an illustrative L stringer, legs 30 mm and 20 mm, 3 mm thick
LEG_A, LEG_B, TH = 30, 20, 3
AREA = (LEG_A + LEG_B - TH) * TH
assert AREA == 141
# centroid of the L (30 x 3 leg plus the 17 x 3 rest of the other leg), mm from the outer corner
CX = (LEG_A * TH * TH / 2 + (LEG_B - TH) * TH * (TH + (LEG_B - TH) / 2)) / AREA
CY = (LEG_A * TH * LEG_A / 2 + (LEG_B - TH) * TH * TH / 2) / AREA
assert np.isclose(CX, 721.5 / 141) and np.isclose(CY, 1426.5 / 141)
# bending stress sigma = (M_x / I_xx) y is linear in y. The stringer sits at the top of a wing box
# 600 mm deep (y from 270 to 300 mm), so across it sigma changes by only 10%: "nearly constant"
Y_TOP, Y_BOT = 300.0, 300.0 - LEG_A
assert np.isclose(Y_BOT / Y_TOP, 0.9)


class S05_Booms(VScene):
    budget = 108

    def construct(self):
        # ---- the big L stringer (built first so the zoom can grow into it)
        s = 0.2                                    # scene units per mm
        org = np.array([-4.6, -3.1, 0])            # outer corner of the L (bottom-left)
        vert = Rectangle(width=TH * s, height=LEG_A * s).move_to(org + np.array([TH * s / 2, LEG_A * s / 2, 0]))
        horz = Rectangle(width=LEG_B * s, height=TH * s).move_to(org + np.array([LEG_B * s / 2, TH * s / 2, 0]))
        for r in (vert, horz):
            r.set_stroke(INK2, 2).set_fill(INK2, 0.55)
        ell = VGroup(vert, horz)
        dimA = T("30 mm", size=34, color=MUTED).next_to(vert, LEFT, buff=0.25)
        dimB = T("20 mm", size=34, color=MUTED).next_to(horz, DOWN, buff=0.2)
        tag = T("one L stringer", size=34, color=INK2).next_to(ell, UP, buff=0.3).align_to(ell, LEFT)

        # ---- beat 1: the wing with its stringers, then zoom on one of them
        wing, spts, fs, rs = wing_outline(14, width=12.8, center=(0, 0.6))
        for m in (wing, fs, rs):
            m.set_stroke(INK2, 3)
        small = VGroup(*[ell.copy().scale_to_fit_height(0.26).move_to(p) for p in spts])
        k = int(np.argmax([p[1] for p in spts]))   # the top-most stringer
        box = Square(0.6, color=ACCENT, stroke_width=4).move_to(spts[k])
        wtag = T("a wing: skin, spars and stringers", size=34, color=INK2).to_edge(DOWN, buff=0.6)
        zoomed = small[k]
        rest = VGroup(*[m for i, m in enumerate(small) if i != k])
        self.beat("Now the main idea. Each stringer is small compared with the whole section.",
                  [Create(wing), Create(fs), Create(rs), FadeIn(small), FadeIn(wtag)], .1,
                  [Create(box), Indicate(zoomed, color=ACCENT, scale_factor=1.6)], .05,
                  [FadeOut(VGroup(wing, fs, rs, rest, wtag)), box.animate.set_opacity(0),
                   ReplacementTransform(zoomed, ell)],
                  [FadeIn(tag), FadeIn(dimA), FadeIn(dimB)], .15,
                  w=(.3, .1, .27, .08))
        self.remove(box)

        # ---- beat 2: GOLD direct-stress arrows, length proportional to y (nearly equal)
        y0 = org[1]

        def ylen(p):
            y_mm = Y_BOT + (p[1] - y0) / s
            return 1.9 * y_mm / Y_TOP              # 1.9 units at the top fibre
        pts = [org + np.array([TH * s / 2, (4.5 + 6 * j) * s, 0]) for j in range(5)]
        pts += [org + np.array([(9 + 6 * j) * s, TH * s / 2, 0]) for j in range(2)]
        dvec = np.array([1.0, 0.33, 0]) / np.linalg.norm([1.0, 0.33])
        arrows = VGroup(*[Arrow(p, p + ylen(p) * dvec, buff=0, color=GOLD, stroke_width=6,
                                max_tip_length_to_length_ratio=0.16) for p in pts])
        arrows.set_z_index(2)
        sig = E(r"\sigma_z|\approx|\text{const}", size=60).move_to(np.array([3.6, 1.6, 0]))
        sig_glow = glow(sig, GOLD)
        notes = VGroup(T("stress grows with height y,", size=30, color=MUTED),
                       T("and y only runs from 270 to 300 mm", size=30, color=MUTED),
                       T("across this one stringer", size=30, color=MUTED)).arrange(DOWN, buff=0.15)
        notes.next_to(sig, DOWN, buff=0.45)
        self.beat("So the bending stress across one stringer hardly changes. We can treat it as constant.",
                  LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), .1,
                  FadeIn(notes), .05, Write(sig), FadeIn(sig_glow), .15,
                  w=(.35, .2, .15, .06))

        # ---- beat 3: the L shrinks into a boom with the same area, at the same place
        areaL = E(r"A|=|(30+20-3)\times 3|=|141\ \text{mm}^2", size=48).move_to(np.array([3.6, 1.2, 0]))
        fit(areaL, 7.0, 2)
        ghost = ell.copy().set_fill(opacity=0).set_stroke(MUTED, 2, opacity=0.8)
        boom = Dot(org + np.array([CX * s, CY * s, 0]), radius=0.4, color=EMBER)
        blab = E(r"B", size=60).next_to(boom, RIGHT, buff=0.35)
        areaB = E(r"B|=|141\ \text{mm}^2", size=60).move_to(areaL).align_to(areaL, LEFT)
        halo = glow(boom, EMBER)
        bnote = VGroup(T("same area, same place,", size=30, color=MUTED),
                       T("now a single point: a boom", size=30, color=MUTED)).arrange(DOWN, buff=0.15)
        bnote.next_to(areaB, DOWN, buff=0.5).align_to(areaB, LEFT)
        self.beat("That means we can replace the stringer by a single point, with the same area, at the same place. We call that point a boom.",
                  [FadeOut(sig), FadeOut(sig_glow), FadeOut(notes), FadeOut(arrows)],
                  Write(areaL), .12,
                  [FadeIn(ghost), FadeOut(dimA), FadeOut(dimB), FadeOut(tag), ReplacementTransform(ell, boom)], .08,
                  [*morph(areaL, areaB, [(1, 1), (4, 2)]), FadeIn(bnote)],
                  [FadeIn(blab), FadeIn(halo)], .15,
                  w=(.08, .2, .2, .14, .1))

        # ---- beat 4: the key assumption
        kb = key_box(E(r"\text{booms carry all the direct stress } |\sigma_z", size=52),
                     E(r"\text{skin carries only shear flow } |q", size=52),
                     E(r"t_D|=|0", size=52),
                     label="KEY ASSUMPTION")
        kb.scale_to_fit_width(12.6)
        fit(kb, 13.2, 5.6)
        kb.move_to(UP * 0.5)
        tnote = VGroup(M(r"t_D", size=48, color=MUTED),
                       T("is the skin thickness that carries direct stress", size=34, color=MUTED)).arrange(RIGHT, buff=0.25)
        tnote.next_to(kb, DOWN, buff=0.45)
        self.beat("Here's the key assumption of this whole topic: the booms carry all of the direct stress, and the skin between them carries only shear.",
                  FadeOut(VGroup(boom, blab, areaB, bnote, ghost, halo)), FadeIn(kb, shift=UP * 0.2), .1, FadeIn(tnote), .15,
                  w=(.15, .5, .15))

        # ---- beat 5: back to the idealized wing; I_xx needs only areas and positions
        wing2, spts2, fs2, rs2 = wing_outline(14, width=12.8, center=(0, 1.0))
        for m in (wing2, fs2, rs2):
            m.set_stroke(INK2, 3)
        booms = VGroup(*[Dot(p, radius=0.15, color=EMBER) for p in spts2])
        na = DashedLine(np.array([-6.7, 1.0, 0]), np.array([6.7, 1.0, 0]), color=MUTED, stroke_width=2)
        k2 = int(np.argmax([p[1] for p in spts2]))
        pk = spts2[k2]
        yarr = DoubleArrow(np.array([pk[0], 1.0, 0]), pk, buff=0, color=INK, stroke_width=4,
                           max_tip_length_to_length_ratio=0.3)
        ylab = E(r"y_r", size=44).next_to(yarr, RIGHT, buff=0.15)
        brl = E(r"B_r", size=44).next_to(booms[k2], UP, buff=0.18)
        ixx = E(r"I_{xx}|=|\sum_r|B_r|\,y_r^2", size=60).move_to(DOWN * 2.0)
        ixx_glow = glow(ixx, EMBER)
        inote = T("only the boom areas and where they are", size=30, color=MUTED).next_to(ixx, DOWN, buff=0.45)
        self.beat("With that, the bending part of the problem only needs the boom areas and where they are. I x x is just each boom area times its height squared, added up.",
                  FadeOut(VGroup(kb, tnote)),
                  [Create(wing2), Create(fs2), Create(rs2), FadeIn(na)],
                  LaggedStart(*[GrowFromCenter(b) for b in booms], lag_ratio=0.06),
                  FadeIn(inote), .06,
                  [Write(ixx[0]), Write(ixx[1])],
                  [Write(ixx[3]), FadeIn(brl), Indicate(booms[k2], color=EMBER, scale_factor=1.8)],
                  [Write(ixx[4]), GrowFromCenter(yarr), FadeIn(ylab)],
                  Write(ixx[2]), FadeIn(ixx_glow), .12,
                  w=(.04, .12, .12, .07, .08, .1, .1, .08, .05))
        self.wait(1.0)
        self.wipe()
