"""S20: the bulge (BRIEF.md S20)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# facts
R_EQ, R_POL = 6378.137, 6356.752
assert np.isclose(R_EQ - R_POL, 21.4, atol=0.05)           # "about twenty one kilometers"
assert round(R_EQ) == 6378 and round(R_POL) == 6357
J2 = 1.08263e-3
assert np.isclose(J2, 1.08e-3, atol=5e-6)                  # "about one point oh eight times ten to the minus three"

SQUASH = 0.80              # drawn polar/equatorial ratio (true ratio 0.99665, exaggerated for the eye)
I_DEG, OM0, OM1 = 40.0, 50.0, -25.0    # drawn orbit: tilt 40 deg, node swings west from 50 to -25 deg
A_ORB = 2.4                 # drawn circular orbit radius (not to scale)


def kvec(om_deg, i_deg=I_DEG):
    """h-hat of an orbit with node om, inclination i: (sin i sin Om, -sin i cos Om, cos i)."""
    o, i = np.radians(om_deg), np.radians(i_deg)
    return np.array([np.sin(i) * np.sin(o), -np.sin(i) * np.cos(o), np.cos(i)])


def nhat(om_deg):
    o = np.radians(om_deg)
    return np.array([np.cos(o), np.sin(o), 0.0])


assert np.allclose(cpn(np.radians(OM0), np.radians(I_DEG), 0.3)[2], kvec(OM0))   # row 3 of C_PN is h-hat


class S20_Oblate(VScene):
    budget = 116

    def construct(self):
        view = View(elev=12, azim=-55, scale=2.3, center=(-3.2, -0.2))
        earth = globe(view)
        o0 = view.p((0, 0, 0))
        # screen radius of the unit sphere: largest screen distance of an equator point from the center
        rs = max(np.linalg.norm((view.p((np.cos(t), np.sin(t), 0)) - o0)[:2]) for t in np.linspace(0, TAU, 721))

        # ---- beat 1: the five frozen elements, with a question mark
        names = [("a", "size"), ("e", "shape"), ("i", "tilt"), (r"\Omega", "node"), (r"\omega", "perigee")]
        rows = VGroup(*[VGroup(E(s, size=48), T(w, 30, INK2)).arrange(RIGHT, buff=0.45) for s, w in names])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        head = T("frozen forever", 32, INK)
        qm = M("?", size=110, color=ACCENT)
        lst = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        grp = VGroup(lst, qm).arrange(RIGHT, buff=0.6)
        place(grp, "right")
        sphere_note = T("only if Earth is a perfect sphere", 28, INK2).next_to(grp, DOWN, buff=0.5)
        self.beat("Five of the elements never change. But that's only exactly true if the Earth is a perfect sphere. It isn't.",
                  [FadeIn(earth), FadeIn(lst)], .1, FadeIn(qm, scale=1.4), FadeIn(sphere_note), .15,
                  Wiggle(earth), w=(.3, .15, .15, .25))

        # ---- beat 2: exaggerated oblate Earth, the two radii
        ref = DashedVMobject(Circle(radius=rs * SQUASH, color=MUTED, stroke_width=3).move_to(o0), num_dashes=48)
        outline = Ellipse(width=2 * rs, height=2 * rs * SQUASH).move_to(o0)
        bulge = Difference(outline, Circle(radius=rs * SQUASH).move_to(o0),
                           fill_color=GOLD, fill_opacity=0.45, stroke_width=0)
        eq_line = Line(o0, o0 + rs * RIGHT, color=INK, stroke_width=5)
        po_line = Line(o0, o0 + rs * SQUASH * UP, color=INK, stroke_width=5)
        eq_lab = backed(T("equatorial 6,378 km", 30)).next_to(eq_line, DOWN, buff=0.25).shift(0.6 * RIGHT)
        po_lab = backed(T("polar 6,357 km", 30)).next_to(po_line.get_end(), UP, buff=0.2)
        diff = VGroup(T("difference 21 km", 36),
                      T("(exaggerated here)", 30, INK2)).arrange(DOWN, buff=0.2)
        bulge_tag = T("the bulge", 34, GOLD)
        right2 = VGroup(diff, bulge_tag).arrange(DOWN, buff=0.6)
        place(right2, "right")
        with self.say("Earth spins, so it bulges at the equator. It's about twenty one kilometers wider than it is tall.") as d:
            self.play(FadeOut(VGroup(lst, qm, sphere_note)), run_time=.12 * d)
            self.play(earth.animate.stretch(SQUASH, 1), run_time=.2 * d)
            self.play(Create(ref), FadeIn(bulge), FadeIn(bulge_tag), run_time=.15 * d)
            self.play(Create(eq_line), FadeIn(eq_lab), Create(po_line), FadeIn(po_lab), run_time=.2 * d)
            self.play(FadeIn(diff), run_time=.13 * d)
            self.wait(.2 * d)

        # ---- beat 3: the J2 potential
        l1 = E(r"V|=|-\frac{\mu}{r}|\Big[\,1", size=46)
        l2 = E(r"-\,J_2|\Big(\frac{R}{r}\Big)^2|\frac{3\sin^2\phi-1}{2}\,\Big]", size=46)
        l2.next_to(l1, DOWN, buff=0.35).align_to(l1[2], LEFT).shift(0.4 * RIGHT)
        n1 = T("a perfect sphere", 28, INK2).next_to(l1[2], UP, buff=0.25)
        n2 = VGroup(T("bulge correction,", 28, INK2), M(r"\phi", size=40), T("= latitude", 28, INK2)).arrange(RIGHT, buff=0.15).next_to(l2, DOWN, buff=0.3)
        jv = E(r"J_2|=|1.08263\times 10^{-3}", size=46)
        pot = VGroup(n1, l1, l2, n2, jv)
        jv.next_to(n2, DOWN, buff=0.6)
        pot.move_to((3.3, -0.2, 0))
        fit(pot, 6.6, 6.8)
        with self.say("Your notes add one correction term to the gravity potential. Its size is set by a single number, J two, about one point oh eight times ten to the minus three.") as d:
            self.play(FadeOut(VGroup(diff, bulge_tag, eq_line, po_line, eq_lab, po_lab)), run_time=.1 * d)
            self.play(Write(l1), FadeIn(n1), run_time=.2 * d)
            self.play(Write(l2), FadeIn(n2), run_time=.2 * d)
            self.play(Circumscribe(l2[0], color=GOLD), run_time=.12 * d)
            jg = glow(jv[2], GOLD)
            self.play(Write(jv), FadeIn(jg), run_time=.2 * d)
            self.wait(.18 * d)
        self.drop(pot, jg)

        # ---- beat 4: the tilted orbit and the bulge's tug
        S1 = 1.22
        k = S1 / 2.3
        Om = ValueTracker(OM0)
        hh = lambda: kvec(Om.get_value())
        nn = lambda: nhat(Om.get_value())
        mm = lambda: np.cross(hh(), nn())                       # in-plane, 90 deg past the node (highest point)
        ring = lambda u: A_ORB * (np.cos(u) * nn() + np.sin(u) * mm())
        eqp = disc3(view, np.array([1., 0, 0]), np.array([0, 1., 0]), 3.0, INK2, opacity=0.07)
        orb = curve(view, ring, 0, TAU, INK, width=4, R=1.0)
        node = line3(view, lambda: -A_ORB * nn(), lambda: A_ORB * nn(), SKY, width=4)
        ndot = dot3(view, lambda: A_ORB * nn(), SKY, radius=0.09)
        harr = arrow3(view, lambda: 0.95 * hh(), lambda: 2.6 * hh(), LILAC)
        hlab = label3(view, r"\hat h", lambda: 2.75 * hh() + 0.45 * nn(), LILAC, 44)
        top, bot = ring(PI / 2), ring(3 * PI / 2)
        tug1 = arrow3(view, top, top - np.array([0, 0, 0.9]), EMBER, width=6)
        tug2 = arrow3(view, bot, bot + np.array([0, 0, 0.9]), EMBER, width=6)
        tipping = arc3(view, nhat(OM0), 2.6 * kvec(OM0), -np.radians(22), 2.6, EMBER)
        n4a = VGroup(T("the bulge pulls the orbit", 30), T("toward the equator", 30)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        n4b = VGroup(T("it tries to shrink the tilt", 30), M("i", size=44, color=EMBER)).arrange(RIGHT, buff=0.2)
        n4c = VGroup(T("like a hand pushing", 30, INK2), T("on a spinning top", 30, INK2)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        txt4 = VGroup(n4a, n4b, n4c).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        fit(txt4, 6.2, 6.5).move_to((0.5, -0.2, 0), aligned_edge=LEFT)
        with self.say("The extra mass at the equator tugs a tilted orbit, trying to pull its plane down toward the equator. Like a hand pushing on a spinning top.") as d:
            self.play(view.scale.animate.set_value(S1), ref.animate.scale(k, about_point=o0),
                      bulge.animate.scale(k, about_point=o0), FadeIn(eqp), run_time=.18 * d)
            self.play(grow(orb), grow(node), FadeIn(ndot), run_time=.18 * d)
            self.play(grow(harr), FadeIn(hlab), run_time=.1 * d)
            self.play(grow(tug1), grow(tug2), FadeIn(n4a), run_time=.14 * d)
            self.play(grow(tipping), FadeIn(n4b), run_time=.12 * d)
            self.wait(.1 * d)
            self.play(FadeIn(n4c), run_time=.1 * d)
            self.wait(.08 * d)

        # ---- beat 5: precession, the node line swings west
        cone = curve(view, lambda t: 2.6 * kvec(np.degrees(t)), 0, TAU, LILAC, width=2)
        e5 = E(r"\dot\Omega|<|0", size=56, cmap={r"\dot\Omega": SKY})
        n5a = T("the node line drifts west", 30, SKY)
        n5b = VGroup(M(r"\hat h", size=44, color=LILAC), T("swings around the pole", 30)).arrange(RIGHT, buff=0.2)
        n5c = VGroup(T("the tilt", 30), M("i", size=44, color=EMBER), T("stays the same", 30)).arrange(RIGHT, buff=0.2)
        txt5 = VGroup(e5, n5a, n5b, n5c).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        fit(txt5, 6.2, 6.5).move_to((0.7, -0.2, 0), aligned_edge=LEFT)
        steps = np.linspace(OM0, OM1, 6)
        ghosts = VGroup()
        with self.say("And like a top, the orbit doesn't fall flat. It precesses: the whole orbit plane slowly swings around the pole.") as d:
            self.play(FadeOut(VGroup(tug1, tug2, tipping, txt4)), FadeIn(e5), run_time=.12 * d)
            self.play(Create(cone), FadeIn(n5b), run_time=.12 * d)
            self.play(FadeIn(n5a), FadeIn(n5c), run_time=.08 * d)
            for a0, a1 in zip(steps[:-1], steps[1:]):
                g = line3(view, -A_ORB * nhat(a0), A_ORB * nhat(a0), SKY, width=3).set_opacity(0.35)
                ghosts.add(g)
                self.add(g)
                self.play(Om.animate.set_value(a1), run_time=.13 * d, rate_func=linear)
            self.wait(.03 * d)
        self.wipe()
