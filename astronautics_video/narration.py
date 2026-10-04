"""Narration script for "Same Arrow, Different Observers" (AERSP 309 kinematics).

Each scene is a list of (segment_id, spoken_text). The segment ids are used by
tts.py to name audio files and by scenes.py to sync animations to the voice.
"""

STYLE = (
    "Speak like a thoughtful math educator narrating an animated explainer: "
    "warm, curious, gently enthusiastic, unhurried, with clear enunciation "
    "and natural pauses."
)

SCRIPT = {
    "Intro": [
        ("intro_1",
         "Here's a question that sounds almost too simple. A UFO is hovering "
         "perfectly still, eighty kilometers above State College. How fast is "
         "it moving?"),
        ("intro_2",
         "Ask Bob, standing on the ground, and the answer is zero. It isn't "
         "going anywhere. But ask someone floating out in space, watching the "
         "Earth turn beneath them, and that same UFO is moving at more than "
         "three hundred and fifty meters per second."),
        ("intro_3",
         "They're both right. The difference isn't the UFO. It's the "
         "observer. And in astronautics, almost every problem comes down to "
         "exactly this: keeping track of who is looking, and how their point "
         "of view is turning."),
        ("intro_4",
         "So in this video, we'll build the whole toolkit from scratch. "
         "Reference frames. Direction cosine matrices. Euler angles. Angular "
         "velocity. And the transport theorem, the one equation that ties it "
         "all together. Then we'll use it to find acceleration, and see where "
         "Coriolis and centripetal terms really come from."),
    ],
    "Frames": [
        ("frames_1",
         "Let's start with the most basic object: a vector. An arrow, with a "
         "length and a direction. The important thing is that this arrow "
         "exists on its own. It doesn't need any numbers to be real."),
        ("frames_2",
         "To describe it with numbers, we need a reference frame. A frame is "
         "an origin, plus three unit vectors, n hat one, two, and three. "
         "They're mutually perpendicular, and right handed: n one cross n two "
         "gives n three."),
        ("frames_3",
         "Now here's the key idea. The components of a vector are just "
         "shadows. Project the arrow onto n one, and the length of that "
         "shadow is r dot n one. Do the same for the other two axes, and "
         "you've got three numbers."),
        ("frames_4",
         "Stack them in a column, and you have r, expressed in the N frame. "
         "Notice that subscript. The arrow is the vector. The column is just "
         "one particular way of writing it down."),
        ("frames_5",
         "Because if someone else uses a different frame, tilted relative to "
         "ours, the very same arrow casts completely different shadows. Same "
         "arrow, different numbers. The whole game of this subject is "
         "translating between those descriptions."),
    ],
    "DCM": [
        ("dcm_1",
         "So how do we translate? Take the simplest case. Frame B starts out "
         "lined up with frame N, then rotates by an angle theta about their "
         "shared third axis."),
        ("dcm_2",
         "Any vector can be broken into pieces along the N axes, and that "
         "includes b one itself. The amount of b one along n one is b one dot "
         "n one. Both are unit vectors, so that's just the cosine of the "
         "angle between them: cosine theta."),
        ("dcm_3",
         "The angle between b one and n two is ninety degrees minus theta, so "
         "that dot product is sine theta. Do the same for b two, and you get "
         "minus sine theta, and cosine theta."),
        ("dcm_4",
         "Collect every one of these dot products in a grid, and that grid is "
         "the direction cosine matrix, C B N. Each entry is the cosine of the "
         "angle between one B axis and one N axis, which is exactly where the "
         "name comes from."),
        ("dcm_5",
         "Read across a row, and you get one of the B axes, written in N "
         "components. Read down a column, and you get one of the N axes, "
         "written in B components."),
        ("dcm_6",
         "Since every row is a unit vector, and the rows are all perpendicular "
         "to each other, the matrix is orthogonal. That gives it the most "
         "useful property of all: its inverse is just its transpose. Going "
         "backwards, from B to N, costs nothing. You simply flip the matrix."),
        ("dcm_7",
         "And here's the payoff. To convert any vector from N components to B "
         "components, multiply by the DCM. r in B equals C B N times r in N. "
         "Watch: the arrow never moves. Only its description changes."),
        ("dcm_8",
         "Nine numbers, but they aren't independent. Each row has unit length: "
         "three constraints. The rows are mutually perpendicular: three more. "
         "Nine minus six leaves three. Orientation in three dimensions has "
         "exactly three degrees of freedom."),
        ("dcm_9",
         "Here's a concrete use, straight from the homework. The Endurance is "
         "spinning at zero point six five radians per second. Six seconds "
         "later, it has turned three point nine radians. The DCM from the "
         "inertial frame to the station's frame is just a single third axis "
         "rotation by that angle, and it's exactly the matrix the lander's "
         "computer needs to line itself up for docking."),
    ],
    "Euler": [
        ("euler_1",
         "Three degrees of freedom suggests something. Maybe any orientation "
         "can be reached with just three simple turns. That's Euler's insight: "
         "every orientation is a sequence of three rotations, each one about "
         "an axis of the frame you just created."),
        ("euler_2",
         "The classic aerospace sequence is three, two, one. Yaw, pitch, and "
         "roll. First, rotate by psi about the third axis. That carries frame "
         "A to an intermediate frame, P."),
        ("euler_3",
         "Next, pitch by theta about the brand new second axis, p two, giving "
         "frame Q."),
        ("euler_4",
         "Finally, roll by phi about the newest first axis, landing on the "
         "body frame, B."),
        ("euler_5",
         "Each step is a single axis DCM, and they chain together by "
         "multiplication, with the last rotation on the left. C B A equals C "
         "one of phi, times C two of theta, times C three of psi."),
        ("euler_6",
         "The first rotation can use any of three axes. The second, either of "
         "the other two. And the third, anything but the one just used. Three "
         "times two times two: twelve possible Euler angle sets, all of them "
         "tabulated in your appendix."),
        ("euler_7",
         "Going backwards, from a DCM to angles, you read them off particular "
         "entries. For three two one, the top right entry is minus sine "
         "theta, and the other two angles come from arc tangents of ratios."),
        ("euler_8",
         "But watch what happens as the pitch approaches ninety degrees. The "
         "roll axis swings around until it lines up with the original yaw "
         "axis. Now yaw and roll do the same thing, and only their difference "
         "matters. We've lost a degree of freedom. This is gimbal lock."),
        ("euler_9",
         "Every Euler angle set has a singularity like this. Asymmetric sets, "
         "like three two one, break at plus or minus ninety degrees. "
         "Symmetric sets, like three one three, break at zero and one eighty. "
         "So you choose the set whose singularity stays far away from the "
         "motion you care about."),
    ],
    "AngularVelocity": [
        ("omega_1",
         "So far, everything has been frozen in time. But spacecraft tumble, "
         "and planets turn. To describe a frame that's rotating, we need "
         "angular velocity."),
        ("omega_2",
         "For a single rotation, it's simple. If B spins about n three at a "
         "rate theta dot, then omega of B relative to N is theta dot times n "
         "three. A vector, pointing along the axis of rotation, whose length "
         "is how fast it spins."),
        ("omega_3",
         "Now ask: how fast is the tip of a B axis moving, as seen from N? The "
         "tip sweeps out a circle around omega. Its radius is sine phi, where "
         "phi is the angle between the axis and omega. So its speed is sine "
         "phi, times the size of omega."),
        ("omega_4",
         "And its direction is perpendicular to both b hat and omega. Size "
         "sine phi, perpendicular to both. That's a cross product! The "
         "derivative of each basis vector is simply omega cross that basis "
         "vector."),
        ("omega_5",
         "Angular velocities also add, as long as you chain them through the "
         "frames. For the three two one sequence, omega of B relative to A is "
         "psi dot along p three, plus theta dot along q two, plus phi dot "
         "along b one."),
        ("omega_6",
         "Careful, though. Those three axes are not perpendicular to each "
         "other. To get omega in clean B components, rotate each piece into "
         "the B frame, and you get this."),
        ("omega_7",
         "In practice, we usually go the other way. A gyroscope measures "
         "omega, and we want to know how the Euler angles evolve. Invert that "
         "matrix, and look at the one over cosine theta out front. At ninety "
         "degrees of pitch, it blows up. That's gimbal lock again, now showing "
         "up as infinite angle rates."),
    ],
    "Transport": [
        ("trans_1",
         "Now for the main event. Here's a question that turns out to be "
         "surprisingly subtle. What is the time derivative of a vector?"),
        ("trans_2",
         "Write r in B components, and differentiate. The product rule gives "
         "two kinds of terms. The components can change: r dot times b hat. "
         "But the basis vectors themselves might change too."),
        ("trans_3",
         "And whether they change depends on who's watching. To an observer "
         "riding along in B, the B axes are frozen, so only the component "
         "terms survive. That's the derivative in B. But to an observer in N, "
         "the B axes are spinning, and each one's derivative is omega cross b "
         "hat."),
        ("trans_4",
         "Put it together, factor out the omega, and the leftover sum is just "
         "r again. This is the transport theorem. The derivative as seen in N "
         "equals the derivative as seen in B, plus omega cross r."),
        ("trans_5",
         "Here's how to picture it. A point sits still on a spinning disk. The "
         "observer on the disk sees nothing happen. The B derivative is zero. "
         "But from N, the point is whipping around in a circle, with velocity "
         "exactly omega cross r. That's the transport velocity: motion you "
         "get for free, just by being carried along with the frame."),
        ("trans_6",
         "Now let the point slide outward along the disk. The B observer sees "
         "only the sliding. The N observer sees the sliding, plus the "
         "carrying. Two motions, simply added together."),
        ("trans_7",
         "And here's the practical magic. This works for any vector, not just "
         "positions. You get to pick the frame where a vector looks simplest, "
         "take the easy derivative there, and let omega cross r handle "
         "everything else."),
        ("trans_8",
         "For example, cylindrical coordinates. In a frame E that turns with "
         "the point, the position is just R e one plus z e three. Its E "
         "derivative is R dot e one plus z dot e three, and omega cross r "
         "adds R theta dot along e two. Done. No sines and cosines to "
         "differentiate."),
    ],
    "UFO": [
        ("ufo_1",
         "Let's go back to Bob and his UFO. Relative to the Earth, the UFO "
         "never moves. It sits at a radius of sixty three seventy plus eighty, "
         "so sixty four fifty kilometers, above latitude forty point eight "
         "degrees north."),
        ("ufo_2",
         "Position first. The UFO's direction is a unit vector set by its "
         "latitude, phi, and its angle around the equator, theta plus lambda. "
         "Scale by sixty four fifty, plug in the numbers, and we have r in "
         "the inertial frame."),
        ("ufo_3",
         "Velocity. The UFO is fixed in the Earth frame, so the Earth "
         "derivative is zero, and the transport theorem leaves only omega "
         "cross r. That works out to about three hundred fifty six meters per "
         "second, due east, for a UFO that isn't moving."),
        ("ufo_4",
         "Acceleration. Apply the theorem one more time, and all that "
         "survives is omega cross omega cross r. It points straight toward "
         "Earth's axis, with size omega squared times the distance from the "
         "axis. About two point six centimeters per second squared. Tiny, but "
         "it's real."),
    ],
    "Acceleration": [
        ("acc_1",
         "Now that we can differentiate in a rotating frame, acceleration is "
         "just doing it twice. Velocity is the B derivative of r, plus omega "
         "cross r. So apply the transport theorem to that entire expression."),
        ("acc_2",
         "Expand everything, and notice that one term appears twice: omega "
         "cross the B derivative of r."),
        ("acc_3",
         "Collect them, and four distinct pieces fall out, each with its own "
         "name."),
        ("acc_4",
         "The first is the acceleration you'd measure riding along in B. The "
         "second, omega dot cross r, appears only when the spin rate itself "
         "changes. It's the tangential kick you feel when a merry go round "
         "speeds up."),
        ("acc_5",
         "The last term, omega cross omega cross r, always points inward, "
         "toward the spin axis. That's centripetal acceleration: the price of "
         "being carried around in a circle."),
        ("acc_6",
         "And the middle one, two omega cross r dot, is Coriolis. It only "
         "shows up when you move within the rotating frame."),
        ("acc_7",
         "Here's a puck sliding without friction across a spinning disk. From "
         "above, in N, it moves in a perfectly straight line. But to someone "
         "riding the disk, its path curves away. No real force is acting. All "
         "of that curving comes from the Coriolis and centripetal terms, "
         "because it's the observer who is turning."),
        ("acc_8",
         "Now the merry go round, straight from lecture. Constant spin rate, "
         "theta dot, and a person at R b one, walking outward. Plug in, and "
         "the B acceleration gives R double dot, Coriolis gives two theta dot "
         "R dot along b two, and centripetal gives minus theta dot squared R."),
        ("acc_9",
         "Stand still, and all you need is the inward centripetal force. But "
         "start walking outward, and suddenly you need a sideways push too. "
         "That's Coriolis, and it's why walking in a straight line on a "
         "spinning ride feels so strange."),
        ("acc_10",
         "Finally, the exact same machinery gives acceleration in polar "
         "coordinates. r double dot minus r theta dot squared, radially. Two r "
         "dot theta dot plus r theta double dot, sideways. Those two lines are "
         "where orbital mechanics begins. Set the sideways part to zero, and "
         "out comes conservation of angular momentum, and Kepler's second "
         "law. Set the radial part equal to gravity, and out come the "
         "ellipses."),
    ],
    "Outro": [
        ("outro_1",
         "Let's step back. A vector is an arrow. A frame is a way of casting "
         "its shadows. The direction cosine matrix translates between frames. "
         "Euler angles build it out of three simple turns. And angular "
         "velocity tells us how fast a frame is turning."),
        ("outro_2",
         "And the transport theorem ties it all together. The derivative "
         "depends on the observer, and omega cross r is the exact price of "
         "switching observers. Apply it once for velocity, twice for "
         "acceleration, and every spinning space station, every Coriolis "
         "puzzle, every orbit, becomes careful bookkeeping."),
        ("outro_3",
         "Same arrow. Different observers. Thanks for watching."),
    ],
}

SCENE_ORDER = list(SCRIPT.keys())


def all_segments():
    for scene in SCENE_ORDER:
        for seg_id, text in SCRIPT[scene]:
            yield scene, seg_id, text
