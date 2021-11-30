import random
import pygame
import pymunk
import pymunk.pygame_util


class HourGlass(object):
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        self.dt = 1/50
        self.steps_per_frame = 1

        pygame.init()
        self.screen_size = 750

        self.one_quarter = self.screen_size/4
        self.between_quarters1 = 1.75*self.screen_size/4
        self.one_half = self.screen_size/2
        self.between_quarters2 = 2.25*self.screen_size/4
        self.three_quarter = 3*self.screen_size/4

        self.screen = pygame.display.set_mode(
            (self.screen_size, self.screen_size)
        )
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.add_glass_component()
        self.balls = []
        self.running = True

    def run(self):
        number_of_balls = 20
        for _ in range(number_of_balls):
            self.create_ball()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((31, 40, 57))
            self.space.debug_draw(self.draw_options)
            for _ in range(10):
                self.space.step(self.dt/10)
            pygame.display.flip()
            self.clock.tick(50)

    def add_glass_component(self):
        radius = 2
        positions = [
            ((self.one_quarter, self.one_quarter),
             (self.three_quarter, self.one_quarter)),  # top
            ((self.one_quarter, self.three_quarter),
             (self.three_quarter, self.three_quarter)),  # bottom
            ((self.three_quarter, self.one_quarter),
             (self.between_quarters2, self.one_half)),  # top-right
            ((self.between_quarters2, self.one_half),
             (self.three_quarter, self.three_quarter)),  # bottom-right
            ((self.one_quarter, self.one_quarter),
             (self.between_quarters1, self.one_half)),  # top-left
            ((self.between_quarters1, self.one_half),
             (self.one_quarter, self.three_quarter))  # bottom_left
        ]
        for position in positions:
            segment = pymunk.Segment(
                self.space.static_body, position[0], position[1], radius
            )
            segment.elasticity = 0.95
            segment.friction = 1
            self.space.add(segment)

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
        shape.friction = 1
        self.space.add(body, shape)
        self.balls.append(shape)


hour_glass = HourGlass()
hour_glass.run()
