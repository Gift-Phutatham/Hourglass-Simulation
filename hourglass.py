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
        self.screen = pygame.display.set_mode(
            (self.screen_size, self.screen_size))
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
        radius = 2
        one_half = self.screen_size/2
        one_quarter = self.screen_size/4
        between_quarters1 = 1.75*self.screen_size/4
        between_quarters2 = 2.25*self.screen_size/4
        three_quarter = 3*self.screen_size/4
        static_body = self.space.static_body
        static_lines = [
            pymunk.Segment(static_body, (one_quarter, one_quarter),
                           (three_quarter, one_quarter), radius),  # top
            pymunk.Segment(static_body, (one_quarter, three_quarter),
                           (three_quarter, three_quarter), radius),  # bottom
            pymunk.Segment(static_body, (three_quarter, one_quarter),
                           (between_quarters2, one_half), radius),  # top-right
            pymunk.Segment(static_body, (between_quarters2, one_half),
                           (three_quarter, three_quarter), radius),  # bottom-right
            pymunk.Segment(static_body, (one_quarter, one_quarter),
                           (between_quarters1, one_half), radius), # top-left
            pymunk.Segment(static_body, (between_quarters1, one_half),
                           (one_quarter, three_quarter), radius) # bottom_left
        ]
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
