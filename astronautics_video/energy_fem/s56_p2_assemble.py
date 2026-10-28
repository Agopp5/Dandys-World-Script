"""S56: HW P2 part a, assemble the global K and F (BRIEF.md S56)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# ---- facts (HW P2): every number on screen, derived here ----
E_MOD, AREA, LEN = 10e3, 2.0, 40.0
EA = E_MOD * AREA
assert np.isclose(EA, 20000)
L_EL = LEN / 2                                   # two elements of 20 in
K_EL = EA / L_EL
assert np.isclose(K_EL, 1000)                    # "two blocks of one thousand"
C_F = -5.0                                       # f = 5 lb/in pointing left
SHARE = C_F * L_EL / 2
assert np.isclose(SHARE, -50)                    # c l / 2 to each node of each element
P1, P2 = 50.0, 100.0
ke = K_EL * np.array([[1, -1], [-1, 1]])
KG = np.zeros((3, 3))
FG = np.zeros(3)
for e in range(2):                               # element e joins nodes e, e+1
    KG[e:e + 2, e:e + 2] += ke
    FG[e:e + 2] += SHARE
FG += [0, P1, P2]                                # node 0 also gets + R
assert np.allclose(KG, 1000 * np.array([[1, -1, 0], [-1, 2, -1], [0, -1, 1]]))
assert np.isclose(1 + 1, 2) and np.isclose(KG[1, 1], 2000)
assert np.allclose(FG, [-50, -50, 50])           # F = {R - 50, -50, 50}
assert np.isclose(-50 - 50 + 50, -50) and np.isclose(-50 + 100, 50)

# ---- the homework bar, drawn as in S54 (shifted up to make room for K and F) ----
X0, X1 = -6.0, 4.4
BY, BH = 1.75, 0.6


def sx(x_in):
    return X0 + (X1 - X0) * x_in / LEN


XN = [sx(0), sx(20), sx(40)]
assert np.isclose(XN[1], -0.8)
MID1, MID2 = (XN[0] + XN[1]) / 2, (XN[1] + XN[2]) / 2
RING_Y = BY - BH / 2 - 0.6
WORK_Y = RING_Y - 0.66


def span_rect(a, b, color, opacity, stroke=0):
    r = Rectangle(width=b - a, height=BH).move_to(((a + b) / 2, BY, 0))
    return r.set_fill(color, opacity).set_stroke(color, stroke)


def clamp(m, lo=-6.85, hi=6.85):
    if m.get_left()[0] < lo:
        m.shift((lo - m.get_left()[0]) * RIGHT)
    if m.get_right()[0] > hi:
        m.shift((hi - m.get_right()[0]) * RIGHT)
    return m


def mat(rows, color, size=48, **kw):
    return Matrix(rows, element_to_mobject=lambda s: M(s, size=size, color=color),
                  v_buff=0.85, **kw)


class S56_P2_Assemble(VScene):
    budget = 128

    def construct(self):
        # ---------- figure ----------
        wall_m = wall((X0, BY, 0), side=LEFT, h=1.0)
        bar_m = bar(X0, X1, y=BY, h=BH)
        fl = dist_load(X0 + 0.5, X1 - 0.05, BY, n=15, d=LEFT, color=ROSE)
        flab = M(r"f = 5\ \text{lb/in}", size=36, color=ROSE).move_to((MID1, BY + BH / 2 + 0.42, 0))
        p1a = force((XN[1], BY + BH / 2 + 0.32, 0), d=RIGHT, length=1.0)
        p1l = M(r"P_1 = 50\ \text{lb}", size=36, color=ROSE).next_to(p1a, UP, buff=0.12)
        p2a = force((X1, BY, 0), d=RIGHT, length=1.1)
        p2l = M(r"P_2 = 100\ \text{lb}", size=36, color=ROSE).next_to(p2a, UP, buff=0.42)
        clamp(p2l)
        dots = VGroup(*[node((x, BY, 0)) for x in XN])
        rings = VGroup()
        for i, x in enumerate(XN):
            c = Circle(radius=0.3).set_stroke(INK2, 3).move_to((x, RING_Y, 0))
            rings.add(VGroup(c, M(str(i), size=36, color=INK).move_to(c)))
        elabs = VGroup(T("element 1", size=36, color=INK2).move_to((MID1, RING_Y, 0)),
                       T("element 2", size=36, color=INK2).move_to((MID2, RING_Y, 0)))

        # element highlights (solid = element 1, dashed = element 2, same as their blocks in K)
        el1 = span_rect(XN[0], XN[1], LILAC, 0.28, stroke=6)
        el2_fill = span_rect(XN[1], XN[2], LILAC, 0.28)
        el2 = VGroup(el2_fill, DashedVMobject(span_rect(XN[1], XN[2], LILAC, 0, stroke=6), num_dashes=40))
        # each node's share of the spread load: half of each neighbouring element
        shares = [span_rect(XN[0], MID1, ROSE, 0.35), span_rect(MID1, MID2, ROSE, 0.35),
                  span_rect(MID2, XN[2], ROSE, 0.35)]

        def arrows_in(a, b):
            return VGroup(*[ar for ar in fl if a <= ar.get_center()[0] <= b])

        # node-by-node load sums, written under each ring
        w0 = E(r"-50|+|R", size=36).set_color(ROSE)
        w1 = E(r"-50|-50|+50|=|-50", size=36).set_color(ROSE)
        w2 = E(r"-50|+100|=|50", size=36).set_color(ROSE)
        for w, x in zip((w0, w1, w2), XN):
            w.move_to((x, WORK_Y, 0))
            clamp(w)
        for w in (w1, w2):
            paint(w, {len(w) - 2: INK})

        # ---------- K and F ----------
        Kmat = mat([["1", "-1", "0"], ["-1", "2", "-1"], ["0", "-1", "1"]], LILAC, h_buff=1.25)
        Klhs = E(r"K|=|1000", size=48)
        Klhs[2].set_color(LILAC)
        Kunit = M(r"\text{lb/in}", size=36, color=INK2)
        Klhs.next_to(Kmat, LEFT, buff=0.25)
        Kunit.next_to(Kmat, RIGHT, buff=0.25)
        Kgrp = VGroup(Klhs, Kmat, Kunit)
        Fmat = mat([["R - 50"], ["-50"], ["50"]], ROSE, left_bracket=r"\{", right_bracket=r"\}")
        Flhs = E(r"F|=", size=48)
        Funit = M(r"\text{lb}", size=36, color=INK2)
        Flhs.next_to(Fmat, LEFT, buff=0.25)
        Funit.next_to(Fmat, RIGHT, buff=0.25)
        Fgrp = VGroup(Flhs, Fmat, Funit)
        row = VGroup(Kgrp, Fgrp).arrange(RIGHT, buff=1.0).move_to((0, -1.95, 0))
        fit(row, 13.6, 3.2)
        ents = Kmat.get_entries()

        def ent(i, j):
            return ents[3 * i + j]

        cols = VGroup(*[M(str(j), size=36, color=MUTED).next_to(Kmat.get_columns()[j], UP, buff=0.42)
                        .set_x(Kmat.get_columns()[j].get_x()) for j in range(3)])
        box1 = SurroundingRectangle(VGroup(ent(0, 0), ent(0, 1), ent(1, 0), ent(1, 1)), buff=0.14,
                                    color=LILAC, stroke_width=4)
        box2 = DashedVMobject(SurroundingRectangle(VGroup(ent(1, 1), ent(1, 2), ent(2, 1), ent(2, 2)),
                                                   buff=0.24, color=LILAC, stroke_width=4), num_dashes=36)
        one11 = M("1", size=48, color=LILAC).move_to(ent(1, 1))
        onep1 = M("1 + 1", size=48, color=LILAC).move_to(ent(1, 1))
        fents = Fmat.get_entries()

        # ---------- beat 1: the bar, then the checkpoint ----------
        self.section("HW P2, part a: assemble K and F")
        self.beat("Your turn first: pause and do checkpoint eight point one in your guide, and assemble K and F.",
                  [FadeIn(wall_m), Create(bar_m)],
                  [FadeIn(dots), FadeIn(rings), FadeIn(elabs)],
                  [FadeIn(fl, lag_ratio=0.1), FadeIn(flab)],
                  [GrowArrow(p1a) if isinstance(p1a, Arrow) else FadeIn(p1a), FadeIn(p1l),
                   GrowArrow(p2a) if isinstance(p2a, Arrow) else FadeIn(p2a), FadeIn(p2l)],
                  w=(.25, .25, .25, .25))
        self.checkpoint("8.1", "HW 2: assemble the global K and F")

        # ---------- beat 2: two blocks drop in, overlap at node 1 ----------
        with self.say("Stiffness: two blocks of one thousand. They overlap at node one, where one plus one "
                      "gives two. So K is one thousand times one, minus one, zero; minus one, two, minus one; "
                      "zero, minus one, one.") as d:
            self.play(FadeIn(Klhs), FadeIn(Kmat.get_brackets()), FadeIn(cols), run_time=.06 * d)
            self.play(FadeIn(el1), Create(box1),
                      *[FadeIn(m, shift=.5 * DOWN) for m in (ent(0, 0), ent(0, 1), ent(1, 0), one11)],
                      run_time=.14 * d)
            self.play(FadeIn(el2), Create(box2),
                      *[FadeIn(m, shift=.5 * DOWN) for m in (ent(1, 2), ent(2, 1), ent(2, 2))],
                      FadeTransform(one11, onep1), run_time=.12 * d)
            self.wait(.04 * d)
            self.play(Indicate(rings[1], color=INK), Indicate(cols[1], color=INK), run_time=.05 * d)
            hal = glow(ent(1, 1), LILAC)
            self.play(ReplacementTransform(onep1, ent(1, 1)), FadeIn(hal), run_time=.06 * d)
            self.play(FadeIn(ent(0, 2)), FadeIn(ent(2, 0)), FadeIn(Kunit),
                      FadeOut(box1), FadeOut(box2), FadeOut(el1), FadeOut(el2), run_time=.06 * d)
            self.wait(.04 * d)
            for r in range(3):
                self.play(Indicate(Kmat.get_rows()[r], color=INK, scale_factor=1.15), run_time=.12 * d)
                self.wait(.02 * d)
            self.play(FadeOut(hal), run_time=.03 * d)

        # ---------- beat 3: node 0 ----------
        with self.say("Loads, node by node. Node zero: minus fifty from element one, plus the reaction R. "
                      "The wall node still gets its share of the spread load; the wall then has to hold it.") as d:
            self.play(FadeIn(Flhs), FadeIn(Fmat.get_brackets()), FadeIn(Funit), run_time=.07 * d)
            self.play(Indicate(rings[0], color=INK), run_time=.06 * d)
            self.play(FadeIn(shares[0]), Indicate(arrows_in(XN[0], MID1), color=ROSE, scale_factor=1.3),
                      Write(w0[0]), run_time=.14 * d)
            self.wait(.06 * d)
            self.play(Write(w0[1:]), run_time=.08 * d)
            self.play(ReplacementTransform(w0.copy(), fents[0]), run_time=.1 * d)
            self.wait(.09 * d)
            self.play(Circumscribe(shares[0], color=ROSE), run_time=.14 * d)
            self.play(Wiggle(wall_m), run_time=.12 * d)

        # ---------- beat 4: nodes 1 and 2 ----------
        with self.say("Node one: minus fifty from each element, plus P one, fifty. That's minus fifty. "
                      "Node two: minus fifty from element two, plus P two, one hundred. That's fifty.") as d:
            self.play(FadeOut(shares[0]), FadeIn(shares[1]), Indicate(rings[1], color=INK), run_time=.05 * d)
            self.play(Write(w1[0]), Write(w1[1]), Indicate(arrows_in(MID1, MID2), color=ROSE, scale_factor=1.3),
                      run_time=.1 * d)
            self.play(Write(w1[2]), Indicate(VGroup(p1a, p1l), color=ROSE), run_time=.09 * d)
            self.play(Write(w1[3:]), run_time=.06 * d)
            self.play(ReplacementTransform(w1[4].copy(), fents[1]), run_time=.07 * d)
            self.wait(.05 * d)
            self.play(FadeOut(shares[1]), FadeIn(shares[2]), Indicate(rings[2], color=INK), run_time=.05 * d)
            self.play(Write(w2[0]), Indicate(arrows_in(MID2, XN[2]), color=ROSE, scale_factor=1.3),
                      run_time=.1 * d)
            self.play(Write(w2[1]), Indicate(VGroup(p2a, p2l), color=ROSE), run_time=.1 * d)
            self.play(Write(w2[2:]), run_time=.06 * d)
            self.play(ReplacementTransform(w2[3].copy(), fents[2]), run_time=.07 * d)
            self.play(FadeOut(shares[2]), run_time=.04 * d)

        # ---------- beat 5: F boxed beside K, part a ----------
        fbox = SurroundingRectangle(Fgrp, buff=0.2, color=GOOD, stroke_width=4)
        tag_t = T("part a", size=36, color=GOOD)
        tag = VGroup(RoundedRectangle(width=tag_t.width + 0.4, height=tag_t.height + 0.26, corner_radius=0.12)
                     .set_stroke(GOOD, 3).set_fill(BG, 1), tag_t)
        tag.next_to(fbox, UP, buff=0.12)
        with self.say("So F is R minus fifty, minus fifty, and fifty. That's part a.") as d:
            for i in range(3):
                self.play(Indicate(fents[i], color=INK, scale_factor=1.2), run_time=.15 * d)
            self.play(FadeOut(VGroup(w0, w1, w2)), run_time=.05 * d)   # the sums now live in F
            self.play(Create(fbox), FadeIn(tag, shift=.2 * DOWN), run_time=.2 * d)
            self.wait(.3 * d)
        self.wipe()
