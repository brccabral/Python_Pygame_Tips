import os
import json
import math
import pygame


def read_json(path: str) -> dict[str, list[int]]:
    f = open(path, "r")
    dat = f.read()
    f.close()
    return json.loads(dat)


def get_dis(p1: list[float], p2: list[float]):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def load_rags(path: str):
    rag_list = os.listdir(path)
    rags: dict[str, dict[str, list[int]]] = {}
    for rag in rag_list:
        rags[rag.split(".")[0]] = read_json(path + "/" + rag)
    return rags


class ClothObj:
    def __init__(self, rag):
        self.points: list[list[float]] = [p + p for p in rag["points"]]  # dupe position for last position
        self.orig_points: list[list[float]] = [p + p for p in rag["points"]]
        self.sticks: list[tuple[int, int, float]] = []
        self.scale: float = rag["scale"]
        for stick in rag["connections"]:
            self.add_stick(stick)
        self.grounded: list[float] = rag["grounded"]
        self.elasticity = 0.85  # if 1 it is a strong/hard connection, if 0.2 it becomes an elastic cord

    def add_stick(self, points: list[int]):
        self.sticks.append((points[0], points[1], get_dis(self.points[points[0]][:2], self.points[points[1]][:2])))

    def update(self):
        for i, point in enumerate(self.points):
            if i not in self.grounded:
                d_x = point[0] - point[2]
                d_y = point[1] - point[3]
                point[2] = point[0]
                point[3] = point[1]
                point[0] += d_x
                point[1] += d_y
                point[1] += 0.05  # adds gravity

    def move_grounded(self, offset: list[int]):
        for i, point in enumerate(self.points):
            if i in self.grounded:
                point[0] = self.orig_points[i][0] + offset[0] / self.scale
                point[1] = self.orig_points[i][1] + offset[1] / self.scale
                point[2] = point[0]
                point[3] = point[1]

    def update_sticks(self):
        for stick in self.sticks:
            dis = get_dis(self.points[stick[0]][:2], self.points[stick[1]][:2])
            dis_dif = stick[2] - dis
            mv_ratio = dis_dif / dis / 2
            dx = self.points[stick[1]][0] - self.points[stick[0]][0]
            dy = self.points[stick[1]][1] - self.points[stick[0]][1]
            if stick[0] not in self.grounded:
                self.points[stick[0]][0] -= dx * mv_ratio * self.elasticity
                self.points[stick[0]][1] -= dy * mv_ratio * self.elasticity
            if stick[1] not in self.grounded:
                self.points[stick[1]][0] += dx * mv_ratio * self.elasticity
                self.points[stick[1]][1] += dy * mv_ratio * self.elasticity

    def render_polygon(self, target_surf: pygame.Surface, color: pygame.Color, offset: tuple[float, float] = (0, 0)):
        y_points = [p[1] * self.scale for p in self.points]
        x_points = [p[0] * self.scale for p in self.points]
        min_x = min(x_points)
        max_x = max(x_points)
        min_y = min(y_points)
        max_y = max(y_points)
        width = int(max_x - min_x + 2)
        height = int(max_y - min_y + 2)
        surf = pygame.Surface((width, height))
        self.render_sticks(surf, (int(min_x), int(min_y)))
        surf.set_colorkey((0, 0, 0))
        m = pygame.mask.from_surface(surf)
        outline = m.outline()  # get outline of mask
        surf.fill((0, 0, 0))  # fill with color that will be colorkey
        surf.set_colorkey((0, 0, 0))
        pygame.draw.polygon(surf, color, outline)
        target_surf.blit(surf, (min_x - offset[0], min_y - offset[1]))

    def render_sticks(self, surf: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        render_points = [[p[0] * self.scale - offset[0], p[1] * self.scale - offset[1]] for p in self.points]
        for stick in self.sticks:
            pygame.draw.line(surf, (255, 255, 255), render_points[stick[0]], render_points[stick[1]], 1)
