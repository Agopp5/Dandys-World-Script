"""S05: what a boom does to the shear flow (BRIEF.md S05)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})

# facts: the boom balance and the jump formula, checked with arbitrary numbers
_sig, _dsig, _B, _dz, _q1 = 37.0, 0.8, 300.0, 1e-3, 5.0
# (sigma + dsigma/dz dz) B - sigma B + q2 dz - q1 dz = 0  ->  q2 = q1 - dsigma/dz B
_q2 = (_q1 * _dz - (_sig + _dsig * _dz) * _B + _sig * _B) / _dz
assert np.isclose(_q2 - _q1, -_dsig * _B)
# sigma_z = M_x y / I_xx with dM_x/dz = S_y  ->  dsigma/dz = S_y y / I_xx (I_xy = 0, only S_y)
_Sy, _Ixx, _y = 4800.0, 48e6, 200.0
_M = lambda z: 1e6 + _Sy * z
_ds = (_M(1.0) * _y / _Ixx - _M(0.0) * _y / _Ixx) / 1.0
assert np.isclose(_ds, _Sy / _Ixx * _y)
# the channel's first jump (S06): -(S_y/I_xx) B y = -6 N/mm
assert np.isclose(-(_Sy / _Ixx) * _B * _y, -6.0)


def note(s):
    m = TX(s, size=30)
    m.set_color(MUTED)
    return m


class S05_Jump(VScene):
    budget = 104

    def construct(self):
        # ---------- the free body: boom (rod) of length dz, skin on both sides ----------
        L, H = 2.6, 0.6          # rod half-length, rod height
        FW, FH = 2.1, 2.55       # skin flap half-width, flap height
        rod = RoundedRectangle(width=2 * L, height=H, corner_radius=0.18,
                               fill_color=EMBER, fill_opacity=0.9, stroke_color=EMBER, stroke_width=3)
        br = E("B_r", size=44)
        br.set_color(BG).move_to(rod)
        top = Rectangle(width=2 * FW, height=FH, fill_color=SURFACE, fill_opacity=1,
                        stroke_color=INK2, stroke_width=3).next_to(rod, UP, buff=0)
        bot = Rectangle(width=2 * FW, height=FH, fill_color=SURFACE, fill_opacity=1,
                        stroke_color=INK2, stroke_width=3).next_to(rod, DOWN, buff=0)
        sk1 = T("skin", size=26, color=MUTED).move_to(top.get_corner(UL) + np.array([0.55, -0.32, 0]))
        sk2 = T("skin", size=26, color=MUTED).move_to(bot.get_corner(DL) + np.array([0.55, 0.32, 0]))
        dzspan = span(np.array([-L, -H / 2 - FH - 0.35, 0]), np.array([L, -H / 2 - FH - 0.35, 0]), "dz")
        body = VGroup(top, bot, rod, br)

        # ---------- forces along z ----------
        aL = Arrow(np.array([-L, 0, 0]), np.array([-L - 1.7, 0, 0]), buff=0, color=GOLD,
                   stroke_width=8, max_tip_length_to_length_ratio=0.25)
        aR = Arrow(np.array([L, 0, 0]), np.array([L + 1.7, 0, 0]), buff=0, color=GOLD,
                   stroke_width=8, max_tip_length_to_length_ratio=0.25)
        lL = E(r"\sigma_z|B_r", size=40).next_to(aL, UP, buff=0.25)
        lR = E(r"\Big(|\sigma_z|+|\frac{d\sigma_z}{dz}|\,dz|\Big)|B_r", size=40)
        paint(lR, {3: GOLD})
        lR.next_to(aR, UP, buff=0.25).align_to(np.array([FW + 0.15, 0, 0]), LEFT)
        a1 = Arrow(np.array([1.5, H / 2 + 0.3, 0]), np.array([-1.5, H / 2 + 0.3, 0]), buff=0, color=SKY,
                   stroke_width=7, max_tip_length_to_length_ratio=0.12)
        a2 = Arrow(np.array([-1.5, -H / 2 - 0.3, 0]), np.array([1.5, -H / 2 - 0.3, 0]), buff=0, color=SKY,
                   stroke_width=7, max_tip_length_to_length_ratio=0.12)
        l1 = E(r"q_1|\,dz", size=40).next_to(a1, UP, buff=0.25)
        l2 = E(r"q_2|\,dz", size=40).next_to(a2, DOWN, buff=0.25)
        zax = VGroup(Arrow(ORIGIN, RIGHT * 1.1, buff=0, color=AXIS, stroke_width=4),
                     M("z", size=32, color=MUTED))
        zax[1].next_to(zax[0], RIGHT, buff=0.1)
        zax.move_to(np.array([-5.6, -3.2, 0]))

        self.beat("Cut out one boom, with a short length d z, and the skin on either side.",
                  FadeIn(rod, scale=0.9), FadeIn(br), [FadeIn(top, shift=DOWN * 0.3), FadeIn(bot, shift=UP * 0.3),
                                                        FadeIn(sk1), FadeIn(sk2)],
                  [FadeIn(dzspan), FadeIn(zax)], w=(.25, .1, .3, .2))

        with self.say("Along the boom, the bending stress changes from sigma to sigma plus d sigma. "
                      "The skin pushes on it with shear flows q one and q two.") as d:
            self.play(GrowArrow(aL), FadeIn(lL), run_time=.18 * d)
            self.play(GrowArrow(aR), FadeIn(lR), run_time=.22 * d)
            self.play(Indicate(lR[3], color=GOLD), run_time=.12 * d)
            self.wait(.04 * d)
            self.play(GrowArrow(a1), FadeIn(l1), run_time=.18 * d)
            self.play(GrowArrow(a2), FadeIn(l2), run_time=.18 * d)
            self.wait(.08 * d)

        # ---------- force balance along z ----------
        pic = VGroup(body, aL, aR, a1, a2)
        bal = E(r"\Big(|\sigma_z|+|\frac{d\sigma_z}{dz}|\,dz|\Big)|B_r|-|\sigma_z|B_r|+|q_2|\,dz|-|q_1|\,dz|=0",
                size=42)
        paint(bal, {3: GOLD})
        bal.move_to(np.array([0, -0.75, 0]))
        sumz = note(r"forces along $z$ add to zero").next_to(bal, UP, buff=0.3)
        res = E(r"q_2|-|q_1|=|-|\frac{d\sigma_z}{dz}|\,B_r", size=48)
        paint(res, {5: GOLD})
        res.move_to(np.array([0, -2.55, 0]))
        why = note(r"$\sigma_z B_r$ cancels, then divide by $dz$").next_to(res, DOWN, buff=0.3)
        cuts = VGroup(strike(bal[1]), strike(VGroup(bal[8], bal[9])),
                      strike(bal[4]), strike(bal[12]), strike(bal[15]))

        with self.say("Force balance along the boom gives q two minus q one equals minus d sigma by d z, times B r.") as d:
            self.play(FadeOut(dzspan), FadeOut(zax), FadeOut(sk1), FadeOut(sk2), FadeOut(lL), FadeOut(lR), FadeOut(l1), FadeOut(l2),
                      pic.animate.scale(0.6).move_to(np.array([0, 2.25, 0])),
                      TransformFromCopy(lR, VGroup(*bal[0:7])),
                      TransformFromCopy(lL, VGroup(bal[8], bal[9])),
                      TransformFromCopy(l2, VGroup(bal[11], bal[12])),
                      TransformFromCopy(l1, VGroup(bal[14], bal[15])),
                      FadeIn(VGroup(bal[7], bal[10], bal[13], bal[16])), FadeIn(sumz),
                      run_time=.3 * d)
            self.play(LaggedStart(*[Create(c) for c in cuts[:2]], lag_ratio=.4), run_time=.15 * d)
            self.play(LaggedStart(*[Create(c) for c in cuts[2:]], lag_ratio=.3), run_time=.15 * d)
            self.play(Write(res), FadeIn(why), run_time=.3 * d)
            self.wait(.1 * d)

        # ---------- substitute d sigma / dz ----------
        tgt = res.copy().move_to(np.array([0, 2.7, 0]))
        sub = E(r"\frac{d\sigma_z}{dz}|=|\frac{S_y}{I_{xx}}|\,y", size=48)
        paint(sub, {0: GOLD})
        tint(sub[2], [((0, 2), ROSE)])
        sub.move_to(np.array([0, 0.9, 0]))
        subn = note(r"only $S_y$ and $I_{xy} = 0$: \ $\sigma_z = \dfrac{M_x}{I_{xx}}\,y$, \ $\dfrac{dM_x}{dz} = S_y$")
        subn.next_to(sub, DOWN, buff=0.3)
        fin = E(r"q_2|-|q_1|=|-|\frac{S_y}{I_{xx}}|\,B_r|\,y_r", size=56)
        tint(fin[5], [((0, 2), ROSE)])
        fin.move_to(np.array([0, -1.75, 0]))
        box = SurroundingRectangle(fin, color=ACCENT, buff=0.3, stroke_width=4)
        finn = note(r"at boom $r$, $y = y_r$").next_to(box, DOWN, buff=0.3)

        with self.say("With only a vertical load and I x y zero, d sigma by d z is S y over I x x, times y. "
                      "So the jump is minus S y over I x x, times B r y r.") as d:
            self.play(FadeOut(pic), FadeOut(bal), FadeOut(cuts), FadeOut(sumz), FadeOut(why),
                      Transform(res, tgt), run_time=.12 * d)
            self.play(Circumscribe(res[5], color=GOLD), run_time=.1 * d)
            self.play(Write(sub), FadeIn(subn), run_time=.2 * d)
            self.wait(.08 * d)
            self.play(TransformFromCopy(VGroup(*res[0:5]), VGroup(*fin[0:5])),
                      TransformFromCopy(sub[2], fin[5]),
                      TransformFromCopy(res[6], fin[6]),
                      TransformFromCopy(sub[3], fin[7]), run_time=.2 * d)
            self.play(Create(box), FadeIn(glow(fin, ACCENT)), FadeIn(finn), run_time=.14 * d)
            self.wait(.16 * d)
        self.wipe()
