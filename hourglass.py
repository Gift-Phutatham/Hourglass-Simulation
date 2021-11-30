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
        self.screen_size = 750

        self.one_quarter = self.screen_size/4
        self.between_quarters1 = 1.75*self.screen_size/4
        self.one_half = self.screen_size/2
        self.between_quarters2 = 2.25*self.screen_size/4
        self.three_quarter = 3*self.screen_size/4

        self.screen = pygame.display.set_mode(
            (self.screen_size, self.screen_size))
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.add_glass_component()
        self.balls = []
        self.running = True

    def run(self):
        for _ in range(5):
            self.create_ball()
        while self.running:
            self.space.step(self.dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((31, 40, 57))
            self.space.debug_draw(self.draw_options)
            pygame.display.flip()
            self.clock.tick(50)

    def add_glass_component(self):
        radius = 2
        static_body = self.space.static_body
        static_lines = [
            pymunk.Segment(static_body, (self.one_quarter, self.one_quarter),
                           (self.three_quarter, self.one_quarter), radius),  # top
            pymunk.Segment(static_body, (self.one_quarter, self.three_quarter),
                           (self.three_quarter, self.three_quarter), radius),  # bottom
            pymunk.Segment(static_body, (self.three_quarter, self.one_quarter),
                           (self.between_quarters2, self.one_half), radius),  # top-right
            pymunk.Segment(static_body, (self.between_quarters2, self.one_half),
                           (self.three_quarter, self.three_quarter), radius),  # bottom-right
            pymunk.Segment(static_body, (self.one_quarter, self.one_quarter),
                           (self.between_quarters1, self.one_half), radius),  # top-left
            pymunk.Segment(static_body, (self.between_quarters1, self.one_half),
                           (self.one_quarter, self.three_quarter), radius)  # bottom_left
        ]
        for line in static_lines:
            line.elasticity = 0.95
            line.friction = 0.9
        self.space.add(*static_lines)

    def create_ball(self):
        mass = 10
        radius = 10
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        x = random.randint(int(self.one_quarter+radius),
                           int(self.three_quarter-radius))
        y = self.one_quarter + radius
        body.position = x, y
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.5
        shape.friction = 1000
        self.space.add(body, shape)
        self.balls.append(shape)


hour_glass = HourGlass()
hour_glass.run()
