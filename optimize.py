# --- START OF FILE optimize.py (Modified for Animation) ---

import turtle
import reeds_shepp as rs
import draw  # Assumes draw.py is modified as described previously
import itertools


# Function to calculate Reeds-Shepp distance between two points *using a specific radius*
def path_distance(p1, p2, radius=1.0):
    """
    Calculate the Reeds-Shepp path length between two waypoints
    using a specific turning radius.
    """
    # Scale points for Reeds-Shepp calculation (which assumes radius 1)
    sp1 = (p1[0] / radius, p1[1] / radius, p1[2])
    sp2 = (p2[0] / radius, p2[1] / radius, p2[2])
    path = rs.get_optimal_path(sp1, sp2)
    return rs.path_length(path) * radius


def solve_tsp(waypoints, radius=1.0, method='exact'):

    n = len(waypoints)
    if n <= 1:
        return waypoints, 0

    # Calculate distances using the specified radius
    dist_func = lambda p_i, p_j: path_distance(waypoints[p_i], waypoints[p_j], radius)

    if method == 'exact' and n < 10:  # Add a reasonable limit for exact TSP
        # Try all permutations starting from waypoint 0
        best_order_indices = None
        best_length = float('inf')

        # Iterate through permutations of points *other than* the start point (index 0)
        other_points = list(range(1, n))
        for perm_indices in itertools.permutations(other_points):
            current_order_indices = [0] + list(perm_indices) # Start at 0
            current_length = 0
            for i in range(n - 1):
                current_length += dist_func(current_order_indices[i], current_order_indices[i + 1])
            # Add return to start for a complete loop
            current_length += dist_func(current_order_indices[n - 1], current_order_indices[0])

            if current_length < best_length:
                best_length = current_length
                best_order_indices = current_order_indices

        if best_order_indices is None: # Handle case n=1 or n=2 if permutations loop doesn't run
             if n == 1:
                 best_order_indices = [0]
                 best_length = 0
             elif n==2:
                 best_order_indices = [0, 1]
                 best_length = dist_func(0, 1) + dist_func(1, 0) # Loop distance
             else: # Should not happen if n > 0 and method=='exact'
                 print("Warning: Could not find exact TSP solution.")
                 return solve_tsp(waypoints, radius, method='greedy') # Fallback


        ordered = [waypoints[i] for i in best_order_indices]
        ordered.append(ordered[0])  # Close the loop
        return ordered, best_length

    else:  # Use greedy algorithm
        if method == 'exact':
            print(f"Warning: Too many waypoints ({n}) for exact TSP. Using greedy method.")

        current_index = 0
        ordered_indices = [current_index]
        unvisited = set(range(1, n))
        total_length = 0

        while unvisited:
            # Find nearest unvisited waypoint from the current one
            nearest_index = min(unvisited, key=lambda next_idx: dist_func(current_index, next_idx))

            unvisited.remove(nearest_index)
            total_length += dist_func(current_index, nearest_index)
            current_index = nearest_index
            ordered_indices.append(current_index)

        # Complete the tour back to start
        total_length += path_distance(waypoints[ordered_indices[-1]], waypoints[ordered_indices[0]], radius) # Use radius here too

        ordered = [waypoints[i] for i in ordered_indices]
        ordered.append(ordered[0])  # Close the loop
        return ordered, total_length


# scale_waypoints remains the same - it's needed for the RS calculation
def scale_waypoints(waypoints, radius):
    """
    Scale waypoints for Reeds-Shepp calculations (which assume radius 1).

    Args:
        waypoints: List of (x, y, theta) tuples (original coordinates).
        radius: The desired turning radius.

    Returns:
        Waypoints scaled for RS calculation: (x/radius, y/radius, theta).
    """
    scaled = []
    for x, y, theta in waypoints:
        # Ensure radius is not zero to avoid division error
        if radius == 0:
             raise ValueError("Turning radius cannot be zero.")
        scaled.append((x / radius, y / radius, theta))
    return scaled


def read_waypoints_from_file(file_path):
    """
    Read waypoints from a file.

    Args:
        file_path: Path to the file containing waypoints. Each line: x,y,theta

    Returns:
        List of (x, y, theta) tuples.
    """
    waypoints = []
    try:
        with open(file_path, 'r') as file:
            for i, line in enumerate(file):
                line = line.strip()
                if not line or line.startswith('#'): # Skip empty lines and comments
                    continue
                try:
                    parts = line.split(',')
                    if len(parts) == 3:
                        x, y, theta = map(float, parts)
                        waypoints.append((x, y, theta))
                    else:
                         print(f"Warning: Skipping malformed line {i+1} in {file_path}: '{line}'")
                except ValueError:
                     print(f"Warning: Skipping non-numeric data on line {i+1} in {file_path}: '{line}'")
    except FileNotFoundError:
        print(f"Error: Waypoint file not found at '{file_path}'")
    return waypoints


def main():
    # Read waypoints from a file
    file_path = 'waypoints.txt'  # Make sure this file exists and is formatted correctly
    original_waypoints = read_waypoints_from_file(file_path)


    # --- TSP Calculation ---
    tsp_radius = 1.0
    print(f"Solving TSP for optimal waypoint order (based on radius={tsp_radius})...")
    ordered_waypoints, _ = solve_tsp(original_waypoints, radius=tsp_radius, method='exact')
    print("Waypoint order determined.")

    # --- Drawing Setup ---
    screen = turtle.Screen()
    max_coord = 0
    if ordered_waypoints:
       max_coord = max(abs(c) for wp in ordered_waypoints for c in wp[:2]) + 5
    screen_size = max(600, int(draw.SCALE * max_coord * 1.1) * 2)
    screen.setup(screen_size, screen_size)
    coord_range = max(10, max_coord*30)
    screen.setworldcoordinates(-coord_range, -coord_range, coord_range, coord_range)

    screen.title("Reeds-Shepp Trajectories with Different Turning Radii")

    radii = [0.5, 1.0, 2.0, 3.0]
    colors = [(1, 0, 0), (0, 0.7, 0), (0, 0, 1), (1, 0.6, 0)]

    # --- Draw Waypoints ---
    # Use a separate turtle for waypoints so its speed doesn't affect path drawing
    waypoint_turtle = turtle.Turtle()
    waypoint_turtle.hideturtle() # Hide during setup
    waypoint_turtle.penup()
    waypoint_turtle.speed(0) # Draw waypoints quickly
    waypoint_turtle.shape('arrow')
    waypoint_turtle.color('black') # Make waypoints distinct
    waypoint_turtle.resizemode('user')
    waypoint_turtle.shapesize(0.8 / draw.SCALE * 40, 0.8 / draw.SCALE * 40) # Adjust size based on draw.SCALE

    print("Drawing waypoints...")
    # Draw waypoints using the *ordered* sequence (excluding the closing loop point)
    for wp in ordered_waypoints[:-1]:
        draw.goto(waypoint_turtle, wp) # goto uses original coords
        waypoint_turtle.showturtle() # Show for drawing vector
        draw.vec(waypoint_turtle)
        waypoint_turtle.hideturtle() # Hide again after drawing
    # Waypoint turtle is now hidden and done

    # --- Add Legend ---
    legend = turtle.Turtle()
    legend.hideturtle()
    legend.penup()
    # Position legend dynamically based on screen coordinates
    lx, ly = screen.window_width() / -2 + 50, screen.window_height() / 2 - 50
    screen_coords_lx = lx / screen.window_width() * 2 * coord_range
    screen_coords_ly = ly / screen.window_height() * 2 * coord_range
    legend.goto(screen_coords_lx, screen_coords_ly) # Use world coordinates for positioning
    legend.write("Turning Radii:", font=("Arial", 14, "normal"), align="left")

    for i, (radius, color) in enumerate(zip(radii, colors)):
        legend.pencolor(color)
        legend.goto(screen_coords_lx + (20 / screen.window_width() * 2 * coord_range), # Adjust offset based on world coords
                     screen_coords_ly - ((20 + i * 20) / screen.window_height() * 2 * coord_range))
        legend.write(f"Radius {radius:.1f}", font=("Arial", 12, "normal"), align="left")

    # --- Draw Paths for Each Radius ---
    print("Drawing paths for different radii...")
    for radius, color in zip(radii, colors):
        print(f"  Calculating and drawing for radius = {radius:.1f}")
        # Scale waypoints for *this specific radius* for RS calculation
        scaled_waypoints_for_radius = scale_waypoints(ordered_waypoints, radius)

        # Initialize turtle for this radius' path
        tesla = turtle.Turtle()
        tesla.hideturtle()
        tesla.penup()

        tesla.speed(10) # <<< SET DRAWING SPEED HERE (e.g., 10 for fast, 3 for slow)


        tesla.pencolor(color)
        tesla.pensize(2)
        tesla.shape('turtle')
        tesla.resizemode('user')
        tesla.shapesize(0.8 / draw.SCALE * 40, 0.8 / draw.SCALE * 40)


        draw.goto(tesla, ordered_waypoints[0])
        tesla.showturtle() # Show the turtle now
        tesla.pendown() # Start drawing path segments

        total_path_length_scaled_units = 0 # Accumulate length in RS units (radius=1)
        # Iterate through the segments defined by the ORDERED waypoints
        # Use the waypoints scaled for *this* radius for path calculation
        for i in range(len(scaled_waypoints_for_radius) - 1):
            start_wp_scaled = scaled_waypoints_for_radius[i]
            end_wp_scaled = scaled_waypoints_for_radius[i+1]

            # Calculate the optimal RS path between the *scaled* waypoints
            path_segment = rs.get_optimal_path(start_wp_scaled, end_wp_scaled)

            # Accumulate length (path_length is in scaled units where radius=1)
            segment_length_scaled = rs.path_length(path_segment)
            total_path_length_scaled_units += segment_length_scaled

            # Draw the path segment using the *actual radius* for scaling the drawing
            # Assumes draw.draw_path is modified to accept radius
            draw.draw_path(tesla, path_segment, radius=radius)

        # Calculate the total path length in original units
        total_path_length_original_units = total_path_length_scaled_units * radius

        print(f"  Path length for radius {radius:.1f}: {total_path_length_original_units:.2f}")
        tesla.hideturtle() # Hide turtle after finishing this path


    print("Drawing complete.")
    # turtle.update() # <<< REMOVED to restore animation
    turtle.done()


if __name__ == '__main__':
    # Create a dummy waypoints.txt if it doesn't exist, so the script can run initially
    try:
        with open('waypoints.txt', 'x') as f:
            f.write("# Example Waypoints (x,y,theta_degrees)\n")
            f.write("-5,5,90\n")
            f.write("5,5,0\n")
            f.write("5,-5,-90\n")
            f.write("-5,-5,180\n")
        print("Created example waypoint file: waypoints.txt")
        print("Please edit it with your desired waypoints and run the script again.")
    except FileExistsError:
        pass # File already exists, proceed normally

    main()

