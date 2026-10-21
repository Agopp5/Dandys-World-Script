"""S22: the critical inclination (BRIEF.md S22)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# ---- facts -------------------------------------------------------------------------------------------
bracket = lambda deg: 2.5 * np.sin(np.radians(deg)) ** 2 - 2
I_CRIT = np.degrees(np.arcsin(np.sqrt(4 / 5)))
assert np.isclose(I_CRIT, 63.43, atol=5e-3) and np.isclose(180 - I_CRIT, 116.57, atol=5e-3)
assert abs(bracket(I_CRIT)) < 1e-12 and bracket(50) < 0 and bracket(90) > 0
MU, RE, J2 = 3.986e5, 6378.137, 1.08263e-3
A_M, E_M, I_M = 26563.6, 0.7411, 63.4


def rates(a, e, i_deg):
    """Secular J2 rates in deg/day: (Omega-dot, omega-dot)."""
    n = np.sqrt(MU / a ** 3)
    k = -3 * n * J2 * RE ** 2 / (2 * a ** 2 * (1 - e ** 2) ** 2)
    day = np.degrees(86400.0)
    return k * np.cos(np.radians(i_deg)) * day, k * bracket(i_deg) * day


Od_M, wd_M = rates(A_M, E_M, I_M)
assert np.isclose(Od_M, -0.149, atol=2e-3) and abs(wd_M) < 2e-3      # node -0.15 deg/day, perigee frozen
assert np.isclose(round(Od_M, 2), -0.15)
# the hook's six elements (Kluever Example 3.1)
assert np.isclose(-MU / (2 * (7.7549 ** 2 / 2 - MU / 10609.0)), 26563.6, rtol=1e-3)

DEG = PI / 180


class S22_Critical(VScene):
    budget = 157

    def construct(self):
        # ---- beat 1: the omega-dot formula --------------------------------------------------------
        wdot = E(r"\dot{\omega}|=|-\frac{3\, n\, J_2 R^2}{2\, a^2 (1-e^2)^2}|\Big(\tfrac{5}{2}\sin^2|i|-\,2\Big)",
                 size=46)
        paint(wdot[0], {0: MINT})
        wdot[0].set_color(MINT)
        wdot.to_edge(UP, buff=0.45)
        brk = VGroup(wdot[3], wdot[4], wdot[5])
        self.beat("J two turns the ellipse inside its plane too. The perigee drifts at omega dot equals minus "
                  "three n J two R squared over two a squared, one minus e squared, squared, times five halves "
                  "sine squared i, minus two.",
                  Write(wdot), .15, Circumscribe(brk, color=GOLD), w=(.7, .3))

        # ---- beat 2: plot the bracket --------------------------------------------------------------
        ax = axes([0, 180, 30], [-2.0, 0.5, 0.5], width=7.6, height=4.6, xlabel="", ylabel="")
        ax.to_corner(DL, buff=1.0).shift(0.6 * RIGHT)
        g = ax.plot(lambda x: bracket(x), x_range=[0, 180, 0.5], color=INK, stroke_width=5)
        pos = ax.get_area(g, x_range=[I_CRIT, 180 - I_CRIT], color=MINT, opacity=0.45)
        neg = VGroup(ax.get_area(g, x_range=[0, I_CRIT], color=ROSE, opacity=0.35),
                     ax.get_area(g, x_range=[180 - I_CRIT, 180], color=ROSE, opacity=0.35))
        plus = M(r"\dot{\omega} > 0", size=34, color=MINT).move_to(ax.c2p(90, -0.55))
        minus = M(r"\dot{\omega} < 0", size=34, color=ROSE).move_to(ax.c2p(30, -0.45))
        ticks = VGroup(*[M(str(x) + r"^\circ", size=30, color=INK2).next_to(ax.c2p(x, -2.0), DOWN, buff=0.2)
                         for x in (0, 90, 180)])
        ticks.add(M("0", size=30, color=INK2).next_to(ax.c2p(0, 0), LEFT, buff=0.2),
                  M("-2", size=30, color=INK2).next_to(ax.c2p(0, -2), LEFT, buff=0.2))
        xl = E(r"i", size=40).next_to(ax.c2p(180, 0), RIGHT, buff=0.25)
        yl = M(r"\tfrac{5}{2}\sin^2 i-2", size=36).next_to(ax.c2p(0, 0.5), UP, buff=0.15).shift(0.6 * RIGHT)
        tint(yl, [((7, 8), EMBER)])
        self.beat("The sign depends on that last bracket. Here it is, plotted against inclination.",
                  Indicate(brk, color=GOLD), [Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl)], Create(g), [FadeIn(pos), FadeIn(neg)],
                  [FadeIn(plus), FadeIn(minus)], w=(.15, .2, .3, .2, .15))

        # ---- beat 3: solve for the zero ------------------------------------------------------------
        s1 = E(r"\tfrac{5}{2}\sin^2|i|=|2", size=44)
        s2 = E(r"\sin^2|i|=|\tfrac{4}{5}", size=44)
        s3 = E(r"i|=|63.43^\circ", size=48)
        s3b = T("(or 116.57°)", size=28, color=MUTED)
        steps = VGroup(s1, s2, s3).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        steps.next_to(ax, RIGHT, buff=0.7).shift(0.3 * UP)
        s3b.next_to(s3, DOWN, buff=0.25, aligned_edge=LEFT)
        z1, z2 = Dot(ax.c2p(I_CRIT, 0), color=GOLD, radius=0.11), Dot(ax.c2p(180 - I_CRIT, 0), color=GOLD, radius=0.11)
        zl1 = M(r"63.43^\circ", size=30, color=GOLD).next_to(z1, UP, buff=0.2).shift(0.45 * LEFT)
        zl2 = M(r"116.57^\circ", size=30, color=GOLD).next_to(z2, UP, buff=0.2).shift(0.5 * RIGHT)
        box = SurroundingRectangle(s3, color=GOLD, buff=0.15)
        self.beat("It crosses zero when five halves sine squared i equals two. So sine squared i is four fifths, "
                  "and i is sixty three point four three degrees.",
                  [FadeIn(z1, scale=2), FadeIn(z2, scale=2)], Write(s1), Write(s2), Write(s3),
                  [Create(box), FadeIn(s3b), FadeIn(zl1), FadeIn(zl2)], w=(.15, .25, .2, .2, .2))

        # ---- beat 4: perigee frozen at 63.4, drifting at 50 ------------------------------------------
        self.drop(wdot, ax, ticks, xl, yl, g, pos, neg, plus, minus, steps, s3b, z1, z2, zl1, zl2, box)
        vL = View(elev=20, azim=-60, scale=0.95, center=(-3.6, -0.7))
        vR = View(elev=20, azim=-60, scale=0.95, center=(3.6, -0.7))
        Om0, w0 = 50 * DEG, 60 * DEG
        t = ValueTracker(0)
        wL = lambda: w0 - 75 * DEG * t.get_value()           # perigee regresses (bracket < 0), sped up
        earthL, earthR = globe(vL), globe(vR)
        orbL = always_redraw(lambda: curve(vL, orbit(2.4, 0.5, Om0, 50 * DEG, wL()), 0, TAU, INK, R=1.0))
        orbR = curve(vR, orbit(2.4, 0.5, Om0, I_CRIT * DEG, w0), 0, TAU, INK, R=1.0)
        oldL = line3(vL, (0, 0, 0), orbit(2.4, 0.5, Om0, 50 * DEG, w0)(0), MUTED, dashed=True)
        apsL = always_redraw(lambda: line3(vL, (0, 0, 0), orbit(2.4, 0.5, Om0, 50 * DEG, wL())(0), ROSE))
        apsR = line3(vR, (0, 0, 0), orbit(2.4, 0.5, Om0, I_CRIT * DEG, w0)(0), ROSE)
        pL = dot3(vL, lambda: orbit(2.4, 0.5, Om0, 50 * DEG, wL())(0), ROSE)
        pR = dot3(vR, orbit(2.4, 0.5, Om0, I_CRIT * DEG, w0)(0), ROSE)
        for m in (pL, pR):
            m.set_z_index(5)
        hL = VGroup(E(r"i|=|50^\circ", size=42), M(r"\dot{\omega} < 0", size=40, color=ROSE)).arrange(RIGHT, buff=0.6)
        hR = VGroup(E(r"i|=|63.4^\circ", size=42), M(r"\dot{\omega} = 0", size=40, color=MINT)).arrange(RIGHT, buff=0.6)
        hL.move_to([-3.6, 3.2, 0])
        hR.move_to([3.6, 3.2, 0])
        note = T("perigee drift sped up", size=26, color=MUTED).to_edge(DOWN, buff=0.3)
        crit = T("critical inclination", size=34, color=GOLD).next_to(hR, DOWN, buff=0.3)
        with self.say("At that inclination, the perigee simply stops turning. It's called the critical "
                      "inclination.") as d:
            self.play(FadeIn(earthL), FadeIn(earthR), Create(orbL), Create(orbR), FadeIn(hL), FadeIn(hR),
                      run_time=.25 * d)
            self.add(oldL)
            self.play(FadeIn(apsL), FadeIn(apsR), FadeIn(pL), FadeIn(pR), FadeIn(note), run_time=.12 * d)
            self.play(t.animate.set_value(0.6), run_time=.38 * d, rate_func=linear)
            self.play(t.animate.set_value(1.0), FadeIn(crit, shift=.2 * DOWN), Indicate(pR, color=GOLD),
                      run_time=.25 * d, rate_func=linear)
        orbL.clear_updaters()
        apsL.clear_updaters()
        self.drop(earthL, earthR, orbL, orbR, oldL, apsL, apsR, pL, pR, hL, hR, note, crit)

        # ---- beat 5: the hook's six elements return ------------------------------------------------
        rows = [E(r"a|=|26{,}564\ \text{km}", size=42), E(r"e|=|0.741", size=42),
                E(r"i|=|63.4^\circ", size=42), E(r"\Omega|=|145^\circ", size=42),
                E(r"\omega|=|270^\circ", size=42), E(r"\theta_0|=|280^\circ", size=42)]
        grid = VGroup(*rows).arrange_in_grid(3, 2, buff=(1.4, 0.55), col_alignments="ll", flow_order="dr")
        card = panel(grid)
        head = T("The hook's orbit: Molniya", size=34, color=INK2).next_to(card, UP, buff=0.35)
        VGroup(head, card).move_to(ORIGIN)
        acc = T("63.4° = the critical inclination", size=32, color=GOLD).next_to(card, DOWN, buff=0.4)
        self.beat("Now look back at the hook. The Molniya orbit was inclined at sixty three point four degrees. "
                  "That's no accident.",
                  [FadeIn(head), FadeIn(card)], .1, FadeIn(glow(rows[2], EMBER)), Circumscribe(rows[2], color=EMBER),
                  FadeIn(acc, shift=.2 * UP), w=(.25, .2, .2, .25))

        # ---- beat 6: Molniya in 3D, perigee parked, node drifting ------------------------------------
        self.wipe()
        v = View(elev=12, azim=-35, scale=0.9, center=(-3.0, -2.2))
        Om = ValueTracker(145 * DEG)
        aM, eM, iM, wM = 3.0, 0.6, I_M * DEG, 270 * DEG
        fM = lambda: orbit(aM, eM, Om.get_value(), iM, wM)
        earth = globe(v)
        orb = always_redraw(lambda: curve(v, fM(), 0, TAU, INK, R=1.0))
        nhat = lambda: np.array([np.cos(Om.get_value()), np.sin(Om.get_value()), 0.0])
        node = always_redraw(lambda: line3(v, -3.0 * nhat(), 3.0 * nhat(), SKY, dashed=True))
        peri = dot3(v, lambda: fM()(0), ROSE)
        apo = dot3(v, lambda: fM()(PI), GOLD)
        peri.set_z_index(5)
        apo.set_z_index(5)
        plab = always_redraw(lambda: T("perigee (south)", size=28, color=ROSE).next_to(peri, DOWN, buff=0.2))
        alab = always_redraw(lambda: T("apogee (north)", size=28, color=GOLD).next_to(apo, RIGHT, buff=0.3))
        r1 = E(r"\dot{\omega}|=|0", size=48)
        r1[0].set_color(MINT)
        r2 = E(r"\dot{\Omega}|=|-0.15^\circ/\text{day}", size=48)
        r2[0].set_color(SKY)
        n1 = T("perigee frozen: no fuel spent", size=28, color=MUTED)
        n2 = T("node drifts slowly (sped up here)", size=28, color=MUTED)
        side = VGroup(r1, n1, r2, n2).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        n1.shift(0.1 * UP)
        n2.shift(0.1 * UP)
        place(side, "right")
        with self.say("At that inclination, the perigee stays parked over the south, so the long, slow apogee "
                      "stays over Russia, year after year, with no fuel spent. Its node still drifts a little, about point one five degrees per day, but that doesn't "
                      "matter for coverage.") as d:
            self.play(FadeIn(earth), Create(orb), run_time=.15 * d)
            self.play(FadeIn(peri, scale=2), FadeIn(apo, scale=2), FadeIn(plab), FadeIn(alab), run_time=.12 * d)
            self.play(Write(r1), FadeIn(n1), Indicate(peri, color=ROSE), run_time=.18 * d)
            self.wait(.08 * d)
            self.play(Create(node), Write(r2), FadeIn(n2), run_time=.15 * d)
            self.play(Om.animate.set_value(115 * DEG), run_time=.32 * d, rate_func=linear)
        for m in (orb, node, plab, alab):
            m.clear_updaters()
        self.wipe()
