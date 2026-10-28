"""S52: stresses in the stepped bar (BRIEF.md S52)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the stepped aluminum bar (N, mm)
E_AL, A1, A2, L_EL, K_SP, P_LOAD = 70_000, 200, 100, 500, 14_000, 7000
k1, k2 = E_AL * A1 / L_EL, E_AL * A2 / L_EL
assert np.isclose(k1, 28_000) and np.isclose(k2, 14_000)
Kr = np.array([[k1 + k2, -k2], [-k2, k2 + K_SP]])
assert np.allclose(Kr, [[42000, -14000], [-14000, 28000]])
q1, q2 = np.linalg.solve(Kr, [P_LOAD, 0])
assert np.isclose(q1, 0.2) and np.isclose(q2, 0.1)
sig1 = E_AL * (q1 - 0) / L_EL
sig2 = E_AL * (q2 - q1) / L_EL
assert np.isclose(sig1, 28) and np.isclose(sig2, -14)

SIG = {r"\sigma_1": ACCENT, r"\sigma_2": ACCENT, r"\sigma": ACCENT,
       r"28\text{ N/mm}^2": ACCENT, r"28\text{ MPa}": ACCENT, r"-14\text{ MPa}": ACCENT}


class S52_Step_Stress(VScene):
    budget = 110

    def construct(self):
        # ---- the shared stepped-bar figure across the top band ----
        sb = stepped_bar()
        wl, el1, el2, spr, wr = sb
        xs = sb.x
        top1, top2 = el1.get_top()[1], el2.get_top()[1]
        qv = VGroup(M(r"q_0 = 0", size=40, color=SKY), M(r"q_1 = 0.2\text{ mm}", size=40, color=SKY),
                    M(r"q_2 = 0.1\text{ mm}", size=40, color=SKY), M(r"q_3 = 0", size=40, color=SKY))
        for m, x in zip(qv, xs):
            m.move_to([x, 0.3, 0])

        # ---- the general formula (below the figure) ----
        geq = E(r"\sigma|=|E\,\frac{q_b - q_a}{l}", size=56, cmap=SIG).move_to([0, -2.0, 0])
        for i in (1, 2, 4, 5):                  # q_b = glyphs 1-2, q_a = glyphs 4-5
            geq[2][i].set_color(SKY)
        p0, p1 = sb.p(0), sb.p(1)
        qa = M(r"q_a", size=40, color=SKY).move_to(p0 + RIGHT * 1.3)
        qb = M(r"q_b", size=40, color=SKY).move_to(p1 + LEFT * 1.3)
        qa_ar = Arrow(qa.get_left(), p0, buff=0.12, color=SKY, stroke_width=6)
        qb_ar = Arrow(qb.get_right(), p1, buff=0.12, color=SKY, stroke_width=6)
        qtags = VGroup(qa, qb, qa_ar, qb_ar).set_z_index(3)

        self.beat("Stress in each element is E times its strain: the displacement of its right node minus its left node, over its length. The same formula as the column.",
                  [FadeIn(sb), FadeIn(sb.nodes), FadeIn(sb.nums), FadeIn(sb.elabs), FadeIn(sb.klab),
                   FadeIn(sb.dims)],
                  [FadeIn(sb.load, shift=RIGHT * 0.2), FadeIn(sb.plab), FadeIn(qv)],
                  Write(geq),
                  [FadeIn(qtags), Indicate(VGroup(geq[2][1], geq[2][2], geq[2][4], geq[2][5]), color=SKY),
                   Indicate(sb.dims[0])],
                  .15, w=(.2, .15, .3, .2))

        # ---- element 1 (left half below the figure) ----
        a = E(r"\sigma_1|=|70{,}000\cdot\frac{0.2 - 0}{500}", size=48, cmap=SIG)
        b = E(r"=|28\text{ N/mm}^2|=|28\text{ MPa}", size=48, cmap=SIG)
        a.shift([-4.6 - a[1].get_center()[0], -1.45 - a.get_center()[1], 0])
        b.next_to(a, DOWN, buff=0.45)
        b.shift([a[1].get_center()[0] - b[0].get_center()[0], 0, 0])
        box1 = SurroundingRectangle(b[3], color=ACCENT, buff=0.1, stroke_width=4)
        c1, c2 = (xs[0] + xs[1]) / 2, (xs[1] + xs[2]) / 2
        yt = 3.2                                # tag row above the bars (dims fade out first)
        ten = T("tension", size=36, color=ACCENT).move_to([c1, yt, 0])

        self.beat("Thick piece: seventy thousand times zero point two minus zero, over five hundred. Twenty eight newtons per square millimeter. That unit is also called a megapascal, M P a. Positive, so tension.",
                  [FadeOut(qtags), geq.animate.move_to([3.6, -2.0, 0]), Write(a), Indicate(qv[1]),
                   Indicate(qv[0]), Indicate(sb.dims[0])], .05,
                  Write(VGroup(b[0], b[1])), [Write(VGroup(b[2], b[3])), Create(box1)],
                  [el1.animate.set_fill(ACCENT, opacity=0.6), FadeOut(sb.dims), FadeIn(ten)],
                  .1, w=(.3, .2, .2, .15))

        # ---- your turn: element 2 (right half) ----
        ask = E(r"\sigma_2|=|?", size=48, cmap=SIG)
        ask.shift([2.4 - ask[1].get_center()[0], -1.45 - ask.get_center()[1], 0])
        self.beat("Your turn: pause and do checkpoint seven point two in your guide, and find the stress in the thin piece.",
                  FadeOut(geq), FadeIn(ask), Circumscribe(el2, color=ACCENT),
                  .1, w=(.25, .25, .35))
        self.checkpoint("7.2", "Stepped bar: the stress in the thin piece")

        # ---- element 2 ----
        c = E(r"\sigma_2|=|70{,}000\cdot\frac{0.1 - 0.2}{500}", size=48, cmap=SIG)
        c.shift([2.4 - c[1].get_center()[0], -1.45 - c.get_center()[1], 0])
        d = E(r"=|-14\text{ MPa}", size=48, cmap=SIG).next_to(c, DOWN, buff=0.45)
        d.shift([c[1].get_center()[0] - d[0].get_center()[0], 0, 0])
        box2 = SurroundingRectangle(d[1], color=ACCENT, buff=0.1, stroke_width=4)
        comp = T("compression", size=36, color=ACCENT).move_to([c2 + 0.3, yt, 0])

        def arr(x0, x1):
            return Arrow([x0, yt, 0], [x1, yt, 0], buff=0, color=INK, stroke_width=8,
                         max_tip_length_to_length_ratio=0.3)
        tl, tr = ten.get_left()[0], ten.get_right()[0]
        cl, cr = comp.get_left()[0], comp.get_right()[0]
        pull = VGroup(arr(tl - 0.15, tl - 1.2), arr(tr + 0.15, tr + 1.2))       # outward: element 1 pulled
        push = VGroup(arr(cl - 1.15, cl - 0.15), arr(cr + 1.15, cr + 0.15))   # inward: element 2 pushed
        assert pull[1].get_right()[0] < push[0].get_left()[0] - 0.2

        self.beat("Thin piece: seventy thousand times zero point one minus zero point two, over five hundred. Minus fourteen megapascals: compression. The load pulls the thick piece and pushes the thin one.",
                  [FadeOut(ask), Write(c), Indicate(qv[2]), Indicate(qv[1])], .05,
                  [Write(d), Create(box2), el2.animate.set_fill(ACCENT, opacity=0.3), FadeIn(comp)],
                  Indicate(VGroup(sb.load, sb.plab), color=ROSE),
                  [GrowArrow(pull[0]), GrowArrow(pull[1])], [GrowArrow(push[0]), GrowArrow(push[1])],
                  .15, w=(.3, .2, .12, .14, .14))
        self.wipe()
