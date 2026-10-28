"""Part 3: HW 3, Problem 1 - shear centre of an unsymmetrical channel."""
from scommon import *  # noqa: F401,F403

# walls in units of a, in the order we integrate (free end of bottom flange -> top flange free end)
W = [((2, 0), (0, 0)), ((0, 0), (0, 2)), ((0, 2), (1, 2))]
TF = [1, 2, 2]
XI, ETA = -45 / 97, 46 / 97

# shear flows for Sy = 1 and Sx = 1 (a = 1), as fractions u of each wall
QY = [lambda u: 3 * (2 * u) * (7 + 12 * u) / 388,
      lambda u: 3 * (76 + 124 * (2 * u) - 53 * (2 * u) ** 2) / 776,
      lambda u: (42 - 33 * u - 9 * u ** 2) / 97]
QX = [lambda u: 3 * (2 * u) * (-23 + 16 * u) / 97,
      lambda u: -3 * (14 - 18 * (2 * u) + 3 * (2 * u) ** 2) / 97,
      lambda u: (30 + 18 * u - 48 * u ** 2) / 97]
SIDES = [1, 1, 1]


class S3Problem(SLesson):
    def construct(self):
        sec = Sec((-4.3, -1.9), 1.45)
        walls = VGroup(*[sec.wall(p0, p1, tf) for (p0, p1), tf in zip(W, TF)])
        with self.voice("s3_01"):
            hdr = header("HW 3, Problem 1: shear center of an unsymmetrical channel")
            self.play(FadeIn(hdr))
            self.play(Create(walls), run_time=1.5)
            dims = VGroup(dim_line(sec.P(0, -0.35), sec.P(2, -0.35), "2a", (0, 0)),
                          dim_line(sec.P(-1.25, 0), sec.P(-1.25, 2), "2a", (0, 0)),
                          dim_line(sec.P(0, 2.35), sec.P(1, 2.35), "a", (0, 0)))
            dims[0][1].next_to(dims[0][0], DOWN, buff=0.05)
            dims[1][1].next_to(dims[1][0], LEFT, buff=0.05)
            dims[2][1].next_to(dims[2][0], UP, buff=0.05)
            self.play(FadeIn(dims))
            goal = T(r"\text{show: }\ \xi_s = -\frac{45a}{97},\qquad \eta_s = \frac{46a}{97}", color=SC_COL).scale(0.8).move_to([3.0, 2.4, 0])
            fromc = Tx("measured from the web / lower-flange corner", color=REASON).scale(0.55).next_to(goal, DOWN, buff=0.2)
            self.play(Write(goal), FadeIn(fromc))
            self.hold()

        with self.voice("s3_02"):
            tl = VGroup(Tx("$t$", color=Q_COL).scale(0.6).next_to(sec.P(1.5, 0), UP, buff=0.12),
                        Tx("$2t$", color=Q_COL).scale(0.6).next_to(sec.P(0, 1.2), RIGHT, buff=0.15),
                        Tx("$2t$", color=Q_COL).scale(0.6).next_to(sec.P(0.6, 2), DOWN, buff=0.15))
            self.play(LaggedStart(*[FadeIn(x) for x in tl], lag_ratio=0.5))
            self.play(Indicate(walls[1], color=Q_COL), Indicate(walls[2], color=Q_COL))
            warn = Tx(r"web and top flange are drawn thick: $2t$\\(any other reading gives a different answer)", color=YELLOW).scale(0.58)
            warn.next_to(fromc, DOWN, buff=0.45)
            self.play(FadeIn(warn))
            self.hold()

        with self.voice("s3_03"):
            self.play(FadeOut(warn))
            ox = Arrow(sec.P(0, 0), sec.P(0.9, 0) + DOWN * 0.0, buff=0, color=DIM, stroke_width=3).shift(DOWN * 0.0)
            ax = VGroup(Arrow(sec.P(-0.45, -0.7), sec.P(0.45, -0.7), buff=0, color=DIM, stroke_width=3),
                        Arrow(sec.P(-0.45, -0.7), sec.P(-0.45, 0.2), buff=0, color=DIM, stroke_width=3))
            axl = VGroup(T("x", color=DIM).scale(0.55).next_to(ax[0], RIGHT, buff=0.05), T("y", color=DIM).scale(0.55).next_to(ax[1], UP, buff=0.05))
            od = sec.dot(0, 0, WHITE)
            self.play(FadeIn(od), GrowArrow(ax[0]), GrowArrow(ax[1]), FadeIn(axl))
            ns = Tx(r"no axis of symmetry $\Rightarrow I_{xy}\neq0$:\\need both $\xi_s$ and $\eta_s$", color=REASON).scale(0.6).next_to(fromc, DOWN, buff=0.45)
            self.play(FadeIn(ns))
            self.hold()
        self.play(FadeOut(VGroup(goal, fromc, ns)))

        # ---- section properties
        with self.voice("s3_04"):
            self.play(Transform(hdr, header("Step 1: centroid")))
            bd = Board(self, left=-1.0, top=2.5, scale=0.72, buff=0.34)
            bd.line(r"A = \underbrace{2a\cdot t}_{\text{bottom}} + \underbrace{2a\cdot 2t}_{\text{web}} + \underbrace{a\cdot 2t}_{\text{top}} = 2at + 4at + 2at = 8at")
            self.hold()

        with self.voice("s3_05"):
            bd.line(r"\bar x = \frac{(2at)(a) + (4at)(0) + (2at)(a/2)}{8at} = \frac{3a}{8}", reason="each area $\\times$ its centre's $x$")
            bd.line(r"\bar y = \frac{(2at)(0) + (4at)(a) + (2at)(2a)}{8at} = a", reason="each area $\\times$ its centre's $y$")
            cd = sec.dot(3 / 8, 1, Q_COL, 0.08)
            cl = sec.label("C", 3 / 8, 1, UR, Q_COL)
            self.play(FadeIn(cd), FadeIn(cl))
            self.hold()

        with self.voice("s3_06"):
            bd.clear()
            self.play(Transform(hdr, header("Step 2: second moments of area (about C)")))
            bd = Board(self, left=-1.0, top=2.5, scale=0.68, buff=0.32)
            bd.line(r"I_{xx} = \underbrace{(2at)a^2}_{\text{bottom}} + \underbrace{\tfrac{(2t)(2a)^3}{12}}_{\text{web}} + \underbrace{(2at)a^2}_{\text{top}} = \frac{16a^3t}{3}")
            self.hold()

        with self.voice("s3_07"):
            bd.line(r"I_{yy} = \Big[\tfrac{t(2a)^3}{12} + 2at\big(\tfrac{5a}{8}\big)^2\Big] + 4at\big(\tfrac{3a}{8}\big)^2 + \Big[\tfrac{2t\,a^3}{12} + 2at\big(\tfrac{a}{8}\big)^2\Big] = \frac{53a^3t}{24}")
            self.hold()

        with self.voice("s3_08"):
            bd.line(r"I_{xy} = (2at)\big(\tfrac{5a}{8}\big)(-a) + 0 + (2at)\big(\tfrac{a}{8}\big)(a) = -\tfrac{5}{4}a^3t + \tfrac14 a^3t = -a^3t",
                    reason="area $\\times$ $x$ offset $\\times$ $y$ offset", below=True)
            self.hold()

        with self.voice("s3_09"):
            l = bd.line(r"I_{xx}I_{yy} - I_{xy}^2 = \Big(\frac{16}{3}\cdot\frac{53}{24} - 1\Big)a^6t^2 = \frac{97}{9}\,a^6t^2", color=YELLOW)
            bd.box(l)
            self.hold()
        bd.clear()
        props = VGroup(T(r"C = (\tfrac{3a}{8},\ a)"), T(r"I_{xx} = \tfrac{16}{3}a^3t,\ \ I_{yy} = \tfrac{53}{24}a^3t,\ \ I_{xy} = -a^3t"),
                       T(r"D = I_{xx}I_{yy} - I_{xy}^2 = \tfrac{97}{9}a^6t^2")).scale(0.55).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        props.to_corner(UR, buff=0.3)
        pbox = SurroundingRectangle(props, color=DIM, buff=0.12)
        self.play(FadeIn(props), Create(pbox))

        # ---- moment centre
        with self.voice("s3_10"):
            self.play(Transform(hdr, header("Step 3: a clever moment center: the corner")))
            self.play(walls[0].animate.set_opacity(0.3), walls[1].animate.set_opacity(0.3), Indicate(walls[2], color=YELLOW))
            arm = dim_line(sec.P(-0.25, 0), sec.P(-0.25, 2), "2a", (0, 0))
            arm.set_color(YELLOW)
            arm[1].next_to(arm[0], LEFT, buff=0.05)
            self.play(FadeOut(dims[1]), FadeIn(arm))
            note = Tx(r"bottom flange and web pass through the corner:\\no moment. Only the top-flange force $F_{top}$ matters.", color=YELLOW).scale(0.6)
            note.move_to([2.9, 0.4, 0])
            self.play(FadeIn(note))
            self.hold()
        self.play(walls[0].animate.set_opacity(1), walls[1].animate.set_opacity(1), FadeOut(note))

        # ---- load case Sy
        fills = VGroup()
        with self.voice("s3_11"):
            self.play(Transform(hdr, header("Load case 1: $S_y$ only $\\to\\ \\xi_s$")))
            bd = Board(self, left=-1.0, top=1.4, scale=0.66, buff=0.3, ceiling=pbox.get_bottom()[1] - 0.05)
            bd.line(r"q_s = \frac{S_y}{D}\Big[I_{xy}\int_0^s t x\,ds - I_{yy}\int_0^s t y\,ds\Big]", reason="general formula with $S_x = 0$")
            bd.line(r"q_s = -\frac{9S_y}{97a^3t}\Big[\int_0^s t x\,ds + \frac{53}{24}\int_0^s t y\,ds\Big]", color=YELLOW, indent=0.4,
                    reason="$x, y$ measured from C")
            self.hold()

        def fill(i, Q, k=2.2):
            f = flow_fill(sec, *W[i], Q[i], k, side=SIDES[i])
            fills.add(f)
            self.play(FadeIn(f), run_time=0.8)

        with self.voice("s3_12"):
            bd.line(r"\text{bottom } (t):\ x = \tfrac{13a}{8} - s,\ y = -a:\quad q_{12} = \frac{3S_y\,s\,(7a + 6s)}{388a^3}", below=False)
            fill(0, QY)
            bd.line(r"\text{corner: } q = \frac{57\,S_y}{194\,a}", indent=0.4, color=Q_FILL)
            self.hold()

        with self.voice("s3_13"):
            bd.line(r"\text{web } (2t):\ x = -\tfrac{3a}{8},\ y = -a + s:\quad q_{23} = \frac{3S_y(76a^2 + 124as - 53s^2)}{776a^3}")
            fill(1, QY)
            bd.line(r"\text{top of web: } q = \frac{42\,S_y}{97\,a}", indent=0.4, color=Q_FILL)
            self.hold()

        with self.voice("s3_14"):
            bd.line(r"\text{top } (2t):\ q_{34} = \frac{S_y(42a^2 - 33as - 9s^2)}{97a^3}", color=Q_FILL)
            fill(2, QY)
            bd.line(r"s = a:\ q = 42 - 33 - 9 = 0\ \checkmark", indent=0.4, color=Q_COL)
            self.hold()

        with self.voice("s3_15"):
            bd.clear()
            bd = Board(self, left=-1.0, top=1.4, scale=0.7, buff=0.36, ceiling=pbox.get_bottom()[1] - 0.05)
            l = bd.line(r"F_{top} = \int_0^a q_{34}\,ds = \frac{S_y}{97a^3}\Big(42a^3 - \frac{33}{2}a^3 - 3a^3\Big) = \frac{45\,S_y}{194}\ \ (\to)")
            Ft = Arrow(sec.P(0.15, 2.45), sec.P(0.9, 2.45), buff=0, color=P_COL, stroke_width=6)
            Ftl = T("F_{top}", color=P_COL).scale(0.6).next_to(Ft, RIGHT, buff=0.1)
            self.play(FadeOut(dims[2]), GrowArrow(Ft), FadeIn(Ftl))
            self.hold()

        with self.voice("s3_16"):
            bd.line(r"\xi_s\,S_y = -\,(2a)\,F_{top}", reason="moments about the corner (counter-clockwise $+$)")
            l = bd.line(r"\xi_s = -2a\cdot\frac{45}{194} = -\frac{45a}{97}", color=SC_COL)
            bd.box(l, SC_COL)
            vline = DashedLine(sec.P(XI, -0.8), sec.P(XI, 2.6), color=SC_COL)
            self.play(Create(vline))
            self.hold()

        # ---- load case Sx
        with self.voice("s3_17"):
            bd.clear()
            self.play(FadeOut(fills), FadeOut(Ft), FadeOut(Ftl))
            fills = VGroup()
            self.play(Transform(hdr, header("Load case 2: $S_x$ only $\\to\\ \\eta_s$")))
            bd = Board(self, left=-1.0, top=1.4, scale=0.66, buff=0.3, ceiling=pbox.get_bottom()[1] - 0.05)
            bd.line(r"q_s = -\frac{S_x}{D}\Big[I_{xx}\int_0^s t x\,ds - I_{xy}\int_0^s t y\,ds\Big]", reason="general formula with $S_y = 0$")
            bd.line(r"q_s = -\frac{9S_x}{97a^3t}\Big[\frac{16}{3}\int_0^s t x\,ds + \int_0^s t y\,ds\Big]", color=YELLOW, indent=0.4)
            self.hold()

        with self.voice("s3_18"):
            bd.line(r"\text{corner: } q = -\frac{42S_x}{97a},\qquad \text{top of web: } q = \frac{30S_x}{97a}")
            fill(0, QX, 1.3)
            fill(1, QX, 1.3)
            bd.line(r"\text{top: } q_{34} = \frac{S_x(30a^2 + 18as - 48s^2)}{97a^3},\qquad q(a) = 0\ \checkmark", color=Q_FILL)
            fill(2, QX, 1.3)
            self.hold()

        with self.voice("s3_19"):
            bd.line(r"F_{top} = \frac{S_x}{97}(30 + 9 - 16) = \frac{23S_x}{97}\ \ (\to)")
            bd.line(r"-\,\eta_s\,S_x = -\,(2a)\,F_{top}", reason="moments about the corner")
            l = bd.line(r"\eta_s = \frac{46a}{97}", color=SC_COL)
            bd.box(l, SC_COL)
            hline = DashedLine(sec.P(-0.9, ETA), sec.P(2.2, ETA), color=SC_COL)
            self.play(Create(hline))
            self.hold()

        with self.voice("s3_20"):
            bd.clear()
            self.play(FadeOut(fills))
            sd = Dot(sec.P(XI, ETA), color=SC_COL, radius=0.1)
            sl = T("S", color=SC_COL).scale(0.8).next_to(sd, LEFT, buff=0.12)
            self.play(FadeIn(sd, scale=2), FadeIn(sl))
            res = T(r"S = \Big(-\frac{45a}{97},\ \frac{46a}{97}\Big) \approx (-0.464a,\ 0.474a)", color=SC_COL).scale(0.85).move_to([2.6, 0.2, 0])
            self.play(Write(res), run_time=2.0)
            self.play(Create(SurroundingRectangle(res, color=SC_COL, buff=0.2)))
            tip = Tx(r"strategy: choose a moment center where most walls drop out", color=REASON).scale(0.6).next_to(res, DOWN, buff=0.6)
            self.play(FadeIn(tip))
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))
