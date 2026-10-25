"""S02: booms carry the direct stress (BRIEF.md S02)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

# facts: an illustrative L stringer, 50 x 30 mm legs, 5 mm thick
LEG_A, LEG_B, TH = 50, 30, 5
AREA = (LEG_A + LEG_B - TH) * TH
assert AREA == 375
# bending stress sigma = M y / I is linear in y: across a stringer sitting 120..150 mm above the
# neutral axis (the HW box half-depth is 150 mm) it changes by only 20%, so it is "nearly constant"
Y_TOP, Y_BOT = 150.0, 150.0 - LEG_A
assert np.isclose(Y_BOT / Y_TOP, 2 / 3)


class S02_Booms(VScene):
    budget = 75

    def construct(self):
        # ---- beat 1: one L stringer, big, with a GOLD direct-stress field across it
        s = 0.105                                  # scene units per mm
        org = np.array([-5.3, -2.9, 0])            # outer corner of the L (bottom-left)
        vert = Rectangle(width=TH * s, height=LEG_A * s).move_to(org + np.array([TH * s / 2, LEG_A * s / 2, 0]))
        horz = Rectangle(width=LEG_B * s, height=TH * s).move_to(org + np.array([LEG_B * s / 2, TH * s / 2, 0]))
        for r in (vert, horz):
            r.set_stroke(INK2, 2).set_fill(INK2, 0.55)
        ell = VGroup(vert, horz)
        dimA = T("50 mm", size=28, color=MUTED).next_to(vert, LEFT, buff=0.25)
        dimB = T("30 mm", size=28, color=MUTED).next_to(horz, DOWN, buff=0.25)
        tag = T("one L stringer", size=30, color=INK2).next_to(ell, UP, buff=0.35).align_to(ell, LEFT)

        # stress arrows: sample points on the L, arrow length proportional to sigma = k y
        y0 = org[1]                                # bottom of the L sits at y = Y_BOT mm
        def ylen(p):
            y_mm = Y_BOT + (p[1] - y0) / s
            return 1.0 * y_mm / Y_TOP              # 1.0 unit at the top fibre
        pts = [org + np.array([TH * s / 2, (5 + 10 * k) * s, 0]) for k in range(5)]
        pts += [org + np.array([(15 + 10 * k) * s, TH * s / 2, 0]) for k in range(2)]
        arrows = VGroup()
        for p in pts:
            L = ylen(p)
            d = np.array([0.8, 0.45, 0]) / np.linalg.norm([0.8, 0.45])
            arrows.add(Arrow(p, p + L * d * 1.6, buff=0, color=GOLD, stroke_width=5,
                             max_tip_length_to_length_ratio=0.18))
        sig = E(r"\sigma_z|\approx|\text{const}", size=56).move_to(np.array([3.0, 1.3, 0]))
        note1 = T("stress is linear in y, and y barely", size=30, color=MUTED)
        note2 = T("changes across one small stringer", size=30, color=MUTED)
        notes = VGroup(note1, note2).arrange(DOWN, buff=0.15).next_to(sig, DOWN, buff=0.4)
        self.beat("Each stringer is small compared with the whole section, so the bending stress across it is nearly constant.",
                  [FadeIn(ell), FadeIn(tag), FadeIn(dimA), FadeIn(dimB)],
                  LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12),
                  [Write(sig), FadeIn(notes)], w=(.25, .4, .35))

        # ---- beat 2: the L becomes a boom with the same area
        areaL = E(r"A|=|(50+30-5)\times 5|=|375\ \text{mm}^2", size=44).move_to(np.array([3.0, 0.4, 0]))
        fit(areaL, 7.2, 2)
        # centroid of the L (50 x 5 leg plus the 25 x 5 remainder of the other leg), in mm from the outer corner
        cx = (250 * 2.5 + 125 * 17.5) / AREA
        cy = (250 * 25 + 125 * 2.5) / AREA
        assert np.isclose(cx, 7.5) and np.isclose(cy, 17.5)
        ghost = ell.copy().set_fill(opacity=0).set_stroke(MUTED, 2, opacity=0.7)
        boom = Dot(org + np.array([cx * s, cy * s, 0]), radius=0.34, color=EMBER)
        blab = E(r"B", size=56).next_to(boom, RIGHT, buff=0.3)
        areaB = E(r"B|=|375\ \text{mm}^2", size=56).move_to(areaL).align_to(areaL, LEFT)
        halo = glow(boom, EMBER)
        bnote = T("same area, now at a single point", size=30, color=MUTED).next_to(areaB, DOWN, buff=0.4)
        self.beat("So we can replace it by a single point with the same area. We call it a boom.",
                  [FadeOut(sig), FadeOut(notes), Write(areaL), FadeIn(ghost)], .1,
                  [FadeOut(arrows), FadeOut(dimA), FadeOut(dimB), ReplacementTransform(ell, boom),
                   FadeOut(tag)],
                  [FadeIn(blab), *morph(areaL, areaB, [(4, 2)]), FadeIn(bnote), FadeIn(halo)],
                  w=(.35, .35, .3))

        # ---- beat 3: the key assumption
        kb = key_box(E(r"\text{booms carry all direct stress } |\sigma_z", size=56),
                     E(r"\text{skin carries only shear flow } |q", size=56),
                     E(r"t_D = 0", size=56), label="KEY ASSUMPTION")
        kb.scale_to_fit_width(12.8)
        kb.move_to(DOWN * 0.3)
        self.beat("Here's the key assumption: the booms carry all of the direct stress, and the skin between them carries only shear.",
                  FadeOut(VGroup(halo, boom, blab, areaB, bnote, ghost)), FadeIn(kb, shift=UP * 0.2),
                  w=(.2, .8))

        # ---- beat 4: back to the idealized wing; I_xx needs only areas and positions
        wing, spts, fs, rs = wing_outline(14, width=12.6, center=(0, 0.9))
        wing.set_stroke(INK2, 3)
        fs.set_stroke(INK2, 3)
        rs.set_stroke(INK2, 3)
        booms = VGroup(*[Dot(p, radius=0.13, color=EMBER) for p in spts])
        na = DashedLine(np.array([-6.6, 0.9, 0]), np.array([6.6, 0.9, 0]), color=MUTED, stroke_width=2)
        k = int(np.argmax([p[1] for p in spts]))
        pk = spts[k]
        yarr = DoubleArrow(np.array([pk[0], 0.9, 0]), pk, buff=0, color=INK, stroke_width=3,
                           max_tip_length_to_length_ratio=0.25)
        ylab = E(r"y_r", size=40).next_to(yarr, RIGHT, buff=0.12)
        brl = E(r"B_r", size=40).next_to(booms[k], UP, buff=0.15)
        ixx = E(r"I_{xx}|=|\sum_r|B_r|y_r^2", size=56).move_to(DOWN * 2.3)
        inote = T("only boom areas and their positions", size=30, color=MUTED).next_to(ixx, DOWN, buff=0.35)
        self.beat("That's a big simplification. The bending part of the problem now only needs the boom areas and their positions.",
                  FadeOut(kb),
                  [Create(wing), Create(fs), Create(rs), FadeIn(na)],
                  LaggedStart(*[GrowFromCenter(b) for b in booms], lag_ratio=0.06),
                  [GrowFromCenter(yarr), FadeIn(ylab), FadeIn(brl)],
                  [Write(ixx), FadeIn(inote)], w=(.08, .2, .22, .15, .35))
        self.wipe()
