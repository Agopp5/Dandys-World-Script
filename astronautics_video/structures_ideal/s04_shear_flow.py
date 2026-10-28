"""S04: shear stress and shear flow (BRIEF.md S04)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# facts: no number is stated in this scene; q = tau t and tau = q / t are inverses (torsion example: 20 N/mm^2, 2 mm)
assert np.isclose(20 * 2, 40) and np.isclose(40 / 2, 20)

L = np.array([-3.6, -0.4, 0])     # picture centre (left)
RX = 3.6                          # algebra column (right)


def arr(p, q, color=SKY, sw=7):
    p, q = np.array(p, dtype=float), np.array(q, dtype=float)
    if len(p) == 2:
        p, q = np.append(p, 0.0), np.append(q, 0.0)
    return Arrow(p, q, buff=0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.22)


class S04_Shear_Flow(VScene):
    budget = 109

    def construct(self):
        self.section("Shear stress and shear flow")

        # ---- beat 1: a thin-walled section, tau running along its walls
        W, H = 6.2, 5.4
        cx, cy = L[0], L[1]
        w, h = W / 2, H / 2
        sec = RoundedRectangle(width=W, height=H, corner_radius=0.7, stroke_color=INK2, stroke_width=7).move_to(L)
        d = 0.38
        taus = VGroup(
            arr([cx - 1.1, cy + h - d], [cx + 1.1, cy + h - d]),      # top: to the right
            arr([cx + w - d, cy + 0.8], [cx + w - d, cy - 0.8]),      # right: down
            arr([cx + 1.1, cy - h + d], [cx - 1.1, cy - h + d]),      # bottom: to the left
            arr([cx - w + d, cy - 0.8], [cx - w + d, cy + 0.8]),      # left: up
        )
        tau_lbl = M(r"\tau", size=64, color=SKY).next_to(taus[0], DOWN, buff=0.15)
        wall_lbl = T("thin wall", size=34, color=INK2).next_to(sec, UP, buff=0.18).align_to(sec, LEFT)
        self.beat("Shear forces and twisting create shear stress in the thin walls. We'll call it tau. "
                  "It acts along the wall, around the section.",
                  Create(sec), FadeIn(wall_lbl), .1,
                  LaggedStart(*[GrowArrow(a) for a in taus], lag_ratio=0.35), FadeIn(tau_lbl), .2,
                  w=(.25, .15, .45, .15))

        # ---- beat 2: magnify one piece of wall: tau uniform through the thickness t
        mag = Rectangle(width=0.9, height=0.6, stroke_color=ACCENT, stroke_width=4).move_to([cx + 1.85, cy + h, 0])
        big = Rectangle(width=6.0, height=2.6, stroke_color=INK2, stroke_width=5,
                        fill_color=SURFACE, fill_opacity=1).move_to([RX, 0.9, 0])
        links = VGroup(
            Line(mag.get_corner(UR), big.get_corner(UL), stroke_color=ACCENT, stroke_width=2.5),
            Line(mag.get_corner(DR), big.get_corner(DL), stroke_color=ACCENT, stroke_width=2.5),
        )
        x0, x1 = big.get_left()[0] + 0.7, big.get_right()[0] - 1.0
        ys = [big.get_center()[1] + k for k in (-0.9, -0.3, 0.3, 0.9)]
        stack = VGroup(*[arr([x0, y], [x1, y], sw=6) for y in ys])
        tips = DashedLine([x1, big.get_bottom()[1] + 0.1, 0], [x1, big.get_top()[1] - 0.1, 0],
                          color=MUTED, stroke_width=3)
        tm_line = DoubleArrow(big.get_corner(DL) + LEFT * 0.3, big.get_corner(UL) + LEFT * 0.3, buff=0,
                              stroke_width=3, tip_length=0.2, color=INK2)
        tmark = VGroup(tm_line, M(r"t", size=56, color=INK).next_to(tm_line, LEFT, buff=0.15))
        stack_tau = M(r"\tau", size=60, color=SKY).next_to(tips, RIGHT, buff=0.2)
        note2 = TX(r"$\tau$ is nearly the same all across $t$", size=48).set_color(INK2)
        note2.next_to(big, DOWN, buff=0.45)
        self.beat("The walls are so thin that tau is nearly constant through the thickness. "
                  "So instead of tau, we usually track tau times the thickness.",
                  Create(mag), Create(links), FadeIn(big), .08,
                  LaggedStart(*[GrowArrow(a) for a in stack], lag_ratio=0.25), Create(tips), FadeIn(stack_tau),
                  FadeIn(tmark), FadeIn(note2), .2,
                  w=(.1, .1, .1, .25, .1, .1, .12, .13))

        # ---- beat 3: q = tau t, boxed, N/mm
        wall = VGroup(big, stack, tips, stack_tau, tmark)
        self.play(FadeOut(VGroup(sec, taus, tau_lbl, wall_lbl, mag, links, note2)),
                  wall.animate.move_to(L + UP * 1.0), run_time=1.2)
        q_arrow = arr([big.get_left()[0] + 0.5, big.get_bottom()[1] - 0.55],
                      [big.get_right()[0] - 0.5, big.get_bottom()[1] - 0.55], sw=12)
        q_lbl = M(r"q", size=64, color=SKY).next_to(q_arrow, DOWN, buff=0.15)
        q_eq = E(r"q|=|\tau|\,t", size=72).move_to([RX, 1.6, 0])
        q_box = SurroundingRectangle(q_eq, color=SKY, buff=0.3, stroke_width=4)
        unit = M(r"\mathrm{N/mm}", size=56, color=INK).next_to(q_box, DOWN, buff=0.35)
        q_note = T("force per unit length along the wall", size=32, color=MUTED).next_to(unit, DOWN, buff=0.3)
        self.beat("That product is called the shear flow, q. "
                  "It's a force per unit length along the wall, in newtons per millimeter.",
                  FadeTransform(stack.copy(), q_arrow), FadeIn(q_lbl), Write(q_eq), Create(q_box), .1,
                  FadeIn(unit), FadeIn(q_note), .2,
                  w=(.2, .1, .25, .15, .15, .15))

        # ---- beat 4: a junction of three walls, flow in = flow out
        self.play(FadeOut(VGroup(wall, q_arrow, q_lbl, q_note)), run_time=1.0)
        J = np.array([-3.4, 1.1, 0])
        A, Bp, Cp = np.array([-6.7, 1.1, 0]), np.array([-0.4, 1.1, 0]), np.array([-3.4, -3.3, 0])
        pipes = VGroup(Line(A, J), Line(J, Bp), Line(J, Cp)).set_stroke(INK2, width=10)
        jdot = Dot(J, radius=0.09, color=INK2)
        q1 = arr([-6.3, 1.55], [-4.1, 1.55])
        q2 = arr([-2.7, 1.55], [-0.6, 1.55])
        q3 = arr([-2.95, 0.4], [-2.95, -2.4])
        l1 = M(r"q_1", size=60, color=SKY).next_to(q1, UP, buff=0.12)
        l2 = M(r"q_2", size=60, color=SKY).next_to(q2, UP, buff=0.12)
        l3 = M(r"q_3", size=60, color=SKY).next_to(q3, RIGHT, buff=0.2)
        j_eq = E(r"q_1|=|q_2|+|q_3", size=68, cmap={"q_3": SKY}).move_to([RX, -0.7, 0])
        j_note = T("what flows in must flow out", size=34, color=MUTED).next_to(j_eq, DOWN, buff=0.4)
        flashes = [ShowPassingFlash(Line(A, J).set_stroke(SKY, width=14), time_width=0.6),
                   ShowPassingFlash(Line(J, Bp).set_stroke(SKY, width=14), time_width=0.6),
                   ShowPassingFlash(Line(J, Cp).set_stroke(SKY, width=14), time_width=0.6)]
        self.beat("Why bother? Where walls meet, the shear flows add up like water flowing through pipes. "
                  "That makes them easy to keep track of.",
                  [Create(pipes), FadeIn(jdot)], .05, [GrowArrow(q1), FadeIn(l1)], flashes[0],
                  [GrowArrow(q2), GrowArrow(q3), FadeIn(l2), FadeIn(l3)], [flashes[1], flashes[2]],
                  Write(j_eq), FadeIn(j_note), .2,
                  w=(.14, .12, .1, .16, .12, .24, .12))

        # ---- beat 5: back to stress: tau = q / t
        self.play(FadeOut(VGroup(pipes, jdot, q1, q2, q3, l1, l2, l3, j_eq, j_note)), run_time=1.0)
        wall2 = VGroup(big, tmark)
        q_arrow2 = arr([big.get_left()[0] + 0.5, big.get_bottom()[1] - 0.55],
                       [big.get_right()[0] - 0.5, big.get_bottom()[1] - 0.55], sw=12)
        q_lbl2 = q_lbl.copy()
        t_eq = E(r"\tau|=|q|\,/\,|t", size=72).move_to([RX, -1.2, 0])
        t_box = SurroundingRectangle(t_eq, color=SKY, buff=0.3, stroke_width=4)
        self.beat("To get back to stress at the end, just divide by the thickness: tau equals q over t.",
                  [FadeIn(wall2), FadeIn(q_arrow2), FadeIn(q_lbl2)], .05,
                  [FadeTransform(q_arrow2.copy(), stack), Indicate(tmark, color=ACCENT)], [FadeIn(tips), FadeIn(stack_tau)],
                  Write(t_eq), Create(t_box), .3,
                  w=(.15, .25, .12, .3, .18))
        self.wipe()
