import pandas as pd
import matplotlib.pyplot as plt
import os

# Read results from CSV
csv_file = "results/results.csv"
data = pd.read_csv(csv_file)

print("Results loaded successfully!")
print(data)

# Create folder for graphs
os.makedirs("graphs", exist_ok=True)

# -----------------------------
# Graph 1: Grid Size vs Expanded Nodes
# -----------------------------

astar_data = data[data["algorithm"] == "A*"]
dijkstra_data = data[data["algorithm"] == "Dijkstra"]

# Calculate average expanded nodes for each grid size
astar_expanded = astar_data.groupby("grid_size")["expanded_nodes"].mean()
dijkstra_expanded = dijkstra_data.groupby("grid_size")["expanded_nodes"].mean()

grid_sizes = ["5x5", "10x10", "20x20", "30x30"]

plt.figure(figsize=(10, 6))

plt.plot(
    grid_sizes,
    astar_expanded.reindex(grid_sizes),
    marker="o",
    label="A*"
)

plt.plot(
    grid_sizes,
    dijkstra_expanded.reindex(grid_sizes),
    marker="o",
    label="Dijkstra"
)

plt.xlabel("Grid Size")
plt.ylabel("Average Expanded Nodes")
plt.title("Grid Size vs Expanded Nodes")
plt.legend()
plt.grid(True)

plt.savefig("graphs/grid_size_vs_expanded_nodes.png")
plt.show()

print("\nGraph 1 saved successfully!")
print("graphs/grid_size_vs_expanded_nodes.png")

# -----------------------------
# Graph 2: Grid Size vs Runtime
# -----------------------------

astar_runtime = astar_data.groupby("grid_size")["runtime"].mean()
dijkstra_runtime = dijkstra_data.groupby("grid_size")["runtime"].mean()

plt.figure(figsize=(10, 6))

plt.plot(
    grid_sizes,
    astar_runtime.reindex(grid_sizes),
    marker="o",
    label="A*"
)

plt.plot(
    grid_sizes,
    dijkstra_runtime.reindex(grid_sizes),
    marker="o",
    label="Dijkstra"
)

plt.xlabel("Grid Size")
plt.ylabel("Average Runtime (seconds)")
plt.title("Grid Size vs Runtime")
plt.legend()
plt.grid(True)

plt.savefig("graphs/grid_size_vs_runtime.png")
plt.show()

print("\nGraph 2 saved successfully!")
print("graphs/grid_size_vs_runtime.png")

# -----------------------------
# Graph 3: Obstacle Density vs Expanded Nodes
# -----------------------------

astar_obstacles = astar_data.groupby("obstacle_density")["expanded_nodes"].mean()
dijkstra_obstacles = dijkstra_data.groupby("obstacle_density")["expanded_nodes"].mean()

obstacle_levels = [0.1, 0.2, 0.3]

plt.figure(figsize=(10, 6))

plt.plot(
    obstacle_levels,
    astar_obstacles.reindex(obstacle_levels),
    marker="o",
    label="A*"
)

plt.plot(
    obstacle_levels,
    dijkstra_obstacles.reindex(obstacle_levels),
    marker="o",
    label="Dijkstra"
)

plt.xlabel("Obstacle Density")
plt.ylabel("Average Expanded Nodes")
plt.title("Obstacle Density vs Expanded Nodes")
plt.xticks(
    obstacle_levels,
    ["10%", "20%", "30%"]
)
plt.legend()
plt.grid(True)

plt.savefig("graphs/obstacle_density_vs_expanded_nodes.png")
plt.show()

print("\nGraph 3 saved successfully!")
print("graphs/obstacle_density_vs_expanded_nodes.png")

# -----------------------------
# Graph 4: Expanded Node Density
# -----------------------------

astar_density = astar_data.groupby("grid_size")["expanded_node_density"].mean()
dijkstra_density = dijkstra_data.groupby("grid_size")["expanded_node_density"].mean()

plt.figure(figsize=(10, 6))

plt.plot(
    grid_sizes,
    astar_density.reindex(grid_sizes),
    marker="o",
    label="A*"
)

plt.plot(
    grid_sizes,
    dijkstra_density.reindex(grid_sizes),
    marker="o",
    label="Dijkstra"
)

plt.xlabel("Grid Size")
plt.ylabel("Average Expanded Node Density (%)")
plt.title("Grid Size vs Expanded Node Density")
plt.legend()
plt.grid(True)

plt.savefig("graphs/grid_size_vs_expanded_node_density.png")
plt.show()

print("\nGraph 4 saved successfully!")
print("graphs/grid_size_vs_expanded_node_density.png")

# -----------------------------
# Graph 5: Path Length vs Grid Size
# -----------------------------

astar_steps = astar_data.groupby("grid_size")["step_count"].mean()
dijkstra_steps = dijkstra_data.groupby("grid_size")["step_count"].mean()

plt.figure(figsize=(10, 6))

plt.plot(
    grid_sizes,
    astar_steps.reindex(grid_sizes),
    marker="o",
    label="A*"
)

plt.plot(
    grid_sizes,
    dijkstra_steps.reindex(grid_sizes),
    marker="o",
    label="Dijkstra"
)

plt.xlabel("Grid Size")
plt.ylabel("Average Path Length (steps)")
plt.title("Grid Size vs Path Length")
plt.legend()
plt.grid(True)

plt.savefig("graphs/grid_size_vs_path_length.png")
plt.show()

print("\nGraph 5 saved successfully!")
print("graphs/grid_size_vs_path_length.png")
