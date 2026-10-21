"""S10: multiplying out the third row and third column of C_PN (BRIEF.md S10)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# facts: every identity shown on screen, checked at several orientations (incl. the generic and Molniya ones)
_K = np.array([0.0, 0.0, 1.0])
for _Om, _inc, _w in [np.radians([50, 40, 60]), np.radians([145.0, 63.4, 270.0]), (0.7, 2.1, -1.3)]:
    _C = np.asarray(cpn(_Om, _inc, _w))
    assert np.allclose(_C, np.asarray(C3(_w)) @ np.asarray(C1(_inc)) @ np.asarray(C3(_Om)))
    assert np.allclose(np.asarray(C3(_w))[2], [0, 0, 1])                                 # row 3 of C3 is (0,0,1)
    assert np.allclose(_K @ np.asarray(C1(_inc)), [0, -np.sin(_inc), np.cos(_inc)])     # row 3 of C1(i)
    assert np.allclose(_C[2], [np.sin(_inc) * np.sin(_Om), -np.sin(_inc) * np.cos(_Om), np.cos(_inc)])
    assert np.allclose(np.asarray(C1(_inc)) @ _K, [0, np.sin(_inc), np.cos(_inc)])      # column 3 of C1(i)
    assert np.allclose(_C @ _K, [np.sin(_w) * np.sin(_inc), np.cos(_w) * np.sin(_inc), np.cos(_inc)])
    assert np.allclose(_C[:, 2], _C @ _K)
# picture of beat 4: generic i = 40 deg; node angle chosen so h-hat leans to screen-left (not toward the camera)
OM_G, I_G = np.radians(-45), np.radians(40)
HH = np.array([np.sin(I_G) * np.sin(OM_G), -np.sin(I_G) * np.cos(OM_G), np.cos(I_G)])
assert np.isclose(np.linalg.norm(HH), 1) and np.isclose(HH @ _K, np.cos(I_G))
assert np.isclose(np.degrees(np.arccos(HH @ _K)), 40)

XL = -1.9          # left edge of the right-hand algebra column


def reason(tex_sentence, line):
    """Grey reason under the right end of a step."""
    r = TX(tex_sentence, size=32).set_color(INK2)   # never scaled after this
    r.next_to(line, DOWN, buff=.12).align_to(line, RIGHT)
    return r


def left_at(m, y):
    m.move_to([0, y, 0]).align_to([XL, 0, 0], LEFT)
    fit(m, 6.9 - XL, 1.2)
    return m.align_to([XL, 0, 0], LEFT)


def under_eq(m, ref_eq, y):
    """Place m at height y with its '=' (part 0) under ref_eq's '=' (part 1)."""
    m.move_to([0, y, 0])
    m.shift((ref_eq[1].get_x() - m[0].get_x()) * RIGHT)
    if m.get_right()[0] > 6.9:
        m.shift((6.9 - m.get_right()[0]) * RIGHT)
    return m


class S10_Multiply(VScene):
    budget = 126

    def construct(self):
        # ---- left column: the product and the matrix of entries
        P = E(r"C_{PN}|=|C_3(|\omega|)\,C_1(|i|)\,C_3(|\Omega|)", size=40)
        fit(P, 4.6, 1).move_to([-4.45, 3.1, 0])
        Mx = Matrix([[f"C_{{{r}{c}}}" for c in (1, 2, 3)] for r in (1, 2, 3)], h_buff=1.15, v_buff=1.0,
                    element_to_mobject_config={"font_size": 42})
        Mx.set_color(INK).move_to([-4.55, 0.2, 0])
        fit(Mx, 4.0, 3.6)
        rows = Mx.get_rows()
        labs = VGroup(*[E(t, size=40).move_to([Mx.get_left()[0] - .45, rows[k].get_y(), 0])
                        for k, t in enumerate([r"\hat p", r"\hat q", r"\hat h"])])
        rowbox = SurroundingRectangle(rows[2], color=LILAC, buff=.12)

        self.beat("We don't need all nine entries. Start with the third row, which is h hat.",
                  [FadeIn(P), FadeIn(Mx), FadeIn(labs)], .15, Create(rowbox), Indicate(labs[2], color=LILAC),
                  w=(.45, .3, .25))

        # ---- third row
        L1 = left_at(E(r"\text{row}_3\,C_{PN}|=|(0,0,1)\,C_1(|i|)\,C_3(|\Omega|)", size=44), 2.5)
        R1 = reason(r"row 3 of $C_3(\omega)$ is $(0,0,1)$", L1)
        L2 = under_eq(E(r"=|(0,\,-\sin|i|,|\cos|i|)\,C_3(|\Omega|)", size=44), L1, 0.4)
        R2 = reason(r"row 3 of $C_1(i)$", L2)
        self.beat("The third row of C three of omega is just zero, zero, one. So the third row of the whole product is the third row of C one of i, times C three of Omega.",
                  Indicate(P[2:5], color=MINT), [Write(L1), FadeIn(R1)], .1, [Write(L2), FadeIn(R2)],
                  w=(.2, .38, .42))

        L3 = under_eq(E(r"=|(\sin|i|\sin|\Omega|,\ -\sin|i|\cos|\Omega|,|\cos|i|)", size=44), L1, -1.7)
        R3 = reason("row times matrix", L3)
        box3 = SurroundingRectangle(L3[1:], color=LILAC, buff=.12)
        self.beat("Multiply that row into C three of Omega. The result is sine i sine Omega, minus sine i cosine Omega, and cosine i.",
                  Indicate(L2[-2:], color=SKY), [Write(L3), FadeIn(R3)], Create(box3), w=(.25, .55, .2))

        # ---- picture check: h-hat leans from K by i
        view = View(elev=18, azim=-52, scale=1.85, center=(-4.4, -1.45))
        ax = axes3(view, 1.9)
        eq_plane = disc3(view, [1, 0, 0], [0, 1, 0], 1.35, INK2, .08)
        hvec = arrow3(view, [0, 0, 0], 1.8 * HH, LILAC)
        hlab = label3(view, r"\hat h", 2.05 * HH, LILAC, 34)
        axis = np.cross(_K, HH)
        axis = axis / np.linalg.norm(axis)
        iarc = arc3(view, axis, _K, I_G, 1.0, EMBER)
        mid = (_K + HH) / np.linalg.norm(_K + HH)
        ilab = label3(view, "i", 1.25 * mid, EMBER, 34)
        foot = 1.8 * np.cos(I_G) * _K
        proj = line3(view, 1.8 * HH, foot, LILAC, dashed=True)
        kseg = Line(view.p([0, 0, 0]), view.p(foot), color=LILAC, stroke_width=7)
        fdot = Dot(view.p(foot), radius=.06, color=LILAC)
        clab = E(r"\cos|i", size=32).next_to(view.p(.5 * foot), RIGHT, buff=.2)
        pic = VGroup(eq_plane, ax, hvec, hlab, iarc, ilab, proj, kseg, fdot, clab)
        self.beat("Check it with the picture. h hat leans away from K by the angle i, so its K component is cosine i.",
                  [FadeOut(Mx), FadeOut(labs), FadeOut(rowbox)], [FadeIn(eq_plane), FadeIn(ax)],
                  [FadeIn(hvec), FadeIn(hlab)], [FadeIn(iarc), FadeIn(ilab)],
                  [Create(proj), FadeIn(fdot), Create(kseg), FadeIn(clab)], Indicate(L3[10:12], color=LILAC),
                  w=(.1, .15, .15, .2, .2, .2))

        # ---- third column
        L3f = left_at(E(r"\text{row}_3\,C_{PN}|=|(\sin|i|\sin|\Omega|,\ -\sin|i|\cos|\Omega|,|\cos|i|)",
                        size=44), 2.95)
        box3f = SurroundingRectangle(L3f[2:], color=LILAC, buff=.12)
        colbox = SurroundingRectangle(Mx.get_columns()[2], color=INK2, buff=.12)
        L4 = left_at(E(r"C_{PN}\,\hat K|=|C_3(|\omega|)\,C_1(|i|)\,(0,0,1)^{T}", size=44), 1.7)
        R4 = reason(r"$\hat K$ picks out column 3", L4)
        L5 = under_eq(E(r"=|C_3(|\omega|)\,(0,|\sin|i|,|\cos|i|)^{T}", size=44), L4, 0.45)
        R5 = reason(r"column 3 of $C_1(i)$", L5)
        with self.say("Now the third column. Multiply C P N by the unit vector along K, working from the right.") as d:
            self.play(FadeOut(pic), FadeOut(L1), FadeOut(R1), FadeOut(L2), FadeOut(R2), FadeOut(R3),
                      *morph(L3, L3f, [(k, k + 1) for k in range(len(L3))]), ReplacementTransform(box3, box3f),
                      run_time=.25 * d)
            self.play(FadeIn(Mx), FadeIn(labs), Create(colbox), run_time=.2 * d)
            self.play(Write(L4), FadeIn(R4), run_time=.25 * d)
            self.play(Write(L5), FadeIn(R5), run_time=.25 * d)
            self.wait(.05 * d)

        L6 = under_eq(E(r"=|(\sin|\omega|\sin|i|,\ \cos|\omega|\sin|i|,|\cos|i|)^{T}", size=44), L4, -0.8)
        R6 = reason("matrix times column", L6)
        box6 = SurroundingRectangle(L6[1:], color=INK2, buff=.12)

        heads = [r"C_{31}", r"C_{32}", r"C_{33}", r"C_{13}", r"C_{23}"]
        vals = [r"\sin|i|\sin|\Omega|", r"-\sin|i|\cos|\Omega|", r"\cos|i|", r"\sin|\omega|\sin|i|",
                r"\cos|\omega|\sin|i|"]
        cols = VGroup(*[VGroup(E(h, size=38).set_color(INK2), E(v, size=42)).arrange(DOWN, buff=.4)
                        for h, v in zip(heads, vals)]).arrange(RIGHT, buff=.7)
        for c in cols:                                     # common baselines for both table rows
            c[0].set_y(cols[0][0].get_y())
            c[1].set_y(cols[0][1].get_y())
        rule = Line(cols.get_left() + LEFT * .2, cols.get_right() + RIGHT * .2, color=HAIR, stroke_width=2)
        rule.set_y((cols[0][0].get_bottom()[1] + cols[0][1].get_top()[1]) / 2)
        table = panel(VGroup(cols, rule))
        fit(table, 13.8, 2.1).move_to([0, -2.85, 0])
        self.beat("That gives sine omega sine i, cosine omega sine i, and cosine i.",
                  [Write(L6), FadeIn(R6)], Create(box6), FadeIn(table, shift=UP * .2), w=(.45, .15, .4))
        self.wait(1.0)
        self.wipe()
