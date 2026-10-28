"""Narration for the AERSP 301 'Shear of Beams' lesson series (5 videos).

Concept videos first (shear flow, shear center, closed sections), then the
two HW 3 problems worked as applications.
"""

STYLE = (
    "Speak slowly and patiently, like a friendly tutor guiding a student who is "
    "seeing this for the first time: warm, clear and unhurried, with a natural "
    "pause between sentences and a slightly longer pause after each step."
)

SCRIPT = {
    # ------------------------------------------------------------ S1: shear flow
    "S1Concept": [
        ("s1_01", "Welcome to this series on the shear of thin walled beams. Aircraft wings and fuselages are "
                  "built from thin sheets of metal: spars, skins, and stringers. In this first lesson, we'll "
                  "answer one question: when a shear load acts on a thin walled beam, how is that load carried "
                  "by the walls?"),
        ("s1_02", "Picture a cantilever beam with a vertical load S y at its tip. The load creates a bending "
                  "moment, and that moment grows as you move away from the tip. A growing moment means growing "
                  "bending stress. Something has to balance that change. That something is shear, flowing "
                  "around the walls of the cross section."),
        ("s1_03", "First, some vocabulary. z runs along the beam. s is a distance measured around the wall of the "
                  "cross section, starting from some convenient origin. The wall has thickness t, which may vary "
                  "with s, but not along the beam."),
        ("s1_04", "We make a few assumptions, all tied to the walls being thin. Stresses are constant through "
                  "the thickness. Shear stress normal to the wall surface is negligible. And terms with t "
                  "squared or t cubed are thrown away."),
        ("s1_05", "Because the shear stress is constant through the thickness, it's convenient to multiply it by "
                  "the thickness. That product, q equals tau times t, is called the shear flow. Its units are "
                  "force per unit length along the wall. Think of it like water flowing through a channel: it "
                  "travels around the cross section, and it's positive in the direction of increasing s."),
        ("s1_06", "Now cut out a tiny element of the wall, delta s wide and delta z long. On its two faces "
                  "normal to z, there's the direct stress sigma z. On the far face it has grown slightly, to "
                  "sigma z plus the partial derivative with respect to z, times delta z."),
        ("s1_07", "On its two edges, there's shear flow. On one edge it's q, and on the other it has changed to q "
                  "plus the partial of q with respect to s, times delta s."),
        ("s1_08", "Add up all the forces in the z direction. Each stress times the area it acts on, and each "
                  "shear flow times the length it acts along. The two sigma z terms partly cancel, and so do the "
                  "two q terms."),
        ("s1_09", "What survives is the partial of sigma z with respect to z, times t, times delta s, times delta "
                  "z, plus the partial of q with respect to s, times delta s, times delta z, equals zero. Divide "
                  "by delta s delta z, and we get the key equation: the partial of q with respect to s, plus t "
                  "times the partial of sigma z with respect to z, equals zero."),
        ("s1_10", "Read it in words. If the bending stress changes as you move along the beam, the shear flow "
                  "must change as you move around the wall. The shear flow is what carries the difference."),
        ("s1_11", "Next we need sigma z. From unsymmetrical bending theory, the direct stress is this "
                  "expression in M x, M y, and the second moments of area I x x, I y y, and I x y, with x and y "
                  "measured from the centroid."),
        ("s1_12", "Differentiate with respect to z. Only the moments depend on z, and the rate of change of "
                  "bending moment is the shear force: the derivative of M x is S y, and the derivative of M y is "
                  "S x. So the partial of sigma z with respect to z has the same form, with S x and S y in place "
                  "of the moments."),
        ("s1_13", "Substitute this into the equilibrium equation, and integrate around the wall from s equals "
                  "zero. If we start at an open edge, the shear flow there is zero, because nothing is attached "
                  "to it. That gives the open section shear flow formula."),
        ("s1_14", "When the section has an axis of symmetry, I x y is zero and the formula simplifies a lot: q "
                  "equals minus S x over I y y, times the integral of t x d s, minus S y over I x x, times the "
                  "integral of t y d s."),
        ("s1_15", "Here's what that integral means. The integral of t y d s, from the free edge to the point s, is "
                  "the first moment of area of the wall you've swept past. As you sweep farther from the neutral "
                  "axis, it grows fastest. That's why shear flow builds up along a flange, peaks at the neutral "
                  "axis, and falls back to zero at the other free edge."),
        ("s1_16", "So here's the recipe. One: find the centroid and the second moments of area. Two: start at a "
                  "free edge, where q is zero. Three: integrate wall by wall, carrying the shear flow across each "
                  "corner. Four: check that q returns to zero at the other free edge, and that the shear flows "
                  "add up to the applied load."),
    ],
    # ------------------------------------------------------ S2: shear center
    "S2Concept": [
        ("s2_01", "In the last lesson, we found the shear flow in an open section. In this lesson, we'll use it to "
                  "find one of the most important points in structural design: the shear center."),
        ("s2_02", "Here's a channel section, with a vertical load applied right along its web. You might expect it "
                  "to simply bend. But it also twists. Why? Because the shear flow in the walls creates a moment, "
                  "and that moment isn't balanced by the load."),
        ("s2_03", "There is exactly one line of action for which a shear load bends the beam without twisting it. "
                  "The point where that line crosses the section is the shear center, S. Load through S: pure "
                  "bending. Load anywhere else: bending plus twist."),
        ("s2_04", "Two shortcuts. If the section has an axis of symmetry, the shear center lies on that axis. And "
                  "for sections made of straight walls that meet at a single point, like an angle or a cross, the "
                  "shear center is at that meeting point, because every wall's force passes through it."),
        ("s2_05", "Let's find the shear center of a channel, step by step. The web has height h, each flange has "
                  "width b, and the thickness t is uniform. The x axis is an axis of symmetry, so I x y is zero, "
                  "and S lies on the x axis. We just need its horizontal position."),
        ("s2_06", "First, I x x. The web contributes t h cubed over twelve. Each flange is a strip of area b t, a "
                  "distance h over two from the axis, so each contributes b t times h squared over four. Adding "
                  "them gives t h cubed over twelve, times one plus six b over h."),
        ("s2_07", "Apply S y through the shear center. With only S y and I x y zero, the shear flow is minus S y "
                  "over I x x, times the integral of t y d s. Start at the free end of the bottom flange, point "
                  "one, where q is zero."),
        ("s2_08", "Along the bottom flange, y is constant, minus h over two. The integral is just minus h over "
                  "two, times t, times s one. So the shear flow grows linearly: q one two equals six S y s one, "
                  "over h squared times one plus six b over h."),
        ("s2_09", "At the corner, point two, s one equals b, so q two equals six S y b over h squared times one "
                  "plus six b over h. That value carries over into the web."),
        ("s2_10", "Along the web, y changes from minus h over two to plus h over two, so the integral gives a "
                  "parabola, added on top of q two. It peaks at the neutral axis. In the top flange, the shear "
                  "flow falls linearly back to zero at the free end. A good check."),
        ("s2_11", "Now the shear center. Take moments about the middle of the web. The web's shear force passes "
                  "right through that point, so it has no moment. Only the two flange forces matter."),
        ("s2_12", "Each flange carries a total force F, the area under its triangle: one half, times b, times q "
                  "two. The bottom flange force points toward the web, and the top flange force points away from "
                  "it. Together they form a couple, F times h, trying to twist the section."),
        ("s2_13", "For no twist, the load must produce an equal and opposite moment. So S y times the distance "
                  "e, to the left of the web, equals F times h. Substituting F, the distance is three b squared "
                  "over h plus six b. The shear center sits outside the channel, on the far side of the web."),
        ("s2_14", "That's the whole method for any open section. Find the shear flow due to a load. Take moments "
                  "about a clever point, where many walls pass through, so their forces drop out. Then set the "
                  "moment of the load equal to the moment of the shear flows."),
    ],
    # -------------------------------------------------- S3: HW 3 problem 1
    "S3Problem": [
        ("s3_01", "Now let's apply everything to problem one of homework three. We need to show that the shear "
                  "center of this section sits at xi s equals minus forty five a over ninety seven, and eta s "
                  "equals forty six a over ninety seven, measured from the corner where the web meets the lower "
                  "flange."),
        ("s3_02", "First, read the drawing carefully. The bottom flange has length two a and thickness t. The web "
                  "has height two a, and the top flange has length a. The web and the top flange are both drawn "
                  "thick: their thickness is two t. Getting this right matters. With any other thicknesses, you "
                  "won't get forty five over ninety seven."),
        ("s3_03", "This section has no axis of symmetry, so I x y won't be zero, and the shear center needs both "
                  "coordinates. We'll put the origin at the corner, with x to the right and y up."),
        ("s3_04", "Step one: the centroid. The bottom flange has area two a t, the web has area four a t, and the "
                  "top flange has area two a t. Eight a t in total."),
        ("s3_05", "x bar is the sum of each area times its center's x position, divided by eight a t. That's two "
                  "a t times a, plus four a t times zero, plus two a t times a over two, all over eight a t: "
                  "three a over eight. In the same way, y bar comes out to exactly a."),
        ("s3_06", "Step two: second moments of area about the centroid. For I x x, the flanges are each a "
                  "distance a from the centroid, so each gives two a t times a squared. The web gives two t times "
                  "two a cubed, over twelve. The total is sixteen a cubed t over three."),
        ("s3_07", "For I y y, each flange contributes its own t times length cubed over twelve, plus its area "
                  "times its offset squared, and the web contributes only its area times its offset squared. The "
                  "total is fifty three a cubed t over twenty four."),
        ("s3_08", "For I x y, each wall contributes its area times its x offset times its y offset. The bottom "
                  "flange gives minus five quarters a cubed t, the web gives zero, and the top flange gives plus "
                  "one quarter. So I x y is minus a cubed t."),
        ("s3_09", "We'll need the denominator, I x x I y y minus I x y squared. That's sixteen thirds times fifty "
                  "three twenty fourths, minus one, all times a to the sixth t squared. It simplifies to ninety "
                  "seven ninths. There's our ninety seven!"),
        ("s3_10", "Step three: a clever moment center. Take moments about the corner itself. Both the bottom "
                  "flange and the web pass through the corner, so their forces have no moment about it. Only the "
                  "top flange matters, with a moment arm of two a. So for each load case, all we need is the "
                  "total force in the top flange."),
        ("s3_11", "Load case one: S y alone, to find xi s. With S x equal to zero, the general formula becomes "
                  "this. Plugging in our numbers, q equals minus nine S y over ninety seven a cubed t, times the "
                  "quantity, integral of t x d s, plus fifty three over twenty four times integral of t y d s."),
        ("s3_12", "Start at the free end of the bottom flange, where q is zero. Along it, x is thirteen a over "
                  "eight minus s, and y is minus a. Integrating gives q one two equals three S y s times seven a "
                  "plus six s, over three hundred eighty eight a cubed. At the corner, that's fifty seven S y over "
                  "one hundred ninety four a."),
        ("s3_13", "Up the web, x is minus three a over eight, y is minus a plus s, and the thickness is two t. "
                  "Integrating and adding the corner value, the shear flow reaches forty two S y over ninety seven "
                  "a at the top of the web."),
        ("s3_14", "Along the top flange, starting with forty two over ninety seven, the shear flow is S y times "
                  "forty two a squared minus thirty three a s minus nine s squared, over ninety seven a cubed. At "
                  "the free end, s equals a, this is exactly zero. That's our check."),
        ("s3_15", "The total top flange force is the integral of that shear flow from zero to a: forty two minus "
                  "sixteen and a half minus three, giving twenty two and a half S y over ninety seven, which is "
                  "forty five S y over one hundred ninety four, pointing to the right."),
        ("s3_16", "Now balance moments about the corner. The top flange force, to the right, at height two a, "
                  "gives a clockwise moment of two a times forty five S y over one hundred ninety four. The load S "
                  "y at position xi s gives a moment of xi s times S y. Setting them equal, xi s is minus forty "
                  "five a over ninety seven. The shear center is to the left of the web."),
        ("s3_17", "Load case two: S x alone, to find eta s. Now the formula becomes minus nine S x over ninety "
                  "seven a cubed t, times sixteen thirds integral of t x d s, plus integral of t y d s."),
        ("s3_18", "Working wall by wall in exactly the same way, the shear flow is minus forty two S x over ninety "
                  "seven a at the corner, thirty S x over ninety seven a at the top of the web, and in the top "
                  "flange it's S x times thirty a squared plus eighteen a s minus forty eight s squared, over "
                  "ninety seven a cubed. Again, zero at the free end."),
        ("s3_19", "The top flange force is thirty plus nine minus sixteen, so twenty three S x over ninety seven. "
                  "Its moment about the corner is two a times that. The load S x, acting at height eta s, has "
                  "moment eta s times S x. Setting them equal, eta s is forty six a over ninety seven."),
        ("s3_20", "So the shear center is at minus forty five a over ninety seven, forty six a over ninety seven, "
                  "exactly as the problem asked us to show. Notice the strategy that made this manageable: a "
                  "moment center where two of the three walls drop out."),
    ],
    # --------------------------------------------- S4: closed sections
    "S4Concept": [
        ("s4_01", "So far, every section has been open, with free edges where the shear flow is zero. In this "
                  "lesson, we'll handle closed sections, like a wing box or a tube, where there are no free "
                  "edges."),
        ("s4_02", "The equilibrium equation is exactly the same, and so is the integral. The difference is the "
                  "starting value. On a closed loop, there's no point where we know the shear flow is zero. So we "
                  "write the shear flow at the origin as an unknown constant, q s zero."),
        ("s4_03", "Here's the trick. Imagine cutting the wall at the origin. Now the section is open, and we can "
                  "compute its shear flow exactly as before. We call that the basic shear flow, q b. The real "
                  "shear flow is q b, plus a constant q s zero that flows all the way around the loop."),
        ("s4_04", "To find q s zero, we use moments. The applied loads' moment about any point must equal the "
                  "moment of the shear flow. Each little piece of shear flow, q d s, has a moment arm p, the "
                  "perpendicular distance from the moment center to the wall."),
        ("s4_05", "Now a beautiful piece of geometry. The little triangle from the moment center to the wall "
                  "segment d s has area one half p d s. So going all the way around the loop, the integral of p d "
                  "s is twice the enclosed area, two A."),
        ("s4_06", "That means a constant shear flow q s zero produces a moment of exactly two A times q s zero. So "
                  "the moment equation becomes: applied moment equals the integral of p q b d s, plus two A q s "
                  "zero. If we choose the moment center on the line of action of the load, the applied moment is "
                  "zero, and q s zero is minus the integral of p q b d s, over two A."),
        ("s4_07", "Closed sections also twist. Using the shear strain and the displacements of the wall, the rate "
                  "of twist turns out to be one over two A, times the loop integral of q over G t, d s."),
        ("s4_08", "This gives us the shear center of a closed section. A load through the shear center produces "
                  "no twist, so that loop integral must be zero. If G t is constant around the section, this "
                  "means q s zero equals minus the loop integral of q b, divided by the total perimeter."),
        ("s4_09", "So we have two ways to find q s zero. If the load's line of action is known, use moments about "
                  "a point on it. If you're looking for the shear center, use the zero twist condition, then take "
                  "moments to locate S."),
        ("s4_10", "And here's the recipe for closed sections. One: find I x x, and the others if needed. Two: cut "
                  "the section somewhere convenient, and compute q b as if it were open. Three: find q s zero from "
                  "moments, or from zero twist. Four: add them, q equals q b plus q s zero, and check that the "
                  "flows add up to the applied load."),
    ],
    # -------------------------------------------- S5: HW 3 problem 2
    "S5Problem": [
        ("s5_01", "Problem two of homework three: a thin walled isosceles triangle, with uniform thickness t, and "
                  "a vertical shear force S y applied at the apex, point one. We need the shear flow distribution, "
                  "with directions and principal values. And for extra credit, we need I x x."),
        ("s5_02", "Let's set up the geometry. The vertical wall, from point two to point three, has height h. The "
                  "two sloping walls each have length d, and meet at the apex. The section is symmetric about the "
                  "horizontal x axis, so I x y is zero, and the centroid lies on that axis."),
        ("s5_03", "Extra credit first: I x x. Along a sloping wall, y grows linearly from zero at the apex to h "
                  "over two at the far corner. So y equals h s over two d. Then the wall's contribution is the "
                  "integral of t y squared d s, from zero to d."),
        ("s5_04", "That integral is t, times h squared over four d squared, times d cubed over three, which "
                  "simplifies to d t h squared over twelve. There are two sloping walls."),
        ("s5_05", "The vertical wall is just a rectangle of height h, centered on the axis: t h cubed over twelve. "
                  "Adding everything, I x x equals two times d t h squared over twelve, plus t h cubed over "
                  "twelve. That's the extra credit result."),
        ("s5_06", "Now the shear flow. This is a closed section, so we cut it. Since the load acts at the apex, "
                  "let's cut there, at point one, and go around: one to two, two to three, three back to one. "
                  "With only S y and I x y zero, q b equals minus S y over I x x, times the integral of t y d s."),
        ("s5_07", "Wall one to two. Going down the lower wall, y is minus h s over two d. Integrating, q b equals S "
                  "y t h over four d I x x, times s squared. At point two, it reaches S y t h d over four I x x."),
        ("s5_08", "Wall two to three. Going up, y is minus h over two plus s. The integral gives minus S y t over "
                  "I x x, times minus h s over two plus s squared over two, added to the value at point two. At "
                  "point three, the integral term is exactly zero, so q b at three equals q b at two."),
        ("s5_09", "Wall three to one. Coming back down to the apex, the basic shear flow returns to exactly zero "
                  "at the cut. That's a good sign our integrals are right."),
        ("s5_10", "Now q s zero. The load passes through the apex, so take moments about the apex: the applied "
                  "moment is zero. And here's the clever part: both sloping walls pass through the apex, so they "
                  "have no moment arm. Only the vertical wall matters, with arm L, the horizontal distance from "
                  "the apex to that wall."),
        ("s5_11", "The moment equation becomes L times the integral of q b over the vertical wall, plus two A q s "
                  "zero, equals zero. The enclosed area is one half L h, so two A equals L h. The L cancels, and q "
                  "s zero is minus the average of q b along the vertical wall."),
        ("s5_12", "Computing that average and substituting I x x, we get q s zero equals minus S y times three d "
                  "plus h, over h times two d plus h."),
        ("s5_13", "Adding q b and q s zero gives the final shear flow. In the sloping walls, it's S y times three s "
                  "squared minus three d squared minus d h, over d h times two d plus h. In the vertical wall, it's "
                  "minus S y times h squared minus six h s plus six s squared, over h squared times two d plus h."),
        ("s5_14", "The principal values. At the apex, the shear flow is S y times three d plus h, over h times two "
                  "d plus h. At corners two and three, it's S y over two d plus h. And in the middle of the "
                  "vertical wall, it's half of that, S y over two times two d plus h."),
        ("s5_15", "Now the directions. A negative value means the flow runs against our s direction. In the lower "
                  "wall, the shear flow runs up toward the apex. In the upper wall, it runs up away from the apex. "
                  "In the vertical wall, it runs downward near the corners and upward in the middle, changing sign "
                  "at about twenty one and seventy nine percent of the height."),
        ("s5_16", "Finally, the checks. The horizontal components of the two sloping walls cancel. The vertical "
                  "components add up to exactly S y. And the total moment about the apex is zero, as it must be. "
                  "The distribution is complete."),
        ("s5_17", "Let's recap the whole series. Shear flow comes from the change in bending stress along the "
                  "beam. In open sections, start from a free edge. The shear center is where loads cause no twist, "
                  "found by balancing moments. And in closed sections, cut, compute the basic flow, and add a "
                  "constant found from moments or from zero twist."),
    ],
}

SCENE_ORDER = list(SCRIPT.keys())


def all_segments():
    for scene in SCENE_ORDER:
        for seg_id, text in SCRIPT[scene]:
            yield scene, seg_id, text
