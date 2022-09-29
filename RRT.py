import pygame
from RRTbase import RRTGraph, RRTMap
from time import sleep, time
from sys import exit as sysexit


def main():
    dimensions = (500, 500)
    start = (50, 50)
    goal = (450, 450)
    object_dimension = 15
    object_number = 30
    iteration = 0

    pygame.init()
    path_map = RRTMap(start, goal, dimensions, object_dimension, object_number)
    graph = RRTGraph(start, goal, dimensions, object_dimension, object_number)

    obstacles = graph.make_objects()
    path_map.draw_map(obstacles)

    t1 = time()
    while not graph.path_to_goal():
        sleep(0.01)
        elapsed = time() - t1
        t1 = time()

        # Raise exception if timeout
        if elapsed > 25: raise Exception("Timeout! Recreating the calculations.")

        # Start calculations
        if iteration % 10 == 0:
            x, y, parent = graph.bias(goal)
            pygame.draw.circle(path_map.map, path_map.colors['grey'], (x[-1], y[-1]), path_map.node_radius * 2, 0)
            pygame.draw.line(path_map.map, path_map.colors['blue'], (x[-1], y[-1]), (x[parent[-1]], y[parent[-1]]), path_map.edge_thickness)
        else:
            x, y, parent = graph.expand()
            pygame.draw.circle(path_map.map, path_map.colors['grey'], (x[-1], y[-1]), path_map.node_radius * 2, 0)
            pygame.draw.line(path_map.map, path_map.colors['blue'], (x[-1], y[-1]), (x[parent[-1]], y[parent[-1]]), path_map.edge_thickness)

        if iteration % 2 == 0:
            pygame.display.update()
        iteration += 1

    path_map.draw_path(graph.path_coords())
    pygame.display.update()

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    while True:
        result = False
        tries = 0

        while not result and tries < 25:
            try:
                main()
                result = True
            except TypeError:
                print("Uh oh, something bad happened to this map! Trying to regenerate it.")
                result = False
            tries += 1

        pygame.init()
        screen = pygame.display.set_mode((400, 200))
        pygame.display.set_caption("Continue?")
        clock = pygame.time.Clock()

        font = pygame.font.SysFont("Verdana", 19, True)
        fontsmall = pygame.font.SysFont("Verdana", 12, True)
        question_surface = font.render("Do you want to continue? (y/n)", True, (0, 0, 0))
        description_surface = fontsmall.render("Click y or n to continue.", True, (0, 0, 0))

        no_input = True
        generate_map = False
        while no_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: no_input = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        generate_map = True
                        no_input = False
                    elif event.key == pygame.K_n: no_input = False

            screen.fill((255, 255, 255))

            screen.blit(question_surface, (25, 50))
            screen.blit(description_surface, (25, 150))

            clock.tick(15)
            pygame.display.update()

        if generate_map: print("Generating new map for you...\n")
        else: sysexit("Bye!")
