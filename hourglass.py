import random
import pygame
import pymunk
import pymunk.pygame_util


class HourGlass(object):
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        self.dt = 1 / 60
        self.steps_per_frame = 1

        pygame.init()
        self.screen = pygame.display.set_mode((750, 750))
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.add_glass_component()
        self.balls = []
        self.running = True
        self.ticks_to_next_ball = 10

    def run(self):
        while self.running:
            for _ in range(self.steps_per_frame):
                self.space.step(self.dt)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                self.screen.fill((217, 217, 217))
                self.space.debug_draw(self.draw_options)
                self.update_balls()
                pygame.display.flip()
                self.clock.tick(50)

    def add_glass_component(self):
        static_body = self.space.static_body
        static_lines = pymunk.Segment(static_body, (125, 500), (500, 500), 3),
        for line in static_lines:
            line.elasticity = 0.95
            line.friction = 0.9
        self.space.add(*static_lines)

    def create_ball(self):
        mass = 10
        radius = 5
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        x = random.randint(115, 350)
        y = random.randint(115, 350)
        body.position = x, y
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.5
        shape.friction = 0.9
        self.space.add(body, shape)
        self.balls.append(shape)

    def update_balls(self):
        self.ticks_to_next_ball -= 1
        if self.ticks_to_next_ball <= 0:
            self.create_ball()
            self.ticks_to_next_ball = 100


hour_glass = HourGlass()
hour_glass.run()
