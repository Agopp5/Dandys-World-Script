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
HUES = [GOLD, MINT, SKY]                   # element tints, as in the slides
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


def land(b, e):
    """Animations that grow element e's block onto rows and columns e+1, e+2 (build at play time)."""
    tgt = (gp(e + 1, e + 1) + gp(e + 2, e + 2)) / 2
    return [m.animate.scale(1 / SC, about_point=b["ctr"]).shift(tgt - b["ctr"]) for m in parts(b)] + \
        [FadeOut(b["labs"]), FadeOut(b["cap"])]


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
        note2 = E(r"\text{each entry}|\times|EA/l", size=36, color=INK2).next_to(grid, DOWN, buff=.25)
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
