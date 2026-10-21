"""S11: reading the angles back out of C_PN (BRIEF.md S11)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# facts ---------------------------------------------------------------------------------------------
# the five entries really are what cpn() builds (generic orientation 50 / 40 / 60 deg)
_Om, _i, _w = np.radians(50), np.radians(40), np.radians(60)
_M = cpn(_Om, _i, _w)
assert np.allclose([_M[2, 2], _M[2, 0], _M[2, 1], _M[0, 2], _M[1, 2]],
                   [np.cos(_i), np.sin(_i) * np.sin(_Om), -np.sin(_i) * np.cos(_Om),
                    np.sin(_w) * np.sin(_i), np.cos(_w) * np.sin(_i)])
# and the recipe recovers the angles
assert np.isclose(np.arccos(_M[2, 2]), _i)
assert np.isclose(np.arctan2(_M[2, 0], -_M[2, 1]), _Om)
assert np.isclose(np.arctan2(_M[0, 2], _M[1, 2]), _w)
# Molniya C_PN (Kluever Ex. 3.1): i = 63.4, Omega = 145.0, omega = -90 -> 270
CPN = np.array([[0.2568, 0.3668, -0.8942], [-0.8192, 0.5736, 0.0], [0.5129, 0.7324, 0.4478]])
assert np.isclose(np.degrees(np.arccos(CPN[2, 2])), 63.4, atol=0.05)
assert np.isclose(np.degrees(np.arctan2(CPN[2, 0], -CPN[2, 1])), 145.0, atol=0.05)
W_RAW = np.degrees(np.arctan2(CPN[0, 2], CPN[1, 2]))
assert np.isclose(W_RAW, -90.0) and np.isclose(W_RAW + 360, 270.0)
# arccos cannot tell 145 from 215; atan2 can
A1, A2 = np.radians(145), np.radians(215)
assert np.isclose(np.cos(A1), np.cos(A2))
assert np.isclose(np.degrees(np.arccos(np.cos(A1))), 145) and np.isclose(np.degrees(np.arccos(np.cos(A2))), 145)
assert np.isclose(np.degrees(np.arctan2(np.sin(A1), np.cos(A1))), 145)
assert np.isclose(np.degrees(np.arctan2(np.sin(A2), np.cos(A2))), -145) and np.isclose(-145 + 360, 215)

RX = 3.6                       # center x of the right-hand workspace


class S11_Read_Angles(VScene):
    budget = 197

    def construct(self):
        self.section("Reading the angles back out")

        # left: the five entries from S10
        specs = [r"C_{33}|=|\cos|i",
                 r"C_{31}|=|\sin|i|\sin|\Omega",
                 r"C_{32}|=|-\sin|i|\cos|\Omega",
                 r"C_{13}|=|\sin|\omega|\sin|i",
                 r"C_{23}|=|\cos|\omega|\sin|i"]
        rows = VGroup(*[E(s, size=38) for s in specs]).arrange(DOWN, aligned_edge=LEFT, buff=.3)
        card = panel(rows)
        card.move_to([-4.0, .75, 0])
        r33, r31, r32, r13, r23 = rows

        def slot(m, k):
            m.generate_target()
            m.target.scale(.72).move_to([0, card.get_bottom()[1] - .5 - .68 * k, 0])
            m.target.align_to(card, LEFT).shift(.2 * RIGHT)
            return MoveToTarget(m)

        # 1: i = arccos C33
        i_eq = E(r"i|=|\arccos|C_{33}", size=50).move_to([RX, 2.4, 0])
        self.beat("Now reverse it. The corner entry C three three is cosine i. So i is the arc cosine of C three three.",
                  FadeIn(card), Circumscribe(r33, color=EMBER), Write(i_eq), FadeIn(glow(i_eq[0], EMBER)),
                  w=(.25, .3, .3, .15))

        # 2: arccos range = inclination range
        nl = NumberLine(x_range=[0, 180, 30], length=4.8, color=AXIS, include_numbers=False)
        nl.move_to([RX - .2, .1, 0])
        ticks = VGroup(*[M(rf"{v}^\circ", size=28).next_to(nl.n2p(v), DOWN, buff=.2) for v in (0, 90, 180)])
        brace = Brace(Line(nl.n2p(0), nl.n2p(180)), UP, color=INK2)
        out_lbl = T("arccos returns", size=26, color=INK2).next_to(brace, UP, buff=.12)
        shade = Line(nl.n2p(0), nl.n2p(180), color=EMBER, stroke_width=14).set_opacity(.75)
        inc_lbl = TX(r"every possible inclination $i$", size=28).next_to(ticks, DOWN, buff=.25)
        inc_lbl.set_color(EMBER)
        check = M(r"\checkmark", size=64, color=GOOD).next_to(nl, RIGHT, buff=.35)
        self.beat("Arc cosine always returns an angle from zero to one hundred eighty degrees. That's exactly the range of inclination, so no extra check is needed.",
                  [Create(nl), FadeIn(ticks)], [GrowFromCenter(brace), FadeIn(out_lbl)], .05,
                  [Create(shade), FadeIn(inc_lbl)], FadeIn(check, scale=1.6),
                  w=(.2, .2, .3, .25))
        nl_grp = VGroup(nl, ticks, brace, out_lbl, shade, inc_lbl, check)

        # 3: (-C32, C31) = sin i (cos Omega, sin Omega): a point on a circle of radius sin i
        O = np.array([RX, -.9, 0])
        R = 1.7
        ang = np.radians(145)
        P = O + R * np.array([np.cos(ang), np.sin(ang), 0])
        xax = Line(O + 2.4 * LEFT, O + 2.4 * RIGHT, color=AXIS, stroke_width=2)
        yax = Line(O + 2.1 * DOWN, O + 2.1 * UP, color=AXIS, stroke_width=2)
        circ = Circle(radius=R, color=INK2, stroke_width=2.5).move_to(O)
        rad = Line(O, P, color=INK, stroke_width=3)
        rad_lbl = E(r"\sin|i", size=30).move_to((O + P) / 2 + .38 * np.array([-np.sin(ang), np.cos(ang), 0]))
        pdot = Dot(P, color=SKY, radius=.09)
        xfoot = np.array([P[0], O[1], 0])
        yfoot = np.array([O[0], P[1], 0])
        dx = DashedLine(P, xfoot, color=MUTED)
        dy = DashedLine(P, yfoot, color=MUTED)
        xl = M(r"-C_{32}", size=30).next_to(xfoot, DOWN, buff=.15)
        yl = M(r"C_{31}", size=30).next_to(yfoot, UL, buff=.08)
        arc = Arc(radius=.5, start_angle=0, angle=ang, arc_center=O, color=SKY, stroke_width=4)
        om_lbl = E(r"\Omega", size=34).move_to(O + .82 * np.array([np.cos(np.radians(62)), np.sin(np.radians(62)), 0]))
        coord = E(r"(-C_{32},\,C_{31})|=|\sin|i|\,(\cos|\Omega|,\,\sin|\Omega|)", size=40).move_to([RX, 2.4, 0])
        nonneg = TX(r"$\sin i \ge 0$", size=28).next_to(coord, DOWN, buff=.2).align_to(coord[2], LEFT)
        with self.say("Next, Omega. C three one is sine i sine Omega, and minus C three two is sine i cosine Omega. Since sine i is never negative, this pair points in the direction of Omega.") as d:
            self.play(FadeOut(nl_grp), slot(i_eq, 0), run_time=.08 * d)
            self.play(Circumscribe(r31, color=SKY), Circumscribe(r32, color=SKY), run_time=.12 * d)
            self.play(Write(coord), run_time=.12 * d)
            self.play(Create(xax), Create(yax), Create(circ), run_time=.1 * d)
            self.play(Create(rad), FadeIn(rad_lbl), FadeIn(pdot, scale=2), run_time=.1 * d)
            self.play(Create(dx), Create(dy), FadeIn(xl), FadeIn(yl), run_time=.12 * d)
            self.play(FadeIn(nonneg), Indicate(coord[2:4]), Indicate(rad_lbl), run_time=.14 * d)
            self.play(Create(arc), FadeIn(om_lbl), run_time=.12 * d)
            self.wait(.1 * d)

        # 4: Omega = atan2(C31, -C32), boxed in SKY
        om_eq = E(r"\Omega|=|\operatorname{atan2}(C_{31},\,-C_{32})", size=46).move_to([RX, 2.4, 0])
        om_box = SurroundingRectangle(om_eq, color=SKY, buff=.18, corner_radius=.08)
        om_grp = VGroup(om_eq, om_box)
        self.beat("So Omega is atan two of C three one and minus C three two.",
                  [FadeOut(coord), FadeOut(nonneg)], Write(om_eq), Create(om_box), Indicate(arc, color=SKY),
                  w=(.15, .4, .25, .2))

        # 5: arccos can't separate 145 from 215; atan2 can
        ang2 = np.radians(215)
        Q = O + R * np.array([np.cos(ang2), np.sin(ang2), 0])
        qdot = Dot(Q, color=SKY, radius=.09)
        rad2 = Line(O, Q, color=INK, stroke_width=3)
        same_x = DashedLine(P, Q, color=GOLD)
        p_lbl = M(r"145^\circ", size=28).next_to(P, LEFT, buff=.15)
        q_lbl = M(r"215^\circ", size=28).next_to(Q, LEFT, buff=.15)
        arc2 = DashedVMobject(Arc(radius=.38, start_angle=0, angle=-ang, arc_center=O, color=SKY, stroke_width=3),
                              num_dashes=14)
        row_ac = VGroup(TX(r"arccos: \ $145^\circ$ and $145^\circ$", size=30),
                        M(r"\times", size=40, color=BAD)).arrange(RIGHT, buff=.3)
        row_at = VGroup(TX(r"atan2: \ $145^\circ$ and $-145^\circ = 215^\circ$", size=30),
                        M(r"\checkmark", size=40, color=GOOD)).arrange(RIGHT, buff=.3)
        table = VGroup(row_ac, row_at).arrange(DOWN, aligned_edge=LEFT, buff=.3).move_to([RX, 2.3, 0])
        with self.say("Why atan two and not arc cosine? Arc cosine can only give zero to one eighty. It can't tell one forty five degrees from two hundred fifteen. atan two looks at the signs of both entries, so it lands in the correct quadrant.") as d:
            self.play(slot(om_grp, 1), FadeOut(VGroup(dx, dy, xl, yl, rad_lbl)), run_time=.1 * d)
            self.play(FadeIn(p_lbl), run_time=.06 * d)
            self.play(Create(rad2), FadeIn(qdot, scale=2), FadeIn(q_lbl), run_time=.12 * d)
            self.play(Create(same_x), run_time=.1 * d)
            self.play(FadeIn(row_ac[0]), run_time=.12 * d)
            self.play(FadeIn(row_ac[1], scale=1.5), run_time=.08 * d)
            self.play(Indicate(pdot, color=SKY), Indicate(qdot, color=SKY), run_time=.1 * d)
            self.play(FadeIn(row_at[0]), Create(arc2), run_time=.14 * d)
            self.play(FadeIn(row_at[1], scale=1.5), run_time=.08 * d)
            self.wait(.1 * d)
        circle_grp = VGroup(xax, yax, circ, rad, pdot, arc, om_lbl, qdot, rad2, same_x, p_lbl, q_lbl, arc2)

        # 6: omega = atan2(C13, C23), boxed in MINT
        sup = E(r"(C_{23},\,C_{13})|=|\sin|i|\,(\cos|\omega|,\,\sin|\omega|)", size=40).move_to([RX, 1.7, 0])
        w_eq = E(r"\omega|=|\operatorname{atan2}(C_{13},\,C_{23})", size=46).move_to([RX, .2, 0])
        w_box = SurroundingRectangle(w_eq, color=MINT, buff=.18, corner_radius=.08)
        w_grp = VGroup(w_eq, w_box)
        self.beat("The same reasoning for the third column gives little omega equals atan two of C one three and C two three.",
                  FadeOut(VGroup(circle_grp, table)),
                  [Circumscribe(r13, color=MINT), Circumscribe(r23, color=MINT)], Write(sup),
                  Write(w_eq), Create(w_box),
                  w=(.1, .2, .25, .3, .15))

        # 7: two practical notes
        n1 = VGroup(badge(1), VGroup(
            TX(r"atan2 returns $-180^\circ$ to $180^\circ$:", size=28),
            TX(r"add $360^\circ$ to a negative answer \ ($-90^\circ \to 270^\circ$)", size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=.15)).arrange(RIGHT, buff=.3)
        n2 = VGroup(badge(2), VGroup(
            TX(r"If $i = 0$: both pairs are $0/0$.", size=28),
            TX(r"The equatorial orbit has no node.", size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=.15)).arrange(RIGHT, buff=.3)
        notes = VGroup(panel(n1), panel(n2)).arrange(DOWN, aligned_edge=LEFT, buff=.35)
        fit(notes, 6.6, 4.5)
        notes.move_to([RX - .1, .6, 0])
        with self.say("Two practical notes. atan two returns minus one eighty to one eighty, so add three sixty to a negative answer. And if i is zero, both pairs are zero over zero: that's the equatorial orbit, with no node.") as d:
            self.play(slot(w_grp, 2), FadeOut(sup), run_time=.12 * d)
            self.play(FadeIn(notes[0], shift=.2 * UP), run_time=.15 * d)
            self.wait(.25 * d)
            self.play(FadeIn(notes[1], shift=.2 * UP), run_time=.15 * d)
            self.play(Indicate(r31[3], color=EMBER), Indicate(r32[3], color=EMBER),
                      Indicate(r13[4], color=EMBER), Indicate(r23[4], color=EMBER), run_time=.15 * d)
            self.wait(.18 * d)
        self.wipe()
