"""Narration for the slow, step-by-step lesson series (6 videos).

Each video has a Concept scene and an Examples scene. Segment ids are
v<video>_<nn>; scene names are V<video>Concept / V<video>Examples.
"""

STYLE = (
    "Speak slowly and patiently, like a friendly tutor guiding a student who is "
    "seeing this for the first time: warm, clear and unhurried, with a natural "
    "pause between sentences and a slightly longer pause after each step."
)

SCRIPT = {
    # ------------------------------------------------------------------ V1
    "V1Concept": [
        ("v1_01", "Welcome to the first lesson in this series on spacecraft kinematics. We're going to go slowly, "
                  "and we won't skip any steps. By the end of this video, you'll know exactly what a reference "
                  "frame is, and how to turn an arrow into three numbers, and back again."),
        ("v1_02", "Let's begin with a vector. A vector is an arrow. It has a length, called its magnitude, and it "
                  "points in a direction. We'll call this one r. Here's the key idea for everything that follows: "
                  "the arrow exists on its own. It doesn't care how we choose to describe it."),
        ("v1_03", "We need two tools for working with arrows. The first is the dot product. Take two vectors, a and "
                  "b, with an angle theta between them. Their dot product is the length of a, times the length of "
                  "b, times the cosine of theta."),
        ("v1_04", "Here's what that means in a picture. Drop a perpendicular from the tip of a down onto b. The "
                  "piece of a that lies along b has length: the length of a, times cosine theta. That's the shadow "
                  "of a on b. The dot product is that shadow, multiplied by the length of b."),
        ("v1_05", "This becomes especially simple when b is a unit vector, meaning its length is exactly one. Then a "
                  "dot b is just the shadow of a along b. Keep this in mind, because it's how we'll find components "
                  "in a moment."),
        ("v1_06", "Two special cases are worth remembering. If two vectors are perpendicular, theta is ninety "
                  "degrees, the cosine is zero, so their dot product is zero. And any unit vector dotted with itself "
                  "gives one, because the angle is zero and both lengths are one."),
        ("v1_07", "The second tool is the cross product. a cross b is a new vector. Its length is the length of a, "
                  "times the length of b, times the sine of theta. That's exactly the area of the parallelogram the "
                  "two vectors span."),
        ("v1_08", "Its direction is perpendicular to both a and b, and we pick which way using the right hand rule. "
                  "Point your fingers along a, curl them toward b, and your thumb points along a cross b. Notice "
                  "that order matters: b cross a points the opposite way."),
        ("v1_09", "Now, a reference frame. A frame is an origin, O, plus three unit vectors. We'll call them n hat "
                  "one, n hat two, and n hat three, and together they form frame N."),
        ("v1_10", "These three vectors must follow three rules. First, each has length one, so n i dot n i equals "
                  "one. Second, they're mutually perpendicular, so n i dot n j equals zero whenever i and j are "
                  "different. And third, they're right handed: n one cross n two equals n three. Cycling the "
                  "indices, n two cross n three is n one, and n three cross n one is n two."),
        ("v1_11", "Now let's describe our arrow using frame N. We claim r can be written as some amount x along n "
                  "one, plus some amount y along n two, plus some amount z along n three. The question is: how do "
                  "we find x, y, and z?"),
        ("v1_12", "Here's the trick. Take the dot product of both sides with n one. On the left, we get r dot n one. "
                  "On the right, the dot product distributes over each term."),
        ("v1_13", "Now use the rules. n one dot n one is one. n two dot n one is zero. And n three dot n one is "
                  "zero. Two of the three terms vanish, and we're left with x equals r dot n one."),
        ("v1_14", "Exactly the same steps give y equals r dot n two, and z equals r dot n three. Each component is "
                  "just the shadow of r on one of the axes. That's the whole idea of components."),
        ("v1_15", "We collect the three numbers into a column, and call it r with a subscript N in parentheses: r "
                  "expressed in frame N. Be careful with this notation. The arrow, r, is the vector. The column of "
                  "numbers is only one description of it, tied to one particular frame."),
        ("v1_16", "Once we have columns, dot products become easy. Write out a dot b with both vectors in "
                  "components, and expand. Every cross term involves two different unit vectors, so it's zero. "
                  "Only the matching terms survive: a one b one, plus a two b two, plus a three b three. In matrix "
                  "form, that's a transpose times b."),
        ("v1_17", "The cross product has a component formula too. It's often written as a determinant, with the "
                  "unit vectors in the top row, the components of a in the middle row, and the components of b in "
                  "the bottom row. Expanding it gives these three components."),
        ("v1_18", "And there's a matrix form. We build a special matrix from the components of a, called a tilde. "
                  "It has zeros on the diagonal, and the entries of a arranged with alternating signs. Multiplying "
                  "a tilde by the column for b gives exactly the column for a cross b."),
    ],
    "V1Examples": [
        ("v1_19", "Let's practice. Example one. A vector has components three, four, and zero in frame N. How long "
                  "is it, and what angle does it make with n one?"),
        ("v1_20", "For the length, dot r with itself: three squared plus four squared plus zero squared is twenty "
                  "five, and the square root of twenty five is five."),
        ("v1_21", "For the angle, use the definition of the dot product. r dot n one equals the length of r, times "
                  "the length of n one, times cosine of the angle. The left side is just the first component, "
                  "three. The right side is five, times one, times cosine alpha. So cosine alpha is three fifths, "
                  "and alpha is about fifty three point one degrees."),
        ("v1_22", "Example two. Take a equals one, two, zero, and b equals zero, one, three, both in frame N. First, "
                  "the dot product: one times zero, plus two times one, plus zero times three. That's two."),
        ("v1_23", "Now the cross product. First component: a two b three minus a three b two, which is two times "
                  "three minus zero times one, so six. Second component: a three b one minus a one b three, which "
                  "is zero minus three, so minus three. Third component: a one b two minus a two b one, which is "
                  "one minus zero, so one."),
        ("v1_24", "Always check your answer. a cross b should be perpendicular to both a and b. Dot it with a: six "
                  "minus six plus zero is zero. Dot it with b: zero minus three plus three is zero. Both checks "
                  "pass."),
        ("v1_25", "Example three. Same arrow, two frames. Here's frame B, rotated relative to N. The arrow doesn't "
                  "move, but its shadows on the B axes are different, so r in B is a different column of numbers. "
                  "In the next lesson, we'll learn exactly how to get from one column to the other. That tool is "
                  "the direction cosine matrix."),
        ("v1_26", "Let's recap. A vector is an arrow. A frame is an origin and three perpendicular, right handed "
                  "unit vectors. Each component is a dot product with an axis. And the column of components always "
                  "depends on which frame you chose."),
    ],
    # ------------------------------------------------------------------ V2
    "V2Concept": [
        ("v2_01", "In the last lesson, we saw that the same arrow has different components in different frames. In "
                  "this lesson, we'll build the tool that converts between them: the direction cosine matrix, or "
                  "D C M. We'll go one entry at a time."),
        ("v2_02", "Here are two frames sharing the same origin: N in grey, and B in blue. Remember, each b hat is "
                  "itself a vector. So we can write it in N components, using exactly the rule from the last "
                  "lesson."),
        ("v2_03", "b one equals b one dot n one, times n one, plus b one dot n two, times n two, plus b one dot n "
                  "three, times n three. Each coefficient is the shadow of b one on one of the N axes."),
        ("v2_04", "We do the same for b two and b three. That gives three equations, with nine dot products in "
                  "total."),
        ("v2_05", "Three equations like this can be written as a single matrix equation. The column of B vectors "
                  "equals a three by three matrix of dot products, times the column of N vectors. This matrix is "
                  "the direction cosine matrix, C B N."),
        ("v2_06", "Why that name? Each entry, row i, column j, is b i dot n j. Both are unit vectors, so this is "
                  "just the cosine of the angle between axis b i and axis n j. Nine direction cosines."),
        ("v2_07", "Let's compute one completely. Frame B starts lined up with N, then rotates by angle theta about "
                  "n three. So b three stays equal to n three."),
        ("v2_08", "Row one is b one. The angle between b one and n one is theta, so the first entry is cosine "
                  "theta. The angle between b one and n two is ninety minus theta, and cosine of ninety minus theta "
                  "is sine theta. And b one is perpendicular to n three, giving zero."),
        ("v2_09", "Row two is b two. b two has turned past n two by theta, so its angle with n one is ninety plus "
                  "theta. The cosine of ninety plus theta is minus sine theta. Its angle with n two is theta, "
                  "giving cosine theta. And again, zero for n three."),
        ("v2_10", "Row three is b three, which equals n three. So the entries are zero, zero, and one."),
        ("v2_11", "Putting it together, the D C M is cosine theta, sine theta, zero; minus sine theta, cosine "
                  "theta, zero; and zero, zero, one. We call this C three of theta: a rotation about the third "
                  "axis."),
        ("v2_12", "Now the most important use: converting a vector's components. Suppose we know r in N components, "
                  "and we want r in B. Start with what a B component is: the first B component is r dot b one."),
        ("v2_13", "Now write r in N components, and substitute. r dot b one becomes b one dot the sum of r j n j."),
        ("v2_14", "The dot product distributes over the sum, and each r j is just a number, so it pulls out. We get "
                  "the sum over j of b one dot n j, times r j."),
        ("v2_15", "But b one dot n j is exactly C one j, an entry of the D C M. So the first B component is row one "
                  "of C, times the column r in N."),
        ("v2_16", "The same is true for every row. So r in B equals C B N times r in N. That's the conversion "
                  "formula, and now you've seen every step of where it comes from."),
        ("v2_17", "Next, a property that will save you a lot of work. Row i of the D C M is b i written in N "
                  "components. So multiplying the D C M by its own transpose takes dot products of rows with rows."),
        ("v2_18", "Entry i k of C times C transpose is row i dotted with row k, which is b i dot b k. That's one "
                  "when i equals k, and zero otherwise. So C times C transpose is the identity matrix."),
        ("v2_19", "That means the inverse of a D C M is just its transpose. To go backwards, from B to N, use C N "
                  "B, which equals C B N transpose. No matrix inversion needed."),
        ("v2_20", "Two more facts. The columns of C are the N axes written in B components. And for right handed "
                  "frames, the determinant of C is plus one. A D C M with determinant minus one would describe a "
                  "mirror image, which isn't a real rotation."),
        ("v2_21", "Finally, notice that the nine entries aren't independent. The rows must be unit vectors: three "
                  "equations. And they must be mutually perpendicular: three more. Nine numbers, minus six "
                  "constraints, leaves three. That's why orientation needs exactly three numbers, like the three "
                  "Euler angles in the next lesson."),
    ],
    "V2Examples": [
        ("v2_22", "Example one: converting a vector. Frame B is rotated thirty degrees about n three, and r in N is "
                  "two, one, zero. Find r in B."),
        ("v2_23", "First, the D C M. Cosine thirty is about zero point eight six six, and sine thirty is zero point "
                  "five. So C B N is zero point eight six six, zero point five, zero; minus zero point five, zero "
                  "point eight six six, zero; zero, zero, one."),
        ("v2_24", "Now multiply, one row at a time. Row one times the column: zero point eight six six times two, "
                  "plus zero point five times one, plus zero. That's two point two three two."),
        ("v2_25", "Row two: minus zero point five times two, plus zero point eight six six times one. That's minus "
                  "zero point one three four. Row three gives zero."),
        ("v2_26", "Check: the length must not change, because rotating the frame doesn't stretch the arrow. In N, "
                  "the length is the square root of five, about two point two three six. In B, the square root of "
                  "two point two three two squared plus zero point one three four squared is also about two point "
                  "two three six. It checks out."),
        ("v2_27", "Example two: rebuilding a D C M from partial data. A satellite sends down only some entries of "
                  "its D C M. The first row is complete. The second row is missing its first entry, a. And the "
                  "third row is missing its first two entries, b and c. Let's recover them."),
        ("v2_28", "Start with row two. It must be a unit vector, so a squared, plus zero point eight eight two six "
                  "squared, plus zero point one six three two squared, equals one. Solving, a is plus or minus zero "
                  "point four four one."),
        ("v2_29", "To pick the sign, use orthogonality: row one dot row two must be zero. With a positive, the dot "
                  "product comes out to about zero point seven two, which is not zero. With a negative, it comes "
                  "out to zero. So a equals minus zero point four four one."),
        ("v2_30", "For row three, there's a shortcut. Because the frame is right handed, b three equals b one cross "
                  "b two. So row three is row one cross row two. Computing the cross product gives zero point three "
                  "seven eight five, zero point zero one eight, and zero point nine two five four. So b is zero "
                  "point three seven eight five, and c is zero point zero one eight."),
        ("v2_31", "One more question you might be asked: what's the angle between b one and n two? That's just "
                  "entry one two, the cosine of that angle. The arc cosine of zero point four six nine eight is "
                  "about sixty two degrees."),
        ("v2_32", "Example three: building a frame from vectors. Spacecraft often use a local vertical, local "
                  "horizontal frame, built from position and velocity. t one points along r, t three points along r "
                  "cross v, and t two completes the triad: t three cross t one."),
        ("v2_33", "Let r be seven thousand, zero, zero kilometers, and v be zero, five, five kilometers per second. "
                  "Then t one is simply one, zero, zero."),
        ("v2_34", "r cross v is zero, minus thirty five thousand, thirty five thousand. Dividing by its length gives "
                  "t three equals zero, minus one over root two, one over root two."),
        ("v2_35", "Then t two, which is t three cross t one, is zero, one over root two, one over root two. And "
                  "here's the payoff: the rows of the D C M, C T N, are just these three vectors. Writing them as "
                  "rows gives the D C M directly."),
        ("v2_36", "Example four: a rotating frame. The Earth fixed frame E spins about n three at omega equals seven "
                  "point two nine two one times ten to the minus five radians per second. If the frames line up at "
                  "time zero, then at time t, the angle is omega t, and C E N is C three of omega t."),
        ("v2_37", "After three hours, which is ten thousand eight hundred seconds, the angle is zero point seven "
                  "eight seven five radians, about forty five point one degrees. A star direction of zero point "
                  "six, zero point eight, zero in N becomes zero point nine nine zero, zero point one three nine, "
                  "zero in the Earth frame."),
        ("v2_38", "Recap. The D C M, C B N, is a table of direction cosines. Its rows are the B axes written in N. "
                  "It converts components with r in B equals C B N times r in N. And its inverse is just its "
                  "transpose."),
    ],
    # ------------------------------------------------------------------ V3
    "V3Concept": [
        ("v3_01", "We now know that an orientation is described by a D C M, and that a D C M has only three degrees "
                  "of freedom. In this lesson, we'll describe orientation with three angles instead of nine "
                  "numbers. These are Euler angles."),
        ("v3_02", "The building block is a rotation about a single axis. We already found C three of theta, a "
                  "rotation about the third axis. Let's find the other two, carefully, because their sign patterns "
                  "are easy to mix up."),
        ("v3_03", "Rotation about axis one by angle theta. Axis one doesn't move, so row one is one, zero, zero. "
                  "Looking down axis one, axes two and three turn exactly like axes one and two did before. So row "
                  "two is zero, cosine theta, sine theta, and row three is zero, minus sine theta, cosine theta."),
        ("v3_04", "Rotation about axis two. Axis two doesn't move, so row two is zero, one, zero. Now look down "
                  "axis two. Going counterclockwise, the order is axis three, then axis one. So axis three plays "
                  "the role of the first axis, and axis one plays the role of the second."),
        ("v3_05", "That means b one equals cosine theta n one, minus sine theta n three, and b three equals sine "
                  "theta n one, plus cosine theta n three. So in C two, the minus sign sits in the top right corner "
                  "instead. This is the one people most often get wrong."),
        ("v3_06", "Here's a way to remember all three. The axis you rotate about gets a one on the diagonal and "
                  "zeros in the rest of its row and column. The other four entries hold cosines on the diagonal and "
                  "sines off it. For C one and C three, the minus sign is below the diagonal. For C two, it's "
                  "above."),
        ("v3_07", "Now we chain rotations. Suppose frame P is reached from A by one rotation, so p equals C P A "
                  "times a. Then frame Q is reached from P, so q equals C Q P times p."),
        ("v3_08", "Substitute the first equation into the second: q equals C Q P times C P A times a. So C Q A is "
                  "the product C Q P times C P A. Notice the order: the most recent rotation goes on the left."),
        ("v3_09", "Euler's theorem says any orientation can be reached with three such rotations, each about an "
                  "axis of the newest frame. The classic aerospace choice is three, two, one: yaw, pitch, and roll."),
        ("v3_10", "Step one: rotate by psi about a three. This gives frame P."),
        ("v3_11", "Step two: rotate by theta about the new axis, p two. This gives frame Q."),
        ("v3_12", "Step three: rotate by phi about the newest axis, q one. This gives the body frame, B."),
        ("v3_13", "Chaining them, C B A equals C one of phi, times C two of theta, times C three of psi. Let's "
                  "actually multiply this out, in two steps."),
        ("v3_14", "First, C two of theta times C three of psi. Row one of C two is cosine theta, zero, minus sine "
                  "theta. Multiply it into each column of C three. The first entry is cosine theta cosine psi. The "
                  "second is cosine theta sine psi. The third is minus sine theta."),
        ("v3_15", "Row two of C two is zero, one, zero, which just copies row two of C three: minus sine psi, "
                  "cosine psi, zero. Row three, sine theta, zero, cosine theta, gives sine theta cosine psi, sine "
                  "theta sine psi, and cosine theta."),
        ("v3_16", "Now multiply by C one of phi on the left. Its first row is one, zero, zero, so the first row "
                  "stays the same. Rows two and three mix the middle and bottom rows using cosine phi and sine phi. "
                  "The result is the full three two one D C M."),
        ("v3_17", "Going backwards is the most useful skill. Given a D C M, find the angles. Look at entry one "
                  "three: it's minus sine theta. So theta is minus the arc sine of C one three."),
        ("v3_18", "Next, divide entry one two by entry one one. The cosine theta cancels, leaving sine psi over "
                  "cosine psi, which is tangent psi. So psi is the two argument arc tangent of C one two and C one "
                  "one. Using atan two, instead of plain arc tangent, puts the angle in the correct quadrant."),
        ("v3_19", "In the same way, C two three over C three three is tangent phi. So phi is atan two of C two three "
                  "and C three three."),
        ("v3_20", "But there's a catch. That division only works if cosine theta isn't zero. When theta is ninety "
                  "degrees, cosine theta is zero, and the first row becomes zero, zero, minus one. We can no longer "
                  "find psi or phi separately."),
        ("v3_21", "Here's what's happening physically. At ninety degrees of pitch, the roll axis has swung around "
                  "until it lines up with the original yaw axis. Yaw and roll now spin about the same line, so only "
                  "their difference matters. This is gimbal lock."),
        ("v3_22", "Every Euler angle sequence has such a singularity. Asymmetric sequences, like three two one, lock "
                  "at a middle angle of plus or minus ninety degrees. Symmetric sequences, like three one three, "
                  "lock at zero or one eighty. There are twelve sequences in total, and your appendix lists all of "
                  "them."),
    ],
    "V3Examples": [
        ("v3_23", "Example one. Take psi equals thirty degrees, theta twenty degrees, and phi ten degrees. Plugging "
                  "into the three two one formula gives this D C M. Look closely: it's exactly the matrix we "
                  "reconstructed in the last lesson!"),
        ("v3_24", "Now let's run it backwards, as a check. C one three is minus zero point three four two, so theta "
                  "is the negative arc sine of that, which is twenty degrees."),
        ("v3_25", "atan two of zero point four six nine eight and zero point eight one three eight gives thirty "
                  "degrees for psi. And atan two of zero point one six three two and zero point nine two five four "
                  "gives ten degrees for phi. All three angles come back."),
        ("v3_26", "Example two: pointing a ground station dish. Define a frame T at a ground station. t one points "
                  "straight up, t two points east, and t three points north. This takes two rotations from the "
                  "inertial frame N."),
        ("v3_27", "First, rotate about n three by the station's angle around the equator, theta plus lambda. Call "
                  "this frame E. e one now points toward the station's meridian, along the equator."),
        ("v3_28", "Second, tip up by the latitude, phi, about e two. To swing e one up toward the north pole, we "
                  "need a rotation of minus phi about axis two. So C T N equals C two of minus phi, times C three "
                  "of theta plus lambda."),
        ("v3_29", "Let's use Kennedy Space Center, at latitude twenty eight point six degrees, at a moment when "
                  "theta plus lambda is forty five degrees. Multiplying the two matrices gives this C T N."),
        ("v3_30", "A satellite is at three thousand five hundred thirty nine, four thousand five hundred thirty, "
                  "three thousand five hundred ninety two kilometers in N. Multiply by C T N to get its position in "
                  "T. Then subtract the station's own position, which is R earth along t one: six thousand three "
                  "hundred seventy eight kilometers up."),
        ("v3_31", "The result is three hundred fifty one up, seven hundred one east, and four hundred twenty three "
                  "north, all in kilometers. The up component is positive, so the satellite is above the horizon."),
        ("v3_32", "Elevation is the arc sine of the up component over the total distance: about twenty three "
                  "degrees. Azimuth, measured from north toward east, is atan two of east over north: about fifty "
                  "nine degrees. That's where the dish should point."),
        ("v3_33", "Recap. Single axis rotations are the building blocks. Chain them with the newest rotation on "
                  "the left. Read the angles back from specific entries using atan two. And watch out for gimbal "
                  "lock."),
    ],
    # ------------------------------------------------------------------ V4
    "V4Concept": [
        ("v4_01", "So far, our frames have been frozen in place. But spacecraft tumble, and the Earth spins. In this "
                  "lesson, we'll describe how fast a frame is rotating, with a vector called angular velocity."),
        ("v4_02", "Start with the simplest case. Frame B rotates relative to N about n three, and the angle between "
                  "them is theta, which changes with time. Its rate of change, theta dot, is the rotation rate."),
        ("v4_03", "The angular velocity of B relative to N is defined as theta dot times n three. It's a vector. "
                  "Its direction is the axis of rotation, chosen by the right hand rule: curl your fingers in the "
                  "direction of turning, and your thumb points along omega. Its length is the rotation rate."),
        ("v4_04", "Notice the superscript, B slash N. This means the rotation of frame B, as seen from frame N. "
                  "Swapping the order flips the sign: omega N slash B is minus omega B slash N."),
        ("v4_05", "Now the key question. As B rotates, its basis vectors move. How fast? Let's find the time "
                  "derivative of b one, as seen in N, directly from the components."),
        ("v4_06", "We know b one equals cosine theta n one plus sine theta n two. The N axes don't move as seen in "
                  "N, so only the cosine and sine change. Using the chain rule, the derivative is minus theta dot "
                  "sine theta n one, plus theta dot cosine theta n two."),
        ("v4_07", "Factor out theta dot. What's left, minus sine theta n one plus cosine theta n two, is exactly b "
                  "two. So the derivative of b one is theta dot times b two."),
        ("v4_08", "Now compare with a cross product. omega cross b one is theta dot b three cross b one. By the "
                  "right handed rule, b three cross b one is b two. So omega cross b one is also theta dot b two. "
                  "They match!"),
        ("v4_09", "This isn't a coincidence. Here's the geometric reason, for any rotation. Picture a unit vector "
                  "b, fixed in B, making an angle phi with omega. As B turns, the tip of b sweeps a circle around "
                  "omega."),
        ("v4_10", "The radius of that circle is sine phi. In a short time delta t, the frame turns through an angle "
                  "omega delta t, so the tip moves a distance sine phi times omega delta t. Divide by delta t: the "
                  "speed of the tip is sine phi times the size of omega."),
        ("v4_11", "The tip moves along the circle, so its velocity is perpendicular to both b and omega. A vector "
                  "perpendicular to both, with size sine phi times omega: that's precisely omega cross b. So for "
                  "every basis vector of B, its derivative in N is omega cross b i."),
        ("v4_12", "Angular velocities can be added, as long as they chain through the frames. If A rotates "
                  "relative to N, and B rotates relative to A, then omega B relative to N equals omega B relative "
                  "to A, plus omega A relative to N."),
        ("v4_13", "For the three two one Euler angles, the chain is A to P to Q to B. Each step is a single "
                  "rotation, so each has a simple angular velocity: psi dot about p three, theta dot about q two, "
                  "and phi dot about b one. Adding them gives omega B relative to A."),
        ("v4_14", "To use this, we want all three pieces in B components. b one is already in B. For the other "
                  "two, we use the D C Ms we already know, one step at a time."),
        ("v4_15", "From the roll rotation, C one of phi, we can write q two in B. q two equals cosine phi b two, "
                  "minus sine phi b three."),
        ("v4_16", "p three takes two steps. From the pitch rotation, p three equals minus sine theta q one, plus "
                  "cosine theta q three. Then q one is b one, and q three is sine phi b two plus cosine phi b "
                  "three. Substituting gives p three equals minus sine theta b one, plus cosine theta sine phi b "
                  "two, plus cosine theta cosine phi b three."),
        ("v4_17", "Now substitute everything, and collect the b one, b two, and b three terms. We get omega one "
                  "equals phi dot minus psi dot sine theta. omega two equals theta dot cosine phi plus psi dot "
                  "cosine theta sine phi. And omega three equals minus theta dot sine phi plus psi dot cosine theta "
                  "cosine phi."),
        ("v4_18", "We can write this as a matrix times the column of Euler angle rates. In practice we need the "
                  "reverse: a gyroscope measures omega, and we want the Euler angle rates, so we can integrate them "
                  "forward in time. Inverting the matrix gives this."),
        ("v4_19", "Look at the factor out front: one over cosine theta. As theta approaches ninety degrees, this "
                  "blows up, and the angle rates become infinite. That's gimbal lock again, now showing up in the "
                  "rates."),
    ],
    "V4Examples": [
        ("v4_20", "Example one: the Earth. The Earth turns once relative to the stars every sidereal day, which is "
                  "about eighty six thousand one hundred sixty four seconds. Two pi divided by that gives omega "
                  "equals seven point two nine two one times ten to the minus five radians per second, pointing "
                  "along n three."),
        ("v4_21", "A point on the ground is fixed in the Earth frame. So its inertial velocity comes entirely from "
                  "the rotation: v equals omega cross r. The size is omega times the distance from the spin axis, "
                  "which is R times cosine of the latitude. The direction is due east."),
        ("v4_22", "Let's compute it for three launch sites. At Kennedy Space Center, latitude twenty eight point "
                  "six degrees, the speed is about four hundred eight meters per second. At Wallops Island, "
                  "latitude thirty seven point nine degrees, it's about three hundred sixty seven. And at Alcantara "
                  "in Brazil, almost on the equator, it's about four hundred sixty five."),
        ("v4_23", "That's a free boost for eastward launches, and it's biggest at the equator. It's one reason "
                  "launch sites for eastward orbits are built as close to the equator as possible."),
        ("v4_24", "Example two: Euler rates to angular velocity. A spacecraft has three two one angles of thirty, "
                  "twenty, and ten degrees, with rates psi dot equals one, theta dot equals two, and phi dot equals "
                  "three degrees per second. Find omega in B."),
        ("v4_25", "omega one is phi dot minus psi dot sine theta: three minus one times sine twenty, which is three "
                  "minus zero point three four two, giving two point six five eight degrees per second."),
        ("v4_26", "omega two is theta dot cosine phi plus psi dot cosine theta sine phi: two times cosine ten, plus "
                  "cosine twenty times sine ten. That's one point nine six nine plus zero point one six three, "
                  "giving two point one three three."),
        ("v4_27", "omega three is minus theta dot sine phi plus psi dot cosine theta cosine phi: minus two times "
                  "sine ten, plus cosine twenty times cosine ten. That's minus zero point three four seven plus "
                  "zero point nine two five, giving zero point five seven eight degrees per second."),
        ("v4_28", "Notice that omega is not simply one, two, three. The Euler angle rates act about tilted, non "
                  "perpendicular axes, so they mix together when written in the body frame."),
        ("v4_29", "Recap. Angular velocity points along the spin axis, with length equal to the spin rate. Every "
                  "basis vector of a rotating frame changes at the rate omega cross b. Angular velocities add "
                  "through a chain of frames. And Euler angle rates relate to omega through a matrix that becomes "
                  "singular at gimbal lock."),
    ],
    # ------------------------------------------------------------------ V5
    "V5Concept": [
        ("v5_01", "In this lesson, we'll answer a deceptively simple question: how do you take the time derivative "
                  "of a vector? The answer, called the transport theorem, is the most important tool in this "
                  "course."),
        ("v5_02", "Here's the puzzle. Picture a vector painted on a spinning disk. To someone riding on the disk, "
                  "the vector never changes. Its derivative is zero. But to someone standing on the ground, the "
                  "vector is clearly swinging around. Its derivative is not zero."),
        ("v5_03", "Both observers are right. So a time derivative of a vector only makes sense once we say which "
                  "frame it's taken in. We write a small N before d by d t to mean the derivative as seen in frame "
                  "N, and a small B to mean the derivative as seen in frame B."),
        ("v5_04", "Let's derive the rule, one step at a time. Start by writing r in B components: r equals r one b "
                  "one, plus r two b two, plus r three b three."),
        ("v5_05", "First, the derivative as seen in B. To an observer in B, the B axes are fixed. So only the "
                  "components change. The B derivative of r is r one dot b one, plus r two dot b two, plus r three "
                  "dot b three."),
        ("v5_06", "Now the derivative as seen in N. Each term is a product, a number times a vector, so we use the "
                  "product rule. Each term splits in two: r i dot times b i, plus r i times the N derivative of b "
                  "i."),
        ("v5_07", "Group the terms. The first group, r i dot b i, is exactly the B derivative we just found."),
        ("v5_08", "For the second group, use the result from the last lesson: the N derivative of b i is omega "
                  "cross b i. So the second group becomes r one omega cross b one, plus r two omega cross b two, "
                  "plus r three omega cross b three."),
        ("v5_09", "The cross product is linear, so we can pull omega out front: omega cross the quantity r one b "
                  "one plus r two b two plus r three b three. And that quantity is just r itself."),
        ("v5_10", "Putting it together: the N derivative of r equals the B derivative of r, plus omega B relative "
                  "to N, cross r. This is the transport theorem."),
        ("v5_11", "Let's read it in words. The rate of change seen by N equals the rate of change seen by B, plus "
                  "an extra term that accounts for B itself turning. That extra term, omega cross r, is called the "
                  "transport term."),
        ("v5_12", "Back to the disk. A point fixed on the disk has B derivative zero. So its N velocity is just "
                  "omega cross r: a vector tangent to the circle the point sweeps out."),
        ("v5_13", "If the point also slides outward along the disk, the B observer sees just the sliding, a radial "
                  "velocity. The N observer sees the sliding, plus the carrying. The total is the vector sum."),
        ("v5_14", "The theorem works for any vector, not just position: velocities, angular momentum, anything. And "
                  "it gives a reliable recipe. One: pick a frame where the vector is simple. Two: write it in that "
                  "frame's components. Three: differentiate the components. Four: add omega cross the vector. Five, "
                  "if needed: convert to another frame with a D C M."),
    ],
    "V5Examples": [
        ("v5_15", "Example one: a point on a spinning disk. The disk spins at constant rate omega about b three, and "
                  "the point sits at R b one, with R constant."),
        ("v5_16", "Step three of the recipe: the B derivative. R is constant, and b one is fixed in B, so the B "
                  "derivative is zero."),
        ("v5_17", "Step four: omega cross r is omega b three cross R b one. b three cross b one is b two, so this is "
                  "omega R b two. So the velocity has size omega R, pointing along b two, tangent to the circle, "
                  "just as we pictured."),
        ("v5_18", "Example two: a telescoping arm. A satellite spins at constant rate omega about b three. An arm "
                  "along b one extends at a steady rate, so its length is L of t equals L zero plus c t. Find the "
                  "velocity of the mass at the tip."),
        ("v5_19", "In B, the tip is simply at L b one. Its B derivative is L dot b one, which is c b one."),
        ("v5_20", "The transport term is omega b three cross L b one, which is omega L b two. So the inertial "
                  "velocity, in B components, is c b one, plus omega times L zero plus c t, b two."),
        ("v5_21", "Now step five: express it in N. Since B started aligned with N and spins about the third axis, b "
                  "one equals cosine omega t n one plus sine omega t n two, and b two equals minus sine omega t n "
                  "one plus cosine omega t n two."),
        ("v5_22", "Substitute and collect. The n one component is c cosine omega t, minus omega L sine omega t. The "
                  "n two component is c sine omega t, plus omega L cosine omega t."),
        ("v5_23", "Let's double check the hard way. In N, the tip is at L cosine omega t n one plus L sine omega t n "
                  "two. Differentiate each component with the product rule. The n one component gives L dot cosine "
                  "omega t, minus L omega sine omega t. Same as before. The n two component also matches. The "
                  "transport theorem gave the right answer, with much less work."),
        ("v5_24", "Example three: cylindrical coordinates. A point is at radius R, angle theta, and height z. Use a "
                  "frame E that turns with the point, so r equals R e one plus z e three, and omega E relative to N "
                  "is theta dot e three."),
        ("v5_25", "The E derivative is R dot e one plus z dot e three. The transport term is theta dot e three "
                  "cross the quantity R e one plus z e three. e three cross e one is e two, and e three cross e "
                  "three is zero, so it's R theta dot e two."),
        ("v5_26", "So the velocity is R dot e one, plus R theta dot e two, plus z dot e three. That's the standard "
                  "cylindrical velocity formula, derived in three lines."),
        ("v5_27", "Recap. The derivative of a vector depends on the observer. The transport theorem connects two "
                  "observers: the N derivative equals the B derivative plus omega cross r. Pick the simple frame, "
                  "differentiate there, and add the transport term."),
    ],
    # ------------------------------------------------------------------ V6
    "V6Concept": [
        ("v6_01", "In the last lesson, the transport theorem gave us velocity. In this lesson, we'll apply it a "
                  "second time to get acceleration, and we'll see where the famous Coriolis and centripetal terms "
                  "come from. Every step will be on the screen."),
        ("v6_02", "Start from the velocity: v equals the B derivative of r, plus omega cross r. To make it easier "
                  "to read, we'll write the B derivative of r as r dot with a small B, and its second derivative as "
                  "r double dot with a small B."),
        ("v6_03", "Acceleration is the N derivative of v. Since v is a sum of two terms, we take the N derivative "
                  "of each term separately."),
        ("v6_04", "Term one: the N derivative of B r dot. This is just another vector, so we apply the transport "
                  "theorem to it. Its N derivative is its B derivative, which is B r double dot, plus omega cross B "
                  "r dot."),
        ("v6_05", "Term two: the N derivative of omega cross r. The product rule works for cross products too, as "
                  "long as we keep the order. We get the derivative of omega, cross r, plus omega cross the N "
                  "derivative of r."),
        ("v6_06", "Two details. First, the derivative of omega is the same whether seen in N or in B, because the "
                  "transport term would be omega cross omega, which is zero. We just call it omega dot. Second, the "
                  "N derivative of r is v, which we already know: B r dot plus omega cross r."),
        ("v6_07", "Substitute that in. omega cross the quantity B r dot plus omega cross r splits into omega cross "
                  "B r dot, plus omega cross omega cross r."),
        ("v6_08", "Now add the two terms together, and write every piece in one line. Notice that omega cross B r "
                  "dot appears twice: once from term one, and once from term two."),
        ("v6_09", "Combine them. The final result: the N acceleration equals B r double dot, plus omega dot cross "
                  "r, plus two omega cross B r dot, plus omega cross omega cross r."),
        ("v6_10", "Each term has a name. B r double dot is the relative acceleration: what you'd measure riding "
                  "along in B."),
        ("v6_11", "omega dot cross r is the tangential, or Euler, acceleration. It only appears when the spin rate "
                  "is changing, like when a merry go round speeds up."),
        ("v6_12", "Two omega cross B r dot is the Coriolis acceleration. It only appears when the point moves "
                  "relative to B."),
        ("v6_13", "And omega cross omega cross r is the centripetal acceleration. Let's check its direction for a "
                  "point at R b one, with omega equal to omega b three. The inner cross product is omega R b two. "
                  "Then omega b three cross omega R b two is omega squared R, times b three cross b two, which is "
                  "minus b one. So it's minus omega squared R b one: pointing inward, toward the axis, with the "
                  "familiar size omega squared R."),
        ("v6_14", "Here's the Coriolis effect, made visible. A puck slides without friction across a spinning disk. "
                  "Seen from above, in N, it moves in a perfectly straight line, because no force acts on it. But "
                  "to someone riding the disk, the path curves. That curving is exactly the Coriolis and "
                  "centripetal terms, appearing because the observer is rotating."),
    ],
    "V6Examples": [
        ("v6_15", "Example one: the telescoping arm again. Constant spin omega about b three, and arm length L of "
                  "t. Let's find the acceleration of the tip, term by term."),
        ("v6_16", "Relative: B r double dot is L double dot b one. Tangential: omega is constant, so omega dot is "
                  "zero, and this term vanishes."),
        ("v6_17", "Coriolis: two omega b three cross L dot b one. b three cross b one is b two, so this is two omega "
                  "L dot b two."),
        ("v6_18", "Centripetal: just as we found before, minus omega squared L b one."),
        ("v6_19", "Adding them, the acceleration is L double dot minus omega squared L, along b one, plus two omega "
                  "L dot, along b two. For our steady extension, L double dot is zero and L dot is c, so a equals "
                  "minus omega squared L b one, plus two omega c b two. The sideways part is pure Coriolis: the arm "
                  "has to push the mass sideways to keep it on the arm."),
        ("v6_20", "Example two: polar coordinates, the doorway to orbital mechanics. A planet is at distance r from "
                  "the Sun, at angle theta. Use a frame E that turns with it, with e r pointing out toward the "
                  "planet, and e theta perpendicular. Then the position is r e r, and omega is theta dot e three."),
        ("v6_21", "Relative: r double dot e r. Tangential: theta double dot e three cross r e r, which is r theta "
                  "double dot e theta. Coriolis: two theta dot e three cross r dot e r, which is two r dot theta dot "
                  "e theta."),
        ("v6_22", "Centripetal: theta dot e three cross theta dot e three cross r e r. The inner part is r theta "
                  "dot e theta. Then e three cross e theta is minus e r, so this gives minus r theta dot squared e "
                  "r."),
        ("v6_23", "Collect: the acceleration is r double dot minus r theta dot squared, along e r, plus r theta "
                  "double dot plus two r dot theta dot, along e theta."),
        ("v6_24", "Gravity pulls only along e r, so the e theta part must be zero. That sideways part equals one "
                  "over r, times the derivative of r squared theta dot. So r squared theta dot is constant. That "
                  "quantity is the specific angular momentum, and its being constant is Kepler's second law: equal "
                  "areas in equal times."),
        ("v6_25", "And setting the radial part equal to gravity, minus mu over r squared, gives the equation that "
                  "leads to elliptical orbits. Everything in orbital mechanics starts from this one application of "
                  "the transport theorem."),
        ("v6_26", "Final recap. Apply the transport theorem twice. Expand with the product rule. Collect the two "
                  "Coriolis pieces. You get four terms: relative, tangential, Coriolis, and centripetal. With this, "
                  "you can find the motion of anything, as seen from any frame."),
    ],
}

SCENE_ORDER = list(SCRIPT.keys())


def all_segments():
    for scene in SCENE_ORDER:
        for seg_id, text in SCRIPT[scene]:
            yield scene, seg_id, text
