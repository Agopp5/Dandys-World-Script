# Booms, Shear Flow and Multi-Cell Torsion  (~28 min)

**Hook**: a real wing section is a skin plus dozens of stringers and spar flanges; computing its I_xx and shear flow
shape by shape is hopeless.
**Insight**: lump every stringer and flange (and the skin's share of direct stress) into a few booms; let the skin
carry only shear. Then shear flow is constant between booms and jumps at each one, and a multi-cell box in torsion is
just one constant shear flow per cell, tied together by "every cell twists the same".
**Payoff**: both HW 5 problems fall out step by step: the idealized box's shear centre at 224.8 mm, and the two-cell
wing box's shear flows.

Audience: an AERSP 301 student who has NOT been coming to class. Assume they know statics and basic mechanics of
materials, but not this course's words: define every term the first time (stringer, spar, web, flange, direct stress,
shear flow, shear centre, rate of twist), and recall every formula before using it. Concepts before examples.
PACE: slow. One idea per beat. After each new equation line or result, hold the picture still for a moment before
the next step (a pause step in beat(), e.g. 0.12-0.2 of the clip, or self.wait(1.0) after a boxed result). Reveal
long equations piece by piece, in step with the narration that reads them. Never put more on screen than the
narration has talked about.

Every file starts:
```python
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student who missed the lectures; warm and clear; slow, deliberate pace, with a full pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT, r"\tau": SKY})
```
Never change the VOICE/STYLE lines: the narration is already voiced with exactly these, and any change re-bills.

Hue meanings, the whole series: booms and boom areas B EMBER; direct (bending) stress sigma GOLD; skin shear flow q
and shear stress tau SKY; the constant closing flow q_s0 MINT; applied shear load S_y and the shear centre position
xi ROSE; torque T LILAC; in multi-cell torsion cell I's flow q_I MINT, cell II's flow q_II LIME, cell III's SKY, the
shared wall's difference GOLD; delta = integral ds/t, modulus-weighted thickness t* and G ACCENT. Walls of a section
are INK2 lines whose stroke width grows with thickness (sect.Section.draw). Signs: shear flow arrows always point the
way the flow actually goes (sect.flow reverses the arrow for a negative value); label the value with its sign.

Layout: the cross-section on the left (Section(..., center=(-3.2, -0.3))), algebra on the right (place(m, "right")),
unless a beat is pure algebra. Readability (this viewer struggles with small text): derivation lines at size 44 or
more, grey "why" notes at 30 or more beside or under each line, labels on pictures 34 or more, numbers and cards 34
or more. Use the full frame height. At most about four equation lines on screen at once: fold finished steps into one
boxed result. Show every substitution: formula, then numbers plugged in, then the result. Units: mm, N, N/mm.
Use the kit (sect.py): Section, flow, cell_flow, torque, presets channel(), hw_box(), hw_twocell(), wing_outline().
Several scenes already exist from the previous, faster cut of this video: the brief names the old file to start from (in old/; read it, write the new file, never edit old/)
("Rework of: ..."). Keep what works, slow it down and enlarge it, and follow the new narration and beats exactly.

## Facts (assert the ones your scene shows)
- Wing box anatomy: thin skin (outer surface); stringers (small stiffeners along the span, attached to the skin);
  spars (front and rear, running spanwise): each spar is a web (the vertical sheet) plus flanges (the thick strips at
  top and bottom where the web meets the skin); ribs (chordwise frames that keep the shape). z runs along the span.
- Bending stress (I_xy = 0, moment M_x only): sigma_z = (M_x/I_xx) y. I_xx = sum A y^2 for small pieces far from the axis.
- Shear flow q = tau t (N/mm): shear stress times wall thickness, a force per unit length along the wall.
- Idealization: booms carry all direct stress; skin carries only shear (t_D = 0). Skin that does carry direct stress is
  added to the booms at its ends: moment about boom 2 of a panel (width b, thickness t_D, stress sigma_1 at boom 1,
  sigma_2 at boom 2, linear between): sigma_2 t_D b^2/2 + (1/2)(sigma_1 - sigma_2) t_D b (2/3) b = sigma_1 B_1 b, so
  B_1 = (t_D b/6)(2 + sigma_2/sigma_1) and B_2 = (t_D b/6)(2 + sigma_1/sigma_2).
  sigma_2/sigma_1 = 1 (both edges the same stress, e.g. a top skin in bending about x, or axial load): B = t_D b/2.
  sigma_2/sigma_1 = -1 (a web symmetric about the neutral axis in bending): B = t_D b/6.
- Boom jump: equilibrium of a boom along z: (sigma_z + d sigma_z/dz dz) B_r - sigma_z B_r + q_2 dz - q_1 dz = 0, so
  q_2 - q_1 = -(d sigma_z/dz) B_r; with I_xy = 0 and only S_y, d sigma_z/dz = (S_y/I_xx) y (because dM_x/dz = S_y), so
  q_2 - q_1 = -(S_y/I_xx) B_r y_r. With t_D = 0 the flow is constant between booms.
- Channel (slide example): four booms B = 300 mm^2: booms 1, 2 at y = +200 mm (top flange), 3, 4 at y = -200 mm; web
  400 mm, flanges 200 mm; S_y = 4.8 kN through the shear centre. I_xx = 4 x 300 x 200^2 = 48 x 10^6 mm^4;
  S_y/I_xx = 10^-4 N/mm^4. q_12 = -6, q_23 = -12, q_34 = -6 N/mm, past boom 4: 0 (free edge).
  Forces: each flange 6 x 200 = 1200 N (opposite directions), web 12 x 400 = 4800 N = S_y (check).
  Shear centre: the flange forces form a couple 1200 x 400 = 480 000 N mm; S_y e = 480 000 -> e = 100 mm from the web,
  on the side away from the flanges (outside the channel).
- Shear centre: the point a shear load must pass through for the section to bend without twisting.
- Closed section: cut one wall, compute the "basic" open flow q_b from the jumps, then q_s = q_b + q_s0 with one
  constant q_s0 around the cell. q_s0 from a moment balance (load through a known point) or, for the shear centre,
  from zero twist: closed integral of q ds/(G t) = 0.
- HW P1 (box 500 x 300 mm; skins top and bottom 10 mm; left web 10 mm; right web 8 mm; corner angles left 60x50x10,
  right 50x40x8): angle areas (60 + 50 - 10) x 10 = 1000 mm^2 and (50 + 40 - 8) x 8 = 656 mm^2.
  Skins (ratio 1): 10 x 500/6 x (2 + 1) = 2500 mm^2 to each corner. Webs in bending (ratio -1): left 10 x 300/6 x 1 = 500,
  right 8 x 300/6 x 1 = 400. Left booms B_1 = B_4 = 1000 + 2500 + 500 = 4000 mm^2; right booms B_2 = B_3 = 656 + 2500 + 400
  = 3556 mm^2. Booms numbered clockwise from top-left: 1 top-left, 2 top-right, 3 bottom-right, 4 bottom-left; y = +-150 mm.
  I_xx = 2(4000 + 3556)(150)^2 = 340.0 x 10^6 mm^4 (I_xy = 0 by symmetry).
  Cut wall 12, s runs 1 -> 2 -> 3 -> 4 -> 1: q_b12 = 0; q_b23 = -(S_y/I_xx)(3556)(150) = -1.569 x 10^-3 S_y;
  q_b34 = q_b23 - (S_y/I_xx)(3556)(-150) = 0; q_b41 = 0 - (S_y/I_xx)(4000)(-150) = +1.765 x 10^-3 S_y.
  Shear centre: zero twist, one G: closed integral of (q_b + q_s0) ds/t = 0, ds/t: top 500/10 = 50, right 300/8 = 37.5,
  bottom 50, left 300/10 = 30, total 167.5. (-1.569 x 10^-3)(37.5) + (1.765 x 10^-3)(30) + 167.5 q_s0 = 0:
  -58.83 x 10^-3 + 52.94 x 10^-3 = -5.89 x 10^-3, so q_s0 = +3.52 x 10^-5 S_y.
  Totals: q_12 = q_34 = 3.52 x 10^-5 S_y; q_23 = -1.534 x 10^-3 S_y (flows UP the right web); q_41 = +1.800 x 10^-3 S_y
  (UP the left web). Web forces 0.460 S_y and 0.540 S_y, sum 1.000 S_y.
  Moments about the left web: right web 0.460 S_y x 500 = 230.0 S_y (counterclockwise); skins' couple
  3.52 x 10^-5 S_y x 500 x 300 = 5.27 S_y (clockwise). xi = 230.04 - 5.27 = 224.8 mm from the left web (0.46007 x 500 = 230.04, unrounded).
- Torsion of one closed cell: a torque T twists the section; rate of twist d theta/dz (radians per mm of span).
  Shear modulus G (N/mm^2): how stiff the material is in shear. In pure torsion the shear flow q is the same all the way
  around a single cell. Torque from q: each bit of wall ds carries force q ds at lever arm p, and p ds is twice the area
  of the thin triangle it makes with the reference point, so T = q closed integral p ds = 2 A q (A = area enclosed by
  the wall's midline). So q = T/(2A). Rate of twist: d theta/dz = (1/(2 A G)) closed integral q ds/t.
  Example: rectangular cell 500 x 250 mm, all walls 2 mm, G = 27 000 N/mm^2, T = 10 kN m = 10 x 10^6 N mm:
  A = 125 000 mm^2, q = 10 x 10^6/(2 x 125 000) = 40 N/mm, tau = 40/2 = 20 N/mm^2; closed integral ds/t = 1500/2 = 750;
  d theta/dz = 40 x 750/(2 x 125 000 x 27 000) = 4.44 x 10^-6 rad/mm = 0.25 deg/m.
- Multi-cell torsion (pure torque, no axial restraint): no direct stress, so booms play no part. Each cell R carries
  one constant q_R; a wall shared by cells R and R+1 carries q_R - q_{R+1}. T = sum 2 A_R q_R.
  d theta/dz = (1/(2 A_R G)) (-q_{R-1} delta_{R-1,R} + q_R delta_R - q_{R+1} delta_{R+1,R}), delta = integral ds/t.
  All cells twist at the same rate. Different materials: t* = (G/G_REF) t, delta = integral ds/t*.
  Slide 3-cell check (11.3 kNm): q_I = 7.1, q_II = 8.9, q_III = 4.2 N/mm.
- HW P2: G_REF = 27 600: skins t* = 0.8768 t. delta_16 = 156.3, delta_25 = 199.8, delta_34 = 165.6,
  delta_12 = delta_56 = 806.4, delta_23 = delta_45 = 1581.2; delta_I = 1969.0; delta_II = 3527.8.
  554.4 x 10^6 q_I = 870.0 x 10^6 q_II -> q_I = 1.569 q_II (use 1.5694 in the torque substitution: 728 200).
  T = 1.244 x 10^6 q_II; q_II = 0.804 x 10^-6 T, q_I = 1.261 x 10^-6 T; per 1 kNm: 1.26, 0.80, spar 0.46 N/mm.
  Boom areas in the HW table: B_1 = B_6 = 1290, B_2 = B_5 = 1936, B_3 = B_4 = 645 mm^2 (irrelevant in pure torsion).

# Episode 1: The Parts of a Wing Box | what carries what

## S01_Hook [101] The problem
Rework of: old/s01_hook.py (class S01_Hook).
Picture: sect.wing_outline(); a real two-spar wing section with L-shaped stringers along the skin.
1. "Here's a slice through a real wing. It's called a cross section: imagine cutting the wing like a loaf of bread, and looking at the cut face."
   → wing_outline appears; a small inset of a wing being sliced, then the section face.
2. "It has a thin outer skin, two spars that run along the wing, and a row of small stiffeners called stringers along the top and the bottom."
   → labels: skin, front spar, rear spar, stringers (one at a time, as named).
3. "To find the stresses in it, you'd need the area and position of every one of these little shapes. That's a lot of bookkeeping."
   → a few stringers light up with "?" marks.
4. "So in this lesson, we'll learn a way to simplify the section, and then use it to solve both of your homework problems."
   → the stringers shrink into EMBER dots; the idealized section.

## S02_Anatomy [127] The parts, and what each one does
New scene. Picture: a single spar drawn large (web + top and bottom flanges), then the wing box between two spars.
1. "Let's name the parts properly. A spar is like an I beam running along the wing. The tall thin sheet in the middle is called the web."
   → a spar cross section: the web highlighted, labelled "web".
2. "The thick strips at the top and bottom of the web are called flanges. They're where the spar connects to the skin."
   → the two flanges highlighted, labelled "flanges".
3. "The box made by the two spars and the skin between them is called the wing box. It does most of the structural work."
   → the wing box region shaded between the spars.
4. "Lift pushes the wing up. That does three things to the wing box: it bends it, it pushes on it with a shear force, and it twists it."
   → three small icons in a row: bending, shear force S_y (ROSE arrow), torque T (LILAC).
5. "Bending makes stresses along the span, into the screen. Shear forces and twisting make stresses that run around the section, in the skin and the webs."
   → GOLD dots/crosses on the stringers (into the screen) vs SKY arrows running along the walls.

## S03_Direct_Stress [94] Direct stress from bending
New scene. Picture: the wing box section with a dashed horizontal neutral axis; stress arrows.
1. "Bending produces direct stress: stress that points along the span. We'll call it sigma z."
   → section with a dashed neutral axis; GOLD sigma_z label.
2. "Above the neutral axis the material is stretched, and below it the material is squeezed. The farther from the axis, the bigger the stress."
   → a linear stress profile beside the section: tension (+) above, compression (-) below, zero at the axis.
3. "The formula, for bending about the horizontal axis, is sigma z equals M x over I x x, times y. Here y is the height above the neutral axis."
   → sigma_z = (M_x/I_xx) y, with each symbol labelled once.
4. "I x x measures how much area sits far from the axis. For small pieces, it's just each area times its height squared, all added up."
   → I_xx = sum A y^2; small squares at different heights with their A and y.

## S04_Shear_Flow [109] Shear stress and shear flow
New scene. Picture: one thin wall, drawn thick enough to see its thickness t; a SKY shear arrow along it.
1. "Shear forces and twisting create shear stress in the thin walls. We'll call it tau. It acts along the wall, around the section."
   → a thin wall segment with SKY tau arrows along it.
2. "The walls are so thin that tau is nearly constant through the thickness. So instead of tau, we usually track tau times the thickness."
   → zoom on the wall: tau uniform across t; t marked.
3. "That product is called the shear flow, q. It's a force per unit length along the wall, in newtons per millimeter."
   → q = tau t, boxed; units N/mm.
4. "Why bother? Where walls meet, the shear flows add up like water flowing through pipes. That makes them easy to keep track of."
   → a junction of three walls with q arrows: q_1 in, q_2 + q_3 out.
5. "To get back to stress at the end, just divide by the thickness: tau equals q over t."
   → tau = q/t.

# Episode 2: Why Booms? | structural idealization

## S05_Booms [108] Booms carry the direct stress
Rework of: old/s02_booms.py (class S02_Booms).
Picture: one stringer cross-section next to its boom.
1. "Now the main idea. Each stringer is small compared with the whole section."
   → zoom on one L stringer inside the wing.
2. "So the bending stress across one stringer hardly changes. We can treat it as constant."
   → GOLD stress arrows across it, all nearly the same length.
3. "That means we can replace the stringer by a single point, with the same area, at the same place. We call that point a boom."
   → the L shrinks into an EMBER dot labelled B; area value stays the same.
4. "Here's the key assumption of this whole topic: the booms carry all of the direct stress, and the skin between them carries only shear."
   → key_box: booms carry sigma; skin carries only q; t_D = 0 (t D is the skin thickness that carries direct stress).
5. "With that, the bending part of the problem only needs the boom areas and where they are. I x x is just each boom area times its height squared, added up."
   → back to the idealized wing; I_xx = sum B_r y_r^2.

## S06_Skin_Area [179] When the skin carries direct stress too
Rework of: old/s03_skin_area.py (class S03_Skin_Area).
Picture: one skin panel between two booms, width b, thickness t_D, with a linear stress from sigma_1 to sigma_2.
1. "Sometimes the skin does carry real direct stress. Then we give its share to the booms at its two edges."
   → a panel (width b, thickness t_D) between boom 1 and boom 2.
2. "Say the stress is sigma one at boom one and sigma two at boom two, changing in a straight line between them."
   → GOLD stress arrows varying linearly from sigma_1 to sigma_2.
3. "The two booms must do exactly what the panel did: give the same total force, and the same moment."
   → beside it, the idealized version: two booms B_1 and B_2, no skin stress; "same force, same moment".
4. "To find B one, take moments about boom two. Split the stress into a rectangle and a triangle."
   → split the stress block: rectangle (height sigma_2) and triangle (height sigma_1 - sigma_2).
5. "The rectangle's force is sigma two times t D times b. It acts at the middle, b over two from boom two."
   → sigma_2 t_D b at b/2: the term sigma_2 t_D b (b/2).
6. "The triangle's force is one half times sigma one minus sigma two, times t D times b. It acts two thirds of the way across, two b over three from boom two."
   → (1/2)(sigma_1 - sigma_2) t_D b at (2/3) b.
7. "Their moments add up to the moment of the boom force, sigma one B one, times b."
   → full line: sigma_2 t_D b (b/2) + (1/2)(sigma_1 - sigma_2) t_D b (2b/3) = sigma_1 B_1 b.
8. "Divide both sides by sigma one times b, and collect terms. You get B one equals t D b over six, times two plus sigma two over sigma one."
   → divide; common denominator 6; boxed B_1 = (t_D b/6)(2 + sigma_2/sigma_1); then B_2 by swapping 1 and 2.

## S07_Ratio [145] Two cases you will use
Rework of: old/s04_ratio.py (class S04_Ratio).
Picture: the boxed formula at the top; two panels below.
1. "So the boom area depends on the ratio of the two stresses. Two cases come up again and again."
   → boxed B formula stays on top.
2. "First case: a top skin, in bending. Both of its edges are at the same height, so they have the same stress. The ratio is one."
   → horizontal panel at constant y; sigma_2/sigma_1 = 1.
3. "Two plus one is three, and three over six is one half. Each boom gets t D b over two."
   → B = (t_D b/6)(2 + 1) = t_D b/2.
4. "Second case: a web that crosses the neutral axis, with its ends equally far above and below. The stresses are equal and opposite. The ratio is minus one."
   → vertical web symmetric about the axis; +sigma at top, -sigma at bottom; sigma_2/sigma_1 = -1.
5. "Two minus one is one. Each boom gets only t D b over six."
   → B = (t_D b/6)(2 - 1) = t_D b/6.
6. "Your turn. Pause here and do checkpoint two point one in your guide."
   → self.checkpoint("2.1", "A 300 mm web, 10 mm thick, in bending: area added?")
7. "Ten times three hundred, over six, is five hundred. So five hundred square millimeters go to each boom. We'll use exactly this in the homework."
   → B = 10 x 300/6 = 500 mm^2, boxed.

# Episode 3: Shear Flow With Booms | the jump at every boom

## S08_Jump [182] What a boom does to the shear flow
Rework of: old/s05_jump.py (class S05_Jump).
Picture: a boom (rod) with skin on both sides, a short length dz.
1. "Now let's see how shear flow behaves when booms carry the direct stress. Cut out one boom, with a short length d z along the span."
   → a horizontal rod of length dz labelled B_r; skin on both sides.
2. "The skin on one side pulls along the boom with shear flow q one. The skin on the other side, with q two."
   → SKY q_1 dz and q_2 dz along the edges.
3. "Along the boom, the bending stress changes a little, from sigma z to sigma z plus d sigma z. So the boom force changes too."
   → GOLD sigma_z B_r and (sigma_z + d sigma_z/dz dz) B_r at the ends.
4. "Add up the forces along the boom. The sigma z B r terms cancel. Divide by d z, and you're left with q two minus q one equals minus d sigma z over d z, times B r."
   → balance line; strike the cancelling terms; divide by dz; q_2 - q_1 = -(d sigma_z/dz) B_r.
5. "Bending stress is M x over I x x, times y. And the moment changes along the span at the rate of the shear force: d M x by d z is S y."
   → sigma_z = (M_x/I_xx) y; dM_x/dz = S_y.
6. "So d sigma z by d z is S y over I x x, times y. And the jump at a boom is minus S y over I x x, times B r, times y r."
   → boxed q_2 - q_1 = -(S_y/I_xx) B_r y_r.

## S09_Channel [174] The channel, step by step
Rework of: old/s06_channel.py (class S06_Channel).
Picture: sect.channel(); four booms of 300 mm^2; S_y = 4.8 kN acting through the shear centre.
1. "Between booms the skin carries no direct stress, so the shear flow can't change there. It's constant, and it only jumps when it crosses a boom."
   → a staircase plot of q along s: flat steps, jumps at the booms.
2. "Here's the channel from your slides: four booms of three hundred square millimeters, two hundred millimeters above and below the axis."
   → channel with booms, B = 300 mm^2, y = +200 and -200.
3. "I x x is four times three hundred times two hundred squared. That's forty eight million. So S y over I x x is forty eight hundred over forty eight million: ten to the minus four."
   → I_xx = 4(300)(200)^2 = 48 x 10^6; S_y/I_xx = 4800/(48 x 10^6) = 10^-4.
4. "Start at the free edge, where the shear flow is zero. Crossing boom one: zero, minus ten to the minus four, times three hundred, times two hundred. That's minus six newtons per millimeter."
   → q_12 = 0 - 10^-4 (300)(200) = -6 N/mm; SKY arrow on the top flange.
5. "Your turn. Pause here and do checkpoint three point one in your guide."
   → self.checkpoint("3.1", "Carry the shear flow past booms 2, 3 and 4")
6. "Boom two adds another minus six. That's minus twelve in the web."
   → q_23 = -6 - 6 = -12.
7. "Boom three is two hundred below the axis, so its jump is plus six. Back to minus six. And boom four brings it to zero at the free edge, just as it must."
   → q_34 = -6, past 4: 0; the staircase completes.

## S10_Shear_Centre [148] What the shear centre is
New scene. Picture: sect.channel() with the final flows from S09.
1. "We said the load acts through the shear centre. What is that? It's the one point where a shear load bends the section without twisting it."
   → channel; a ROSE load arrow at the web twists the channel (small rotation); moved to the shear centre, no twist.
2. "Look at the forces in the walls. Each flange carries six times two hundred: twelve hundred newtons. The web carries twelve times four hundred: forty eight hundred newtons."
   → flange forces 6 x 200 = 1200 N (opposite directions); web 12 x 400 = 4800 N.
3. "The web's force equals the load, good. But the two flange forces point opposite ways, so together they make a couple: twelve hundred times four hundred, which is four hundred eighty thousand newton millimeters."
   → 4800 = S_y (check); couple 1200 x 400 = 480 000 N mm.
4. "For no twist, the load has to balance that couple. Forty eight hundred times e equals four hundred eighty thousand. So e is one hundred millimeters, outside the channel."
   → S_y e = 480 000; e = 100 mm; ROSE dot at the shear centre, 100 mm from the web, away from the flanges.
5. "Notice that the shear centre doesn't have to be inside the material. For a wing, we want to know where it is, because lift that misses it will twist the wing."
   → note card.

## S11_Closed [131] Closed sections: cut, then close
Rework of: old/s07_closed.py (class S07_Closed).
Picture: a single-cell box with booms.
1. "A box is a closed section. Its walls go all the way around, so there's no free edge where we know the shear flow is zero."
   → a box with booms.
2. "So we make one. Imagine cutting any wall. Now it's an open section, and the shear flow is zero at the cut."
   → a small cut mark in the top wall.
3. "March around from the cut, jumping at each boom, exactly as for the channel. The result is called the basic shear flow, q b."
   → q_b arrows wall by wall.
4. "Of course, the real box isn't cut. Closing the cut adds one extra constant shear flow, q s zero, all the way around."
   → a MINT cell_flow arrow; q_s = q_b + q_s0.
5. "To find q s zero, use moments: the shear flows must make the same moment as the load. And if the load is at the shear centre, there's a simpler condition: the box must not twist."
   → two boxed conditions: moment balance; closed integral q ds/(G t) = 0.

# Episode 4: Homework Problem 1 | idealize the box, find its shear centre

## S12_P1_Booms [224] Idealize the box
Rework of: old/s08_p1_booms.py (class S08_P1_Booms).
Picture: sect.hw_box(); 500 x 300 mm, skins 10 mm, left web 10 mm, right web 8 mm, corner angles.
1. "Here's homework problem one. A box, five hundred millimeters wide and three hundred tall. The top and bottom skins and the left web are ten millimeters thick. The right web is eight."
   → hw_box with dimensions and wall thicknesses.
2. "Each corner has an angle, a little L shaped stiffener. Sixty by fifty by ten on the left. Fifty by forty by eight on the right."
   → L angles at the corners, labelled.
3. "The problem asks us to replace all this with four corner booms, so let's add up what goes into each boom. First the angles."
   → corners highlighted.
4. "An angle's area is the two leg lengths, minus the overlap, times the thickness. Sixty plus fifty minus ten is one hundred, times ten: one thousand square millimeters on the left."
   → (60 + 50 - 10) x 10 = 1000.
5. "Fifty plus forty minus eight is eighty two, times eight: six hundred fifty six on the right."
   → (50 + 40 - 8) x 8 = 656.
6. "Next the skins. Top and bottom skins have the same stress at both ends, so the ratio is one. Each gives ten times five hundred over two: twenty five hundred to each corner."
   → 10 x 500/6 x (2 + 1) = 2500 to each corner.
7. "Last, the webs. They cross the neutral axis, so the ratio is minus one. The left web gives ten times three hundred over six: five hundred. The right web gives eight times three hundred over six: four hundred."
   → 10 x 300/6 = 500; 8 x 300/6 = 400.
8. "Adding it all up: each left boom is four thousand square millimeters, and each right boom is three thousand five hundred fifty six."
   → B_1 = B_4 = 1000 + 2500 + 500 = 4000; B_2 = B_3 = 656 + 2500 + 400 = 3556; boom dots sized by area.

## S13_P1_Basic [197] I x x and the basic shear flow
Rework of: old/s09_p1_basic.py (class S09_P1_Basic).
Picture: the idealized box: booms 1 top-left, 2 top-right, 3 bottom-right, 4 bottom-left.
1. "Number the booms: one at the top left, then clockwise: two, three, four. Every boom is one hundred fifty millimeters above or below the middle."
   → numbers; y = +150 and -150 marked.
2. "The box is symmetric top to bottom, so I x y is zero. I x x is each boom area times one fifty squared, added up: two times four thousand plus three thousand five hundred fifty six, times one fifty squared. That's three hundred forty million."
   → I_xx = 2(4000 + 3556)(150)^2 = 340.0 x 10^6 mm^4.
3. "We want the shear centre. So put a vertical load S y at an unknown distance xi from the left web."
   → ROSE S_y arrow at unknown xi.
4. "Cut the top wall. Then go around in order: one, two, three, four. Wall one two starts at zero, because of the cut."
   → cut mark in wall 12; direction s; q_b12 = 0.
5. "Crossing boom two: minus S y over I x x, times three five five six, times one fifty. That's minus one point five six nine times ten to the minus three, S y, in the right web."
   → q_b23 = -(S_y/I_xx)(3556)(150) = -1.569 x 10^-3 S_y.
6. "Boom three is one fifty below the middle, so it cancels that exactly: the bottom wall is zero."
   → q_b34 = q_b23 - (S_y/I_xx)(3556)(-150) = 0.
7. "Boom four is also below the middle, and bigger: the left web gets plus one point seven six five times ten to the minus three, S y."
   → q_b41 = 0 - (S_y/I_xx)(4000)(-150) = +1.765 x 10^-3 S_y.

## S14_P1_Close [180] Close the cut: no twist
Rework of: old/s10_p1_close.py (class S10_P1_Close).
Picture: the box with q_b on each wall; a table of ds/t.
1. "Now close the cut with a constant q s zero. Because the load is at the shear centre, the box doesn't twist. With one material, that means the integral of q d s over t, all the way around, is zero."
   → closed integral (q_b + q_s0) ds/t = 0.
2. "d s over t is each wall's length over its thickness. Top: five hundred over ten, fifty. Right: three hundred over eight, thirty seven and a half."
   → 500/10 = 50; 300/8 = 37.5.
3. "Bottom: fifty again. Left: three hundred over ten, thirty. In total, one hundred sixty seven and a half."
   → 50; 300/10 = 30; sum 167.5.
4. "Only the two webs have basic flow. So: minus one point five six nine times thirty seven and a half, plus one point seven six five times thirty, plus one sixty seven and a half times q s zero, equals zero."
   → (-1.569 x 10^-3)(37.5) + (1.765 x 10^-3)(30) + 167.5 q_s0 = 0.
5. "The first two terms add up to minus five point eight nine times ten to the minus three. So q s zero is three point five two times ten to the minus five, S y. A small correction, all the way around."
   → -5.89 x 10^-3 + 167.5 q_s0 = 0; q_s0 = 3.52 x 10^-5 S_y (MINT).
6. "Add it to every wall to get the final shear flows."
   → totals: q_12 = q_34 = 3.52 x 10^-5 S_y, q_23 = -1.534 x 10^-3 S_y, q_41 = 1.800 x 10^-3 S_y.

## S15_P1_Centre [163] Where the shear centre is
Rework of: old/s11_p1_centre.py (class S11_P1_Centre).
Picture: the box with final flows: both webs flowing up.
1. "Both webs now carry shear flow upward. Multiply by their height, three hundred millimeters, to get forces."
   → web flows; x 300.
2. "The right web carries zero point four six S y, and the left web zero point five four S y. Together, exactly S y. Good, that's our check."
   → 0.460 S_y + 0.540 S_y = 1.000 S_y (GOOD check).
3. "Now take moments about the left web. The right web's force, zero point four six S y, is five hundred millimeters away. That's two hundred thirty S y."
   → 0.460 S_y x 500 = 230.0 S_y.
4. "The small flows in the top and bottom skins point opposite ways, so they make a small couple, the other way: about five point three S y."
   → 3.52 x 10^-5 S_y x 500 x 300 = 5.27 S_y, opposite sense.
5. "So S y times xi equals two thirty point zero four, minus five point two seven. xi is two hundred twenty four point eight millimeters from the left web. That's the answer."
   → xi = 224.8 mm, ROSE, glowing; dashed line marks the shear centre.
6. "It sits left of the middle, because the left booms are heavier and carry more of the load."
   → dashed "middle" at 250 mm; the left booms flash.
7. "Your turn. Pause here and do checkpoint four point one: the same steps for the practice box."
   → self.checkpoint("4.1", "Practice box: booms, then the shear centre")

# Episode 5: Torsion of Closed Sections | from one cell to many

## S16_Torsion_Basics [134] One closed cell under a torque
New scene. Picture: a single rectangular cell (500 x 250 mm, 2 mm walls) under a LILAC torque.
1. "Now a different load: a pure twist. A torque T is applied to the wing box, and nothing else."
   → a single rectangular cell; LILAC torque arrow.
2. "In a single closed cell under pure torque, the shear flow is the same all the way around. Call it q."
   → SKY arrows of equal length on all four walls, all one way around.
3. "Each little piece of wall carries a force q d s. Its moment about the middle is that force times its lever arm."
   → a short piece ds, force q ds, lever arm p drawn to the centre.
4. "Lever arm times d s is twice the area of the thin triangle it sweeps. Going all the way around, the triangles fill the whole cell. So the torque is two times the enclosed area, times q."
   → triangles sweeping the cell; T = 2 A q, boxed.
5. "For a five hundred by two fifty cell, A is one hundred twenty five thousand square millimeters. Under ten kilonewton meters, q is ten million over two hundred fifty thousand: forty newtons per millimeter."
   → A = 125 000 mm^2; q = 10 x 10^6/(2 x 125 000) = 40 N/mm; tau = 40/2 = 20 N/mm^2.

## S17_Twist_Rate [152] How much it twists
New scene. Picture: the same cell; then a short length of the box twisting.
1. "The torque also twists the box a little. The twist per unit length along the span is called the rate of twist, d theta by d z."
   → two sections a distance dz apart, one rotated slightly by d theta.
2. "How much it twists depends on the material's shear stiffness, the shear modulus G, and on how thin the walls are."
   → G (ACCENT) and t labels.
3. "The formula is: d theta by d z equals one over two A G, times the integral of q d s over t, all the way around."
   → d theta/dz = (1/(2 A G)) closed integral q ds/t.
4. "We'll call the integral of d s over t, for a wall, delta. For our cell, every wall is two millimeters thick, so delta around the cell is fifteen hundred over two: seven fifty."
   → delta = integral ds/t; closed integral ds/t = 1500/2 = 750.
5. "So the rate of twist is forty times seven fifty, over two times one twenty five thousand times twenty seven thousand. That's four point four four times ten to the minus six radians per millimeter: about a quarter of a degree per meter."
   → 40 x 750/(2 x 125 000 x 27 000) = 4.44 x 10^-6 rad/mm = 0.25 deg/m.

## S18_Cells [87] Several cells: one shear flow per cell
Rework of: old/s12_cells.py (class S12_Cells).
Picture: a generic three-cell wing box under a torque T.
1. "Real wings often have several cells side by side. With pure torque, there's no bending stress, so the booms don't matter at all."
   → three-cell box, LILAC torque; booms fade.
2. "Each cell still carries its own constant shear flow: q one, q two, q three."
   → cell_flow arrows q_I (MINT), q_II (LIME), q_III (SKY).
3. "A wall shared by two cells has both flows on it, in opposite directions. So it carries the difference."
   → shared walls labelled q_I - q_II, q_II - q_III in GOLD.
4. "The torque is the sum of two A q for every cell."
   → T = sum 2 A_R q_R, then written out per cell.
5. "But that's only one equation, and there's one unknown shear flow for every cell. We need more equations."
   → "N unknowns, 1 equation".

## S19_Twist [125] Every cell twists the same
Rework of: old/s13_twist.py (class S13_Twist).
Picture: two cells side by side, the shared wall highlighted.
1. "The extra equations come from one simple fact. The whole wing box rotates as one piece, so every cell must twist at the same rate."
   → both cells rotate together; d theta/dz the same.
2. "For each cell, the rate of twist is the same formula as before: one over two A G, times the integral of q d s over t around that cell."
   → d theta/dz = (1/(2 A_R G)) closed integral q ds/t.
3. "Your turn. Pause here and do checkpoint five point one in your guide."
   → self.checkpoint("5.1", "Write the twist rate for cell I of a two-cell box")
4. "Going around cell one, every wall carries q one, except the shared wall, which carries q one minus q two. Collect the terms. You get q one times delta one, minus q two times delta one two."
   → (1/(2 A_I G)) (q_I delta_I - q_II delta_12), built wall by wall.
5. "Set cell one's rate equal to cell two's. Together with the torque equation, that's two equations for the two unknowns."
   → the two boxed equations.

## S20_Gstar [99] Walls made of different materials
Rework of: old/s14_gstar.py (class S14_Gstar).
Picture: the twist-rate formula; a wing box with skins and spars labelled.
1. "Sometimes the skins and the spars are made of different materials. Then G is different on each wall, and it has to move inside the integral."
   → d theta/dz = (1/(2A)) closed integral q ds/(G t).
2. "Here's the trick. Pick one reference G. Then scale each wall's thickness by its own G over the reference G. That's called the modulus weighted thickness, t star."
   → t* = (G/G_REF) t.
3. "Now use t star wherever you had t. Delta becomes the integral of d s over t star. Everything else stays the same."
   → delta = integral ds/t*; G_REF d theta/dz = (1/(2A)) closed integral q ds/t*.
4. "Your slides' three cell example, worked this way, gives seven point one, eight point nine, and four point two newtons per millimeter."
   → q_I = 7.1, q_II = 8.9, q_III = 4.2 N/mm.

# Episode 6: Homework Problem 2 | the two-cell wing box

## S21_P2_Setup [146] Set up the two-cell box
Rework of: old/s15_p2_setup.py (class S15_P2_Setup).
Picture: sect.hw_twocell(); the HW table.
1. "Here's homework problem two: a two cell wing box under a counterclockwise torque. The problem doesn't give the size of the torque, so we'll find each shear flow per unit of torque."
   → hw_twocell with cells I and II, LILAC counterclockwise torque; "T not given: solve per unit T".
2. "The table also lists boom areas. In pure torsion there's no direct stress, so the booms carry nothing. We can ignore them."
   → boom areas struck through.
3. "The walls have two different G values. Take the reference G as twenty seven thousand six hundred. The webs already have that G, so they keep their thickness."
   → G_REF = 27 600; webs: t* = t.
4. "The skins have G of twenty four thousand two hundred. So their thickness is scaled by twenty four two hundred over twenty seven six hundred: zero point eight seven seven."
   → t* = (24 200/27 600) t = 0.8768 t for walls 12, 56, 23, 45.
5. "Now each wall's delta is its length over t star."
   → table: wall | L | t* | delta: 156.3, 199.8, 165.6, 806.4, 1581.2.
6. "Around cell one: one nineteen sixty nine. Around cell two: thirty five twenty eight. And the shared spar alone: one ninety nine point eight."
   → delta_I = 1969.0; delta_II = 3527.8; delta_25 = 199.8.

## S22_P2_Solve [222] Solve for the shear flows
Rework of: old/s16_p2_solve.py (class S16_P2_Solve).
Picture: the two boxed equations; data card.
1. "First equation, equal twist. Cell one's rate: q one times nineteen sixty nine, minus q two times one ninety nine point eight, over two times two hundred thirty two thousand."
   → left side.
2. "That must equal cell two's rate: minus q one times one ninety nine point eight, plus q two times thirty five twenty eight, over two times two hundred fifty eight thousand."
   → full equal-twist equation.
3. "Cross multiply and collect. Five hundred fifty four million q one equals eight hundred seventy million q two. So q one is one point five seven times q two."
   → 554.4 x 10^6 q_I = 870.0 x 10^6 q_II; q_I = 1.569 q_II.
4. "Second equation, the torque. T equals two times two hundred thirty two thousand times q one, plus two times two hundred fifty eight thousand times q two."
   → T = 2(232 000) q_I + 2(258 000) q_II.
5. "Substitute q one. That gives T equals one point two four four million times q two."
   → (728 200 + 516 000) q_II = 1.244 x 10^6 q_II.
6. "So q two is zero point eight zero four times ten to the minus six, T. And q one is one point two six one times ten to the minus six, T, with T in newton millimeters."
   → q_II = 0.804 x 10^-6 T; q_I = 1.261 x 10^-6 T, boxed.
7. "For a torque of one kilonewton meter: one point two six in cell one, zero point eight zero in cell two, and the spar carries the difference, zero point four six newtons per millimeter."
   → per 1 kNm: q_I = 1.26, q_II = 0.80, spar 0.46 N/mm; counterclockwise arrows.
8. "Your turn. Pause here and do checkpoint six point one: a two cell box with a real torque."
   → self.checkpoint("6.1", "Practice two-cell box: T = 15 kN m")

## S23_Recap [96] Recap
Rework of: old/s17_recap.py (class S17_Recap).
Picture: key_box lines, one per beat.
1. "Let's recap. Booms carry the direct stress, and the skin carries shear. Any direct stress the skin does carry is added to the booms with t D b over six, times two plus the stress ratio."
   → card 1.
2. "Shear flow is constant between booms, and jumps at each one. For a closed section: cut, march around, then close with q s zero."
   → card 2.
3. "In torsion, a single cell has T equals two A q. With several cells, each has its own q: the torque gives one equation, equal twist gives the rest, and different materials just scale the thickness."
   → card 3.
