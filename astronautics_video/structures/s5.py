"""Part 5: HW 3, Problem 2 - shear flow in a thin-walled isosceles triangle."""
from scommon import *  # noqa: F401,F403

H, LL = 2.4, 3.2                      # drawing: wall 2-3 height h, apex distance L
D = float(np.sqrt(LL ** 2 + (H / 2) ** 2))
P1, P2, P3 = (LL, 0.0), (0.0, -H / 2), (0.0, H / 2)
WALLS = [(P1, P2), (P2, P3), (P3, P1)]
IXX = H ** 2 * (2 * D + H) / 12       # per unit t

# basic (cut at apex) and final shear flows for Sy = 1, as functions of the fraction u along each wall
QB = [lambda u: H * (u * D) ** 2 / (4 * D * IXX),
      lambda u: -((-H * (u * H) / 2 + (u * H) ** 2 / 2)) / IXX + H * D / (4 * IXX),
      lambda u: -(H * (u * D) / 2 - H * (u * D) ** 2 / (4 * D)) / IXX + H * D / (4 * IXX)]
QS0 = -(3 * D + H) / (H * (2 * D + H))
QF = [lambda u, f=f: f(u) + QS0 for f in QB]


class S5Problem(SLesson):
    def construct(self):
        sec = Sec((-5.7, -0.55), 1.0)
        tri = VGroup(*[sec.wall(a, b) for a, b in WALLS])
        nums = VGroup(sec.label("1", *P1, RIGHT), sec.label("2", *P2, DOWN), sec.label("3", *P3, UP))
        with self.voice("s5_01"):
            hdr = header("HW 3, Problem 2: an isosceles triangle")
            self.play(FadeIn(hdr))
            self.play(Create(tri), FadeIn(nums), run_time=1.5)
            ld = load_arrow(sec.P(LL, -1.4), sec.P(LL, -0.12), r"S_y", direction=RIGHT)
            ld[1].next_to(ld[0].get_start(), RIGHT, buff=0.12)
            self.play(GrowArrow(ld[0]), FadeIn(ld[1]))
            tasks = VGroup(Tx(r"$\bullet$ shear flow distribution $q(s)$"), Tx(r"$\bullet$ directions and principal values"),
                           Tx(r"$\bullet$ extra credit: $I_{xx} = 2\,\dfrac{d\,t\,h^2}{12} + \dfrac{t\,h^3}{12}$", color=YELLOW)).scale(0.62)
            tasks.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 1.6, 0])
            for tk in tasks:
                self.play(FadeIn(tk, shift=RIGHT * 0.2), run_time=0.6)
            self.hold()

        with self.voice("s5_02"):
            hd = dim_line(sec.P(-0.45, -H / 2), sec.P(-0.45, H / 2), "h", (0, 0))
            hd[1].next_to(hd[0], LEFT, buff=0.05)
            dd = dim_line(sec.P(*P3), sec.P(*P1), "d", (0, 0))
            dd.shift(np.array([0.18, 0.32, 0]))
            xax = DashedLine(sec.P(-0.8, 0), sec.P(LL + 1.0, 0), color=DIM)
            xl = T("x", color=DIM).scale(0.55).next_to(xax, RIGHT, buff=0.05)
            self.play(FadeIn(hd), FadeIn(dd), Create(xax), FadeIn(xl))
            sym = Tx(r"symmetric about $x$: $I_{xy} = 0$,\\centroid on the $x$ axis", color=REASON).scale(0.6).next_to(tasks, DOWN, buff=0.5)
            self.play(FadeIn(sym))
            self.hold()
        self.play(FadeOut(VGroup(tasks, sym)))

        # ---- extra credit: Ixx
        with self.voice("s5_03"):
            self.play(Transform(hdr, header("Extra credit: $I_{xx}$")))
            self.play(Indicate(tri[0], color=YELLOW), Indicate(tri[2], color=YELLOW))
            bd = Board(self, left=-0.8, top=2.4, scale=0.75, buff=0.42)
            bd.line(r"\text{sloping wall: } y = \frac{h}{2d}\,s,\quad 0\le s\le d", reason="$y$ grows linearly from the apex")
            bd.line(r"\int_0^d t\,y^2\,ds = t\,\frac{h^2}{4d^2}\int_0^d s^2\,ds", indent=0.4)
            self.hold()

        with self.voice("s5_04"):
            bd.line(r"= t\,\frac{h^2}{4d^2}\cdot\frac{d^3}{3} = \frac{d\,t\,h^2}{12}", indent=0.4, reason="each sloping wall (there are two)")
            self.hold()

        with self.voice("s5_05"):
            self.play(Indicate(tri[1], color=YELLOW))
            bd.line(r"\text{vertical wall: } \frac{t\,h^3}{12}", reason="rectangle of height $h$ about its middle")
            l = bd.line(r"I_{xx} = 2\,\frac{d\,t\,h^2}{12} + \frac{t\,h^3}{12} = \frac{t\,h^2}{12}(2d + h)", color=YELLOW)
            bd.box(l)
            self.hold()
        bd.clear()

        # ---- basic shear flow
        cutd = Line(sec.P(LL - 0.18, 0.1), sec.P(LL - 0.18, -0.1), color=BG, stroke_width=16)
        with self.voice("s5_06"):
            self.play(Transform(hdr, header("Cut at the apex: the basic shear flow $q_b$")))
            self.play(FadeIn(cutd))
            cl = Tx("cut", color=YELLOW).scale(0.55).next_to(sec.P(LL, 0), UP, buff=0.35)
            s_arrows = VGroup(*[Arrow(sec.P(*a) + 0.25 * (np.array([*b, 0]) - np.array([*a, 0])) / np.linalg.norm(np.array(b) - np.array(a)) * 2,
                                     sec.P(*a) + 0.25 * (np.array([*b, 0]) - np.array([*a, 0])) / np.linalg.norm(np.array(b) - np.array(a)) * 4,
                                     buff=0, color=YELLOW, stroke_width=3, tip_length=0.12) for a, b in WALLS])
            self.play(FadeIn(cl), FadeIn(s_arrows))
            bd = Board(self, left=-0.6, top=2.4, scale=0.72, buff=0.38)
            bd.line(r"q_b = -\frac{S_y}{I_{xx}}\int_0^s t\,y\,ds", reason="$S_x = 0,\\ I_{xy} = 0$; path $1\\to2\\to3\\to1$")
            self.hold()

        fills = VGroup()

        def show_fill(i, Q, k=1.6):
            f = flow_fill(sec, *WALLS[i], Q[i], k, side=-1 if i != 1 else 1)
            fills.add(f)
            self.play(FadeIn(f), run_time=0.8)
        with self.voice("s5_07"):
            bd.line(r"1\to2:\ y = -\frac{h\,s}{2d}:\quad q_{b,12} = \frac{S_y\,t\,h}{4\,d\,I_{xx}}\,s^2", color=Q_FILL)
            show_fill(0, QB)
            bd.line(r"q_{b,2} = \frac{S_y\,t\,h\,d}{4\,I_{xx}}", indent=0.6, color=Q_FILL)
            self.hold()

        with self.voice("s5_08"):
            bd.line(r"2\to3:\ y = -\frac{h}{2} + s:\quad q_{b,23} = -\frac{S_y t}{I_{xx}}\Big(-\frac{h s}{2} + \frac{s^2}{2}\Big) + q_{b,2}", color=Q_FILL)
            show_fill(1, QB)
            bd.line(r"s = h:\ \ -\tfrac{h^2}{2} + \tfrac{h^2}{2} = 0\ \Rightarrow\ q_{b,3} = q_{b,2}", indent=0.6)
            self.hold()

        with self.voice("s5_09"):
            show_fill(2, QB)
            bd.line(r"3\to1:\ \ q_b \text{ returns to } 0 \text{ at the cut}\ \checkmark", color=Q_COL)
            self.hold()
        bd.clear()

        # ---- q_s0 from moments about the apex
        with self.voice("s5_10"):
            self.play(Transform(hdr, header("Find $q_{s,0}$: moments about the apex")))
            self.play(fills[0].animate.set_opacity(0.12), fills[2].animate.set_opacity(0.12),
                      tri[0].animate.set_opacity(0.35), tri[2].animate.set_opacity(0.35))
            arm = dim_line(sec.P(0, -H / 2 - 0.55), sec.P(LL, -H / 2 - 0.55), "L", (0, 0))
            arm.set_color(YELLOW)
            arm[1].next_to(arm[0], DOWN, buff=0.05)
            self.play(FadeIn(arm))
            bd = Board(self, left=-0.6, top=2.4, scale=0.72, buff=0.38)
            bd.line(r"\text{load through the apex} \Rightarrow \text{applied moment} = 0")
            bd.line(r"\text{walls 1-2 and 3-1 pass through the apex: } p = 0", reason="only the vertical wall has a moment arm", below=True)
            self.hold()

        with self.voice("s5_11"):
            bd.line(r"0 = L\int_0^h q_{b,23}\,ds + 2A\,q_{s,0}")
            bd.line(r"2A = L\,h\ \Rightarrow\ q_{s,0} = -\frac{1}{h}\int_0^h q_{b,23}\,ds", indent=0.6, color=YELLOW,
                    reason="minus the average of $q_b$ on the vertical wall", below=True)
            self.hold()

        with self.voice("s5_12"):
            bd.clear()
            bd = Board(self, left=-0.6, top=2.4, scale=0.72, buff=0.4)
            bd.line(r"q_{s,0} = -\frac{1}{h}\int_0^h q_{b,23}\,ds", color=YELLOW)
            bd.line(r"\int_0^h q_{b,23}\,ds = \frac{S_y t h^3}{12 I_{xx}} + \frac{S_y t h^2 d}{4 I_{xx}}", indent=0.6)
            l = bd.line(r"q_{s,0} = -\frac{S_y\,(3d + h)}{h\,(2d + h)}", color=YELLOW, indent=0.6, reason="using $I_{xx} = \\tfrac{t h^2}{12}(2d+h)$")
            bd.box(l)
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(fills, arm, cutd, s_arrows, cl)), tri.animate.set_opacity(1))

        # ---- final distribution
        ffills = VGroup(*[flow_fill(sec, *WALLS[i], QF[i], 0.9, side=-1 if i != 1 else 1) for i in range(3)])
        with self.voice("s5_13"):
            self.play(Transform(hdr, header("The final shear flow: $q = q_b + q_{s,0}$")))
            bd = Board(self, left=-0.6, top=2.4, scale=0.72, buff=0.4)
            bd.line(r"q_{12} = \frac{S_y\,(3s^2 - 3d^2 - dh)}{d\,h\,(2d + h)}", color=Q_FILL, reason="sloping walls ($q_{31}$ is the mirror image)")
            bd.line(r"q_{23} = -\frac{S_y\,(h^2 - 6hs + 6s^2)}{h^2\,(2d + h)}", color=Q_FILL, reason="vertical wall")
            self.play(FadeIn(ffills))
            self.hold()

        with self.voice("s5_14"):
            bd.line(r"\text{apex: } |q_1| = \frac{S_y(3d + h)}{h(2d + h)}", color=YELLOW)
            bd.line(r"\text{corners 2, 3: } |q| = \frac{S_y}{2d + h},\qquad \text{mid-wall: } q = \frac{S_y}{2(2d + h)}", color=YELLOW)
            v1 = Tx(r"$\dfrac{S_y(3d+h)}{h(2d+h)}$", color=YELLOW).scale(0.5).next_to(sec.P(*P1), UR, buff=0.25)
            v2 = Tx(r"$\dfrac{S_y}{2d+h}$", color=YELLOW).scale(0.5).next_to(sec.P(*P2), DL, buff=0.15)
            v3 = Tx(r"$\dfrac{S_y}{2d+h}$", color=YELLOW).scale(0.5).next_to(sec.P(*P3), UL, buff=0.15)
            vm = Tx(r"$\dfrac{S_y}{2(2d+h)}$", color=YELLOW).scale(0.5).next_to(sec.P(0, 0), LEFT, buff=0.55)
            self.play(FadeOut(VGroup(hd, dd, xl)), FadeIn(v1), FadeIn(v2), FadeIn(v3), FadeIn(vm))
            self.hold()

        with self.voice("s5_15"):
            arrows = VGroup(flow_arrows(sec, *WALLS[0], QF[0], 3, color=WHITE, length=0.5, side=0.0),
                            flow_arrows(sec, *WALLS[1], QF[1], 5, color=WHITE, length=0.38),
                            flow_arrows(sec, *WALLS[2], QF[2], 3, color=WHITE, length=0.5))
            self.play(LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.3), run_time=2.0)
            dirs = VGroup(Tx(r"lower wall: flows up toward the apex"), Tx(r"upper wall: flows up away from the apex"),
                          Tx(r"vertical wall: down near the corners, up in the middle"),
                          T(r"q_{23} = 0 \text{ at } s = \tfrac{3\mp\sqrt3}{6}h \approx 0.21h,\ 0.79h")).scale(0.55)
            dirs.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.3, 1.2, 0])
            bd.clear()
            self.play(FadeIn(dirs))
            self.hold()

        with self.voice("s5_16"):
            self.play(FadeOut(dirs))
            bd = Board(self, left=-0.6, top=2.4, scale=0.75, buff=0.42)
            bd.line(r"\sum F_x = 0", reason="the two sloping walls cancel", color=Q_COL)
            bd.line(r"\sum F_y = S_y", reason="verified by integrating every wall", color=Q_COL)
            bd.line(r"\sum M_{\text{apex}} = 0", reason="the load passes through the apex", color=Q_COL)
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("s5_17"):
            h, rows = recap(self, [
                r"Shear flow comes from the change of bending stress along the beam: $\partial q/\partial s = -t\,\partial\sigma_z/\partial z$.",
                r"Open sections: start where $q = 0$ (a free edge) and integrate wall by wall.",
                r"Shear center: the point where a load causes no twist, found by balancing moments.",
                r"Closed sections: cut, find $q_b$, add a constant $q_{s,0}$ from moments or zero twist.",
            ], title="Series recap")
            for rr in rows:
                self.play(FadeIn(rr, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
