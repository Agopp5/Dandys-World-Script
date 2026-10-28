"""S10: what the shear centre is (BRIEF.md S10)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# facts (channel of S09): four booms of 300 mm^2 at y = +-200, web 400 mm, flanges 200 mm, S_y = 4.8 kN
B, Y, H, W, SY = 300, 200, 400, 200, 4800
IXX = 4 * B * Y ** 2
assert IXX == 48e6 and np.isclose(SY / IXX, 1e-4)
q12 = -(SY / IXX) * B * Y
q23 = q12 - (SY / IXX) * B * Y
q34 = q23 - (SY / IXX) * B * (-Y)
assert np.isclose(q12, -6) and np.isclose(q23, -12) and np.isclose(q34, -6)
assert np.isclose(q34 - (SY / IXX) * B * (-Y), 0)          # free edge past boom 4
F_FL, F_WEB = 6 * W, 12 * H
assert F_FL == 1200 and F_WEB == 4800 == SY                  # web force = load (check)
COUPLE = F_FL * H
assert COUPLE == 480_000
E_SC = COUPLE / SY
assert np.isclose(E_SC, 100)                                 # mm from the web, away from the flanges

EQX = 0.45         # left edge of the algebra column


def dim(a, b, text, side, angle=0):
    """dimension line a-b with a size-34 label on `side`"""
    ln = DoubleArrow(a, b, buff=0, color=MUTED, stroke_width=3, tip_length=0.18,
                     max_tip_length_to_length_ratio=0.2)
    lab = T(text, size=34, color=INK2).rotate(angle).next_to(ln, side, buff=0.12)
    return VGroup(ln, lab)


def at_left(m, y):
    return m.move_to([EQX, y, 0], aligned_edge=LEFT)


class S10_Shear_Centre(VScene):
    budget = 148

    def construct(self):
        sec = channel(width=2.8, center=(-2.75, -0.1))
        walls = sec.draw()
        booms = sec.booms({1: B, 2: B, 3: B, 4: B})
        names = sec.names(size=34)
        k = (sec.p(1)[0] - sec.p(2)[0]) / W                      # scene units per mm
        xw = sec.p(2)[0]                                          # web line
        cy = (sec.p(2)[1] + sec.p(3)[1]) / 2                       # mid-height (neutral axis)
        sc = np.array([xw - E_SC * k, cy, 0])                      # shear centre, left of the web

        flows = VGroup(
            flow(sec, 1, 2, q12, label=r"-6", size=34),
            flow(sec, 2, 3, q23, label=r"-12", size=34),
            flow(sec, 3, 4, q34, label=r"-6", size=34),
        )
        unit = T("q in N/mm", size=30, color=SKY).next_to(sec.p(3), DL, buff=0.25)

        def load_at(x):
            a = Arrow([x, cy - 1.1, 0], [x, cy + 1.1, 0], buff=0, color=ROSE, stroke_width=9,
                      max_tip_length_to_length_ratio=0.18).set_z_index(5)
            lab = E(r"S_y", size=44).next_to(a.get_end(), LEFT, buff=0.15).set_z_index(5)
            return VGroup(a, lab)

        load = load_at(xw)
        body = VGroup(walls, booms, names, flows)

        twist_note = at_left(T("Load at the web: it twists", size=34, color=BAD), 2.4)
        twist_arc = torque(sc + 0.0 * UP, radius=0.55, ccw=True, label=None).set_color(BAD).move_to(
            sec.p(1) + 0.6 * RIGHT + 0.3 * DOWN)
        ok_note = at_left(VGroup(T("Load at the shear centre:", size=34, color=GOOD),
                                 T("no twist", size=34, color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15), 1.2)
        sc_dot = Dot(sc, radius=0.11, color=ROSE).set_z_index(6)
        sc_q = E(r"?", size=44, cmap={"?": ROSE}).next_to(sc_dot, DOWN, buff=0.2)

        # 1. the idea: twist vs no twist
        with self.say("We said the load acts through the shear centre. What is that? It's the one point where a shear load bends the section without twisting it.") as d:
            self.play(Create(walls), FadeIn(booms), FadeIn(names), run_time=.12 * d)
            self.play(LaggedStart(*[FadeIn(f) for f in flows], lag_ratio=.3), FadeIn(unit), run_time=.08 * d)
            self.play(GrowArrow(load[0]), FadeIn(load[1]), run_time=.08 * d)
            self.play(Rotate(VGroup(body, load), 9 * DEGREES, about_point=sc), FadeIn(twist_note),
                      FadeIn(twist_arc), run_time=.13 * d)
            self.snap("twisted")
            self.wait(.05 * d)
            self.play(Rotate(VGroup(body, load), -9 * DEGREES, about_point=sc), FadeOut(twist_arc),
                      run_time=.08 * d)
            new_load = load_at(sc[0])
            self.play(FadeIn(sc_dot), FadeIn(sc_q), Transform(load, new_load), run_time=.12 * d)
            self.play(VGroup(body, load, sc_dot, sc_q).animate.shift(.35 * UP), FadeIn(ok_note), run_time=.1 * d)
            self.play(VGroup(body, load, sc_dot, sc_q).animate.shift(.35 * DOWN), run_time=.08 * d)
            self.wait(.12 * d)
        self.play(FadeOut(twist_note), FadeOut(ok_note), FadeOut(load), FadeOut(sc_q), FadeOut(sc_dot))

        # 2. forces carried by the walls = shear flow x wall length
        top_y = sec.p(1)[1] + 0.32
        bot_y = sec.p(4)[1] - 0.32
        xm = (sec.p(1)[0] + xw) / 2
        f_top = Arrow([xm - 0.8, top_y, 0], [xm + 0.8, top_y, 0], buff=0, color=SKY, stroke_width=9)
        f_bot = Arrow([xm + 0.8, bot_y, 0], [xm - 0.8, bot_y, 0], buff=0, color=SKY, stroke_width=9)
        f_web = Arrow([xw + 0.45, cy - 1.2, 0], [xw + 0.45, cy + 1.2, 0], buff=0, color=SKY, stroke_width=9)
        l_top = T("1200 N", size=34, color=SKY).next_to(f_top, UP, buff=0.12)
        l_bot = T("1200 N", size=34, color=SKY).next_to(f_bot, DOWN, buff=0.12)
        l_web = T("4800 N", size=34, color=SKY).next_to(f_web, RIGHT, buff=0.15)

        ln_fl = at_left(E(r"F_{\rm flange}|=|6|\times|200|=|1200\ \rm N", size=44), 2.5)
        paint(ln_fl, {2: SKY, 6: SKY})
        note_f = at_left(T("force = shear flow × wall length", size=30, color=MUTED), 1.75)
        ln_web = at_left(E(r"F_{\rm web}|=|12|\times|400|=|4800\ \rm N", size=44), 0.85)
        paint(ln_web, {2: SKY, 6: SKY})

        self.beat("Look at the forces in the walls. Each flange carries six times two hundred: twelve hundred newtons. The web carries twelve times four hundred: forty eight hundred newtons.",
                  [Indicate(flows[0]), Indicate(flows[2])], [Write(ln_fl), FadeIn(note_f)],
                  [ReplacementTransform(flows[0], f_top), ReplacementTransform(flows[2], f_bot),
                   FadeIn(l_top), FadeIn(l_bot), FadeOut(unit)], .15,
                  Write(ln_web), [ReplacementTransform(flows[1], f_web), FadeIn(l_web)], .15,
                  w=(.08, .2, .12, .17, .1))

        # 3. web force = load; flange forces = couple
        ln_chk = at_left(E(r"4800\ \rm N|=|S_y|\ \checkmark", size=44), -0.2)
        paint(ln_chk, {3: GOOD})
        ln_cpl = at_left(E(r"1200|\times|400|=|480\,000\ \rm N\,mm", size=44), -1.35)
        note_c = at_left(VGroup(T("equal and opposite, 400 mm apart:", size=30, color=MUTED),
                                T("together they make a couple", size=30, color=MUTED)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12), -2.35)
        gap = dim(np.array([sec.p(1)[0] + 0.3, sec.p(1)[1], 0]), np.array([sec.p(1)[0] + 0.3, sec.p(4)[1], 0]),
                  "400 mm", RIGHT, angle=PI / 2)
        cpl_arc = torque(np.array([xm, cy, 0]), radius=0.6, ccw=False, label=None).set_color(SKY)

        self.beat("The web's force equals the load, good. But the two flange forces point opposite ways, so together they make a couple: twelve hundred times four hundred, which is four hundred eighty thousand newton millimeters.",
                  [Indicate(f_web), Indicate(l_web)], Write(ln_chk), .1,
                  [Indicate(f_top), Indicate(f_bot)], [FadeIn(gap), FadeIn(cpl_arc)],
                  [Write(ln_cpl), FadeIn(note_c)], .18,
                  w=(.08, .12, .1, .12, .2))

        # 4. load balances the couple -> e = 100 mm
        self.play(FadeOut(ln_fl), FadeOut(note_f), FadeOut(ln_web), FadeOut(ln_chk), FadeOut(note_c),
                  ln_cpl.animate.move_to([EQX, 2.5, 0], aligned_edge=LEFT))
        ln_bal = at_left(E(r"S_y|\,|e|=|480\,000", size=48), 1.35)
        paint(ln_bal, {2: ROSE})
        note_b = at_left(T("load's moment = the couple", size=30, color=MUTED), 0.6)
        ln_num = at_left(E(r"4800|\,|e|=|480\,000", size=48), -0.35)
        paint(ln_num, {2: ROSE})
        ln_e = at_left(E(r"e|=|\frac{480\,000}{4800}|=|100\ \rm mm", size=48), -1.75)
        paint(ln_e, {0: ROSE})
        box = SurroundingRectangle(ln_e, color=ROSE, buff=0.18)

        sc_dot = Dot(sc, radius=0.12, color=ROSE).set_z_index(6)
        e_span = dim(sc + 1.55 * DOWN, np.array([xw, sc[1] - 1.55, 0]), "e = 100 mm", DOWN)
        e_span[1].next_to(e_span[0], DOWN, buff=0.12).align_to(np.array([xw - 0.2, 0, 0]), RIGHT)
        e_dash = DashedLine(sc + 1.1 * DOWN, sc + 1.55 * DOWN, color=MUTED)
        load2 = load_at(sc[0])

        self.beat("For no twist, the load has to balance that couple. Forty eight hundred times e equals four hundred eighty thousand. So e is one hundred millimeters, outside the channel.",
                  [Write(ln_bal), FadeIn(note_b)], .08, Write(ln_num), .08,
                  [Write(ln_e), Create(box)], [FadeIn(sc_dot), FadeIn(glow(sc_dot, ROSE)), FadeIn(e_dash),
                                               FadeIn(e_span)], GrowArrow(load2[0]), FadeIn(load2[1]), .15,
                  w=(.17, .15, .16, .14, .08, .04))
        self.wait(1.0)

        # 5. take-away card
        self.play(FadeOut(ln_cpl), FadeOut(ln_bal), FadeOut(note_b), FadeOut(ln_num), FadeOut(gap),
                  VGroup(ln_e, box).animate.move_to([EQX, 2.4, 0], aligned_edge=LEFT))
        card = panel(VGroup(
            T("The shear centre need not lie", size=34),
            T("inside the material.", size=34),
            T("On a wing, lift that misses it", size=34),
            T("twists the wing.", size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22), color=ROSE)
        card.move_to([EQX, -0.9, 0], aligned_edge=LEFT)
        self.beat("Notice that the shear centre doesn't have to be inside the material. For a wing, we want to know where it is, because lift that misses it will twist the wing.",
                  Circumscribe(sc_dot, color=ROSE, shape=Circle), FadeIn(card, shift=UP * .2), .3,
                  w=(.2, .2))
        self.wipe()
