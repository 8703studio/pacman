from src.maze.maze_adapter import MazeAdapter


adapter = MazeAdapter()

maze = adapter.generate_level(
    level=1,
    seed_base=42,
    width=21,
    height=21,
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

spawns = adapter.get_spawn_positions(maze)
print("\nSpawn positions:")
print(spawns)

pacgums = adapter.get_pacgum_positions(maze)
print("\nPacgum positions:")
print(pacgums)

super_pacgums = adapter.get_super_pacgum_positions(maze)
print("\nSuper pacgum positions:")
print(super_pacgums)