"""S35: the element stiffness matrix (BRIEF.md S35)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# ---- facts -------------------------------------------------------------------------------------------
EA_num, l_num = 2e6, 500.0
assert np.isclose(EA_num / l_num, 4000.0)                       # 2 x 10^6 N / 500 mm = 4000 N/mm
_u1, _u2 = 0.13, 0.41
_s = np.linspace(0, 1, 2001)
_Ue_int = 0.5 * np.trapz(np.full_like(_s, EA_num * ((_u2 - _u1) / l_num) ** 2 * l_num), _s)
assert np.isclose(_Ue_int, 0.5 * EA_num / l_num * (_u2 - _u1) ** 2)  # integral of ds over 0..1 is 1
_K = np.array([[1, -1], [-1, 1]])
_uv = np.array([_u1, _u2])
assert np.allclose(_K @ _uv, [_u1 - _u2, -_u1 + _u2])           # matrix times column
assert np.isclose(_uv @ _K @ _uv, (_u2 - _u1) ** 2)              # row times that
assert np.isclose((_u2 - _u1) ** 2, _u1 ** 2 - 2 * _u1 * _u2 + _u2 ** 2)
assert np.allclose(_K.sum(axis=1), 0)                             # rows sum to zero

SQ = {"{u_1}^2": SKY, "{u_2}^2": SKY}
EQ_SIZE = 52
ENT = 50


def rowvec():
    return Matrix([["u_1", "u_2"]], element_to_mobject=lambda s: E(s, size=ENT), h_buff=1.05)


def colvec(entries):
    return Matrix([[a] for a in entries], element_to_mobject=lambda s: E(s, size=ENT),
                  left_bracket="\\{", right_bracket="\\}", v_buff=0.85)


def kmat(color=INK):
    return Matrix([["1", "-1"], ["-1", "1"]], element_to_mobject=lambda s: M(s, size=ENT, color=color),
                  h_buff=1.15, v_buff=0.85)


class S35_Element_K(VScene):
    budget = 247

    def regroup(self, g):
        """Make g one top-level mobject again (after part-wise morphs/transforms)."""
        self.remove(*g.get_family())
        self.add(g)

    def construct(self):
        # ---- beat 1: U_e in x, then in s -------------------------------------------------------------
        eqA = E(r"U_e|=|\frac12\int_{x_1}^{x_2}|EA|\,\varepsilon^2|\,dx", size=EQ_SIZE).move_to(UP * 1.3)
        paint(eqA, {4: ACCENT})
        eqB = E(r"U_e|=|\frac12\int_0^1|EA|\Big(\frac{u_2-u_1}{l}\Big)^2|\,l\,d|s", size=EQ_SIZE).move_to(UP * 1.3)
        tint(eqB[4], [((1, 3), SKY), ((4, 6), SKY)])
        n1 = E(r"\varepsilon|=|\frac{u_2-u_1}{l}", size=44)
        tint(n1[2], [((0, 2), SKY), ((3, 5), SKY)])
        n2 = E(r"dx|=|l\,d|s|,\qquad|0\le|s|\le 1", size=44)
        notes1 = VGroup(n1, n2).arrange(RIGHT, buff=1.4).move_to(DOWN * 1.3)
        self.beat("Now the strain energy of one element: one half, the integral of E A times strain squared, d x. "
                  "Change to s: d x is l d s, and s runs from zero to one.",
                  Write(eqA), .05, FadeIn(n1, shift=.2 * UP), FadeIn(n2, shift=.2 * UP),
                  morph(eqA, eqB, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]), .2,
                  w=(.25, .13, .13, .24))
        self.regroup(eqB)

        # ---- beat 2: constants out, integral of ds is one ----------------------------------------------
        eqC = E(r"U_e|=|\frac12|\frac{EA}{l}|(|u_2|-|u_1|)^2", size=EQ_SIZE).move_to(UP * 1.3)
        n3 = E(r"\int_0^1 d|s|=|1", size=44)
        n4 = E(r"\frac{l}{l^2}|=|\frac{1}{l}", size=44)
        notes2 = VGroup(n3, n4).arrange(RIGHT, buff=2.2).move_to(DOWN * 1.3)
        self.beat("Everything inside is constant, and the integral of d s from zero to one is one. "
                  "So U e is one half, E A over l, times u two minus u one, squared.",
                  FadeOut(notes1), [Circumscribe(eqB[3], color=INK2), Circumscribe(eqB[4], color=INK2)],
                  FadeIn(n3, shift=.2 * UP), FadeIn(n4, shift=.2 * UP),
                  morph(eqB, eqC, [(0, 0), (1, 1), (2, 2), (3, 3)]), .23,
                  w=(.08, .17, .12, .12, .28))
        self.regroup(eqC)

        # ---- beat 3: it's a spring ------------------------------------------------------------------
        xa, xb, yb = -4.5, 4.5, -0.45
        pa, pb = np.array([xa, yb, 0]), np.array([xb, yb, 0])
        elem = bar(xa, xb, y=yb, h=0.62)
        na, nb = node(pa, r=0.13).set_z_index(3), node(pb, r=0.13).set_z_index(3)
        tag = T("one element", size=38, color=INK2).next_to(elem, UP, buff=0.4)
        da = disp(pa, label="u_1", length=1.2, below=0.8, size=44)
        db = disp(pb, label="u_2", length=1.2, below=0.8, size=44)
        spr = spring(pa, pb, coils=7, amp=0.4)
        klab = E(r"k|=|\frac{EA}{l}", size=48).next_to(spr, UP, buff=0.35)
        paint(klab, {2: LILAC})
        stretch = E(r"\text{stretch}|=|u_2|-|u_1|", size=44).move_to(DOWN * 3.15)
        self.beat("Pay close attention, because you've seen this before. It's a spring! An element of a bar behaves "
                  "exactly like a spring with stiffness E A over l, stretched by u two minus u one.",
                  [FadeOut(notes2), eqC.animate.move_to(UP * 2.65)],
                  self.spotlight(eqC),
                  [FadeIn(elem), FadeIn(na), FadeIn(nb), FadeIn(tag), FadeIn(da), FadeIn(db)], .05,
                  [ReplacementTransform(elem, spr), FadeOut(tag)],
                  [TransformFromCopy(eqC[3], klab[2]), FadeIn(klab[0]), FadeIn(klab[1])],
                  [TransformFromCopy(VGroup(eqC[5], eqC[6], eqC[7]), VGroup(stretch[2], stretch[3], stretch[4])),
                   FadeIn(stretch[0]), FadeIn(stretch[1])], .29,
                  w=(.08, .1, .1, .14, .12, .12), style="slower and deliberate, stressing the key words")
        self.regroup(klab)
        self.regroup(stretch)

        # ---- beat 4: expand the square --------------------------------------------------------------
        ex = E(r"(|u_2|-|u_1|)^2|=|{u_1}^2|-|2|u_1|u_2|+|{u_2}^2", size=EQ_SIZE, cmap=SQ).move_to(UP * 0.3)
        self.beat("Now write it with a matrix. Expand the square: u two minus u one, squared, is u one squared, "
                  "minus two u one u two, plus u two squared.",
                  [self.unspot(), FadeOut(VGroup(spr, na, nb, da, db, klab, stretch))],
                  TransformFromCopy(VGroup(*eqC[4:9]), VGroup(*ex[0:5])),
                  [FadeIn(ex[5]), FadeIn(ex[6], shift=.15 * UP)],
                  FadeIn(VGroup(*ex[7:11]), shift=.15 * UP),
                  FadeIn(VGroup(*ex[11:13]), shift=.15 * UP), .23,
                  w=(.12, .2, .15, .15, .15))
        self.regroup(ex)
