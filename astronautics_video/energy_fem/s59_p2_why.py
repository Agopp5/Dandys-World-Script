"""S59: why point 1 doesn't move (BRIEF.md S59)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# ---------------- facts (HW P2), asserted before any animation ----------------
E_MOD, AREA, L_BAR = 10e3, 2.0, 40.0          # psi, in^2, in
EA = E_MOD * AREA
P1, P2, F_LOAD = 50.0, 100.0, 5.0             # lb, lb, lb/in (f points LEFT)
assert np.isclose(EA, 20000)
assert P1 + P2 == 150 and F_LOAD * L_BAR == 200 and F_LOAD * (L_BAR - 20) == 100


def N_int(x):
    """internal force (tension +) = sum of the loads on the piece to the right of x"""
    return (P1 if x < 20 else 0.0) + P2 - F_LOAD * (L_BAR - x)


assert np.isclose(N_int(0), -50) and np.isclose(N_int(20 - 1e-9), 50) and np.isclose(N_int(10), 0)
_xs = np.linspace(0, 19.99, 400)
assert np.allclose([N_int(x) for x in _xs], -50 + 5 * _xs)          # left half: N = -50 + 5x
A_NEG, A_POS = 0.5 * 10 * N_int(0), 0.5 * 10 * N_int(20 - 1e-12)   # triangles 0..10 and 10..20
assert np.isclose(A_NEG, -250) and np.isclose(A_POS, 250) and np.isclose(A_NEG + A_POS, 0)


def u_left(x):
    """exact u(x) on the left half: integral from 0 to x of N / EA"""
    return (-50 * x + 2.5 * x ** 2) / EA


_xq = np.linspace(0, 10, 10001)
_Nq = -50 + 5 * _xq
assert np.isclose(np.sum((_Nq[1:] + _Nq[:-1]) / 2 * np.diff(_xq)) / EA, u_left(10))   # trapezoid (exact for a line)
assert np.isclose(u_left(10), -250 / 20000) and np.isclose(u_left(10), -0.0125) and np.isclose(u_left(20), 0)
assert all(u_left(x) <= 0 for x in np.linspace(0, 20, 81))          # the left half dips, never rises


def fem(ne):
    """ne equal linear elements, consistent load vector c l / 2, node 0 fixed"""
    l = L_BAR / ne
    k = EA / l
    K = np.zeros((ne + 1, ne + 1))
    F = np.zeros(ne + 1)
    for e in range(ne):
        K[e:e + 2, e:e + 2] += k * np.array([[1, -1], [-1, 1]])
        F[e:e + 2] += -F_LOAD * l / 2
    F[ne // 2] += P1
    F[ne] += P2
    q = np.zeros(ne + 1)
    q[1:] = np.linalg.solve(K[1:, 1:], F[1:])
    return q


Q2, Q4 = fem(2), fem(4)
assert np.allclose(Q2, [0, 0, 0.05])                                  # two elements: q1 = 0, q2 = 0.05 in
assert np.allclose(Q4[:3], [0, u_left(10), u_left(20)])               # four elements: node at x = 10 is exact

# ---------------- layout ----------------
X0, SC = -5.8, 0.26            # wall face; screen units per inch (bar 40 in -> 10.4 units)
YB, BH = -2.05, 0.6            # bar centre line, bar height
Y0, SYN = 0.75, 3.2 / 120      # plot zero line; screen units per lb (plot spans -60..60 lb)
U2N = 50 / 0.0125              # u plot: -0.0125 in sits where -50 lb sat
S_EXAG = 0.65 / 0.0125         # bar deformation drawn exaggerated: 0.65 units for 0.0125 in
XR = 3.6                       # right column centre


def XL(x):
    return X0 + SC * x


def pN(x, n):
    return np.array([XL(x), Y0 + SYN * n, 0])


def pU(x, u):
    return pN(x, U2N * u)


class S59_P2_Why(VScene):
    budget = 281

    def construct(self):
        t1, t2 = ValueTracker(0), ValueTracker(0)

        def D(x):
            """exaggerated screen displacement of material point x: stage 1 shortens 0..10, stage 2 stretches 10..20"""
            xa, xb = min(x, 10.0), min(max(x, 10.0), 20.0)
            return S_EXAG * (t1.get_value() * u_left(xa) + t2.get_value() * (u_left(xb) - u_left(10.0)))

        # ---------- the shared homework bar (S54-S58), on this scene's x scale ----------
        hb = hw2_bar(y=YB, x0=X0, x1=XL(40), h=BH)
        assert np.isclose(hb.X(10), XL(10)) and np.isclose(hb.X(40), XL(40))
        fl, tags, tag3 = hb.farr, hb.rings, hb.ring3
        p1g, p2 = hb.P1.set_z_index(7), hb.P2
        p1 = p1g[0]
        p1g.d_last = 0.0

        def follow(m):
            dd = D(20)
            m.shift((dd - m.d_last) * RIGHT)
            m.d_last = dd
        p1g.add_updater(follow)
        dot1, tick3 = hb.nodes[1], hb.tick3
        n1 = always_redraw(lambda: dot1.copy().move_to([XL(20) + D(20), YB, 0]).set_z_index(4))
        p3 = always_redraw(lambda: tick3.copy().move_to([XL(10) + D(10), YB, 0]).set_z_index(3))
        fig = VGroup(hb.wall, hb.bar, fl, hb.flab, p2, hb.nodes[0], hb.nodes[2], tags, tag3)

        # ---------- the cut ----------
        def shade_at(xc):
            r = Rectangle(width=XL(xc) - (X0 - 0.5), height=1.75, stroke_width=0, fill_color=BG, fill_opacity=0.72)
            return r.move_to([(XL(xc) + X0 - 0.5) / 2, YB - 0.05, 0]).set_z_index(5)

        def box_at(xc):
            x1, x2 = XL(xc) + 0.07, XL(40) + 1.2
            r = RoundedRectangle(corner_radius=0.12, width=x2 - x1, height=1.23, stroke_color=ROSE, stroke_width=3,
                                 fill_color=ROSE, fill_opacity=0.07)
            return r.move_to([(x1 + x2) / 2, YB - 0.235, 0]).set_z_index(1)

        def cut_at(xc):
            return DashedLine([XL(xc), YB - 0.75, 0], [XL(xc), YB + 0.36, 0], color=INK, stroke_width=4,
                              dash_length=0.1).set_z_index(6)

        def right_of(xc):
            return VGroup(*[a for a in fl if a.get_center()[0] > XL(xc)])

        xc1 = 13.0
        cut, shade, box = cut_at(xc1), shade_at(xc1), box_at(xc1)
        narr = Arrow([XL(xc1), YB, 0], [XL(xc1) - 0.9, YB, 0], buff=0, color=ACCENT, stroke_width=6,
                     max_tip_length_to_length_ratio=0.3).set_z_index(6)
        nlab = M("N", size=40, color=ACCENT).next_to(narr, UP, buff=0.32).set_z_index(6)
        deflab = E(r"N(x)|=|\text{sum of loads to the right}", size=44, cmap={"N(x)": ACCENT})
        fit(deflab, 6.4, 1.0)
        deflab.move_to([XR, 2.85, 0])
        tens = T("(tension positive)", size=36, color=INK2).next_to(deflab, DOWN, buff=0.18)

        # ---------- beat 1 ----------
        with self.say("Now, why does point one stay put? Cut the bar anywhere. The force inside the bar at the cut, "
                      "call it N, tension positive, must balance all the loads on the piece to the right of the cut.") as d:
            self.section("Why point 1 doesn't move")
            self.play(FadeIn(fig), FadeIn(p1g), FadeIn(n1), FadeIn(p3), run_time=.12 * d)
            self.play(Indicate(tags[1], color=ACCENT, scale_factor=1.3), run_time=.06 * d)
            self.play(Create(cut), run_time=.05 * d)
            self.play(FadeIn(shade), FadeIn(box), run_time=.07 * d)
            self.play(GrowArrow(narr), FadeIn(nlab), run_time=.08 * d)
            self.play(Write(deflab), run_time=.12 * d)
            self.play(FadeIn(tens), run_time=.05 * d)
            self.play(Indicate(VGroup(p1, p2[0], right_of(xc1)), color=INK), run_time=.12 * d)

        # ---------- the N(x) plot, above the left half of the bar (same x scale) ----------
        xax = Line(pN(0, 0), pN(21, 0), color=AXIS, stroke_width=3)
        yax = Line(pN(0, -60), pN(0, 60), color=AXIS, stroke_width=3)
        xt = VGroup(*[Line(pN(x, 0) + .08 * DOWN, pN(x, 0) + .08 * UP, color=AXIS, stroke_width=3) for x in (10, 20)])
        yt = VGroup(*[Line(pN(0, n) + .08 * LEFT, pN(0, n) + .08 * RIGHT, color=AXIS, stroke_width=3)
                      for n in (-50, 50)])
        ylabN = E(r"N|\ (\text{lb})", size=40, cmap={"N": ACCENT}).next_to(pN(0, 60), UP, buff=0.12)
        xlab = E(r"x|\ (\text{in})", size=40).next_to(pN(21, 0), RIGHT, buff=0.15)
        lab_m50 = M("-50", size=36).next_to(pN(0, -50), LEFT, buff=0.15)
        lab_p50 = M("50", size=36).next_to(pN(0, 50), LEFT, buff=0.15)
        lab10 = M("10", size=36).next_to(pN(10, 0), UL, buff=0.08)
        lab20 = M("20", size=36).next_to(pN(20, 0), DL, buff=0.08)
        guides = VGroup(*[DashedLine(pN(x, -60), [XL(x), YB + 0.33, 0], color=MUTED, stroke_width=2,
                                     dash_length=0.07) for x in (10, 20)])
        dot0 = Dot(pN(0, -50), radius=0.08, color=ACCENT).set_z_index(5)
        dot20 = Dot(pN(20, 50), radius=0.08, color=ACCENT).set_z_index(5)
        zdot = Dot(pN(10, 0), radius=0.08, color=ACCENT).set_z_index(5)
        nline = Line(pN(0, -50), pN(20, 50), color=ACCENT, stroke_width=5).set_z_index(3)

        eq1 = E(r"N(0)|=|150|-|200|=|-50\text{ lb}", size=48,
                cmap={"N(0)": ACCENT, "150": ROSE, "200": ROSE, r"-50\text{ lb}": ACCENT}).move_to([XR, 1.6, 0])
        comp = T("compression", size=36, color=INK2).next_to(eq1, DOWN, buff=0.16)
        eq2 = E(r"N(20^-)|=|150|-|100|=|+50\text{ lb}", size=48,
                cmap={"N(20^-)": ACCENT, "150": ROSE, "100": ROSE, r"+50\text{ lb}": ACCENT}).move_to([XR, 0.1, 0])
        tnote = T("tension", size=36, color=INK2).next_to(eq2, DOWN, buff=0.16)

        # ---------- beat 2 ----------
        x2 = 0.6
        with self.say("Cut right at the wall. To the right: fifty plus one hundred pushing right, and the whole spread "
                      "load, two hundred, pulling left. One fifty minus two hundred: N is minus fifty. Compression.") as d:
            self.play(FadeOut(narr, nlab), Transform(cut, cut_at(x2)), Transform(shade, shade_at(x2)),
                      Transform(box, box_at(x2)), run_time=.14 * d)
            self.wait(.02 * d)
            self.play(Indicate(p1, color=INK), Indicate(p2[0], color=INK), Write(eq1[0:3]), run_time=.2 * d)
            self.wait(.09 * d)
            self.play(Indicate(fl, color=INK), Write(eq1[3:5]), run_time=.16 * d)
            self.wait(.1 * d)
            self.play(Write(eq1[5:]), run_time=.1 * d)
            self.play(Create(VGroup(xax, yax, xt, yt)), FadeIn(ylabN, xlab, lab_m50, guides), FadeIn(dot0),
                      FadeIn(comp), run_time=.14 * d)

        # ---------- beat 3 ----------
        x3 = 19.5
        with self.say("Now cut just left of point one. The spread load to the right is only one hundred now. One fifty "
                      "minus one hundred: plus fifty. Tension. In between, N climbs in a straight line, and crosses "
                      "zero at x equals ten.") as d:
            self.play(Transform(cut, cut_at(x3)), Transform(shade, shade_at(x3)), Transform(box, box_at(x3)),
                      run_time=.14 * d)
            self.wait(.04 * d)
            self.play(Indicate(right_of(x3), color=INK), run_time=.12 * d)
            self.play(Write(eq2[0:5]), run_time=.14 * d)
            self.wait(.03 * d)
            self.play(Write(eq2[5:]), FadeIn(dot20), FadeIn(lab_p50), FadeIn(tnote), run_time=.12 * d)
            self.wait(.07 * d)
            self.play(Create(nline), run_time=.16 * d)
            self.play(FadeIn(zdot), FadeIn(lab10), Flash(pN(10, 0), color=ACCENT), FadeIn(lab20), run_time=.1 * d)

        # ---------- beat 4: area under N ----------
        sl_bar = Rectangle(width=1.2 * SC, height=BH, stroke_width=0, fill_color=ACCENT, fill_opacity=0.6)
        sl_bar.move_to([XL(4), YB, 0]).set_z_index(2)
        sl_dx = M("dx", size=36).next_to(sl_bar, UP, buff=0.32)
        sl_plot = Polygon(pN(3.4, 0), pN(4.6, 0), pN(4.6, N_int(4.6)), pN(3.4, N_int(3.4)), stroke_width=0,
                          fill_color=ACCENT, fill_opacity=0.6).set_z_index(2)
        eqd = E(r"d\Delta|=|\frac{N}{EA}\,dx", size=48).move_to([XR, 2.45, 0])
        eqint = E(r"\Delta_{\text{left}}|=|\frac{1}{EA}\int_0^{20} N\,dx", size=48).move_to([XR, 1.15, 0])
        eanote = M(r"EA = 20{,}000\text{ lb}", size=40, color=INK2).move_to([XR, 0.2, 0])
        sweep = ValueTracker(0.01)

        def area_upto(xe):
            a = min(xe, 10.0)
            g = VGroup(Polygon(pN(0, 0), pN(a, 0), pN(a, N_int(a)), pN(0, -50)))
            if xe > 10:
                g.add(Polygon(pN(10, 0), pN(xe, 0), pN(xe, N_int(xe))))
            return g.set_stroke(width=0).set_fill(ACCENT, opacity=0.3).set_z_index(1)
        area = always_redraw(lambda: area_upto(sweep.get_value()))
        tL = Polygon(pN(0, 0), pN(10, 0), pN(0, -50)).set_stroke(width=0).set_fill(ACCENT, opacity=0.3).set_z_index(1)
        tR = Polygon(pN(10, 0), pN(20, 0), pN(20, 50)).set_stroke(width=0).set_fill(ACCENT, opacity=0.3).set_z_index(1)
        labneg = M("-250", size=40).move_to(pN(10 / 3, -50 / 3)).set_z_index(4)
        labpos = M("+250", size=40).move_to(pN(50 / 3, 50 / 3)).set_z_index(4)
        with self.say("A slice shortens or stretches by N over E A, times its length. So the change in length of the "
                      "left half is the area under N, divided by E A. And look: the area below zero and the area "
                      "above zero are equal triangles.") as d:
            self.play(FadeOut(cut, shade, box, deflab, tens, eq1, comp, eq2, tnote), run_time=.08 * d)
            self.play(FadeIn(sl_bar), FadeIn(sl_plot), FadeIn(sl_dx), run_time=.08 * d)
            self.play(Write(eqd), run_time=.12 * d)
            self.wait(.03 * d)
            self.add(area)
            self.play(FadeOut(sl_bar, sl_plot, sl_dx), sweep.animate.set_value(20), run_time=.17 * d)
            self.play(Write(eqint), run_time=.12 * d)
            self.play(FadeIn(eanote), run_time=.06 * d)
            self.wait(.03 * d)
            self.remove(area)
            self.add(tL, tR)
            self.play(FadeIn(labneg), FadeIn(labpos), run_time=.08 * d)
            cp = tL.copy().set_fill(ACCENT, opacity=0.55).set_z_index(2)
            self.play(Rotate(cp, PI, about_point=pN(10, 0)), run_time=.12 * d)
            self.play(FadeOut(cp), run_time=.06 * d)

        # ---------- beat 5: equal and opposite, so point 1 returns ----------
        eqnum = E(r"\Delta_{\text{left}}|=|\frac{-250+250}{EA}|=|0", size=48).move_to([XR, 1.15, 0])
        mat_x = [1.25 * i for i in range(1, 16) if i != 8]
        mat = always_redraw(lambda: VGroup(*[Line([XL(x) + D(x), YB - 0.24, 0], [XL(x) + D(x), YB + 0.24, 0],
                                                   color=INK2, stroke_width=2.5) for x in mat_x]).set_z_index(2))
        exag = T("deformation exaggerated", size=30, color=MUTED).move_to([XR, -0.45, 0])
        lab_sh = T("shortens", size=36, color=INK2).move_to([XL(5), -0.95, 0])
        lab_st = T("stretches", size=36, color=INK2).move_to([XL(15.1), -0.95, 0])
        with self.say("Minus two hundred fifty plus two hundred fifty is zero. The left half shortens near the wall "
                      "and stretches near the middle by exactly the same amount, so point one ends up where it "
                      "started.") as d:
            self.play(*morph(eqint, eqnum, [(0, 0), (1, 1)]), run_time=.14 * d)
            self.play(Circumscribe(eqnum[4], color=ACCENT), run_time=.08 * d)
            self.wait(.06 * d)
            self.play(FadeIn(mat), FadeIn(exag), run_time=.06 * d)
            self.play(t1.animate.set_value(1), FadeIn(lab_sh), Indicate(labneg, color=ACCENT), run_time=.18 * d)
            self.play(t2.animate.set_value(1), FadeIn(lab_st), Indicate(labpos, color=ACCENT), run_time=.18 * d)
            self.wait(.07 * d)
            self.play(Flash(np.array([XL(20), YB, 0]), color=SKY), Indicate(tags[1], color=SKY, scale_factor=1.3),
                      run_time=.1 * d)

        # ---------- beat 6: point 3 does move; N plot becomes the exact u(x) ----------
        equ = E(r"u(10)|=|\frac{-250}{20{,}000}|=|-0.0125\text{ in}", size=48,
                cmap={"u(10)": SKY, r"-0.0125\text{ in}": SKY})
        fit(equ, 6.4, 1.3)
        equ.move_to([XR, 2.3, 0])
        barrow = Arrow([XL(10), YB + 0.45, 0], [XL(10) + S_EXAG * u_left(10), YB + 0.45, 0], buff=0, color=SKY,
                       stroke_width=5, max_tip_length_to_length_ratio=0.35).set_z_index(6)
        ucurve = VMobject(color=SKY, stroke_width=5).set_points_smoothly(
            [pU(x, u_left(x)) for x in np.linspace(0, 20, 41)]).set_z_index(3)
        ylabU = E(r"u|\ (\text{in})", size=40).next_to(pN(0, 60), UP, buff=0.12)
        udot = Dot(pU(10, u_left(10)), radius=0.09, color=SKY).set_z_index(6)
        exact_lab = T("exact", size=36, color=SKY).move_to(pU(10, u_left(10)) + 0.4 * DOWN)
        with self.say("But inside that half, the bar does move. At point three, x equals ten, the area so far is minus "
                      "two hundred fifty. Divide by twenty thousand: point three moves minus zero point zero one two "
                      "five inches, to the left.") as d:
            self.play(FadeOut(eqd, eqnum, exag, lab_sh, lab_st), Indicate(tag3, color=SKY, scale_factor=1.3),
                      run_time=.12 * d)
            self.play(GrowArrow(barrow), run_time=.08 * d)
            self.wait(.03 * d)
            self.play(Indicate(VGroup(tL, labneg), color=ACCENT), run_time=.1 * d)
            self.play(Write(equ[0:3]), run_time=.14 * d)
            self.wait(.12 * d)
            self.play(Write(equ[3:]), run_time=.1 * d)
            self.play(FadeOut(tL, tR, labneg, labpos, lab_m50, lab_p50, yt, zdot, dot0, dot20, guides),
                      Transform(nline, ucurve), FadeTransform(ylabN, ylabU),
                      lab20.animate.next_to(pN(20, 0), UP, buff=0.12), run_time=.16 * d)
            self.play(FadeIn(udot), FadeIn(exact_lab), run_time=.08 * d)

        # ---------- beat 7: the two-element model is flat there ----------
        fem2 = Line(pU(0, Q2[0]), pU(20, Q2[1]), color=LIME, stroke_width=6).set_z_index(4)
        fem4 = VMobject(color=LIME, stroke_width=6).set_points_as_corners(
            [pU(0, Q4[0]), pU(10, Q4[1]), pU(20, Q4[2])]).set_z_index(4)
        old2 = DashedLine(pU(0, 0), pU(20, 0), color=MUTED, stroke_width=4, dash_length=0.1).set_z_index(3)
        nds = VGroup(Dot(pU(0, Q2[0]), radius=0.09, color=SKY), Dot(pU(20, Q2[1]), radius=0.09, color=SKY))
        nds.set_z_index(6)
        lab2 = T("2 elements", size=36, color=LIME).move_to(pN(10, 0) + 0.78 * UP)
        lab4 = T("4 elements", size=36, color=LIME).move_to(pU(10, -0.0036))
        eqf = E(r"u_{\text{FEM}}(10)|=|0", size=48, cmap={r"u_{\text{FEM}}(10)": LIME}).move_to([XR, 1.15, 0])
        eqf2 = E(r"\text{2 elements: }|u(10)|=|0", size=48).set_color(MUTED)
        fit(eqf2, 6.4, 0.8)
        eqf2.move_to([XR, 1.15, 0])
        eq4 = E(r"\text{4 elements: }|u(10)|=|-0.0125", size=48).set_color(LIME)
        fit(eq4, 6.4, 0.8)
        eq4.move_to([XR, 0.2, 0])
        assert np.isclose(Q4[1], -0.0125)
        gap = DoubleArrow(pU(10, 0), pU(10, u_left(10)), buff=0, color=BAD, stroke_width=5, tip_length=0.18,
                          max_tip_length_to_length_ratio=0.2).set_z_index(5)
        with self.say("Pay close attention to this last point. Our two-element model draws a straight line from zero "
                      "to zero there, so it says point three doesn't move. The nodes are right, but between them the "
                      "model is only approximate. More elements, and the straight lines follow the true curve.",
                      style="slower and deliberate, stressing the key words") as d:
            self.play(Indicate(udot, color=SKY, scale_factor=1.6), run_time=.08 * d)
            self.wait(.03 * d)
            self.play(Create(fem2), FadeIn(nds), run_time=.12 * d)
            self.play(FadeIn(lab2), run_time=.05 * d)
            self.play(Write(eqf), run_time=.1 * d)
            self.play(GrowFromCenter(gap), run_time=.06 * d)
            self.play(self.spotlight(gap, udot), run_time=.05 * d)
            self.wait(2)
            self.play(self.unspot(), run_time=.05 * d)
            self.play(Indicate(nds, color=SKY, scale_factor=1.6), run_time=.1 * d)
            self.wait(.04 * d)
            self.add(old2)
            self.play(Transform(fem2, fem4), FadeOut(gap), lab2.animate.set_color(MUTED), FadeTransform(eqf, eqf2),
                      FadeOut(eanote), run_time=.13 * d)
            self.play(FadeIn(lab4), FadeIn(eq4), run_time=.06 * d)
        self.wipe()
