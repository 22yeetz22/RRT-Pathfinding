import pygame
import random
import math


class RRTMap:
    def __init__(self, start, goal, map_dimensions, obsdim, obsnum):
        self.start = start
        self.goal = goal
        self.map_dimensions = map_dimensions
        self.maph, self.mapw = self.map_dimensions

        self.WINDOWNAME = "RRT Pathfinding"
        pygame.display.set_caption(self.WINDOWNAME)
        self.map = pygame.display.set_mode((self.mapw, self.maph))

        self.map.fill((255, 255, 255))

        self.node_radius = 0
        self.node_thickness = 0
        self.edge_thickness = 1

        self.obstacles = []
        self.obsdim = obsdim
        self.obs_number = obsnum

        # Colors
        self.colors = {
            'grey': (70, 70, 70),
            'blue': (0, 0, 255),
            'green': (0, 255, 0),
            'red': (225, 0, 0),
            'white': (255, 255, 255)
        }

    def drawMap(self):

    def drawPath(self):

    def drawObs(self):


class RRTGraph:
    def __init__(self, start, goal, map_dimensions, obsdim, obsnum):
        x, y = start
        self.start = start
        self.goal = goal
        self.goal_flag = False

        self.maph, self.mapw = map_dimensions
        self.x = self.y = self.parent = []
        # Initialize the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)

        # Obstacles
        self.obstacles = []
        self.obsdim = obsdim
        self.obsnum = obsnum

        # Path
        self.goalstate = None
        self.path = []

    def make_random_rect(self):
        # Create rect at upper left corner x, y
        cornerx = int(random.uniform(0, self.mapw - self.obsdim))
        cornery = int(random.uniform(0, self.maph - self.obsdim))

        return (cornerx, cornery)

    def makeobs(self):

    def add_node(self):

    def remove_node(self):

    def add_edge(self):

    def remove_edge(self):

    def number_of_nodes(self):

    def distance(self):

    def nearest(self):

    def isFree(self):

    def crossObstacle(self):

    def connect(self):

    def step(self):

    def path_to_goal(self):

    def getPathCoords(self):

    def bias(self):

    def expand(self):

    def cost(self):
