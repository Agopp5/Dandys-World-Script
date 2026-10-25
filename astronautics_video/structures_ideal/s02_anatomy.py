"""S02: the parts of a wing box, and what each one does (BRIEF.md S02)."""
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})

# ---- geometry (scene units). A stylized airfoil, thickened so the box reads at video size (not to scale).
CH, LE, Y0, TT = 12.4, -6.2, -0.45, 0.32


def _u(x):
    return np.clip((x - LE) / CH, 0.0, 1.0)


def _yt(x):   # NACA-style half thickness, closed trailing edge
    u = _u(x)
    return 5 * TT * CH * (0.2969 * np.sqrt(u) - 0.1260 * u - 0.3516 * u ** 2 + 0.2843 * u ** 3 - 0.1036 * u ** 4)


def _yc(x):   # gentle camber
    return 0.3 * np.sin(np.pi * _u(x))


def yu(x):
    return Y0 + _yc(x) + _yt(x)


def yl(x):
    return Y0 + _yc(x) - _yt(x)


def slope(f, x, h=1e-3):
    return (f(x + h) - f(x - h)) / (2 * h)


XF, XR = LE + 0.18 * CH, LE + 0.62 * CH       # front and rear spar stations
assert yu(XF) - yl(XF) > yu(XR) - yl(XR) > 2.5   # front spar taller than rear, both large on screen
assert abs(yu(LE + CH) - yl(LE + CH)) < 1e-6      # trailing edge closes
ST_X = list(np.linspace(XF, XR, 6)[1:-1])        # four stringers on each skin between the spars


def poly(pts, color=INK2, width=6):
    return VMobject().set_points_as_corners([[x, y, 0] for x, y in pts]).set_stroke(color, width)


def ibeam(x, yb, yt, fw, ft, ww, tilt=True, color=INK2):
    """Spar seen end-on: web (index 0) plus top (1) and bottom (2) flanges; flanges follow the skin slope."""
    web = Rectangle(width=ww, height=yt - yb - 2 * ft).move_to([x, (yb + yt) / 2, 0])
    top = Rectangle(width=fw, height=ft).move_to([x, yt - ft / 2, 0])
    bot = Rectangle(width=fw, height=ft).move_to([x, yb + ft / 2, 0])
    if tilt:
        top.rotate(np.arctan(slope(yu, x)))
        bot.rotate(np.arctan(slope(yl, x)))
    for r in (web, top, bot):
        r.set_fill(color, 1).set_stroke(width=0)
    return VGroup(web, top, bot)


def small_spar(x):
    return ibeam(x, yl(x) + 0.04, yu(x) - 0.04, 0.78, 0.17, 0.1)


def cross(p, r=0.17):
    """A stress pointing into the screen: a circle with an X."""
    c = Circle(radius=r).set_stroke(GOLD, 5).set_fill(BG, 1).move_to(p)
    d = r * 0.68
    x1 = Line(p + np.array([-d, -d, 0]), p + np.array([d, d, 0])).set_stroke(GOLD, 5)
    x2 = Line(p + np.array([-d, d, 0]), p + np.array([d, -d, 0])).set_stroke(GOLD, 5)
    return VGroup(c, x1, x2).set_z_index(5)


class S02_Anatomy(VScene):
    budget = 127

    def construct(self):
        # ---------------- beat 1: one spar, drawn large; the web
        big = ibeam(-2.6, -3.5, 3.1, 3.0, 0.5, 0.3, tilt=False)
        web, top_fl, bot_fl = big
        spar_lbl = T("spar", 46, INK, weight=BOLD).move_to([4.3, 2.1, 0])
        spar_note = VGroup(T("seen end-on: it runs", 30, INK2),
                           T("along the wing, into the screen", 30, INK2)).arrange(DOWN, buff=.15)
        spar_note.next_to(spar_lbl, DOWN, buff=.3)
        web_lbl = T("web", 40, INK).move_to([0.9, -1.3, 0])
        web_arr = Arrow(web_lbl.get_left() + LEFT * .1, web.get_right() + DOWN * .9 + RIGHT * .05,
                        buff=.05, color=INK, stroke_width=5)
        web_glow = glow(web, ACCENT)
        self.beat("Let's name the parts properly. A spar is like an I beam running along the wing. The tall thin sheet in the middle is called the web.",
                  [FadeIn(big, shift=UP * .2)], [FadeIn(spar_lbl), FadeIn(spar_note)], .15,
                  [FadeIn(web_glow), web.animate.set_fill(INK), FadeIn(web_lbl), GrowArrow(web_arr)], .2,
                  w=(.2, .2, .25))

        # ---------------- beat 2: the flanges, and the skin they carry
        fl_lbl = T("flanges", 40, INK).move_to([-5.6, -0.2, 0])
        fl_arrs = VGroup(Arrow(fl_lbl.get_top() + UP * .05, top_fl.get_left() + RIGHT * .25, buff=.08,
                               color=INK, stroke_width=5),
                         Arrow(fl_lbl.get_bottom() + DOWN * .05, bot_fl.get_left() + RIGHT * .25, buff=.08,
                               color=INK, stroke_width=5))
        fl_glow = VGroup(glow(top_fl, ACCENT), glow(bot_fl, ACCENT))
        skin_t = Rectangle(width=8.6, height=.1).set_fill(INK2, 1).set_stroke(width=0)
        skin_t.next_to(top_fl, UP, buff=0).set_x(-2.3)
        skin_b = skin_t.copy().next_to(bot_fl, DOWN, buff=0).set_x(-2.3)
        skin_lbl = T("skin", 36, INK2).next_to(skin_t, RIGHT, buff=.25)
        self.beat("The thick strips at the top and bottom of the web are called flanges. They're where the spar connects to the skin.",
                  [FadeOut(web_glow), web.animate.set_fill(INK2), web_lbl.animate.set_color(MUTED),
                   web_arr.animate.set_color(MUTED)],
                  [FadeIn(fl_glow), top_fl.animate.set_fill(INK), bot_fl.animate.set_fill(INK),
                   FadeIn(fl_lbl), GrowArrow(fl_arrs[0]), GrowArrow(fl_arrs[1])], .15,
                  [GrowFromCenter(skin_t), GrowFromCenter(skin_b), FadeIn(skin_lbl)], .2,
                  w=(.1, .3, .25))

        # ---------------- beat 3: two spars plus the skin between them = the wing box
        s = np.linspace(0, 1, 50)
        xs_n = LE + (XF - LE) * s ** 2
        nose = poly([(x, yu(x)) for x in xs_n[::-1]] + [(x, yl(x)) for x in xs_n[1:]])
        xs_t = np.linspace(XR, LE + CH, 60)
        tail = poly([(x, yu(x)) for x in xs_t] + [(x, yl(x)) for x in xs_t[::-1][1:]])
        xs_b = np.linspace(XF, XR, 60)
        box_top = poly([(x, yu(x)) for x in xs_b])
        box_bot = poly([(x, yl(x)) for x in xs_b])
        box_fill = Polygon(*[[x, yu(x), 0] for x in xs_b], *[[x, yl(x), 0] for x in xs_b[::-1]])
        box_fill.set_fill(MUTED, .28).set_stroke(width=0).set_z_index(-2)
        front = small_spar(XF)
        rear = small_spar(XR)
        stringers = VGroup(*[Dot([x, yu(x) - .09, 0], radius=.07, color=INK2) for x in ST_X],
                           *[Dot([x, yl(x) + .09, 0], radius=.07, color=INK2) for x in ST_X])
        fs_lbl = T("front spar", 36, INK).move_to([XF - 0.6, 2.75, 0])
        rs_lbl = T("rear spar", 36, INK).move_to([XR + 0.6, 2.75, 0])
        fs_arr = Arrow(fs_lbl.get_bottom(), front[1].get_top() + UP * .05, buff=.08, color=INK, stroke_width=5)
        rs_arr = Arrow(rs_lbl.get_bottom(), rear[1].get_top() + UP * .05, buff=.08, color=INK, stroke_width=5)
        sk_lbl = T("skin", 36, INK2).move_to([4.6, 1.75, 0])
        sk_arr = Arrow(sk_lbl.get_bottom(), [3.6, yu(3.6) + .05, 0], buff=.08, color=INK2, stroke_width=4)
        wb_lbl = T("wing box", 40, INK, weight=BOLD).move_to([(XF + XR) / 2, Y0 + .2, 0])
        self.beat("The box made by the two spars and the skin between them is called the wing box.",
                  [FadeOut(VGroup(spar_lbl, spar_note, web_lbl, web_arr, fl_lbl, fl_arrs, fl_glow,
                                  skin_t, skin_b, skin_lbl)),
                   big.animate.set_fill(INK2)],
                  [ReplacementTransform(big, front), FadeIn(fs_lbl), GrowArrow(fs_arr)],
                  [FadeIn(rear), FadeIn(rs_lbl), GrowArrow(rs_arr)],
                  [Create(nose), Create(box_top), Create(box_bot), Create(tail), FadeIn(stringers),
                   FadeIn(sk_lbl), GrowArrow(sk_arr)], .08,
                  [FadeIn(box_fill), FadeIn(wb_lbl)], .15,
                  w=(.1, .17, .15, .2, .15))
        box = VGroup(box_fill, box_top, box_bot, front, rear, stringers)
        box_orig = box.copy()
        self.beat("It does most of the structural work.",
                  [box_fill.animate.set_fill(MUTED, .45), Circumscribe(VGroup(box_fill, front, rear), color=INK,
                                                                       stroke_width=4)], .45,
                  w=(.55,))

        # ---------------- beat 4: lift, and the three things it does
        lift = VGroup(*[Arrow([x, yl(x) - 1.05, 0], [x, yl(x) - .1, 0], buff=0, color=ROSE, stroke_width=7,
                              max_tip_length_to_length_ratio=.3)
                        for x in np.linspace(-5.0, 3.6, 6)])
        lift_lbl = T("lift", 38, ROSE).next_to(lift[-1], RIGHT, buff=.35)
        wing = VGroup(nose, tail, box, wb_lbl, lift, lift_lbl)
        self.beat("Lift pushes the wing up.",
                  [FadeOut(VGroup(fs_lbl, fs_arr, rs_lbl, rs_arr, sk_lbl, sk_arr))],
                  [LaggedStart(*[GrowArrow(a) for a in lift], lag_ratio=.12), FadeIn(lift_lbl)],
                  VGroup(nose, tail, box, wb_lbl, lift, lift_lbl).animate.shift(UP * .3), .2,
                  w=(.1, .4, .3))
