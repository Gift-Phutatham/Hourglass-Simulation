import pygame
import pymunk
import pymunk.pygame_util
from random import randrange


def create_ball(space, mass, radius):
    temp = 50
    balls = []
    inertia = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, inertia)
    body.position = randrange(temp, screen_size-temp), randrange(0, temp)
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.1
    shape.friction = 0.1
    space.add(body, shape)
    balls.append(shape)


def create_segment(space, radius):
    temp1 = 150
    positions = [
        ((0, screen_size), (screen_size, screen_size)),
        ((0, 0), (0, temp1/2)),
        ((screen_size, 0), (screen_size, temp1/2)),
        ((0, temp1/2), (screen_size/2 - temp1/2, temp1)),
        ((screen_size, temp1/2), (screen_size/2 + temp1/2, temp1))
    ]
    temp2 = 100
    for i in range(0, 400, 50):
        positions.append(((screen_size/2 - i, screen_size/2 + temp2),
                          (screen_size/2 - i, screen_size)))
        positions.append(((screen_size/2 + i, screen_size/2 + temp2),
                          (screen_size/2 + i, screen_size)))
    for position in positions:
        segment = pymunk.Segment(
            space.static_body, position[0], position[1], radius
        )
        segment.elasticity = 0.5
        segment.friction = 1
        segment.color = pygame.color.THECOLORS['brown']
        space.add(segment)


def create_constraint(space, radius, offset):
    constraint = pymunk.Circle(space.static_body, radius, offset)
    constraint.elasticity = 0.1
    constraint.friction = 0.5
    space.add(constraint)


fps = 60
screen_size = 750
ball_mass = 1
ball_radius = 7

pygame.init()
screen = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)
space = pymunk.Space()
space.gravity = (0, 8000)

constraint_radius = 10
for i in range(100, screen_size, 50):
    create_constraint(space, constraint_radius, (i, 200))
    create_constraint(space, constraint_radius, (i-25, 250))
    create_constraint(space, constraint_radius, (i, 300))
    create_constraint(space, constraint_radius, (i-25, 350))

create_segment(space, 3)
for _ in range(750):
    create_ball(space, ball_mass, ball_radius)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color('black'))
    space.debug_draw(draw_options)
    for _ in range(10):
        space.step(1/60/10)
    pygame.display.flip()
    clock.tick(60)
