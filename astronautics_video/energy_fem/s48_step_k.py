"""S48: three springs in disguise (BRIEF.md S48)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts (stepped aluminum bar, N and mm)
E_al, A1, A2, l_e, K_spring, P_load = 70_000, 200, 100, 500, 14_000, 7000
k1 = E_al * A1 / l_e
k2 = E_al * A2 / l_e
assert np.isclose(k1, 28_000)
assert np.isclose(k2, 14_000)
assert np.isclose(k2, k1 / 2)          # half the area, half the stiffness
assert np.isclose(K_spring, 14_000)
assert np.isclose(A2, A1 / 2)

# figure geometry: wall | thick elem 1 | step | thin elem 2 | spring | wall
XW0, XN1, XN2, XW3 = -6.0, -2.0, 2.0, 5.6
H1, H2 = 1.0, 0.5                      # element 1 twice as tall as element 2


def figure(y):
    p = lambda x, dy=0.0: np.array([x, y + dy, 0.0])
    g = VDict()
    g["w0"] = wall(p(XW0), side=LEFT, h=2.3)
    g["w3"] = wall(p(XW3), side=RIGHT, h=2.3)
    g["e1"] = bar(XW0, XN1, y=y, h=H1)
    g["e2"] = bar(XN1, XN2, y=y, h=H2)
    g["s3"] = spring(p(XN2), p(XW3), coils=6, amp=0.28)
    g["n"] = VGroup(*[node(p(x), r=0.1) for x in (XW0, XN1, XN2, XW3)])
    g["n"].set_z_index(3)
    lab = VGroup(*[M(str(i), size=40) for i in range(4)])
    lab[0].move_to(p(XW0 + 0.3, -0.95))
    lab[1].move_to(p(XN1, -0.95))
    lab[2].move_to(p(XN2, -0.95))
    lab[3].move_to(p(XW3 - 0.3, -0.95))
    g["nl"] = lab
    arr = Arrow(p(XN1, 0.42), p(XN1 + 1.5, 0.42), buff=0, color=ROSE, stroke_width=8,
                max_tip_length_to_length_ratio=0.3)
    plab = E(r"P|=|7000\text{ N}", size=36).next_to(arr, UP, buff=0.12).align_to(arr, LEFT).shift(LEFT * 0.3)
    g["P"] = VGroup(arr, plab).set_z_index(4)
    return g


def springs_for(y):
    p = lambda x: np.array([x, y, 0.0])
    s1 = spring(p(XW0), p(XN1), coils=6, amp=0.45).set_stroke(width=7)
    s2 = spring(p(XN1), p(XN2), coils=6, amp=0.26)
    return s1, s2


def klabel(tex, spr, y):
    return M(tex, size=40, color=LILAC).move_to([spr.get_center()[0], y - 0.95, 0])


class S48_Step_k(VScene):
    budget = 69

    def construct(self):
        Y = 1.75
        fig = figure(Y)
        s1, s2 = springs_for(Y)
        rule = E(r"k|=|\frac{EA}{l}", size=52)

        self.beat("Each piece of bar is an element, and each element is a spring with stiffness E A over l.",
                  FadeIn(fig), .1,
                  [ReplacementTransform(fig["e1"], s1), ReplacementTransform(fig["e2"], s2)],
                  Write(rule.move_to([0, -0.9, 0])), w=(.25, .4, .3))

        eq1 = E(r"k_1|=|\frac{70{,}000 \times 200}{500}|=|28{,}000\text{ N/mm}", size=48)
        eq2 = E(r"k_2|=|14{,}000\text{ N/mm}", size=48)
        note = T("half the area, half the stiffness", size=30, color=MUTED)
        eq1.move_to([0, -2.15, 0])
        eq2.next_to(eq1, DOWN, buff=0.4).align_to(eq1, LEFT)
        note.next_to(eq2, RIGHT, buff=0.6)
        L1 = klabel(r"28{,}000", s1, Y)
        L2 = klabel(r"14{,}000", s2, Y)
        L3 = klabel(r"14{,}000", fig["s3"], Y)
        self.beat("Thick piece: seventy thousand times two hundred, over five hundred: twenty eight thousand "
                  "newtons per millimeter. Thin piece: half the area, so half the stiffness, fourteen thousand.",
                  Write(eq1), TransformFromCopy(eq1[4], L1), .05,
                  [Write(eq2), FadeIn(note)], TransformFromCopy(eq2[2], L2),
                  w=(.32, .13, .3, .2))

        chain = VGroup(fig["w0"], s1, L1, fig["n"][1], s2, L2, fig["n"][2], fig["s3"], L3, fig["w3"])
        with self.say("And the real spring is already a spring, fourteen thousand. "
                      "So the whole thing is three springs in a row, between two walls.") as d:
            self.play(Indicate(fig["s3"], color=LILAC, scale_factor=1.12), Write(L3), run_time=.3 * d)
            self.play(FadeOut(VGroup(rule, eq1, eq2, note)), run_time=.12 * d)
            self.play(VGroup(fig, s1, s2, L1, L2, L3).animate.shift(DOWN * 1.9), run_time=.13 * d)
            self.play(LaggedStart(*[Indicate(m, color=m.get_color(), scale_factor=1.15) for m in chain],
                                  lag_ratio=.35), run_time=.35 * d)
            self.wait(.1 * d)
        self.wipe()
