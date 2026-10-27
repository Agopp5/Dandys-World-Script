"""S15: the pattern in the matrix (BRIEF.md S15)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})


# facts: the stamp pattern rebuilds the slides' four-node matrix; rows sum to zero; the wall row/col must go
def assemble(n, springs):
    K = np.zeros((n, n))
    for i, j, k in springs:          # spring k between nodes i, j: +k at (i,i), (j,j); -k at (i,j), (j,i)
        K[i, i] += k; K[j, j] += k; K[i, j] -= k; K[j, i] -= k
    return K


_k1, _k2, _k3 = 3.0, 5.0, 7.0
_K = assemble(4, [(0, 1, _k1), (1, 2, _k2), (1, 2, _k2), (2, 3, _k3)])   # two parallel k2 springs
assert np.allclose(_K, [[_k1, -_k1, 0, 0], [-_k1, _k1 + 2 * _k2, -2 * _k2, 0],
                        [0, -2 * _k2, 2 * _k2 + _k3, -_k3], [0, 0, -_k3, _k3]])
assert np.allclose(_K.sum(axis=1), 0)                       # every row sums to zero
assert np.allclose(_K[2], [0, -2 * _k2, 2 * _k2 + _k3, -_k3])  # row three
assert abs(np.linalg.det(_K)) < 1e-9 and abs(np.linalg.det(_K[1:, 1:])) > 1   # full singular, reduced not
# S12 two-spring matrix (wall node left out): k1 = 40, k2 = 20 -> [[60, -20], [-20, 20]]
assert np.allclose(assemble(3, [(0, 1, 40), (1, 2, 20)])[1:, 1:], [[60, -20], [-20, 20]])

ENT = [["k_1", "-|k_1", "0", "0"],
       ["-|k_1", "k_1|+|2|k_2", "-|2|k_2", "0"],
       ["0", "-|2|k_2", "2|k_2|+|k_3", "-|k_3"],
       ["0", "0", "-|k_3", "k_3"]]
# which glyph parts each spring contributes: (row, col, parts or None = whole entry)
BLOCKS = [
    [(0, 0, None), (0, 1, None), (1, 0, None), (1, 1, [0])],
    [(1, 1, [1, 2, 3]), (1, 2, None), (2, 1, None), (2, 2, [0, 1])],
    [(2, 2, [2, 3]), (2, 3, None), (3, 2, None), (3, 3, None)],
]
TINTS = [LILAC, GOLD, LIME]


class S15_Pattern(VScene):
    budget = 231

    def construct(self):
        # ---- the matrix, all entries faded ----
        mobs = [[E(s, size=44) for s in row] for row in ENT]
        mat = MobjectMatrix(mobs, h_buff=2.15, v_buff=1.0)
        mat.get_brackets().set_color(INK2)
        mat.move_to([-1.95, 0.8, 0])
        ents = mat.get_entries()
        e = lambda i, j: ents[4 * i + j]
        for m in ents:
            m.set_opacity(0.22)
        row_y = [np.mean([e(i, j).get_y() for j in range(4)]) for i in range(4)]
        col_x = [np.mean([e(i, j).get_x() for i in range(4)]) for j in range(4)]
        col_lab = VGroup(*[T(str(j + 1), size=30, color=MUTED).next_to(e(0, j), UP, buff=0.42)
                           .set_x(e(0, j).get_x()) for j in range(4)])
        y_top = max(c.get_y() for c in col_lab)
        for c in col_lab:
            c.set_y(y_top)
        row_lab = VGroup(*[T(str(i + 1), size=30, color=MUTED).set_y(e(i, 0).get_y())
                           .set_x(mat.get_left()[0] - 0.35) for i in range(4)])
        node_tag = T("node", size=26, color=MUTED).next_to(col_lab, LEFT, buff=0.5)

        # ---- the four-node chain (node 1 drawn free for now) ----
        y0 = -2.7
        xs = [-5.6, -2.6, 0.4, 3.4]
        P = [np.array([x, y0, 0]) for x in xs]
        dy = 0.38
        sp1 = spring(P[0], P[1], label="k_1")
        bar2 = Line(P[1] + dy * UP, P[1] + dy * DOWN, color=INK2, stroke_width=4)
        bar3 = Line(P[2] + dy * UP, P[2] + dy * DOWN, color=INK2, stroke_width=4)
        sp2a = spring(P[1] + dy * UP, P[2] + dy * UP, coils=4, amp=0.14, label="k_2")
        sp2b = spring(P[1] + dy * DOWN, P[2] + dy * DOWN, coils=4, amp=0.14)
        lab2b = M("k_2", size=32, color=LILAC).move_to((P[1] + P[2]) / 2 + (dy + 0.42) * DOWN)
        sp3 = spring(P[2], P[3], label="k_3")
        dots = VGroup(*[node(p) for p in P])
        badges = VGroup(*[badge(n + 1).move_to(P[n] + 0.85 * DOWN) for n in (0, 1, 2, 3)])
        badges[1].shift(0.35 * LEFT); badges[2].shift(0.35 * RIGHT)
        chain = VGroup(sp1, bar2, bar3, sp2a, sp2b, lab2b, sp3, dots, badges)
        spr = [VGroup(sp1), VGroup(sp2a, sp2b, lab2b), VGroup(sp3)]

        self.beat("Look at that matrix one spring at a time, and a pattern jumps out.",
                  [FadeIn(mat), FadeIn(col_lab), FadeIn(row_lab), FadeIn(node_tag), FadeIn(chain)])

        # ---- generic rule card ----
        gi = np.array([3.4, 2.35, 0]); gj = np.array([6.0, 2.35, 0])
        g_fig = VGroup(spring(gi, gj, coils=4, label="k"), node(gi), node(gj),
                       M("i", size=34, color=INK2).next_to(gi, DOWN, buff=0.2),
                       M("j", size=34, color=INK2).next_to(gj, DOWN, buff=0.2))
        gm = MobjectMatrix([[E("+|k", size=38), E("-|k", size=38)], [E("-|k", size=38), E("+|k", size=38)]],
                           h_buff=1.15, v_buff=0.85)
        gm.get_brackets().set_color(INK2)
        gm.move_to([5.0, 0.35, 0])
        ge = gm.get_entries()
        g_cols = VGroup(*[M(c, size=30, color=MUTED).next_to(ge[k], UP, buff=0.3) for k, c in ((0, "i"), (1, "j"))])
        g_rows = VGroup(*[M(c, size=30, color=MUTED).set_y(ge[k].get_y()).set_x(gm.get_left()[0] - 0.3)
                          for k, c in ((0, "i"), (2, "j"))])
        y_gc = max(c.get_y() for c in g_cols)
        for c in g_cols:
            c.set_y(y_gc)
        card = VGroup(g_fig, gm, g_cols, g_rows)

        # ---- block rectangles ----
        def block_rect(b, tint):
            r0 = min(i for i, _, _ in BLOCKS[b]); c0 = min(j for _, j, _ in BLOCKS[b])
            # height from the row pitch; width hugs the block's own entries
            grp = VGroup(e(r0, c0), e(r0, c0 + 1), e(r0 + 1, c0), e(r0 + 1, c0 + 1))
            w = grp.width + 0.3; h = 1.0 * 2 - 0.22
            cx = grp.get_center()[0]
            cy = (row_y[r0] + row_y[r0 + 1]) / 2
            return RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=tint, stroke_width=3,
                                    fill_color=tint, fill_opacity=0.12).move_to([cx, cy, 0])
        rects = [block_rect(b, TINTS[b]) for b in range(3)]
        for r in rects:
            r.set_z_index(-1)

        def light(b):
            anims = [FadeIn(rects[b]), Indicate(spr[b], color=TINTS[b], scale_factor=1.08)]
            for i, j, parts in BLOCKS[b]:
                tgt = e(i, j) if parts is None else VGroup(*[e(i, j)[p] for p in parts])
                anims.append(tgt.animate.set_opacity(1))
            return anims

        zeros = VGroup(*[e(i, j) for i in range(4) for j in range(4) if ENT[i][j] == "0"])
        self.beat("A spring of stiffness k between nodes i and j puts plus k on the diagonal at i, plus k on the "
                  "diagonal at j, and minus k in the two spots that connect them.",
                  FadeIn(card), light(0), light(1), [*light(2), zeros.animate.set_opacity(0.6)],
                  w=(.3, .23, .23, .24))

        d11, d22 = e(1, 1), e(2, 2)
        self.beat("This is the key idea for everything that follows: each spring brings its own little two by two "
                  "block, and where blocks share a node, the entries simply add.",
                  self.spotlight(d11, d22), .55, style="slower and deliberate, stressing the key words")

        self.beat("Use the pattern: pause and do checkpoint two point two in your guide, and write row three.",
                  [self.unspot(), FadeOut(card)])
        self.checkpoint("2.2", "Four-node springs: write row 3 of the stiffness matrix")

        # ---- row three, row sums, rigid slide ----
        row3 = VGroup(*[e(2, j) for j in range(4)])
        r3_box = SurroundingRectangle(row3, color=ACCENT, buff=0.16, corner_radius=0.1, stroke_width=4)
        sums = VGroup(*[M(r"\to 0", size=38, color=GOOD).set_y(e(i, 0).get_y()).set_x(mat.get_right()[0] + 0.75)
                        for i in range(4)])
        rigid = T("no stretch, so no force", size=30, color=MUTED).move_to([4.6, -1.65, 0])
        with self.say("Row three: minus two k two, then two k two plus k three, then minus k three. And notice: "
                      "every row adds up to zero. Shift every node by the same amount, and no spring stretches, "
                      "so no force is needed. That's what a zero row sum says.") as d:
            self.play(*[FadeOut(r) for r in rects], Create(r3_box), zeros.animate.set_opacity(1), run_time=.08 * d)
            self.play(LaggedStart(*[Indicate(e(2, j), color=ACCENT, scale_factor=1.12) for j in (1, 2, 3)],
                                  lag_ratio=.6), run_time=.2 * d)
            self.play(LaggedStart(*[FadeIn(s, shift=.2 * LEFT) for s in sums], lag_ratio=.3), run_time=.14 * d)
            self.wait(.08 * d)
            self.play(chain.animate(rate_func=there_and_back).shift(1.1 * RIGHT), run_time=.26 * d)
            self.play(FadeIn(rigid), run_time=.08 * d)
            self.play(Indicate(sums, color=GOOD), run_time=.1 * d)
            self.wait(.06 * d)

        # ---- the wall node goes ----
        wl = wall(P[0], side=LEFT, h=1.4)
        q1z = E(r"q_1|=|0", size=36).move_to(P[0] + 1.05 * UP + 0.1 * LEFT)
        r1 = VGroup(*[e(0, j) for j in range(4)])
        c1 = VGroup(*[e(i, 0) for i in range(4)])
        s_row = Line(r1.get_left() + 0.25 * LEFT, r1.get_right() + 0.25 * RIGHT, color=BAD, stroke_width=5)
        s_col = Line(c1.get_top() + 0.25 * UP, c1.get_bottom() + 0.25 * DOWN, color=BAD, stroke_width=5)
        rest = VGroup(*[e(i, j) for i in range(1, 4) for j in range(1, 4)])
        box3 = SurroundingRectangle(rest, color=GOOD, buff=0.2, corner_radius=0.1, stroke_width=4)
        old = MobjectMatrix([[E("k_1|+|k_2", size=34), E("-|k_2", size=34)],
                             [E("-|k_2", size=34), E("k_2", size=34)]], h_buff=1.9, v_buff=0.8)
        old.get_brackets().set_color(INK2)
        old_head = T("two springs, earlier", size=30, color=INK2)
        old_note = T("wall node already left out", size=30, color=MUTED)
        old_grp = VGroup(old_head, old, old_note).arrange(DOWN, buff=0.3)
        old_grp.move_to([5.0, 0.9, 0]).set_x(min(5.0, 6.75 - old_grp.width / 2))
        with self.say("But node one is on the wall: q one is zero, and the wall supplies whatever force it needs. "
                      "So its row and column don't belong in the equations we solve. Cross them out, and three "
                      "equations remain, for q two, q three and q four. Our two-spring matrix was like that too: "
                      "its wall node was never in it.") as d:
            self.play(FadeOut(sums), FadeOut(r3_box), FadeOut(rigid), FadeIn(wl), Write(q1z), run_time=.12 * d)
            self.wait(.2 * d)
            self.play(Create(s_row), Create(s_col), r1.animate.set_opacity(.3), c1.animate.set_opacity(.3),
                      row_lab[0].animate.set_opacity(.3), col_lab[0].animate.set_opacity(.3), run_time=.12 * d)
            self.play(Create(box3), run_time=.1 * d)
            self.play(Indicate(VGroup(row_lab[1:], col_lab[1:]), color=SKY), run_time=.12 * d)
            self.wait(.04 * d)
            self.play(FadeIn(old_grp, shift=.2 * LEFT), run_time=.12 * d)
            self.wait(.18 * d)

        kb = key_box(r"\text{stretch} = q_j - q_i", r"\frac{\partial \Pi}{\partial q_i} = 0\ \text{for every free node}",
                     r"\text{each spring adds } k\begin{bmatrix}1&-1\\-1&1\end{bmatrix}", label="KEY IDEA")
        kb.scale_to_fit_width(12.4).move_to(ORIGIN)
        everything = VGroup(mat, col_lab, row_lab, node_tag, chain, wl, q1z, s_row, s_col, box3, old_grp)
        self.beat("So, stepping back: write U and W, take one partial derivative per free node, and the stiffness "
                  "matrix builds itself from little blocks. Next, your first homework problem.",
                  [FadeOut(everything)], FadeIn(kb), .6)
        self.wipe()
