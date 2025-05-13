
from utils import *
import reeds_shepp as rs
import random as rd
import turtle # Ensure turtle is imported if not already

# drawing n units (eg turtle.forward(n)) will draw n * SCALE pixels
SCALE = 40

def scale(x):
    """
    Scale the input coordinate(s) or distance by the global SCALE factor.
    Maps world units to pixel units.
    """
    if isinstance(x, (tuple, list)):
        return [p * SCALE for p in x]
    # Handle potential None or non-numeric types gracefully if needed,
    # but assuming numeric input based on usage.
    try:
        return x * SCALE
    except TypeError:
        print(f"Warning: scale() received non-numeric type: {type(x)}, value: {x}")
        return 0 # Or raise error, or return None


def unscale(x):
    """
    Unscale the input coordinate(s) or pixel distance.
    Maps pixel units back to world units.
    """
    if SCALE == 0:
         raise ValueError("draw.SCALE cannot be zero for unscale operation.")
    if isinstance(x, (tuple, list)):
        return [p / SCALE for p in x]
    try:
        return x / SCALE
    except TypeError:
        print(f"Warning: unscale() received non-numeric type: {type(x)}, value: {x}")
        return 0 # Or raise error, or return None


# note: bob is a turtle

def vec(bob):
    """
    Draw an arrow indicating position and heading.
    Arrow size is relative to SCALE.
    """
    arrow_len = scale(0.6) # Base length in pixels
    arrow_width_angle = 25
    arrow_back_dist = scale(0.2) # Back part length in pixels

    original_pen = bob.pen() # Store original pen state
    bob.pendown()
    bob.pensize(max(1, SCALE / 20)) # Make pensize slightly dependent on scale
    bob.pencolor('black') # Ensure consistent color

    # bob.forward(scale(1.2)) # Original fixed size
    bob.forward(arrow_len)
    bob.right(arrow_width_angle)
    # bob.backward(scale(.4))
    bob.backward(arrow_back_dist)
    bob.forward(arrow_back_dist)
    bob.left(arrow_width_angle * 2)
    # bob.backward(scale(.4))
    bob.backward(arrow_back_dist)
    bob.forward(arrow_back_dist)
    bob.right(arrow_width_angle) # Return to original heading

    # bob.pensize(1) # Original fixed size
    bob.penup()
    bob.pen(original_pen) # Restore original pen state (color, size, up/down)


def goto(bob, pos, scale_pos=True):
    """
    Go to a position (x, y, heading_degrees) without drawing.
    Assumes 'pos' contains (x, y, theta_degrees).
    If scale_pos is True, input x, y are world coordinates and are scaled.
    If scale_pos is False, input x, y are already pixel coordinates.
    """
    bob.penup() # Ensure not drawing while moving
    if scale_pos:
        # Scale only the x, y coordinates
        pixel_pos = scale(pos[:2])
        bob.setpos(pixel_pos[0], pixel_pos[1])
    else:
        # Assume pos[:2] are already pixel coordinates
        bob.setpos(pos[0], pos[1])

    # Set heading (expects degrees)
    if len(pos) > 2 and pos[2] is not None:
        bob.setheading(pos[2])
    # bob.pendown() # Decide in the calling code whether to draw after goto

# --- MODIFIED draw_path ---
def draw_path(bob: turtle.Turtle, path: list[rs.PathElement], radius: float = 1.0):
    """
    Draw the path (list of rs.PathElements) using the specified turning radius.

    Args:
        bob: The turtle object to draw with.
        path: A list of PathElement objects from reeds_shepp.py.
        radius: The turning radius the path corresponds to in world units.
    """
    if not isinstance(bob, turtle.Turtle):
        raise TypeError("bob must be a turtle.Turtle object")
    if radius <= 0:
        raise ValueError("radius must be positive")

    # Ensure turtle starts drawing if it wasn't already
    bob.pendown()

    for e in path:
        # PathElement param is the length/angle in the scaled RS world (where radius=1)
        # We need to convert this back to world units and then scale to pixels.
        gear = 1 if e.gear == rs.Gear.FORWARD else -1
        angle_degrees = rad2deg(e.param) # Angle remains the same regardless of radius
        world_length = e.param * radius # World length scales with radius

        # Calculate screen coordinates based on world radius and length
        screen_radius = scale(radius)
        screen_length = scale(world_length)

        if e.steering == rs.Steering.LEFT:
            # turtle.circle(radius, extent=angle)
            # Positive radius makes turtle turn left.
            bob.circle(screen_radius, gear * angle_degrees)
        elif e.steering == rs.Steering.RIGHT:
            # Negative radius makes turtle turn right.
            bob.circle(-screen_radius, gear * angle_degrees)
        elif e.steering == rs.Steering.STRAIGHT:
            # Forward distance depends on gear and calculated screen length
            bob.forward(gear * screen_length)


def set_random_pencolor(bob):
    """
    Sets the turtle's pen color to a random, reasonably bright color.
    """
    r, g, b = 1, 1, 1
    # Ensure the color is not too close to white (sum > 2.5)
    # and not too close to black (sum < 0.5) for visibility.
    while (r + g + b > 2.5) or (r + g + b < 0.5) :
        r, g, b = rd.uniform(0, 1), rd.uniform(0, 1), rd.uniform(0, 1)
    bob.pencolor(r, g, b)
