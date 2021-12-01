import pygame
import pymunk
import pymunk.pygame_util
from random import randrange


class NormalDistributionHourglass(object):
    def __init__(self):
        pygame.init()
        self.space = pymunk.Space()
        self.space.gravity = (0, 8000)
        self.screen_size = 750
        self.screen = pygame.display.set_mode(
            (self.screen_size, self.screen_size)
        )
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True
        self.fps = 50
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
        for _ in range(450):
            self.create_ball()

        self.create_segment()

        temp = 25
        for i in range(100, self.screen_size, 50):
            self.create_constraint((i-temp, 250))
            self.create_constraint((i, 300))
            self.create_constraint((i-temp, 350))
            self.create_constraint((i, 400))

    def create_ball(self):
        balls = []
        mass = 1
        radius = 7
        offset = 50
        inertia = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, inertia)
        x = randrange(offset, self.screen_size-offset)
        y = randrange(0, offset)
        body.position = x, y
        ball = pymunk.Circle(body, radius)
        ball.elasticity = 0.1
        ball.friction = 0.8
        ball.color = pygame.color.THECOLORS['darkolivegreen2']
        self.space.add(body, ball)
        balls.append(ball)

    def create_segment(self):
        radius = 3
        offset1 = 150
        positions = [
            ((0, self.screen_size), (self.screen_size, self.screen_size)),
            ((0, 0), (0, offset1/2)),
            ((self.screen_size, 0), (self.screen_size, offset1/2)),
            ((0, offset1/2), (self.screen_size/2 - offset1/2, offset1)),
            ((self.screen_size, offset1/2), (self.screen_size/2 + offset1/2, offset1))
        ]
        offset2 = 100
        for i in range(0, 400, 50):
            positions.append(((self.screen_size/2 - i, self.screen_size/2 + offset2),
                              (self.screen_size/2 - i, self.screen_size)))
            positions.append(((self.screen_size/2 + i, self.screen_size/2 + offset2),
                              (self.screen_size/2 + i, self.screen_size)))
        for position in positions:
            segment = pymunk.Segment(
                self.space.static_body, position[0], position[1], radius
            )
            segment.elasticity = 0.5
            segment.friction = 1
            segment.color = pygame.color.THECOLORS['brown']
            self.space.add(segment)

    def create_constraint(self, offset):
        radius = 10
        constraint = pymunk.Circle(self.space.static_body, radius, offset)
        constraint.elasticity = 0.1
        constraint.friction = 0.5
        constraint.color = pygame.color.THECOLORS['brown1']
        self.space.add(constraint)


normal_distribution_hourglass = NormalDistributionHourglass()
normal_distribution_hourglass.run()
pygame.quit()
