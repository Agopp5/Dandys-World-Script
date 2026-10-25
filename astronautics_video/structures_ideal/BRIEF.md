# Booms, Shear Flow and Multi-Cell Torsion  (~20 min)

**Hook**: a real wing section is a skin plus dozens of stringers and spar flanges; computing its I_xx and shear flow
shape by shape is hopeless.
**Insight**: lump every stringer and flange (and the skin's share of direct stress) into a few booms; let the skin
carry only shear. Then shear flow is constant between booms and jumps at each one, and a multi-cell box in torsion is
just one constant shear flow per cell, tied together by "every cell twists the same".
**Payoff**: both HW 5 problems fall out step by step: the idealized box's shear centre at 224.8 mm, and the two-cell
wing box's shear flows.

Audience: an AERSP 301 student who struggles with small text and skipped steps. Go slowly, one idea per beat, every
algebra step on screen. Concepts before examples. Pace is deliberately unhurried; let pictures sit.

Every file starts:
```python
from sect import *          # re-exports everything from mtk, plus the cross-section kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{"B": EMBER, "B_r": EMBER, "B_1": EMBER, "B_2": EMBER, r"\sigma_1": GOLD, r"\sigma_2": GOLD, r"\sigma_z": GOLD,
          "q": SKY, "q_1": SKY, "q_2": SKY, "q_b": SKY, r"q_{s,0}": MINT, "S_y": ROSE, r"\xi": ROSE, "T": LILAC,
          "q_I": MINT, "q_{II}": LIME, r"\delta": ACCENT, "t^*": ACCENT, "G": ACCENT})
```
Never change the VOICE/STYLE lines: the narration is already voiced with exactly these, and any change re-bills.

Hue meanings, the whole series: booms and boom areas B EMBER; direct (bending) stress sigma GOLD; skin shear flow q
SKY; the constant closing flow q_s0 MINT; applied shear load S_y and the shear centre position xi ROSE; torque T
LILAC; in multi-cell torsion cell I's flow q_I MINT, cell II's flow q_II LIME, the shared wall's difference GOLD;
delta = integral ds/t and modulus-weighted thickness t* and G ACCENT. Walls of a section are INK2 lines whose
stroke width grows with thickness (sect.Section.draw). Signs: shear flow arrows always point the way the flow actually
goes (sect.flow reverses the arrow for a negative value); label the value with its sign as computed.

Layout: the cross-section on the left (Section(..., center=(-3.2, -0.3))), algebra on the right (place(m, "right")),
unless a beat is pure algebra. Readability (this viewer struggles with small text): derivation lines at size 40 or
more, grey "why" notes at 26 or more beside or under each line, numbers and cards at 30 or more. Use the full frame
height; never pack algebra into the top third. At most about four equation lines on screen at once: fold finished steps
into one boxed result. Show every substitution: formula, then numbers plugged in, then the result. Units: mm, N, N/mm.
Use the kit (sect.py): Section, flow, cell_flow, torque, presets channel(), hw_box(), hw_twocell(), wing_outline().

## Facts (assert the ones your scene shows)
- Idealization: booms carry all direct stress; skin carries only shear (t_D = 0). Skin that does carry direct stress is
  added to the booms at its ends: moment about boom 2 of a panel (width b, thickness t_D, stress sigma_1 at boom 1,
  sigma_2 at boom 2, linear between): sigma_2 t_D b^2/2 + (1/2)(sigma_1 - sigma_2) t_D b (2/3) b = sigma_1 B_1 b, so
  B_1 = (t_D b/6)(2 + sigma_2/sigma_1) and B_2 = (t_D b/6)(2 + sigma_1/sigma_2).
  sigma_2/sigma_1 = 1 (both edges the same stress, e.g. a top skin in bending about x, or axial load): B = t_D b/2.
  sigma_2/sigma_1 = -1 (a web symmetric about the neutral axis in bending): B = t_D b/6.
- Boom jump: equilibrium of a boom along z: (sigma_z + d sigma_z/dz dz) B_r - sigma_z B_r + q_2 dz - q_1 dz = 0, so
  q_2 - q_1 = -(d sigma_z/dz) B_r; with I_xy = 0 and only S_y, d sigma_z/dz = (S_y/I_xx) y, so
  q_2 - q_1 = -(S_y/I_xx) B_r y_r. With t_D = 0 the flow is constant between booms.
- Channel (slide example): four booms B = 300 mm^2 at (+-200 mm), web 400 mm, flanges 200 mm; S_y = 4.8 kN through the
  shear centre. I_xx = 4 x 300 x 200^2 = 48 x 10^6 mm^4; S_y/I_xx = 10^-4 N/mm^4.
  q_12 = 0 - 10^-4 x 300 x 200 = -6 N/mm; q_23 = -6 - 10^-4 x 300 x 200 = -12 N/mm; q_34 = -12 - 10^-4 x 300 x (-200) = -6;
  past boom 4: -6 - 10^-4 x 300 x (-200) = 0 (free edge, as it must). Negative = flow opposite to the direction s.
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
  (UP the left web). Check: web forces 1.534 x 10^-3 x 300 = 0.460 S_y and 1.800 x 10^-3 x 300 = 0.540 S_y, sum 1.000 S_y.
  Moments about the left web: right web 0.460 S_y x 500 = 230.0 S_y (counterclockwise); top and bottom skins form a
  couple 3.52 x 10^-5 S_y x 500 x 300 = 5.27 S_y (clockwise). S_y xi = 230.0 S_y - 5.3 S_y, so xi = 224.8 mm from the left
  web (left of the middle, 250 mm, because the left booms are heavier).
- Multi-cell torsion (pure torque, no axial restraint): no direct stress, so booms play no part. Each cell R carries
  one constant q_R; a wall shared by cells R and R+1 carries q_R - q_{R+1}. T = sum 2 A_R q_R.
  Rate of twist of cell R: d theta/dz = (1/(2 A_R G)) closed integral q ds/t
  = (1/(2 A_R G)) (-q_{R-1} delta_{R-1,R} + q_R delta_R - q_{R+1} delta_{R+1,R}), delta = integral ds/t, delta_R over all of
  cell R's walls. All cells twist at the same rate: N - 1 equations; plus the torque equation: N unknowns.
  Different materials: t* = (G/G_REF) t, delta = integral ds/t*, and G_REF d theta/dz is the common value.
  Slide 3-cell check (11.3 kNm): q_I = 7.1, q_II = 8.9, q_III = 4.2 N/mm.
- HW P2 (two cells; booms 1, 6 left; 2 (bottom), 5 (top) on the spar; 3, 4 right). Torque magnitude is NOT given in the
  HW: solve per unit torque T (N mm). Booms are irrelevant (pure torsion).
  G_REF = 27 600: skins (G = 24 200) get t* = (24 200/27 600) t = 0.8768 t; webs (27 600) keep t.
  delta_16 = 254/1.625 = 156.3; delta_25 = 406/2.032 = 199.8; delta_34 = 202/1.220 = 165.6;
  delta_12 = delta_56 = 647/0.8023 = 806.4; delta_23 = delta_45 = 775/0.4901 = 1581.2.
  delta_I = 156.3 + 2(806.4) + 199.8 = 1969.0; delta_II = 165.6 + 2(1581.2) + 199.8 = 3527.8.
  Equal twist: (1969.0 q_I - 199.8 q_II)/(2 x 232 000) = (-199.8 q_I + 3527.8 q_II)/(2 x 258 000)
  -> 258 000(1969.0 q_I - 199.8 q_II) = 232 000(-199.8 q_I + 3527.8 q_II) -> 554.4 x 10^6 q_I = 870.0 x 10^6 q_II
  -> q_I = 1.569 q_II. Torque: T = 2(232 000) q_I + 2(258 000) q_II = (728 200 + 516 000) q_II = 1.244 x 10^6 q_II.
  q_II = 0.804 x 10^-6 T, q_I = 1.261 x 10^-6 T, spar 25 carries q_I - q_II = 0.458 x 10^-6 T.
  Per 1 kNm (T = 10^6 N mm): q_I = 1.26, q_II = 0.80, spar 0.46 N/mm. Counterclockwise T: both cells' flows counterclockwise.

# Episode 1: Why Booms? | structural idealization

## S01_Hook [62] The problem
Picture: sect.wing_outline(); a real two-spar wing section with L-shaped stringers along the skin.
1. "Here's a real wing section: a thin skin, two spars, and a row of stringers along the top and bottom."
   → wing_outline with small L-shaped stringer symbols at each stringer point; the two spars.
2. "To find its bending stresses and shear flow, you'd need the area and position of every one of these shapes, and the skin between them."
   → highlight a few stringers and a skin segment in turn; small "?" marks.
3. "That's a lot of bookkeeping. So we simplify the section in a way that keeps what matters."
   → the stringer shapes shrink into EMBER dots: the idealized section (same outline, dots, thin skin).

## S02_Booms [75] Booms carry the direct stress
Picture: one stringer cross-section next to its boom.
1. "Each stringer is small compared with the whole section, so the bending stress across it is nearly constant."
   → zoom on one L stringer; a GOLD stress arrow field across it, all nearly the same length.
2. "So we can replace it by a single point with the same area. We call it a boom."
   → the L morphs into an EMBER dot labelled B; the area value stays the same.
3. "Here's the key assumption: the booms carry all of the direct stress, and the skin between them carries only shear."
   → key_box: booms carry sigma; skin carries only q; t_D = 0.
4. "That's a big simplification. The bending part of the problem now only needs the boom areas and their positions."
   → back to the idealized wing; I_xx = sum B_r y_r^2 written under it.

## S03_Skin_Area [97] When the skin carries direct stress too
Picture: one skin panel between two booms, width b, thickness t_D, with a linear stress from sigma_1 to sigma_2.
1. "Sometimes the skin does carry real direct stress. Then we add its share to the booms at its two edges."
   → a panel (width b, thickness t_D) between boom 1 and boom 2; GOLD stress arrows varying linearly from sigma_1 to sigma_2.
2. "The rule: the two booms must give the same force and the same moment as the panel."
   → beside it, the idealized version: two booms B_1 and B_2, no skin stress.
3. "Take moments about boom two. The uniform part of the stress, sigma two, acts at the middle. The triangle on top acts two thirds of the way across."
   → split the stress block into a rectangle (sigma_2 t_D b at b/2) and a triangle ((1/2)(sigma_1 - sigma_2) t_D b at (2/3) b).
4. "Setting their moment equal to sigma one times B one times b, and dividing through, gives B one equals t D b over six, times two plus sigma two over sigma one."
   → the equation line by line: moment balance, divide by sigma_1 b, boxed B_1 = (t_D b/6)(2 + sigma_2/sigma_1); then B_2 by swapping 1 and 2.

## S04_Ratio [99] Two cases you will use
Picture: the boxed formula at the top; two small panels below.
1. "The stress ratio depends on where the panel is."
   → boxed B formula stays on top.
2. "A top skin in bending has the same stress at both edges, so the ratio is one, and each boom gets t D b over two."
   → a horizontal panel at constant y; sigma_2/sigma_1 = 1 -> B = t_D b/2.
3. "A web that crosses the neutral axis has equal and opposite stresses at its ends, so the ratio is minus one, and each boom gets only t D b over six."
   → a vertical web symmetric about the neutral axis; sigma_2/sigma_1 = -1 -> B = t_D b/6.
4. "Your turn. Pause here and do checkpoint one point one in your guide."
   → self.checkpoint("1.1", "A 300 mm web, 10 mm thick, in bending: area added?")
5. "Ten times three hundred over six: five hundred square millimeters to each boom. We'll use exactly that in the homework."
   → B = 10 x 300/6 = 500 mm^2, boxed.

# Episode 2: Shear Flow With Booms | the jump at every boom

## S05_Jump [104] What a boom does to the shear flow
Picture: a boom (rod) with skin on both sides, a short length dz; the slide's free body.
1. "Cut out one boom, with a short length d z, and the skin on either side."
   → a horizontal rod of length dz labelled B_r; skin flaps left and right.
2. "Along the boom, the bending stress changes from sigma to sigma plus d sigma. The skin pushes on it with shear flows q one and q two."
   → GOLD arrows sigma_z B_r and (sigma_z + d sigma_z/dz dz) B_r at the ends; SKY q_1 dz and q_2 dz along the edges.
3. "Force balance along the boom gives q two minus q one equals minus d sigma by d z, times B r."
   → the equation, then cancel to q_2 - q_1 = -(d sigma_z/dz) B_r.
4. "With only a vertical load and I x y zero, d sigma by d z is S y over I x x, times y. So the jump is minus S y over I x x, times B r y r."
   → substitute; boxed q_2 - q_1 = -(S_y/I_xx) B_r y_r.

## S06_Channel [137] The channel, step by step
Picture: sect.channel(); four booms of 300 mm^2; S_y = 4.8 kN acting through the shear centre.
1. "Between booms the skin carries no direct stress, so the shear flow is constant. It only changes when it crosses a boom."
   → a staircase plot of q along s: flat steps, jumps at the booms.
2. "For this channel, I x x is four times three hundred times two hundred squared: forty eight million. So S y over I x x is ten to the minus four."
   → I_xx line with substitution; S_y/I_xx = 4.8 x 10^3/48 x 10^6 = 10^-4.
3. "Start at the free edge, where q is zero. Crossing boom one: zero minus ten to the minus four, times three hundred, times two hundred. Minus six newtons per millimeter."
   → q_12 = 0 - 10^-4 (300)(200) = -6 N/mm; SKY arrow on the top flange.
4. "Your turn. Pause here and do checkpoint two point one in your guide."
   → self.checkpoint("2.1", "Carry the shear flow past booms 2, 3 and 4")
5. "Boom two adds another minus six: minus twelve in the web. Boom three sits at minus two hundred, so it adds plus six: back to minus six. And boom four brings it to zero at the free edge, as it must."
   → q_23 = -12, q_34 = -6, past 4: 0; arrows drawn; the staircase completes.

## S07_Closed [96] Closed sections: cut, then close
Picture: a single-cell box with booms.
1. "In a closed section there is no free edge to start from. So we make one: cut any wall."
   → a box; a small cut mark in the top wall.
2. "With the cut, it's an open section. March around from the cut, jumping at each boom. That's the basic shear flow, q b."
   → q_b arrows wall by wall.
3. "Closing the cut adds one constant shear flow, q s zero, all the way around the cell."
   → a MINT cell_flow arrow; q_s = q_b + q_s0.
4. "To find q s zero, use moments. If the load passes through the shear center, there's another condition: the section must not twist. The integral of q d s over G t around the cell is zero."
   → two boxed conditions: moment balance; closed integral q ds/(G t) = 0 for the shear centre.

# Episode 3: Homework Problem 1 | idealize the box, find its shear centre

## S08_P1_Booms [96] Idealize the box
Picture: sect.hw_box(); the HW figure: 500 x 300 mm, skins 10 mm, left web 10 mm, right web 8 mm, corner angles.
1. "Here's the box. Each corner has an angle: sixty by fifty by ten on the left, fifty by forty by eight on the right."
   → hw_box drawn with small L angles at the corners and dimensions.
2. "An angle's area is the sum of its legs minus the overlap, times thickness. Left: one thousand square millimeters. Right: six hundred fifty six."
   → (60 + 50 - 10) x 10 = 1000; (50 + 40 - 8) x 8 = 656.
3. "The top and bottom skins have the same stress at both ends, ratio one. Each gives ten times five hundred over two: twenty five hundred to each corner."
   → 10 x 500/6 x (2 + 1) = 2500.
4. "The webs cross the neutral axis, ratio minus one: five hundred from the left web, four hundred from the right."
   → 10 x 300/6 = 500; 8 x 300/6 = 400. Booms: left 1000 + 2500 + 500 = 4000; right 656 + 2500 + 400 = 3556; EMBER dots sized by area.

## S09_P1_Basic [131] I x x and the basic shear flow
Picture: the idealized box: four booms, numbered 1 top-left, 2 top-right, 3 bottom-right, 4 bottom-left.
1. "The box is symmetric about its horizontal axis, so I x y is zero. I x x is two times four thousand plus three thousand five hundred fifty six, times one fifty squared."
   → I_xx = 2(4000 + 3556)(150)^2 = 340.0 x 10^6 mm^4.
2. "Put a vertical load S y somewhere, at a distance xi from the left web. Cut the top wall, and go around: one, two, three, four."
   → ROSE S_y arrow at unknown xi; cut mark in wall 12; direction s marked.
3. "Wall one two: zero. Crossing boom two: minus S y over I x x, times three five five six, times one fifty. That's minus one point five six nine times ten to the minus three, S y."
   → q_b12 = 0; q_b23 = -(S_y/I_xx)(3556)(150) = -1.569 x 10^-3 S_y.
4. "Boom three is at minus one fifty, so it cancels that: wall three four is zero. Boom four brings the left web to plus one point seven six five times ten to the minus three."
   → q_b34 = 0; q_b41 = +1.765 x 10^-3 S_y; SKY arrows.

## S10_P1_Close [124] Close the cut: no twist
Picture: the box with q_b on each wall; a table of ds/t.
1. "At the shear center the box doesn't twist. With one material, that means the integral of q d s over t around the box is zero."
   → closed integral (q_b + q_s0) ds/t = 0.
2. "d s over t for each wall: fifty on top, thirty seven and a half on the right, fifty on the bottom, thirty on the left. One hundred sixty seven and a half in total."
   → 500/10 = 50, 300/8 = 37.5, 500/10 = 50, 300/10 = 30; sum 167.5.
3. "Only the two webs have basic flow. Minus one point five six nine times thirty seven and a half, plus one point seven six five times thirty, plus one sixty seven and a half q s zero, equals zero."
   → (-1.569 x 10^-3)(37.5) + (1.765 x 10^-3)(30) + 167.5 q_s0 = 0 -> -5.89 x 10^-3 + 167.5 q_s0 = 0.
4. "So q s zero is three point five two times ten to the minus five, S y. A small correction, all the way around."
   → q_s0 = 3.52 x 10^-5 S_y (MINT); totals: q_12 = q_34 = 3.52 x 10^-5 S_y, q_23 = -1.534 x 10^-3 S_y, q_41 = 1.800 x 10^-3 S_y.

## S11_P1_Centre [132] Where the shear centre is
Picture: the box with final flows: both webs flowing up.
1. "Both webs now carry shear flow upward. Times three hundred millimeters, the right web carries zero point four six S y, the left web zero point five four. Together, exactly S y."
   → web forces 0.460 S_y and 0.540 S_y; sum 1.000 S_y (GOOD check).
2. "Take moments about the left web. The right web's force, zero point four six S y, acts five hundred millimeters away: two hundred thirty S y."
   → 0.460 S_y x 500 = 230.0 S_y.
3. "The small flows in the top and bottom skins form a couple the other way, about five point three S y."
   → 3.52 x 10^-5 S_y x 500 x 300 = 5.27 S_y, opposite sense.
4. "So S y times xi equals two thirty minus five point three, and xi is two hundred twenty four point eight millimeters from the left web. Left of the middle, because the left booms are heavier."
   → xi = 224.8 mm, ROSE, glowing; a dashed line marks the shear centre on the box.
5. "Your turn. Pause here and do checkpoint three point one: the same steps for the practice box."
   → self.checkpoint("3.1", "Practice box: booms, then the shear centre")

# Episode 4: Torsion of Multi-Cell Sections | one shear flow per cell

## S12_Cells [71] One shear flow per cell
Picture: a generic three-cell wing box under a torque T.
1. "Now twist a wing box with several cells. With no axial restraint, there's no direct stress, so the booms play no part at all."
   → three-cell box (straight walls), LILAC torque arrow; booms fade.
2. "Each cell carries its own constant shear flow. A wall shared by two cells carries the difference."
   → cell_flow arrows q_I (MINT), q_II (LIME), q_III; the shared walls labelled q_I - q_II, q_II - q_III in GOLD.
3. "The torque is two times the area of each cell, times its shear flow, added up."
   → T = sum 2 A_R q_R; per cell 2 A q terms.
4. "But that's one equation, and there's one unknown for every cell. We need more."
   → "N unknowns, 1 equation" note.

## S13_Twist [118] Every cell twists the same
Picture: two cells side by side, the shared wall highlighted.
1. "The extra equations come from compatibility. The whole section rotates as one piece, so every cell has the same rate of twist."
   → both cells rotate together by a small angle; d theta/dz the same.
2. "For one cell, the rate of twist is one over two A G, times the integral of q d s over t around that cell."
   → d theta/dz = (1/(2 A_R G)) closed integral q ds/t.
3. "Your turn. Pause here and do checkpoint four point one in your guide."
   → self.checkpoint("4.1", "Write the twist rate for cell I of a two-cell box")
4. "Around cell one, every wall carries q one, except the shared wall, which carries q one minus q two. Call delta the integral of d s over t. Then it's q one delta one, minus q two delta one two."
   → (1/(2 A_I G)) (q_I delta_I - q_II delta_12): each term built from the walls.
5. "Set cell one's rate equal to cell two's. With the torque equation, that's two equations for two unknowns."
   → the two boxed equations.

## S14_Gstar [70] Walls made of different materials
Picture: the twist-rate formula with G inside the integral.
1. "Skins and spars are often different materials. Then G is different on each wall, and it moves inside the integral."
   → d theta/dz = (1/(2A)) closed integral q ds/(G t).
2. "The trick: pick a reference G, and scale each wall's thickness by its G over the reference. That's the modulus weighted thickness, t star."
   → t* = (G/G_REF) t; delta = integral ds/t*.
3. "Everything else stays the same. Your notes' three cell example works out to seven point one, eight point nine and four point two newtons per millimeter."
   → the slide's 3-cell result: q_I = 7.1, q_II = 8.9, q_III = 4.2 N/mm.

# Episode 5: Homework Problem 2 | the two-cell wing box

## S15_P2_Setup [107] Set up the two-cell box
Picture: sect.hw_twocell(); the HW table.
1. "Here's the two cell wing box. The torque is counterclockwise, but the problem doesn't give its size, so we'll find each shear flow per unit of torque."
   → hw_twocell with cells I and II, LILAC counterclockwise torque; note "T not given: solve per unit T".
2. "Notice the boom areas in the table. In pure torsion they don't matter at all."
   → boom area column struck through.
3. "Take the reference G as twenty seven thousand six hundred. The webs keep their thickness. The skins, at twenty four thousand two hundred, are scaled by zero point eight seven seven."
   → G_REF = 27 600; t* = (24 200/27 600) t = 0.8768 t for walls 12, 56, 23, 45.
4. "Now delta for each wall is its length over t star."
   → table: delta_16 = 156.3, delta_25 = 199.8, delta_34 = 165.6, delta_12 = delta_56 = 806.4, delta_23 = delta_45 = 1581.2.
5. "Around cell one: one nineteen sixty nine. Around cell two: thirty five twenty eight. The shared spar alone: one ninety nine point eight."
   → delta_I = 156.3 + 2(806.4) + 199.8 = 1969.0; delta_II = 165.6 + 2(1581.2) + 199.8 = 3527.8; delta_25 = 199.8.

## S16_P2_Solve [177] Solve for the shear flows
Picture: the two boxed equations; the two-cell box on the left.
1. "Equal twist: q one times nineteen sixty nine, minus q two times one ninety nine point eight, over two times two thirty two thousand, equals the same for cell two."
   → (1969.0 q_I - 199.8 q_II)/(2 x 232 000) = (-199.8 q_I + 3527.8 q_II)/(2 x 258 000).
2. "Cross multiply and collect. That leaves five fifty four million q one equals eight hundred seventy million q two. So q one is one point five seven times q two."
   → expand; 554.4 x 10^6 q_I = 870.0 x 10^6 q_II; q_I = 1.569 q_II.
3. "Now the torque equation. T equals two times two thirty two thousand q one, plus two times two fifty eight thousand q two. Substituting, that's one point two four four million q two."
   → T = 2(232 000) q_I + 2(258 000) q_II = (728 200 + 516 000) q_II = 1.244 x 10^6 q_II.
4. "So q two is zero point eight zero four times ten to the minus six, T. And q one is one point two six one times ten to the minus six, T."
   → q_II = 0.804 x 10^-6 T; q_I = 1.261 x 10^-6 T (T in N mm), MINT and LIME, boxed.
5. "For a torque of one kilonewton meter: one point two six in cell one, zero point eight zero in cell two, and the spar carries the difference, zero point four six newtons per millimeter."
   → per 1 kNm: q_I = 1.26, q_II = 0.80, spar 0.46 N/mm; arrows on the box, both cells counterclockwise.
6. "Your turn. Pause here and do checkpoint five point one: a two cell box with a real torque."
   → self.checkpoint("5.1", "Practice two-cell box: T = 15 kN m")

## S17_Recap [94] Recap
Picture: key_box lines, one per beat.
1. "Let's recap. Booms carry the direct stress. The skin carries shear, and any direct stress it takes is added to the booms with t D b over six times two plus the stress ratio."
   → card 1: booms carry sigma; B = (t_D b/6)(2 + sigma_2/sigma_1).
2. "The shear flow is constant between booms, and jumps by minus S y over I x x, B r y r, at each one. Closed sections: cut, march, then close with q s zero."
   → card 2: q_2 - q_1 = -(S_y/I_xx) B_r y_r; q_s = q_b + q_s0.
3. "In pure torsion, each cell has one shear flow. The torque gives one equation, and equal twist gives the rest. Different materials just scale the thickness."
   → card 3: T = sum 2 A_R q_R; equal d theta/dz; t* = (G/G_REF) t.
