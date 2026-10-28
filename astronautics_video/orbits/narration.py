"""Narration for the AERSP 309 'Two-Body Orbital Mechanics' lesson series (12 videos).

Parts 1-7 build the concepts slowly (Kepler -> Newton -> constants of motion ->
orbit equation -> ellipse -> velocity -> open trajectories). Parts 8-9 work the
assigned textbook problems; parts 10-12 work HW 3 problems 1, 2 and 4, each
introducing the one new tool it needs.
"""

STYLE = (
    "Narrate like a calm, curious math explainer on a video: clear and warm, at a steady, "
    "natural speaking pace, with brief pauses only where a sentence ends."
)

SCRIPT = {
    # ------------------------------------------------------------ 1: Kepler's laws
    "O1Concept": [
        ("o1_01", "Welcome to a new chapter: orbits. Four hundred years ago, Johannes Kepler spent years fitting "
                  "Tycho Brahe's careful measurements of the planet Mars. Out of that work came three laws. In this "
                  "lesson we'll see what the three laws say, and we'll build the tools we need to turn them into "
                  "physics."),
        ("o1_02", "Kepler's first law, from sixteen oh nine. The orbit of a planet is an ellipse, with the Sun at "
                  "one of its two foci. Here's one way to draw an ellipse. Put two pins in a board, tie a loop of "
                  "string around them, and pull it tight with a pencil. The sum of the two distances to the pins "
                  "never changes."),
        ("o1_03", "The Sun sits at one focus. The other focus is empty. It's called the vacant focus. Notice that "
                  "the Sun is not at the center. So the planet's distance from the Sun changes as it goes around. "
                  "There's a closest point, and a farthest point."),
        ("o1_04", "Kepler's second law, also from sixteen oh nine. The line joining the planet to the Sun sweeps "
                  "out equal areas in equal amounts of time. Watch the two shaded wedges. Each one took the same "
                  "amount of time. Near the Sun, the planet moves fast, and the wedge is short and wide. Far away, "
                  "it moves slowly, and the wedge is long and thin. But the areas are the same."),
        ("o1_05", "Kepler's third law, from sixteen nineteen. The square of a planet's orbital period is "
                  "proportional to the cube of its mean distance from the Sun. T squared is proportional to a "
                  "cubed. If we plot the planets with period against distance, on logarithmic axes, they all fall "
                  "on one straight line, with a slope of three halves."),
        ("o1_06", "These laws describe the motion, but they don't explain it. That came from Isaac Newton. To follow "
                  "his reasoning, we first need a good way to describe motion around the Sun. We'll use polar "
                  "coordinates, and a frame that rides along with the planet."),
        ("o1_07", "Put the Sun at the origin. The unit vector e r points from the Sun to the planet. The unit vector "
                  "e theta is ninety degrees ahead of it, in the direction of motion. And e three points out of the "
                  "screen, completing a right handed set. The planet's position is simply r equals r times e r, "
                  "where r is the distance."),
        ("o1_08", "Here's the catch. As the planet moves, e r turns. This whole frame rotates, at the rate theta dot, "
                  "about e three. So its angular velocity relative to the inertial frame is theta dot, e three."),
        ("o1_09", "How fast does a turning unit vector change? We met this in the transport theorem. The derivative "
                  "of a unit vector fixed in a rotating frame is omega cross that vector. So e r dot is theta dot e "
                  "three cross e r, which is theta dot e theta. And e theta dot is theta dot e three cross e theta, "
                  "which is minus theta dot e r."),
        ("o1_10", "Here's a picture of why. When e r turns through a small angle, d theta, its tip moves a distance d "
                  "theta, sideways, in the e theta direction. Its length can't change, because it's a unit vector. "
                  "So its rate of change points along e theta."),
        ("o1_11", "Now the velocity. Differentiate r e r with the product rule. We get r dot e r, plus r times e r "
                  "dot. And e r dot is theta dot e theta. So the velocity is r dot e r, plus r theta dot e theta."),
        ("o1_12", "Two pieces. r dot is the radial velocity: how fast the distance is growing. r theta dot is the "
                  "transverse velocity: how fast the planet is swinging around the Sun."),
        ("o1_13", "Now let's translate Kepler's second law into math. In a short time, delta t, the position moves "
                  "from r to r plus delta r. The radius sweeps out a thin triangle. Its area is one half, times the "
                  "length of r, times the length of delta r, times the sine of the angle between them. That's half "
                  "the magnitude of r cross delta r."),
        ("o1_14", "The cross product also gives the direction, e three, out of the plane. So the swept area, as a "
                  "vector, is one half r cross delta r. Divide by delta t, and let delta t shrink to zero. The rate "
                  "of sweeping area is one half, r cross v."),
        ("o1_15", "Kepler says this rate is constant. And the orbit stays in one plane, so the direction is constant "
                  "too. So r cross v is a constant vector."),
        ("o1_16", "Let's compute r cross v with our polar pieces. r e r, cross, r dot e r plus r theta dot e theta. "
                  "e r cross e r is zero. e r cross e theta is e three. So r cross v equals r squared theta dot, e "
                  "three. The area sweeps at the rate one half r squared theta dot."),
        ("o1_17", "This vector gets a name. h equals r cross v is the specific angular momentum. The angular momentum "
                  "of the planet is capital H, equals r cross m v. Specific means per unit mass, so h is just H "
                  "divided by m."),
        ("o1_18", "Now Newton's question: what could change H? Differentiate r cross m v. The first term is v cross "
                  "m v, which is zero, because any vector crossed with itself is zero. The second term is r cross m "
                  "a, which is r cross F."),
        ("o1_19", "Kepler's second law says H doesn't change. So r cross F must be zero. That means the force is "
                  "parallel to r. The force on a planet always points along the line to the Sun. It's a central "
                  "force. That's the first thing Kepler's laws tell us about gravity."),
        ("o1_20", "Let's recap. Kepler gave us three laws: ellipses, equal areas, and T squared proportional to a "
                  "cubed. The polar frame turns at theta dot, so velocity is r dot e r plus r theta dot e theta. "
                  "Equal areas means r cross v is constant, and that means the force is central. Next time, we'll "
                  "find out how strong the force is."),
    ],

    # ------------------------------------------------- 2: ellipses -> inverse square
    "O2Concept": [
        ("o2_01", "Last time, Kepler's second law told us that the force on a planet points at the Sun. In this "
                  "lesson, the first law will tell us how strong the force is: it falls off like one over r "
                  "squared. Then the third law will tell us that the same constant works for every planet. And "
                  "finally, we'll set up the two body problem."),
        ("o2_02", "We need the acceleration. Start from the velocity, r dot e r plus r theta dot e theta, and "
                  "differentiate it slowly with the product rule. The first term gives two pieces: r double dot e "
                  "r, and r dot times e r dot. The second term is a product of three things, so it gives three "
                  "pieces."),
        ("o2_03", "Now replace e r dot with theta dot e theta, and e theta dot with minus theta dot e r. Then "
                  "collect everything along e r and everything along e theta."),
        ("o2_04", "Along e r we get r double dot, minus r theta dot squared. Along e theta, we get two r dot theta "
                  "dot, plus r theta double dot. That's the acceleration in polar coordinates."),
        ("o2_05", "Look at the e theta part. It's exactly one over r, times the time derivative of r squared theta "
                  "dot. Check it with the product rule: the derivative of r squared theta dot is two r r dot theta "
                  "dot, plus r squared theta double dot. Divide by r, and you get our expression."),
        ("o2_06", "But r squared theta dot is h, and h is constant. So the e theta part of the acceleration is zero. "
                  "Good. That agrees with the force being purely radial."),
        ("o2_07", "So only one equation is left. Call the force per unit mass f. Then f equals r double dot, minus r "
                  "theta dot squared. And since h equals r squared theta dot, theta dot is h over r squared. "
                  "Substituting, f equals r double dot, minus h squared over r cubed. We'll call this equation one."),
        ("o2_08", "Here's the difficulty. Kepler told us the shape of the orbit, r as a function of theta. But "
                  "equation one has derivatives with respect to time. The trick is to use u equals one over r, and "
                  "to change variables from time to angle using the chain rule: d by d t equals theta dot, times d "
                  "by d theta. And theta dot equals h u squared."),
        ("o2_09", "First derivative. r is one over u, so r dot is minus one over u squared, times u dot. And u dot is "
                  "theta dot times d u by d theta, which is h u squared, d u by d theta. The u squared terms "
                  "cancel. So r dot is simply minus h, d u by d theta."),
        ("o2_10", "Second derivative. h is constant, so r double dot is minus h, times the time derivative of d u by "
                  "d theta. Use the chain rule once more: that's theta dot, times d squared u by d theta squared. "
                  "With theta dot equal to h u squared, r double dot equals minus h squared u squared, d squared u "
                  "by d theta squared."),
        ("o2_11", "Put this into equation one. The second term, h squared over r cubed, is h squared u cubed. "
                  "Factor out h squared u squared. We get f equals minus h squared u squared, times the quantity, u "
                  "double prime plus u. This is equation two. It works for any central force."),
        ("o2_12", "Now Kepler's first law. An ellipse with the Sun at a focus has a polar equation: r equals p, over "
                  "one plus e cosine theta. Here e is the eccentricity, which describes the shape, and p is called "
                  "the semi latus rectum. It's the distance from the focus straight out to the ellipse, at ninety "
                  "degrees. We'll derive this equation ourselves in a later lesson."),
        ("o2_13", "Flip it over: u equals one plus e cosine theta, all over p. Differentiate: u prime is minus e over "
                  "p, sine theta. Differentiate again: u double prime is minus e over p, cosine theta."),
        ("o2_14", "Now add u double prime and u. The cosine terms cancel exactly. All that's left is one over p. A "
                  "constant!"),
        ("o2_15", "So f equals minus h squared over p, times u squared, which is one over r squared. The force is "
                  "inversely proportional to the square of the distance. And the minus sign means it points toward "
                  "the Sun. It's an attraction."),
        ("o2_16", "Is the constant, h squared over p, the same for every planet? That's what the third law decides. "
                  "The area rate is h over two, and it's constant. Over one full period, T, the planet sweeps the "
                  "whole ellipse, whose area is pi a b. So pi a b equals h T over two, and h equals two pi a b over "
                  "T."),
        ("o2_17", "For an ellipse, p equals b squared over a. So h squared over p equals four pi squared a squared b "
                  "squared over T squared, times a over b squared. The b squared cancels, and we're left with four "
                  "pi squared, a cubed over T squared."),
        ("o2_18", "Kepler's third law says that a cubed over T squared is the same for all the planets. So h squared "
                  "over p is the same for all of them. It isn't a property of any planet. It's a property of the "
                  "Sun. We call it mu, the gravitational parameter. Then f equals minus mu over r squared. In "
                  "vector form, r double dot equals minus mu r over r cubed."),
        ("o2_19", "Newton went one step further. Mu is proportional to the mass of the attracting body: mu equals G "
                  "M, where G is the universal gravitational constant. Its value was first measured by Henry "
                  "Cavendish in seventeen ninety eight. This is the law of universal gravitation."),
        ("o2_20", "But wait. If the Sun pulls on the planet, the planet pulls on the Sun, equally and oppositely. So "
                  "both bodies move. This is the two body problem. Take masses M and m, at positions r one and r "
                  "two in an inertial frame. The relative position is r equals r two minus r one."),
        ("o2_21", "Write Newton's second law for each. m r two double dot equals minus G M m r over r cubed. And M r "
                  "one double dot equals plus G M m r over r cubed. Add the two equations. The right hand sides "
                  "cancel, so M r one double dot plus m r two double dot equals zero."),
        ("o2_22", "That's the acceleration of the center of mass, times the total mass. So the center of mass never "
                  "accelerates. It drifts along at constant velocity, which makes it a perfectly good inertial "
                  "origin."),
        ("o2_23", "Now subtract. First divide each equation by its own mass. r two double dot is minus G M r over r "
                  "cubed, and r one double dot is plus G m r over r cubed. Subtracting, r double dot equals minus G, "
                  "times M plus m, r over r cubed."),
        ("o2_24", "It's the same equation as before, with mu equal to G times M plus m. When the satellite is tiny "
                  "compared with the planet, mu is just G M. From now on, this is the equation of motion: r double "
                  "dot equals minus mu r over r cubed."),
        ("o2_25", "Recap. In polar coordinates, the radial acceleration is r double dot minus r theta dot squared. "
                  "The substitution u equals one over r turns it into an equation in theta. Ellipses force the "
                  "inverse square law. The third law makes mu the same for every planet. And the two body problem "
                  "reduces to one equation, with mu equal to G times M plus m. Kepler only ever saw ellipses, but "
                  "Newton's equation allows other shapes too. We'll meet them soon."),
    ],

    # ------------------------------------------------- 3: constants of motion
    "O3Concept": [
        ("o3_01", "Our equation of motion is r double dot equals minus mu r over r cubed. Solving it head on is "
                  "hard. A smarter approach is to look for quantities that never change as the satellite moves. "
                  "These are called constants of motion. There are two big ones: angular momentum, and energy."),
        ("o3_02", "Start with angular momentum, h equals r cross v. Take its time derivative with the product rule. "
                  "The first term is v cross v, which is zero. The second term is r cross r double dot. Substitute "
                  "the equation of motion: r cross minus mu r over r cubed. That's a multiple of r cross r, which "
                  "is also zero."),
        ("o3_03", "Both terms vanish. So h is constant: in size and in direction. Last time we got this from "
                  "Kepler's observations. Now it comes straight out of Newton's law."),
        ("o3_04", "This has a big consequence. r dot h is r dot r cross v, and that's always zero. So r is always "
                  "perpendicular to h. Since h never changes direction, the satellite is stuck in one plane: the "
                  "plane through the center of the Earth, perpendicular to h. Every orbit is planar."),
        ("o3_05", "In the plane, we already computed h equals r squared theta dot. So r squared theta dot is "
                  "constant. That's Kepler's second law, equal areas in equal times. And notice: we only used the "
                  "fact that the force is central."),
        ("o3_06", "Here's another useful way to write h. Only the transverse part of the velocity contributes to r "
                  "cross v. So h equals r times v theta. Define the flight path angle, gamma, as the angle between "
                  "the velocity and the local horizontal, e theta. Then v theta is v cosine gamma, and h equals r v "
                  "cosine gamma."),
        ("o3_07", "At the closest and farthest points, the velocity is exactly horizontal, so gamma is zero. There, "
                  "h is simply r times v. So r p v p equals r a v a. The satellite is fastest where it's closest."),
        ("o3_08", "Now energy. The kinetic energy per unit mass is one half v squared, which is one half r dot dotted "
                  "with r dot. Differentiate with the product rule. We get one half, r double dot dot r dot, plus r "
                  "dot dot r double dot. Those are the same, so the derivative is r dot dotted with r double dot."),
        ("o3_09", "Substitute the equation of motion. The derivative becomes minus mu over r cubed, times r dot "
                  "dotted with r."),
        ("o3_10", "What is r dotted with r dot? r is r e r, and r dot is r dot e r plus r theta dot e theta. Only "
                  "the e r parts survive the dot product. So r dot r dot is r times r dot. The derivative of the "
                  "kinetic energy is minus mu r dot over r squared."),
        ("o3_11", "Now compare with the derivative of mu over r. By the chain rule, it's minus mu over r squared, "
                  "times r dot. That's exactly the same thing! So the derivative of the kinetic energy, minus mu over "
                  "r, is zero."),
        ("o3_12", "So v squared over two minus mu over r is constant. This is the specific mechanical energy, which "
                  "we'll call E. The first term is kinetic energy per unit mass. The second, minus mu over r, is "
                  "the potential energy per unit mass."),
        ("o3_13", "Why the minus sign? We're free to choose where the potential is zero, and we choose infinity. So "
                  "the potential is zero infinitely far away, and negative everywhere else. Here is its graph. "
                  "It's a well. The closer you are to the planet, the deeper you sit in it."),
        ("o3_14", "The total energy is a horizontal line on this graph. The kinetic energy is the gap between the "
                  "line and the curve, and it can never be negative. So the satellite can only be where the line "
                  "is above the curve."),
        ("o3_15", "If E is negative, the line hits the curve at some distance. The satellite can't go beyond it. "
                  "It's bound, and it comes back. If E is zero or positive, the line never meets the curve, and the "
                  "satellite can escape to infinity."),
        ("o3_16", "And as the satellite climbs, its potential energy goes up, so its kinetic energy goes down. It "
                  "slows. When it falls back in, it speeds up again. That's the same thing the second law told us, "
                  "seen through energy."),
        ("o3_17", "Recap. The angular momentum vector, h, is constant. That makes every orbit planar, and it gives "
                  "Kepler's second law. The energy, v squared over two minus mu over r, is constant. Negative "
                  "energy means a bound orbit. Next, we'll find a third constant, and it will give us the shape of "
                  "the orbit."),
    ],

    # ------------------------------------------------- 4: the orbit equation
    "O4Concept": [
        ("o4_01", "We want the shape of the orbit, r as a function of theta, straight from the equation of motion. "
                  "The trick is to find one more conserved vector. Consider v cross h."),
        ("o4_02", "Differentiate it. The derivative of v cross h is r double dot cross h, plus v cross h dot. But h "
                  "is constant, so the second term is zero. Substitute the equation of motion, and h equals r cross "
                  "v. We get minus mu over r cubed, times r cross, r cross v."),
        ("o4_03", "To expand a double cross product, use the identity: a cross, b cross c, equals b times a dot c, "
                  "minus c times a dot b. Here a and b are both r, and c is v. So r cross, r cross v, equals r times "
                  "r dot v, minus v times r dot r."),
        ("o4_04", "We know r dot v is r r dot, and r dot r is r squared. So it equals r r dot times the vector r, "
                  "minus r squared v. Multiply by minus mu over r cubed. The derivative of v cross h becomes mu, "
                  "times r v minus r dot times the vector r, all over r squared."),
        ("o4_05", "Now here's the clever part. What's the time derivative of the unit vector r over r? By the "
                  "quotient rule, it's r times v, minus r dot times the vector r, all over r squared. That's exactly "
                  "what we just found!"),
        ("o4_06", "So the derivative of v cross h equals mu times the derivative of r over r. Bring everything to "
                  "one side: the derivative of v cross h minus mu r over r is zero. So v cross h, minus mu r over r, "
                  "is a constant vector. Call it c."),
        ("o4_07", "Now dot both sides with r. On the left, r dot c. On the right, r dot v cross h, minus mu r. For "
                  "the triple product, we can cycle the vectors: r dot v cross h equals h dot r cross v, which is h "
                  "dot h, or h squared. So r dot c equals h squared minus mu r."),
        ("o4_08", "Let theta be the angle between r and c. Then r dot c is r c cosine theta. So r c cosine theta "
                  "equals h squared minus mu r. Collect the r terms: r times mu plus c cosine theta equals h "
                  "squared."),
        ("o4_09", "Divide by mu and solve for r. r equals h squared over mu, all over, one plus c over mu cosine "
                  "theta. This is the orbit equation."),
        ("o4_10", "It has exactly the form of a conic section, r equals p over one plus e cosine theta. Matching the "
                  "pieces, p equals h squared over mu, and e equals c over mu. The angular momentum sets the size, "
                  "and c sets the shape."),
        ("o4_11", "Dividing c by mu gives the eccentricity vector. e equals v cross h over mu, minus r over r. Its "
                  "length is the eccentricity. And since r is smallest when theta is zero, the eccentricity vector "
                  "points from the focus to the closest point, the periapsis."),
        ("o4_12", "The angle theta, measured from periapsis in the direction of motion, is called the true anomaly. "
                  "Your homework calls it f. Same angle."),
        ("o4_13", "Why are these called conic sections? Take a double cone and slice it with a flat plane. Slice "
                  "straight across, and you get a circle. Tilt the plane a little, less steeply than the side of the "
                  "cone, and you get an ellipse."),
        ("o4_14", "Tilt it until it's exactly parallel to the side of the cone, and the curve never closes. That's a "
                  "parabola. Tilt it steeper still, and the plane cuts both halves of the cone. You get a hyperbola, "
                  "with two branches."),
        ("o4_15", "The eccentricity picks which one. e equals zero is a circle. e between zero and one is an "
                  "ellipse. e equals one is a parabola. And e greater than one is a hyperbola. Watch the orbit as e "
                  "grows, with p held fixed. The ellipse stretches, opens up at e equals one, and becomes a "
                  "hyperbola."),
        ("o4_16", "There's one more way to see a conic. Draw a line called the directrix, a distance p over e from "
                  "the focus. A conic is every point whose distance to the focus is e times its distance to the "
                  "directrix."),
        ("o4_17", "Check that this gives our equation. The distance to the directrix is p over e, minus r cosine "
                  "theta. So r equals e times that, which is p minus e r cosine theta. Move the r term over: r "
                  "times one plus e cosine theta equals p. The same orbit equation."),
        ("o4_18", "Finally, three special points. At theta equals zero, r is p over one plus e. That's the periapsis "
                  "radius. At theta equals ninety degrees, r equals p. That's what the semi latus rectum is. And for "
                  "an ellipse, at a hundred and eighty degrees, r is p over one minus e: the apoapsis radius."),
        ("o4_19", "Recap. v cross h minus mu r over r is constant. Dotting with r gives the orbit equation, r equals p "
                  "over one plus e cosine theta, with p equal to h squared over mu. The eccentricity vector points "
                  "to periapsis, theta is the true anomaly, and e decides the type of conic."),
    ],

    # ------------------------------------------------- 5: ellipse anatomy, energy, period
    "O5Concept": [
        ("o5_01", "Let's look closely at the closed orbit, the ellipse. Here's the vocabulary. The center is C. The "
                  "focus, F, is where the planet is. a is the semi major axis, half the longest width. b is the semi "
                  "minor axis. c is the distance from the center to the focus. And p, the semi latus rectum."),
        ("o5_02", "The full length of the major axis is two a. It runs from periapsis to apoapsis, so two a equals r "
                  "p plus r a. Use the orbit equation for each: p over one plus e, plus p over one minus e."),
        ("o5_03", "Put them over a common denominator, one minus e squared. The top becomes p times one minus e, plus "
                  "one plus e, which is two p. So two a equals two p over one minus e squared. That gives p equals a "
                  "times one minus e squared."),
        ("o5_04", "Now put that back into the periapsis and apoapsis radii. r p equals a times one minus e. And r a "
                  "equals a times one plus e. Add them and divide by two: a is the average of the closest and "
                  "farthest distances."),
        ("o5_05", "The distance from the center to the focus is c equals a minus r p. That's a minus a times one "
                  "minus e, which is a e. So e equals c over a. The eccentricity is how far the focus sits from the "
                  "center, as a fraction of a."),
        ("o5_06", "Now b. Go to the end of the minor axis. By the string property, its distances to the two foci add "
                  "up to two a. By symmetry, they're equal, so each one is a. That makes a right triangle with legs "
                  "b and c, and hypotenuse a."),
        ("o5_07", "So b squared plus a squared e squared equals a squared, and b equals a times the square root of one "
                  "minus e squared. And since p is a times one minus e squared, p also equals b squared over a."),
        ("o5_08", "A quick note on names. The general words are periapsis and apoapsis. Around the Earth, we say "
                  "perigee and apogee. Around the Sun, perihelion and aphelion. Around the Moon, perilune and "
                  "apolune. And around Jupiter, perijove and apojove."),
        ("o5_09", "Now let's connect energy to the geometry. Energy is the same everywhere on the orbit, so evaluate it "
                  "where it's easiest: at periapsis. There, the velocity is perpendicular to r, so h equals r p v "
                  "p."),
        ("o5_10", "From the orbit equation, h is the square root of mu p, and p is a times one minus e squared. So v "
                  "p equals h over r p, which is the square root of mu a times one minus e squared, over a times one "
                  "minus e."),
        ("o5_11", "Square it. One minus e squared is one minus e times one plus e. One factor of one minus e cancels, "
                  "and one a cancels. v p squared equals mu, times one plus e, over a times one minus e."),
        ("o5_12", "Now the energy. E equals v p squared over two, minus mu over r p. Write both terms over a times one "
                  "minus e. Factor that out, and inside the brackets we have one plus e over two, minus one. That's e "
                  "minus one, over two."),
        ("o5_13", "The e minus one on top cancels the one minus e on the bottom, leaving a minus sign. E equals minus "
                  "mu over two a. The energy depends only on the semi major axis. Not on the eccentricity at all."),
        ("o5_14", "Combine this with the definition of energy. v squared over two, minus mu over r, equals minus mu "
                  "over two a. Solve for v squared: v squared equals mu, times two over r, minus one over a. This "
                  "is called the vis viva equation. It gives the speed anywhere on the orbit, from just r and a."),
        ("o5_15", "The sign of E matches the type of orbit. Negative energy means positive a: an ellipse. Zero "
                  "energy means a is infinite: a parabola. Positive energy means a negative a: a hyperbola."),
        ("o5_16", "Two special speeds. For a circle, r equals a everywhere. Vis viva gives v squared equals mu over r. "
                  "That's the circular speed, the square root of mu over r. In low Earth orbit it's about seven and "
                  "a half kilometers per second."),
        ("o5_17", "For escape, set the energy to zero. v squared over two equals mu over r, so the escape speed is the "
                  "square root of two mu over r. That's root two times the circular speed. And it doesn't depend on "
                  "direction, as long as you don't hit the planet."),
        ("o5_18", "Let's watch this. Launch horizontally from the same point, with more and more speed. Slower than "
                  "circular speed, the orbit is an ellipse that falls inside, and the launch point is the apoapsis. At "
                  "exactly circular speed, it's a circle. Faster, the ellipse stretches outward, and the launch point "
                  "becomes the periapsis. At escape speed, it opens into a parabola. Faster still, a hyperbola."),
        ("o5_19", "Last, the period. The area sweeps at the constant rate h over two. In one full period, it sweeps "
                  "the whole ellipse, pi a b. So pi a b equals h T over two, and T equals two pi a b over h."),
        ("o5_20", "Substitute b equals a root one minus e squared, and h equals the square root of mu a times one minus "
                  "e squared. The square roots of one minus e squared cancel! T equals two pi a squared over root mu "
                  "a, which is two pi times the square root of a cubed over mu."),
        ("o5_21", "The period depends only on a. Square it, and T squared equals four pi squared over mu, times a "
                  "cubed. That's Kepler's third law, now with the constant filled in. We'll also use the mean motion, "
                  "n, equals two pi over T, which is the square root of mu over a cubed."),
        ("o5_22", "Recap. p equals a times one minus e squared. r p and r a are a times one minus e, and one plus e. "
                  "b is a root one minus e squared. The energy is minus mu over two a, which gives vis viva. And the "
                  "period is two pi root a cubed over mu."),
    ],

    # ------------------------------------------------- 6: velocity on the orbit
    "O6Concept": [
        ("o6_01", "We know where the satellite is. Now let's find how fast it's moving, and in which direction. "
                  "First, two frames that both sit at the focus. The perifocal frame is fixed: p hat points to "
                  "periapsis, along the eccentricity vector, q hat is ninety degrees ahead in the orbit plane, and w "
                  "hat points along h."),
        ("o6_02", "The orbital frame rides with the satellite: e r, e theta, and e h, which is the same as w hat. The "
                  "two frames differ by a single rotation about h, through the true anomaly, theta."),
        ("o6_03", "Write the orbital axes in perifocal components. e r is cosine theta p hat plus sine theta q hat. e "
                  "theta is minus sine theta p hat plus cosine theta q hat. Those are the rows of the direction "
                  "cosine matrix, C O P. It's our old friend, the third axis rotation, C three of theta."),
        ("o6_04", "Now the velocity components. Recall the velocity is r dot e r plus r theta dot e theta. Start with "
                  "the transverse part, v theta, equals r theta dot. Since theta dot is h over r squared, v theta is "
                  "h over r."),
        ("o6_05", "From the orbit equation, one over r is one plus e cosine theta, over p. So v theta equals h over p, "
                  "times one plus e cosine theta. And since p is h squared over mu, h over p is mu over h. So v "
                  "theta equals mu over h, times one plus e cosine theta."),
        ("o6_06", "Next, the radial part, v r, equals r dot. Differentiate the orbit equation with the chain rule. r "
                  "dot equals p e sine theta, over one plus e cosine theta squared, times theta dot."),
        ("o6_07", "Now substitute theta dot equals h over r squared, which is h times one plus e cosine theta "
                  "squared, over p squared. The squared terms cancel. r dot equals h e sine theta over p, which is "
                  "mu over h, times e sine theta."),
        ("o6_08", "Look at what this says. v r is zero at periapsis and at apoapsis, where sine theta is zero. It's "
                  "positive on the way out, for theta between zero and a hundred and eighty degrees. And negative on "
                  "the way back in."),
        ("o6_09", "The flight path angle, gamma, is the angle from the local horizontal up to the velocity. Its "
                  "tangent is v r over v theta. The mu over h cancels, so tangent gamma equals e sine theta, over "
                  "one plus e cosine theta."),
        ("o6_10", "Watch gamma as the satellite goes around. It's zero at periapsis, positive while climbing, back "
                  "to zero at apoapsis, and negative while falling back in. Using the arctangent keeps gamma between "
                  "minus ninety and ninety degrees, so the sign comes out right automatically."),
        ("o6_11", "Here's a beautiful picture. Write the velocity in the fixed perifocal frame. Convert e r and e "
                  "theta, and collect terms. v equals mu over h, times minus sine theta p hat, plus e plus cosine "
                  "theta, q hat."),
        ("o6_12", "Now draw every velocity vector from one common point. The tips trace out a perfect circle! It has "
                  "radius mu over h, and its center is shifted up by e mu over h. This is called the hodograph. The "
                  "velocity is a rotating arrow of fixed length, plus a constant arrow."),
        ("o6_13", "From the circle you can read off the extremes. The fastest speed is mu over h times one plus e, at "
                  "periapsis. The slowest is mu over h times one minus e, at apoapsis. Their ratio is one plus e over "
                  "one minus e, which is exactly r a over r p. That matches r p v p equals r a v a."),
        ("o6_14", "One more useful rate. Theta dot equals h over r squared. Using the orbit equation and h equals the "
                  "square root of mu p, theta dot equals the square root of mu over p cubed, times one plus e "
                  "cosine theta, squared. The true anomaly races through periapsis and crawls near apoapsis."),
        ("o6_15", "Recap. v r equals mu over h e sine theta. v theta equals mu over h, one plus e cosine theta. The "
                  "flight path angle has tangent e sine theta over one plus e cosine theta. The orbital frame is C "
                  "three of theta from the perifocal frame. And the hodograph is a circle."),
    ],

    # ------------------------------------------------- 7: parabolas and hyperbolas
    "O7Concept": [
        ("o7_01", "Now the trajectories that don't come back. First, the parabola, with e equals one. It's the "
                  "border between bound and unbound. Its energy is exactly zero, and its semi major axis is "
                  "infinite."),
        ("o7_02", "Zero energy means v squared over two equals mu over r at every point. So the speed is always the "
                  "local escape speed, the square root of two mu over r. The satellite just barely escapes, with "
                  "nothing left over."),
        ("o7_03", "The orbit equation becomes r equals p over one plus cosine theta. At periapsis, r p equals p over "
                  "two. As theta approaches a hundred and eighty degrees, the denominator goes to zero, and r goes to "
                  "infinity. The two arms never close."),
        ("o7_04", "The flight path angle has a neat form. Tangent gamma equals sine theta over one plus cosine "
                  "theta. Use the half angle identities: sine theta is two sine theta over two cosine theta over "
                  "two, and one plus cosine theta is two cosine squared theta over two."),
        ("o7_05", "Cancel, and tangent gamma equals tangent theta over two. So on a parabola, gamma equals theta over "
                  "two. Far away, theta approaches a hundred and eighty degrees, so gamma approaches ninety: the "
                  "satellite heads straight out."),
        ("o7_06", "Now the hyperbola, e greater than one. The energy is positive. Since E equals minus mu over two a, "
                  "the semi major axis is negative. That seems strange, but all our formulas keep working if we "
                  "simply let a be negative."),
        ("o7_07", "For example, r p equals a times one minus e. Both a and one minus e are negative, so r p comes out "
                  "positive. And p equals a times one minus e squared is positive too."),
        ("o7_08", "Where does r go to infinity? When the denominator, one plus e cosine theta, is zero. That happens "
                  "at cosine theta equals minus one over e. This angle is the true anomaly of the asymptote, theta "
                  "infinity. It's between ninety and a hundred and eighty degrees. The satellite can only ever be "
                  "between minus theta infinity and plus theta infinity."),
        ("o7_09", "How fast is it going when it gets far away? Use vis viva, and let r go to infinity. Two over r "
                  "vanishes, so v infinity squared equals minus mu over a, which is positive. This is the hyperbolic "
                  "excess speed. The energy is simply v infinity squared over two."),
        ("o7_10", "Here's the geometry. The hyperbola has a center, and two straight asymptotes that it approaches far "
                  "away. The distance from the center to periapsis is the size of a. The focus is a distance a e from "
                  "the center. And b equals the size of a, times the square root of e squared minus one."),
        ("o7_11", "The satellite comes in along one asymptote and leaves along the other. The angle between the "
                  "incoming and outgoing directions is the turning angle, delta. It's how much the flyby bends the "
                  "path."),
        ("o7_12", "The outgoing direction is at theta infinity. By symmetry, the incoming one is at minus theta "
                  "infinity, but moving inward. Work it out, and delta equals two theta infinity minus a hundred and "
                  "eighty degrees."),
        ("o7_13", "So sine of delta over two equals sine of theta infinity minus ninety degrees, which is minus "
                  "cosine theta infinity. And that's one over e. So sine delta over two equals one over e. Large e "
                  "means a straighter path and a small turn. e near one means a sharp hairpin turn."),
        ("o7_14", "Notice the other branch of the hyperbola, around the empty focus. It's a valid conic, but it "
                  "would need a repulsive force. A satellite always flies on the branch wrapped around the attracting "
                  "body."),
        ("o7_15", "Let's put all four conics side by side. Circle: e zero, a positive, energy negative. Ellipse: e "
                  "between zero and one, a positive, energy negative. Parabola: e one, a infinite, energy zero. "
                  "Hyperbola: e greater than one, a negative, energy positive."),
    ],

    # ------------------------------------------------- 8: examples, closed orbits
    "O8Examples": [
        ("o8_01", "Time to use these tools. We'll start with homework three, problem three, and then work textbook "
                  "problems two sixteen, two seventeen, two twenty eight, and two thirty two. As the textbook says, "
                  "we'll use mu equals three point nine eight six times ten to the fifth kilometers cubed per second "
                  "squared, and an Earth radius of six thousand three hundred seventy eight kilometers."),
        ("o8_02", "Homework problem three. Prove three facts about an ellipse with periapsis r p and apoapsis r a. "
                  "First, a equals one half, r p plus r a. We showed r p is a times one minus e, and r a is a times "
                  "one plus e. Add them. The e terms cancel, leaving two a. Divide by two, and we're done."),
        ("o8_03", "Second, b equals the square root of r p r a. Multiply the two radii: a squared, times one minus e, "
                  "times one plus e. That's a squared times one minus e squared. And that's exactly b squared, since b "
                  "is a root one minus e squared. Take the square root."),
        ("o8_04", "Third, the semi latus rectum. p equals b squared over a. b squared is r p r a, and a is r p plus "
                  "r a over two. So p equals two r p r a, over r p plus r a."),
        ("o8_05", "A note on the homework sheet. It prints the denominator as r p plus r a plus a. That extra a "
                  "looks like a typo. Here's a quick check: for a circle, r p and r a both equal r, and p should be r. "
                  "Our formula gives two r squared over two r, which is r. With the extra a, you'd get two thirds of "
                  "r, which is wrong."),
        ("o8_06", "Here's a nicer way to remember it. From the orbit equation, one over r p is one plus e over p, "
                  "and one over r a is one minus e over p. Their average is one over p. So p is the harmonic mean of "
                  "r p and r a."),
        ("o8_07", "Problem two sixteen. A launch vehicle's guidance fails. At burnout it's at an altitude of two "
                  "hundred fifty kilometers, going seven point seven nine one kilometers per second, with a flight "
                  "path angle of four point five degrees. Has it reached a stable orbit? Our plan: find a and e, "
                  "then check whether the periapsis clears the Earth."),
        ("o8_08", "The radius is six thousand three seventy eight plus two fifty, which is six thousand six hundred "
                  "twenty eight kilometers. The energy is v squared over two, thirty point three five, minus mu over "
                  "r, sixty point one four. That's minus twenty nine point seven nine kilometers squared per second "
                  "squared. Negative, so the orbit is closed. And a equals minus mu over two E, which is six "
                  "thousand six hundred ninety point four kilometers."),
        ("o8_09", "Next, the angular momentum. h equals r v cosine gamma, which is fifty one thousand four hundred "
                  "eighty kilometers squared per second. Then p equals h squared over mu: six thousand six hundred "
                  "forty eight point six kilometers."),
        ("o8_10", "Now e. From p equals a times one minus e squared, e equals the square root of one minus p over a. "
                  "That's zero point zero seven nine zero."),
        ("o8_11", "The periapsis radius is a times one minus e: six thousand one hundred sixty one point eight "
                  "kilometers. But the Earth's radius is six thousand three seventy eight. The periapsis is about two "
                  "hundred sixteen kilometers underground! The vehicle will hit the atmosphere and the Earth long "
                  "before it gets there. So no, it's not a stable orbit. Negative energy alone isn't enough. The "
                  "periapsis must also clear the planet."),
        ("o8_12", "Problem two seventeen. Satellite A is in a circular orbit at eight hundred kilometers altitude. "
                  "Satellite B is on an ellipse with the same eight hundred kilometer perigee, and it's passing "
                  "through perigee right now. A is sixty degrees behind it. We want B's apogee altitude, so that the "
                  "two meet when B comes back to perigee after one revolution."),
        ("o8_13", "Think before calculating. B's orbit is bigger than A's, so B has the longer period. In the time "
                  "B takes to go around once, A must cover the sixty degrees it's behind, plus a full lap. That's "
                  "four hundred twenty degrees. So B's period must be four twenty over three sixty, or seven sixths, "
                  "of A's period."),
        ("o8_14", "A's radius is seven thousand one hundred seventy eight kilometers. Its period, two pi root r cubed "
                  "over mu, is six thousand fifty two seconds, about a hundred and one minutes. So B's period is "
                  "seven sixths of that: seven thousand sixty one seconds."),
        ("o8_15", "Solve the period formula for a: a equals mu times T over two pi squared, all to the one third. "
                  "That's seven thousand nine hundred fifty five kilometers. Or, faster: a scales as T to the two "
                  "thirds, so a is seven thousand one seventy eight times seven sixths to the two thirds. Same "
                  "answer."),
        ("o8_16", "The apogee radius is two a minus r p, which is eight thousand seven hundred thirty two kilometers. "
                  "Subtract the Earth's radius: the apogee altitude is about two thousand three hundred fifty four "
                  "kilometers."),
        ("o8_17", "Problem two twenty eight. The Chandra X-ray Observatory used two transfer orbits. Both have a "
                  "perigee altitude of three hundred kilometers. Their apogee altitudes are thirteen thousand two "
                  "hundred, and seventy two thousand kilometers. We want each orbit's eccentricity and period."),
        ("o8_18", "Here's the recipe. Convert altitudes to radii. a is the average of r p and r a. For e, note that r "
                  "a minus r p is two a e, and r a plus r p is two a. So e equals r a minus r p, over r a plus r p. "
                  "Then the period is two pi root a cubed over mu."),
        ("o8_19", "Transfer orbit one. r p is six thousand six seventy eight, and r a is nineteen thousand five "
                  "seventy eight kilometers. So a is thirteen thousand one twenty eight, e is zero point four nine one "
                  "three, and the period is about fourteen thousand nine hundred seventy seconds, or four point one "
                  "six hours."),
        ("o8_20", "Transfer orbit two. r a is seventy eight thousand three seventy eight kilometers. So a is forty "
                  "two thousand five twenty eight, e is zero point eight four three zero, and the period is about "
                  "eighty seven thousand three hundred seconds. That's twenty four point two four hours, about one "
                  "day."),
        ("o8_21", "Problem two thirty two. Lunar Orbiter one, the first U S spacecraft to orbit the Moon. Its "
                  "angular momentum was three thousand five hundred nine point eight kilometers squared per second, "
                  "and its energy was minus zero point eight eight six six four one. For the Moon, mu is four "
                  "thousand nine hundred two point eight, and the radius is one thousand seven hundred thirty seven "
                  "point five kilometers."),
        ("o8_22", "Energy gives a: minus mu over two E, which is two thousand seven hundred sixty four point eight "
                  "kilometers. Angular momentum gives p: h squared over mu, which is two thousand five hundred twelve "
                  "point six. And e is the square root of one minus p over a: zero point three zero two."),
        ("o8_23", "Perilune radius: a times one minus e, one thousand nine hundred twenty nine point seven. That's an "
                  "altitude of one hundred ninety two kilometers. Apolune radius: a times one plus e, three thousand "
                  "five hundred ninety nine point nine, an altitude of one thousand eight hundred sixty two "
                  "kilometers."),
        ("o8_24", "Speeds at the apsides come from h equals r v. At perilune, v is h over r p: one point eight one "
                  "nine kilometers per second. At apolune, h over r a: zero point nine seven five kilometers per "
                  "second."),
        ("o8_25", "Velocity components at a true anomaly of two hundred twenty degrees. Mu over h is one point three "
                  "nine seven. v r is mu over h, e sine theta: minus zero point two seven one kilometers per second. "
                  "Negative, because past apolune it's falling back toward the Moon. v theta is mu over h, one plus "
                  "e cosine theta: one point zero seven four kilometers per second."),
        ("o8_26", "Finally the period: two pi root a cubed over mu. That's about thirteen thousand forty five "
                  "seconds, or two hundred seventeen minutes. Recap: from any two of the numbers r, v, gamma, h, E, "
                  "a, e, and p, you can find the rest. Energy gives a. Angular momentum gives p. And together they "
                  "give e."),
    ],

    # ------------------------------------------------- 9: examples, open trajectories
    "O9Examples": [
        ("o9_01", "Now the open trajectories. We'll work textbook problems two nineteen and two twenty, which are "
                  "parabolas, and then two twenty one, two twenty two, and two forty two, which are hyperbolas."),
        ("o9_02", "Problem two nineteen. A satellite on a parabolic trajectory is four thousand kilometers above the "
                  "Earth, with a flight path angle of twenty five degrees. Find its speed and true anomaly. The radius "
                  "is ten thousand three hundred seventy eight kilometers."),
        ("o9_03", "On a parabola, the speed is always the local escape speed: the square root of two mu over r. "
                  "That's eight point seven six five kilometers per second. And on a parabola, gamma equals theta "
                  "over two. So the true anomaly is fifty degrees. Gamma is positive, so the satellite is moving "
                  "away, which matches theta between zero and a hundred eighty."),
        ("o9_04", "As a bonus check, p equals r times one plus cosine theta: about seventeen thousand forty nine "
                  "kilometers. So the perigee radius, p over two, is eight thousand five hundred twenty four. That's "
                  "comfortably above the Earth."),
        ("o9_05", "Problem two twenty. A satellite is approaching Earth on a parabola at five point four two three "
                  "kilometers per second. The projected perigee altitude is eight hundred kilometers. Find the "
                  "radius, flight path angle, and true anomaly."),
        ("o9_06", "Escape speed works backwards too. v squared equals two mu over r, so r equals two mu over v "
                  "squared. That's twenty seven thousand one hundred seven kilometers."),
        ("o9_07", "For a parabola, r p equals p over two, so p is twice seven thousand one seventy eight, which is "
                  "fourteen thousand three hundred fifty six. The orbit equation gives one plus cosine theta equals p "
                  "over r. So cosine theta is minus zero point four seven zero four."),
        ("o9_08", "The arccosine gives plus or minus one hundred eighteen point zero six degrees. The satellite is "
                  "approaching, so we take the negative one: minus one hundred eighteen point zero six degrees, which "
                  "is the same as two hundred forty one point nine four. And gamma equals theta over two: minus fifty "
                  "nine point zero three degrees. Diving in steeply."),
        ("o9_09", "Problem two twenty one. A spacecraft leaves low Earth orbit. At engine cutoff it's at two hundred "
                  "kilometers altitude, going eleven point eight one four kilometers per second, with zero flight "
                  "path angle. Zero flight path angle means this point is the periapsis. So r p is six thousand five "
                  "hundred seventy eight kilometers."),
        ("o9_10", "Part a, the eccentricity. h equals r p v p: seventy seven thousand seven hundred twelve. Then p "
                  "equals h squared over mu: fifteen thousand one hundred fifty one. Since r p equals p over one plus "
                  "e, e equals p over r p minus one: one point three zero three three. Greater than one: a "
                  "hyperbola."),
        ("o9_11", "Part b, the speed at four hundred thousand kilometers. The energy is v squared over two minus mu "
                  "over r: sixty nine point seven nine minus sixty point six zero, which is nine point one eight nine. "
                  "Then at the new radius, v equals the square root of two times E plus mu over r. That's four point "
                  "five one four kilometers per second."),
        ("o9_12", "Part c, the flight path angle. h equals r v cosine gamma, so cosine gamma is h over r v: zero "
                  "point zero four three. Gamma is eighty seven point five three degrees, positive because it's "
                  "leaving. It's moving almost straight away from the Earth."),
        ("o9_13", "Part d, the true anomaly. Cosine theta equals p over r minus one, all over e: minus zero point "
                  "seven three eight. Theta is one hundred thirty seven point five eight degrees. Compare with the "
                  "asymptote, theta infinity, the arccosine of minus one over e: one hundred forty point one one. "
                  "We're getting close to it, as we should, far from Earth."),
        ("o9_14", "Part e, the hyperbolic excess speed. E equals v infinity squared over two, so v infinity is the "
                  "square root of two E: four point two eight seven kilometers per second. Notice the speed at four "
                  "hundred thousand kilometers is only a little higher."),
        ("o9_15", "Problem two twenty two. A departure hyperbola has e equals one point four, and a equals minus "
                  "sixteen thousand nine hundred kilometers. Part a: the perigee radius is a times one minus e. Minus "
                  "sixteen thousand nine hundred, times minus zero point four, is six thousand seven hundred sixty. "
                  "So the perigee altitude is three hundred eighty two kilometers."),
        ("o9_16", "Part b, velocity components at theta equals one hundred degrees. p equals a times one minus e "
                  "squared: sixteen thousand two hundred twenty four. h is the square root of mu p, and mu over h is "
                  "four point nine five seven. So v r, mu over h e sine theta, is six point eight three four. And v "
                  "theta, mu over h one plus e cosine theta, is three point seven five two kilometers per second."),
        ("o9_17", "Part c, the asymptote's true anomaly: the arccosine of minus one over one point four, which is one "
                  "hundred thirty five point five eight degrees. Part d, the turning angle: two times the arcsine of "
                  "one over e, which is ninety one point one seven degrees. Check: two theta infinity minus one "
                  "eighty gives the same."),
        ("o9_18", "Problem two forty two. The Juno spacecraft approached Jupiter on a hyperbola with e equals one "
                  "point zero one seven two, and a equals minus four point three eight four million kilometers. "
                  "Jupiter's mu is one point two six seven times ten to the eighth."),
        ("o9_19", "The approach speed is v infinity, the square root of minus mu over a. That's five point three "
                  "seven six kilometers per second. The closest approach is a times one minus e: about seventy five "
                  "thousand four hundred kilometers. Jupiter's radius is seventy one thousand four hundred ninety two, "
                  "so Juno skimmed only about four thousand kilometers above the clouds."),
        ("o9_20", "Since e is barely above one, the path is almost a parabola, and the turn is a sharp hairpin: two "
                  "arcsine one over e is about one hundred fifty nine degrees. Recap: on open trajectories, the same "
                  "formulas work. On a parabola, use escape speed and gamma equals theta over two. On a hyperbola, "
                  "let a be negative, and use v infinity, theta infinity, and the turning angle."),
    ],

    # ------------------------------------------------- 10: HW 3 P1, the velocity frame
    "O10Problem": [
        ("o10_01", "Homework three, problem one. The velocity frame, V, has axes i n, i v, and i h. The orbit frame, "
                   "O, has i r, i theta, and i h. They differ by one rotation about i h. We need the direction cosine "
                   "matrix C V O as a function of e and f, and then the angular velocity and angular acceleration of "
                   "V relative to the perifocal frame."),
        ("o10_02", "Read the figure. i v points along the velocity. i theta is the local horizontal. So the angle "
                   "between them, beta, is exactly the flight path angle from our velocity lesson. Since both frames "
                   "are right handed and share i h, the same angle beta sits between i r and i n."),
        ("o10_03", "Which way does it tilt? While the satellite is climbing, the velocity tips from i theta toward i "
                   "r. So i v equals sine beta i r, plus cosine beta i theta. And i n is perpendicular to i v in the "
                   "plane, with i n cross i v equal to i h. That gives i n equals cosine beta i r, minus sine beta i "
                   "theta."),
        ("o10_04", "Check it: i n cross i v gives cosine squared beta, plus sine squared beta, times i r cross i "
                   "theta. That's one times i h. Good."),
        ("o10_05", "The rows of C V O are the V axes written in O components. So the first row is cosine beta, minus "
                   "sine beta, zero. The second row is sine beta, cosine beta, zero. And the third row is zero, zero, "
                   "one. This is C three of minus beta: a rotation about i h by minus beta."),
        ("o10_06", "Now write beta in terms of e and f. From the velocity lesson, tangent beta equals v r over v "
                   "theta, which is e sine f over one plus e cosine f. Draw a right triangle with those two sides."),
        ("o10_07", "The hypotenuse squared is one plus e cosine f, squared, plus e squared sine squared f. Expand: one, "
                   "plus two e cosine f, plus e squared cosine squared f, plus e squared sine squared f. The last two "
                   "combine to e squared. Call the square root of one plus two e cosine f plus e squared, k."),
        ("o10_08", "So sine beta is e sine f over k, and cosine beta is one plus e cosine f, over k. Put these into "
                   "the matrix. That's C V O as a function of e and f. Check: with e equals zero, k is one, and the "
                   "matrix is the identity. On a circle, the velocity is always horizontal. Good."),
        ("o10_09", "Now the angular velocity of V relative to the perifocal frame, P. Use the addition rule: omega V "
                   "P equals omega V O plus omega O P. The orbit frame turns relative to P through the true anomaly, "
                   "so omega O P is f dot i h. And V is O rotated by minus beta, so omega V O is minus beta dot i h."),
        ("o10_10", "So omega V P equals f dot minus beta dot, along i h. In the picture: i n sits at the angle f minus "
                   "beta from p hat. Its turning rate is f dot minus beta dot."),
        ("o10_11", "We need beta dot. Differentiate tangent beta equals e sine f over one plus e cosine f, with "
                   "respect to time. The left side gives secant squared beta, times beta dot. The right side uses the "
                   "quotient rule, times f dot."),
        ("o10_12", "The quotient rule gives: e cosine f, times one plus e cosine f, minus e sine f, times minus e sine "
                   "f, over one plus e cosine f squared. The top simplifies to e cosine f plus e squared. So the "
                   "right side is e times e plus cosine f, over one plus e cosine f squared, times f dot."),
        ("o10_13", "Secant squared beta is one over cosine squared beta, which is k squared over one plus e cosine f "
                   "squared. Divide both sides by it. The one plus e cosine f squared cancels, and beta dot equals e "
                   "times e plus cosine f, over k squared, times f dot."),
        ("o10_14", "Now f dot minus beta dot is f dot times one minus e times e plus cosine f over k squared. Over a "
                   "common denominator, the top is k squared minus e squared minus e cosine f, which is one plus e "
                   "cosine f. So omega equals f dot, times one plus e cosine f, over k squared."),
        ("o10_15", "Finally, f dot is the square root of mu over p cubed, times one plus e cosine f squared. So omega V "
                   "P equals the square root of mu over p cubed, times one plus e cosine f cubed, over one plus two e "
                   "cosine f plus e squared, along i h. The square root factor is a constant of the orbit."),
        ("o10_16", "Check: on a circle, e is zero, and omega is the square root of mu over r cubed. That's the mean "
                   "motion. The velocity turns exactly as fast as the satellite goes around. Good."),
        ("o10_17", "Now the angular acceleration. i h is fixed in both frames, so we only need the time derivative of "
                   "the magnitude. By the chain rule, it's d omega by d f, times f dot. Call the fraction g of f. Use "
                   "the quotient rule on g."),
        ("o10_18", "The top of the quotient rule is three times one plus e cosine f squared, times minus e sine f, "
                   "times k squared, minus one plus e cosine f cubed, times minus two e sine f. Factor out minus e "
                   "sine f, times one plus e cosine f squared."),
        ("o10_19", "Inside the brackets is three k squared, minus two times one plus e cosine f. That's three plus "
                   "six e cosine f plus three e squared, minus two, minus two e cosine f. Which is one plus four e "
                   "cosine f plus three e squared."),
        ("o10_20", "Multiply by the square root of mu over p cubed, and by f dot. The angular acceleration of V "
                   "relative to P is minus mu over p cubed, times e sine f, times one plus e cosine f to the fourth, "
                   "times one plus four e cosine f plus three e squared, all over k to the fourth, along i h."),
        ("o10_21", "Checks. On a circle, e is zero, and the angular acceleration is zero: steady turning. At "
                   "periapsis and apoapsis, sine f is zero, so it's zero there too. Here are both curves for e equals "
                   "one half."),
        ("o10_22", "Recap. The velocity frame is the orbit frame rotated by minus the flight path angle. Angular "
                   "velocities add: f dot minus beta dot. And because the axis i h never moves, the angular "
                   "acceleration is just the derivative of that one number."),
    ],

    # ------------------------------------------------- 11: HW 3 P2, time on an orbit
    "O11Problem": [
        ("o11_01", "Homework three, problem two. A space probe orbits the Sun, with perihelion at zero point five A "
                   "U and aphelion at two point five A U. How much of each orbit does it spend closer than one A U to "
                   "the Sun? This needs one new tool: connecting position to time."),
        ("o11_02", "First the orbit. a is the average of the two: one point five A U. e is r a minus r p, over r a "
                   "plus r p: two over three. And p is a times one minus e squared: one point five times five ninths, "
                   "which is five sixths of an A U."),
        ("o11_03", "Where does it cross one A U? Set r equal to one in the orbit equation. One plus two thirds "
                   "cosine theta equals five sixths. So cosine theta equals minus one quarter, and theta is plus or "
                   "minus one hundred four point four eight degrees. Inside one A U is the arc around perihelion, "
                   "between those two angles."),
        ("o11_04", "It's tempting to say the fraction of time is two hundred nine over three sixty. But that's wrong. "
                   "By Kepler's second law, time is proportional to swept area, not to angle. And near perihelion the "
                   "probe moves fast. We need this shaded area."),
        ("o11_05", "That area, a slice of an ellipse measured from a focus, is awkward to integrate directly. "
                   "Kepler's trick: draw a circle of radius a around the ellipse's center. This is the auxiliary "
                   "circle. The ellipse is just this circle, squashed vertically by the factor b over a."),
        ("o11_06", "Take the probe at P. Go straight up, perpendicular to the major axis, to the point Q on the circle. "
                   "The angle at the center, from the periapsis direction to Q, is called the eccentric anomaly, E. Q "
                   "has coordinates a cosine E, a sine E. Squashing gives P: a cosine E, b sine E."),
        ("o11_07", "The focus is a distance a e from the center. So from the focus, P is at a times cosine E minus e, "
                   "and b sine E. Then r squared is a squared, cosine E minus e squared, plus a squared one minus e "
                   "squared, sine squared E."),
        ("o11_08", "Expand and use sine squared plus cosine squared equals one. Everything collapses to a squared, "
                   "times one minus e cosine E, squared. So r equals a times one minus e cosine E. A very handy "
                   "formula."),
        ("o11_09", "Comparing the horizontal coordinates, r cosine theta equals a times cosine E minus e. Divide by r, "
                   "and solve for cosine E. You get cosine E equals e plus cosine theta, over one plus e cosine "
                   "theta. This converts true anomaly to eccentric anomaly."),
        ("o11_10", "Now the area. The region of the ellipse swept from the focus, between periapsis and P, is the "
                   "squashed version of the region of the circle between periapsis and Q, seen from the same focus. "
                   "Squashing multiplies every area by b over a."),
        ("o11_11", "The circle region is easy. It's a pie slice from the center, with area one half a squared E, minus "
                   "a triangle. The triangle has base a e and height a sine E, so its area is one half a squared e "
                   "sine E. So the circle region is a squared over two, times E minus e sine E."),
        ("o11_12", "Multiply by b over a. The swept area of the ellipse is a b over two, times E minus e sine E."),
        ("o11_13", "The area sweeps at a constant rate, and the whole ellipse, pi a b, takes one period. So the time "
                   "since periapsis is that area over pi a b, times T. The a b cancels, and t minus t p equals T over "
                   "two pi, times E minus e sine E."),
        ("o11_14", "Define the mean anomaly, M, as two pi over T, times t minus t p. That's n times t minus t p. It's "
                   "an angle that grows perfectly steadily. Then we get Kepler's equation: M equals E minus e sine E."),
        ("o11_15", "So from a position, finding the time is straightforward: theta, then E, then M, then t. Going the "
                   "other way, from time to position, needs an iterative solution, which we'll see later in the "
                   "course."),
        ("o11_16", "Back to the probe. At one A U, use r equals a times one minus e cosine E. One equals one point "
                   "five, times one minus two thirds cosine E. So cosine E is one half, and E is sixty degrees, or pi "
                   "over three. Check with the other formula: two thirds minus one quarter, over one minus one sixth. "
                   "That's five twelfths over five sixths, which is one half. It matches."),
        ("o11_17", "The mean anomaly is E minus e sine E: pi over three, minus two thirds times root three over two. "
                   "That's one point zero four seven two minus zero point five seven seven four, which is zero point "
                   "four six nine eight radians."),
        ("o11_18", "By symmetry, the probe is inside one A U from minus M to plus M. That's two M out of two pi, so "
                   "the fraction of the period is M over pi: zero point one four nine six. Only about fifteen percent "
                   "of the time, even though it covers fifty eight percent of the angle."),
        ("o11_19", "Now the period. Kepler's third law in solar units is easy: one A U gives one year, so T equals a "
                   "to the three halves, in years. One point five to the three halves is one point eight three seven "
                   "years, or six hundred seventy one days. Using the Sun's mu in kilometers gives the same thing."),
        ("o11_20", "So the time inside one A U is zero point one four nine six times six hundred seventy one days. "
                   "That's about one hundred days, or zero point two seven five years, on every orbit."),
        ("o11_21", "Recap. Time is proportional to swept area. The auxiliary circle turns that area into a triangle "
                   "and a pie slice. The result is Kepler's equation, M equals E minus e sine E, with r equal to a "
                   "times one minus e cosine E."),
    ],

    # ------------------------------------------------- 12: HW 3 P4, orbital elements
    "O12Problem": [
        ("o12_01", "So far, everything has lived inside the orbit plane. But that plane is tilted in space. Homework "
                   "problem four gives us two position vectors in an Earth centered inertial frame, and asks for all "
                   "the orbital elements. First, let's define them."),
        ("o12_02", "The geocentric equatorial frame has n one in the equatorial plane, pointing toward the vernal "
                   "equinox. n three points through the North Pole. And n two completes the right handed set. The "
                   "frame doesn't rotate. The Earth spins inside it."),
        ("o12_03", "The orbit plane cuts the equatorial plane along a line, called the line of nodes. The ascending "
                   "node is where the satellite crosses the equator heading north. The node vector, n three cross h, "
                   "points to it."),
        ("o12_04", "There are six classical orbital elements. a and e give the size and shape. The inclination, i, is "
                   "the angle between n three and h: the tilt of the plane. The right ascension of the ascending node, "
                   "capital Omega, is the angle in the equator, from n one to the node."),
        ("o12_05", "The argument of periapsis, little omega, is the angle in the orbit plane, from the node to "
                   "periapsis. And the true anomaly, f, goes from periapsis to the satellite. The angle from the node "
                   "all the way to the satellite, omega plus f, is called the argument of latitude, u."),
        ("o12_06", "Notice that capital Omega, i, and little omega are a three one three Euler angle sequence. Rotate "
                   "about n three by capital Omega, then about the node line by i, then about h by little omega. That "
                   "lands exactly on the perifocal frame. So C P N equals C three of omega, times C one of i, times C "
                   "three of capital Omega."),
        ("o12_07", "To compute the angles: cosine i is h three over h, which always gives an angle between zero and a "
                   "hundred eighty. Capital Omega comes from the node vector's components. And for angles measured "
                   "from the node, like u, the arccosine needs a quadrant check: if the point is below the equator, "
                   "take three sixty minus the angle."),
        ("o12_08", "Now the problem. r one is fourteen thousand four fifty point six, minus one thousand five twenty "
                   "nine point nine, minus six thousand five twenty four kilometers. r two is minus six thousand one "
                   "ninety nine point five, fourteen thousand six ninety nine point two, eight thousand five thirty one "
                   "point nine. And p is two point eight eight Earth radii: eighteen thousand three hundred sixty nine "
                   "kilometers."),
        ("o12_09", "The key idea: both positions lie in the orbit plane, so their cross product points along h. We "
                   "assume the satellite travels from r one to r two the short way, through less than a hundred eighty "
                   "degrees. Normalizing r one cross r two gives h hat: zero point three five three six, minus zero "
                   "point three five three six, zero point eight six six zero."),
        ("o12_10", "The inclination is the arccosine of zero point eight six six zero. That's the cosine of thirty "
                   "degrees, so i equals thirty degrees."),
        ("o12_11", "The node vector, n three cross h hat, has components minus h two, h one, zero. That's zero point "
                   "three five three six, zero point three five three six, zero. Both components are positive, so "
                   "it's in the first quadrant: capital Omega equals forty five degrees."),
        ("o12_12", "Now work inside the plane. The angle between r one and r two comes from the dot product. The "
                   "magnitudes are fifteen thousand nine twenty nine, and eighteen thousand ninety one kilometers. "
                   "Cosine delta f is minus zero point five eight two one, so delta f is one hundred twenty five point "
                   "six zero degrees. That means f two equals f one plus one twenty five point six."),
        ("o12_13", "Apply the orbit equation at both points. e cosine f one equals p over r one minus one: zero point "
                   "one five three two. And e cosine of f one plus delta f equals p over r two minus one: zero point "
                   "zero one five four. Two equations, two unknowns, e and f one."),
        ("o12_14", "Expand the cosine of the sum. e cosine f one, cosine delta f, minus e sine f one, sine delta f, "
                   "equals zero point zero one five four. We already know e cosine f one, so we can solve for e sine f "
                   "one. It's minus zero point one two eight six."),
        ("o12_15", "Now e is the square root of the sum of the squares: zero point two. And f one is the angle whose "
                   "cosine part is positive and sine part is negative: minus forty degrees, or three hundred twenty "
                   "degrees. Then f two is three twenty plus one twenty five point six, which wraps around to eighty "
                   "five point six degrees."),
        ("o12_16", "The semi major axis is p over one minus e squared: eighteen thousand three sixty nine over zero "
                   "point nine six. That's nineteen thousand one hundred thirty four kilometers, which is exactly "
                   "three Earth radii."),
        ("o12_17", "Last, little omega. Find the argument of latitude of r one: the angle from the node to r one. Its "
                   "cosine is zero point five seven three six, which is fifty five degrees. But r one is below the "
                   "equator, so u one is three sixty minus fifty five: three hundred five degrees. Then omega equals u "
                   "one minus f one: three oh five minus three twenty, which is minus fifteen, or three hundred forty "
                   "five degrees."),
        ("o12_18", "Check with r two. It's above the equator, and u two is seventy point six degrees. Omega is seventy "
                   "point six minus eighty five point six: again minus fifteen, so three forty five. Both points agree."),
        ("o12_19", "Ascending or descending? At f one, three hundred twenty degrees, the true anomaly is between one "
                   "eighty and three sixty, so the flight path angle is negative. The satellite is heading down toward "
                   "perigee: descending. At f two, eighty five point six degrees, gamma is positive: it's climbing "
                   "toward apogee, ascending. In terms of latitude, both points happen to be northbound."),
        ("o12_20", "Here's the full answer: a is three Earth radii, e is zero point two, i is thirty degrees, capital "
                   "Omega is forty five, little omega is three forty five, f one is three twenty, and f two is eighty "
                   "five point six. And with that, we've gone from Kepler's three laws all the way to a full orbit in "
                   "three dimensions. Thanks for watching."),
    ],
}

SCENE_ORDER = list(SCRIPT.keys())


def all_segments():
    for scene in SCENE_ORDER:
        for seg_id, text in SCRIPT[scene]:
            yield scene, seg_id, text
