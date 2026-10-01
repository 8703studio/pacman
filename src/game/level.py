from ..enums import GridObject


class Level():
    def __init__(self, wall_grid: list[list[int]], time: int) -> None:
        self.time: int = time
        self.grid: list[list[int]] = wall_grid
        self.corners: list[tuple] = self._get_corners()
        self.grid_level: list[list[GridObject]] = self._create_grid_object()
        self.element_numb: int = self._get_numb_elem()

    def _get_corners(self) -> list[tuple]:
        width: int = len(self.grid[0])
        height: int = len(self.grid)
        return [
            (0, 0),
            (0, width - 1),
            (height - 1, 0),
            (height - 1, width - 1)
        ]

    def _get_numb_elem(self) -> int:
        total: int = 0
        for row in self.grid_level:
            for elem in row:
                if elem != GridObject.EMPTY:
                    total += 1
        return total

    def _create_grid_object(self) -> list[list[GridObject]]:
        obj_grid: list[list[GridObject]] = [[GridObject.GUM if obj != 15 else
                                             GridObject.EMPTY for obj in
                                            row] for row in self.grid]
        for coor in self.corners:
            y, x = coor
            obj_grid[y][x] = GridObject.SUPERGUM
        return obj_grid

    def consume_object(self, case: tuple) -> GridObject:
        y, x = case
        obj = self.grid_level[y][x]
        self.grid_level[y][x] = GridObject.EMPTY
        if obj == GridObject.GUM or obj == GridObject.SUPERGUM:
            self.element_numb -= 1
        return obj

    def clear_grid(self) -> None:
        self.grid_level = [[GridObject.EMPTY
                            for _ in row] for row in self.grid]
        self.element_numb = 0

    def is_finished(self) -> bool:
        return self.element_numb == 0
