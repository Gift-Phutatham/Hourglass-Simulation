import random
import pygame
import pymunk
import pymunk.pygame_util


class HourGlass(object):
    def __init__(self):
        self.gravity = float(input("Gravity: "))
        self.friction = float(input("Friction of the hourglass: "))
        self.number_of_balls = int(input("Number of the balls: "))
        self.ball_mass = float(input("Mass of the ball: "))
        self.ball_radius = float(input("Radius of the ball: "))
        self.ball_elasticity = float(input("Elasticity of the ball: "))

        pygame.init()
        self.space = pymunk.Space()
        self.space.gravity = (0, self.gravity)
        self.screen_size = 750
        self.screen = pygame.display.set_mode(
            (self.screen_size, self.screen_size)
        )
        self.running = True
        self.dt = 1/50
        self.steps_per_frame = 1
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        self.one_quarter = self.screen_size/4
        self.between_quarters1 = 1.75*self.screen_size/4
        self.one_half = self.screen_size/2
        self.between_quarters2 = 2.25*self.screen_size/4
        self.three_quarter = 3*self.screen_size/4

        self.create_glass_component()
        self.barrier = self.create_barrier()

    def run(self):
        for _ in range(self.number_of_balls):
            self.create_ball()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if self.barrier != None:
                            self.space.remove(self.barrier, self.barrier.body)
                            self.barrier = None
            self.screen.fill((31, 40, 57))
            self.space.debug_draw(self.draw_options)
            for _ in range(10):
                self.space.step(self.dt/10)
            pygame.display.flip()
            self.clock.tick(50)

    def create_glass_component(self):
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
            segment.elasticity = 0.5
            segment.friction = self.friction
            self.space.add(segment)

    def create_ball(self):
        balls = []
        inner_radius = 0
        offset = (0, 0)
        inertia = pymunk.moment_for_circle(
            self.ball_mass, inner_radius, self.ball_radius, offset
        )
        body = pymunk.Body(self.ball_mass, inertia)
        x = random.randint(int(self.one_quarter + self.ball_radius),
                           int(self.three_quarter - self.ball_radius))
        y = self.one_quarter + self.ball_radius
        body.position = x, y
        shape = pymunk.Circle(body, self.ball_radius, (0, 0))
        shape.elasticity = self.ball_elasticity
        shape.friction = 1
        self.space.add(body, shape)
        balls.append(shape)

    def create_barrier(self):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (self.one_half, self.one_half)
        shape = pymunk.Poly.create_box(
            body, (abs(self.between_quarters2-self.between_quarters1), 5)
        )
        self.space.add(body, shape)
        return shape


hour_glass = HourGlass()
hour_glass.run()
