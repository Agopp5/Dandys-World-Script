"""S34: strain inside an element (BRIEF.md S34)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: u(s) = (1 - s) u1 + s u2 with s = (x - x1)/l  =>  du/dx = (u2 - u1)/l, the same at every x
_x1, _l, _u1, _u2 = 2.0, 3.0, 0.4, 1.1
_u = lambda x: (1 - (x - _x1) / _l) * _u1 + (x - _x1) / _l * _u2
for _x in (2.1, 3.0, 4.7):
    assert np.isclose((_u(_x + 1e-6) - _u(_x - 1e-6)) / 2e-6, (_u2 - _u1) / _l)
# element change in length: ((x2 + u2) - (x1 + u1)) - (x2 - x1) = u2 - u1
assert np.isclose(((_x1 + _l + _u2) - (_x1 + _u1)) - _l, _u2 - _u1)

U1, U2 = 0.45, 1.15          # drawn nodal displacements (illustrative, data units of the u axis)
X0 = -6.4                    # s = 0: node 1 of the element
YB = -1.45                   # element bar height
YD = -3.2                   # the stretched copy


def tex(s, size=36, color=INK):
    return M(s, size=size, color=color)


class S34_Strain(VScene):
    budget = 106

    def construct(self):
        # ---- left half: the u(s) line above, the element below, aligned (s = 0 at node 1, s = 1 at node 2)
        ax = Axes(x_range=[0, 1.15, 1], y_range=[0, 1.4, 1], x_length=5.6, y_length=3.0, tips=True,
                  axis_config={"color": AXIS, "include_numbers": False, "stroke_width": 3})
        ax.move_to([X0 + 2.8, 1.75, 0])
        ax.shift([X0 - ax.c2p(0, 0)[0], 0, 0])
        X1 = ax.c2p(1, 0)[0]
        s_lab = tex("s", 44, LIME).next_to(ax.x_axis.get_end(), DOWN, buff=.18)
        u_lab = tex("u", 44, SKY).next_to(ax.y_axis.get_end(), LEFT, buff=.18)
        t0 = tex("0", 40, INK2).next_to(ax.c2p(0, 0), DOWN, buff=.15)
        t1 = tex("1", 40, INK2).next_to(ax.c2p(1, 0), DOWN, buff=.15)
        tick1 = Line(ax.c2p(1, 0) + .1 * DOWN, ax.c2p(1, 0) + .1 * UP, color=AXIS, stroke_width=3)
        frame = VGroup(ax, s_lab, u_lab, t0, t1, tick1)

        line = Line(ax.c2p(0, U1), ax.c2p(1, U2), color=SKY, stroke_width=6)
        d1, d2 = Dot(ax.c2p(0, U1), color=SKY, radius=.09), Dot(ax.c2p(1, U2), color=SKY, radius=.09)
        l1 = tex("u_1", 40, SKY).next_to(d1, LEFT, buff=.15)
        l2 = tex("u_2", 40, SKY).next_to(d2, UL, buff=.12)
        uline = VGroup(line, d1, d2, l1, l2)

        bar0 = bar(X0, X1, y=YB)
        n1, n2 = node([X0, YB, 0]), node([X1, YB, 0])
        drop1 = DashedLine(ax.c2p(1, 0) + .45 * DOWN, [X1, YB + .3, 0], color=MUTED, stroke_width=2)
        elem = VGroup(bar0, n1, n2, drop1)

        # ---- right half: the chain rule
        eq1 = E(r"\frac{du}{dx}|=|\frac{du}{ds}|\qquad\cdot\qquad|\frac{ds}{dx}", size=56).move_to([4.0, 2.5, 0])

        self.beat("Strain is d u d x. Our u is written in s, so use the chain rule: d u d x equals d u d s, "
                  "times d s d x.",
                  [Create(frame), FadeIn(elem)], [Create(line), FadeIn(d1), FadeIn(d2), FadeIn(l1), FadeIn(l2)],
                  Write(eq1), w=(.25, .25, .5))

        # ---- beat 2: each factor below its spot; the slope triangle on the plot; the length l under the bar
        f1 = E(r"u_2|-|u_1", size=50)
        f1.move_to([eq1[2].get_center()[0], 0, 0])
        f2 = E(r"\frac{1}{l}", size=50)
        f2.move_to([eq1[4].get_center()[0], 0, 0])
        a1 = Arrow(eq1[2].get_bottom(), f1.get_top(), buff=.12, color=MUTED, stroke_width=4,
                   max_tip_length_to_length_ratio=.3)
        a2 = Arrow(eq1[4].get_bottom(), f2.get_top(), buff=.12, color=MUTED, stroke_width=4,
                   max_tip_length_to_length_ratio=.3)
        run = DashedLine(ax.c2p(0, U1), ax.c2p(1, U1), color=MUTED, stroke_width=3)
        rise = Line(ax.c2p(1, U1), ax.c2p(1, U2), color=SKY, stroke_width=5)
        run_l = tex("1", 40, INK2).next_to(run, DOWN, buff=.12)
        rise_l = tex(r"u_2 - u_1", 40, SKY).next_to(rise, RIGHT, buff=.15)
        span_l = VGroup(Line([X0, YB - .5, 0], [X1, YB - .5, 0], color=INK2, stroke_width=3),
                        Line([X0, YB - .38, 0], [X0, YB - .62, 0], color=INK2, stroke_width=3),
                        Line([X1, YB - .38, 0], [X1, YB - .62, 0], color=INK2, stroke_width=3))
        l_l = tex("l", 40, INK).next_to(span_l, DOWN, buff=.12)
        with self.say("d u d s is u two minus u one: the slope of our straight line in s. And d s d x is one over l.") as d:
            self.play(Indicate(eq1[2], color=SKY), Create(run), run_time=.12 * d)
            self.play(Create(rise), FadeIn(run_l), FadeIn(rise_l), run_time=.14 * d)
            self.play(GrowArrow(a1), FadeIn(f1, shift=DOWN * .2), run_time=.16 * d)
            self.wait(.1 * d)
            self.play(Indicate(eq1[4], color=LIME), Create(span_l), FadeIn(l_l), run_time=.16 * d)
            self.play(GrowArrow(a2), FadeIn(f2, shift=DOWN * .2), run_time=.16 * d)
            self.wait(.16 * d)

        # ---- beat 3: the strain, boxed; the element stretches by u2 - u1
        eq3 = E(r"\varepsilon|=|\frac{u_2 - u_1}{l}", size=56).move_to([4.0, -1.55, 0])
        tint(eq3[2], [((0, 2), SKY), ((3, 5), SKY)])
        box = SurroundingRectangle(eq3, color=ACCENT, buff=.22, corner_radius=.1, stroke_width=4)
        DX1, STR = .35, .55   # drawn: rigid shift u1, extra length u2 - u1
        bar_d = bar(X0, X1, y=YD)
        bar_s = bar(X0 + DX1, X1 + DX1 + STR, y=YD)
        ghost = DashedVMobject(Rectangle(width=X1 - X0, height=.42, color=MUTED, stroke_width=2)
                               .move_to([(X0 + X1) / 2, YD, 0]), num_dashes=40)
        ext = VGroup(Line([X1 + DX1, YD + .42, 0], [X1 + DX1 + STR, YD + .42, 0], color=SKY, stroke_width=4),
                     Line([X1 + DX1, YD + .3, 0], [X1 + DX1, YD + .54, 0], color=SKY, stroke_width=3),
                     Line([X1 + DX1 + STR, YD + .3, 0], [X1 + DX1 + STR, YD + .54, 0], color=SKY, stroke_width=3))
        ext_l = tex(r"u_2 - u_1", 40, SKY).next_to(ext, UP, buff=.1)
        with self.say("So the strain is u two minus u one, over l. The element's change in length, over its length. "
                      "Exactly what strain means.") as d:
            self.play(Write(eq3), run_time=.2 * d)
            self.play(Create(box), FadeIn(glow(eq3, ACCENT)), run_time=.12 * d)
            self.play(FadeIn(ghost), FadeIn(bar_d), run_time=.1 * d)
            self.play(bar_d.animate.shift(RIGHT * DX1), run_time=.12 * d)
            self.play(Transform(bar_d, bar_s), run_time=.16 * d)
            self.play(Create(ext), FadeIn(ext_l), Indicate(eq3[2], color=SKY), run_time=.14 * d)
            self.wait(.16 * d)

        # ---- beat 4: constant in s: a flat ACCENT line across the element; a probe slides along both
        YF = -.75
        flat = Line([X0, YF, 0], [X1, YF, 0], color=ACCENT, stroke_width=7)
        eps_l = tex(r"\varepsilon", 44, ACCENT).next_to(flat, UP, buff=.12)
        note = T("constant in each element", size=34, color=INK2).next_to(box, DOWN, buff=.4)
        tr = ValueTracker(0)
        probe_u = always_redraw(lambda: Dot(ax.c2p(tr.get_value(), U1 + tr.get_value() * (U2 - U1)),
                                            color=INK, radius=.1))
        probe_e = always_redraw(lambda: Dot([X0 + tr.get_value() * (X1 - X0), YF, 0], color=INK, radius=.1))
        with self.say("Notice it doesn't depend on s at all. Inside one element, the strain is constant. "
                      "Remember that; it will matter when we look at stresses.") as d:
            self.play(Circumscribe(eq3[2], color=ACCENT), FadeOut(run), FadeOut(run_l), run_time=.16 * d)
            self.play(Create(flat), FadeIn(eps_l), run_time=.14 * d)
            self.add(probe_u, probe_e)
            self.play(tr.animate.set_value(1), run_time=.26 * d, rate_func=there_and_back)
            self.remove(probe_u, probe_e)
            self.play(FadeIn(note, shift=UP * .2), run_time=.12 * d)
            self.wait(.32 * d)
        self.wipe()
