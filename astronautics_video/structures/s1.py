"""Part 1: shear flow in thin-walled beams."""
from scommon import *  # noqa: F401,F403


def airfoil_box(center, scale=1.0):
    """A stylised wing section: airfoil skin, two spars, a few stringers."""
    xs = np.linspace(0, 1, 60)
    yt = 0.6 * (0.2969 * np.sqrt(xs) - 0.126 * xs - 0.3516 * xs ** 2 + 0.2843 * xs ** 3 - 0.1036 * xs ** 4)
    up = [np.array([x * 6 - 3, y * 6, 0]) for x, y in zip(xs, yt)]
    lo = [np.array([x * 6 - 3, -y * 6, 0]) for x, y in zip(xs, yt)][::-1]
    skin = VMobject(stroke_color=WALL, stroke_width=4).set_points_smoothly(up + lo + [up[0]])
    g = VGroup(skin)
    for xf in (0.2, 0.6):
        y = 0.6 * (0.2969 * np.sqrt(xf) - 0.126 * xf - 0.3516 * xf ** 2 + 0.2843 * xf ** 3 - 0.1036 * xf ** 4) * 6
        g.add(Line([xf * 6 - 3, -y, 0], [xf * 6 - 3, y, 0], color=B_COL, stroke_width=6))
    for xf in (0.3, 0.4, 0.5):
        y = 0.6 * (0.2969 * np.sqrt(xf) - 0.126 * xf - 0.3516 * xf ** 2 + 0.2843 * xf ** 3 - 0.1036 * xf ** 4) * 6
        g.add(Dot([xf * 6 - 3, y - 0.05, 0], radius=0.06, color=Q_COL), Dot([xf * 6 - 3, -y + 0.05, 0], radius=0.06, color=Q_COL))
    return g.scale(scale).move_to(center)


class S1Concept(SLesson):
    def construct(self):
        with self.voice("s1_01"):
            card = s_title(self, 1, "Shear Flow in Thin-Walled Beams", "how a shear load travels around the walls")
            self.wait(1.0)
            self.play(card.animate.scale(0.6).to_edge(UP, buff=0.4))
            wing = airfoil_box(DOWN * 0.8, 1.3)
            self.play(Create(wing[0]), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(m) for m in wing[1:]], lag_ratio=0.1))
            labs = VGroup(Tx("skin", color=WALL).scale(0.55).next_to(wing[0], UP, buff=0.1),
                          Tx("spars", color=B_COL).scale(0.55).next_to(wing[1], DOWN, buff=0.4),
                          Tx("stringers", color=Q_COL).scale(0.55).next_to(wing, DOWN, buff=0.2))
            self.play(FadeIn(labs))
            self.hold()
        self.play(FadeOut(VGroup(card, wing, labs)))

        # ---- why shear: moment varies along the beam
        with self.voice("s1_02"):
            hdr = header("Why does a shear load create shear flow?")
            self.play(FadeIn(hdr))
            root, tip = np.array([-5.0, 1.0, 0]), np.array([1.5, 1.0, 0])
            beam = Rectangle(width=6.5, height=0.7, color=WALL, fill_color="#20283A", fill_opacity=1).move_to((root + tip) / 2)
            wallh = VGroup(Line([-5.0, 0.1, 0], [-5.0, 1.9, 0], color=WALL, stroke_width=5),
                           *[Line([-5.0, y, 0], [-5.3, y - 0.25, 0], color=DIM, stroke_width=2) for y in np.linspace(0.2, 1.9, 8)])
            ld = load_arrow(tip + RIGHT * 0.0 + DOWN * 0.0 + UP * 1.2, tip + UP * 0.35, r"S_y")
            self.play(FadeIn(wallh), FadeIn(beam))
            self.play(GrowArrow(ld[0]), FadeIn(ld[1]))
            ax = Line([-5.0, -1.6, 0], [1.5, -1.6, 0], color=DIM)
            tri = Polygon([-5.0, -1.6, 0], [1.5, -1.6, 0], [-5.0, -3.3, 0], color=P_COL, fill_color=P_COL, fill_opacity=0.3)
            ml = T(r"M_x(z)", color=P_COL).scale(0.7).next_to(tri, LEFT, buff=0.1)
            self.play(Create(ax), DrawBorderThenFill(tri), FadeIn(ml), run_time=1.5)
            note = Tx(r"moment grows away from the tip\\$\Rightarrow$ bending stress $\sigma_z$ grows\\$\Rightarrow$ shear must balance the change",
                      color=YELLOW).scale(0.6).move_to([4.6, -1.0, 0])
            dm = T(r"\frac{dM_x}{dz} = S_y", color=Q_COL).scale(0.8).move_to([4.6, 1.2, 0])
            self.play(FadeIn(note))
            self.play(Write(dm))
            self.hold()
        self.play(FadeOut(VGroup(beam, wallh, ld, ax, tri, ml, note, dm)))

        # ---- vocabulary on a channel
        sec = Sec((-3.8, -0.6), 1.5)
        chan = VGroup(sec.wall((1, -1), (0, -1)), sec.wall((0, -1), (0, 1)), sec.wall((0, 1), (1, 1)))
        with self.voice("s1_03"):
            self.play(Transform(hdr, header("Vocabulary")))
            self.play(Create(chan), run_time=1.5)
            sarr = CurvedArrow(sec.P(1.0, -1.25), sec.P(-0.25, -0.3), color=YELLOW, angle=-PI / 3)
            sl = T("s", color=YELLOW).scale(0.8).next_to(sarr, LEFT, buff=0.05)
            o = sec.dot(1, -1, YELLOW)
            ol = Tx("origin of $s$", color=YELLOW).scale(0.5).next_to(o, DR, buff=0.05)
            zdot = VGroup(Circle(radius=0.13, color=WHITE, stroke_width=2), Dot(radius=0.04)).move_to(sec.P(1.6, 0))
            zl = Tx(r"$z$ out of the page\\(along the beam)", color=DIM).scale(0.5).next_to(zdot, RIGHT, buff=0.15)
            tl = Tx(r"thickness $t(s)$", color=WALL).scale(0.55).next_to(sec.P(0, 0.2), LEFT, buff=0.2)
            self.play(Create(sarr), FadeIn(sl), FadeIn(o), FadeIn(ol))
            self.play(FadeIn(zdot), FadeIn(zl))
            self.play(FadeIn(tl))
            self.hold()

        with self.voice("s1_04"):
            asm = VGroup(*[Tx(r"$\bullet$\ " + x).scale(0.62) for x in (
                r"stresses are constant through the thickness",
                r"shear stress normal to the wall is negligible",
                r"thin walls: drop $t^2,\ t^3,\ \dots$ terms",
                r"uniform section along the beam")]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            asm.move_to([3.4, 0.6, 0])
            ah = Tx("Assumptions", color=B_COL).scale(0.75).next_to(asm, UP, buff=0.35).align_to(asm, LEFT)
            self.play(FadeIn(ah))
            for m in asm:
                self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(0.6)
            self.hold()

        with self.voice("s1_05"):
            self.play(FadeOut(VGroup(asm, ah)))
            qdef = T(r"q = \tau\, t", color=Q_FILL).scale(1.1).move_to([3.4, 1.8, 0])
            qu = Tx(r"shear flow: force per unit length of wall", color=Q_FILL).scale(0.6).next_to(qdef, DOWN, buff=0.25)
            self.play(Write(qdef), FadeIn(qu))
            # water-like flow: dots travelling along the walls
            path = VMobject().set_points_as_corners([sec.P(1, -1), sec.P(0, -1), sec.P(0, 1), sec.P(1, 1)])
            dots = VGroup(*[Dot(radius=0.06, color=Q_FILL) for _ in range(10)])
            tr = ValueTracker(0)
            for i, dd in enumerate(dots):
                dd.add_updater(lambda m, i=i: m.move_to(path.point_from_proportion(((tr.get_value() + i / 10) % 1))))
            self.add(tr, dots)
            pos = Tx(r"positive in the direction of increasing $s$", color=REASON).scale(0.55).next_to(qu, DOWN, buff=0.3)
            self.play(FadeIn(pos), tr.animate.set_value(1.0), run_time=max(2.0, self.left() - 0.3), rate_func=linear)
            for dd in dots:
                dd.clear_updaters()
        self.play(FadeOut(VGroup(chan, sarr, sl, o, ol, zdot, zl, tl, qdef, qu, pos, dots)))

        # ---- element equilibrium
        A0 = np.array([-5.6, -1.2, 0])
        W, H = 3.6, 2.2
        rect = Rectangle(width=W, height=H, color=WALL, fill_color="#20283A", fill_opacity=1).move_to(A0 + np.array([W / 2, H / 2, 0]))
        zax = Arrow(A0 + DOWN * 0.6, A0 + DOWN * 0.6 + RIGHT * 1.2, buff=0, color=DIM, stroke_width=3)
        sax = Arrow(A0 + DOWN * 0.6, A0 + DOWN * 0.6 + UP * 1.0, buff=0, color=DIM, stroke_width=3)
        zl = T("z", color=DIM).scale(0.6).next_to(zax, RIGHT, buff=0.05)
        sl = T("s", color=DIM).scale(0.6).next_to(sax, UP, buff=0.05)
        dz = T(r"\delta z", color=DIM).scale(0.6).next_to(rect, DOWN, buff=0.1)
        ds = T(r"\delta s", color=DIM).scale(0.6).move_to(rect.get_corner(UL) + np.array([0.35, -0.35, 0]))
        with self.voice("s1_06"):
            self.play(Transform(hdr, header("Equilibrium of a tiny piece of wall")))
            self.play(FadeIn(rect), GrowArrow(zax), GrowArrow(sax), FadeIn(zl), FadeIn(sl), FadeIn(dz))
            left = Arrow(rect.get_left() + RIGHT * 0.05, rect.get_left() + LEFT * 0.9, buff=0, color=P_COL, stroke_width=6)
            right = Arrow(rect.get_right() + LEFT * 0.05, rect.get_right() + RIGHT * 1.1, buff=0, color=P_COL, stroke_width=7)
            ll = T(r"\sigma_z", color=P_COL).scale(0.7).next_to(left, UP, buff=0.05)
            rl = T(r"\sigma_z + \frac{\partial\sigma_z}{\partial z}\delta z", color=P_COL).scale(0.6).next_to(right, UP, buff=0.05).shift(RIGHT * 0.45)
            self.play(GrowArrow(left), FadeIn(ll))
            self.play(GrowArrow(right), FadeIn(rl))
            self.hold()

        with self.voice("s1_07"):
            bot = Arrow(rect.get_bottom() + RIGHT * 0.9, rect.get_bottom() + LEFT * 0.9, buff=0, color=Q_FILL, stroke_width=5)
            top = Arrow(rect.get_top() + LEFT * 1.0, rect.get_top() + RIGHT * 1.0, buff=0, color=Q_FILL, stroke_width=6)
            bl = T("q", color=Q_FILL).scale(0.7).next_to(bot, DOWN, buff=0.35)
            tl = T(r"q + \frac{\partial q}{\partial s}\delta s", color=Q_FILL).scale(0.6).next_to(top, UP, buff=0.05)
            self.play(GrowArrow(bot), FadeIn(bl))
            self.play(GrowArrow(top), FadeIn(tl))
            self.play(FadeIn(ds))
            self.hold()

        with self.voice("s1_08"):
            bd = Board(self, left=-0.8, top=2.4, scale=0.66, buff=0.4)
            bd.line(r"\Big(\sigma_z + \frac{\partial\sigma_z}{\partial z}\delta z\Big)t\,\delta s - \sigma_z t\,\delta s"
                    r" + \Big(q + \frac{\partial q}{\partial s}\delta s\Big)\delta z - q\,\delta z = 0",
                    reason="sum of forces in $z$ = 0 (stress $\\times$ area, flow $\\times$ length)", below=True, rt=2.5)
            self.hold()

        with self.voice("s1_09"):
            bd.line(r"\frac{\partial\sigma_z}{\partial z}\,t\,\delta s\,\delta z + \frac{\partial q}{\partial s}\,\delta s\,\delta z = 0",
                    reason="$\\sigma_z t\\,\\delta s$ and $q\\,\\delta z$ cancel", below=True)
            l = bd.line(r"\frac{\partial q}{\partial s} + t\,\frac{\partial\sigma_z}{\partial z} = 0", color=YELLOW,
                        reason="divide by $\\delta s\\,\\delta z$", scale=0.95)
            bd.box(l)
            self.hold()

        with self.voice("s1_10"):
            words = Tx(r"$\sigma_z$ changes along the beam\\$\Rightarrow$ $q$ must change around the wall", color=YELLOW).scale(0.7)
            words.next_to(bd.lines[-1], DOWN, buff=0.6).align_to(bd.lines[-1], LEFT)
            self.play(Write(words))
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(rect, zax, sax, zl, sl, dz, ds, left, right, ll, rl, bot, top, bl, tl, words)))

        # ---- bending stress -> q formula
        with self.voice("s1_11"):
            self.play(Transform(hdr, header("From bending stress to shear flow")))
            bd = Board(self, left=-6.3, top=2.4, scale=0.75, buff=0.45)
            bd.line(r"\sigma_z = \Big(\frac{M_y I_{xx} - M_x I_{xy}}{I_{xx}I_{yy} - I_{xy}^2}\Big)x + \Big(\frac{M_x I_{yy} - M_y I_{xy}}{I_{xx}I_{yy} - I_{xy}^2}\Big)y",
                    reason="unsymmetrical bending, $x,y$ from the centroid", below=True, rt=2.5)
            self.hold()

        with self.voice("s1_12"):
            bd.line(r"\frac{\partial M_x}{\partial z} = S_y,\qquad \frac{\partial M_y}{\partial z} = S_x", reason="rate of change of moment = shear")
            bd.line(r"\frac{\partial\sigma_z}{\partial z} = \Big(\frac{S_x I_{xx} - S_y I_{xy}}{I_{xx}I_{yy} - I_{xy}^2}\Big)x + \Big(\frac{S_y I_{yy} - S_x I_{xy}}{I_{xx}I_{yy} - I_{xy}^2}\Big)y", rt=2.5)
            self.hold()

        with self.voice("s1_13"):
            bd.clear()
            bd = Board(self, left=-6.3, top=2.4, scale=0.75, buff=0.45)
            bd.line(r"\frac{\partial q}{\partial s} = -\,t\,\frac{\partial\sigma_z}{\partial z}", reason="the equilibrium equation")
            bd.line(r"q_s - \underbrace{q_{s=0}}_{0\ \text{(free edge)}} = -\int_0^s t\,\frac{\partial\sigma_z}{\partial z}\,ds", reason="integrate around the wall")
            l = bd.line(r"q_s = -\Big(\frac{S_x I_{xx} - S_y I_{xy}}{I_{xx}I_{yy} - I_{xy}^2}\Big)\int_0^s t\,x\,ds - \Big(\frac{S_y I_{yy} - S_x I_{xy}}{I_{xx}I_{yy} - I_{xy}^2}\Big)\int_0^s t\,y\,ds",
                        color=YELLOW, rt=2.5)
            bd.box(l)
            self.hold()

        with self.voice("s1_14"):
            l2 = bd.line(r"I_{xy} = 0:\qquad q_s = -\frac{S_x}{I_{yy}}\int_0^s t\,x\,ds - \frac{S_y}{I_{xx}}\int_0^s t\,y\,ds", color=Q_COL,
                         reason="section with an axis of symmetry")
            bd.box(l2, Q_COL)
            self.hold()
        bd.clear()

        # ---- meaning: first moment of swept area
        sec = Sec((-4.4, -0.9), 1.6)
        b, hh = 1.0, 2.0
        walls = [((b, -1), (0, -1)), ((0, -1), (0, 1)), ((0, 1), (b, 1))]
        chan = VGroup(*[sec.wall(p0, p1) for p0, p1 in walls])
        Ix = hh ** 3 / 12 + 2 * b * (hh / 2) ** 2

        def qprof(sv):
            """|q| (Sy = t = 1) after sweeping length sv from the bottom free edge."""
            if sv <= b:
                return (hh / 2) * sv / Ix
            if sv <= b + hh:
                s2 = sv - b
                return ((hh / 2) * b + (hh / 2) * s2 - s2 ** 2 / 2) / Ix
            s3 = sv - b - hh
            return ((hh / 2) * b - (hh / 2) * s3) / Ix
        sw = ValueTracker(0.0)
        total = 2 * b + hh
        lens = [b, hh, b]

        def swept():
            g = VGroup()
            v = sw.get_value()
            start = 0.0
            for (p0, p1), Lw in zip(walls, lens):
                frac = np.clip((v - start) / Lw, 0, 1)
                if frac > 0:
                    a_, b_ = np.array(p0, float), np.array(p1, float)
                    g.add(Line(sec.P(*a_), sec.P(*(a_ + frac * (b_ - a_))), color=YELLOW, stroke_width=9))
                    g.add(flow_fill(sec, tuple(a_), tuple(a_ + frac * (b_ - a_)),
                                    lambda u, st=start, L=Lw, f=frac: qprof(st + u * f * L), 1.6,
                                    side=1 if p0[1] == p1[1] and p0[1] < 0 else (-1 if p0[1] == p1[1] else 1)))
                start += Lw
            return g
        live = always_redraw(swept)
        with self.voice("s1_15"):
            self.play(Transform(hdr, header("What the integral means")))
            self.play(Create(chan))
            na = DashedLine(sec.P(-0.6, 0), sec.P(1.5, 0), color=DIM)
            nal = Tx("neutral axis", color=DIM).scale(0.5).next_to(na, RIGHT, buff=0.1)
            self.play(Create(na), FadeIn(nal))
            mean = T(r"\int_0^s t\,y\,ds", r"= \text{first moment of the wall swept so far}").scale(0.7).move_to([2.6, 2.3, 0])
            mean[0].set_color(YELLOW)
            self.play(Write(mean))
            self.add(live)
            self.play(sw.animate.set_value(total), run_time=max(3.0, self.left() - 3.0), rate_func=linear)
            pk = Tx(r"builds up along the flange, peaks at the neutral axis,\\falls back to zero at the other free edge", color=Q_FILL).scale(0.6)
            pk.next_to(mean, DOWN, buff=0.5)
            self.play(FadeIn(pk))
            self.hold()
        live.clear_updaters()
        self.play(FadeOut(VGroup(chan, na, nal, mean, live, pk)))

        with self.voice("s1_16"):
            self.play(FadeOut(hdr), run_time=0.4)
            h, rows = recap(self, [
                r"1.\ Find the centroid and $I_{xx},\ I_{yy},\ I_{xy}$.",
                r"2.\ Start at a free edge, where $q = 0$.",
                r"3.\ Integrate wall by wall, carrying $q$ across each corner.",
                r"4.\ Check: $q = 0$ at the other free edge; flows add up to the load.",
            ], title="Recipe: shear flow in an open section")
            for rr in rows:
                self.play(FadeIn(rr, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))
