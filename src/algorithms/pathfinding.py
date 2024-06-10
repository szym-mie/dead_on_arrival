from dataclasses import  dataclass, field
from src.level.level import Level
from math import sqrt
from queue import PriorityQueue
from collections import deque


@dataclass
class PathFinder:
    level_map :Level
    directions_cords: list[tuple[int, int]] = field(default_factory=lambda: [(0, 1), (1, 1), (0, 1), (-1, 1), (0, -1), (-1,-1), (-1, 0), (-1, 1)])


    def can_go_to(self, x:int, y:int) -> bool:
        return self.level_map.get_tile_at(x, y) is not None and self.level_map.get_tile_at(x, y) != 0

    @staticmethod
    def heuristic(pos_1:tuple[int, int], pos_2:tuple[int, int]) ->int:
        return abs(pos_1[0]-pos_2[0]) + abs(pos_1[1]-pos_2[1])
    @staticmethod
    def get_distance(pos_1:tuple[int, int], pos_2:tuple[int, int]) -> float:
        return sqrt(abs(pos_1[0]-pos_2[0])**2 + abs(pos_1[1]-pos_2[1])**2)


    def get_neighbours(self, position:tuple[int, int]) -> list[tuple[int, int]]:
        neighbours = []
        for dx, dy in self.directions_cords:
            nx =  position[0] + dx
            ny = position[1] + dy

            if self.can_go_to(nx, ny):
                neighbours.append((nx, ny))

        return neighbours

    @staticmethod
    def reconstruct_path(came_from:dict[tuple[int, int], tuple[int, int]], start:tuple[int, int], goal:tuple[int, int]) -> list[tuple[int, int]]:
        current = goal
        path = []

        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path


    def get_mid_point(self, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:

        x_max =  self.level_map.chunks.x_size*self.level_map.chunk_size
        y_max = self.level_map.chunks.y_size * self.level_map.chunk_size

        # Case 1
        possible_mid_points = []
        if start[0] <= goal[0] and start[1] <= goal[1]:
                print(f'Case 1')

                for x in range(goal[0]):
                    for y in range(y_max, start[1], -1):

                        if self.can_go_to(x, y):
                            possible_mid_points.append((x, y))


                for x in range(x_max, start[0], -1):
                    for y in range(goal[1]):

                        if self.can_go_to(x, y):
                            possible_mid_points.append((x, y))



        # Case 2

        if start[0] <= goal[0] and start[1] >= goal[1]:
            print(f'Case 2')
            for x in range(goal[0]):
                for y in range(start[1]):

                    if self.can_go_to(x, y):
                        possible_mid_points.append((x, y))

            for x in range(x_max, start[0], -1):
                for y in range(y_max, goal[1], -1):

                    if self.can_go_to(x, y):
                        possible_mid_points.append((x, y))


        # Case 3

        if start[0] >= goal[0] and start[1] <= goal[1]:
            print(f'Case 3')
            for x in range(start[0]):
                for y in range(goal[1], start[1], -1):
                    if self.can_go_to(x, y):
                        possible_mid_points.append((x, y))


            for x in range(x_max, goal[0], -1):
                for y in range(y_max, start[1], -1):
                    if self.can_go_to(x, y):
                        possible_mid_points.append((x, y))


        # Case 4

        if start[0] >= goal[0] and start[1] >= goal[1]:
            print(f'Case 4')
            for x in range(start[0]):
                for y in range(y_max, start[1],-1):
                    if self.can_go_to(x, y):
                        possible_mid_points.append((x, y))


            for x in range(x_max,  start[0], -1):
                for y in range(start[1]):
                    if self.can_go_to(x, y):
                        possible_mid_points.append((x, y))

        print(f'{possible_mid_points = }')
        possible_mid_points.append(start)

        return possible_mid_points





    def flank(self, start:tuple[int, int], goal:tuple[int, int]) -> list[tuple[int, int]]:
        mid_points = self.get_mid_point(start, goal)

        for mid_point in mid_points:
            print(f'{mid_point = }')

            flanking_path =  self.get_shortest_path(start, mid_point)[:-1] + self.get_shortest_path(mid_point, goal)
            if flanking_path:
                return flanking_path
        return []


    def get_shortest_path(self, start:tuple[int, int], goal:tuple[int, int]) -> list[tuple[int, int]]:

        if not self.can_go_to(start[0], start[1]) or not self.can_go_to(goal[0], goal[1]):
            return []

        pq = PriorityQueue()
        pq.put((0, start))
        came_from = {}
        distance = {}
        came_from[start] = None
        distance[start] = 0

        while not pq.empty():

            dist, current = pq.get()

            if current == goal:
                print(f'{dist=}')
                return self.reconstruct_path(came_from, start, goal)


            for neighbour in self.get_neighbours(current):
                new_dist = distance[current] + self.get_distance(current, neighbour)

                if neighbour not in distance or new_dist < distance[neighbour]:
                    distance[neighbour] =  new_dist
                    priority = new_dist + self.heuristic(neighbour, goal)
                    pq.put((priority, neighbour))
                    came_from[neighbour] = current

        return []


    def can_hear(self, pos:tuple[int, int], enemy_pos:tuple[int, int], max_hearing_range:int) -> bool:
        queue = deque()
        queue.append([pos, 0])
        visited =   {}
        visited[pos] = True

        while queue:
            current_pos, current_distance = queue.popleft()

            if current_distance <= max_hearing_range and current_pos == enemy_pos:
                return True

            if current_distance > max_hearing_range:
                return False


            for neighbour in self.get_neighbours(current_pos):
                if neighbour not in visited:
                    queue.append([neighbour, current_distance+1])
            visited[current_pos] = True

        return False
