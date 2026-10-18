from math import dist
from src import (GhostGlutton, Engine, Level,
                 Pacman, GridObject, EntityDirection)
import mazegenerator as mazegen


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


def display_level(level, engine, pacman, gluttony):
    height = len(level.grid_level)
    width = len(level.grid_level[0])

    print("+" + "---+" * width)

    for y in range(height):
        line = "|"
        bottom = "+"

        for x in range(width):
            pos = (y, x)
            obj = level.grid_level[y][x]

            if pos == gluttony.current_pos:
                char = "G"
            elif pos == pacman.current_pos:
                char = "P"
            elif obj == GridObject.GUM:
                char = "."
            elif obj == GridObject.SUPERGUM:
                char = "O"
            else:
                char = " "

            line += f" {char} "

            if engine.is_valid_position(EntityDirection.RIGHT.value, pos):
                line += " "
            else:
                line += "|"

            if engine.is_valid_position(EntityDirection.DOWN.value, pos):
                bottom += "   +"
            else:
                bottom += "---+"

        print(line)
        print(bottom)

if __name__ == "__main__":

    mazegene = mazegen.MazeGenerator((5, 5))
    level = Level(mazegene.maze, 90)
    engine = Engine(level.grid)
    pacman = Pacman()
    gluttony = GhostGlutton(engine)
    pacman.start_pos = (4, 4)
    pacman.current_pos = (4, 4)







    while not level.is_finished():
        mv = input("veuillez entrez votre mouvement : ")
        mv_input = input_mv(mv)
        if mv_input is not None:
            pacman.add_move_to_buffer(mv_input)
        print("buffer  : ", pacman.input_buffer[0])
        pacman.move()

        direction = pacman.next_move()
        if direction is not None:
            if engine.is_valid_position(direction.value, pacman.current_pos):
                pacman.update_entity(direction.value)
        level.consume_object(pacman.current_pos)

        gluttony.target = pacman.current_pos
        gluttony.move()
        titi = gluttony.next_move()
        gluttony.update_entity(titi.value)
        if pacman.current_pos == gluttony.current_pos:
            print("pacman perds une vie")
            break

        print("======== Ghost =========")
        print()
        print(gluttony.current_pos)
        print("queue : ", pacman.queue)
        print("pacman: ", pacman.current_pos)
        display_level(level, engine, pacman, gluttony)
