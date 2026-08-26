from src.maze.maze_adapter import MazeAdapter


adapter = MazeAdapter()

maze = adapter.generate_level(
    level=1,
    seed_base=42,
    width=5,
    height=5,
)

print("Maze:")
for y, row in enumerate(maze):
    print(f"y={y}: {row}")

walkable = adapter.get_walkable_cells(maze)

print("\nWalkable cells:")
print(walkable)

center = (len(maze[0]) // 2, len(maze) // 2)
print("\nCenter:")
print(center)

corners = adapter.get_corners(maze)
print("\nCorners:")
print(corners)

for y in range(len(maze)):
    for x in range(len(maze[y])):
        neighbors = adapter.get_neighbors(maze, x, y)
        print(f"({x}, {y}) -> {neighbors}")
