# Optimized Reeds-Shepp Trajectories

This project implements optimal path planning for non-holonomic vehicles using Reeds-Shepp curves. It extends the original implementation with trajectory optimization capabilities by solving two key challenges:

1. **Waypoint Order Optimization**: Determines the optimal sequence of waypoints to minimize total path length using the Traveling Salesman Problem (TSP) approach.
2. **Turning Radius Visualization**: Illustrates resulting trajectories for various values of the minimum turning radius.

## Features

- **TSP Optimization**: Automatically finds the optimal waypoint order to minimize the total path length
  - Exact solution for small problems (< 10 waypoints)
  - Greedy nearest-neighbor approach for larger problems
- **Multi-Radius Visualization**: Simultaneously visualizes trajectories with different turning radii
- **Waypoint File Support**: Loads waypoints from a simple CSV-style text file
- **Interactive Animation**: Visualizes the path generation process with Turtle graphics

## Requirements

- Python 3.7+
- `turtle` module (included in standard Python library)

## Usage

1. Create a waypoint file (or use the example one generated automatically):

```
# Format: x,y,theta_degrees
-6,-7,0
-6,0,90
-4,6,45
0,5,30
0,-2,-45
-2,-6,-90
```

2. Run the optimizer:

```
$ python optimize.py
```

3. The script will:
   - Determine optimal waypoint order using TSP
   - Draw waypoints and vectors indicating positions
   - Visualize paths with different turning radii (0.5, 1.0, 2.0, 3.0 by default)
   - Display the total path length for each radius

## Example Output

The visualization shows:
- Black arrows representing waypoints with their orientation
- Colored paths representing trajectories with different turning radii
- A legend indicating which color corresponds to which turning radius value

## Technical Approach

The implementation combines:

1. **Reeds-Shepp Curves**: Optimal paths for a car that can move both forward and backward
2. **TSP Solver**: Finds the best order to visit all waypoints
   - For small sets: Uses exact solution through permutation analysis
   - For larger sets: Uses greedy nearest-neighbor heuristic
3. **Radius Scaling**: Properly scales coordinates and distances based on the turning radius
4. **Turtle Graphics**: Visualizes the resulting paths with animation

## Original Reeds-Shepp Implementation

This project makes use of the Python implementation of Reeds-Shepp from:

https://github.com/nathanlct/reeds-shepp-curves


## Contributors
- **Matei-Alexandru Podeanu** ([contact](mailto:matei-alexandru.podeanu@s.unibuc.ro))
- **Robert Eduard Schmidt** ([contact](mailto:robert-eduard.schmidt@s.unibuc.ro))
