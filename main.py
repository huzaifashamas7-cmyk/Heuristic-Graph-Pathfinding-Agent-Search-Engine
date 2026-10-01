import time
import random
import csv
import os
import matplotlib.pyplot as plt


# ============================================================
# 1. Fixed Test Grid
# ============================================================

grid = [
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)


# ============================================================
# 2. Generate Random Grid
# ============================================================

def generate_grid(rows, cols, obstacle_probability):

    grid = []

    for row in range(rows):

        current_row = []

        for col in range(cols):

            if random.random() < obstacle_probability:
                current_row.append(1)
            else:
                current_row.append(0)

        grid.append(current_row)

    # Start and goal must always be free
    grid[0][0] = 0
    grid[rows - 1][cols - 1] = 0

    return grid


# ============================================================
# 3. Display Grid
# ============================================================

def display_grid(grid, start, goal):

    for row in range(len(grid)):

        for col in range(len(grid[row])):

            if (row, col) == start:
                print("S", end=" ")

            elif (row, col) == goal:
                print("G", end=" ")

            elif grid[row][col] == 0:
                print(".", end=" ")

            else:
                print("#", end=" ")

        print()


# ============================================================
# 4. Get Neighbors
# ============================================================

def get_neighbors(position, grid):

    row, col = position

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    neighbors = []

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):

            if grid[new_row][new_col] == 0:
                neighbors.append((new_row, new_col))

    return neighbors


# ============================================================
# 5. Manhattan Heuristic
# ============================================================

def heuristic(position, goal):

    row, col = position
    goal_row, goal_col = goal

    distance = abs(row - goal_row) + abs(col - goal_col)

    return distance


# ============================================================
# 6. Reconstruct Path
# ============================================================

def reconstruct_path(came_from, current):

    path = [current]

    while current in came_from:

        current = came_from[current]

        path.append(current)

    path.reverse()

    return path


# ============================================================
# 7. A* Search
# ============================================================

def a_star(grid, start, goal):

    open_set = [start]

    came_from = {}

    g_score = {
        start: 0
    }

    expanded_nodes = 0
    expanded_order = []

    while open_set:

        current = open_set[0]

        for node in open_set:

            current_f = g_score[node] + heuristic(node, goal)
            best_f = g_score[current] + heuristic(current, goal)

            if current_f < best_f:
                current = node

        if current == goal:

            path = reconstruct_path(came_from, current)

            return path, expanded_nodes, expanded_order

        open_set.remove(current)

        expanded_nodes += 1
        expanded_order.append(current)

        for neighbor in get_neighbors(current, grid):

            new_g_score = g_score[current] + 1

            if neighbor not in g_score or new_g_score < g_score[neighbor]:

                g_score[neighbor] = new_g_score
                came_from[neighbor] = current

                if neighbor not in open_set:
                    open_set.append(neighbor)

    return None, expanded_nodes, expanded_order


# ============================================================
# 8. Dijkstra Search
# ============================================================

def dijkstra(grid, start, goal):

    open_set = [start]

    came_from = {}

    distance = {
        start: 0
    }

    expanded_nodes = 0
    expanded_order = []

    while open_set:

        current = open_set[0]

        for node in open_set:

            if distance[node] < distance[current]:
                current = node

        if current == goal:

            path = reconstruct_path(came_from, current)

            return path, expanded_nodes, expanded_order

        open_set.remove(current)

        expanded_nodes += 1
        expanded_order.append(current)

        for neighbor in get_neighbors(current, grid):

            new_distance = distance[current] + 1

            if neighbor not in distance or new_distance < distance[neighbor]:

                distance[neighbor] = new_distance
                came_from[neighbor] = current

                if neighbor not in open_set:
                    open_set.append(neighbor)

    return None, expanded_nodes, expanded_order


# ============================================================
# 9. Compare A* and Dijkstra
# ============================================================

def compare_algorithms(grid, start, goal):

    # A* timing
    start_time = time.perf_counter()

    astar_path, astar_expanded, astar_order = a_star(
        grid,
        start,
        goal
    )

    end_time = time.perf_counter()

    astar_runtime = end_time - start_time

    if astar_path is not None:
        astar_steps = len(astar_path) - 1
    else:
        astar_steps = 0

    # Dijkstra timing
    start_time = time.perf_counter()

    dijkstra_path, dijkstra_expanded, dijkstra_order = dijkstra(
        grid,
        start,
        goal
    )

    end_time = time.perf_counter()

    dijkstra_runtime = end_time - start_time

    if dijkstra_path is not None:
        dijkstra_steps = len(dijkstra_path) - 1
    else:
        dijkstra_steps = 0

    return (
        astar_path,
        astar_steps,
        astar_expanded,
        astar_runtime,
        astar_order,

        dijkstra_path,
        dijkstra_steps,
        dijkstra_expanded,
        dijkstra_runtime,
        dijkstra_order
    )


# ============================================================
# 10. Display Path
# ============================================================

def display_path(grid, start, goal, path):

    for row in range(len(grid)):

        for col in range(len(grid[row])):

            position = (row, col)

            if position == start:
                print("S", end=" ")

            elif position == goal:
                print("G", end=" ")

            elif path is not None and position in path:
                print("*", end=" ")

            elif grid[row][col] == 0:
                print(".", end=" ")

            else:
                print("#", end=" ")

        print()


# ============================================================
# 11. Display Search
# ============================================================

def display_search(grid, start, goal, expanded_order, path):

    for row in range(len(grid)):

        for col in range(len(grid[row])):

            position = (row, col)

            if position == start:
                print("S", end=" ")

            elif position == goal:
                print("G", end=" ")

            elif path is not None and position in path:
                print("*", end=" ")

            elif position in expanded_order:
                print("+", end=" ")

            elif grid[row][col] == 0:
                print(".", end=" ")

            else:
                print("#", end=" ")

        print()


# ============================================================
# 12. Save Visualization
# ============================================================

def save_visualization(
    grid,
    start,
    goal,
    path,
    expanded_order,
    filename,
    algorithm_name
):

    rows = len(grid)
    cols = len(grid[0])

    plt.figure(figsize=(8, 8))

    for row in range(rows):

        for col in range(cols):

            position = (row, col)

            if grid[row][col] == 1:

                plt.fill_between(
                    [col, col + 1],
                    row,
                    row + 1
                )

            elif position in expanded_order:

                plt.fill_between(
                    [col, col + 1],
                    row,
                    row + 1
                )

    if path is not None:

        path_rows = []
        path_cols = []

        for row, col in path:

            path_rows.append(row + 0.5)
            path_cols.append(col + 0.5)

        plt.plot(
            path_cols,
            path_rows,
            linewidth=3
        )

    plt.scatter(
        start[1] + 0.5,
        start[0] + 0.5,
        s=100
    )

    plt.scatter(
        goal[1] + 0.5,
        goal[0] + 0.5,
        s=100
    )

    plt.xlim(0, cols)
    plt.ylim(rows, 0)

    plt.xticks(range(cols + 1))
    plt.yticks(range(rows + 1))

    plt.grid(True)

    plt.title(f"{algorithm_name} Pathfinding Visualization")

    plt.savefig(filename)

    plt.close()


# ============================================================
# 13. Initial Fixed-Grid Test
# ============================================================

display_grid(grid, start, goal)

print("\nNeighbors of Start:")

neighbors = get_neighbors(start, grid)

print(neighbors)

print("\nHeuristic Values:")

print("Start:", heuristic(start, goal))
print("(1, 2):", heuristic((1, 2), goal))
print("(3, 4):", heuristic((3, 4), goal))


# ============================================================
# 14. Dijkstra Test
# ============================================================

dijkstra_path, dijkstra_expanded, dijkstra_order = dijkstra(
    grid,
    start,
    goal
)

print("\nDijkstra Path:")

if dijkstra_path is not None:
    print(dijkstra_path)
else:
    print("No path found.")

print("\nDijkstra Step Count:")

if dijkstra_path is not None:
    print(len(dijkstra_path) - 1)
else:
    print("N/A")

print("\nDijkstra Expanded Nodes:")
print(dijkstra_expanded)

print("\nDijkstra Expanded Order:")
print(dijkstra_order)


# ============================================================
# 15. A* vs Dijkstra Test
# ============================================================

comparison = compare_algorithms(
    grid,
    start,
    goal
)

print("\nA* vs Dijkstra Comparison")

print("\nA*:")
print("Steps:", comparison[1])
print("Expanded Nodes:", comparison[2])
print("Runtime:", comparison[3], "seconds")

print("\nDijkstra:")
print("Steps:", comparison[6])
print("Expanded Nodes:", comparison[7])
print("Runtime:", comparison[8], "seconds")


# ============================================================
# 16. Initial A* Metrics
# ============================================================

start_time = time.perf_counter()

path, expanded_nodes, expanded_order = a_star(
    grid,
    start,
    goal
)

end_time = time.perf_counter()

runtime = end_time - start_time

if path is not None:
    step_count = len(path) - 1
else:
    step_count = 0

total_free_cells = 0

for row in grid:

    for cell in row:

        if cell == 0:
            total_free_cells += 1

if total_free_cells > 0:

    expanded_density = (
        expanded_nodes / total_free_cells
    ) * 100

else:

    expanded_density = 0

print("\nInitial A* Metrics:")
print("Steps:", step_count)
print("Expanded Nodes:", expanded_nodes)
print("Runtime:", runtime, "seconds")
print("Expanded Node Density:", expanded_density, "%")


# ============================================================
# 17. Grid Size Experiments
# ============================================================

print("\nGrid Size Experiments:")

grid_sizes = [
    (5, 5),
    (10, 10),
    (20, 20),
    (30, 30)
]

obstacle_probabilities = [
    0.10,
    0.20,
    0.30
]

os.makedirs("visualizations", exist_ok=True)
os.makedirs("results", exist_ok=True)

results = []


# ============================================================
# 18. Run Experiments
# ============================================================

for rows, cols in grid_sizes:

    for obstacle_probability in obstacle_probabilities:

        # Generate ONE grid for this experiment.
        # Both algorithms use this same grid.
        experiment_grid = generate_grid(
            rows,
            cols,
            obstacle_probability
        )

        start = (0, 0)
        goal = (rows - 1, cols - 1)

        # ----------------------------------------------------
        # A* Search
        # ----------------------------------------------------

        start_time = time.perf_counter()

        astar_path, astar_expanded, astar_order = a_star(
            experiment_grid,
            start,
            goal
        )

        end_time = time.perf_counter()

        astar_runtime = end_time - start_time

        if astar_path is not None:
            astar_steps = len(astar_path) - 1
        else:
            astar_steps = 0

        # ----------------------------------------------------
        # Dijkstra Search
        # ----------------------------------------------------

        start_time = time.perf_counter()

        dijkstra_path, dijkstra_expanded, dijkstra_order = dijkstra(
            experiment_grid,
            start,
            goal
        )

        end_time = time.perf_counter()

        dijkstra_runtime = end_time - start_time

        if dijkstra_path is not None:
            dijkstra_steps = len(dijkstra_path) - 1
        else:
            dijkstra_steps = 0

        # ----------------------------------------------------
        # Count Free Cells
        # ----------------------------------------------------

        total_free_cells = 0

        for row in experiment_grid:

            for cell in row:

                if cell == 0:
                    total_free_cells += 1

        # ----------------------------------------------------
        # Expanded Node Density
        # ----------------------------------------------------

        if total_free_cells > 0:

            astar_density = (
                astar_expanded / total_free_cells
            ) * 100

            dijkstra_density = (
                dijkstra_expanded / total_free_cells
            ) * 100

        else:

            astar_density = 0
            dijkstra_density = 0

        # ----------------------------------------------------
        # Store A* Result
        # ----------------------------------------------------

        results.append({

            "algorithm": "A*",

            "grid_size": f"{rows}x{cols}",

            "obstacle_density": obstacle_probability,

            "path_found": astar_path is not None,

            "step_count": astar_steps,

            "expanded_nodes": astar_expanded,

            "runtime": astar_runtime,

            "expanded_node_density": astar_density
        })

        # ----------------------------------------------------
        # Store Dijkstra Result
        # ----------------------------------------------------

        results.append({

            "algorithm": "Dijkstra",

            "grid_size": f"{rows}x{cols}",

            "obstacle_density": obstacle_probability,

            "path_found": dijkstra_path is not None,

            "step_count": dijkstra_steps,

            "expanded_nodes": dijkstra_expanded,

            "runtime": dijkstra_runtime,

            "expanded_node_density": dijkstra_density
        })

        # ----------------------------------------------------
        # Save A* Visualization
        # ----------------------------------------------------

        astar_filename = (
            f"visualizations/"
            f"astar_{rows}x{cols}_"
            f"{int(obstacle_probability * 100)}percent.png"
        )

        save_visualization(
            experiment_grid,
            start,
            goal,
            astar_path,
            astar_order,
            astar_filename,
            "A*"
        )

        # ----------------------------------------------------
        # Save Dijkstra Visualization
        # ----------------------------------------------------

        dijkstra_filename = (
            f"visualizations/"
            f"dijkstra_{rows}x{cols}_"
            f"{int(obstacle_probability * 100)}percent.png"
        )

        save_visualization(
            experiment_grid,
            start,
            goal,
            dijkstra_path,
            dijkstra_order,
            dijkstra_filename,
            "Dijkstra"
        )


# ============================================================
# 19. Export Results to CSV
# ============================================================

csv_file = "results/results.csv"

with open(csv_file, "w", newline="") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "algorithm",
            "grid_size",
            "obstacle_density",
            "path_found",
            "step_count",
            "expanded_nodes",
            "runtime",
            "expanded_node_density"
        ]
    )

    writer.writeheader()

    for result in results:

        writer.writerow(result)


print("\nResults exported to:")
print(csv_file)

print("\nTotal experiment results:", len(results))
print("Visualizations saved in: visualizations/")