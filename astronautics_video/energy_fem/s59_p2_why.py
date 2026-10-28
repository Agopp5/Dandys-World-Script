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

        # ---------- the homework bar, as S54/S55 draw it ----------
        wl = wall(np.array([X0, YB, 0]), side=LEFT, h=1.6)
        br = bar(X0, XL(40), y=YB, h=BH)
        fl = dist_load(XL(0) + 0.3, XL(40) - 0.05, YB - 0.62, n=16, d=LEFT, color=ROSE)
        flab = E(r"f|=|5\text{ lb/in}", size=40).move_to([2.0, YB - 1.38, 0])
        p1 = force(np.array([XL(20), YB, 0]), d=RIGHT, length=1.0, color=ROSE).set_z_index(3)
        p1lab = E(r"P_1|=|50\text{ lb}", size=40)
        p1lab.move_to([XL(20) + 0.1 + p1lab.width / 2, YB + 0.62, 0])
        p1g = VGroup(p1, p1lab)
        p1g.d_last = 0.0

        def follow(m):
            dd = D(20)
            m.shift((dd - m.d_last) * RIGHT)
            m.d_last = dd
        p1g.add_updater(follow)
        p2 = force(np.array([XL(40), YB, 0]), d=RIGHT, length=1.0, color=ROSE).set_z_index(3)
        p2lab = E(r"P_2|=|100\text{ lb}", size=40).move_to([XL(40) + 0.5, YB + 0.62, 0])
        n2 = node(np.array([XL(40), YB, 0])).set_z_index(4)
        n1 = always_redraw(lambda: node(np.array([XL(20) + D(20), YB, 0])).set_z_index(4))
        p3 = always_redraw(lambda: DashedLine([XL(10) + D(10), YB - 0.42, 0], [XL(10) + D(10), YB + 0.42, 0],
                                              color=MUTED, stroke_width=3, dash_length=0.08).set_z_index(3))

        def tag(n, x, col=INK2, dashed=False):
            c = Circle(radius=0.33, color=col, stroke_width=3)
            if dashed:
                c = DashedVMobject(c, num_dashes=14)
            return VGroup(c, M(str(n), size=44, color=MUTED if dashed else INK)).move_to([XL(x), YB - 1.38, 0])
        tags = VGroup(tag(0, 0), tag(1, 20), tag(2, 40))
        tag3 = tag(3, 10, MUTED, dashed=True)
        fig = VGroup(wl, br, fl, flab, p2, p2lab, n2, tags, tag3)

        # ---------- the cut ----------
        def shade_at(xc):
            r = Rectangle(width=XL(xc) - (X0 - 0.5), height=1.75, stroke_width=0, fill_color=BG, fill_opacity=0.72)
            return r.move_to([(XL(xc) + X0 - 0.5) / 2, YB - 0.05, 0]).set_z_index(5)

        def box_at(xc):
            x1, x2 = XL(xc) + 0.07, XL(40) + 1.2
            r = RoundedRectangle(corner_radius=0.12, width=x2 - x1, height=1.35, stroke_color=ROSE, stroke_width=3,
                                 fill_color=ROSE, fill_opacity=0.07)
            return r.move_to([(x1 + x2) / 2, YB - 0.2, 0]).set_z_index(1)

        def cut_at(xc):
            return DashedLine([XL(xc), YB - 0.75, 0], [XL(xc), YB + 0.6, 0], color=INK, stroke_width=4,
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
        tens = TX(r"(tension $+$)", size=32, color=MUTED).next_to(deflab, DOWN, buff=0.18)

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
            self.play(Indicate(VGroup(p1, p2, right_of(xc1)), color=INK), run_time=.12 * d)
