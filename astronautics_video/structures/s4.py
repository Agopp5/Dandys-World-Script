"""Part 4: shear of closed-section beams."""
from scommon import *  # noqa: F401,F403

CEN = np.array([-3.9, -0.5, 0])


def blob(th):
    r = 1.75 + 0.28 * np.cos(2 * th) + 0.12 * np.sin(3 * th)
    return CEN + np.array([1.15 * r * np.cos(th), 0.85 * r * np.sin(th), 0])


def blob_tangent(th):
    e = 1e-4
    v = blob(th + e) - blob(th - e)
    return v / np.linalg.norm(v)


def blob_curve(t0=0.0, t1=TAU, color=WALL, width=5):
    return ParametricFunction(blob, t_range=[t0, t1, 0.02], color=color, stroke_width=width)


def loop_arrows(n=8, color=Q_FILL, length=0.45, t0=0.0):
    g = VGroup()
    for i in range(n):
        th = t0 + TAU * (i + 0.5) / n
        c, tv = blob(th), blob_tangent(th)
        g.add(Arrow(c - tv * length / 2, c + tv * length / 2, buff=0, color=color, stroke_width=4, tip_length=0.15,
                    max_tip_length_to_length_ratio=0.5))
    return g


class S4Concept(SLesson):
    def construct(self):
        with self.voice("s4_01"):
            card = s_title(self, 4, "Closed-Section Beams", "wing boxes and tubes: no free edges")
            self.wait(1.0)
            self.play(card.animate.scale(0.6).to_edge(UP, buff=0.4))
            box = VGroup(Line([-2.5, 1.0, 0], [2.5, 1.2, 0], color=WALL, stroke_width=5),
                         Line([-2.5, -1.4, 0], [2.5, -1.2, 0], color=WALL, stroke_width=5),
                         Line([-2.5, -1.4, 0], [-2.5, 1.0, 0], color=B_COL, stroke_width=7),
                         Line([2.5, -1.2, 0], [2.5, 1.2, 0], color=B_COL, stroke_width=7))
            self.play(Create(box), run_time=1.5)
            lab = Tx(r"a wing box: skins + spars form a closed loop\\no free edge where $q = 0$", color=YELLOW).scale(0.65).next_to(box, DOWN, buff=0.5)
            self.play(FadeIn(lab))
            self.hold()
        self.play(FadeOut(VGroup(card, box, lab)))

        hdr = header("The same integral, one new unknown")
        with self.voice("s4_02"):
            self.play(FadeIn(hdr))
            bd = Board(self, left=-6.3, top=2.4, scale=0.72, buff=0.45)
            bd.line(r"q_s = -\Big(\tfrac{S_x I_{xx} - S_y I_{xy}}{I_{xx}I_{yy} - I_{xy}^2}\Big)\int_0^s t\,x\,ds - \Big(\tfrac{S_y I_{yy} - S_x I_{xy}}{I_{xx}I_{yy} - I_{xy}^2}\Big)\int_0^s t\,y\,ds",
                    reason="same as the open section", below=True)
            l = bd.line(r"\qquad\qquad + \ q_{s,0}", color=YELLOW, reason="unknown shear flow at the origin $s = 0$")
            self.hold()
        bd.clear()

        with self.voice("s4_03"):
            self.play(Transform(hdr, header("Cut it open, then close it")))
            full = blob_curve()
            self.play(Create(full), run_time=1.5)
            cut_th = 0.0
            gap = Line(blob(cut_th) + LEFT * 0.12, blob(cut_th) + RIGHT * 0.12, color=BG, stroke_width=14)
            cutl = Tx("cut ($s = 0$)", color=YELLOW).scale(0.55).next_to(blob(cut_th), RIGHT, buff=0.15)
            self.play(FadeIn(gap), FadeIn(cutl))
            qb = T(r"q_s = ", r"q_b", r" + ", r"q_{s,0}").scale(1.0).move_to([2.8, 2.0, 0])
            qb[1].set_color(Q_FILL)
            qb[3].set_color(YELLOW)
            self.play(Write(qb))
            # basic shear flow on the cut (open) section: zero at the cut, smooth elsewhere
            fill_pts_in = [blob(th) for th in np.linspace(0.02, TAU - 0.02, 120)]
            mag = lambda th: 0.55 * np.sin(th / 2) ** 2 * (1 + 0.3 * np.cos(th))
            fill_pts_out = [blob(th) + (blob(th) - CEN) / np.linalg.norm(blob(th) - CEN) * mag(th) for th in np.linspace(0.02, TAU - 0.02, 120)]
            qbfill = Polygon(*(fill_pts_in + fill_pts_out[::-1]), stroke_width=0, fill_color=Q_FILL, fill_opacity=0.35)
            l1 = Tx(r"$q_b$: open-section flow,\\zero at the cut", color=Q_FILL).scale(0.6).next_to(qb, DOWN, buff=0.4)
            self.play(FadeIn(qbfill), FadeIn(l1))
            self.wait(1.0)
            arr = loop_arrows(8, YELLOW)
            l2 = Tx(r"$q_{s,0}$: a constant flow\\all the way around", color=YELLOW).scale(0.6).next_to(l1, DOWN, buff=0.4)
            self.play(LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.1), FadeIn(l2))
            self.hold()
        self.play(FadeOut(VGroup(gap, cutl, qbfill, arr, l1, l2)), qb.animate.scale(0.8).to_corner(UR, buff=0.4))

        # ---- moment of the shear flow and the enclosed area
        O = CEN + np.array([-0.2, 0.15, 0])
        th0 = 0.9
        with self.voice("s4_04"):
            self.play(Transform(hdr, header("Moments: each piece $q\\,ds$ has a moment arm $p$")))
            od = Dot(O, color=WHITE)
            ol = T("O", color=WHITE).scale(0.6).next_to(od, LEFT, buff=0.1)
            self.play(FadeIn(od), FadeIn(ol))
            c, tv = blob(th0), blob_tangent(th0)
            tline = Line(c - tv * 2.2, c + tv * 1.2, color=DIM, stroke_width=2)
            foot = c + tv * np.dot(O - c, tv)
            pl = DashedLine(O, foot, color=YELLOW)
            plab = T("p", color=YELLOW).scale(0.7).next_to(pl.get_center(), UL, buff=0.05)
            qarr = Arrow(c - tv * 0.3, c + tv * 0.45, buff=0, color=Q_FILL, stroke_width=6)
            qlab = T(r"q\,ds", color=Q_FILL).scale(0.65).next_to(qarr.get_end(), UR, buff=0.05)
            ra = RightAngle(Line(foot, O), Line(foot, c), length=0.15, color=YELLOW)
            self.play(Create(tline), GrowArrow(qarr), FadeIn(qlab))
            self.play(Create(pl), FadeIn(plab), Create(ra))
            m = T(r"dM = p\,q\,ds", color=WHITE).scale(0.85).move_to([2.6, 1.0, 0])
            self.play(Write(m))
            self.hold()

        with self.voice("s4_05"):
            ds_pts = [blob(th0 - 0.12), blob(th0 + 0.12)]
            tri = Polygon(O, *ds_pts, color=Q_COL, fill_color=Q_COL, fill_opacity=0.5, stroke_width=2)
            self.play(FadeIn(tri))
            dA = T(r"\delta A = \tfrac12\,p\,\delta s", color=Q_COL).scale(0.85).next_to(m, DOWN, buff=0.45)
            self.play(Write(dA))
            self.play(FadeOut(VGroup(tline, pl, plab, qarr, qlab, ra)))
            sweep = ValueTracker(0.0)
            fan = always_redraw(lambda: Polygon(O, *[blob(th) for th in np.linspace(0, max(0.05, sweep.get_value()), 80)],
                                                stroke_width=0, fill_color=Q_COL, fill_opacity=0.3))
            self.add(fan, sweep)
            self.play(sweep.animate.set_value(TAU), run_time=4.0, rate_func=linear)
            res = T(r"\oint p\,ds = 2A", color=YELLOW).scale(1.0).next_to(dA, DOWN, buff=0.45)
            al = Tx("$A$ = enclosed area", color=REASON).scale(0.55).next_to(res, DOWN, buff=0.2)
            self.play(Write(res), FadeIn(al))
            self.hold()

        with self.voice("s4_06"):
            fan.clear_updaters()
            self.play(FadeOut(VGroup(m, dA, res, al, tri)))
            bd = Board(self, left=-0.9, top=2.0, scale=0.72, buff=0.4)
            bd.line(r"S_x\eta_0 - S_y\xi_0 = \oint p\,q\,ds", reason="applied moment = moment of the flow")
            bd.line(r"= \oint p\,q_b\,ds + q_{s,0}\oint p\,ds = \oint p\,q_b\,ds + 2A\,q_{s,0}", indent=0.6)
            bd.line(r"\text{choose the moment center on the load's line of action:}")
            bd.line(r"0 = \oint p\,q_b\,ds + 2A\,q_{s,0}", indent=0.6)
            l = bd.line(r"q_{s,0} = -\frac{\oint p\,q_b\,ds}{2A}", color=YELLOW, indent=0.6)
            bd.box(l)
            self.hold()
        bd.clear()
        self.play(FadeOut(fan), FadeOut(od), FadeOut(ol))

        with self.voice("s4_07"):
            self.play(Transform(hdr, header("Closed sections also twist")))
            spin = ValueTracker(0)
            self.add(spin)
            twist = always_redraw(lambda: blob_curve().rotate(0.25 * np.sin(spin.get_value()), about_point=CEN))
            self.remove(full)
            self.add(twist)
            self.play(spin.animate.set_value(TAU), run_time=3.0, rate_func=linear)
            bd = Board(self, left=-0.9, top=1.6, scale=0.8, buff=0.4)
            l = bd.line(r"\frac{d\theta}{dz} = \frac{1}{2A}\oint\frac{q_s}{G\,t}\,ds", color=YELLOW,
                        reason="from $q = G t\\,\\gamma$ and the wall displacements")
            bd.box(l)
            self.hold()

        with self.voice("s4_08"):
            twist.clear_updaters()
            bd.line(r"\text{load through the shear center: } \frac{d\theta}{dz} = 0", below=False)
            bd.line(r"0 = \oint\frac{q_b + q_{s,0}}{G\,t}\,ds", indent=0.6)
            l = bd.line(r"G t\ \text{const}:\quad q_{s,0} = -\frac{\oint q_b\,ds}{\oint ds}", color=YELLOW, indent=0.6)
            bd.box(l)
            self.hold()
        bd.clear()

        with self.voice("s4_09"):
            self.play(FadeOut(twist), FadeOut(qb))
            two = VGroup(
                VGroup(Tx("Load's line of action known", color=B_COL).scale(0.75),
                       T(r"q_{s,0} = -\frac{\oint p\,q_b\,ds}{2A}").scale(0.8),
                       Tx("(moments about a point on it)", color=REASON).scale(0.55)).arrange(DOWN, buff=0.3),
                VGroup(Tx("Looking for the shear center", color=Q_COL).scale(0.75),
                       T(r"q_{s,0} = -\frac{\oint q_b\,ds}{\oint ds}").scale(0.8),
                       Tx("(zero twist), then moments to locate $S$", color=REASON).scale(0.55)).arrange(DOWN, buff=0.3),
            ).arrange(RIGHT, buff=1.4).move_to(DOWN * 0.2)
            self.play(Transform(hdr, header("Two ways to find $q_{s,0}$")))
            self.play(FadeIn(two[0], shift=UP * 0.2))
            self.wait(1.5)
            self.play(FadeIn(two[1], shift=UP * 0.2))
            self.hold()
        self.play(FadeOut(two), FadeOut(hdr))

        with self.voice("s4_10"):
            h, rows = recap(self, [
                r"1.\ Find $I_{xx}$ (and $I_{yy}, I_{xy}$ if needed).",
                r"2.\ Cut the section at a convenient point; compute $q_b$ as if open.",
                r"3.\ Find $q_{s,0}$ from moments or from zero twist.",
                r"4.\ $q_s = q_b + q_{s,0}$; check that the flows add up to the load.",
            ], title="Recipe: shear flow in a closed section")
            for rr in rows:
                self.play(FadeIn(rr, shift=RIGHT * 0.2), run_time=0.6)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.6))
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))
