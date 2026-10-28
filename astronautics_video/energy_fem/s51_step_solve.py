"""S51: solving the stepped bar's 2 by 2 system (BRIEF.md S51)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the stepped aluminum bar, reduced system and its solution
E_AL, A1, A2, LEN, KS, PLOAD = 70000, 200, 100, 500, 14000, 7000
k1, k2 = E_AL * A1 / LEN, E_AL * A2 / LEN
assert k1 == 28000 and k2 == 14000
KR = np.array([[k1 + k2, -k2], [-k2, k2 + KS]])
assert np.allclose(KR, [[42000, -14000], [-14000, 28000]])
assert np.isclose(42000 * 28000 - 14000 ** 2, 9.8e8)
QSOL = np.linalg.solve(KR, [PLOAD, 0])
assert np.allclose(QSOL, [0.2, 0.1])
assert np.isclose(28000 / 14000, 2)                 # row 2: q1 = 2 q2
assert 42000 * 2 == 84000 and 84000 - 14000 == 70000
assert np.isclose(7000 / 70000, 0.1) and np.isclose(2 * 0.1, 0.2)

# figure: the shared S47-S53 stepped bar (efem.stepped_bar, default proportions)
SB = stepped_bar()
X0, X1, X2, X3 = SB.x
SPAN = X3 - X0
SC = 5.0            # screen units per mm: displacements exaggerated
QY = SB.qs.get_y()  # the q-arrow row under the node numbers


def figure(d1=0.0, d2=0.0):
    """The stepped bar with node 1 moved d1 and node 2 moved d2 (screen units)."""
    b = stepped_bar(f1=(X1 + d1 - X0) / SPAN, f2=((X2 + d2) - (X1 + d1)) / SPAN)
    assert np.isclose(b.x[1], X1 + d1) and np.isclose(b.x[2], X2 + d2)
    return VGroup(b, b.nodes, b.nums, b.klab, b.load, b.plab), b.elabs


def vec(rows, color):
    m = Matrix(rows, element_to_mobject_config={"font_size": 48}, h_buff=2.3)
    m.get_entries().set_color(color)
    return m


class S51_Step_Solve(VScene):
    budget = 109

    def construct(self):
        fig, elabs = figure()

        Km = vec([["42{,}000", "-14{,}000"], ["-14{,}000", "28{,}000"]], LILAC)
        qv = vec([["q_1"], ["q_2"]], SKY)
        rhs = vec([["7000"], ["0"]], ROSE)
        system = VGroup(Km, qv, M("=", size=48), rhs).arrange(RIGHT, buff=.25)
        system.move_to([0, -1.1, 0]).to_edge(LEFT, buff=.6)

        def rowbox(r):
            return VGroup(*[SurroundingRectangle(m.get_rows()[r], color=INK, buff=.1, stroke_width=3)
                            for m in (Km, qv, rhs)])

        box2 = rowbox(1)

        eqA = E(r"-14{,}000\,|q_1|+|28{,}000\,|q_2|=|0", size=48)
        paint(eqA, {0: LILAC, 3: LILAC, 6: ROSE})
        eqA.move_to([0, -2.7, 0])
        eqB = E(r"q_1|=|2\,|q_2", size=48).move_to([0, -3.55, 0])

        self.beat("Two equations. Start with the second one: minus fourteen thousand q one, plus twenty eight "
                  "thousand q two, equals zero. So q one is twice q two.",
                  [FadeIn(fig), FadeIn(system)], Create(box2), Write(eqA), .1, Write(eqB),
                  w=(.12, .1, .42, .26))

        # beat 2: substitute into row 1
        memo_pos = np.array([(system.get_right()[0] + 7.1) / 2, -1.1, 0])
        memo_box = SurroundingRectangle(eqB.copy().move_to(memo_pos), color=INK2, buff=.22)
        box1 = rowbox(0)
        eqC = E(r"42{,}000\,|(2|q_2|)|-|14{,}000\,|q_2|=|7000", size=48)
        paint(eqC, {0: LILAC, 1: INK, 3: INK, 5: LILAC, 8: ROSE})
        eqC.move_to([0, -2.7, 0])
        eqC2 = E(r"84{,}000\,|q_2|-|14{,}000\,|q_2|=|7000", size=48)
        paint(eqC2, {0: LILAC, 3: LILAC, 6: ROSE})
        eqC2.move_to([0, -2.7, 0])
        eqD = E(r"70{,}000\,|q_2|=|7000", size=48)
        paint(eqD, {0: LILAC, 3: ROSE})
        eqD.move_to([0, -3.55, 0])

        self.beat("Put that into the first: forty two thousand times two q two, minus fourteen thousand q two, "
                  "equals seven thousand. That's eighty four thousand minus fourteen thousand, seventy thousand "
                  "q two, equals seven thousand.",
                  [FadeOut(eqA), eqB.animate.move_to(memo_pos), Create(memo_box), ReplacementTransform(box2, box1)],
                  Write(eqC), Indicate(VGroup(eqC[1], eqC[2], eqC[3]), color=SKY),
                  morph(eqC, eqC2, [(2, 1), (4, 2), (5, 3), (6, 4), (7, 5), (8, 6)]),
                  Write(eqD),
                  w=(.1, .2, .12, .3, .28))

        # beat 3: the answers
        res2 = E(r"q_2|=|0.1\text{ mm}", size=56)
        res1 = E(r"q_1|=|0.2\text{ mm}", size=56)
        VGroup(res1, res2).arrange(RIGHT, buff=1.6).move_to([0, -2.6, 0])
        b2 = SurroundingRectangle(res2, color=INK, buff=.25)
        b1 = SurroundingRectangle(res1, color=INK, buff=.25)
        self.beat("So q two is zero point one millimeters, and q one, twice that, is zero point two millimeters.",
                  [FadeOut(system), FadeOut(box1), FadeOut(eqC2), FadeOut(memo_box)],
                  ReplacementTransform(eqD, res2), Create(b2), .1, ReplacementTransform(eqB, res1), Create(b1),
                  w=(.15, .25, .1, .25, .15))

        # beat 4: the bar deforms (exaggerated)
        d1, d2 = SC * QSOL[0], SC * QSOL[1]
        ghost = VGroup(*[DashedVMobject(e.copy().set_fill(opacity=0), num_dashes=40).set_stroke(MUTED, 2.5)
                         for e in (fig[0][1], fig[0][2])]).set_z_index(3)
        note = T("displacements exaggerated", size=30, color=MUTED).move_to([3.6, 3.72, 0])
        target, elabs_t = figure(d1, d2)
        a1 = Arrow([X1, QY, 0], [X1 + d1, QY, 0], buff=0, color=SKY, stroke_width=7,
                   max_tip_length_to_length_ratio=.3)
        a2 = Arrow([X2, QY, 0], [X2 + d2, QY, 0], buff=0, color=SKY, stroke_width=7,
                   max_tip_length_to_length_ratio=.5)
        l1 = M(r"0.2\text{ mm}", size=40, color=SKY).next_to(a1, RIGHT, buff=.15)
        l2 = M(r"0.1\text{ mm}", size=40, color=SKY).next_to(a2, RIGHT, buff=.15)
        self.beat("Picture it. The step moves two tenths of a millimeter to the right. The end moves only one tenth. "
                  "So the thin piece got shorter, and the spring got squeezed.",
                  [FadeIn(ghost), FadeIn(note), FadeIn(elabs)], [Transform(fig, target), Transform(elabs, elabs_t)],
                  [GrowArrow(a1), FadeIn(l1)], [GrowArrow(a2), FadeIn(l2)],
                  Indicate(fig[0][2], color=SKY, scale_factor=1.06), Indicate(fig[0][3], color=LILAC, scale_factor=1.1),
                  .1, w=(.06, .18, .18, .16, .16, .16))
        self.wipe()
