"""S04: turn one, Omega about K (BRIEF.md S04)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# facts: generic orbit a = 2.4, e = 0.5 (not to scale), Omega = 50 deg for episode 2
A, ECC = 2.4, 0.5
OM_END = np.radians(50)
assert np.allclose(orbit(A, ECC, 0, 0, 0)(0), [A * (1 - ECC), 0, 0])          # flat orbit: periapsis on +I
assert np.allclose(orbit(A, ECC, OM_END, 0, 0)(0),
                   A * (1 - ECC) * np.array([np.cos(OM_END), np.sin(OM_END), 0]))  # after turn one
assert np.allclose(cpn(OM_END, 0, 0), C3(OM_END))                             # turn one is just C3(Omega)
L_NODE = 4.0                                                                  # half-length of the node line


class S04_Turn_Omega(VScene):
    budget = 93

    def construct(self):
        view = View(scale=.82)
        Om = ValueTracker(0.0)

        def f(t):
            return orbit(A, ECC, Om.get_value(), 0, 0)(t)

        def node_dir():
            x = Om.get_value()
            return np.array([np.cos(x), np.sin(x), 0.0])

        earth = globe(view)
        eq_disc = disc3(view, (1, 0, 0), (0, 1, 0), 3.9, MUTED, 0.12)
        axs = axes3(view, 3.9)
        orb = curve(view, f, 0, TAU, INK, width=4, R=1.0)
        orb.k.set_value(0)
        self.add(orb)
        peri = dot3(view, lambda: f(0), ROSE)
        peri_lbl = label3(view, r"\text{periapsis}", lambda: f(0) + np.array([0, 0, -0.45]), ROSE, 28)

        head = self.section("Turn one: about K")
        self.beat("Here's a way to see all three angles. Start with the orbit lying flat in the equator, "
                  "with its periapsis pointing straight along I.",
                  [FadeIn(earth), FadeIn(eq_disc), FadeIn(axs)], .1,
                  orb.k.animate.set_value(1), .1, [FadeIn(peri, scale=1.6), FadeIn(peri_lbl)],
                  w=(.3, .5, .2))

        arc = arc3(view, (0, 0, 1), (1, 0, 0), lambda: max(Om.get_value(), 1e-3), 1.7, SKY)
        om_lbl = label3(view, r"\Omega",
                        lambda: 2.1 * np.array([np.cos(Om.get_value() / 2), np.sin(Om.get_value() / 2), 0]),
                        SKY, 40)
        rot = E(r"C_3(|\Omega|)", size=48)
        rot_note = T("a spin about K", size=28, color=INK2)
        side = VGroup(rot, rot_note).arrange(DOWN, buff=.3)
        place(side, "right")
        self.add(arc, om_lbl)
        self.beat("Turn one: spin the whole orbit about K by an angle, capital Omega.",
                  [Write(rot), FadeIn(rot_note), FadeOut(peri_lbl)],
                  Om.animate.set_value(OM_END), Indicate(rot[1], color=SKY),
                  w=(.25, .55, .2))

        node = line3(view, lambda: -L_NODE * node_dir(), lambda: L_NODE * node_dir(), SKY, dashed=True)
        node_lbl = T("line of nodes", size=28, color=SKY)
        node_lbl.next_to(side, DOWN, buff=.6).align_to(side, LEFT)
        self.beat("The direction where the periapsis now points is about to become a hinge. "
                  "It's called the line of nodes.",
                  Indicate(peri, color=ROSE, scale_factor=1.8), .1, Create(node), FadeIn(node_lbl, shift=UP * .2),
                  w=(.3, .45, .25))

        rng = E(r"0^\circ \le |\Omega| < 360^\circ", size=44)
        ccw = T("from I, counterclockwise", size=28, color=INK2)
        ccw2 = T("seen from the North Pole", size=28, color=INK2)
        tag = chip("RAAN", SKY)
        name = VGroup(T("right ascension of", size=28), T("the ascending node", size=28)).arrange(DOWN, buff=.15)
        slot = rot.copy()
        col = VGroup(slot, VGroup(ccw, ccw2).arrange(DOWN, buff=.12), rng, tag, name).arrange(DOWN, buff=.4)
        place(col, "right")
        with self.say("Capital Omega is measured in the equator, from I, counterclockwise as seen from the North Pole. "
                      "It can be anything from zero to three hundred sixty degrees. "
                      "Its name is the right ascension of the ascending node.") as d:
            self.play(FadeOut(rot_note), FadeOut(node_lbl), Transform(rot, slot),
                      view.elev.animate.set_value(78), run_time=.2 * d)
            self.play(FadeIn(col[1]), Om.animate.set_value(0), run_time=.1 * d)
            self.play(Om.animate.set_value(OM_END), run_time=.17 * d)
            self.play(Write(rng), run_time=.08 * d)
            self.play(Om.animate.set_value(TAU * .97), run_time=.12 * d)
            self.play(Om.animate.set_value(OM_END), run_time=.08 * d)
            self.play(FadeIn(tag, scale=1.2), FadeIn(name), run_time=.12 * d)
            self.play(FadeIn(glow(tag, SKY)), run_time=.05 * d)
            self.wait(.08 * d)
        self.wipe()
