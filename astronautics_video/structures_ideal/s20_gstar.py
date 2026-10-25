"""S20: walls made of different materials, modulus-weighted thickness (BRIEF.md S20). Rework of old/s14_gstar.py."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# facts
Q_I, Q_II, Q_III = 7.1, 8.9, 4.2          # slide 3-cell check, N/mm (brief facts)
G_SKIN, G_REF = 24200.0, 27600.0          # N/mm^2, HW P2 materials: skins t* = 0.8768 t
assert np.isclose(G_SKIN / G_REF, 0.8768, atol=1e-4)
assert Q_II > Q_I > Q_III > 0

# a schematic three-cell wing box (mm): skins one material, spars another
PTS = {"a": (0, 0), "b": (280, 20), "c": (560, 50), "d": (800, 90),
       "e": (0, 800), "f": (280, 780), "g": (560, 740), "h": (800, 680)}
SKINS = [("a", "b", 2.0), ("b", "c", 2.0), ("c", "d", 2.0), ("e", "f", 2.0), ("f", "g", 2.0), ("g", "h", 2.0)]
SPARS = [("a", "e", 3.0), ("b", "f", 3.0), ("c", "g", 3.0), ("d", "h", 3.0)]
RX = 3.6                                   # centre of the algebra column


class S20_Gstar(VScene):
    budget = 99

    def construct(self):
        sec = Section(PTS, SKINS + SPARS, width=5.0, center=(-3.7, -0.5))
        walls = sec.draw(t_scale=1.4)
        skins = VGroup(*[sec.walls_m[(a, b)] for a, b, _ in SKINS])
        spars = VGroup(*[sec.walls_m[(a, b)] for a, b, _ in SPARS])
        skins.set_color(INK2)
        spars.set_color(MUTED)
        g_sk = VGroup(T("skin", size=34, color=INK2), M(r"G_{\text{skin}}", size=44, color=ACCENT)).arrange(RIGHT, buff=.25)
        g_sk.next_to(sec.mid("e", "f"), UP, buff=.45)
        sk_ln = Line(g_sk.get_bottom() + DOWN * .05, sec.mid("e", "f"), color=INK2, stroke_width=2)
        g_sp = VGroup(T("spar", size=34, color=MUTED), M(r"G_{\text{spar}}", size=44, color=ACCENT)).arrange(RIGHT, buff=.25)
        g_sp.next_to(sec.p("b"), DOWN, buff=.45)
        sp_ln = Line(g_sp.get_top() + UP * .05, sec.p("b") + UP * .9, color=MUTED, stroke_width=2)
        g_sk.add(sk_ln)
        g_sp.add(sp_ln)

        # beat 1: G moves inside the integral
        old = E(r"\frac{d\theta}{dz}|=|\frac{1}{2AG}|\oint|q|\,\frac{ds}{t}", size=50)
        new = E(r"\frac{d\theta}{dz}|=|\frac{1}{2A}|\oint|q|\,\frac{ds}{G\,t}", size=50)
        old.move_to([RX, 2.6, 0])
        new.move_to(old)
        n1 = T("one material: G sat outside", size=30, color=MUTED).next_to(old, DOWN, buff=.3)
        n2 = T("G changes wall to wall: it goes inside", size=30, color=MUTED).next_to(new, DOWN, buff=.3)
        self.beat("Sometimes the skins and the spars are made of different materials. Then G is different on each wall, and it has to move inside the integral.",
                  [Create(walls)], [FadeIn(g_sk), FadeIn(g_sp)], [Write(old), FadeIn(n1)], .12,
                  morph(old, new, [(0, 0), (1, 1), (3, 3), (4, 4)]) + [FadeOut(n1)],
                  [FadeIn(n2), Circumscribe(new[5], color=ACCENT)], .15,
                  w=(.18, .14, .2, .26, .22))

        # beat 2: modulus-weighted thickness
        tstar = E(r"t^*|=|\frac{G}{G_{\text{ref}}}|\,t", size=52).move_to([RX, .55, 0])
        n3 = T("modulus-weighted thickness", size=30, color=MUTED).next_to(tstar, DOWN, buff=.3)
        thin = [sk.animate.set_stroke(width=sk.get_stroke_width() * G_SKIN / G_REF) for sk in skins]
        self.beat("Here's the trick. Pick one reference G. Then scale each wall's thickness by its own G over the reference G. That's called the modulus weighted thickness, t star.",
                  .1, [Write(tstar[0:2])], [Write(tstar[2:])], thin + [Indicate(g_sk, color=ACCENT)],
                  [FadeIn(n3), FadeIn(glow(tstar[0], ACCENT))], .15,
                  w=(.2, .3, .25, .25))

        # beat 3: same formulas, t* in place of t
        delta = E(r"\delta|=|\int|\frac{ds}{t^*}", size=52).move_to([RX, -1.55, 0])
        twist = E(r"G_{\text{ref}}\,\frac{d\theta}{dz}|=|\frac{1}{2A}|\oint|q|\,\frac{ds}{t^*}", size=50).move_to(new)
        n4 = T("same formulas, with t* in place of t", size=30, color=MUTED).next_to(delta, DOWN, buff=.35)
        self.beat("Now use t star wherever you had t. Delta becomes the integral of d s over t star. Everything else stays the same.",
                  [Write(delta)], .12, [FadeOut(n2)] + morph(new, twist, [(1, 1), (2, 2), (3, 3), (4, 4)]),
                  [FadeIn(n4), Circumscribe(twist[5], color=ACCENT)], .15,
                  w=(.35, .4, .25))

        # beat 4: the slides' three-cell result
        self.drop(tstar, n3, delta, n4, g_sk, g_sp)
        cells = [("a", "b", "f", "e"), ("b", "c", "g", "f"), ("c", "d", "h", "g")]
        cols = [MINT, LIME, SKY]
        tex = [r"q_I", r"q_{II}", r"q_{III}"]
        vals = [Q_I, Q_II, Q_III]
        flows, labs = VGroup(), VGroup()
        for k, cell in enumerate(cells):
            cen = np.mean([sec.p(n) for n in cell], axis=0)
            flows.add(cell_flow(cen, radius=.62, color=cols[k], ccw=True))
            labs.add(M(tex[k], size=44, color=cols[k]).move_to(cen))
        rows = VGroup(*[M(tex[k] + r"\;=\;" + str(vals[k]) + r"\ \text{N/mm}", size=50)
                        for k in range(3)]).arrange(DOWN, buff=.5, aligned_edge=LEFT)
        for k, r in enumerate(rows):
            r[0][0:k + 2].set_color(cols[k])
        head = T("your slides' three-cell box", size=34, color=MUTED)
        card = panel(VGroup(head, rows).arrange(DOWN, buff=.45))
        card.move_to([RX, -1.0, 0])
        self.beat("Your slides' three cell example, worked this way, gives seven point one, eight point nine, and four point two newtons per millimeter.",
                  [Create(flows), FadeIn(labs)], [FadeIn(card[0]), FadeIn(head)],
                  FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[2]), .15,
                  w=(.3, .1, .2, .2, .2))
        self.wait(1.0)
        self.wipe()
