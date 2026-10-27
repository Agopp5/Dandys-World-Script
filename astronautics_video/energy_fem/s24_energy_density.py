"""S24: strain energy, piece by piece (BRIEF.md S24)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

CM = {"U^*": MINT, "E": LILAC, r"\varepsilon^2": ACCENT, "q^2": SKY}

# facts: the triangle under sigma = E eps, from 0 to eps0, has area (1/2) eps0 (E eps0) = (1/2) E eps0^2
for Ev, e0 in [(70000.0, 1e-3), (2.0, 0.75)]:
    xs = np.linspace(0, e0, 2001)
    assert np.isclose(np.trapezoid(Ev * xs, xs), 0.5 * e0 * (Ev * e0))
    assert np.isclose(0.5 * e0 * (Ev * e0), 0.5 * Ev * e0 ** 2)
# rescaling: (sigma A)(eps dx) = (sigma eps) A dx, so the force-stretch triangle is the stress-strain one times A dx
A_, dx_, Ev, e0 = 3.0, 0.2, 5.0, 0.4
assert np.isclose(0.5 * (Ev * e0 * A_) * (e0 * dx_), 0.5 * Ev * e0 ** 2 * (A_ * dx_))
# the spring analogue from before: K = 20 N/mm, q = 5 mm -> U = 250 N mm
assert np.isclose(0.5 * 20 * 5 ** 2, 250)

SL = 0.85       # slope of the drawn line (E in plot units)
E0 = 0.75       # strain at which the triangle is drawn


class S24_Energy_Density(VScene):
    budget = 159

    def construct(self):
        frame = self.camera.frame
        # ---------- beat 1: the bar, zoom on a slice ----------
        wl = wall(np.array([-6.4, 0, 0]), side=LEFT, h=1.6)
        br = bar(-6.4, 6.4, y=0.0, h=0.6)
        x0, x1 = -0.75, -0.45
        sl = Rectangle(width=x1 - x0, height=0.6, stroke_color=ACCENT, stroke_width=3,
                       fill_color=ACCENT, fill_opacity=0.35).move_to([(x0 + x1) / 2, 0, 0])
        cx, w0, h0 = -3.8, 2.4, 3.4
        big = Rectangle(width=w0, height=h0, stroke_color=ACCENT, stroke_width=4,
                        fill_color=ACCENT, fill_opacity=0.18).move_to([cx, 0.1, 0])
        ghost = DashedVMobject(big.copy().set_fill(opacity=0).set_stroke(MUTED, 3), num_dashes=40)
        st = 0.5
        big_s = Rectangle(width=w0 + st, height=h0, stroke_color=ACCENT, stroke_width=4,
                          fill_color=ACCENT, fill_opacity=0.18).move_to([cx + st / 2, 0.1, 0])
        lft, rgt = cx - w0 / 2, cx + w0 / 2 + st
        aL = Arrow([lft, 0.1, 0], [lft - 1.2, 0.1, 0], buff=0, color=ACCENT, stroke_width=7)
        aR = Arrow([rgt, 0.1, 0], [rgt + 1.2, 0.1, 0], buff=0, color=ACCENT, stroke_width=7)
        sgL = M(r"\sigma", size=52, color=ACCENT).next_to(aL, UP, buff=0.15)
        sgR = M(r"\sigma", size=52, color=ACCENT).next_to(aR, UP, buff=0.15)
        brc = BraceBetweenPoints([lft, -1.75, 0], [lft + w0, -1.75, 0], DOWN, color=INK2)
        dxl = M(r"dx", size=48).next_to(brc, DOWN, buff=0.12)
        epl = VGroup(T("strain", size=34, color=ACCENT), M(r"\varepsilon", size=52, color=ACCENT)) \
            .arrange(RIGHT, buff=0.2).next_to(big_s, UP, buff=0.3)
        stl = T("stress", size=34, color=ACCENT).next_to(aR, DOWN, buff=0.2)
        with self.say("To find the energy in the bar, zoom in on a tiny slice, of length d x. Inside it, the "
                      "material is stretched by a strain epsilon, and carries a stress sigma.") as d:
            self.play(FadeIn(wl), FadeIn(br), run_time=.12 * d)
            self.play(FadeIn(sl), Indicate(sl, color=ACCENT, scale_factor=1.6), run_time=.1 * d)
            frame.save_state()
            self.play(frame.animate.scale(0.22).move_to(sl), run_time=.14 * d)
            self.play(Restore(frame), FadeOut(wl), FadeOut(br), ReplacementTransform(sl, big),
                      run_time=.14 * d)
            self.play(GrowFromCenter(brc), FadeIn(dxl), run_time=.1 * d)
            self.add(ghost)
            self.play(Transform(big, big_s), run_time=.12 * d)
            self.play(FadeIn(epl, shift=DOWN * .2), run_time=.1 * d)
            self.play(GrowArrow(aL), GrowArrow(aR), FadeIn(sgL), FadeIn(sgR), FadeIn(stl), run_time=.12 * d)
            self.wait(.06 * d)
        slice_grp = VGroup(big, ghost, aL, aR, sgL, sgR, brc, dxl, epl, stl)

        # ---------- beat 2: the stress-strain line ----------
        ax = axes((0, 1, 0.25), (0, 1, 0.25), width=5.2, height=5.0, xlabel=r"\varepsilon", ylabel=r"\sigma")
        ax.remove(*ax.submobjects[2:])
        ax.move_to([3.9, -0.3, 0])
        xl = M(r"\varepsilon", size=52, color=ACCENT).next_to(ax.c2p(1, 0), DOWN, buff=0.3)
        yl = M(r"\sigma", size=52, color=ACCENT).next_to(ax.c2p(0, 1), LEFT, buff=0.3)
        line = ax.plot(lambda e: SL * e, x_range=[0, 1], color=LILAC, stroke_width=6)
        p0, p1 = ax.c2p(0.25, SL * 0.25), ax.c2p(0.45, SL * 0.25)
        p2 = ax.c2p(0.45, SL * 0.45)
        run = Line(p0, p1, color=INK2, stroke_width=3)
        rise = Line(p1, p2, color=LILAC, stroke_width=4)
        one = M("1", size=40, color=INK2).next_to(run, DOWN, buff=0.12)
        Elab = M("E", size=44, color=LILAC).next_to(rise, RIGHT, buff=0.12)
        hooke = E(r"\sigma|=|E|\varepsilon", size=52, cmap=CM).move_to(ax.c2p(0.3, 0.88))
        hk = T("Hooke's law", size=32, color=MUTED).next_to(hooke, UP, buff=0.2)
        self.beat("For an elastic material, stress and strain are related by Hooke's law: sigma equals E times "
                  "epsilon. On a graph, a straight line from the origin with slope E.",
                  [Create(ax), FadeIn(xl), FadeIn(yl)], [Write(hooke), FadeIn(hk)], .1, Create(line),
                  [Create(run), Create(rise), FadeIn(one), FadeIn(Elab)], .2, w=(.2, .3, .25, .25))

        # ---------- beat 3: rescale to the spring graph ----------
        Al = M("A", size=52, color=INK).move_to(big_s)
        alab = T("area", size=32, color=INK2).next_to(Al, DOWN, buff=0.15)
        xl2 = VGroup(T("stretch", size=34, color=SKY), M(r"\varepsilon\,dx", size=48, color=SKY)) \
            .arrange(RIGHT, buff=0.2).next_to(ax.c2p(1, 0), DOWN, buff=0.3).align_to(ax.c2p(1, 0), RIGHT)
        yl2 = VGroup(T("force", size=34, color=ROSE), M(r"\sigma A", size=48, color=ROSE)) \
            .arrange(RIGHT, buff=0.2).next_to(ax.c2p(0, 1), UP, buff=0.25).align_to(ax.c2p(0, 1), LEFT)
        g_old = Polygon(ax.c2p(0, 0), ax.c2p(0.5, 0), ax.c2p(0.5, 0.5 * 1.7), color=INK2, stroke_width=4)
        g_old = DashedVMobject(g_old, num_dashes=36)
        g_new = DashedVMobject(Polygon(ax.c2p(0, 0), ax.c2p(E0, 0), ax.c2p(E0, SL * E0), stroke_width=4,
                                       color=INK2), num_dashes=36)
        gl = E(r"F|=|K|q", size=44).next_to(ax.c2p(0.05, 0.78), RIGHT, buff=0)
        gtag = T("the spring", size=32, color=INK2).next_to(gl, UP, buff=0.15).align_to(gl, LEFT)
        self.beat("Now connect it to the spring. Stress times the slice's area A is a force. Strain times its "
                  "length d x is a stretch. So this graph is just the spring's force-stretch graph, rescaled.",
                  [FadeOut(hooke), FadeOut(hk), FadeOut(VGroup(run, rise, one, Elab))],
                  [FadeIn(Al), FadeIn(alab)], [ReplacementTransform(yl, yl2), Indicate(Al)],
                  [ReplacementTransform(xl, xl2), Indicate(dxl)],
                  [FadeIn(g_old), FadeIn(gl), FadeIn(gtag)], Transform(g_old, g_new), .1,
                  w=(.06, .14, .22, .22, .18, .18))

        # ---------- beat 4: the triangle and U* ----------
        tri = Polygon(ax.c2p(0, 0), ax.c2p(E0, 0), ax.c2p(E0, SL * E0), stroke_width=0,
                      fill_color=MINT, fill_opacity=0.5)
        vline = DashedLine(ax.c2p(E0, 0), ax.c2p(E0, SL * E0), color=INK2, stroke_width=3)
        bl = M(r"\varepsilon", size=48, color=ACCENT).next_to(ax.c2p(E0 / 2, 0), UP, buff=0.15)
        hl = E(r"E|\varepsilon", size=48, cmap=CM).next_to(vline, RIGHT, buff=0.15)
        xl3 = M(r"\varepsilon", size=52, color=ACCENT).next_to(ax.c2p(1, 0), DOWN, buff=0.3)
        yl3 = M(r"\sigma", size=52, color=ACCENT).next_to(ax.c2p(0, 1), UP, buff=0.25)
        note = E(r"\text{slice}|=|\text{area}|\times|A\,dx", size=44, cmap={r"\text{area}": MINT}) \
            .move_to([-3.6, 2.6, 0])
        pv = T("per unit volume:", size=32, color=MUTED).move_to([-3.6, 1.3, 0])
        eq1 = E(r"U^*|=|\tfrac12|\varepsilon|\cdot|E|\varepsilon", size=56, cmap=CM).move_to([-3.6, 0.2, 0])
        eq2 = E(r"=|\tfrac12|E|\varepsilon^2", size=56, cmap=CM)
        eq2.next_to(eq1, DOWN, buff=0.55)
        eq2.shift((eq1[1].get_center()[0] - eq2[0].get_center()[0]) * RIGHT)
        with self.say("So the slice stores the area of the triangle under the line, times A d x. Per unit volume, "
                      "the energy is just the triangle's area: half base times height, one half, epsilon, times "
                      "E epsilon.") as d:
            self.play(FadeOut(gl), FadeOut(gtag), FadeOut(g_old), FadeIn(tri), Create(vline), run_time=.12 * d)
            self.play(FadeOut(slice_grp), FadeOut(Al), FadeOut(alab), FadeIn(note), run_time=.14 * d)
            self.play(ReplacementTransform(xl2, xl3), ReplacementTransform(yl2, yl3), FadeIn(pv),
                      run_time=.12 * d)
            self.play(FadeIn(bl), FadeIn(hl), run_time=.1 * d)
            self.play(Write(eq1[0:3]), run_time=.12 * d)
            self.play(TransformFromCopy(bl, eq1[3]), run_time=.1 * d)
            self.play(FadeIn(eq1[4]), TransformFromCopy(hl, eq1[5:7]), run_time=.12 * d)
            self.play(FadeIn(eq2[0]), TransformFromCopy(eq1[2], eq2[1]), TransformFromCopy(eq1[5], eq2[2]),
                      TransformFromCopy(VGroup(eq1[3], eq1[6]), eq2[3]), run_time=.12 * d)
            self.play(Indicate(eq2[3], color=ACCENT), run_time=.06 * d)

        # ---------- beat 5: name it, compare with the spring ----------
        eqA = E(r"U^*|=|\tfrac12|E|\varepsilon^2", size=56, cmap=CM).move_to([-3.6, 1.7, 0])
        tagA = T("strain energy per unit volume", size=32, color=MINT).next_to(eqA, UP, buff=0.3)
        eqB = E(r"U|=|\tfrac12|K|q^2", size=56, cmap=CM).move_to([-3.6, -0.6, 0])
        eqB.shift((eqA[1].get_center()[0] - eqB[1].get_center()[0]) * RIGHT)
        tagB = T("the spring", size=32, color=MUTED).next_to(eqB, UP, buff=0.3)
        bx_k = VGroup(*[Underline(e[3], color=LILAC, buff=.1, stroke_width=6) for e in (eqA, eqB)])
        bx_d = VGroup(*[Underline(e[4], color=SKY, buff=.1, stroke_width=6) for e in (eqA, eqB)])
        bx_h = VGroup(*[Underline(e[2], color=INK2, buff=.1, stroke_width=6) for e in (eqA, eqB)])
        lk = T("stiffness", size=34, color=LILAC)
        ld = T("deformation", size=34, color=SKY)
        lh = T("one half", size=34, color=INK2)
        legend = VGroup(lk, ld, lh).arrange(RIGHT, buff=0.5).move_to([-3.6, -2.4, 0])
        self.beat("We'll call it U star: the strain energy per unit volume. It's the same shape as one half K q "
                  "squared. Stiffness, times deformation, squared, times one half.",
                  [FadeOut(note), FadeOut(pv), FadeOut(eq1[1:]), ReplacementTransform(VGroup(eq1[0], *eq2), eqA)],
                  [FadeIn(tagA), FadeIn(glow(eqA[0], MINT))], [FadeIn(eqB), FadeIn(tagB)],
                  [Create(bx_k), FadeIn(lk)], [Create(bx_d), FadeIn(ld)],
                  [Indicate(eqA[4]), Indicate(eqB[4])], [Create(bx_h), FadeIn(lh)], .1,
                  w=(.12, .14, .18, .14, .14, .12, .16))
        self.wipe()
