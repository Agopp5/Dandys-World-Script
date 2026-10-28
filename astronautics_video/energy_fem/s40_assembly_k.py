"""S40: assembling the stiffness matrix (BRIEF.md S40)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# ---------------------------------------------------------------- facts
KL = np.array([[1, -1], [-1, 1]])                      # element stiffness, in units of E A / l
KG = np.zeros((4, 4))
for _e in range(3):                                    # element e joins nodes e+1, e+2: add its block there
    KG[_e:_e + 2, _e:_e + 2] += KL
KG_TRUE = np.array([[1, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 1]])
assert np.array_equal(KG, KG_TRUE)
assert KG[1, 1] == 1 + 1 and KG[2, 2] == 1 + 1         # shared nodes: one plus one gives two
assert np.allclose(KG.sum(axis=1), 0)                  # moving everything together stores no energy


def _U(q):                                             # U_1 + U_2 + U_3 per E A / l
    return sum(.5 * (q[e + 1] - q[e]) ** 2 for e in range(3))


_h, _I = 1e-3, np.eye(4)
_H = np.array([[(_U(_h * (_I[i] + _I[j])) - _U(_h * (_I[i] - _I[j])) - _U(_h * (_I[j] - _I[i]))
                 + _U(-_h * (_I[i] + _I[j]))) / (4 * _h * _h) for j in range(4)] for i in range(4)])
assert np.allclose(_H, KG_TRUE)                        # dPi/dq_i = 0 gives exactly this matrix

# ---------------------------------------------------------------- layout
CS = 1.2                                   # global cell size
G0 = np.array([-6.1, 2.0, 0.])             # top-left corner of the 4 by 4 grid
SC = .7                                    # element blocks wait at 70 % size, then grow as they land
BX, BY = [1.05, 3.5, 5.95], .85            # where the three element blocks wait
HUES = [LILAC, interpolate_color(LILAC, INK, .45), interpolate_color(LILAC, BG, .35)]  # stiffness shades
FC, C2 = np.array([1.3, -.4, 0.]), 1.05    # the finished matrix: centre and entry pitch
UC = {"U_1": MINT, "U_2": MINT, "U_3": MINT}


def gp(i, j):
    """Centre of global cell (i, j), 1-indexed."""
    return G0 + np.array([CS * (j - .5), -CS * (i - .5), 0.])


def fp(i, j):
    """Position of entry (i, j) in the finished matrix."""
    return FC + np.array([C2 * (j - 2.5), -C2 * (i - 2.5), 0.])


def make_block(e):
    hue, ctr, s = HUES[e], np.array([BX[e], BY, 0.]), CS * SC
    fills, ents = {}, {}
    for r in (1, 2):
        for k in (1, 2):
            p = ctr + np.array([s * (k - 1.5), -s * (r - 1.5), 0.])
            fills[(r, k)] = Square(s).set_stroke(width=0).set_fill(hue, .22).move_to(p).set_z_index(1)
            ents[(r, k)] = M("1" if r == k else "-1", size=52 * SC, color=hue).move_to(p).set_z_index(4)
    outline = Square(2 * s).set_stroke(hue, 5).set_fill(opacity=0).move_to(ctr).set_z_index(2)
    tops = [M(str(k), size=36, color=INK2).move_to(ctr + np.array([s * (k - 1.5), s + .3, 0.])) for k in (1, 2)]
    lefts = [M(str(r), size=36, color=INK2).move_to(ctr + np.array([-s - .3, -s * (r - 1.5), 0.])) for r in (1, 2)]
    cap = VGroup(T("element " + str(e + 1), size=34, color=hue),
                 T("nodes " + str(e + 1) + ", " + str(e + 2), size=32, color=INK2)).arrange(DOWN, buff=.12)
    cap.next_to(outline, DOWN, buff=.25)
    return dict(hue=hue, ctr=ctr, fills=fills, ents=ents, outline=outline, labs=VGroup(*tops, *lefts), cap=cap)


def parts(b):
    return [*b["fills"].values(), b["outline"], *b["ents"].values()]


def land(b, e, shared=None):
    """Animations that grow element e's block onto rows and columns e+1, e+2 (build at play time).
    shared: the entry already in the block's (1,1) spot; it steps left and the new one lands beside it."""
    tgt = (gp(e + 1, e + 1) + gp(e + 2, e + 2)) / 2
    anims = [m.animate.scale(1 / SC, about_point=b["ctr"]).shift(tgt - b["ctr"]) for m in parts(b)
             if shared is None or m is not b["ents"][(1, 1)]]
    if shared is not None:
        m = b["ents"][(1, 1)]
        anims += [m.animate.scale(1 / SC, about_point=b["ctr"]).shift(tgt - b["ctr"] + RIGHT * .3),
                  shared.animate.shift(LEFT * .3)]
    return anims + [FadeOut(b["labs"]), FadeOut(b["cap"])]


def trace(b, e):
    """Box the block's local (1,1), box its global home, and an arrow between them."""
    loc = Square(CS * SC).set_stroke(b["hue"], 7).set_fill(opacity=0).move_to(b["fills"][(1, 1)]).set_z_index(6)
    glob = Square(CS).set_stroke(b["hue"], 7).set_fill(opacity=0).move_to(gp(e + 1, e + 1)).set_z_index(6)
    arr = Arrow(loc.get_left(), glob.get_right(), buff=.12, color=b["hue"], stroke_width=6).set_z_index(6)
    return loc, glob, arr


def bracket(side):
    x0, top, bot, w = FC[0] + side * (2 * C2 + .1), FC[1] + 2 * C2 - .05, FC[1] - 2 * C2 + .05, .22
    return VMobject().set_points_as_corners([[x0 - side * w, top, 0], [x0, top, 0], [x0, bot, 0],
                                             [x0 - side * w, bot, 0]]).set_stroke(INK, 4)


class S40_Assembly_K(VScene):
    budget = 239

    def construct(self):
        # ------------------------------------------------ beat 1: Pi is a sum; one equation per node
        pi_eq = E(r"\Pi|=|U_1|+|U_2|+|U_3|-|W", size=60, cmap=UC).move_to(UP * 1.6)
        bU = Brace(VGroup(*pi_eq[2:7]), DOWN, color=MINT)
        lU = T("strain energy of each element", size=34, color=MINT).next_to(bU, DOWN, buff=.15)
        bW = Brace(pi_eq[8], UP, color=EMBER)
        lW = T("work potential of the loads", size=34, color=EMBER).next_to(bW, UP, buff=.15)
        cards = VGroup()
        for i in range(1, 5):
            m = M(r"\frac{\partial \Pi}{\partial q_" + str(i) + r"} = 0", size=48)
            tint(m, [((1, 2), GOLD), ((4, 6), SKY)])
            cards.add(panel(m))
        cards.arrange(RIGHT, buff=.35).move_to(DOWN * 1.9)
        note1 = T("one equation for each node", size=32, color=MUTED).next_to(cards, DOWN, buff=.3)
        self.beat("First, connect this back to the bowl. The column's Pi is the sum of every element's strain "
                  "energy, minus the work potential of the loads. Take a partial derivative for each node and set "
                  "it to zero, just as we did for the springs in episode two.",
                  Write(pi_eq), [GrowFromCenter(bU), FadeIn(lU)], [GrowFromCenter(bW), FadeIn(lW)], .05,
                  LaggedStart(*[FadeIn(c, shift=.3 * UP) for c in cards], lag_ratio=.3), FadeIn(note1), .08,
                  w=(.25, .14, .12, .3, .06))

        # ------------------------------------------------ beat 2: element blocks beside an empty 4 by 4 grid
        gcell = {(i, j): Square(CS).set_stroke(AXIS, 2).set_fill(opacity=0).move_to(gp(i, j))
                 for i in range(1, 5) for j in range(1, 5)}
        rlab = {i: M(str(i), size=40, color=INK2).next_to(gcell[(i, 1)], LEFT, buff=.2) for i in range(1, 5)}
        clab = {j: M(str(j), size=40, color=INK2).next_to(gcell[(1, j)], UP, buff=.15) for j in range(1, 5)}
        grid = VGroup(*gcell.values())
        labs = VGroup(*rlab.values(), *clab.values())
        note2 = VGroup(T("each entry times", size=34, color=INK2), M(r"EA/l", size=44, color=INK2))
        note2.arrange(RIGHT, buff=.2).next_to(grid, DOWN, buff=.25)
        kqf = E("K|q|=|F", size=60).move_to([-3.7, 3.25, 0])
        keq = E(r"k|=|\frac{EA}{l}|\begin{bmatrix}1&-1\\-1&1\end{bmatrix}", size=48).move_to([3.5, -2.45, 0])
        blocks = [make_block(e) for e in range(3)]
        self.beat("Each element's energy is the spring formula, with stiffness E A over l. So the result is the "
                  "same kind of matrix we built from springs: a stiffness matrix K, times the displacements q, "
                  "equals the loads F.",
                  [FadeOut(cards), FadeOut(note1), FadeOut(bU), FadeOut(lU), FadeOut(bW), FadeOut(lW),
                   pi_eq.animate.scale(.8).move_to([3.5, 3.25, 0])],
                  Write(keq),
                  [*[FadeIn(m, shift=.4 * UP) for b in blocks for m in parts(b)],
                   *[FadeIn(b["labs"]) for b in blocks], *[FadeIn(b["cap"]) for b in blocks]],
                  [Create(grid), FadeIn(labs), FadeIn(note2)], .05,
                  Write(kqf), .1,
                  w=(.12, .2, .14, .2, .17))

        # ------------------------------------------------ beat 3: element 1 lands on rows/columns 1, 2
        b = blocks[0]
        loc, glob, arr = trace(b, 0)
        with self.say("Element one connects nodes one and two. Its local spot one-one goes to the big matrix's "
                      "spot one-one, and its block fills rows and columns one and two.") as d:
            self.play(Indicate(b["cap"], color=INK, scale_factor=1.1),
                      *[l.animate.set_color(b["hue"]) for l in (rlab[1], rlab[2], clab[1], clab[2])], run_time=.2 * d)
            self.wait(.03 * d)
            self.play(Create(loc), run_time=.1 * d)
            self.play(GrowArrow(arr), Create(glob), run_time=.17 * d)
            self.wait(.1 * d)
            self.play(*land(b, 0), FadeOut(loc), FadeOut(arr), run_time=.2 * d)
            self.play(FadeOut(glob), Indicate(VGroup(rlab[1], rlab[2], clab[1], clab[2]), color=INK),
                      run_time=.12 * d)
            self.wait(.08 * d)

        # ------------------------------------------------ beat 4: element 2 lands; spot (2,2) is shared
        b = blocks[1]
        loc, glob, arr = trace(b, 1)
        with self.say("Element two connects nodes two and three. Its local spot one-one goes to the big matrix's "
                      "spot two-two. But spot two-two is already taken by element one.") as d:
            self.play(Indicate(b["cap"], color=INK, scale_factor=1.1),
                      *[l.animate.set_color(INK2) for l in (rlab[1], clab[1])],
                      *[l.animate.set_color(b["hue"]) for l in (rlab[2], rlab[3], clab[2], clab[3])], run_time=.2 * d)
            self.wait(.04 * d)
            self.play(Create(loc), run_time=.1 * d)
            self.play(GrowArrow(arr), Create(glob), run_time=.17 * d)
            self.wait(.06 * d)
            self.snap("element 2: local (1,1) to global (2,2)")
            a, bb = blocks[0]["ents"][(2, 2)], b["ents"][(1, 1)]
            self.play(*land(b, 1, shared=a), FadeOut(loc), FadeOut(arr), run_time=.2 * d)
            self.play(FadeOut(glob), Circumscribe(gcell[(2, 2)], color=INK), run_time=.1 * d)
            self.play(Indicate(a, color=INK, scale_factor=1.4), run_time=.1 * d)
            self.wait(.03 * d)

        # ------------------------------------------------ beat 5 (crux): overlapping entries add
        plus = M("+", size=48, color=INK).move_to(gp(2, 2)).set_z_index(30)
        two = M("2", size=56, color=INK).move_to(gp(2, 2)).set_z_index(30)
        L1 = E(r"U_1|=|\frac12|\frac{EA}{l}|\big(|q_2|-|q_1|\big)^2", size=48, cmap=UC)
        L2 = E(r"U_2|=|\frac12|\frac{EA}{l}|\big(|q_3|-|q_2|\big)^2", size=48, cmap=UC)
        Ls = VGroup(L1, L2).arrange(DOWN, buff=.35, aligned_edge=LEFT).move_to([3.5, -2.45, 0])
        for m in (a, bb, plus, two, Ls):         # stay bright above the spotlight's dimming
            m.set_z_index(500)
        with self.say("This is the key step of assembly, so watch it closely. Where two blocks land on the same "
                      "spot, their entries add. One plus one gives two. Why? Because q two appears in two elements' "
                      "energies, so the derivative with respect to q two picks up a term from each.",
                      style="slower and deliberate, stressing the key words") as d:
            self.play(FadeOut(keq), run_time=.05 * d)
            self.play(self.spotlight(gcell[(2, 2)], pi_eq[2], pi_eq[4]), run_time=.12 * d)
            self.wait(.05 * d)
            self.play(FadeIn(plus), Circumscribe(gcell[(2, 2)], color=INK), run_time=.15 * d)
            self.snap("1 + 1 at spot (2,2)")
            self.wait(.08 * d)
            self.play(ReplacementTransform(a, two), FadeOut(bb, target_position=gp(2, 2)),
                      FadeOut(plus, target_position=gp(2, 2)), run_time=.1 * d)
            self.wait(.05 * d)
            self.play(FadeIn(Ls), Indicate(pi_eq[2], color=INK), Indicate(pi_eq[4], color=INK), run_time=.14 * d)
            self.play(Circumscribe(L1[5], color=INK), Circumscribe(L2[7], color=INK), run_time=.12 * d)
            self.wait(.14 * d)

        # ------------------------------------------------ beat 6: element 3, zeros, the finished K
        b = blocks[2]
        a3, b3 = blocks[1]["ents"][(2, 2)], b["ents"][(1, 1)]
        plus3 = M("+", size=48, color=INK).move_to(gp(3, 3)).set_z_index(30)
        two3 = M("2", size=56, color=INK).move_to(gp(3, 3)).set_z_index(30)
        zeros = {(i, j): M("0", size=52, color=INK2).move_to(gp(i, j)).set_z_index(4)
                 for (i, j) in [(1, 3), (1, 4), (2, 4), (3, 1), (4, 1), (4, 2)]}
        e0, e1, e2 = (bl["ents"] for bl in blocks)
        ent = {(1, 1): e0[(1, 1)], (1, 2): e0[(1, 2)], (2, 1): e0[(2, 1)], (2, 2): two,
               (2, 3): e1[(1, 2)], (3, 2): e1[(2, 1)], (3, 3): two3,
               (3, 4): e2[(1, 2)], (4, 3): e2[(2, 1)], (4, 4): e2[(2, 2)], **zeros}
        assert all(ent[(i, j)].get_tex_string() == str(int(KG_TRUE[i - 1, j - 1]))
                   for (i, j) in ent if (i, j) not in ((2, 2), (3, 3)))
        brL, brR = bracket(-1), bracket(1)
        prefix = E(r"K|=|\frac{EA}{l}", size=56).next_to(brL, LEFT, buff=.3)
        box = SurroundingRectangle(VGroup(prefix, brL, brR), buff=.3, color=LILAC, stroke_width=4)
        boxlab = VGroup(T("global stiffness matrix", size=38), M("K", size=48, color=LILAC)).arrange(RIGHT, buff=.2)
        boxlab.next_to(box, DOWN, buff=.2)
        rowbox = Rectangle(width=4 * C2 + .2, height=.8).set_stroke(LILAC, 3).move_to(FC + UP * 1.5 * C2)
        with self.say("Element three goes into rows and columns three and four, adding at spot three-three. "
                      "Everywhere no element touches, it's zero. The result: E A over l, times one, minus one, "
                      "zero, zero; minus one, two, minus one, zero; zero, minus one, two, minus one; zero, zero, "
                      "minus one, one.") as d:
            self.play(self.unspot(), FadeOut(Ls), Indicate(b["cap"], color=INK, scale_factor=1.1),
                      *[l.animate.set_color(INK2) for l in (rlab[2], clab[2])],
                      *[l.animate.set_color(b["hue"]) for l in (rlab[3], rlab[4], clab[3], clab[4])], run_time=.1 * d)
            self.play(*land(b, 2, shared=a3), run_time=.1 * d)
            self.play(FadeIn(plus3), run_time=.04 * d)
            self.play(ReplacementTransform(a3, two3), FadeOut(b3, target_position=gp(3, 3)),
                      FadeOut(plus3, target_position=gp(3, 3)), run_time=.04 * d)
            self.play(LaggedStart(*[FadeIn(z, scale=1.3) for z in zeros.values()], lag_ratio=.15), run_time=.11 * d)
            self.play(*[m.animate.move_to(fp(i, j)).set_color(INK) for (i, j), m in ent.items()],
                      FadeOut(grid), FadeOut(labs), FadeOut(note2), FadeOut(pi_eq),
                      *[FadeOut(f) for bl in blocks for f in bl["fills"].values()],
                      *[FadeOut(bl["outline"]) for bl in blocks], run_time=.08 * d)
            self.play(FadeIn(brL), FadeIn(brR), Write(prefix), Create(box), FadeIn(boxlab), run_time=.06 * d)
            self.play(Create(rowbox), run_time=.03 * d)
            self.wait(.07 * d)
            for r, hold in ((2, .1), (3, .11), (4, .05)):
                self.play(rowbox.animate.move_to(FC + UP * (2.5 - r) * C2), run_time=.03 * d)
                self.wait(hold * d)
            self.play(FadeOut(rowbox), run_time=.02 * d)
        self.wait(1.0)
        self.wipe()
