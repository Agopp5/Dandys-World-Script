# Orbit Determination: An Orbit's Address  (~21 min)

**Hook**: a tracking station's six raw numbers (r0, v0) tell you nothing you can picture, and all six keep changing.
**Insight**: six different numbers, the classical orbital elements, describe the same orbit; five are frozen and
each is a picture: size, shape, and three turns (Omega about K, i about the node line, omega about h).
**Payoff**: the hook's numbers turn out to be a Molniya orbit, and its strange inclination of 63.4 degrees is exactly
the angle where Earth's bulge stops turning the perigee (episode 6).

Audience: an AERSP 309 student who found the notes confusing. Go slowly, one idea per beat, every algebra step on
screen. Pace is deliberately unhurried; let pictures sit.

Every file starts:
```python
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})
```
Never change the VOICE/STYLE lines: the narration is already voiced with exactly these, and any change re-bills.

Hue meanings, the whole series: Omega (node angle, the node line and ascending node) SKY; inclination i EMBER;
argument of periapsis omega MINT; true anomaly theta / argument of latitude u GOLD; angular momentum h and h-hat
LILAC; eccentricity vector, p-hat and periapsis ROSE; q-hat and the node vector n LIME. The ECI axes I, J, K are
INK2. The orbit curve itself is INK (white) unless a scene says otherwise; the Earth is the globe() from orbit3d.
Position r: INK, velocity v: EMBER is taken, so draw v in ACCENT.

3D: use the shared kit `orbit3d.py` (View, globe, curve, arrow3, line3, arc3, disc3, label3, axes3, cpn, orbit,
rv_perifocal). Draw in Earth radii (Earth radius 1). For clarity the drawn orbits are NOT to scale unless a beat
says so: use a = 2.4, e = 0.5 for the generic orbit and a = 3.0, e = 0.6 for the drawn Molniya (its true size,
a = 4.16 R_E, e = 0.741, does not fit). Generic orientation for episode 2: Omega = 50 deg, i = 40 deg,
omega = 60 deg, theta0 = 40 deg. Keep the 3D view on the left two thirds and text/equations on the right
(place(m, "right")), unless a beat is pure algebra.
Notation: matrices are C_{PN} (rows: p-hat, q-hat, h-hat written in ECI), C_1, C_3 the course's elementary rotations
(rows = new axes in old): C_3(x) = [[cos x, sin x, 0], [-sin x, cos x, 0], [0, 0, 1]],
C_1(x) = [[1, 0, 0], [0, cos x, sin x], [0, -sin x, cos x]]. Use theta (not nu) for true anomaly.

## Facts (assert the ones your scene shows)
- mu = 3.986e5 km^3/s^2. Earth equatorial radius 6378.137 km, polar 6356.752 km (difference 21.4 km).
- Kluever Example 3.1 state vector (ECI): r0 = (9031.5, -5316.9, -1647.2) km, v0 = (-2.8640, 5.1112, -5.0805) km/s.
  |r0| = 10,609.0 km, |v0| = 7.7549 km/s. Energy = v0^2/2 - mu/r0 = -7.5027 km^2/s^2. a = -mu/(2 E) = 26,563.6 km
  (period 11.97 h, about 12 h).
- h = r0 x v0 = (35,432, 50,602, 30,934) km^2/s, |h| = 69,086 km^2/s.
- e-vector = (v x h)/mu - r/r = (0.1903, 0.2718, -0.6627), e = 0.7411. Check: sqrt(1 + 2 E h^2/mu^2) = 0.7411.
  r_p = a(1-e) = 6,877 km (altitude about 500 km); r_a = a(1+e) = 46,250 km (altitude about 39,870 km).
- p-hat = e/e = (0.2568, 0.3668, -0.8942); h-hat = h/h = (0.5129, 0.7324, 0.4478);
  q-hat = h-hat x p-hat = (-0.8192, 0.5736, 0.0000). C_PN = [[0.2568, 0.3668, -0.8942], [-0.8192, 0.5736, 0],
  [0.5129, 0.7324, 0.4478]].
- i = arccos(C33) = arccos(0.4478) = 63.4 deg. Omega = atan2(C31, -C32) = atan2(0.5129, -0.7324) = 145.0 deg.
  omega = atan2(C13, C23) = atan2(-0.8942, 0) = -90 deg, i.e. 270 deg.
- Textbook route: n = K x h = (-50,602, 35,432, 0), |n| = 61,774; cos Omega = -0.8192, sin Omega = 0.5736
  (second quadrant: 145 deg). cos omega = n.e/(n e) = 0.00001 (90 or 270); e_Z = -0.6627 < 0 so 270 deg.
  Coincidence worth one sentence: with omega = 270, q-hat points exactly at the ascending node (q-hat = n-hat).
- cos theta0 = e.r0/(e r0) = 0.1736, arccos = 80 deg; r0.v0 = -44,673 km^2/s < 0 (radius shrinking, heading to
  perigee) so theta0 = 360 - 80 = 280 deg.
- Third row of C_PN: (sin i sin Omega, -sin i cos Omega, cos i). Third column: (sin omega sin i, cos omega sin i, cos i).
  Derivation: row 3 of C3(w) is (0,0,1), so row 3 of C_PN = row 3 of C1(i) times C3(Omega) = (0, -sin i, cos i) C3(Omega).
  Column 3: C_PN k = C3(w) C1(i) (0,0,1) = C3(w) (0, sin i, cos i) = (sin w sin i, cos w sin i, cos i).
- Reverse (Molniya, theta = 280 deg): p = a(1-e^2) = 11,974 km, h = sqrt(mu p) = 69,086, r = p/(1 + e cos theta) =
  10,609 km. r_P = (r cos theta, r sin theta, 0) = (1,842, -10,448, 0) km. v_P = (mu/h)(-sin theta, e + cos theta, 0) =
  (5.682, 5.278, 0) km/s. r_N = C_PN^T r_P = (9,031, -5,317, -1,647) km; v_N = (-2.864, 5.111, -5.081) km/s
  (round trip matches r0, v0).
- J2 = 1.08263e-3. Potential V = -(mu/r) [1 - J2 (R/r)^2 (3 sin^2(phi) - 1)/2], phi = geocentric latitude.
  Omega-dot = -(3 n J2 R^2) / (2 a^2 (1-e^2)^2) cos i.  omega-dot = -(3 n J2 R^2) / (2 a^2 (1-e^2)^2) (5/2 sin^2 i - 2).
  n = sqrt(mu/a^3) (mean motion). a, e, i: no secular change, only periodic wiggles.
- ISS-like orbit (400 km circular, i = 51.6 deg): Omega-dot = -5.0 deg/day, omega-dot = +3.7 deg/day.
- Sun-synchronous: Omega-dot = +360 deg per 365.24 days = +0.9856 deg/day. Needs cos i < 0: i = 97.4 deg at 500 km,
  98.2 deg at 700 km, 98.6 deg at 800 km (circular).
- Critical inclination: omega-dot = 0 when sin^2 i = 4/5: i = 63.43 deg (or 116.57 deg). Molniya: Omega-dot =
  -0.149 deg/day, omega-dot = 0.0004 deg/day (essentially frozen).

# Episode 1: An Orbit's Address | state vectors versus orbital elements

## S01_Hook [120] The problem
Picture: left, the 3D view with globe and ECI axes; right, two column vectors r0 and v0 (Example 3.1 values).
1. "A tracking station measures a satellite and radios down six numbers: three for its position, and three for its velocity."
   → r0 and v0 columns write in on the right; on the left, arrows r (INK) and v (ACCENT) appear from the Earth.
2. "Here they are. Can you tell what this orbit looks like? Is it round or stretched? Tilted or flat? Where is the satellite in its loop?"
   → three small question marks pop beside the 3D view; nothing else drawn.
3. "Worse, as the satellite moves, all six numbers keep changing."
   → the satellite moves along the (still invisible) Molniya path; the six components tick as live readouts.
4. "Now here is the same orbit, described by a different set of six numbers."
   → the drawn Molniya ellipse fades in; the r0, v0 columns morph into a list: a = 26,564 km, e = 0.741, i = 63.4 deg, Omega = 145 deg, omega = 270 deg, theta0 = 280 deg (each in its hue).
5. "Five of them never change. Only the last one moves, like the hand of a clock. And every one of them has a picture you can see."
   → satellite moves; only the theta readout changes; the five frozen ones get a soft glow.
6. "This lesson is about those six numbers: what each one means, how to get them from a measurement, and how to go back."
   → three chips: meaning, r v to elements, elements to r v.

## S02_ECI_Frame [158] The ECI frame
Picture: globe with axes; an inset (right) of Earth's yearly orbit around the Sun with the tilted equator plane.
1. "First we need a frame to measure everything in. It's called the Earth centered inertial frame, or E C I."
   → globe + axes3 grow in; title chip "ECI".
2. "K points through the North Pole. I and J lie in the plane of the equator."
   → K highlighted; a translucent equatorial disc fades in containing I and J.
3. "But which way, exactly, does I point? It has to be a direction the stars agree on."
   → I arrow pulses with a question mark.
4. "Picture Earth going around the Sun. Earth's equator is tilted about twenty three and a half degrees to the plane of its orbit, the ecliptic."
   → right inset: Sun, Earth's circular path (ecliptic), a small Earth with a tilted equator ring; the 23.4 deg tilt marked.
5. "The two planes cross along one line. On the March equinox, that line points from the Earth straight at the Sun. That is the vernal equinox direction, and I points along it."
   → the intersection line glows; an arrow from Earth toward the Sun labeled "vernal equinox"; it maps onto I in the main view.
6. "J is ninety degrees from I in the equator, completing a right handed set with K."
   → J and K pulse; a right-hand-rule curl arrow I to J about K.
7. "One more detail matters a lot. This frame does not spin with the Earth. The Earth turns underneath it once a day, while I, J and K stay fixed against the stars."
   → the globe rotates (redraw with azim of the surface only, axes fixed); a tiny clock "1 day".

## S03_Six_Numbers [113] Two ways to say the same thing
Picture: right column grows a three-group list; left shows the corresponding picture for each group.
1. "Position and velocity together are called the state vector. Those six numbers completely determine the orbit."
   → r, v columns with a brace "state vector, all six change".
2. "The classical orbital elements are a different six numbers that determine the same orbit."
   → list a, e | i, Omega, omega | theta0 appears in three bracketed groups.
3. "Two describe size and shape: the semi major axis a, and the eccentricity e. You already know these from the last chapter."
   → 2D ellipse; a marked; e sweeps 0 to 0.7 and back (shape changes).
4. "Three describe orientation: how steeply the orbit plane is tilted, which way that tilt faces, and how the ellipse is turned within its plane."
   → the ellipse lifts into 3D and tilts and turns (generic orientation); group 2 highlights.
5. "And one says where the satellite is at the moment of the measurement: the true anomaly at epoch, theta zero."
   → a GOLD dot on the orbit with the theta arc from periapsis.
6. "Five constants and one clock. Next, we'll build the three orientation angles, one turn at a time."
   → key_box: "a, e: size, shape   |   i, Omega, omega: orientation   |   theta0: where, now".

# Episode 2: Placing the Orbit in Space | three turns: Omega, i, omega

## S04_Turn_Omega [93] Turn one: Omega
Picture: 3D view, globe, axes, equatorial disc; generic orbit (a 2.4, e 0.5).
1. "Here's a way to see all three angles. Start with the orbit lying flat in the equator, with its periapsis pointing straight along I."
   → orbit drawn flat in the equatorial plane, periapsis on +I; a ROSE dot at periapsis.
2. "Turn one: spin the whole orbit about K by an angle, capital Omega."
   → animate Omega 0 to 50 deg; SKY arc in the equator from I; label Omega.
3. "The direction where the periapsis now points is about to become a hinge. It's called the line of nodes."
   → a SKY dashed line through the center along the turned direction, both ways.
4. "Capital Omega is measured in the equator, from I, counterclockwise as seen from the North Pole. It can be anything from zero to three hundred sixty degrees. Its name is the right ascension of the ascending node."
   → camera rises (elev up) to look down; the arc is shown counterclockwise; name chip "RAAN".

## S05_Turn_i [147] Turn two: inclination
Picture: continue from the Omega-turned orbit.
1. "Turn two: tilt the orbit about the line of nodes, by the inclination, i."
   → animate i 0 to 40 deg about the node line; EMBER arc between equator and orbit plane at the node.
2. "Now the orbit plane and the equator cross along the line of nodes. Each lap, the satellite crosses the equator twice."
   → satellite moves around; flashes at both crossings.
3. "Where it crosses heading north is the ascending node. Where it crosses heading south is the descending node. Now you can see why Omega is measured to the ascending node."
   → SKY dot "ascending node", dimmer dot "descending node"; Omega arc re-highlighted ending at the ascending node.
4. "The inclination is also the angle between K and the angular momentum vector h, which sticks straight out of the orbit plane."
   → LILAC h arrow from the center; EMBER arc between K and h labeled i.
5. "Inclination only runs from zero to one hundred eighty degrees."
   → readout i = 40 deg.
6. "Below ninety, the satellite travels eastward, the same way the Earth spins. That's a prograde orbit. At exactly ninety, it passes over both poles: a polar orbit. Above ninety, it travels westward: retrograde."
   → i sweeps 40 to 90 to 150; motion arrow on the orbit flips from eastward to westward (seen from above); labels prograde, polar, retrograde as it passes.
7. "So i says how steeply the plane is tilted, and Omega says which way the tilt faces."
   → back to 40 deg; both arcs highlighted together.

## S06_Turn_omega [181] Turn three: omega, then theta zero
Picture: the tilted orbit from S05.
1. "Turn three happens inside the tilted plane. Spin the ellipse about h by the argument of periapsis, little omega."
   → animate omega 0 to 60 deg; the ellipse rotates within its plane; periapsis moves away from the ascending node.
2. "So little omega is the angle from the ascending node to the periapsis, measured in the orbit plane, in the direction the satellite moves."
   → MINT arc in the orbit plane from the ascending node to periapsis, labeled omega.
3. "The ellipse is now completely placed. The last number, the true anomaly at epoch theta zero, is the angle from periapsis to the satellite at the moment of the measurement."
   → GOLD dot at theta0 = 40 deg; GOLD arc from periapsis.
4. "Notice the order of the turns: about K, then about the node line, then about h. Three, then one, then three. Keep that pattern in mind; it comes back as a rotation matrix."
   → three small badges "1: K (3)", "2: node line (1)", "3: h (3)" stack on the right.
5. "Here's the Molniya orbit from the beginning, built the same way."
   → morph to the drawn Molniya: Omega 145, i 63.4, omega 270.
6. "Little omega of two seventy puts the perigee at the southernmost point of the orbit. So the long, slow apogee half hangs high over the northern hemisphere, where it can watch Russia for hours."
   → ROSE perigee dot below the equator; a GOLD bracket on the apogee half above; satellite slows near apogee.
7. "Quick question before we move on."
   → self.predict("If the inclination were greater than ninety degrees, which way would the satellite cross the equator at the ascending node?", <this line>)
8. "Still northward. The ascending node is always the northbound crossing. What changes is that the motion over the Earth runs westward instead of east."
   → short demo with i = 120: the northbound crossing highlighted, westward arrow.

## S07_Special_Cases [120] When an angle does not exist
Picture: two small 3D views side by side, then a key box.
1. "Two kinds of orbit break these definitions."
   → split screen: left a circular inclined orbit, right an elliptical orbit in the equator.
2. "A circular orbit has no periapsis, so little omega and theta have nothing to measure from. Instead we use the argument of latitude, u, measured from the ascending node straight to the satellite. For any orbit, u equals little omega plus theta."
   → left: GOLD arc from the ascending node to the satellite labeled u; equation u = omega + theta.
3. "An equatorial orbit never crosses the equator, so it has no ascending node, and capital Omega is undefined. Then we use the longitude of periapsis, measured from I straight to the periapsis. It equals capital Omega plus little omega."
   → right: arc from I to periapsis; equation varpi = Omega + omega.
4. "And the true longitude, capital Omega plus little omega plus theta, measures from I all the way to the satellite. It always exists."
   → equation l = Omega + omega + theta under both.
5. "That's every orbital element and what it looks like."
   → key_box: a: size; e: shape; i: tilt, 0 to 180; Omega: node, 0 to 360; omega: node to periapsis, 0 to 360; theta0: periapsis to satellite, 0 to 360.

# Episode 3: The Perifocal Frame | the rotation matrix C_PN

## S08_Perifocal [120] A frame that rides on the orbit
Picture: 3D view with the generic orbit; then a flat 2D view of the orbit plane on the right.
1. "Your notes describe the orbit's orientation with a frame that rides on the orbit. It's called the perifocal frame."
   → generic orbit (Omega 50, i 40, omega 60) with globe.
2. "p hat points from the focus to the periapsis, the same direction as the eccentricity vector. q hat is ninety degrees ahead of it, in the orbit plane, in the direction of motion. And h hat sticks out of the plane, completing the set."
   → p-hat (ROSE), q-hat (LIME), h-hat (LILAC) grow from the center one at a time.
3. "In this frame the orbit is simple. The satellite sits at r cosine theta along p hat, and r sine theta along q hat, with nothing out of the plane."
   → right: the orbit plane drawn flat (2D) with p and q axes, satellite at theta, components dashed; r_P = (r cos theta, r sin theta, 0).
4. "So all of the three dimensional information lives in one question: how are p hat, q hat and h hat pointed in the E C I frame?"
   → the three arrows pulse in the 3D view; question mark.

## S09_DCM [145] The direction cosine matrix C_PN
Picture: mostly algebra on the right; small 3D view with the PQW triad on the left.
1. "That's exactly what a direction cosine matrix stores. Write p hat, q hat and h hat in their I, J, K components, and stack them as rows. That stack is C P N."
   → matrix with rows labeled p-hat, q-hat, h-hat (colored), entries as dot products p.I, p.J, p.K etc.
2. "Each entry is a dot product, the cosine of the angle between one perifocal axis and one E C I axis."
   → one entry (p-hat dot I) highlighted with its angle drawn in 3D.
3. "Because we built the orientation with three turns, Omega about K, then i about the node line, then omega about h, the matrix is a product of three simple rotations."
   → the three badges from S06 return.
4. "C P N equals C three of little omega, times C one of i, times C three of capital Omega. Read it right to left: first the Omega turn, then the tilt, then the spin in the plane."
   → C_PN = C_3(omega) C_1(i) C_3(Omega), with an arrow under it pointing right to left and the three badges under their factors.
5. "These are the same elementary rotations from the kinematics lessons. C three turns about the third axis. C one turns about the first."
   → C_3(x) and C_1(x) matrices written out.

## S10_Multiply [126] Multiplying out what we need
Picture: algebra, line by line, with a grey reason beside each step (sheet-style rows).
1. "We don't need all nine entries. Start with the third row, which is h hat."
   → C_PN shown with its third row boxed in LILAC.
2. "The third row of C three of omega is just zero, zero, one. So the third row of the whole product is the third row of C one of i, times C three of Omega."
   → step: row3(C_PN) = (0, 0, 1) C_1(i) C_3(Omega) = (0, -sin i, cos i) C_3(Omega). Reason: "row 3 of C3 is (0,0,1)".
3. "Multiply that row into C three of Omega. The result is sine i sine Omega, minus sine i cosine Omega, and cosine i."
   → step: = (sin i sin Omega, -sin i cos Omega, cos i). Reason: "row times matrix".
4. "Check it with the picture. h hat leans away from K by the angle i, so its K component is cosine i."
   → small 3D: h-hat with the i arc from K; the cos i projection onto K dashed.
5. "Now the third column. Multiply C P N by the unit vector along K, working from the right."
   → step: C_PN K = C_3(omega) C_1(i) (0, 0, 1) = C_3(omega) (0, sin i, cos i).
6. "That gives sine omega sine i, cosine omega sine i, and cosine i."
   → step: = (sin omega sin i, cos omega sin i, cos i), boxed. Both results in a small table: C31, C32, C33, C13, C23.

## S11_Read_Angles [197] Reading the angles back out
Picture: the five entries from S10 on the left; unit-circle sketch for atan2 on the right.
1. "Now reverse it. The corner entry C three three is cosine i. So i is the arc cosine of C three three."
   → i = arccos(C33).
2. "Arc cosine always returns an angle from zero to one hundred eighty degrees. That's exactly the range of inclination, so no extra check is needed."
   → number line 0 to 180 with i's range shaded; GOOD check mark.
3. "Next, Omega. C three one is sine i sine Omega, and minus C three two is sine i cosine Omega. Since sine i is never negative, this pair points in the direction of Omega."
   → C31 and -C32 placed as (y, x) of a point on a circle of radius sin i; the angle from the x axis is Omega.
4. "So Omega is atan two of C three one and minus C three two."
   → Omega = atan2(C31, -C32), boxed in SKY.
5. "Why atan two and not arc cosine? Arc cosine can only give zero to one eighty. It can't tell one forty five degrees from two hundred fifteen. atan two looks at the signs of both entries, so it lands in the correct quadrant."
   → two points mirrored across the x axis with the same cosine; arccos gives the same answer for both; atan2 separates them.
6. "The same reasoning for the third column gives little omega equals atan two of C one three and C two three."
   → omega = atan2(C13, C23), boxed in MINT.
7. "Two practical notes. atan two returns minus one eighty to one eighty, so add three sixty to a negative answer. And if i is zero, both pairs are zero over zero: that's the equatorial orbit, with no node."
   → two small note rows.

# Episode 4: From r and v to the Elements | the Molniya example, step by step

## S12_Energy_a [107] Step one: the semi major axis
Picture: the measurement card stays at top right for the whole episode; algebra below it.
1. "Now the real job: start from one measurement and find all six elements. We'll use the textbook's example."
   → card: r0 = (9031.5, -5316.9, -1647.2) km, v0 = (-2.8640, 5.1112, -5.0805) km/s; the r0, v0 arrows in the 3D view.
2. "First, the lengths. The position vector is ten thousand six hundred nine kilometers long. The speed is seven point seven five five kilometers per second."
   → |r0| = 10,609 km, |v0| = 7.7549 km/s (each with its square-root-of-sum line).
3. "The energy is v squared over two, minus mu over r. That's minus seven point five zero three kilometers squared per second squared. Negative, so it's an ellipse."
   → E = v0^2/2 - mu/r0 = 30.069 - 37.572 = -7.5027 km^2/s^2. Reason: "negative: bound, an ellipse".
4. "Energy gives the semi major axis directly: a equals minus mu over two E. That's twenty six thousand five hundred sixty four kilometers."
   → a = -mu/(2E) = 26,564 km, boxed.
5. "That's about four Earth radii, and a period of almost exactly twelve hours."
   → T = 2 pi sqrt(a^3/mu) = 11.97 h.

## S13_h_and_e [135] Step two: angular momentum and eccentricity
Picture: algebra; 3D view shows h and e vectors appear.
1. "Next, the angular momentum: h equals r cross v."
   → h = r0 x v0 = (35,432, 50,602, 30,934) km^2/s; |h| = 69,086. LILAC h arrow grows in the 3D view.
2. "h sticks straight out of the orbit plane, so it already pins down the plane's tilt. We'll use that in a moment."
   → the orbit plane (disc perpendicular to h) fades in.
3. "Now the eccentricity vector, from the last chapter: v cross h over mu, minus the unit vector along r."
   → e = (v x h)/mu - r/r = (0.1903, 0.2718, -0.6627). ROSE e arrow grows from the center.
4. "Its length is the eccentricity: zero point seven four one one. And it points from the focus straight to the perigee."
   → e = |e| = 0.7411; the ROSE arrow extended to a perigee dot.
5. "Your notes give a second way to get the same number, from energy and h alone: e equals the square root of one plus two E h squared over mu squared. It agrees."
   → e = sqrt(1 + 2 E h^2/mu^2) = 0.7411, GOOD check.
6. "So the perigee radius is about six thousand eight hundred seventy seven kilometers, just five hundred kilometers up, and the apogee is about forty six thousand two hundred fifty kilometers away."
   → r_p = a(1-e) = 6,877 km; r_a = a(1+e) = 46,250 km.

## S14_Build_C [75] Step three: build C_PN, read the inclination
Picture: three unit vectors become the rows of C_PN.
1. "Now build the perifocal frame from these two vectors. p hat is the eccentricity vector divided by its length."
   → p-hat = (0.2568, 0.3668, -0.8942).
2. "h hat is h divided by its length."
   → h-hat = (0.5129, 0.7324, 0.4478).
3. "And q hat completes the right handed set: h hat cross p hat."
   → q-hat = h-hat x p-hat = (-0.8192, 0.5736, 0.0000). The three arrows in the 3D view.
4. "Stack them as rows, and that's C P N, with real numbers in it."
   → the three rows slide into the matrix C_PN.
5. "The corner entry is zero point four four seven eight. Its arc cosine is the inclination: sixty three point four degrees."
   → C33 highlighted; i = arccos(0.4478) = 63.4 deg in EMBER; the i arc between K and h in 3D.

## S15_Omega [139] Step four: Omega, two ways
Picture: C_PN third row highlighted; unit circle for the quadrant.
1. "For capital Omega, take the first two entries of the bottom row. C three one is zero point five one two nine. C three two is zero point seven three two four, so minus C three two is negative."
   → C31 = 0.5129, -C32 = -0.7324 marked.
2. "Positive sine, negative cosine. That's the second quadrant. atan two gives one hundred forty five degrees."
   → point in quadrant two on a unit circle; Omega = atan2(0.5129, -0.7324) = 145.0 deg in SKY.
3. "The textbook gets the same answer with the node vector: n equals K cross h. It points along the line of nodes, toward the ascending node."
   → n = K x h = (-50,602, 35,432, 0); LIME n arrow along the node line in 3D.
4. "Its components give cosine Omega equals minus zero point eight one nine two, and sine Omega equals zero point five seven three six. The same quadrant, the same one hundred forty five degrees."
   → cos Omega = -0.8192, sin Omega = 0.5736, check mark; Omega arc in the equator in 3D.
5. "A fun coincidence: q hat equals the node direction here. That's not an accident; it happens because little omega turns out to be two seventy."
   → q-hat arrow and n-hat arrow overlap; brief glow.

## S16_omega [115] Step five: little omega
Picture: third column of C_PN highlighted.
1. "Little omega uses the third column: C one three is minus zero point eight nine four two, and C two three is zero."
   → C13, C23 marked.
2. "atan two of a negative number and zero is minus ninety degrees. Add three sixty: little omega is two hundred seventy degrees."
   → omega = atan2(-0.8942, 0) = -90 deg -> 270 deg in MINT.
3. "The textbook route: the cosine of omega is n dot e over n e, which is essentially zero. So omega is ninety or two seventy. Arc cosine can't tell which."
   → cos omega = 0.00001 -> 90 or 270?
4. "Look at the eccentricity vector's K component: minus zero point six six two seven. Perigee is below the equator, so it's two seventy."
   → e_Z = -0.6627 < 0 -> 270 deg; in 3D the perigee dot is below the equatorial disc.
5. "That matches the picture: perigee at the very bottom of the orbit, apogee high over the north."
   → MINT arc from the ascending node to perigee in the orbit plane.

## S17_theta0 [101] Step six: where is the satellite?
Picture: e and r0 arrows in 3D and on the 2D orbit plane.
1. "Last, the true anomaly. Its cosine is e dot r over e times r, which comes out to zero point one seven three six."
   → cos theta0 = e.r0/(e r0) = 0.1736.
2. "Arc cosine says eighty degrees. But the satellite could be eighty degrees past perigee, or eighty degrees before it."
   → 2D orbit plane: two candidate dots at +80 and -80 (280) from perigee.
3. "Which one is it?"
   → self.predict("80 degrees or 280 degrees? What could tell you?", <this line>)
4. "Check r dot v. It's minus forty four thousand six hundred seventy three. Negative means the distance is shrinking: the satellite is falling toward perigee. So theta zero is three sixty minus eighty: two hundred eighty degrees."
   → r0.v0 = -44,673 km^2/s < 0; the inbound candidate highlighted; theta0 = 280 deg in GOLD.
5. "And that's all six: a, e, i, capital Omega, little omega, and theta zero, from one measurement."
   → sheet with the six results; recipe rows: energy -> a; h and e-vector -> e; C_PN -> i, Omega, omega; e.r with r.v check -> theta0.

# Episode 5: Going Back | from elements to r and v

## S18_Perifocal_rv [145] Step one: r and v in the perifocal frame
Picture: 2D orbit plane on the left (p and q axes), algebra right.
1. "Sometimes we need the reverse: start from the elements and find r and v in E C I. It takes two steps, and the first one is easy."
   → title row "elements -> (r, v)".
2. "In the perifocal frame the orbit is flat. The position is r cosine theta, r sine theta, zero, where r comes from the orbit equation."
   → r_P = (r cos theta, r sin theta, 0), r = p/(1 + e cos theta).
3. "The velocity is mu over h, times minus sine theta, e plus cosine theta, zero. That's the hodograph result from the last chapter."
   → v_P = (mu/h)(-sin theta, e + cos theta, 0).
4. "For the Molniya at theta equals two eighty: p is eleven thousand nine hundred seventy four kilometers, h is sixty nine thousand eighty six, and r is ten thousand six hundred nine."
   → p = 11,974 km, h = 69,086 km^2/s, r = 10,609 km.
5. "So the position is one thousand eight hundred forty two, minus ten thousand four hundred forty eight, zero kilometers, and the velocity is five point six eight two, five point two seven eight, zero kilometers per second."
   → r_P = (1,842, -10,448, 0) km; v_P = (5.682, 5.278, 0) km/s; arrows drawn in the 2D plane.

## S19_Rotate_Back [148] Step two: rotate into ECI
Picture: the 2D plane lifts into the 3D view while the algebra completes.
1. "Step two: rotate into E C I. The rows of C P N are p hat, q hat and h hat, so going back uses the transpose."
   → r_N = C_PN^T r_P.
2. "In words: r is its p component times p hat, plus its q component times q hat. The transpose just adds those arrows in E C I coordinates."
   → in 3D: 1,842 p-hat + (-10,448) q-hat tip to tail landing on r.
3. "Multiply it out, and we get nine thousand thirty one, minus five thousand three hundred seventeen, minus one thousand six hundred forty seven kilometers. The velocity comes out minus two point eight six four, five point one one one, minus five point zero eight one."
   → r_N = (9,031, -5,317, -1,647) km; v_N = (-2.864, 5.111, -5.081) km/s.
4. "Those are exactly the measured r and v we started from. The round trip closes."
   → side by side with r0, v0 from S12; GOOD check marks.
5. "And here's why elements are worth the trouble. To move the satellite forward in time, five numbers stay frozen. Only theta advances, using Kepler's equation. Then one rotation gives r and v again."
   → satellite moves; five elements frozen, theta ticking; arrow "Kepler's equation -> theta -> r_P, v_P -> C_PN^T -> r, v".

# Episode 6: Earth Is Not a Sphere | J2 and the critical inclination

## S20_Oblate [116] The bulge
Picture: a globe squashed (exaggerated) with the equatorial bulge shaded; a tilted orbit around it.
1. "Five of the elements never change. But that's only exactly true if the Earth is a perfect sphere. It isn't."
   → globe; five-element list from before with a question mark.
2. "Earth spins, so it bulges at the equator. It's about twenty one kilometers wider than it is tall."
   → exaggerated oblate Earth; equatorial 6,378 km vs polar 6,357 km labels; "difference 21 km (exaggerated here)".
3. "Your notes add one correction term to the gravity potential. Its size is set by a single number, J two, about one point oh eight times ten to the minus three."
   → V = -(mu/r)[1 - J2 (R/r)^2 (3 sin^2 phi - 1)/2]; J2 = 1.08263 x 10^-3.
4. "The extra mass at the equator tugs a tilted orbit, trying to pull its plane down toward the equator. Like a hand pushing on a spinning top."
   → tug arrows on the tilted orbit where it passes over the bulge.
5. "And like a top, the orbit doesn't fall flat. It precesses: the whole orbit plane slowly swings around the pole."
   → animate Omega slowly decreasing; the node line sweeps westward; a ghost trail of earlier node lines.

## S21_Node_Drift [150] The node drifts
Picture: formula on the right, the drifting plane on the left; a Sun inset later.
1. "The drift rate of the node is Omega dot equals minus three n J two R squared, over two a squared, times one minus e squared, squared, times cosine i."
   → Omega-dot formula written; n = sqrt(mu/a^3) noted as the mean motion.
2. "Read the cosine i. For a prograde orbit, cosine i is positive, so Omega dot is negative: the node slides westward. For the space station, about five degrees per day."
   → cos i > 0 -> westward drift; ISS: -5.0 deg/day.
3. "For a polar orbit, cosine i is zero, and the node doesn't drift at all. For a retrograde orbit, it drifts eastward."
   → i sweeps to 90 (drift stops) then 98 (drift reverses).
4. "Engineers use that eastward drift on purpose. If the node turns exactly once per year, about one degree per day, the orbit plane keeps the same angle to the Sun all year."
   → Sun inset: Earth around the Sun with the orbit plane turning to stay at the same angle to the Sun.
5. "That's a sun synchronous orbit. At seven hundred kilometers, it needs an inclination of about ninety eight degrees."
   → i = 98.2 deg at 700 km; "same lighting every pass".
6. "Meanwhile a, e and i don't drift. They only wiggle a little each orbit, like your notes sketch."
   → two small plots: a(t) wiggling flat; Omega(t) wiggling with a steady downward trend.

## S22_Critical [157] The critical inclination
Picture: omega-dot formula; graph of (5/2 sin^2 i - 2) versus i; the Molniya at the end.
1. "J two turns the ellipse inside its plane too. The perigee drifts at omega dot equals minus three n J two R squared over two a squared, one minus e squared, squared, times five halves sine squared i, minus two."
   → omega-dot formula.
2. "The sign depends on that last bracket. Here it is, plotted against inclination."
   → graph of 5/2 sin^2 i - 2 for i from 0 to 180; positive region shaded MINT, negative region shaded ROSE.
3. "It crosses zero when five halves sine squared i equals two. So sine squared i is four fifths, and i is sixty three point four three degrees."
   → step lines: 5/2 sin^2 i = 2 -> sin^2 i = 4/5 -> i = 63.43 deg (and 116.57 deg); zero crossings marked.
4. "At that inclination, the perigee simply stops turning. It's called the critical inclination."
   → the perigee dot on an orbit at 63.4 deg stays put while a 50 deg orbit's perigee drifts.
5. "Now look back at the hook. The Molniya orbit was inclined at sixty three point four degrees. That's no accident."
   → the hook's six-element list returns with i = 63.4 deg glowing.
6. "At that inclination, the perigee stays parked over the south, so the long, slow apogee stays over Russia, year after year, with no fuel spent. Its node still drifts a little, about point one five degrees per day, but that doesn't matter for coverage."
   → Molniya in 3D: perigee fixed in the south; node line drifting slowly; label omega-dot = 0, Omega-dot = -0.15 deg/day.

## S23_Recap [145] Recap
Picture: a stack of key boxes.
1. "Let's recap. The E C I frame points I at the vernal equinox and K at the North Pole, and it doesn't spin with the Earth."
   → key line 1.
2. "Six elements place any orbit: a and e for size and shape, three turns for orientation, capital Omega about K, i about the node line, little omega about h, and theta for where the satellite is."
   → key line 2 with the colored symbols.
3. "Those three turns are the rows of C P N, C three of omega, C one of i, C three of Omega. The angles come back out with an arc cosine and two atan twos."
   → key line 3.
4. "From r and v: energy gives a, h and the eccentricity vector give e and the frame, and r dot v settles theta. The transpose takes you back."
   → key line 4.
5. "And Earth's bulge slowly turns the node and the perigee, except at the critical inclination, where the perigee stands still."
   → key line 5; fade to the Molniya orbit.
