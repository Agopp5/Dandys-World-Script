"""S14: walls made of different materials, modulus-weighted thickness (BRIEF.md S14)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

# facts
Q_I, Q_II, Q_III = 7.1, 8.9, 4.2          # slide 3-cell check, N/mm (from the notes)
T_SLIDE = 11.3                            # kNm
G_SKIN, G_REF = 24200.0, 27600.0          # N/mm^2, HW P2 materials used as the example
assert np.isclose(G_SKIN / G_REF, 0.8768, atol=1e-4)
assert Q_II > Q_I > Q_III > 0

# a schematic three-cell wing box (mm): skins one material, spars another
PTS = {"a": (0, 0), "b": (300, 15), "c": (600, 40), "d": (800, 70),
       "e": (0, 600), "f": (300, 585), "g": (600, 545), "h": (800, 500)}
SKINS = [("a", "b", 2.0), ("b", "c", 2.0), ("c", "d", 2.0), ("e", "f", 2.0), ("f", "g", 2.0), ("g", "h", 2.0)]
SPARS = [("a", "e", 3.0), ("b", "f", 3.0), ("c", "g", 3.0), ("d", "h", 3.0)]


class S14_Gstar(VScene):
    budget = 70

    def construct(self):
        sec = Section(PTS, SKINS + SPARS, width=5.6, center=(-3.4, -0.5))
        walls = sec.draw()
        skins = VGroup(*[sec.walls_m[(a, b)] for a, b, _ in SKINS])
        spars = VGroup(*[sec.walls_m[(a, b)] for a, b, _ in SPARS])
        skins.set_color(INK2)
        spars.set_color(MUTED)
        g_sk = VGroup(T("skin", size=28, color=INK2), M(r"G_{\text{skin}}", size=40, color=ACCENT)).arrange(RIGHT, buff=.2)
        g_sk.next_to(sec.mid("e", "f"), UP, buff=.3)
        g_sp = VGroup(T("spar", size=28, color=MUTED), M(r"G_{\text{spar}}", size=40, color=ACCENT)).arrange(RIGHT, buff=.2)
        g_sp.next_to(sec.mid("a", "b"), DOWN, buff=.35).align_to(sec.p("a"), LEFT)

        old = E(r"\frac{d\theta}{dz}|=|\frac{1}{2AG}|\oint|q|\,\frac{ds}{t}", size=48)
        new = E(r"\frac{d\theta}{dz}|=|\frac{1}{2A}|\oint|q|\,\frac{ds}{G\,t}", size=48)
        old.move_to([3.6, 2.2, 0])
        new.move_to(old)
        n1 = T("one G: it sat outside", size=26, color=MUTED).next_to(old, DOWN, buff=.3)
        n2 = T("G changes wall to wall: it goes inside", size=26, color=MUTED).next_to(new, DOWN, buff=.3)

        self.beat("Skins and spars are often different materials. Then G is different on each wall, and it moves inside the integral.",
                  [Create(walls), FadeIn(g_sk), FadeIn(g_sp)], [Write(old), FadeIn(n1)], .1,
                  morph(old, new, [(0, 0), (1, 1), (3, 3), (4, 4)]) + [FadeOut(n1)], [FadeIn(n2), Circumscribe(new[5], color=ACCENT)],
                  w=(.25, .2, .3, .2))

        # beat 2: modulus-weighted thickness
        tstar = E(r"t^*|=|\frac{G}{G_{\text{ref}}}|\,t", size=48).move_to([3.6, .3, 0])
        n3 = T("modulus-weighted thickness", size=26, color=MUTED).next_to(tstar, DOWN, buff=.25)
        delta = E(r"\delta|=|\int|\frac{ds}{t^*}", size=48).move_to([3.6, -1.6, 0])
        twist = E(r"G_{\text{ref}}\,\frac{d\theta}{dz}|=|\frac{1}{2A}|\oint|q|\,\frac{ds}{t^*}", size=48).move_to(new)
        paint(twist, {0: INK})
        n4 = T("same formulas, with t* in place of t", size=26, color=MUTED).next_to(delta, DOWN, buff=.3)
        thin = [sk.animate.set_stroke(width=sk.get_stroke_width() * G_SKIN / G_REF) for sk in skins]
        self.beat("The trick: pick a reference G, and scale each wall's thickness by its G over the reference. That's the modulus weighted thickness, t star.",
                  [Write(tstar)], thin + [Indicate(g_sk, color=ACCENT)], [FadeIn(n3), FadeIn(glow(tstar[0], ACCENT))],
                  [Write(delta), FadeIn(n4)], [FadeOut(n2)] + morph(new, twist, [(1, 1), (2, 2), (3, 3), (4, 4)]),
                  w=(.2, .2, .15, .2, .25))

        # beat 3: the notes' three-cell result
        self.drop(tstar, n3, delta, n4, g_sk, g_sp)
        cells = [("a", "b", "f", "e"), ("b", "c", "g", "f"), ("c", "d", "h", "g")]
        cols = [MINT, LIME, SKY]
        tex = [r"q_I", r"q_{II}", r"q_{III}"]
        vals = [Q_I, Q_II, Q_III]
        flows, labs = VGroup(), VGroup()
        for k, cell in enumerate(cells):
            cen = np.mean([sec.p(n) for n in cell], axis=0)
            flows.add(cell_flow(cen, radius=.5, color=cols[k], ccw=True))
            labs.add(M(tex[k], size=44, color=cols[k]).move_to(cen))
        rows = VGroup(*[M(tex[k] + r"\;=\;" + str(vals[k]) + r"\ \text{N/mm}", size=48)
                        for k in range(3)]).arrange(DOWN, buff=.5, aligned_edge=LEFT)
        for k, r in enumerate(rows):
            r[0][0:k + 2].set_color(cols[k])
        head = TX(r"your notes' three-cell box, $T = 11.3$ kNm", size=30, color=MUTED)
        card = panel(VGroup(head, rows).arrange(DOWN, buff=.45))
        card.move_to([3.6, -1.2, 0])
        self.beat("Everything else stays the same. Your notes' three cell example works out to seven point one, eight point nine and four point two newtons per millimeter.",
                  [Circumscribe(twist, color=ACCENT)], [Create(flows), FadeIn(labs)], [FadeIn(card[0]), FadeIn(head)],
                  FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[2]), .1, FadeIn(glow(rows[1], LIME)),
                  w=(.1, .25, .1, .13, .13, .14, .15))
        self.wipe()
