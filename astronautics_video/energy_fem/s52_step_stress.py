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
        # ---- the stepped bar (left half) ----
        yb = 0.5
        n0, n1, n2, n3 = -6.2, -4.2, -2.2, -0.4
        h1, h2 = 2.0, 1.0                      # element 1 twice as tall as element 2
        wl = wall(np.array([n0, yb, 0]), side=LEFT, h=3.0)
        wr = wall(np.array([n3, yb, 0]), side=RIGHT, h=3.0)
        el1 = bar(n0, n1, y=yb, h=h1)
        el2 = bar(n1, n2, y=yb, h=h2)
        spr = spring(np.array([n2, yb, 0]), np.array([n3, yb, 0]), color=LILAC, amp=0.3)
        xs = [n0, n1, n2, n3]
        dots = VGroup(*[node(np.array([x, yb, 0])) for x in xs]).set_z_index(3)
        nlab = VGroup(*[M(str(i), size=40, color=INK).move_to([x + (0.2 if i == 0 else -0.2 if i == 3 else 0), yb - h1 / 2 - 0.4, 0])
                        for i, x in enumerate(xs)])

        def tag(n, x):
            c = Circle(radius=0.32, color=INK2, stroke_width=3).set_fill(BG, 1)
            return VGroup(c, M(str(n), size=40, color=INK)).move_to([x, yb, 0]).set_z_index(2)
        etag = VGroup(tag(1, (n0 + n1) / 2), tag(2, (n1 + n2) / 2))

        pa = Arrow([n1, yb + 0.75, 0], [n1 + 1.15, yb + 0.75, 0], buff=0, color=ROSE, stroke_width=7,
                   max_tip_length_to_length_ratio=0.3)
        plab = M(r"P = 7000\text{ N}", size=40, color=ROSE).next_to(pa, RIGHT, buff=0.12).shift(UP * 0.12)
        qv = VGroup(M(r"q_0 = 0", size=40, color=SKY), M(r"q_1 = 0.2", size=40, color=SKY),
                    M(r"q_2 = 0.1", size=40, color=SKY), M(r"q_3 = 0", size=40, color=SKY))
        for m, x in zip(qv, xs):
            m.move_to([x, yb - h1 / 2 - 1.2, 0])
        note = T("displacements in mm", size=30, color=MUTED).move_to([(n0 + n3) / 2, -2.75, 0])

        # ---- the general formula (right half) ----
        geq = E(r"\sigma|=|E\,\frac{q_b - q_a}{l}", size=56, cmap=SIG).move_to([3.7, 2.55, 0])
        for i in (1, 2, 4, 5):                  # q_b = glyphs 1-2, q_a = glyphs 4-5
            geq[2][i].set_color(SKY)
        qa = M(r"q_a", size=40, color=SKY).move_to([n0 + 0.35, 2.75, 0])
        qb = M(r"q_b", size=40, color=SKY).move_to([n1, 2.75, 0])
        qa_ar = Arrow(qa.get_bottom(), [n0 + 0.05, yb + h1 / 2 + 0.02, 0], buff=0.08, color=SKY, stroke_width=5)
        qb_ar = Arrow(qb.get_bottom(), [n1, yb + h1 / 2 + 0.02, 0], buff=0.08, color=SKY, stroke_width=5)
        qtags = VGroup(qa, qb, qa_ar, qb_ar)

        self.beat("Stress in each element is E times its strain: the displacement of its right node minus its left node, over its length. The same formula as the column.",
                  [FadeIn(wl), FadeIn(wr), FadeIn(el1), FadeIn(el2), Create(spr), FadeIn(dots),
                   FadeIn(nlab), FadeIn(etag)],
                  [FadeIn(pa, shift=RIGHT * 0.2), FadeIn(plab), FadeIn(qv), FadeIn(note)],
                  Write(geq),
                  [FadeIn(qtags), Indicate(VGroup(geq[2][1], geq[2][2], geq[2][4], geq[2][5]), color=SKY)],
                  .15, w=(.2, .15, .3, .2))

        # ---- element 1 ----
        a = E(r"\sigma_1|=|70{,}000\cdot\frac{0.2 - 0}{500}", size=48, cmap=SIG)
        b = E(r"=|28\text{ N/mm}^2|=|28\text{ MPa}", size=48, cmap=SIG)
        a.shift([1.45 - a[1].get_center()[0], 0.95 - a.get_center()[1], 0])
        b.next_to(a, DOWN, buff=0.4)
        b.shift([a[1].get_center()[0] - b[0].get_center()[0], 0, 0])
        gl1 = glow(b[3], ACCENT)
        ten = T("tension", size=36, color=ACCENT).move_to([(n0 + n1) / 2 + 0.2, 2.5, 0])

        self.beat("Thick piece: seventy thousand times zero point two minus zero, over five hundred. Twenty eight newtons per square millimeter. That unit is also called a megapascal, M P a. Positive, so tension.",
                  [FadeOut(qtags), Write(a), Indicate(qv[1]), Indicate(qv[0])], .05,
                  Write(VGroup(b[0], b[1])), Write(VGroup(b[2], b[3])),
                  [el1.animate.set_fill(ACCENT, opacity=0.6), FadeIn(ten), FadeIn(gl1)],
                  .1, w=(.3, .2, .2, .15))

        # ---- your turn: element 2 ----
        s1 = VGroup(a, b)
        s1_target = s1.copy().shift(UP * (2.75 - a.get_center()[1]))
        ask = E(r"\sigma_2|=|?", size=48, cmap=SIG)
        ask.shift([a[1].get_center()[0] - ask[1].get_center()[0], -0.15 - ask.get_center()[1], 0])
        self.beat("Your turn: pause and do checkpoint seven point two in your guide, and find the stress in the thin piece.",
                  [FadeOut(geq), FadeOut(gl1), Transform(s1, s1_target)], FadeIn(ask), Circumscribe(el2, color=ACCENT),
                  .1, w=(.3, .2, .35))
        self.checkpoint("7.2", "Stepped bar: the stress in the thin piece")

        # ---- element 2 ----
        c = E(r"\sigma_2|=|70{,}000\cdot\frac{0.1 - 0.2}{500}", size=48, cmap=SIG)
        c.shift([a[1].get_center()[0] - c[1].get_center()[0], -0.15 - c.get_center()[1], 0])
        d = E(r"=|-14\text{ MPa}", size=48, cmap=SIG).next_to(c, DOWN, buff=0.4)
        d.shift([c[1].get_center()[0] - d[0].get_center()[0], 0, 0])
        comp = T("compression", size=36, color=ACCENT).move_to([(n1 + n2) / 2 + 0.6, 2.5, 0])

        def arr(x0, x1):
            return Arrow([x0, yb, 0], [x1, yb, 0], buff=0, color=INK, stroke_width=7,
                         max_tip_length_to_length_ratio=0.45).set_z_index(2)
        c1, c2 = (n0 + n1) / 2, (n1 + n2) / 2
        pull = VGroup(arr(c1 - 0.42, c1 - 0.95), arr(c1 + 0.42, c1 + 0.95))     # outward: pulled
        push = VGroup(arr(c2 - 0.95, c2 - 0.42), arr(c2 + 0.95, c2 + 0.42))     # inward: pushed

        self.beat("Thin piece: seventy thousand times zero point one minus zero point two, over five hundred. Minus fourteen megapascals: compression. The load pulls the thick piece and pushes the thin one.",
                  [FadeOut(ask), Write(c), Indicate(qv[2]), Indicate(qv[1])], .05,
                  [Write(d), el2.animate.set_fill(ACCENT, opacity=0.3), FadeIn(comp)],
                  Indicate(VGroup(pa, plab), color=ROSE),
                  [GrowArrow(pull[0]), GrowArrow(pull[1])], [GrowArrow(push[0]), GrowArrow(push[1])],
                  .15, w=(.3, .2, .12, .14, .14))
        self.wipe()
