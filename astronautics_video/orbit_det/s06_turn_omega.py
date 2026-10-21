"""S06: turn three, omega, then theta zero (BRIEF.md S06)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

# ---------------------------------------------------------------- facts
R = np.radians
K = np.array([0.0, 0.0, 1.0])

# Molniya (Kluever Ex. 3.1): rows of C_PN from Omega 145, i 63.4, omega 270
Cm = cpn(R(145.0), R(63.4), R(270.0))
assert np.allclose(Cm[0], [0.2568, 0.3668, -0.8942], atol=2e-3)       # p-hat
assert np.allclose(Cm[1], [-0.8192, 0.5736, 0.0], atol=2e-3)          # q-hat
assert np.allclose(Cm[2], [0.5129, 0.7324, 0.4478], atol=2e-3)        # h-hat
# omega = 270: perigee is the southernmost point (p-hat z = sin w sin i = -sin i, the minimum possible)
assert np.isclose(Cm[0][2], -np.sin(R(63.4)), atol=1e-9) and Cm[0][2] < 0
# apogee direction -p-hat is the northernmost point
assert -Cm[0][2] > 0.89

# order of turns: C_PN = C3(w) C1(i) C3(Om)  (3, then 1, then 3)
assert np.allclose(cpn(R(50), R(40), R(60)), C3(R(60)) @ C1(R(40)) @ C3(R(50)))

# i = 120 demo: at the ascending node (theta = -omega) the satellite moves north but westward
def node_velocity(Om, inc, w, a=2.4, e=0.5):
    rP, vP = rv_perifocal(a * 6378.137, e, -w)
    return cpn(Om, inc, w).T @ np.asarray(vP)
for inc_deg, west in [(120.0, True), (40.0, False)]:
    vN = node_velocity(R(50), R(inc_deg), R(90.0))
    east = np.array([-np.sin(R(50)), np.cos(R(50)), 0.0])
    assert vN[2] > 0                                  # still northbound at the ascending node
    assert (vN @ east < 0) == west                    # westward only when i > 90


def kepler_theta(M, e):
    """true anomaly from mean anomaly (Newton on Kepler's equation, 30 iterations, converged for e <= 0.6)"""
    E_ = M if e < 0.8 else np.pi
    for _ in range(30):
        E_ = E_ - (E_ - e * np.sin(E_) - M) / (1 - e * np.cos(E_))
    return 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E_ / 2), np.sqrt(1 - e) * np.cos(E_ / 2))


assert np.isclose(kepler_theta(np.pi, 0.6), np.pi)
# satellite slows near apogee: half the period covers only theta in [-90, 90]... check time spent in apogee half
_th = np.array([kepler_theta(m, 0.6) for m in np.linspace(0, 2 * np.pi, 2001)])
_apo_frac = np.mean(np.cos(_th) < 0)
assert _apo_frac > 0.8                            # e = 0.6: over 80 percent of the period in the apogee half


class S06_Turn_omega(VScene):
    budget = 181

    def construct(self):
        view = View(scale=0.85)
        Om, Inc, W = ValueTracker(50.0), ValueTracker(40.0), ValueTracker(0.0)
        A, Ecc = ValueTracker(2.4), ValueTracker(0.5)

        def Cn():
            return cpn(R(Om.get_value()), R(Inc.get_value()), R(W.get_value()))

        def pos(th):
            return np.asarray(orbit(A.get_value(), Ecc.get_value(), R(Om.get_value()), R(Inc.get_value()),
                                    R(W.get_value()))(th))

        def nh():
            o = R(Om.get_value())
            return np.array([np.cos(o), np.sin(o), 0.0])

        def hh():
            return Cn()[2]

        def ph():
            return Cn()[0]

        def mh():                     # in-plane direction 90 deg ahead of the node
            return np.cross(hh(), nh())

        # ---------------- the tilted orbit from S05
        earth = globe(view)
        ax = axes3(view, 2.0)
        equator = disc3(view, np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), 3.9, MUTED, opacity=0.08)
        plane = disc3(view, nh, mh, 3.5, LILAC, opacity=0.10)
        node_line = line3(view, lambda: -4.0 * nh(), lambda: 4.0 * nh(), SKY, dashed=True)
        ell = curve(view, lambda t: pos(t), 0, TAU, INK, R=1.0)
        harr = arrow3(view, lambda: np.zeros(3), lambda: 2.2 * hh(), LILAC)
        hlab = label3(view, r"\vec h", lambda: 2.5 * hh(), LILAC)
        node_dot = dot3(view, lambda: pos(-R(W.get_value())), SKY)
        peri_line = line3(view, lambda: np.zeros(3), lambda: 2.3 * ph(), ROSE)
        peri_txt = label3(view, r"\text{periapsis}", lambda: 2.75 * ph(), ROSE, 28)
        peri_dot = dot3(view, lambda: pos(0.0), ROSE, radius=0.09)
        scene3d = Group(equator, plane, earth, ax, node_line, ell, harr, hlab, peri_line, node_dot, peri_dot, peri_txt)

        w_eq = E(r"\omega|=|60^\circ", size=48)
        place(w_eq, "right")
        w_eq.shift(UP * 1.2)
        self.beat("Turn three happens inside the tilted plane. Spin the ellipse about h by the argument of periapsis, little omega.",
                  FadeIn(scene3d), .1, Indicate(harr, color=LILAC), W.animate.set_value(60.0), FadeIn(w_eq),
                  w=(.2, .15, .45, .2))

        # ---------------- the omega arc: node -> periapsis, in the plane, in the direction of motion
        w_arc = arc3(view, hh, nh, lambda: R(W.get_value()), 2.0, MINT, width=7, k=0.0)
        self.add(w_arc)
        w_lab = label3(view, r"\omega", lambda: 2.35 * (np.cos(R(W.get_value()) / 2) * nh()
                                                       + np.sin(R(W.get_value()) / 2) * mh()), MINT, 40)
        defn = VGroup(T("from the ascending node", size=28, color=INK2),
                      T("to periapsis, in the orbit plane,", size=28, color=INK2),
                      T("along the motion", size=28, color=INK2)).arrange(DOWN, aligned_edge=LEFT, buff=.15)
        defn.next_to(w_eq, DOWN, buff=.5)
        self.beat("So little omega is the angle from the ascending node to the periapsis, measured in the orbit plane, in the direction the satellite moves.",
                  [Indicate(node_dot, color=SKY, scale_factor=2)], w_arc.k.animate.set_value(1.0), FadeIn(w_lab),
                  FadeIn(defn, shift=UP * .2), Indicate(peri_dot, color=ROSE, scale_factor=2),
                  w=(.15, .35, .1, .25, .15))

        # ---------------- theta zero
        TH0 = 40.0
        th_arc = arc3(view, hh, ph, R(TH0), 1.65, GOLD, width=7, k=0.0)
        self.add(th_arc)
        th_ray = line3(view, lambda: np.zeros(3), lambda: 2.0 * pos(R(TH0)) / np.linalg.norm(pos(R(TH0))), GOLD)
        sat = dot3(view, lambda: pos(R(TH0)), GOLD, radius=0.1)
        th_lab = label3(view, r"\theta_0", lambda: 2.4 * pos(R(TH0)) / np.linalg.norm(pos(R(TH0))), GOLD, 36)
        th_eq = E(r"\theta_0|=|40^\circ", size=48)
        th_eq.next_to(w_eq, DOWN, buff=.5).align_to(w_eq, LEFT)
        self.beat("The ellipse is now completely placed. The last number, the true anomaly at epoch theta zero, is the angle from periapsis to the satellite at the moment of the measurement.",
                  Circumscribe(ell, color=INK2), FadeOut(defn), .1, [FadeIn(sat, scale=2), FadeIn(th_ray)], th_arc.k.animate.set_value(1.0),
                  FadeIn(th_lab), FadeIn(th_eq), w=(.25, .1, .15, .25, .1, .15))

        # ---------------- the order of the turns: 3, 1, 3
        chips = VGroup(chip("1: K (3)", SKY), chip("2: node line (1)", EMBER), chip("3: h (3)", MINT))
        chips.arrange(DOWN, aligned_edge=LEFT, buff=.3)
        pattern = E(r"C_3|\;|C_1|\;|C_3", size=52)
        stack = VGroup(chips, pattern).arrange(DOWN, buff=.6)
        place(stack, "right")
        self.beat("Notice the order of the turns: about K, then about the node line, then about h. Three, then one, then three. Keep that pattern in mind; it comes back as a rotation matrix.",
                  [FadeOut(w_eq), FadeOut(th_eq)], FadeIn(chips[0], shift=LEFT * .3), FadeIn(chips[1], shift=LEFT * .3),
                  FadeIn(chips[2], shift=LEFT * .3), .1, Write(pattern), w=(.1, .15, .15, .15, .45))
        paint(pattern, {0: SKY, 2: EMBER, 4: MINT})

        # ---------------- morph to the drawn Molniya: Omega 145, i 63.4, omega 270 (a = 3.0, e = 0.6 drawn)
        mol = VGroup(E(r"\Omega|=|145^\circ", size=46), E(r"i|=|63.4^\circ", size=46),
                     E(r"\omega|=|270^\circ", size=46)).arrange(DOWN, aligned_edge=LEFT, buff=.35)
        mol_head = T("Molniya", size=34, weight=BOLD)
        mol_card = VGroup(mol_head, mol).arrange(DOWN, aligned_edge=LEFT, buff=.4)
        place(mol_card, "right")
        self.beat("Here's the Molniya orbit from the beginning, built the same way.",
                  [FadeOut(stack), FadeOut(w_arc), FadeOut(w_lab), FadeOut(th_arc), FadeOut(th_lab), FadeOut(sat), FadeOut(th_ray), FadeOut(peri_txt)],
                  [Om.animate.set_value(145.0), Inc.animate.set_value(63.4), W.animate.set_value(270.0),
                   A.animate.set_value(3.0), Ecc.animate.set_value(0.6), view.scale.animate.set_value(0.7)],
                  FadeIn(mol_card), w=(.15, .6, .25))
        self.drop(w_arc, w_lab, th_arc, th_lab, sat, th_ray, peri_txt)

        # ---------------- perigee far south, apogee half over the north
        apo = curve(view, lambda t: 1.1 * pos(t), R(90), R(270), GOLD, width=7, k=0.0)
        apo_lab = label3(view, r"\text{apogee half}", lambda: 1.18 * pos(np.pi) + 0.35 * K, GOLD, 30)
        peri_lab = label3(view, r"\text{perigee}", lambda: pos(0.0) - 0.9 * K + 0.3 * nh(), ROSE, 30)
        self.add(apo)
        M = ValueTracker(0.0)
        moving = dot3(view, lambda: pos(kepler_theta(M.get_value(), Ecc.get_value())), GOLD, radius=0.1)
        notes = VGroup(T("perigee: far south", size=28, color=ROSE),
                       T("apogee: high over the north,", size=28, color=GOLD),
                       T("slow, for hours", size=28, color=GOLD)).arrange(DOWN, aligned_edge=LEFT, buff=.15)
        notes.next_to(mol_card, DOWN, buff=.55).align_to(mol_card, LEFT)
        place(VGroup(mol_card, notes), "right")
        with self.say("Little omega of two seventy puts the perigee at the southernmost point of the orbit. So the long, slow apogee half hangs high over the northern hemisphere, where it can watch Russia for hours.") as d:
            self.play(Indicate(mol[2], color=MINT), Flash(peri_dot, color=ROSE), FadeIn(peri_lab), run_time=.15 * d)
            self.play(FadeIn(notes[0]), run_time=.1 * d)
            self.play(apo.k.animate.set_value(1.0), FadeIn(apo_lab), FadeIn(notes[1:]), run_time=.2 * d)
            self.add(moving)
            self.play(M.animate.set_value(TAU), rate_func=linear, run_time=.5 * d)   # mean anomaly is linear in time
            self.wait(.05 * d)

        # ---------------- predict: i greater than ninety
        self.drop(apo, apo_lab, peri_lab, moving, notes, mol_card)
        self.beat("Quick question before we move on.")
        self.checkpoint("2.1", "Inclination over ninety: which way at the node?")

        # ---------------- i = 120 demo: still northbound, but westward
        def vel_dir():
            w = R(W.get_value())
            _, vP = rv_perifocal(A.get_value() * 6378.137, Ecc.get_value(), -w)
            v = Cn().T @ np.asarray(vP)
            return v / np.linalg.norm(v)
        v_arr = arrow3(view, lambda: pos(-R(W.get_value())), lambda: pos(-R(W.get_value())) + 1.3 * vel_dir(),
                       ACCENT, k=0.0)
        def west_dir():
            o = R(Om.get_value())
            return np.array([np.sin(o), -np.cos(o), 0.0])
        node_p = lambda: pos(-R(W.get_value()))
        west = arrow3(view, node_p, lambda: node_p() + 1.1 * west_dir(), INK2, k=0.0)
        west_lab = label3(view, r"\text{west}", lambda: node_p() + 1.45 * west_dir() + 0.25 * K, INK2, 30)
        i_eq = E(r"i|=|120^\circ", size=48)
        tips = VGroup(T("ascending node:", size=28, color=SKY),
                      T("always the northbound crossing", size=28, color=INK2),
                      T("past ninety degrees,", size=28, color=INK2),
                      T("the motion runs west", size=28, color=INK2)).arrange(DOWN, aligned_edge=LEFT, buff=.18)
        card = VGroup(i_eq, tips).arrange(DOWN, aligned_edge=LEFT, buff=.5)
        place(card, "right")
        with self.say("Still northward. The ascending node is always the northbound crossing. What changes is that the motion over the Earth runs westward instead of east.") as d:
            self.play(Om.animate.set_value(50.0), Inc.animate.set_value(120.0), W.animate.set_value(90.0),
                      A.animate.set_value(2.4), Ecc.animate.set_value(0.5), view.scale.animate.set_value(0.85),
                      FadeIn(i_eq), FadeOut(ax[0:4]), run_time=.3 * d)
            self.add(v_arr)
            self.play(Flash(node_dot, color=SKY), v_arr.k.animate.set_value(1.0), FadeIn(tips[:2]), run_time=.3 * d)
            self.add(west)
            self.play(west.k.animate.set_value(1.0), FadeIn(west_lab), FadeIn(tips[2:]), run_time=.3 * d)
            self.wait(.1 * d)
        self.wipe()
