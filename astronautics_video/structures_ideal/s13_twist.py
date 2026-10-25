"""S13: every cell twists the same (BRIEF.md S13)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

# facts: the wall-by-wall sum equals q_I delta_I - q_II delta_12 (checked with the HW P2 numbers, per unit T)
dI, dII, d12 = 1969.0, 3527.8, 199.8
qI, qII = 1.261e-6, 0.804e-6
outer_I = dI - d12                                   # cell I's walls other than the shared one
assert np.isclose(qI * outer_I + (qI - qII) * d12, qI * dI - qII * d12)
# equal twist really holds for those flows (A_I = 232 000, A_II = 258 000 mm^2)
rI = (qI * dI - qII * d12) / (2 * 232000)
rII = (-qI * d12 + qII * dII) / (2 * 258000)
assert np.isclose(rI, rII, rtol=3e-3)
assert np.isclose(2 * 232000 * qI + 2 * 258000 * qII, 1.0, rtol=3e-3)

DCM = {r"\delta_I": ACCENT, r"\delta_{II}": ACCENT, r"\delta_{12}": ACCENT}
DTDZ = r"\frac{d\theta}{dz}"


def note(s):
    return T(s, size=26, color=MUTED)


class S13_Twist(VScene):
    budget = 118

    def construct(self):
        self.section("Every cell twists the same")

        # two-cell box: A bottom-left, B/E the shared spar, C/D the (shorter) right web, F top-left
        pts = {"A": (0, 0), "B": (240, 0), "C": (500, 50), "D": (500, 550), "E": (240, 600), "F": (0, 600)}
        walls = [("A", "B", 1.0), ("B", "C", 1.0), ("C", "D", 1.6), ("D", "E", 1.0),
                 ("E", "F", 1.0), ("F", "A", 1.6), ("B", "E", 2.0)]
        sec = Section(pts, walls, width=4.4, center=(-4.0, -0.4))
        box = sec.draw()
        shared = sec.walls_m[("B", "E")]
        shared.set_color(GOLD)
        cI = (sec.p("A") + sec.p("B") + sec.p("E") + sec.p("F")) / 4
        cII = (sec.p("B") + sec.p("C") + sec.p("D") + sec.p("E")) / 4
        labI = T("Cell I", size=30, color=MINT).move_to(cI + UP * 1.4)
        labII = T("Cell II", size=30, color=LIME).move_to(cII + UP * 1.4)
        pivot = (cI + cII) / 2
        RX = 2.6                                           # right column centre

        # ---- beat 1: the whole section rotates as one piece
        ghost = box.copy().set_stroke(color=MUTED, opacity=.45)
        fig = VGroup(box, labI, labII)
        twI = M(DTDZ, size=40, color=INK).move_to(cI + DOWN * .4)
        twII = M(DTDZ, size=40, color=INK).move_to(cII + DOWN * .4)
        same = M(r"\left.\frac{d\theta}{dz}\right|_{\mathrm{I}}", r"=",
                 r"\left.\frac{d\theta}{dz}\right|_{\mathrm{II}}", size=52)
        same.move_to([RX, .6, 0])
        same_n = note("one rigid rotation: the same rate of twist in every cell").next_to(same, DOWN, buff=.45)
        fit(same_n, 8.2, 1)
        with self.say("The extra equations come from compatibility. The whole section rotates as one piece, "
                      "so every cell has the same rate of twist.") as d:
            self.play(Create(box), FadeIn(labI), FadeIn(labII), run_time=.2 * d)
            self.add(ghost)
            self.play(Rotate(fig, angle=7 * DEGREES, about_point=pivot), run_time=.2 * d)
            self.play(FadeIn(twI), FadeIn(twII), run_time=.12 * d)
            self.play(Write(same), FadeIn(same_n), run_time=.2 * d)
            self.play(Rotate(fig, angle=-7 * DEGREES, about_point=pivot), FadeOut(ghost),
                      FadeOut(twI), FadeOut(twII), run_time=.15 * d)
            self.wait(.13 * d)

        # ---- beat 2: the twist rate of one cell
        rate = E(r"\frac{d\theta}{dz}|=|\frac{1}{2A_R\,G}|\oint|q|\frac{ds}{t}", size=52)
        rate.move_to([RX, .7, 0])
        rn1 = TX(r"$A_R$: the area enclosed by cell $R$", size=28).set_color(MUTED)
        rn2 = note("the integral runs once around that cell's walls")
        rnotes = VGroup(rn1, rn2).arrange(DOWN, buff=.3).next_to(rate, DOWN, buff=.55)
        self.beat("For one cell, the rate of twist is one over two A G, times the integral of q d s over t around that cell.",
                  [FadeOut(same), FadeOut(same_n)], Write(rate), FadeIn(rnotes), Circumscribe(rate[3:], color=SKY),
                  w=(.12, .38, .2, .3))

        # ---- beat 3: checkpoint
        with self.say("Your turn. Pause here and do checkpoint four point one in your guide.") as d:
            self.checkpoint("4.1", "Write the twist rate for cell I of a two-cell box")

        # ---- beat 4: build cell I's integral wall by wall
        top = E(r"\frac{d\theta}{dz}|=|\frac{1}{2A_R\,G}|\oint|q|\frac{ds}{t}", size=40)
        dl = E(r"\delta|=|\int|\frac{ds}{t}", size=44)
        dn = note("along one wall (or a whole cell)")
        l2 = E(r"\oint q\,\frac{ds}{t}|=|q_I|\Big(|\delta_I|-|\delta_{12}|\Big)|+|\Big(|q_I|-|q_{II}|\Big)|\delta_{12}",
               size=42, cmap=DCM)
        n2 = note("outer walls of cell I  +  the shared wall")
        l3 = E(r"=|q_I|\delta_I|-|q_{II}|\delta_{12}", size=44, cmap=DCM)
        col = VGroup(top, VGroup(dl, dn).arrange(RIGHT, buff=.45), VGroup(l2, n2).arrange(DOWN, buff=.25),
                     l3).arrange(DOWN, buff=.55)
        fit(col, 8.4, 6.4)
        col.move_to([RX, -.3, 0])
        l3.shift(RIGHT * (l2[1].get_center()[0] - l3[0].get_center()[0]))
        # walls of cell I and their flows
        outer = VGroup(*[sec.walls_m[k] for k in [("A", "B"), ("E", "F"), ("F", "A")]])
        fI = VGroup(flow(sec, "A", "B", 1, color=MINT, label="q_I"),
                    flow(sec, "E", "F", 1, color=MINT, label="q_I"),
                    flow(sec, "F", "A", 1, color=MINT, label="q_I"))
        fS = flow(sec, "B", "E", 1, color=GOLD, label=r"q_I - q_{II}")
        fII = cell_flow(cII + DOWN * .3, radius=.55, color=LIME, ccw=True, label="q_{II}")
        final = E(r"\frac{d\theta}{dz}\Big\vert_{\mathrm{I}}|=|\frac{1}{2A_{\mathrm{I}}\,G}|\Big(|q_I|\delta_I|-|q_{II}|\delta_{12}|\Big)",
                  size=48, cmap=DCM)
        final.move_to([RX, -.3, 0])
        frame_f = SurroundingRectangle(final, color=ACCENT, buff=.3)
        with self.say("Around cell one, every wall carries q one, except the shared wall, which carries q one minus q two. "
                      "Call delta the integral of d s over t. Then it's q one delta one, minus q two delta one two.") as d:
            self.play(ReplacementTransform(rate, top), FadeOut(rnotes), run_time=.07 * d)
            self.play(outer.animate.set_color(MINT), LaggedStart(*[FadeIn(f) for f in fI], lag_ratio=.4),
                      FadeIn(fII), run_time=.17 * d)
            self.play(FadeIn(fS), Indicate(shared, color=GOLD), run_time=.12 * d)
            self.wait(.04 * d)
            self.play(Write(dl), FadeIn(dn), run_time=.13 * d)
            self.play(Write(l2), FadeIn(n2), run_time=.16 * d)
            self.play(Write(l3), run_time=.1 * d)
            self.play(FadeIn(glow(VGroup(l3[1], l3[2], l3[3], l3[4]), MINT)), run_time=.05 * d)
            self.play(FadeOut(VGroup(dl, dn, l2, n2, l3, top)), run_time=.06 * d)
            self.play(Write(final), Create(frame_f), run_time=.1 * d)

        # ---- beat 5: the two equations
        eqA = E(r"\frac{1}{2A_{\mathrm{I}}\,G}|\Big(|q_I|\delta_I|-|q_{II}|\delta_{12}|\Big)|=|"
                r"\frac{1}{2A_{\mathrm{II}}\,G}|\Big(|-|q_I|\delta_{12}|+|q_{II}|\delta_{II}|\Big)", size=44, cmap=DCM)
        eqB = E(r"T|=|2A_{\mathrm{I}}\,|q_I|+|2A_{\mathrm{II}}\,|q_{II}", size=48)
        nA = note("equal twist:  cell I's rate = cell II's rate")
        nB = note("torque: each cell's flow adds 2 A q")
        bA = VGroup(eqA, nA).arrange(DOWN, buff=.3)
        bB = VGroup(eqB, nB).arrange(DOWN, buff=.3)
        stack = VGroup(bA, bB).arrange(DOWN, buff=1.0)
        fit(stack, 13.0, 5.6)
        stack.move_to(DOWN * .2)
        rA = SurroundingRectangle(eqA, color=ACCENT, buff=.25)
        rB = SurroundingRectangle(eqB, color=LILAC, buff=.25)
        tally = VGroup(T("two equations, two unknowns:", size=32), E(r"q_I|,\;|q_{II}", size=44)).arrange(RIGHT, buff=.3)
        tally.next_to(stack, DOWN, buff=.45)
        with self.say("Set cell one's rate equal to cell two's. With the torque equation, that's two equations for two unknowns.") as d:
            self.play(FadeOut(VGroup(box, labI, labII, fI, fS, fII, frame_f, final)), run_time=.12 * d)
            self.play(Write(eqA), FadeIn(nA), run_time=.25 * d)
            self.play(Create(rA), run_time=.08 * d)
            self.play(Write(eqB), FadeIn(nB), Create(rB), run_time=.22 * d)
            self.play(FadeIn(tally, shift=UP * .2), run_time=.13 * d)
            self.wait(.2 * d)
        self.wipe()
