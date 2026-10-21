"""S18: step one of the reverse problem, r and v in the perifocal frame (BRIEF.md S18)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# ---- facts (Kluever Example 3.1, Molniya, theta = 280 deg) ----
MU = 3.986e5                      # km^3/s^2
A_M, E_M = 26563.6, 0.7411        # km, -
TH_M = np.radians(280)
P_M = A_M * (1 - E_M ** 2)
H_M = np.sqrt(MU * P_M)
R_M = P_M / (1 + E_M * np.cos(TH_M))
check(P_M, 11974)
check(H_M, 69086)
check(R_M, 10609)
RP_M = R_M * np.array([np.cos(TH_M), np.sin(TH_M), 0])
VP_M = MU / H_M * np.array([-np.sin(TH_M), E_M + np.cos(TH_M), 0])
check(RP_M[0], 1842)
check(RP_M[1], -10448)
check(VP_M[0], 5.682)
check(VP_M[1], 5.278)
# beat-5 intermediate steps, each as shown on screen
check(np.cos(TH_M), .1736)
check(np.sin(TH_M), -.9848)
check(10609 * .1736, 1842)
check(10609 * -.9848, -10448)
check(398600 / 69086, 5.770)
check(MU / H_M, 5.770)
check(-np.sin(TH_M), .9848)
check(.7411 + np.cos(TH_M), .9147)
check(5.770 * .9848, 5.682)
check(5.770 * .9147, 5.278)

# ---- drawn orbit (not to scale): a = 3.0, e = 0.6 in Earth radii, flat in the p-q plane ----
A_D, E_D = 3.0, 0.6
P_D = A_D * (1 - E_D ** 2)
S = 1.1                           # screen units per Earth radius
F = np.array([-1.5, -0.6, 0])   # focus (Earth's center) on screen
VS = 1.0                          # drawn mu/h (screen units), only sets the velocity arrow length


def pt(th):
    r = P_D / (1 + E_D * np.cos(th))
    return F + S * r * np.array([np.cos(th), np.sin(th), 0])


def vel(th):
    return VS * np.array([-np.sin(th), E_D + np.cos(th), 0])


class S18_Perifocal_rv(VScene):
    budget = 145

    def construct(self):
        RX = 3.75                 # right column center
        # ---- beat 1: the reverse problem ----
        title = E(r"(a,\ e,\ |i|,\ |\Omega|,\ |\omega|,\ |\theta|)\;\longrightarrow\;(\vec r,\ \vec v)", size=56)
        title.move_to([0, 1.3, 0])
        box1 = panel(VGroup(T("Step 1", size=36, color=GOLD, weight=BOLD),
                            T("perifocal frame", size=34)).arrange(DOWN, buff=.2), color=GOLD)
        box2 = panel(VGroup(T("Step 2", size=36, color=INK2, weight=BOLD),
                            T("rotate into ECI", size=34)).arrange(DOWN, buff=.2), color=HAIR)
        box2.match_height(box1)
        steps = VGroup(box1, box2).arrange(RIGHT, buff=1.6).move_to([0, -1.1, 0])
        step_arrow = Arrow(box1.get_right(), box2.get_left(), buff=.2, color=MUTED, stroke_width=5)
        steps.add(step_arrow)
        self.beat("Sometimes we need the reverse: start from the elements and find r and v in E C I. It takes two steps, and the first one is easy.",
                  Write(title), .07, FadeIn(box1, shift=UP * .2), GrowArrow(step_arrow), FadeIn(box2, shift=UP * .2),
                  .13, Indicate(box1, color=GOLD, scale_factor=1.05), w=(.33, .12, .08, .12, .15))

        # ---- the orbit plane ----
        th = ValueTracker(np.radians(150))
        ell = ParametricFunction(pt, t_range=[0, TAU], color=INK, stroke_width=4)
        earth = Circle(radius=S, stroke_color=AXIS, stroke_width=2, fill_color=SKY, fill_opacity=.35).move_to(F)
        pax = Arrow(F, F + RIGHT * 1.65, buff=0, color=ROSE, stroke_width=4, max_tip_length_to_length_ratio=.1)
        qax = Arrow(F, F + UP * 2.85, buff=0, color=LIME, stroke_width=4, max_tip_length_to_length_ratio=.08)
        plab = M(r"\hat p", size=44, color=ROSE).next_to(pax.get_end(), DOWN, buff=.15)
        qlab = M(r"\hat q", size=44, color=LIME).next_to(qax.get_end(), LEFT, buff=.15)
        peri = Dot(pt(0), color=ROSE, radius=.06)
        plane = VGroup(earth, ell, pax, qax, plab, qlab, peri)

        rvec = always_redraw(lambda: Arrow(F, pt(th.get_value()), buff=0, color=INK, stroke_width=5,
                                           max_tip_length_to_length_ratio=.12))
        sat = always_redraw(lambda: Dot(pt(th.get_value()), color=INK, radius=.08).set_z_index(3))
        arc = always_redraw(lambda: Arc(radius=1.22 * S, start_angle=0, angle=th.get_value(), arc_center=F,
                                        color=GOLD, stroke_width=4))
        thlab = M(r"\theta", size=44, color=GOLD)
        thlab.add_updater(lambda m: m.move_to(F + 1.55 * S * np.array([np.cos(th.get_value() / 2),
                                                                  np.sin(th.get_value() / 2), 0])))
        projx = always_redraw(lambda: DashedLine(pt(th.get_value()), [pt(th.get_value())[0], F[1], 0],
                                                 color=MUTED, stroke_width=2))
        projy = always_redraw(lambda: DashedLine(pt(th.get_value()), [F[0], pt(th.get_value())[1], 0],
                                                 color=MUTED, stroke_width=2))

        def rlab_pos(m):
            t = th.get_value()
            a, b = F, pt(t)
            d = (b - a) / np.linalg.norm(b - a)
            nrm = np.array([-d[1], d[0], 0])
            if np.dot(nrm, [np.cos(t / 2), np.sin(t / 2), 0]) > 0:   # keep the label off the theta arc
                nrm = -nrm
            m.move_to(a + .55 * (b - a) + .38 * nrm)
        rlab = M(r"\vec r", size=44)
        rlab.add_updater(rlab_pos)

        # ---- beat 2: position ----
        req = E(r"\vec r_P = \big(|r\cos|\theta|,\ r\sin|\theta|,\ 0\big)", size=44)
        rorb = E(r"r = p\,/\,\big(1+e\cos|\theta|\big)", size=44)
        rnote = T("orbit equation", size=26, color=MUTED)
        fit(req, 6.6, 1.2)
        req.move_to([RX, 1.75, 0])
        rorb.move_to([RX, .75, 0])
        rnote.next_to(rorb, DOWN, buff=.18)
        with self.say("In the perifocal frame the orbit is flat. The position is r cosine theta, r sine theta, zero, where r comes from the orbit equation.") as d:
            self.play(FadeOut(steps), title.animate.scale(52 / 56).move_to([0, 3.3, 0]), FadeIn(earth), Create(ell), GrowArrow(pax), GrowArrow(qax),
                      FadeIn(plab), FadeIn(qlab), FadeIn(peri), run_time=.22 * d)
            self.play(FadeIn(rvec), FadeIn(sat), FadeIn(arc), FadeIn(thlab), FadeIn(rlab), run_time=.12 * d)
            self.play(Write(req), run_time=.18 * d)
            self.play(FadeIn(projx), FadeIn(projy), Indicate(req[1], color=INK2), run_time=.13 * d)
            self.play(Indicate(req[3], color=INK2), run_time=.1 * d)
            self.play(Write(rorb), FadeIn(rnote), run_time=.17 * d)
            self.wait(.08 * d)

        # ---- beat 3: velocity ----
        vvec = always_redraw(lambda: Arrow(pt(th.get_value()), pt(th.get_value()) + vel(th.get_value()), buff=0,
                                           color=ACCENT, stroke_width=5, max_tip_length_to_length_ratio=.2))
        vlab = M(r"\vec v", size=44, color=ACCENT)
        vlab.add_updater(lambda m: m.move_to(pt(th.get_value()) + vel(th.get_value())
                                             + .32 * vel(th.get_value()) / np.linalg.norm(vel(th.get_value()))))
        veq = E(r"\vec v_P|=\frac{\mu}{h}\Big(|-\sin|\theta|,\ e+\cos|\theta|,\ 0\Big)", size=44,
                cmap={r"\vec v_P": ACCENT})
        fit(veq, 6.6, 1.4)
        veq.move_to([RX, -.95, 0])
        vnote = T("hodograph result (last chapter)", size=26, color=MUTED).next_to(veq, DOWN, buff=.18)
        self.beat("The velocity is mu over h, times minus sine theta, e plus cosine theta, zero. That's the hodograph result from the last chapter.",
                  [FadeIn(vvec), FadeIn(vlab)], Write(veq), .1, FadeIn(vnote, shift=UP * .15), .1,
                  w=(.15, .45, .2))

        # ---- beat 4: the Molniya numbers at theta = 280 deg ----
        general = VGroup(req, veq)
        box_target = VGroup(req.copy(), veq.copy()).arrange(DOWN, buff=.35).move_to([RX, 1.55, 0])
        frame_box = SurroundingRectangle(box_target, color=HAIR, buff=.2, corner_radius=.12)
        head = E(r"\text{Molniya at }|\theta|=280^\circ", size=40).move_to([RX, -.05, 0])
        nums = VGroup(E(r"p = a(1-e^2) = 11{,}974\ \text{km}", size=40),
                      E(r"h = \sqrt{\mu p} = 69{,}086\ \text{km}^2/\text{s}", size=40),
                      E(r"r = p\,/\,\big(1+e\cos|\theta|\big) = 10{,}609\ \text{km}", size=40))
        nums.arrange(DOWN, buff=.3, aligned_edge=LEFT)
        fit(nums, 6.6, 2.6)
        nums.next_to(head, DOWN, buff=.35)
        with self.say("For the Molniya at theta equals two eighty: p is eleven thousand nine hundred seventy four kilometers, h is sixty nine thousand eighty six, and r is ten thousand six hundred nine.") as d:
            self.play(FadeOut(rorb), FadeOut(rnote), FadeOut(vnote), FadeOut(projx), FadeOut(projy),
                      run_time=.08 * d)
            self.play(req.animate.move_to(box_target[0]), veq.animate.move_to(box_target[1]),
                      Create(frame_box), run_time=.1 * d)
            self.play(th.animate.set_value(TH_M), FadeIn(head), run_time=.2 * d)
            self.play(FadeIn(nums[0], shift=UP * .15), run_time=.1 * d)
            self.wait(.12 * d)
            self.play(FadeIn(nums[1], shift=UP * .15), run_time=.1 * d)
            self.wait(.1 * d)
            self.play(FadeIn(nums[2], shift=UP * .15), run_time=.1 * d)
            self.wait(.1 * d)

        # ---- beat 5: the perifocal state vector, every substitution shown ----
        g = {"280^\\circ": GOLD, r"\vec v_P": ACCENT}
        r1 = E(r"\vec r_P = 10{,}609\,\big(\cos |280^\circ|,\ \sin |280^\circ|,\ 0\big)", size=40, cmap=g)
        r2 = E(r"= 10{,}609\,\big(0.1736,\ -0.9848,\ 0\big)", size=40)
        r3 = E(r"= (1{,}842,\ -10{,}448,\ 0)\ \text{km}", size=40)
        res_r = E(r"\vec r_P = (1{,}842,\ -10{,}448,\ 0)\ \text{km}", size=40)
        v1 = E(r"\vec v_P| = \frac{398{,}600}{69{,}086}\begin{pmatrix}-\sin 280^\circ\\ 0.7411+\cos 280^\circ\\ 0\end{pmatrix}",
               size=40, cmap=g)
        v2 = E(r"= 5.770\,\big(0.9848,\ 0.9147,\ 0\big)", size=40)
        v3 = E(r"= (5.682,\ 5.278,\ 0)\ \text{km/s}", size=40)
        res_v = E(r"\vec v_P| = (5.682,\ 5.278,\ 0)\ \text{km/s}", size=40, cmap=g)
        rchain = VGroup(r1, r2, r3).arrange(DOWN, buff=.3)
        for m in (r2, r3):
            m.align_to(r1[1], LEFT).shift(LEFT * M(r"=", size=40).width * 1.6)
        rchain.move_to([RX, .9, 0])
        res_r.move_to([RX, 1.55, 0])
        vchain = VGroup(v1, v2, v3).arrange(DOWN, buff=.3)
        for m in (v2, v3):
            m.align_to(v1[1], LEFT)
        vchain.next_to(res_r, DOWN, buff=.45)
        vchain.set_x(RX)
        res_v.next_to(res_r, DOWN, buff=.45)
        rP_lab = M(r"\vec r_P", size=44).move_to(rlab)
        vP_lab = M(r"\vec v_P", size=44, color=ACCENT).move_to(vlab)
        rlab.clear_updaters()
        vlab.clear_updaters()
        with self.say("So the position is one thousand eight hundred forty two, minus ten thousand four hundred forty eight, zero kilometers, and the velocity is five point six eight two, five point two seven eight, zero kilometers per second.") as d:
            self.play(FadeOut(nums), FadeOut(general), FadeOut(frame_box), head.animate.move_to([RX, 2.45, 0]),
                      run_time=.06 * d)
            self.play(FadeIn(r1, shift=UP * .15), run_time=.07 * d)
            self.play(FadeIn(r2, shift=UP * .15), run_time=.07 * d)
            self.play(FadeIn(r3, shift=UP * .15), Transform(rlab, rP_lab), Indicate(rvec, color=INK2),
                      run_time=.1 * d)
            self.play(FadeOut(r1), FadeOut(r2), ReplacementTransform(r3, res_r), run_time=.07 * d)
            self.snap("position done")
            self.play(FadeIn(v1, shift=UP * .15), run_time=.1 * d)
            self.play(FadeIn(v2, shift=UP * .15), run_time=.1 * d)
            self.play(FadeIn(v3, shift=UP * .15), Transform(vlab, vP_lab), Indicate(vvec, color=ACCENT),
                      run_time=.12 * d)
            self.play(FadeOut(v1), FadeOut(v2), ReplacementTransform(v3, res_v), run_time=.08 * d)
            self.play(FadeIn(glow(VGroup(res_r, res_v), ACCENT)), run_time=.08 * d)
            self.wait(.15 * d)
        thlab.clear_updaters()
        self.wipe()
