"""Part 2: the shear centre of an open section (channel)."""
from scommon import *  # noqa: F401,F403

B, Hh = 1.0, 2.0                       # channel: flange width b, web height h (drawing units)
IXX = Hh ** 3 / 12 * (1 + 6 * B / Hh)  # per unit t
Q2 = 6 * B / (Hh ** 2 * (1 + 6 * B / Hh))
E = 3 * B ** 2 / (Hh + 6 * B)


def q12(u):
    return Q2 * u


def q23(u):
    s2 = u * Hh
    return Q2 + (Hh * s2 / 2 - s2 ** 2 / 2) / IXX


def q34(u):
    return Q2 * (1 - u)


class S2Concept(SLesson):
    def construct(self):
        with self.voice("s2_01"):
            card = s_title(self, 2, "The Shear Center", "where a shear load bends a beam without twisting it")
            self.hold()
        self.play(FadeOut(card))

        sec = Sec((-3.6, -0.5), 1.5)
        W = [((B, -1), (0, -1)), ((0, -1), (0, 1)), ((0, 1), (B, 1))]
        chan = VGroup(*[sec.wall(p0, p1) for p0, p1 in W])
        arrows = VGroup(flow_arrows(sec, *W[0], q12, 2), flow_arrows(sec, *W[1], q23, 3), flow_arrows(sec, *W[2], q34, 2))
        Spt = sec.P(-E, 0)
        with self.voice("s2_02"):
            hdr = header("A puzzle: why does this channel twist?")
            self.play(FadeIn(hdr))
            self.play(Create(chan))
            ld = load_arrow(sec.P(0, -2.0), sec.P(0, -1.15), r"S_y", direction=LEFT)
            self.play(GrowArrow(ld[0]), FadeIn(ld[1]))
            self.play(FadeIn(arrows))
            body = VGroup(chan, arrows, ld)
            self.play(Rotate(body, angle=-0.35, about_point=Spt), run_time=1.5)
            tw = Tx(r"it bends \emph{and} twists", color=P_COL).scale(0.75).move_to([2.8, 1.6, 0])
            self.play(Write(tw))
            why = Tx(r"the flange shear flows form a couple\\that the load does not balance", color=REASON).scale(0.6).next_to(tw, DOWN, buff=0.35)
            self.play(FadeIn(why))
            self.play(Rotate(body, angle=0.35, about_point=Spt), run_time=1.2)
            self.hold()

        with self.voice("s2_03"):
            self.play(FadeOut(tw), FadeOut(why), FadeOut(ld))
            sdot = Dot(Spt, color=SC_COL, radius=0.09)
            sl = T("S", color=SC_COL).scale(0.8).next_to(sdot, LEFT, buff=0.12)
            self.play(FadeIn(sdot), FadeIn(sl))
            ld2 = load_arrow(Spt + DOWN * 1.6, Spt + DOWN * 0.1, r"S_y", direction=LEFT)
            self.play(GrowArrow(ld2[0]), FadeIn(ld2[1]))
            ok = Tx(r"load through $S$: bends, no twist", color=Q_COL).scale(0.75).move_to([2.8, 1.6, 0])
            self.play(Write(ok))
            self.play(VGroup(chan, arrows, sdot, sl, ld2).animate.shift(UP * 0.35), rate_func=there_and_back, run_time=2.0)
            dfn = Tx(r"shear center $S$: the point a shear load must pass through\\to cause bending without twisting", color=SC_COL).scale(0.6)
            dfn.next_to(ok, DOWN, buff=0.4)
            self.play(FadeIn(dfn))
            self.hold()
        self.play(FadeOut(VGroup(chan, arrows, sdot, sl, ld2, ok, dfn)))

        with self.voice("s2_04"):
            self.play(Transform(hdr, header("Two shortcuts")))
            i_sec = Sec((-4.5, 0.2), 0.8)
            ibeam = VGroup(i_sec.wall((-1, 1), (1, 1)), i_sec.wall((0, 1), (0, -1)), i_sec.wall((-1, -1), (1, -1)))
            iax = DashedLine(i_sec.P(-1.6, 0), i_sec.P(1.6, 0), color=DIM)
            isd = Dot(i_sec.P(0, 0), color=SC_COL)
            ang_sec = Sec((0.0, -0.4), 0.9)
            angle = VGroup(ang_sec.wall((0, 0), (0, 2)), ang_sec.wall((0, 0), (1.6, 0)))
            asd = Dot(ang_sec.P(0, 0), color=SC_COL)
            cr_sec = Sec((4.2, 0.2), 0.8)
            cross = VGroup(cr_sec.wall((-1.2, 0), (1.2, 0)), cr_sec.wall((0, -1.2), (0, 1.2)))
            csd = Dot(cr_sec.P(0, 0), color=SC_COL)
            l1 = Tx(r"symmetric: $S$ on the\\axis of symmetry", color=REASON).scale(0.55).next_to(ibeam, DOWN, buff=0.6)
            l2 = Tx(r"walls meet at one point:\\$S$ is that point", color=REASON).scale(0.55).next_to(angle, DOWN, buff=0.35)
            l3 = Tx(r"cruciform:\\$S$ at the center", color=REASON).scale(0.55).next_to(cross, DOWN, buff=0.35)
            self.play(Create(ibeam), Create(iax), FadeIn(isd), FadeIn(l1))
            self.wait(1.5)
            self.play(Create(angle), FadeIn(asd), FadeIn(l2))
            self.play(Create(cross), FadeIn(csd), FadeIn(l3))
            self.hold()
        self.play(FadeOut(VGroup(ibeam, iax, isd, angle, asd, cross, csd, l1, l2, l3)))

        # ---- the channel, worked
        sec = Sec((-4.0, -0.6), 1.6)
        chan = VGroup(*[sec.wall(p0, p1) for p0, p1 in W])
        pts = VGroup(sec.label("1", B, -1, DOWN), sec.label("2", 0, -1, UR), sec.label("3", 0, 1, UL), sec.label("4", B, 1, UP))
        with self.voice("s2_05"):
            self.play(Transform(hdr, header("Worked: the shear center of a channel")))
            self.play(Create(chan), FadeIn(pts))
            dims = VGroup(dim_line(sec.P(0, 1.35), sec.P(B, 1.35), "b", (0, 0.0)),
                          dim_line(sec.P(-0.95, -1), sec.P(-0.95, 1), "h", (0, 0)),
                          Tx(r"uniform $t$", color=DIM).scale(0.5).next_to(sec.P(B, -1), RIGHT, buff=0.3))
            dims[1][1].next_to(dims[1][0], LEFT, buff=0.1)
            dims[0][1].next_to(dims[0][0], UP, buff=0.05)
            xax = DashedLine(sec.P(-0.6, 0), sec.P(1.6, 0), color=DIM)
            xl = Tx(r"$x$: axis of symmetry", color=DIM).scale(0.5).next_to(xax, RIGHT, buff=0.1)
            self.play(FadeIn(dims), Create(xax), FadeIn(xl))
            bd = Board(self, left=0.6, top=2.4, scale=0.75)
            bd.line(r"I_{xy} = 0\ \Rightarrow\ S \text{ is on the } x \text{ axis}", reason="only its $x$-position is unknown", below=True)
            self.hold()

        with self.voice("s2_06"):
            bd.line(r"I_{xx} = \frac{t h^3}{12} + 2\,(b\,t)\Big(\frac{h}{2}\Big)^2", reason="web + two flanges", below=True)
            l = bd.line(r"I_{xx} = \frac{t h^3}{12}\Big(1 + \frac{6b}{h}\Big)", color=YELLOW, indent=0.5)
            self.hold()

        with self.voice("s2_07"):
            bd.clear()
            bd = Board(self, left=0.6, top=2.4, scale=0.72, buff=0.36)
            bd.line(r"q_s = -\frac{S_y}{I_{xx}}\int_0^s t\,y\,ds", reason="$S_x = 0,\\ I_{xy} = 0$")
            ld = load_arrow(sec.P(0, -2.2), sec.P(0, -1.2), r"S_y", direction=LEFT)
            o1 = sec.dot(B, -1, YELLOW)
            self.play(FadeIn(o1), FadeIn(ld))
            st = Tx(r"start at 1: $q = 0$", color=YELLOW).scale(0.55).next_to(o1, RIGHT, buff=0.15)
            self.play(FadeIn(st))
            self.hold()

        f12 = flow_fill(sec, *W[0], q12, 1.6)
        f23 = flow_fill(sec, *W[1], q23, 1.6)
        f34 = flow_fill(sec, *W[2], q34, 1.6)
        with self.voice("s2_08"):
            bd.line(r"1\to2:\ \ y = -\tfrac{h}{2}:\quad q_{12} = -\frac{S_y}{I_{xx}}\,t\Big(-\frac{h}{2}\Big)s_1", below=True,
                    reason="$y$ is constant along the flange")
            bd.line(r"q_{12} = \frac{6\,S_y\,s_1}{h^2\big(1 + \tfrac{6b}{h}\big)}", color=Q_FILL, indent=0.5, reason="linear in $s_1$")
            self.play(FadeOut(st), FadeIn(f12))
            self.hold()

        with self.voice("s2_09"):
            l = bd.line(r"q_2 = \frac{6\,S_y\,b}{h^2\big(1 + \tfrac{6b}{h}\big)}", color=Q_FILL, indent=0.5, reason="at $s_1 = b$")
            q2l = T("q_2", color=Q_FILL).scale(0.6).next_to(sec.P(0, -1), DOWN, buff=0.55).shift(RIGHT * 0.2)
            self.play(FadeIn(q2l))
            self.hold()

        with self.voice("s2_10"):
            bd.line(r"2\to3:\ \ q_{23} = -\frac{S_y t}{I_{xx}}\Big(-\frac{h}{2}s_2 + \frac{s_2^2}{2}\Big) + q_2", reason="parabola, peak at $y=0$", below=True)
            self.play(FadeIn(f23))
            bd.line(r"3\to4:\ \text{falls linearly to } q_4 = 0\ \checkmark", color=Q_COL)
            self.play(FadeIn(f34))
            self.hold()
        bd.clear()

        Opt = sec.P(0, 0)
        with self.voice("s2_11"):
            self.play(Transform(hdr, header("Moments about the middle of the web")))
            od = Dot(Opt, color=WHITE)
            ol = T("O", color=WHITE).scale(0.6).next_to(od, RIGHT, buff=0.1)
            self.play(FadeIn(od), FadeIn(ol), f23.animate.set_opacity(0.15))
            note = Tx(r"web force passes through $O$: no moment", color=REASON).scale(0.6).move_to([3.4, 2.3, 0])
            self.play(FadeIn(note))
            self.hold()

        with self.voice("s2_12"):
            Fb = Arrow(sec.P(B * 0.85, -1.35), sec.P(B * 0.15, -1.35), buff=0, color=P_COL, stroke_width=6)
            Ft = Arrow(sec.P(B * 0.15, 1.35), sec.P(B * 0.85, 1.35), buff=0, color=P_COL, stroke_width=6)
            Fbl = T("F", color=P_COL).scale(0.7).next_to(Fb, DOWN, buff=0.05)
            Ftl = T("F", color=P_COL).scale(0.7).next_to(Ft, UP, buff=0.05)
            self.play(GrowArrow(Fb), GrowArrow(Ft), FadeIn(Fbl), FadeIn(Ftl))
            bd = Board(self, left=0.6, top=1.6, scale=0.75, buff=0.4)
            bd.line(r"F = \tfrac{1}{2}\,b\,q_2 = \frac{3\,S_y\,b^2}{h^2\big(1 + \tfrac{6b}{h}\big)}", reason="area of the flange triangle", below=True)
            bd.line(r"\text{couple of the flanges} = F\,h")
            self.hold()

        with self.voice("s2_13"):
            bd.line(r"S_y\,e = F\,h", reason="load moment balances the couple")
            l = bd.line(r"e = \frac{3\,b^2}{h\big(1 + \tfrac{6b}{h}\big)} = \frac{3\,b^2}{h + 6b}", color=SC_COL)
            bd.box(l, SC_COL)
            sd = Dot(sec.P(-E, 0), color=SC_COL, radius=0.09)
            sdl = T("S", color=SC_COL).scale(0.8).next_to(sd, LEFT, buff=0.12)
            el = dim_line(sec.P(-E, -0.35), sec.P(0, -0.35), "e", (0, 0))
            el[1].next_to(el[0], DOWN, buff=0.05)
            self.play(FadeIn(sd), FadeIn(sdl), FadeIn(el), FadeOut(ld))
            out = Tx(r"outside the section,\\behind the web", color=SC_COL).scale(0.55).next_to(sd, UP, buff=0.5)
            self.play(FadeIn(out))
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not hdr and not isinstance(m, ValueTracker)])))

        with self.voice("s2_14"):
            self.play(FadeOut(hdr), run_time=0.4)
            h, rows = recap(self, [
                r"1.\ Apply a load (e.g.\ $S_y$) and find the shear flow $q_s$.",
                r"2.\ Pick a moment center where many walls pass through.",
                r"3.\ Moment of the load $=$ moment of the shear flows.",
                r"4.\ Solve for the shear center coordinate. Repeat with $S_x$ if needed.",
            ], title="Finding the shear center of an open section")
            for rr in rows:
                self.play(FadeIn(rr, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(VGroup(h, rows)))
