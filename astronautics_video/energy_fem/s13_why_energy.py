"""S13: why bother with energy? (BRIEF.md S13)."""
from efem import *
colors(**{"U": MINT, "U_e": MINT, "W": EMBER, r"\Pi": GOLD, "q": SKY, "q_1": SKY, "q_2": SKY, "q_3": SKY,
          "q_4": SKY, "u": SKY, "u_1": SKY, "u_2": SKY, "F": ROSE, "F_1": ROSE, "F_2": ROSE, "P": ROSE, "P_1": ROSE,
          "P_2": ROSE, "P_3": ROSE, "P_4": ROSE, "f": ROSE, "R": ROSE, "Q_1": ROSE, "Q_2": ROSE, "K": LILAC,
          "k": LILAC, "k_1": LILAC, "k_2": LILAC, "k_3": LILAC, "K_1": LILAC, "K_2": LILAC, "K_3": LILAC,
          "N_1": LIME, "N_2": LIME, "s": LIME, r"\sigma": ACCENT, r"\varepsilon": ACCENT})

# facts: the two-spring bowl (k1 = 40, k2 = 20 N/mm, F1 = 40, F2 = 20 N)
k1, k2, F1, F2 = 40.0, 20.0, 40.0, 20.0


def Pi2(a, b):
    return 0.5 * k1 * a ** 2 + 0.5 * k2 * (b - a) ** 2 - F1 * a - F2 * b


assert np.isclose(0.5 * k1, 20) and np.isclose(0.5 * k2, 10)
Q1, Q2 = np.linalg.solve([[k1 + k2, -k2], [-k2, k2]], [F1, F2])
assert np.isclose(Q1, 1.5) and np.isclose(Q2, 2.5)
assert np.isclose(Pi2(1.5, 2.5), -55)
# stationary: both partial derivatives vanish there
assert np.isclose(k1 * Q1 - k2 * (Q2 - Q1) - F1, 0) and np.isclose(k2 * (Q2 - Q1) - F2, 0)
# it is the minimum on the plotted floor (q1 in [0, 3], q2 in [0, 5])
_A, _B = np.meshgrid(np.linspace(0, 3, 61), np.linspace(0, 5, 101))
assert Pi2(_A, _B).min() >= -55 - 1e-9

ZS, ZOFF = 80.0, 70.0          # surface height z = (Pi + 70) / 80: floor (z = 0) sits below the minimum


def zof(p):
    return (p + ZOFF) / ZS


class S13_Why_Energy(VScene):
    budget = 146

    def construct(self):
        # ---------- beat 1: a node with five springs, Newton vs energy ----------
        ctr = np.array([-4.6, -0.6, 0])
        angs = [180, 115, 45, -20, -105]
        dirs = [np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0]) for a in angs]
        hub = node(ctr, r=0.11)
        springs = VGroup(*[spring(ctr + 0.12 * d, ctr + 1.75 * d, coils=4, amp=0.14) for d in dirs])
        anchors = VGroup(*[Square(0.22, color=INK2, fill_color=SURFACE, fill_opacity=1).move_to(ctr + 1.86 * d)
                           for d in dirs])
        fig = VGroup(springs, anchors, hub)

        fb = np.array([-0.4, -0.6, 0])
        fhub = node(fb, r=0.11)
        arrows = VGroup(*[Arrow(fb, fb + 1.35 * d, buff=0.1, color=LILAC, stroke_width=5,
                                max_tip_length_to_length_ratio=0.22) for d in dirs])
        qs = VGroup(*[T("sign?", 36, BAD).next_to(arrows[i].get_end(), dirs[i], buff=0.1) for i in (1, 3, 4)])
        newton_t = T("Newton: 5 arrows", 36, INK).move_to([-0.4, 2.0, 0])

        cmap = {"k_4": LILAC, "k_5": LILAC}
        lines = [E(r"U|=|\tfrac12|k_1|\Delta_1^2", size=48, cmap=cmap)]
        for i in range(2, 6):
            lines.append(E(r"+|\tfrac12|k_" + str(i) + r"|\Delta_" + str(i) + "^2", size=48, cmap=cmap))
        sumv = VGroup(*lines).arrange(DOWN, aligned_edge=RIGHT, buff=0.22).move_to([4.2, -0.6, 0])
        energy_t = T("Energy: 1 sum", 36, INK).move_to([4.2, 2.0, 0])
        note = T("Δ = stretch of a spring", 30, MUTED).next_to(sumv, DOWN, buff=0.35)

        with self.say("So which way was easier? For two springs, about the same. But picture a node with five springs on it. Newton needs five arrows, each with the right direction and the right sign. Energy needs one more term in a sum.") as d:
            self.play(FadeIn(hub), LaggedStart(*[Create(s) for s in springs], lag_ratio=0.2),
                      FadeIn(anchors), run_time=0.22 * d)
            self.play(FadeIn(newton_t), FadeIn(fhub), run_time=0.06 * d)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=0.2 * d)
            self.play(LaggedStart(*[FadeIn(q, scale=1.3) for q in qs], lag_ratio=0.3),
                      *[Indicate(arrows[i], color=BAD) for i in (1, 3, 4)], run_time=0.14 * d)
            self.play(FadeIn(energy_t), run_time=0.05 * d)
            for i in range(5):
                self.play(FadeIn(lines[i], shift=0.2 * DOWN), Indicate(springs[i], color=GOLD),
                          run_time=0.058 * d)
            self.play(FadeIn(note), Wiggle(qs), run_time=0.04 * d)

        # ---------- beat 2: one scalar ----------
        big = M(r"\Pi", size=140, color=GOLD).move_to(0.3 * UP)
        scal = T("a scalar: one number, no directions", 36, INK).next_to(big, DOWN, buff=0.6)
        self.beat("That's the first reason: energy is a scalar, a single number, with no directions to keep track of.",
                  [FadeOut(arrows), FadeOut(qs), FadeOut(fhub), FadeOut(newton_t), FadeOut(fig),
                   FadeOut(energy_t), FadeOut(note)],
                  [ReplacementTransform(sumv, big)], FadeIn(glow(big, GOLD)), FadeIn(scal, shift=0.2 * UP),
                  w=(.25, .3, .2, .25))
        self.wipe()

        # ---------- beat 3: the bowl Pi(q1, q2) ----------
        # SurfaceImage cannot render here (PIL 13 + manim image path), so the bowl is a vector mesh:
        # orthographic view, quads depth-sorted far to near (painter's rule), shaded by a fixed light.
        al, el, S = np.radians(42), np.radians(34), 1.6

        def raw(a, b, z):
            X, Y, Z = a, 0.6 * b, 0.85 * z
            xr, yr = X * np.cos(al) - Y * np.sin(al), X * np.sin(al) + Y * np.cos(al)
            return np.array([S * xr, S * (yr * np.sin(el) + Z * np.cos(el)), 0.0]), yr * np.cos(el) - Z * np.sin(el)

        na, nb = 12, 20
        A_ = np.linspace(0, 3, na + 1)
        B_ = np.linspace(0, 5, nb + 1)
        quads = []
        light = np.array([-0.4, -0.5, 0.77])
        light /= np.linalg.norm(light)
        for i in range(na):
            for j in range(nb):
                cs = [(A_[i], B_[j]), (A_[i + 1], B_[j]), (A_[i + 1], B_[j + 1]), (A_[i], B_[j + 1])]
                pts = [raw(a, b, zof(Pi2(a, b))) for a, b in cs]
                depth = np.mean([q[1] for q in pts])
                am, bm = (A_[i] + A_[i + 1]) / 2, (B_[j] + B_[j + 1]) / 2
                ga = (k1 * am - k2 * (bm - am) - F1) * 0.85 / ZS          # dz/dq1 (scaled)
                gb = (k2 * (bm - am) - F2) * 0.85 / ZS / 0.6               # dz/dY (scaled)
                nrm = np.array([-ga, -gb, 1.0])
                lam = max(0.0, float(nrm @ light / np.linalg.norm(nrm)))
                col = interpolate_color(ManimColor(BG), ManimColor(GOLD), 0.25 + 0.65 * lam)
                quads.append((depth, Polygon(*[q[0] for q in pts], stroke_color=BG, stroke_width=0.8,
                                             stroke_opacity=0.6, fill_color=col, fill_opacity=1)))
        quads.sort(key=lambda t: -t[0])
        mesh = VGroup(*[q[1] for q in quads])
        off = np.array([-2.8, -0.85, 0]) - mesh.get_center()
        mesh.shift(off)

        def P3(a, b, z):
            return raw(a, b, z)[0] + off

        floor = Polygon(P3(0, 0, 0), P3(3, 0, 0), P3(3, 5, 0), P3(0, 5, 0), stroke_color=HAIR, stroke_width=2,
                        fill_color=SURFACE, fill_opacity=1).set_z_index(-1)
        ax1 = Arrow(P3(0, 0, 0), P3(3.5, 0, 0), buff=0, color=SKY, stroke_width=6).set_z_index(3)
        ax2 = Arrow(P3(0, 0, 0), P3(0, 5.6, 0), buff=0, color=SKY, stroke_width=6).set_z_index(3)
        l1 = M("q_1", size=44, color=SKY).next_to(ax1.get_end(), UP, buff=0.12).set_z_index(3)
        l2 = M("q_2", size=44, color=SKY).next_to(ax2.get_end(), UP, buff=0.12).set_z_index(3)

        eq1 = E(r"\Pi|=|20\,|q_1^2", size=48, cmap={"q_1^2": SKY})
        eq2 = E(r"+\,10\,(|q_2|-|q_1|)^2", size=48)
        eq3 = E(r"-\,40\,|q_1|-\,20\,|q_2|", size=48)
        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        eq2.shift(0.95 * RIGHT)
        eq3.shift(0.95 * RIGHT)
        eqs.move_to([3.9, 0.9, 0])
        units = T("q in mm, Π in N mm", 30, MUTED).next_to(eqs, DOWN, buff=0.4)

        zmin = zof(-55)
        dot = Dot(P3(1.5, 2.5, zmin + 2.8), radius=0.12, color=INK).set_z_index(5)
        drop_line = DashedLine(P3(1.5, 2.5, zmin), P3(1.5, 2.5, 0), color=INK, stroke_width=3).set_z_index(4)
        foot = Dot(P3(1.5, 2.5, 0), radius=0.08, color=SKY).set_z_index(4)
        r1 = E(r"q_1|=|1.5,\quad|q_2|=|2.5\ \text{mm}", size=48)
        r2 = E(r"\Pi|=|-55\ \text{N mm}", size=52)
        reads = VGroup(r1, r2).arrange(DOWN, buff=0.45).move_to([3.95, 0.2, 0])

        with self.say("And the picture still works. With two unknowns, Pi is a bowl over a floor. One floor direction is q one, the other is q two. The answer is the lowest point of the bowl: one point five and two point five, where Pi is minus fifty five.") as d:
            self.play(FadeIn(floor), FadeIn(mesh), Write(eqs), FadeIn(units), run_time=0.24 * d)
            self.play(GrowArrow(ax1), FadeIn(l1, scale=1.4), run_time=0.1 * d)
            self.play(GrowArrow(ax2), FadeIn(l2, scale=1.4), run_time=0.1 * d)
            self.play(FadeOut(eqs), FadeOut(units), FadeIn(dot), run_time=0.07 * d)
            self.play(dot.animate.move_to(P3(1.5, 2.5, zmin)), rate_func=rush_into, run_time=0.13 * d)
            self.play(Create(drop_line), FadeIn(foot), FadeIn(r1), run_time=0.12 * d)
            self.play(FadeIn(r2), FadeIn(glow(r2, GOLD)), Flash(dot, color=INK), run_time=0.1 * d)
            self.wait(0.14 * d)
        self.wipe()

        # ---------- beat 4: it scales ----------
        n = 34
        x0, step, yc = -6.4, 0.95, 1.7
        chain = VGroup(wall([x0, yc, 0], side=LEFT, h=0.9))
        xs = [x0 + step * (i + 1) for i in range(n)]
        prev = x0
        for x in xs:
            chain.add(spring([prev, yc, 0], [x - 0.06, yc, 0], coils=3, amp=0.13))
            chain.add(node([x, yc, 0], r=0.06))
            prev = x
        dots_t = M(r"\cdots", size=48, color=INK2).move_to([prev + 0.6, yc, 0])
        chain.add(dots_t)
        count = T("100 springs", 30, MUTED).move_to([4.6, yc + 0.85, 0])

        cm = {r"\Delta_i^2": INK, "k_i": LILAC, "F_j": ROSE, "q_j": SKY, "q_n": SKY}
        u_eq = E(r"U|=|\sum_i \tfrac12\,|k_i|\,\Delta_i^2", size=48, cmap=cm)
        w_eq = E(r"W|=|\sum_j\,|F_j|\,|q_j|", size=48, cmap=cm)
        d_eq = E(r"\frac{\partial \Pi}{\partial q_n}|=|0,\quad n = 1, \dots, 100", size=48)
        eqs4 = VGroup(u_eq, w_eq, d_eq).arrange(DOWN, buff=0.3).move_to([0, -0.95, 0])
        note4 = backed(T("one function, many derivatives", 36, GOLD)).move_to([0, -3.45, 0])

        with self.say("Second reason: it scales. For a hundred springs, you write one sum for U, one sum for W, and take derivatives mechanically. A computer can do that without ever drawing a free-body diagram. That's exactly what finite elements do.") as d:
            self.add(chain)
            self.play(chain.animate.shift(20 * LEFT), FadeIn(count),
                      Succession(Wait(0.15 * d), FadeIn(u_eq, shift=0.2 * UP, run_time=0.12 * d),
                                 FadeIn(w_eq, shift=0.2 * UP, run_time=0.12 * d),
                                 FadeIn(d_eq, shift=0.2 * UP, run_time=0.14 * d),
                                 FadeIn(note4, run_time=0.12 * d)),
                      run_time=0.85 * d, rate_func=linear)
            self.play(Circumscribe(note4, color=GOLD), run_time=0.15 * d)
        self.wipe()
