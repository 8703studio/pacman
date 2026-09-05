from collections import deque


class Ghost():
    def __init__(self):
        self.queue: deque[tuple[int, int]] = deque()
        self.visited: deque[tuple[int, int]] = deque()
