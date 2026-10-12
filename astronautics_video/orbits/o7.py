"""Part 7: parabolic and hyperbolic trajectories."""
from ocommon import *  # noqa: F401,F403

PP = 1.6                      # parabola semi-latus rectum
EH, AH = 1.6, -1.0            # hyperbola e, a
PH = AH * (1 - EH ** 2)
TINF = np.arccos(-1 / EH)


class O7Concept(OLesson):
    def construct(self):
        orb = Orb(focus=(-2.4, -0.4), k=1.0)
        par = orb.conic(PP, 1.0, -2.14, 2.14, color=YELLOW, width=4)
        with self.voice("o7_01"):
            t = o_title(self, 7, "Parabolas and Hyperbolas", "the trajectories that never come back")
            self.wait(1.2)
            self.play(FadeOut(t))
            hdr = header("The parabola: $e = 1$")
            self.play(FadeIn(hdr))
            self.play(FadeIn(earth(orb.f, 0.16)), Create(par), run_time=2)
            bd = Board(self, left=1.0, top=2.7, scale=0.8, buff=0.42)
            bd.line(r"e = 1,\qquad \mathcal E = 0,\qquad a\to\infty", color=YELLOW, reason="the border case", below=True)
            self.hold()

        with self.voice("o7_02"):
            bd.line(r"\frac{v^2}{2} - \frac{\mu}{r} = 0")
            l = bd.line(r"v = \sqrt{\frac{2\mu}{r}} = v_{esc}", color=YELLOW, reason="escape speed, everywhere")
            self.hold()

        with self.voice("o7_03"):
            bd.line(r"r = \frac{p}{1 + \cos\theta},\qquad r_p = \frac{p}{2}")
            bd.line(r"\theta\to 180^\circ:\ r\to\infty", indent=0.4, reason="the arms never close")
            rp = Line(orb.f, orb.at(PP, 1.0, 0), color=Q_COL, stroke_width=5)
            rpl = T(r"r_p = p/2", color=Q_COL).scale(0.55).next_to(rp, DOWN, buff=0.1)
            self.play(Create(rp), FadeIn(rpl))
            self.hold()
        bd.clear()

        th0 = 1.4
        q = orb.at(PP, 1.0, th0)
        er, et = orb.unit(th0), orb.unit(th0 + PI / 2)
        g0 = th0 / 2
        vdir = np.sin(g0) * er + np.cos(g0) * et
        with self.voice("o7_04"):
            self.play(Transform(hdr, header("Flight-path angle on a parabola")))
            rl = Line(orb.f, q, color=WHITE, stroke_width=3)
            tha = Arc(radius=0.5, start_angle=0, angle=th0, arc_center=orb.f, color=B_COL)
            thl = T(r"\theta", color=B_COL).scale(0.6).move_to(orb.f + 0.75 * orb.unit(th0 / 2))
            self.play(Create(rl), FadeIn(planet(q)), Create(tha), FadeIn(thl))
            bd = Board(self, left=1.0, top=2.7, scale=0.8, buff=0.42)
            bd.line(r"\tan\gamma = \frac{\sin\theta}{1 + \cos\theta}", reason="$e = 1$")
            bd.line(r"= \frac{2\sin\frac\theta2\cos\frac\theta2}{2\cos^2\frac\theta2}", indent=0.5, reason="half-angle identities")
            self.hold()

        with self.voice("o7_05"):
            l = bd.line(r"\tan\gamma = \tan\frac{\theta}{2}\ \Rightarrow\ \gamma = \frac{\theta}{2}", color=YELLOW)
            bd.box(l)
            hz = DashedLine(q - 0.6 * et, q + 1.4 * et, color=ET_COL)
            va = Arrow(q, q + 1.4 * vdir, buff=0, color=VEL, stroke_width=5, tip_length=0.16)
            ga = Arc(radius=0.75, start_angle=th0 + PI / 2, angle=-g0, arc_center=q, color=YELLOW, stroke_width=4)
            gl = T(r"\gamma", color=YELLOW).scale(0.6).move_to(q + 1.0 * (np.cos(th0 + PI / 2 - g0 / 2) * RIGHT + np.sin(th0 + PI / 2 - g0 / 2) * UP))
            self.play(Create(hz), GrowArrow(va), Create(ga), FadeIn(gl))
            bd.line(r"\theta\to180^\circ:\ \gamma\to 90^\circ", indent=0.4, reason="heads straight out")
            self.hold()
        bd.clear()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker) and m is not hdr])))

        # ------------------------------------------------ hyperbola
        orb = Orb(focus=(-2.4, -0.3), k=1.1)
        hyp = orb.conic(PH, EH, -1.88, 1.88, color=YELLOW, width=4)
        with self.voice("o7_06"):
            self.play(Transform(hdr, header("The hyperbola: $e > 1$")))
            self.play(FadeIn(earth(orb.f, 0.16)), Create(hyp), run_time=2)
            bd = Board(self, left=1.0, top=2.7, scale=0.8, buff=0.42)
            bd.line(r"\mathcal E > 0\ \text{ and }\ \mathcal E = -\frac{\mu}{2a}\ \Rightarrow\ a < 0", color=YELLOW, reason="keep using the same formulas", below=True)
            self.hold()

        with self.voice("o7_07"):
            bd.line(r"r_p = \underbrace{a}_{<0}\,\underbrace{(1 - e)}_{<0} > 0")
            bd.line(r"p = a\,(1 - e^2) > 0", reason="both factors negative")
            self.hold()
        bd.clear()

        asym_l = VGroup(*[DashedLine(orb.f, orb.f + 4.2 * orb.unit(s * TINF), color=V_COL) for s in (1, -1)])
        with self.voice("o7_08"):
            self.play(Transform(hdr, header("The asymptote: where $r\\to\\infty$")))
            bd = Board(self, left=1.0, top=2.7, scale=0.8, buff=0.42)
            bd.line(r"1 + e\cos\theta = 0")
            l = bd.line(r"\theta_\infty = \cos^{-1}\!\Big(-\frac{1}{e}\Big)", color=V_COL, reason="between $90^\\circ$ and $180^\\circ$")
            bd.box(l, color=V_COL)
            self.play(Create(asym_l))
            tl = T(r"\theta_\infty", color=V_COL).scale(0.6).move_to(orb.f + 0.95 * orb.unit(TINF / 2) + 0.15 * UP)
            ta = Arc(radius=0.6, start_angle=0, angle=TINF, arc_center=orb.f, color=V_COL)
            self.play(Create(ta), FadeIn(tl))
            bd.line(r"-\theta_\infty < \theta < \theta_\infty", indent=0.4, reason="the only angles it can reach")
            self.hold()

        with self.voice("o7_09"):
            bd.line(r"v^2 = \mu\Big(\frac{2}{r} - \frac{1}{a}\Big)\ \xrightarrow{\ r\to\infty\ }\ v_\infty^2 = -\frac{\mu}{a}", reason="vis-viva", below=True)
            l = bd.line(r"\mathcal E = \frac{v_\infty^2}{2}", color=YELLOW, reason="hyperbolic excess speed")
            bd.box(l)
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(ta, tl)))

        # geometry
        ca = abs(AH) * EH
        ctr = orb.P(ca, 0)
        bb = abs(AH) * np.sqrt(EH ** 2 - 1)
        with self.voice("o7_10"):
            self.play(Transform(hdr, header("Hyperbola geometry")))
            cdot = Dot(ctr, color=WHITE, radius=0.05)
            cl = Tx("center", color=WHITE).scale(0.45).next_to(ctr, DOWN, buff=0.12)
            asym = VGroup(*[DashedLine(ctr - 3.3 * orb.unit(s * TINF), ctr + 4.0 * orb.unit(s * TINF), color=V_COL) for s in (1, -1)])
            self.play(FadeOut(asym_l), FadeIn(cdot), FadeIn(cl), Create(asym))
            box = Rectangle(width=2 * abs(AH) * orb.k, height=2 * bb * orb.k, color=B_COL, stroke_width=2).move_to(ctr)
            self.play(Create(box))
            al = brace_between_pts(orb.P(ca - abs(AH), 0), ctr, r"|a|", B_COL, DOWN)
            bl = brace_between_pts(orb.P(ca + abs(AH), 0), orb.P(ca + abs(AH), bb), r"b", B_COL, RIGHT)
            cl2 = brace_between_pts(orb.f, ctr, r"c = |a|e", Q_COL, UP)
            cl2.shift(UP * (bb * orb.k + 0.1))
            self.play(FadeIn(al), FadeIn(bl), FadeIn(cl2))
            bd = Board(self, left=2.4, top=2.7, scale=0.75, buff=0.42)
            bd.line(r"b = |a|\sqrt{e^2 - 1}", color=B_COL)
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(box, al, bl, cl2, cl, cdot)))

        # turning angle
        vin = np.array([-np.cos(TINF), np.sin(TINF), 0])
        vout = np.array([np.cos(TINF), np.sin(TINF), 0])
        with self.voice("o7_11"):
            self.play(Transform(hdr, header("The turning angle $\\delta$")))
            pin = orb.at(PH, EH, -1.75)
            pout = orb.at(PH, EH, 1.75)
            ain = Arrow(pin - 0.2 * vin, pin + 1.1 * vin, buff=0, color=Q_COL, stroke_width=6, tip_length=0.2)
            aout = Arrow(pout, pout + 1.1 * vout, buff=0, color=P_COL, stroke_width=6, tip_length=0.2)
            self.play(GrowArrow(ain), GrowArrow(aout))
            o_ = np.array([3.6, -2.7, 0])
            a1 = Arrow(o_, o_ + 1.8 * vin, buff=0, color=Q_COL, stroke_width=6, tip_length=0.2)
            a2 = Arrow(o_, o_ + 1.8 * vout, buff=0, color=P_COL, stroke_width=6, tip_length=0.2)
            l1 = Tx("in", color=Q_COL).scale(0.55).next_to(a1.get_end(), RIGHT, buff=0.1)
            l2 = Tx("out", color=P_COL).scale(0.55).next_to(a2.get_end(), LEFT, buff=0.1)
            darc = Arc(radius=0.8, start_angle=np.arctan2(vin[1], vin[0]), angle=np.arctan2(vout[1], vout[0]) - np.arctan2(vin[1], vin[0]), arc_center=o_, color=YELLOW, stroke_width=4)
            dl = T(r"\delta", color=YELLOW).scale(0.7).next_to(darc, UP, buff=0.08)
            self.play(TransformFromCopy(ain, a1), TransformFromCopy(aout, a2), FadeIn(l1), FadeIn(l2))
            self.play(Create(darc), FadeIn(dl))
            self.hold()

        with self.voice("o7_12"):
            bd = Board(self, left=1.6, top=2.7, scale=0.78, buff=0.42)
            bd.line(r"\text{out: along } \theta_\infty,\quad \text{in: along } -\theta_\infty \text{ (inward)}")
            l = bd.line(r"\delta = 2\theta_\infty - 180^\circ", color=YELLOW)
            self.hold()

        with self.voice("o7_13"):
            bd.line(r"\sin\frac{\delta}{2} = \sin(\theta_\infty - 90^\circ) = -\cos\theta_\infty")
            l = bd.line(r"\sin\frac{\delta}{2} = \frac{1}{e}", color=YELLOW, reason="large $e$: small turn")
            bd.box(l)
            self.hold()
        bd.clear()
        self.play(FadeOut(VGroup(a1, a2, l1, l2, darc, dl)))

        with self.voice("o7_14"):
            self.play(Transform(hdr, header("The other branch")))
            F2 = orb.P(2 * ca, 0)
            other = VMobject(stroke_color=DIM, stroke_width=3)
            # mirror image of our branch through the center
            pts = [2 * ctr - orb.at(PH, EH, t_) for t_ in np.linspace(-1.75, 1.75, 120)]
            other.set_points_smoothly(pts)
            other = DashedVMobject(other, num_dashes=40)
            fd = Dot(F2, color=DIM, radius=0.06)
            fl = Tx("empty focus", color=DIM).scale(0.5).next_to(F2, DOWN, buff=0.12)
            self.play(Create(other), FadeIn(fd), FadeIn(fl), run_time=2)
            note = Tx(r"needs a \emph{repulsive} force:\\ never flown by a satellite", color=DIM).scale(0.55).move_to([4.6, 2.3, 0])
            self.play(FadeIn(note))
            self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)])))

        with self.voice("o7_15"):
            hd = Tx("The four conics", color=YELLOW).scale(1.0).to_edge(UP, buff=0.6)
            rows = [("", r"$e$", r"$a$", r"$\mathcal E$", "speed"),
                    ("circle", r"$0$", r"$>0$", r"$<0$", r"$\sqrt{\mu/r}$"),
                    ("ellipse", r"$0<e<1$", r"$>0$", r"$<0$", r"vis-viva"),
                    ("parabola", r"$1$", r"$\infty$", r"$0$", r"$\sqrt{2\mu/r}$"),
                    ("hyperbola", r"$>1$", r"$<0$", r"$>0$", r"$v_\infty^2 = -\mu/a$")]
            xs = [-4.6, -2.2, -0.2, 1.6, 4.0]
            tab = VGroup()
            for i, row in enumerate(rows):
                g = VGroup()
                for j, c in enumerate(row):
                    m = Tx(c, color=B_COL if (i == 0 or j == 0) else WHITE).scale(0.7).move_to([xs[j], 1.6 - 0.85 * i, 0])
                    g.add(m)
                tab.add(g)
            ul = Line([-5.8, 1.15, 0], [5.6, 1.15, 0], color=DIM)
            self.play(Write(hd), FadeIn(tab[0]), Create(ul))
            for r_ in tab[1:]:
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.8)
                self.wait(max(0.2, (self.left() - 1.0) / 4 - 0.8))
            self.hold()
        self.play(FadeOut(VGroup(hd, tab, ul)))


def brace_between_pts(p0, p1, tex, color, direction):
    br = BraceBetweenPoints(p0, p1, direction=direction, color=color, buff=0.05)
    lab = T(tex, color=color).scale(0.55).next_to(br, direction, buff=0.06)
    return VGroup(br, lab)
