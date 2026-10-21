"""S02: the ECI frame (BRIEF.md S02)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# facts
EPS_DEG = 23.4                                   # obliquity of the ecliptic (narration: "about 23 and a half")
assert abs(EPS_DEG - 23.5) < 0.15
EPS = np.radians(EPS_DEG)
I_, J_, K_ = np.eye(3)
assert np.allclose(np.cross(I_, J_), K_)         # right handed: I x J = K
assert np.isclose(np.degrees(np.arccos(I_ @ J_)), 90)
# inset: Earth at the inset origin, Sun at +X; at the March equinox the Earth->Sun line is the node line
N_EQ = np.array([0, np.cos(EPS), np.sin(EPS)])   # second in-plane direction of the equator (first is X)
assert np.isclose(np.degrees(np.arccos(N_EQ @ J_)), EPS_DEG)
assert np.isclose(N_EQ @ I_, 0)                  # the intersection line is X, pointing at the Sun

def grow(m):
    """Draw a k-tracked piece (arrow3, curve, arc3) from nothing."""
    m.k.set_value(0)
    return UpdateFromAlphaFunc(m, lambda mob, a: m.k.set_value(a), suspend_mobject_updating=False)


L = 2.3                                          # axis length in Earth radii


class S02_ECI_Frame(VScene):
    budget = 158

    def construct(self):
        view = View()
        earth = globe(view)
        aI = arrow3(view, (0, 0, 0), (L, 0, 0), INK2)
        aJ = arrow3(view, (0, 0, 0), (0, L, 0), INK2)
        aK = arrow3(view, (0, 0, 0), (0, 0, L), INK2)
        lI = label3(view, r"\hat I", (L + .3, 0, 0), INK2, 36)
        lJ = label3(view, r"\hat J", (0, L + .3, 0), INK2, 36)
        lK = label3(view, r"\hat K", (0, 0, L + .3), INK2, 36)
        tag = chip("ECI", INK2).to_corner(UL, buff=.4)

        self.beat("First we need a frame to measure everything in. It's called the Earth centered inertial frame, or E C I.",
                  FadeIn(earth), [grow(aI), grow(aJ), grow(aK)], [FadeIn(lI), FadeIn(lJ), FadeIn(lK), FadeIn(tag)],
                  w=(.3, .4, .3))

        eq_disc = disc3(view, (1, 0, 0), (0, 1, 0), 2.0, INK2, .14)
        self.beat("K points through the North Pole. I and J lie in the plane of the equator.",
                  [Indicate(aK, color=ACCENT), Indicate(lK, color=ACCENT)], .1,
                  FadeIn(eq_disc), [Indicate(aI), Indicate(aJ)], w=(.35, .35, .3))

        q = M("?", size=48, color=ACCENT).next_to(lI, RIGHT, buff=.15)
        self.beat("But which way, exactly, does I point? It has to be a direction the stars agree on.",
                  FadeIn(q, scale=1.5), [Indicate(aI, color=ACCENT, scale_factor=1.3), Wiggle(q)], .3,
                  w=(.3, .7))

        # inset: Earth at origin, Sun at (2, 0, 0); the ecliptic is the circle around the Sun through Earth
        v2 = View(elev=22, azim=-72, scale=1.1, center=(2.3, -.9))
        sun_c = np.array([2.0, 0, 0])
        ecl = curve(v2, lambda t: sun_c + 2.0 * np.array([np.cos(t), np.sin(t), 0]), 0, TAU, MUTED, width=3)
        sun = Dot(v2.p(sun_c), radius=.16, color=GOLD)
        sun_lab = T("Sun", size=26, color=INK2).next_to(sun, RIGHT, buff=.15)
        mini = globe(v2, R=.32)
        ecl_disc = disc3(v2, (1, 0, 0), (0, 1, 0), 1.0, MUTED, .18)
        equ = curve(v2, lambda t: 1.0 * (np.cos(t) * I_ + np.sin(t) * N_EQ), 0, TAU, INK2, width=3)
        tilt = arc3(v2, (1, 0, 0), (0, 1, 0), EPS, .85, ACCENT)
        rays = VGroup(line3(v2, (0, 0, 0), 1.15 * J_, MUTED), line3(v2, (0, 0, 0), 1.15 * N_EQ, INK2))
        tilt_lab = label3(v2, r"23.4^\circ", (0, 1.0, .75), ACCENT, 32)
        ecl_lab = T("ecliptic", size=26, color=MUTED).move_to(v2.p(sun_c + 2.0 * np.array([0, 1, 0])) + UP * .3)
        equ_lab = T("equator", size=26, color=INK2).next_to(v2.p(-1.0 * N_EQ), DOWN, buff=.12)
        frame = RoundedRectangle(width=6.6, height=5.4, corner_radius=.15, stroke_color=HAIR, stroke_width=2) \
            .move_to((3.55, -.5, 0))
        inset = Group(frame, ecl, sun, sun_lab, ecl_lab, mini, ecl_disc, equ, equ_lab, rays, tilt, tilt_lab)
        self.beat("Picture Earth going around the Sun. Earth's equator is tilted about twenty three and a half degrees to the plane of its orbit, the ecliptic.",
                  FadeOut(q), [Create(frame), FadeIn(sun), FadeIn(sun_lab)], [grow(ecl), FadeIn(mini), FadeIn(ecl_lab)],
                  .1, [FadeIn(ecl_disc), FadeIn(equ), FadeIn(equ_lab)], [FadeIn(rays), grow(tilt), FadeIn(tilt_lab)],
                  w=(.05, .2, .25, .25, .25))

        node = line3(v2, (-1.2, 0, 0), (1.2, 0, 0), ACCENT)
        halo = glow(node, ACCENT)
        vern = arrow3(v2, (.4, 0, 0), (1.7, 0, 0), INK2)
        vern_lab = T("vernal equinox", size=26, color=INK2).next_to(v2.p((1.0, 0, 0)), DOWN, buff=.3)
        with self.say("The two planes cross along one line. On the March equinox, that line points from the Earth straight at the Sun. That is the vernal equinox direction, and I points along it.") as d:
            self.play(FadeIn(node), FadeIn(halo), run_time=.15 * d)
            self.wait(.1 * d)
            self.play(grow(vern), run_time=.2 * d)
            self.play(FadeIn(vern_lab), run_time=.1 * d)
            self.wait(.1 * d)
            ghost = vern.copy().clear_updaters()
            target = aI.copy().clear_updaters()
            self.play(Transform(ghost, target), run_time=.2 * d)
            self.remove(ghost)
            self.play(Indicate(aI, color=ACCENT, scale_factor=1.25), Indicate(lI, color=ACCENT), run_time=.15 * d)

        rh = E(r"\hat I|\times|\hat J|=|\hat K", size=52)
        rh_lab = T("right handed", size=28, color=INK2)
        rh_box = place(VGroup(rh, rh_lab).arrange(DOWN, buff=.35), "right")
        curl = arc3(view, (0, 0, 1), (1, 0, 0), PI / 2 * .9, 1.45, ACCENT)
        head = arrow3(view, 1.45 * np.array([np.cos(PI / 2 * .8), np.sin(PI / 2 * .8), 0]),
                      1.45 * np.array([0, 1, 0]), ACCENT)
        self.beat("J is ninety degrees from I in the equator, completing a right handed set with K.",
                  [FadeOut(inset), FadeOut(node), FadeOut(halo), FadeOut(vern), FadeOut(vern_lab)],
                  [grow(curl), FadeIn(head)], [Indicate(aJ, color=ACCENT), Indicate(lJ, color=ACCENT),
                                               Indicate(aK, color=ACCENT), Indicate(lK, color=ACCENT)],
                  Write(rh), FadeIn(rh_lab), w=(.15, .25, .25, .25, .1))

        # Earth spins under fixed axes: meridians and a station ride the surface, the arrows do not move
        spin = ValueTracker(0)

        def merid(lon):
            return lambda t: 1.01 * np.array([np.sin(t) * np.cos(lon + spin.get_value()),
                                              np.sin(t) * np.sin(lon + spin.get_value()), np.cos(t)])
        mers = VGroup(*[curve(view, merid(k * PI / 3), 0, PI, GOLD if k == 0 else MUTED, width=4 if k == 0 else 2,
                              R=1.0) for k in range(6)])
        clk_c = np.array([3.8, -2.2, 0])
        dial = Circle(radius=.55, color=INK2, stroke_width=3).move_to(clk_c)
        hand = Line(clk_c, clk_c + UP * .45, color=ACCENT, stroke_width=5)
        clk_lab = T("1 day", size=28, color=INK2).next_to(dial, RIGHT, buff=.3)
        clock = VGroup(dial, hand, clk_lab)
        fixed = T("fixed against the stars", size=28, color=INK2)
        fixed.next_to(dial, UP, buff=.5).align_to(dial, LEFT)
        with self.say("One more detail matters a lot. This frame does not spin with the Earth. The Earth turns underneath it once a day, while I, J and K stay fixed against the stars.") as d:
            self.play(FadeOut(curl), FadeOut(head), FadeOut(rh_box), run_time=.12 * d)
            self.play(FadeIn(mers), FadeIn(clock), run_time=.12 * d)
            self.play(spin.animate.set_value(TAU), Rotate(hand, -TAU, about_point=clk_c),
                      rate_func=linear, run_time=.56 * d)
            self.play(FadeIn(fixed), Indicate(VGroup(aI, aJ, aK), color=ACCENT, scale_factor=1.05),
                      run_time=.2 * d)
        self.wipe()
