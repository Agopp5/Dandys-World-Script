"""S19: every cell twists the same (BRIEF.md S19). Rework of old/s13_twist.py, slower and larger."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

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


def note(s, size=30):
    return T(s, size=size, color=MUTED)


class S19_Twist(VScene):
    budget = 125

    def construct(self):
        self.section("Every cell twists the same")

        # two-cell box: A bottom-left, B/E the shared spar, C/D the right web, F top-left
        pts = {"A": (0, 0), "B": (240, 0), "C": (500, 50), "D": (500, 550), "E": (240, 600), "F": (0, 600)}
        walls = [("A", "B", 1.0), ("B", "C", 1.0), ("C", "D", 1.6), ("D", "E", 1.0),
                 ("E", "F", 1.0), ("F", "A", 1.6), ("B", "E", 2.0)]
        sec = Section(pts, walls, width=5.0, center=(-4.0, -0.5))
        box = sec.draw()
        shared = sec.walls_m[("B", "E")]
        shared.set_stroke(color=GOLD, width=8)
        cI = (sec.p("A") + sec.p("B") + sec.p("E") + sec.p("F")) / 4
        cII = (sec.p("B") + sec.p("C") + sec.p("D") + sec.p("E")) / 4
        labI = T("Cell I", size=36, color=MINT).move_to(cI + UP * 1.7)
        labII = T("Cell II", size=36, color=LIME).move_to(cII + UP * 1.7)
        pivot = (cI + cII) / 2
        RX = 2.9                                           # right column centre

        # ---- beat 1: the whole section rotates as one piece
        ghost = box.copy().set_stroke(color=MUTED, opacity=.45)
        fig = VGroup(box, labI, labII)
        twI = M(DTDZ, size=48, color=INK).move_to(cI + DOWN * .5)
        twII = M(DTDZ, size=48, color=INK).move_to(cII + DOWN * .5)
        same = M(r"\left.\frac{d\theta}{dz}\right|_{\mathrm{I}}", r"=",
                 r"\left.\frac{d\theta}{dz}\right|_{\mathrm{II}}", size=60)
        same.move_to([RX, .8, 0])
        same_n = VGroup(note("one rigid rotation:"),
                        note("the same rate of twist in every cell")).arrange(DOWN, buff=.18)
        same_n.next_to(same, DOWN, buff=.55)
        with self.say("The extra equations come from one simple fact. The whole wing box rotates as one piece, "
                      "so every cell must twist at the same rate.") as d:
            self.play(Create(box), FadeIn(labI), FadeIn(labII), run_time=.16 * d)
            self.wait(.06 * d)
            self.add(ghost)
            self.play(Rotate(fig, angle=8 * DEGREES, about_point=pivot), run_time=.18 * d)
            self.play(FadeIn(twI), FadeIn(twII), run_time=.1 * d)
            self.snap("rotated together")
            self.wait(.06 * d)
            self.play(Write(same), run_time=.14 * d)
            self.play(FadeIn(same_n), run_time=.08 * d)
            self.wait(.06 * d)
            self.play(Rotate(fig, angle=-8 * DEGREES, about_point=pivot), FadeOut(ghost),
                      FadeOut(twI), FadeOut(twII), run_time=.1 * d)
            self.wait(.06 * d)
        self.wait(1.0)

        # ---- beat 2: the twist rate of one cell
        rate = E(r"\frac{d\theta}{dz}|=|\frac{1}{2A_R\,G}|\oint|q|\frac{ds}{t}", size=60)
        rate.move_to([RX, 1.0, 0])
        rn1 = VGroup(M(r"A_R", size=44), note(": area enclosed by cell R")).arrange(RIGHT, buff=.15)
        rn2 = VGroup(M(r"\oint", size=44), note(": once around that cell's walls")).arrange(RIGHT, buff=.15)
        rnotes = VGroup(rn1, rn2).arrange(DOWN, buff=.4, aligned_edge=LEFT).next_to(rate, DOWN, buff=.7)
        fit(rnotes, 8.0, 2.4)
        cellI_fill = Polygon(sec.p("A"), sec.p("B"), sec.p("E"), sec.p("F"),
                             stroke_width=0, fill_color=MINT, fill_opacity=.12)
        self.beat("For each cell, the rate of twist is the same formula as before: one over two A G, "
                  "times the integral of q d s over t around that cell.",
                  [FadeOut(same), FadeOut(same_n)], Write(rate), .12, FadeIn(rn1), FadeIn(cellI_fill),
                  [FadeIn(rn2), Circumscribe(rate[3:], color=SKY)], .2,
                  w=(.08, .26, .12, .14, .22, .18))
        self.wait(1.0)

        # ---- beat 3: checkpoint
        self.beat("Your turn. Pause here and do checkpoint five point one in your guide.")
        self.checkpoint("5.1", "Write the twist rate for cell I of a two-cell box")

        # ---- beat 4: build cell I's integral wall by wall
        dl = VGroup(E(r"\delta|=|\int|\frac{ds}{t}", size=44), note("for one wall")).arrange(RIGHT, buff=.4)
        la = E(r"\oint q\,\frac{ds}{t}|=|q_I|\Big(|\delta_I|-|\delta_{12}|\Big)", size=46, cmap=DCM)
        na = note("outer walls of cell I")
        lb = E(r"+|\Big(|q_I|-|q_{II}|\Big)|\delta_{12}", size=46, cmap=DCM)
        nb = note("the shared wall")
        lc = E(r"=|q_I|\delta_I|-|q_{II}|\delta_{12}", size=50, cmap=DCM)
        nc = note("collect the terms")
        rowa = VGroup(la, na).arrange(DOWN, buff=.2)
        rowb = VGroup(lb, nb).arrange(DOWN, buff=.2)
        rowc = VGroup(lc, nc).arrange(DOWN, buff=.2)
        col = VGroup(dl, rowa, rowb, rowc).arrange(DOWN, buff=.5)
        fit(col, 8.2, 6.6)
        col.move_to([RX, -.45, 0])
        lb.shift(RIGHT * (la[1].get_center()[0] - lb[0].get_center()[0]))
        lc.shift(RIGHT * (la[1].get_center()[0] - lc[0].get_center()[0]))
        nb.next_to(lb, DOWN, buff=.2)
        nc.next_to(lc, DOWN, buff=.2)
        # walls of cell I and their flows
        outer = VGroup(*[sec.walls_m[k] for k in [("A", "B"), ("E", "F"), ("F", "A")]])
        fI = VGroup(flow(sec, "A", "B", 1, color=MINT, label="q_I", size=40),
                    flow(sec, "E", "F", 1, color=MINT, label="q_I", size=40),
                    flow(sec, "F", "A", 1, color=MINT, label="q_I", size=40))
        fS = VGroup(flow(sec, "B", "E", 1, color=GOLD),
                    backed(E(r"q_I|-|q_{II}", size=40)).next_to(sec.mid("B", "E"), RIGHT, buff=.45).shift(UP * .6))
        cf = cell_flow(cII + RIGHT * .3 + DOWN * 1.3, radius=.55, color=LIME, ccw=True)
        fII = VGroup(cf, M(r"q_{II}", size=40, color=LIME).move_to(cf))
        final = E(r"\frac{d\theta}{dz}\Big\vert_{\mathrm{I}}|=|\frac{1}{2A_{\mathrm{I}}\,G}|\Big(|q_I|\delta_I|-|q_{II}|\delta_{12}|\Big)",
                  size=52, cmap=DCM)
        fit(final, 8.2, 2)
        final.move_to([RX, -.3, 0])
        frame_f = SurroundingRectangle(final, color=ACCENT, buff=.3)
        with self.say("Going around cell one, every wall carries q one, except the shared wall, which carries "
                      "q one minus q two. Collect the terms. You get q one times delta one, minus q two times "
                      "delta one two.") as d:
            self.play(FadeOut(rate), FadeOut(rnotes), run_time=.05 * d)
            self.play(outer.animate.set_color(MINT), LaggedStart(*[FadeIn(f) for f in fI], lag_ratio=.4),
                      FadeIn(dl), run_time=.13 * d)
            self.play(Write(la), FadeIn(na), run_time=.1 * d)
            self.wait(.04 * d)
            self.play(FadeIn(fS), FadeIn(fII), Indicate(shared, color=GOLD), run_time=.1 * d)
            self.play(Write(lb), FadeIn(nb), run_time=.1 * d)
            self.wait(.06 * d)
            self.play(Write(lc), FadeIn(nc), run_time=.12 * d)
            gl = glow(VGroup(lc[1], lc[2], lc[3], lc[4]), MINT)
            self.play(FadeIn(gl), run_time=.05 * d)
            self.snap("built from the walls")
            self.wait(.08 * d)
            self.play(FadeOut(VGroup(dl, rowa, rowb, rowc, gl)), run_time=.06 * d)
            self.play(Write(final), Create(frame_f), run_time=.1 * d)
            self.wait(.01 * d)
        self.wait(1.2)

        # ---- beat 5: the two equations
        eqA1 = E(r"\frac{1}{2A_{\mathrm{I}}\,G}|\Big(|q_I|\delta_I|-|q_{II}|\delta_{12}|\Big)", size=50, cmap=DCM)
        eqA2 = E(r"=|\frac{1}{2A_{\mathrm{II}}\,G}|\Big(|-|q_I|\delta_{12}|+|q_{II}|\delta_{II}|\Big)", size=50, cmap=DCM)
        eqA = VGroup(eqA1, eqA2).arrange(RIGHT, buff=.25)
        eqB = E(r"T|=|2A_{\mathrm{I}}\,|q_I|+|2A_{\mathrm{II}}\,|q_{II}", size=54)
        nA = note("equal twist: cell I's rate = cell II's rate")
        nB = note("torque: each cell's flow adds 2 A q")
        bA = VGroup(eqA, nA).arrange(DOWN, buff=.35)
        bB = VGroup(eqB, nB).arrange(DOWN, buff=.35)
        stack = VGroup(bA, bB).arrange(DOWN, buff=1.0)
        fit(stack, 13.4, 5.8)
        stack.move_to(DOWN * .1)
        rA = SurroundingRectangle(eqA, color=ACCENT, buff=.25)
        rB = SurroundingRectangle(eqB, color=LILAC, buff=.25)
        tally = VGroup(T("two equations, two unknowns:", size=36), E(r"q_I|,\;|q_{II}", size=52)).arrange(RIGHT, buff=.3)
        tally.next_to(stack, DOWN, buff=.5)
        with self.say("Set cell one's rate equal to cell two's. Together with the torque equation, "
                      "that's two equations for the two unknowns.") as d:
            self.play(FadeOut(VGroup(box, labI, labII, fI, fS, fII, cellI_fill)),
                      final.animate.move_to(eqA1).scale(eqA1.height / final.height), FadeOut(frame_f),
                      run_time=.12 * d)
            self.play(FadeIn(eqA2), FadeOut(final), FadeIn(eqA1), run_time=.16 * d)
            self.play(FadeIn(nA), Create(rA), run_time=.08 * d)
            self.wait(.1 * d)
            self.play(Write(eqB), FadeIn(nB), Create(rB), run_time=.18 * d)
            self.wait(.08 * d)
            self.play(FadeIn(tally, shift=UP * .2), run_time=.1 * d)
            self.wait(.18 * d)
        self.wait(1.5)
        self.wipe()
