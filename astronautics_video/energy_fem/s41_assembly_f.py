"""S41: assembling the load vector of the column under its own weight (BRIEF.md S41)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: each element's load vector is (c l / 2){1, 1}; assembling three of them into four nodes
conn = [(0, 1), (1, 2), (2, 3)]
Fg = np.zeros(4)
Kg = np.zeros((4, 4))
for a, b in conn:
    Fg[[a, b]] += [1, 1]                                   # in units of c l / 2
    Kg[np.ix_([a, b], [a, b])] += [[1, -1], [-1, 1]]       # in units of E A / l
assert np.allclose(Fg, [1, 2, 2, 1])
assert np.allclose(Kg, [[1, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 1]])
assert np.allclose(Kg.sum(axis=1), 0)                      # rows sum to zero before supports
# total nodal load equals the column's whole weight: (c l / 2) * 6 = 3 c l = c L
rho, A, g, L = 2700.0, 0.01, 9.81, 6.0
c, l = -rho * A * g, L / 3
assert np.isclose((c * l / 2) * Fg.sum(), c * L)
assert c < 0                                               # weight points down (minus x)

COLX = -4.3                      # column centre line
YN = [-2.8, -1.0, 0.8, 2.6]      # node heights (node 1 at the base)
LA = 0.55                        # length of one c l / 2 arrow
XB, XA, XS = 0.8, 1.2, 1.0       # arrow x-offsets: from element below, from element above, stacked
VX = 1.15                        # left edge of the right-hand math


def down_arrow(x, y, length, sw=5):
    return Arrow(start=[x, y, 0], end=[x, y - length, 0], buff=0, color=ROSE, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=12)


def fvec(entries, y=-0.35):
    """F = {entries}, with MUTED node names beside the rows, left edge at VX."""
    m = MobjectMatrix([[E(s, size=48)] for s in entries], v_buff=1.1)
    head = E(r"F|=", size=56)
    head.next_to(m, LEFT, buff=0.3)
    labs = VGroup()
    for i in range(4):
        t = T("node %d" % (i + 1), size=30, color=MUTED)
        t.next_to(m.get_brackets()[1], RIGHT, buff=0.35).set_y(m.get_entries()[i].get_y())
        labs.add(t)
    grp = VGroup(head, m, labs)
    grp.shift((VX - grp.get_left()[0]) * RIGHT + (y - m.get_y()) * UP)
    return grp


class S41_Assembly_F(VScene):
    budget = 167

    def construct(self):
        # ---------- the column (left half) ----------
        elems = VGroup(*[bar(YN[i], YN[i + 1], y=0, h=0.8).rotate(PI / 2, about_point=ORIGIN).shift(COLX * RIGHT)
                         for i in range(3)])
        ground = wall(np.array([COLX, YN[0], 0]), side=DOWN, h=1.3)
        dots = VGroup(*[node(np.array([COLX, y, 0]), r=0.09) for y in YN])
        nlabs = VGroup(*[T(str(i + 1), size=36, color=INK).move_to([COLX - 0.75, YN[i], 0]) for i in range(4)])
        tags = VGroup()
        for i in range(3):
            ring = Circle(radius=0.34, color=INK2, stroke_width=3)
            tags.add(VGroup(ring, T(str(i + 1), size=36, color=INK2)).move_to(
                [COLX - 1.55, (YN[i] + YN[i + 1]) / 2, 0]))
        xax = Arrow(start=[-6.75, YN[0], 0], end=[-6.75, YN[0] + 1.6, 0], buff=0, color=INK2, stroke_width=4)
        xlab = M("x", size=40, color=INK2).next_to(xax, UP, buff=0.15)
        column = VGroup(elems, ground, dots, nlabs, tags, xax, xlab)

        # distributed weight: four small arrows per element
        dist = []
        for i in range(3):
            dist.append([down_arrow(COLX + XB, YN[i] + t, 0.42, sw=4) for t in (0.6, 0.95, 1.3, 1.65)])
        # nodal arrows: below[n] comes from the element under node n, above[n] from the element over it
        below = {n: down_arrow(COLX + XB, YN[n], LA) for n in (1, 2, 3)}
        above = {n: down_arrow(COLX + XA, YN[n], LA) for n in (0, 1, 2)}

        # ---------- right-hand math ----------
        cnote = E(r"c|=|-\rho A g", size=48).move_to([3.4, 3.0, 0])
        each_t = T("each element:", size=36, color=INK2)
        each_e = E(r"c\,l|=|\frac{cl}{2}|+|\frac{cl}{2}", size=48)
        each = VGroup(each_t, each_e).arrange(RIGHT, buff=0.3).move_to([3.4, 1.3, 0])

        with self.say("The loads assemble the same way. Each element carries a total weight c l, with c equal "
                      "to minus rho A g, and sends half of it to each of its two nodes.") as d:
            self.play(FadeIn(column), run_time=.12 * d)
            self.play(LaggedStart(*[GrowArrow(a) for e in dist for a in e], lag_ratio=.08),
                      FadeIn(each_t), Write(each_e[0]), run_time=.2 * d)
            self.play(Write(cnote), run_time=.15 * d)
            anims = []
            for i in range(3):
                anims.append(ReplacementTransform(VGroup(*dist[i][:2]), above[i]))
                anims.append(ReplacementTransform(VGroup(*dist[i][2:]), below[i + 1]))
            self.play(*anims, Write(each_e[1:]), run_time=.3 * d)
            self.wait(.2 * d)

        # empty load vector waiting to be filled
        vec = fvec([r"\frac{cl}{2}", r"cl", r"cl", r"\frac{cl}{2}"])
        head, mat, rlabs = vec
        qs = VGroup(*[E("?", size=48).set_color(MUTED).move_to(e) for e in mat.get_entries()])
        self.beat("Your turn: pause and do checkpoint six point one in your guide, and build the load vector.",
                  FadeOut(each), [Write(head), FadeIn(mat.get_brackets()), FadeIn(qs), FadeIn(rlabs)],
                  w=(.3, .7))
        self.checkpoint("6.1", "Column under its own weight: assemble the load vector")

        # ---------- stacking at each node ----------
        stacked = {0: down_arrow(COLX + XS, YN[0], LA), 3: down_arrow(COLX + XS, YN[3], LA),
                   1: down_arrow(COLX + XS, YN[1], 2 * LA), 2: down_arrow(COLX + XS, YN[2], 2 * LA)}
        stex = [r"\frac{cl}{2}", r"cl", r"cl", r"\frac{cl}{2}"]
        slabs = [E(stex[n], size=40).next_to(stacked[n], RIGHT, buff=0.22) for n in range(4)]
        work = [E(r"\text{node 1: }|\frac{cl}{2}", size=44),
                E(r"\text{node 2: }|\frac{cl}{2}|+|\frac{cl}{2}|=|cl", size=44),
                E(r"\text{node 3: }|\frac{cl}{2}|+|\frac{cl}{2}|=|cl", size=44),
                E(r"\text{node 4: }|\frac{cl}{2}", size=44)]
        for w_ in work:
            w_.move_to([3.4, -3.25, 0])
        ent = mat.get_entries()
        with self.say("Node one gets c l over two from element one. Node two is shared: c l over two from "
                      "element one, plus c l over two from element two. That's c l. Node three also gets c l. "
                      "Node four, at the top, only c l over two.") as d:
            # node 1
            self.play(Indicate(above[0], color=ROSE), FadeIn(work[0]), run_time=.08 * d)
            self.play(Transform(above[0], stacked[0]), FadeIn(slabs[0]),
                      ReplacementTransform(qs[0], ent[0]), Indicate(rlabs[0], color=INK), run_time=.1 * d)
            # node 2: element one's half, then element two's half, then they stack
            self.play(FadeOut(work[0]), FadeIn(work[1][:2]), Indicate(below[1], color=ROSE, scale_factor=1.4),
                      run_time=.12 * d)
            self.play(FadeIn(work[1][2:4]), Indicate(above[1], color=ROSE, scale_factor=1.4), run_time=.14 * d)
            self.play(ReplacementTransform(VGroup(below[1], above[1]), stacked[1]), FadeIn(slabs[1]),
                      FadeIn(work[1][4:]), ReplacementTransform(qs[1], ent[1]), run_time=.14 * d)
            self.wait(.04 * d)
            # node 3
            self.play(FadeOut(work[1]), FadeIn(work[2]),
                      ReplacementTransform(VGroup(below[2], above[2]), stacked[2]), FadeIn(slabs[2]),
                      ReplacementTransform(qs[2], ent[2]), run_time=.14 * d)
            # node 4
            self.play(FadeOut(work[2]), FadeIn(work[3]), Transform(below[3], stacked[3]), FadeIn(slabs[3]),
                      ReplacementTransform(qs[3], ent[3]), run_time=.14 * d)
            self.wait(.1 * d)
        nodal = VGroup(above[0], stacked[1], stacked[2], below[3])

        # factored form, held under the vector
        fac = E(r"F|=|\frac{cl}{2}|\{\,1,\;2,\;2,\;1\,\}^{T}", size=44).move_to([3.4, -3.25, 0])
        fac_r = E(r"F|=|\frac{cl}{2}|\{\,1,\;2,\;2,\;1\,\}^{T}|+|\{\,|R|,\;0,\;0,\;0\,\}^{T}", size=44)
        fit(fac_r, 6.4, 1.2)
        fac_r.move_to([3.4, -3.25, 0])
        self.play(FadeOut(work[3]), FadeIn(fac), run_time=1.2)
        self.wait(.8)

        # ---------- the reaction ----------
        rarrow = Arrow(start=[COLX, YN[0] - 1.15, 0], end=[COLX, YN[0] - 0.05, 0], buff=0, color=ROSE,
                       stroke_width=6, max_tip_length_to_length_ratio=0.3).set_z_index(5)
        rlab = E("R", size=44).next_to(rarrow, LEFT, buff=0.2).shift(0.3 * DOWN)
        vec2 = fvec([r"\frac{cl}{2}+|R", r"cl", r"cl", r"\frac{cl}{2}"])
        head2, mat2, rlabs2 = vec2
        ent2 = mat2.get_entries()
        with self.say("And one more force: the ground pushes up on node one with a reaction R that we don't know "
                      "yet. R is a force at node one like any other, so it goes in node one's entry. We include it "
                      "so that row one stays a true equation we can use later.") as d:
            self.play(GrowArrow(rarrow), FadeIn(rlab), run_time=.15 * d)
            self.wait(.2 * d)
            self.play(ReplacementTransform(head, head2), ReplacementTransform(mat.get_brackets(), mat2.get_brackets()),
                      *[ReplacementTransform(ent[i], ent2[i]) for i in range(1, 4)],
                      ReplacementTransform(ent[0], ent2[0][0]), FadeIn(ent2[0][1:], shift=.2 * UP),
                      ReplacementTransform(rlabs, rlabs2),
                      ReplacementTransform(fac[:4], fac_r[:4]), FadeIn(fac_r[4:]), run_time=.2 * d)
            self.play(Circumscribe(VGroup(ent2[0], rlabs2[0]), color=ROSE), run_time=.15 * d)
            self.wait(.3 * d)

        # ---------- the full system ----------
        kq = E(r"K|q|=|F", size=56).move_to([-0.6, 3.0, 0])
        qmark = M("?", size=110, color=GOLD).next_to(kq, RIGHT, buff=0.6)
        rows = [["1", "-1", "0", "0"], ["-1", "2", "-1", "0"], ["0", "-1", "2", "-1"], ["0", "0", "-1", "1"]]
        kmat = MobjectMatrix([[E(x, size=44).set_color(LILAC) for x in r] for r in rows], h_buff=1.05, v_buff=1.1)
        pre = E(r"\frac{EA}{l}", size=48).set_color(LILAC)
        qv = MobjectMatrix([[E("q_%d" % i, size=44)] for i in range(1, 5)], v_buff=1.1)
        eqs = E("=", size=48)
        rhs = MobjectMatrix([[E(s, size=44)] for s in (r"\frac{cl}{2}+|R", r"cl", r"cl", r"\frac{cl}{2}")],
                            v_buff=1.1)
        system = VGroup(pre, kmat, qv, eqs, rhs).arrange(RIGHT, buff=0.3)
        fit(system, 13.2, 5.0)
        system.move_to([0, -0.4, 0])
        note = T("four equations", size=36, color=INK2).next_to(system, DOWN, buff=0.35)
        with self.say("So K times q equals F, with four equations. But we can't solve it yet. Something's missing.") as d:
            self.play(FadeOut(VGroup(column, nodal, VGroup(*slabs), rarrow, rlab, cnote, fac_r, head2, rlabs2)),
                      ReplacementTransform(mat2, rhs), FadeIn(VGroup(pre, kmat, qv, eqs)), Write(kq),
                      run_time=.35 * d)
            self.play(FadeIn(note), run_time=.15 * d)
            self.wait(.1 * d)
            self.play(FadeIn(qmark, scale=1.6), run_time=.15 * d)
            self.wait(.25 * d)
        self.wipe()
