import pygame
import pymunk
import pymunk.pygame_util
from random import randrange


class NormalDistributionHourglass(object):
    def __init__(self):
        self.ball_mass = 1
        self.ball_radius = 7

        pygame.init()
        self.space = pymunk.Space()
        self.space.gravity = (0, 8000)
        self.screen_size = 750
        self.screen = pygame.display.set_mode(
            (self.screen_size, self.screen_size))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()

    def run(self):
        self.create_component()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill(pygame.Color('black'))
            self.space.debug_draw(self.draw_options)
            pygame.display.flip()
            for _ in range(10):
                self.space.step(1/self.fps/10)
            self.clock.tick(self.fps)

    def create_component(self):
        for _ in range(500):
            self.create_ball(self.space, self.ball_mass, self.ball_radius)

        constraint_radius = 10
        for i in range(100, self.screen_size, 50):
            self.create_constraint(self.space, constraint_radius, (i, 200))
            self.create_constraint(self.space, constraint_radius, (i-25, 250))
            self.create_constraint(self.space, constraint_radius, (i, 300))
            self.create_constraint(self.space, constraint_radius, (i-25, 350))

        self.create_segment(self.space, 3)

    def create_ball(self, space, mass, radius):
        temp = 50
        balls = []
        inertia = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, inertia)
        body.position = randrange(
            temp, self.screen_size-temp), randrange(0, temp)
        shape = pymunk.Circle(body, radius)
        shape.elasticity = 0.1
        shape.friction = 0.1
        space.add(body, shape)
        balls.append(shape)

    def create_segment(self, space, radius):
        temp1 = 150
        positions = [
            ((0, self.screen_size), (self.screen_size, self.screen_size)),
            ((0, 0), (0, temp1/2)),
            ((self.screen_size, 0), (self.screen_size, temp1/2)),
            ((0, temp1/2), (self.screen_size/2 - temp1/2, temp1)),
            ((self.screen_size, temp1/2), (self.screen_size/2 + temp1/2, temp1))
        ]
        temp2 = 100
        for i in range(0, 400, 50):
            positions.append(((self.screen_size/2 - i, self.screen_size/2 + temp2),
                              (self.screen_size/2 - i, self.screen_size)))
            positions.append(((self.screen_size/2 + i, self.screen_size/2 + temp2),
                              (self.screen_size/2 + i, self.screen_size)))
        for position in positions:
            segment = pymunk.Segment(
                space.static_body, position[0], position[1], radius
            )
            segment.elasticity = 0.5
            segment.friction = 1
            segment.color = pygame.color.THECOLORS['brown']
            space.add(segment)

    def create_constraint(self, space, radius, offset):
        constraint = pymunk.Circle(space.static_body, radius, offset)
        constraint.elasticity = 0.1
        constraint.friction = 0.5
        space.add(constraint)


normal_distribution_hourglass = NormalDistributionHourglass()
normal_distribution_hourglass.run()
