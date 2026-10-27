"""S29: the course slides' beam example (BRIEF.md S29)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})
VC = {"v": SKY, "v_B": SKY, "v''": SKY}   # the sag v is a displacement: SKY

# facts: the sine shape, its energy, the stationary point, and the comparison with beam theory
EI_, L_, P_, vB_ = 3.0, 2.0, 5.0, 0.7
zz = np.linspace(0, L_, 20001)
vpp = -vB_ * (np.pi / L_) ** 2 * np.sin(np.pi * zz / L_)          # v'' of v = vB sin(pi z / L)
M_ = -EI_ * vpp
U_num = np.trapz(M_ ** 2 / (2 * EI_), zz)
assert np.isclose(U_num, np.pi ** 4 * EI_ * vB_ ** 2 / (4 * L_ ** 3), rtol=1e-6)
assert np.isclose(np.trapz(np.sin(np.pi * zz / L_) ** 2, zz), L_ / 2, rtol=1e-6)
vB_star = 2 * P_ * L_ ** 3 / (np.pi ** 4 * EI_)                     # d Pi / d vB = 0
dPi = lambda v: np.pi ** 4 * EI_ * v / (2 * L_ ** 3) - P_
assert np.isclose(dPi(vB_star), 0)
assert np.isclose(round(2 / np.pi ** 4, 5), 0.02053)
assert np.isclose(round(1 / 48, 5), 0.02083)
low = 1 - (2 / np.pi ** 4) / (1 / 48)
assert np.isclose(round(100 * low, 2), 1.45)

# figure geometry (left half)
X0, X1, YB = -6.2, -1.0, 1.3       # beam ends and centerline
XM = (X0 + X1) / 2
AMP = 1.5                          # drawn sag at the middle
YZ = -1.25                         # z axis height


def sag_y(x):
    return YB - AMP * np.sin(np.pi * (x - X0) / (X1 - X0))


def pin(x):
    tri = Triangle(color=INK2, stroke_width=4).scale(0.32)
    tri.move_to([x, YB - 0.15 - tri.height / 2, 0])
    gnd = Line([x - 0.45, tri.get_bottom()[1], 0], [x + 0.45, tri.get_bottom()[1], 0], color=INK2, stroke_width=4)
    return VGroup(tri, gnd)


def roller(x):
    tri = Triangle(color=INK2, stroke_width=4).scale(0.32)
    tri.move_to([x, YB - 0.15 - tri.height / 2, 0])
    yb = tri.get_bottom()[1]
    wheels = VGroup(*[Circle(radius=0.08, color=INK2, stroke_width=3).move_to([x + dx, yb - 0.09, 0])
                      for dx in (-0.18, 0.18)])
    gnd = Line([x - 0.45, yb - 0.18, 0], [x + 0.45, yb - 0.18, 0], color=INK2, stroke_width=4)
    return VGroup(tri, wheels, gnd)


class S29_Beam(VScene):
    budget = 277

    def construct(self):
        # ---- beat 1: the beam, its supports, the load P -------------------------------------------
        beam = bar(X0, X1, y=YB, h=0.3)
        sup = VGroup(pin(X0), roller(X1))
        ei = M(r"EI", size=40, color=INK2).next_to(beam, UP, buff=0.2).align_to(beam, LEFT).shift(RIGHT * 0.3)
        p_arr = force([XM, YB + 1.75, 0], d=DOWN, length=1.6)
        p_lab = M(r"P", size=48, color=ROSE).next_to(p_arr, LEFT, buff=0.2).shift(UP * 0.3)
        note_w = TX(r"slides: $W$", size=30).set_color(MUTED).next_to(p_arr, RIGHT, buff=0.3).shift(UP * 0.3)
        span_l = span(np.array([X0, YZ, 0]), np.array([X1, YZ, 0]), "L")
        self.beat("The course slides use the same trick on a beam, so let's see it once. A beam of length L, "
                  "stiffness E I, supported at both ends, with a point load at the middle. The slides call that "
                  "load W; we'll call it P, so it doesn't clash with work potential.",
                  [FadeIn(beam), FadeIn(sup)], FadeIn(span_l), FadeIn(ei), .1, GrowArrow(p_arr), FadeIn(p_lab),
                  .1, FadeIn(note_w), w=(.2, .15, .1, .05, .15, .1, .05, .2))

        # ---- beat 2: z along the beam, v down, point B -------------------------------------------
        z_ax = Arrow([X0 - 0.1, YZ, 0], [X1 + 0.6, YZ, 0], buff=0, color=AXIS, stroke_width=4)
        z_lab = M(r"z", size=40).next_to(z_ax, RIGHT, buff=0.12)
        ticks = VGroup(*[Line([x, YZ - 0.12, 0], [x, YZ + 0.12, 0], color=AXIS, stroke_width=4) for x in (X0, X1)])
        tick_l = VGroup(M(r"0", size=36).next_to(ticks[0], DOWN, buff=0.12),
                        M(r"L", size=36).next_to(ticks[1], DOWN, buff=0.12))
        xq = X0 + 0.25 * (X1 - X0)
        v_arr = Arrow([xq, YB, 0], [xq, sag_y(xq), 0], buff=0, color=SKY, stroke_width=6,
                      max_tip_length_to_length_ratio=0.3)
        v_lab = M(r"v", size=44, color=SKY).next_to(v_arr, LEFT, buff=0.15)
        b_dot = node([XM, YB, 0], color=INK)
        b_lab = M(r"B", size=40).next_to(b_dot, UR, buff=0.12).shift(RIGHT * 0.15)
        vb_arr = Arrow([XM, YB, 0], [XM, sag_y(XM), 0], buff=0, color=SKY, stroke_width=6,
                       max_tip_length_to_length_ratio=0.2)
        vb_lab = M(r"v_B", size=44, color=SKY).next_to(vb_arr, RIGHT, buff=0.15)
        vdef = TX(r"$v(z)$: the sag, positive downward", size=36).move_to([3.6, 2.6, 0])
        self.beat("Measure z along the beam, and let v be how far it sags, positive downward, the way the load "
                  "points. Call the middle point B, and its sag v B.",
                  [FadeOut(span_l), Create(z_ax), FadeIn(ticks), FadeIn(tick_l), FadeIn(z_lab)],
                  [GrowArrow(v_arr), FadeIn(v_lab), FadeIn(vdef)], [FadeIn(b_dot), FadeIn(b_lab)],
                  [GrowArrow(vb_arr), FadeIn(vb_lab)], w=(.3, .35, .15, .2))

        # ---- beat 3: the sine hump ---------------------------------------------------------------
        hump = FunctionGraph(sag_y, x_range=[X0, X1], color=SKY, stroke_width=6)
        shape = E(r"v|=|v_B|\sin\frac{\pi z}{L}", size=56, cmap=VC).move_to([3.6, 1.2, 0])
        zeros = VGroup(*[Dot([x, YB, 0], color=SKY, radius=0.1) for x in (X0, X1)])
        zl = VGroup(M(r"v=0", size=36, color=SKY).move_to([X0 + 0.35, YB - 1.05, 0]),
                    M(r"v=0", size=36, color=SKY).move_to([X1 - 0.35, YB - 1.05, 0]))
        n1 = TX(r"zero at $z=0$ and $z=L$", size=32).move_to([3.6, -0.3, 0])
        n2 = TX(r"peak $v_B$ at $z=L/2$", size=32).move_to([3.6, -1.1, 0])
        self.beat("Assume the sag is a sine hump: v equals v B times sine of pi z over L. It's zero at both "
                  "supports, and peaks at v B in the middle. It respects the supports.",
                  [Write(shape), Create(hump)], .05, [FadeIn(zeros), FadeIn(zl), FadeIn(n1)],
                  [Indicate(vb_lab, color=SKY), FadeIn(n2)], .05, Indicate(sup, color=GOOD),
                  w=(.35, .05, .2, .2, .05, .15))

        # ---- beat 4: strain energy of bending ----------------------------------------------------
        RX = 3.6
        u_int = E(r"U|=|\int_0^L \frac{M^2}{2EI}\,dz", size=52).move_to([RX, 2.3, 0])
        m_def = E(r"M|=|-EI|\,v''", size=48, cmap=VC).move_to([RX, 0.6, 0])
        n_pat = TX(r"$=\tfrac12\,EI\,(\text{curvature})^2$, integrated", size=32).move_to([RX, -0.7, 0])
        self.beat("For a beam, the deformation is the bending, the curvature, and the strain energy is the "
                  "integral of M squared over two E I, with M equal to minus E I times v double prime. Same "
                  "pattern: one half, stiffness, times deformation squared.",
                  [FadeOut(vdef), FadeOut(shape), FadeOut(n1), FadeOut(n2)], Write(u_int), .05, Write(m_def), .05,
                  FadeIn(n_pat), Indicate(u_int[2], color=MINT), w=(.1, .25, .05, .25, .05, .15, .15))

        # ---- beat 5: put the sine in -------------------------------------------------------------
        vpp_eq = E(r"v''|=|-v_B\frac{\pi^2}{L^2}\sin\frac{\pi z}{L}", size=48, cmap=VC).move_to([RX, 0.6, 0])
        n_sin = TX(r"using $\int_0^L \sin^2\frac{\pi z}{L}\,dz = \frac{L}{2}$", size=32).move_to([RX, -0.75, 0])
        u_res = E(r"U|=|\frac{\pi^4 EI\,v_B^2}{4L^3}", size=56).move_to([RX, -2.2, 0])
        u_glow = glow(u_res, MINT)
        self.beat("Put the sine in. Its second derivative is minus v B, pi over L squared, times the sine. Square "
                  "it and integrate, and U comes out to pi to the fourth, E I, v B squared, over four L cubed.",
                  [FadeOut(n_pat), FadeOut(m_def)], Write(vpp_eq), .05, FadeIn(n_sin), Write(u_res),
                  FadeIn(u_glow), w=(.08, .32, .05, .2, .25, .1))

        # ---- beat 6: Pi and its stationary point -------------------------------------------------
        pi_eq = E(r"\Pi|=|\frac{\pi^4 EI\,v_B^2}{4L^3}|-|P|\,v_B", size=52, cmap=VC).move_to([RX, 2.3, 0])
        dpi = E(r"\frac{d\Pi}{dv_B}|=|\frac{\pi^4 EI\,v_B}{2L^3}|-|P|=|0", size=48, cmap=VC).move_to([RX, 0.5, 0])
        res = E(r"v_B|=|\frac{2PL^3}{\pi^4 EI}|\approx|0.02053\,\frac{PL^3}{EI}", size=48, cmap=VC)
        res.move_to([RX, -1.6, 0])
        res_box = SurroundingRectangle(res, color=SKY, buff=0.2, stroke_width=4)
        with self.say("Pi is that, minus P times v B. Set its derivative with respect to v B to zero: v B equals "
                      "two P L cubed over pi to the fourth E I. That's zero point zero two zero five three, P L "
                      "cubed over E I.") as d:
            self.play(FadeOut(u_int), FadeOut(vpp_eq), FadeOut(n_sin), FadeOut(u_glow), run_time=.08 * d)
            self.play(*morph(u_res, pi_eq, [(1, 1), (2, 2)]), run_time=.2 * d)
            self.play(Write(dpi), run_time=.22 * d)
            self.play(Write(res[:3]), run_time=.2 * d)
            self.play(Write(res[3:]), run_time=.15 * d)
            self.play(Create(res_box), run_time=.1 * d)
            self.wait(.05 * d)

        # ---- beat 7: compare with beam theory ----------------------------------------------------
        exact = E(r"\frac{PL^3}{48EI}|\approx|0.02083\,\frac{PL^3}{EI}", size=48).move_to([RX, -0.3, 0])
        ex_tag = T("beam theory, exact", size=30, color=MUTED).next_to(exact, UP, buff=0.25)
        gs_tag = T("sine guess", size=30, color=MUTED)
        BW = 4.6                                   # exact bar length; the guess is 98.55 percent of it
        b_lbl = VGroup(T("guess", size=32, color=SKY), T("exact", size=32, color=INK2))
        bx = RX - 2.2
        g_bar = Rectangle(width=BW * (1 - low), height=0.55, color=SKY, fill_color=SKY, fill_opacity=.6)
        e_bar = Rectangle(width=BW, height=0.55, color=INK2, fill_color=INK2, fill_opacity=.35)
        g_bar.move_to([bx, -1.65, 0], aligned_edge=LEFT)
        e_bar.move_to([bx, -2.4, 0], aligned_edge=LEFT)
        b_lbl[0].next_to(g_bar, LEFT, buff=0.25)
        b_lbl[1].next_to(e_bar, LEFT, buff=0.25)
        n_low = T("1.45 percent low", size=34, color=INK).next_to(e_bar, DOWN, buff=0.3)
        self.beat("Beam theory's exact answer is P L cubed over forty eight E I, which is zero point zero two "
                  "zero eight three. A one-line guess, within about one and a half percent.",
                  [FadeOut(pi_eq), FadeOut(dpi), VGroup(res, res_box).animate.move_to([RX, 2.4, 0])],
                  [FadeIn(gs_tag.next_to(res_box, DOWN, buff=0.15)), FadeIn(ex_tag), Write(exact)], .05,
                  [GrowFromEdge(g_bar, LEFT), GrowFromEdge(e_bar, LEFT), FadeIn(b_lbl)], FadeIn(n_low), .1,
                  w=(.15, .35, .05, .2, .15, .1))
        self.wipe()
