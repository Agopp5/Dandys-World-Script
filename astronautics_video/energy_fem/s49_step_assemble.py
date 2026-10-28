"""S49: assembling the stepped bar's four by four stiffness matrix (BRIEF.md S49)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: stepped aluminum bar (N, mm)
E_al, A1, A2, l = 70000, 200, 100, 500
k1, k2, ks = E_al * A1 / l, E_al * A2 / l, 14000
assert k1 == 28000 and k2 == 14000 and ks == 14000
Kg = np.zeros((4, 4))
for (i, j), k in zip([(0, 1), (1, 2), (2, 3)], [k1, k2, ks]):
    Kg[np.ix_([i, j], [i, j])] += k * np.array([[1, -1], [-1, 1]])
assert np.allclose(Kg, [[28000, -28000, 0, 0], [-28000, 42000, -14000, 0],
                        [0, -14000, 28000, -14000], [0, 0, -14000, 14000]])
assert k1 + k2 == 42000 and k2 + ks == 28000
assert np.allclose(Kg.sum(axis=1), 0)          # rows sum to zero before supports
P = 7000

# layout
YB = 2.45                                      # bar axis
XN = [-6.0, -2.0, 2.0, 6.0]                    # nodes 0..3
CW, CH = 1.9, 0.85                             # grid cell
GX, GTOP = -2.4, 0.4                           # grid centre x, grid top y
VX, VW = 2.6, 1.4                              # load-vector column


def cell_c(i, j):
    return np.array([GX + (j - 1.5) * CW, GTOP - (i + .5) * CH, 0])


def fmt(v):
    s = "{:,}".format(int(abs(v))).replace(",", r"\,")
    return ("-" if v < 0 else "") + s


def entry(i, j, v, color=LILAC):
    return M(fmt(v), size=40, color=color).move_to(cell_c(i, j))


def block(i, j, k, skip=()):
    """2x2 element block for nodes i, j: tinted card plus its four entries (minus skipped spots)."""
    c = (cell_c(i, i) + cell_c(j, j)) / 2
    card = Rectangle(width=2 * CW - .12, height=2 * CH - .12).set_stroke(LILAC, 3).set_fill(LILAC, .12).move_to(c)
    ents = VGroup(*[entry(a, b, k if a == b else -k) for a in (i, j) for b in (i, j) if (a, b) not in skip])
    return VGroup(card, ents)


def sum_card(a, b, c, spot):
    tag = M(spot, size=40, color=INK2)
    top = M(a, size=48, color=LILAC)
    mid = M(r"+\;" + b, size=48, color=LILAC)
    rows = VGroup(top, mid).arrange(DOWN, aligned_edge=RIGHT, buff=.3)
    line = Line(LEFT, RIGHT, color=INK2, stroke_width=3).set_width(rows.width + .2)
    line.next_to(rows, DOWN, buff=.2).align_to(rows, RIGHT)
    bot = M(c, size=48, color=LILAC).next_to(line, DOWN, buff=.25).align_to(rows, RIGHT)
    tag.next_to(VGroup(rows, line), UP, buff=.35)
    g = VGroup(tag, top, mid, line, bot).move_to([5.5, -1.3, 0])
    return g


class S49_Step_Assemble(VScene):
    budget = 128

    def construct(self):
        # ---- the stepped bar (top half) ----
        wl = wall([XN[0], YB, 0], side=LEFT, h=1.8)
        wr = wall([XN[3], YB, 0], side=RIGHT, h=1.8)
        e1 = bar(XN[0], XN[1], y=YB, h=0.9)
        e2 = bar(XN[1], XN[2], y=YB, h=0.45)
        sp = spring([XN[2], YB, 0], [XN[3], YB, 0], coils=6, amp=0.22, color=LILAC)
        dots = VGroup(*[node([x, YB, 0]) for x in XN]).set_z_index(3)
        nlab = VGroup(*[M(str(n), size=40, color=INK).move_to([x, YB - .85, 0]) for n, x in enumerate(XN)])
        klab = VGroup(M(r"k_1 = 28\,000", size=36, color=LILAC).move_to([(XN[0] + XN[1]) / 2, YB - .85, 0]),
                      M(r"k_2 = 14\,000", size=36, color=LILAC).move_to([(XN[1] + XN[2]) / 2, YB - .85, 0]),
                      M(r"k_3 = 14\,000", size=36, color=LILAC).move_to([(XN[2] + XN[3]) / 2, YB - .85, 0]))
        arr = Arrow([XN[1] + .02, YB + .33, 0], [XN[1] + 1.5, YB + .33, 0], buff=0, color=ROSE,
                    stroke_width=8, max_tip_length_to_length_ratio=.3)
        plab = M(r"P = 7000\ \mathrm{N}", size=40, color=ROSE).next_to(arr, UP, buff=.15)
        fig = VGroup(wl, wr, e1, e2, sp, dots, nlab, klab, arr, plab)

        # ---- the empty 4x4 grid ----
        cells = VGroup(*[Rectangle(width=CW, height=CH).set_stroke(HAIR, 2).move_to(cell_c(i, j))
                         for i in range(4) for j in range(4)])
        rlab = VGroup(*[M(str(i), size=40, color=INK2).move_to([GX - 2 * CW - .4, cell_c(i, 0)[1], 0])
                        for i in range(4)])
        clab = VGroup(*[M(str(j), size=40, color=INK2).move_to([cell_c(0, j)[0], GTOP + .38, 0])
                        for j in range(4)])
        kname = M("K", size=48, color=LILAC).move_to([rlab[0].get_x(), clab[0].get_y(), 0])
        note = T("stiffness in N/mm", size=30, color=MUTED).move_to([GX, GTOP - 4 * CH - .45, 0])
        grid = VGroup(cells, rlab, clab, kname)

        self.beat("Four nodes, so a four by four matrix. Each of the three springs drops in its two by two block.",
                  FadeIn(fig), [Create(cells), FadeIn(rlab), FadeIn(clab), FadeIn(kname), FadeIn(note)],
                  [Indicate(e1, color=LILAC), Indicate(e2, color=LILAC), Indicate(sp, color=LILAC)],
                  w=(.25, .35, .4))

        self.beat("Your turn first: pause and do checkpoint seven point one in your guide, and assemble it yourself.",
                  Circumscribe(cells, color=ACCENT), .5)
        self.checkpoint("7.1", "Stepped bar: assemble the 4 by 4 stiffness matrix")

        # ---- element 1: nodes 0, 1 ----
        b1 = block(0, 1, 28000)
        self.beat("Element one, nodes zero and one: twenty eight thousand on the diagonal at zero and one, "
                  "minus twenty eight thousand between them.",
                  [e1.animate.set_stroke(LILAC, 6), Indicate(VGroup(nlab[0], nlab[1]), color=LILAC)],
                  FadeIn(b1, shift=DOWN * .8),
                  [Indicate(b1[1][0], color=LILAC), Indicate(b1[1][3], color=LILAC)],
                  [Indicate(b1[1][1], color=LILAC), Indicate(b1[1][2], color=LILAC)],
                  w=(.15, .25, .3, .3))
        old11 = b1[1][3]

        # ---- element 2: nodes 1, 2 ----
        b2 = block(1, 2, 14000, skip=[(1, 1)])
        sc1 = sum_card(r"28\,000", r"14\,000", r"42\,000", r"\text{spot } (1,1)")
        new11 = entry(1, 1, 42000)
        self.beat("Element two, nodes one and two: fourteen thousand. At spot one-one it adds to the twenty "
                  "eight thousand already there, making forty two thousand.",
                  [e1.animate.set_stroke(INK2, 2), e2.animate.set_stroke(LILAC, 6), FadeIn(b2, shift=DOWN * .8)],
                  [Indicate(old11, color=GOLD), FadeIn(sc1[0]), TransformFromCopy(old11, sc1[1]),
                   FadeIn(sc1[2], shift=LEFT * .5)],
                  [Create(sc1[3]), Write(sc1[4])],
                  [FadeOut(old11), TransformFromCopy(sc1[4], new11)],
                  .15, w=(.25, .25, .15, .2))
        old22 = b2[1][2]          # entries of b2: (1,2), (2,1), (2,2)

        # ---- the spring: nodes 2, 3 ----
        b3 = block(2, 3, 14000, skip=[(2, 2)])
        sc2 = sum_card(r"14\,000", r"14\,000", r"28\,000", r"\text{spot } (2,2)")
        new22 = entry(2, 2, 28000)
        zeros = VGroup(*[entry(i, j, 0, color=MUTED) for i, j in
                         [(0, 2), (0, 3), (1, 3), (2, 0), (3, 0), (3, 1)]])
        self.beat("The spring, nodes two and three: fourteen thousand again. At spot two-two, fourteen plus "
                  "fourteen, twenty eight thousand.",
                  [FadeOut(sc1), e2.animate.set_stroke(INK2, 2), Indicate(sp, color=LILAC),
                   FadeIn(b3, shift=DOWN * .8)],
                  [Indicate(old22, color=GOLD), FadeIn(sc2[0]), TransformFromCopy(old22, sc2[1]),
                   FadeIn(sc2[2], shift=LEFT * .5)],
                  [Create(sc2[3]), Write(sc2[4])],
                  [FadeOut(old22), TransformFromCopy(sc2[4], new22)],
                  LaggedStart(*[FadeIn(z) for z in zeros], lag_ratio=.15),
                  w=(.2, .2, .15, .2, .25))

        # ---- the load vector ----
        vcells = VGroup(*[Rectangle(width=VW, height=CH).set_stroke(HAIR, 2).move_to([VX, cell_c(i, 0)[1], 0])
                          for i in range(4)])
        vname = M("F", size=48, color=ROSE).move_to([VX, clab[0].get_y(), 0])
        vals = [M(r"R_0", size=44, color=ROSE), M(r"7000", size=40, color=ROSE),
                M(r"0", size=40, color=MUTED), M(r"R_3", size=44, color=ROSE)]
        for i, v in enumerate(vals):
            v.move_to(vcells[i])
        self.beat("The load vector: the reaction R zero at node zero, seven thousand at node one, nothing at "
                  "node two, and the reaction R three at node three.",
                  [FadeOut(sc2), Create(vcells), FadeIn(vname)],
                  [FadeIn(vals[0]), Indicate(wl, color=ROSE), Indicate(nlab[0], color=ROSE)],
                  [FadeIn(vals[1]), Indicate(VGroup(arr, plab), color=ROSE)],
                  [FadeIn(vals[2]), Indicate(nlab[2], color=ROSE)],
                  [FadeIn(vals[3]), Indicate(wr, color=ROSE), Indicate(nlab[3], color=ROSE)],
                  .15, w=(.12, .2, .2, .15, .18))
        self.wipe()
