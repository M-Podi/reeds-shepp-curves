import turtle
import reeds_shepp as rs
import draw
import itertools


def path_distance(p1, p2):
    """
    Calculate the Reeds-Shepp path length between two waypoints.
    """
    path = rs.get_optimal_path(p1, p2)
    return rs.path_length(path)


def solve_tsp(waypoints, method='exact'):
    """
    Solve the traveling salesman problem for the waypoints.

    Args:
        waypoints: List of (x, y, theta) tuples.
        method: 'exact' or 'greedy'. Exact is only practical for small sets of waypoints.

    Returns:
        Ordered list of waypoints and the total path length.
    """
    n = len(waypoints)
    if n <= 1:
        return waypoints, 0

    if method == 'exact':  # Exact is feasible for small n
        # Try all permutations
        best_order = None
        best_length = float('inf')

        for perm in itertools.permutations(range(n)):
            length = 0
            for i in range(n - 1):
                length += path_distance(waypoints[perm[i]], waypoints[perm[i + 1]])
            # Add return to start for a complete loop
            length += path_distance(waypoints[perm[n - 1]], waypoints[perm[0]])

            if length < best_length:
                best_length = length
                best_order = perm

        ordered = [waypoints[i] for i in best_order]
        ordered.append(ordered[0])  # Close the loop
        return ordered, best_length

    else:  # Use greedy algorithm
        # Start with the first waypoint
        current = 0
        ordered_indices = [current]
        unvisited = set(range(1, n))
        total_length = 0

        while unvisited:
            nearest = min(unvisited, key=lambda x: path_distance(waypoints[current], waypoints[x]))
            unvisited.remove(nearest)
            total_length += path_distance(waypoints[current], waypoints[nearest])
            current = nearest
            ordered_indices.append(current)

        # Complete the tour back to start
        total_length += path_distance(waypoints[ordered_indices[-1]], waypoints[ordered_indices[0]])

        ordered = [waypoints[i] for i in ordered_indices]
        ordered.append(ordered[0])  # Close the loop
        return ordered, total_length


def scale_waypoints(waypoints, radius):
    """
    Scale waypoints to simulate a different turning radius.

    Args:
        waypoints: List of (x, y, theta) tuples.
        radius: The desired turning radius (1 is the default in Reeds-Shepp).

    Returns:
        Scaled waypoints.
    """
    scaled = []
    for x, y, theta in waypoints:
        scaled.append((x / radius, y / radius, theta))
    return scaled


def read_waypoints_from_file(file_path):
    """
    Read waypoints from a file.

    Args:
        file_path: Path to the file containing waypoints.

    Returns:
        List of (x, y, theta) tuples.
    """
    waypoints = []
    with open(file_path, 'r') as file:
        for line in file:
            # Parse each line as x, y, theta
            parts = line.strip().split(',')
            if len(parts) == 3:
                x, y, theta = map(float, parts)
                waypoints.append((x, y, theta))
    return waypoints


def main():
    # Read waypoints from a file
    file_path = 'waypoints.txt'  # Replace with your file path
    waypoints = read_waypoints_from_file(file_path)

    if not waypoints:
        print("No waypoints found in the file.")
        return

    # Find optimal order of waypoints
    print("Solving TSP for optimal waypoint order...")
    ordered_waypoints, total_length = solve_tsp(waypoints, method='exact')
    print(f"Optimal path length with unit turning radius: {total_length:.2f}")

    # Setup the window
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.title("Reeds-Shepp Trajectories with Different Turning Radii")

    # Different radius values and colors
    radii = [0.5, 1.0, 2.0]
    colors = [(1, 0, 0), (0, 0.7, 0), (0, 0, 1)]  # Red, Green, Blue

    # Initialize turtle for drawing waypoints
    waypoint_turtle = turtle.Turtle()
    waypoint_turtle.speed(0)
    waypoint_turtle.shape('arrow')
    waypoint_turtle.resizemode('user')
    waypoint_turtle.shapesize(1, 1)

    # Draw waypoints (using the unscaled coordinates)
    for wp in ordered_waypoints[:-1]:  # Don't draw the last one (it's the same as the first)
        draw.goto(waypoint_turtle, wp)
        draw.vec(waypoint_turtle)

    # Add a legend
    legend = turtle.Turtle()
    legend.hideturtle()
    legend.penup()
    legend.goto(-350, 250)
    legend.write("Turning Radii:", font=("Arial", 14, "normal"))

    for i, (radius, color) in enumerate(zip(radii, colors)):
        legend.pencolor(color)
        legend.goto(-330, 230 - i * 20)
        legend.write(f"Radius {radius}", font=("Arial", 12, "normal"))

    # Draw paths for each radius
    for radius, color in zip(radii, colors):
        # Scale waypoints for this radius
        scaled_waypoints = scale_waypoints(ordered_waypoints, radius)

        # Initialize turtle for this radius
        tesla = turtle.Turtle()
        tesla.speed(0)
        tesla.pencolor(color)
        tesla.pensize(2)

        # Draw path
        draw.goto(tesla, scaled_waypoints[0])

        path_length = 0
        for i in range(len(scaled_waypoints) - 1):
            path = rs.get_optimal_path(scaled_waypoints[i], scaled_waypoints[i + 1])
            path_length += rs.path_length(path)
            draw.draw_path(tesla, path)

        # Scale the path length back to the original units
        scaled_length = path_length * radius
        print(f"Path length with turning radius {radius}: {scaled_length:.2f}")

    turtle.done()


if __name__ == '__main__':
    main()