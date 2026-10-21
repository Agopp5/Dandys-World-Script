"""S03: Two ways to say the same thing (BRIEF.md S03)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# facts: the state vector shown (Kluever Example 3.1) and the drawn generic orbit
R0 = np.array([9031.5, -5316.9, -1647.2])      # km
V0 = np.array([-2.8640, 5.1112, -5.0805])      # km/s
assert np.isclose(np.linalg.norm(R0), 10609.0, rtol=1e-4)
assert np.isclose(np.linalg.norm(V0), 7.7549, rtol=1e-4)
RE = 6378.137
A, E0 = 2.4, 0.5                               # drawn generic orbit (not to scale)
OM, INC, W, TH0 = np.radians([50, 40, 60, 40])  # generic orientation for episode 2
assert np.isclose(A * (1 - E0), 1.2) and A * (1 + 0.7) < 4.2


class S03_Six_Numbers(VScene):
    budget = 113

    def construct(self):
        view = View(elev=22, azim=-55, scale=0.9)
        earth = globe(view)

        # ---- beat 1: the state vector -------------------------------------------------
        rN = R0 / np.linalg.norm(R0) * 2.6      # direction of r0 (not to scale)
        vdir = V0 / np.linalg.norm(V0) * 1.3    # direction only
        r_arr = arrow3(view, (0, 0, 0), rN, INK)
        v_arr = arrow3(view, rN, rN + vdir, ACCENT)
        sat = dot3(view, rN, INK)
        r_lab = label3(view, r"\vec r_0", rN * 0.55 + np.array([0, 0, 0.35]), INK, 34)
        v_lab = label3(view, r"\vec v_0", rN + vdir * 1.15, ACCENT, 34)
        r_arr.k.set_value(0)
        v_arr.k.set_value(0)

        def column(sym, color, entries, unit):
            mat = M(r"\begin{bmatrix}" + r"\\".join(entries) + r"\end{bmatrix}", size=34)
            return VGroup(M(sym, size=38, color=color), mat, T(unit, size=26, color=MUTED)).arrange(DOWN, buff=.2)

        rcol = column(r"\vec r_0", INK, ["9031.5", "-5316.9", "-1647.2"], "km")
        vcol = column(r"\vec v_0", ACCENT, ["-2.8640", "5.1112", "-5.0805"], "km/s")
        cols = VGroup(rcol, vcol).arrange(RIGHT, buff=.7, aligned_edge=UP)
        br = Brace(cols, DOWN, color=MUTED)
        br_lab = T("state vector, all six change", size=26, color=INK2).next_to(br, DOWN, buff=.15)
        state = place(VGroup(cols, br, br_lab), "right")

        self.add(earth, r_arr, v_arr)
        self.beat("Position and velocity together are called the state vector. Those six numbers completely determine the orbit.",
                  [r_arr.k.animate.set_value(1), FadeIn(sat), FadeIn(rcol)],
                  [v_arr.k.animate.set_value(1), FadeIn(r_lab), FadeIn(v_lab), FadeIn(vcol)],
                  [GrowFromCenter(br), FadeIn(br_lab, shift=UP * .2)],
                  Indicate(VGroup(rcol[1], vcol[1]), color=ACCENT), w=(.22, .22, .28, .28))

        # ---- beat 2: the six classical elements, in three groups ------------------------
        head = T("classical orbital elements", size=28, color=MUTED)
        g1 = panel(E(r"a|,\;|e", size=48))
        g2 = panel(E(r"i|,\;|\Omega|,\;|\omega", size=48))
        g3 = panel(E(r"\theta_0", size=48))
        cards = [g1, g2, g3]
        wmax = max(c[0].width for c in cards)
        for c in cards:
            c[0].stretch_to_fit_width(wmax)
        lst = place(VGroup(head, g1, g2, g3).arrange(DOWN, buff=.35), "right")

        self.beat("The classical orbital elements are a different six numbers that determine the same orbit.",
                  FadeOut(state, shift=UP * .3), FadeIn(head),
                  LaggedStart(*[FadeIn(c, shift=LEFT * .3) for c in cards], lag_ratio=.35),
                  w=(.2, .15, .65))

        def focus(k):
            anims = []
            for j, c in enumerate(cards):
                on = j == k
                anims.append(c[0].animate.set_stroke(ACCENT if on else HAIR, width=3 if on else 1.5))
                anims.append(c[1].animate.set_opacity(1 if on else .35))
            return anims

        # ---- beat 3: size and shape, a flat ellipse ---------------------------------------
        et = ValueTracker(E0)
        om, inc, w = ValueTracker(0), ValueTracker(0), ValueTracker(0)

        def Cm():
            return cpn(om.get_value(), inc.get_value(), w.get_value())

        def f(t):
            return orbit(A, et.get_value(), om.get_value(), inc.get_value(), w.get_value())(t)

        path = curve(view, f, 0, TAU, INK, width=4, R=1.0)
        center = lambda: -A * et.get_value() * Cm()[0]
        apo = lambda: -A * (1 + et.get_value()) * Cm()[0]
        peri = lambda: A * (1 - et.get_value()) * Cm()[0]
        a_line = line3(view, center, apo, ACCENT)
        a_dot = dot3(view, center, MUTED)
        a_lab = label3(view, "a", lambda: (center() + apo()) / 2 + 0.35 * Cm()[1], ACCENT, 40)
        e_read = readout(r"e =", lambda: et.get_value(), digits=2)
        e_read.move_to(np.array([-3.2, -3.3, 0]))

        with self.say("Two describe size and shape: the semi major axis a, and the eccentricity e. "
                      "You already know these from the last chapter.") as d:
            self.play(FadeOut(VGroup(r_arr, v_arr, sat, r_lab, v_lab)), *focus(0), run_time=.12 * d)
            self.play(view.elev.animate.set_value(88), view.azim.animate.set_value(-90), run_time=.15 * d)
            self.play(Create(path), run_time=.15 * d)
            self.play(FadeIn(a_line), FadeIn(a_dot), FadeIn(a_lab), FadeIn(e_read), run_time=.15 * d)
            self.play(et.animate.set_value(0.0), run_time=.1 * d)
            self.play(et.animate.set_value(0.7), run_time=.15 * d)
            self.play(et.animate.set_value(E0), run_time=.1 * d)

        # ---- beat 4: orientation, the ellipse lifts into 3D --------------------------------
        ax = axes3(view, 2.2)
        plane = disc3(view, lambda: Cm()[0], lambda: Cm()[1], 3.6, LILAC, .12)
        with self.say("Three describe orientation: how steeply the orbit plane is tilted, which way that tilt "
                      "faces, and how the ellipse is turned within its plane.") as d:
            self.play(FadeOut(VGroup(a_line, a_dot, a_lab)), *focus(1), run_time=.12 * d)
            self.play(view.elev.animate.set_value(22), view.azim.animate.set_value(-55),
                      FadeIn(ax), FadeIn(plane), run_time=.2 * d)
            self.play(inc.animate.set_value(INC), Indicate(g2[1][0]), run_time=.22 * d)
            self.play(om.animate.set_value(OM), Indicate(g2[1][2]), run_time=.22 * d)
            self.play(w.animate.set_value(W), Indicate(g2[1][4]), run_time=.22 * d)
            self.wait(.02 * d)

        # ---- beat 5: where the satellite is now --------------------------------------------
        peri_line = line3(view, (0, 0, 0), peri, ROSE)
        peri_dot = dot3(view, peri, ROSE)
        sat_line = line3(view, (0, 0, 0), lambda: f(TH0), GOLD)
        sat_dot = dot3(view, lambda: f(TH0), GOLD)
        th_arc = arc3(view, lambda: Cm()[2], lambda: Cm()[0], TH0, 1.7, GOLD)
        th_arc.k.set_value(0)
        self.add(th_arc)
        th_lab = label3(view, r"\theta_0", lambda: 2.05 * (np.cos(TH0 / 2) * Cm()[0] + np.sin(TH0 / 2) * Cm()[1]),
                        GOLD, 40)
        g3_glow = glow(g3[1], GOLD)
        self.beat("And one says where the satellite is at the moment of the measurement: "
                  "the true anomaly at epoch, theta zero.",
                  [*focus(2), FadeOut(e_read), FadeOut(ax), view.elev.animate.set_value(48)], [FadeIn(peri_line), FadeIn(peri_dot)],
                  [FadeIn(sat_line), FadeIn(sat_dot, scale=1.6)],
                  [th_arc.k.animate.set_value(1), FadeIn(th_lab)], FadeIn(g3_glow),
                  w=(.15, .15, .2, .25, .25))

        # ---- beat 6: key box ---------------------------------------------------------------
        kb = place(key_box(E(r"a|,\ |e|:\ \text{size, shape}", size=44),
                           E(r"i|,\ |\Omega|,\ |\omega|:\ \text{orientation}", size=44),
                           E(r"\theta_0|:\ \text{where, now}", size=44)), "full")
        with self.say("Five constants and one clock. Next, we'll build the three orientation angles, one turn at a time.") as d:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=.2 * d)
            self.play(FadeIn(kb, shift=UP * .2), run_time=.25 * d)
            self.wait(.55 * d)
        self.wipe()
