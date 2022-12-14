import random
import math
import pygame


class RRTMap:
    def __init__(self, start, goal, map_dimensions, obsdim, obsnum):
        self.start = start
        self.goal = goal
        self.map_dimensions = map_dimensions
        self.maph, self.mapw = self.map_dimensions

        # Window settings
        self.win_name = 'RRT Pathfinding'
        pygame.display.set_caption(self.win_name)
        self.map = pygame.display.set_mode((self.mapw, self.maph))

        self.map.fill((255, 255, 255))

        self.node_radius = 2
        self.node_thickness = 1
        self.edge_thickness = 1

        self.obstacles = []
        self.obstacle_dimension = obsdim
        self.obstacle_number = obsnum

        # Colors
        self.colors = {
            'grey': (70, 70, 70),
            'blue': (10, 30, 250),
            'green': (20, 250, 40),
            'red': (250, 30, 10),
            'white': (255, 255, 255)
        }

    def draw_map(self, obstacles):
        pygame.draw.circle(self.map, self.colors['green'], self.start, self.node_radius + 5, 0)
        pygame.draw.circle(self.map, self.colors['green'], self.goal, self.node_radius + 20, 1)
        self.draw_object(obstacles)

    def draw_path(self, path):
        for node in path:
            pygame.draw.circle(self.map, self.colors['red'], node, 3, 0)

    def draw_object(self, obstacles):
        obstaclesList = obstacles.copy()
        while len(obstaclesList) > 0:
            obstacle = obstaclesList.pop(0)
            pygame.draw.rect(self.map, self.colors['grey'], obstacle)


class RRTGraph:
    def __init__(self, start, goal, map_dimensions, obsdim, obsnum):
        x, y = start
        self.start = start
        self.goal = goal
        self.goal_flag = False
        self.maph, self.mapw = map_dimensions
        self.x = []
        self.y = []
        self.parent = []

        # Initialize the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)

        # Create the obstacles
        self.obstacles = []
        self.object_dimension = obsdim
        self.object_number = obsnum

        # Create the path
        self.goalstate = None
        self.path = []

    def random_rect(self):
        uppercornerx = int(random.uniform(0, self.mapw - self.object_dimension))
        uppercornery = int(random.uniform(0, self.maph - self.object_dimension))

        return uppercornerx, uppercornery

    def make_objects(self):
        obs = [pygame.Rect((350, 0), (50, 300)), pygame.Rect((350, 310), (50, 200))]
        for i in range(0, self.object_number):
            rectangle = None
            startgoalcol = True
            while startgoalcol:
                upper = self.random_rect()
                rectangle = pygame.Rect(upper, (self.object_dimension, self.object_dimension))
                if rectangle.collidepoint(self.start) or rectangle.collidepoint(self.goal): startgoalcol = True
                else: startgoalcol = False
            obs.append(rectangle)

        self.obstacles = obs.copy()
        return obs

    def add_node(self, n, x, y):
        self.x.insert(n, x)
        self.y.append(y)

    def remove_node(self, n):
        self.x.pop(n)
        self.y.pop(n)

    def add_edge(self, parent, child):
        self.parent.insert(child, parent)

    def remove_edge(self, n):
        self.parent.pop(n)

    def num_nodes(self):
        return len(self.x)

    def distance(self, n1, n2):
        x1, y1 = self.x[n1], self.y[n1]
        x2, y2 = self.x[n2], self.y[n2]
        px = (float(x1) - float(x2)) ** 2
        py = (float(y1) - float(y2)) ** 2
        return (px + py) ** 0.5

    def sample_envir(self):
        x = int(random.uniform(0, self.mapw))
        y = int(random.uniform(0, self.maph))
        return x, y

    def nearest(self, n):
        dmin = self.distance(0, n)
        nnear = 0
        for i in range(0, n):
            if self.distance(i, n) < dmin:
                dmin = self.distance(i, n)
                nnear = i
        return nnear

    def is_free(self):
        n = self.num_nodes() - 1
        x, y = self.x[n], self.y[n]
        obs = self.obstacles.copy()
        while len(obs) > 0:
            rectangle = obs.pop(0)
            if rectangle.collidepoint(x, y):
                self.remove_node(n)
                return False

        return True

    def cross_obstacle(self, x1, x2, y1, y2):
        obs = self.obstacles.copy()
        while len(obs) > 0:
            rectangle = obs.pop(0)
            for i in range(0, 101):
                u = i / 100
                x = x1 * u + x2 * (1 - u)
                y = y1 * u + y2 * (1 - u)
                if rectangle.collidepoint(x, y):
                    return True
        return False

    def connect(self, n1, n2):
        x1, y1 = self.x[n1], self.y[n1]
        x2, y2 = self.x[n2], self.y[n2]
        if self.cross_obstacle(x1, x2, y1, y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1, n2)
            return True

    def step(self, nnear, nrand, dmax=35):
        d = self.distance(nnear, nrand)
        if d > dmax:
            xnear, ynear = self.x[nnear], self.y[nnear]
            xrand, yrand = self.x[nrand], self.y[nrand]
            px, py = xrand - xnear, yrand - ynear
            theta = math.atan2(py, px)
            x, y = int(xnear + dmax * math.cos(theta)), int(ynear + dmax * math.sin(theta))

            self.remove_node(nrand)
            if abs(x - self.goal[0]) <= dmax and abs(y - self.goal[1]) <= dmax:
                self.add_node(nrand, self.goal[0], self.goal[1])
                self.goalstate = nrand
                self.goal_flag = True
            else: self.add_node(nrand, x, y)

    def bias(self, ngoal):
        n = self.num_nodes()
        self.add_node(n, ngoal[0], ngoal[1])
        nnear = self.nearest(n)
        self.step(nnear, n)
        self.connect(nnear, n)
        return self.x, self.y, self.parent

    def expand(self):
        n = self.num_nodes()
        x, y = self.sample_envir()
        self.add_node(n, x, y)
        if self.is_free():
            xnearest = self.nearest(n)
            self.step(xnearest, n)
            self.connect(xnearest, n)

        return self.x, self.y, self.parent

    def path_to_goal(self):
        if self.goal_flag:
            self.path = []
            try:
                self.path.append(self.goalstate)
                newpos = self.parent[self.goalstate]
                while newpos != 0:
                    self.path.append(newpos)
                    newpos = self.parent[newpos]
                self.path.append(0)
            except IndexError: self.goal_flag = False
        return self.goal_flag

    def path_coords(self):
        path_coords = []
        for node in self.path:
            x, y = self.x[node], self.y[node]
            path_coords.append((x, y))
        return path_coords

    def cost(self, n):
        ninit = 0
        n = n
        parent = self.parent[n]
        c = 0
        while n is not ninit:
            c += self.distance(n, parent)
            n = parent
            if n is not ninit: parent = self.parent[n]

        return c

    @staticmethod
    def get_true_object(obs):
        tobs = []
        for ob in obs:
            tobs.append(ob.inflate(-50, -50))
        return tobs

    def waypoints_to_path(self):
        oldpath = self.path_coords()
        path = []
        for i in range(0, len(self.path) - 1):
            if i >= len(self.path): break

            x1, y1 = oldpath[i]
            x2, y2 = oldpath[i + 1]
            for j in range(0, 5):
                u = j / 5
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))
                path.append((x, y))

        return path


def make_random_rect(self):
    uppercornerx = int(random.uniform(0, self.mapw - self.object_dimension))
    uppercornery = int(random.uniform(0, self.maph - self.object_dimension))
    return uppercornerx, uppercornery


def make_object(self):
    obs = []
    for i in range(0, self.object_number):
        startgoalcol = True
        while startgoalcol:
            upper = self.random_rect()
            rectangle = pygame.Rect(upper, (self.object_dimension, self.object_dimension))
            if rectangle.collidepoint(self.start) or rectangle.collidepoint(self.goal): startgoalcol = True
            else: startgoalcol = False
            obs.append(rectangle)
        self.obstacles = obs.copy()

    return obs
