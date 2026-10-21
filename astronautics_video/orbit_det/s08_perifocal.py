"""S08: a frame that rides on the orbit (BRIEF.md S08)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# generic orbit of episode 2 (drawn size, not to scale)
A, ECC = 2.4, 0.5
OM, INC, W, TH0 = np.radians(50), np.radians(40), np.radians(60), np.radians(40)
CM = cpn(OM, INC, W)
P_HAT, Q_HAT, H_HAT = CM[0], CM[1], CM[2]
F = orbit(A, ECC, OM, INC, W)

# facts: the frame is right-handed and orthonormal, periapsis lies along p-hat, h-hat is normal to the plane
assert np.allclose(CM @ CM.T, np.eye(3), atol=1e-9)
assert np.allclose(np.cross(H_HAT, P_HAT), Q_HAT, atol=1e-9)
assert np.allclose(F(0.0), A * (1 - ECC) * P_HAT, atol=1e-9)
assert abs(np.dot(F(1.234), H_HAT)) < 1e-9
# q-hat is ninety degrees ahead of p-hat: the point at theta = 90 deg lies along q-hat
assert np.allclose(F(PI / 2) / np.linalg.norm(F(PI / 2)), Q_HAT, atol=1e-9)
# perifocal position at theta: (r cos theta, r sin theta, 0), the same point the 3D orbit draws
P_SL = A * (1 - ECC ** 2)
R0 = P_SL / (1 + ECC * np.cos(TH0))
rP, vP = rv_perifocal(A, ECC, TH0)
assert np.allclose(np.asarray(rP)[:2], [R0 * np.cos(TH0), R0 * np.sin(TH0)], atol=1e-9)
assert abs(np.asarray(rP)[2]) < 1e-12
assert np.allclose(CM.T @ np.asarray(rP), F(TH0), atol=1e-9)

# flat (2D) view of the orbit plane, on the right
S2 = 1.05                        # screen units per Earth radius in the flat view
FOC = np.array([4.6, 0.95, 0.0])  # the focus on screen


def flat(th):
    r = P_SL / (1 + ECC * np.cos(th))
    return FOC + S2 * np.array([r * np.cos(th), r * np.sin(th), 0.0])


class S08_Perifocal(VScene):
    budget = 120

    def construct(self):
        view = View(elev=22, azim=-55, scale=1.0, center=(-3.2, -0.3))
        earth = globe(view)
        plane = disc3(view, P_HAT, Q_HAT, 3.2, MUTED, .12)
        orb = curve(view, F, 0, TAU, INK, width=4, R=1.0)
        sat = dot3(view, F(TH0), INK)
        peri = dot3(view, F(0.0), ROSE)

        # beat 1: the generic orbit with the globe
        with self.say("Your notes describe the orbit's orientation with a frame that rides on the orbit. "
                      "It's called the perifocal frame.") as d:
            head = self.section("The perifocal frame")
            self.play(FadeIn(earth), FadeIn(plane), run_time=.15 * d)
            orb.k.set_value(0)
            self.add(orb)
            self.play(orb.k.animate.set_value(1), FadeIn(sat), run_time=.35 * d)
            self.play(view.turn(18), run_time=.4 * d)

        # beat 2: p-hat, q-hat, h-hat grow from the center one at a time
        L = 1.9
        ap = arrow3(view, ORIGIN, L * P_HAT, ROSE)
        aq = arrow3(view, ORIGIN, L * Q_HAT, LIME)
        ah = arrow3(view, ORIGIN, L * H_HAT, LILAC)
        lp = label3(view, r"\hat p", (L + .35) * P_HAT, ROSE, 36)
        lq = label3(view, r"\hat q", (L + .35) * Q_HAT, LIME, 36)
        lh = label3(view, r"\hat h", (L + .35) * H_HAT, LILAC, 36)
        for a in (ap, aq, ah):
            a.k.set_value(0)
            a.set_z_index(3)
        for lab in (lp, lq, lh):
            lab.set_z_index(4)
        self.add(ap, aq, ah)
        with self.say("p hat points from the focus to the periapsis, the same direction as the eccentricity vector. "
                      "q hat is ninety degrees ahead of it, in the orbit plane, in the direction of motion. "
                      "And h hat sticks out of the plane, completing the set.") as d:
            self.play(FadeIn(peri, scale=2), run_time=.06 * d)
            self.play(ap.k.animate.set_value(1), run_time=.14 * d)
            self.play(FadeIn(lp), Flash(peri.get_center(), color=ROSE), run_time=.1 * d)
            self.play(aq.k.animate.set_value(1), run_time=.2 * d)
            self.play(FadeIn(lq), run_time=.1 * d)
            self.play(ah.k.animate.set_value(1), run_time=.2 * d)
            self.play(FadeIn(lh), run_time=.1 * d)

        # beat 3: the orbit plane drawn flat, with the satellite's components
        ell = ParametricFunction(flat, t_range=[0, TAU], color=INK, stroke_width=4)
        foc = Dot(FOC, color=INK2, radius=.06)
        px = Arrow(FOC + LEFT * 4.1, FOC + RIGHT * 1.85, buff=0, color=ROSE, stroke_width=4,
                   max_tip_length_to_length_ratio=.05)
        qy = Arrow(FOC + DOWN * 2.35, FOC + UP * 2.75, buff=0, color=LIME, stroke_width=4,
                   max_tip_length_to_length_ratio=.06)
        tp = M(r"\hat p", size=36, color=ROSE).next_to(px.get_end(), DOWN, buff=.15)
        tq = M(r"\hat q", size=36, color=LIME).next_to(qy.get_end(), LEFT, buff=.15)
        S = flat(TH0)
        foot = np.array([S[0], FOC[1], 0.0])
        rad = Line(FOC, S, color=INK, stroke_width=4)
        sdot = Dot(S, color=INK, radius=.08).set_z_index(5)
        xs = DashedLine(FOC, foot, color=ROSE, stroke_width=5)
        ys = DashedLine(foot, S, color=LIME, stroke_width=5)
        ang = Arc(radius=.38, start_angle=0, angle=TH0, arc_center=FOC, color=GOLD, stroke_width=5)
        tth = M(r"\theta", size=28, color=GOLD).move_to(FOC + .62 * np.array([np.cos(TH0 / 2), np.sin(TH0 / 2), 0]))
        lx = M(r"r\cos\theta", size=28).next_to(xs, DOWN, buff=.12)
        ly = M(r"r\sin\theta", size=28).next_to(ys, RIGHT, buff=.12)
        tint(lx, [((4, 5), GOLD)])
        tint(ly, [((4, 5), GOLD)])
        ly = backed(ly)
        eq = E(r"\vec r_P|=|\big(r\cos|\theta|,\ r\sin|\theta|,\ 0\big)", size=44).move_to([3.9, -2.55, 0])
        with self.say("In this frame the orbit is simple. The satellite sits at r cosine theta along p hat, "
                      "and r sine theta along q hat, with nothing out of the plane.") as d:
            self.play(Create(px), Create(qy), FadeIn(tp), FadeIn(tq), FadeIn(foc), run_time=.1 * d)
            self.play(Create(ell), run_time=.15 * d)
            self.play(Create(rad), FadeIn(sdot), Create(ang), FadeIn(tth), Indicate(sat, color=GOLD),
                      run_time=.17 * d)
            self.play(Create(xs), FadeIn(lx), run_time=.15 * d)
            self.play(Create(ys), FadeIn(ly), run_time=.15 * d)
            self.play(Write(eq[:5]), run_time=.13 * d)
            self.play(Write(eq[5:]), run_time=.06 * d)
            self.play(Circumscribe(eq[6], color=INK2), run_time=.06 * d)

        # beat 4: the three arrows pulse in the 3D view; question mark
        flatv = VGroup(ell, foc, px, qy, tp, tq, rad, sdot, xs, ys, ang, tth, lx, ly)
        ax = axes3(view, 2.8)
        ask = E(r"\hat p|,\;|\hat q|,\;|\hat h|\;\text{in ECI}", size=44)
        qm = M("?", size=110, color=ACCENT)
        qgrp = VGroup(ask, qm).arrange(DOWN, buff=.4).move_to([3.9, .5, 0])
        tips = [L * P_HAT, L * Q_HAT, L * H_HAT]
        cols = [ROSE, LIME, LILAC]
        with self.say("So all of the three dimensional information lives in one question: "
                      "how are p hat, q hat and h hat pointed in the E C I frame?") as d:
            self.play(FadeOut(flatv), eq.animate.set_opacity(.25), FadeIn(ax), run_time=.2 * d)
            self.play(LaggedStart(*[Flash(view.p(t), color=c, flash_radius=.35, line_length=.25)
                                    for t, c in zip(tips, cols)], lag_ratio=.4),
                      FadeIn(ask), run_time=.35 * d)
            self.play(FadeIn(qm, scale=1.6), FadeIn(glow(qm, ACCENT)), run_time=.25 * d)
            self.play(LaggedStart(*[Flash(view.p(t), color=c, flash_radius=.35, line_length=.25)
                                    for t, c in zip(tips, cols)], lag_ratio=.3), run_time=.2 * d)
        self.wipe()
