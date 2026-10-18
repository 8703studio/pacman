from mazegenerator import MazeGenerator
from src import Pacman, Level, Engine, EntityDirection, GridObject


def input_mv(event: str) -> EntityDirection | None:
    if event == "z":
        return EntityDirection.UP
    elif event == "q":
        return EntityDirection.LEFT
    elif event == "s":
        return EntityDirection.DOWN
    elif event == "d":
        return EntityDirection.RIGHT
    else:
        return None


def display_level(level, pacman):
    for y, row in enumerate(level.grid_level):
        for x, obj in enumerate(row):
            if (y, x) == pacman.current_pos:
                print("P", end=" ")
            elif obj == GridObject.GUM:
                print(".", end=" ")
            elif obj == GridObject.SUPERGUM:
                print("O", end=" ")
            else:
                print(" ", end=" ")
        print()


if __name__ == "__main__":
    mazegen = MazeGenerator((5, 5))
    level = Level(mazegen.maze, 90)
    engine = Engine(level.grid)
    pacman = Pacman()
    spawn_pacman = (len(level.grid_level) // 2, len(level.grid_level[0]) // 2)
    pacman.start_pos = spawn_pacman
    pacman.current_pos = spawn_pacman

    print()
    print(level.grid)
    while not level.is_finished():
        mv = input("veuillez entrez votre mouvement : ")

        if not input_mv(mv) is None:
            pacman.add_move_to_buffer(input_mv(mv))
        print("buffer  : ", pacman.input_buffer[0])

        pacman.move()
        print("queue : ", pacman.queue)

        print("pacman: ", pacman.current_pos)
        direction = pacman.next_move()
        if direction is not None:
            if engine.is_valid_position(direction.value, pacman.current_pos):
                pacman.update_entity(direction.value)

        display_level(level, pacman)
        print("pacman: ", pacman.current_pos)
        level.consume_object(pacman.current_pos)
