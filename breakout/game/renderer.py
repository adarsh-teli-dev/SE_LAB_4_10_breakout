"""
renderer: all pygame drawing lives here.

Task 3:
- Different brick types have different appearances.

Task 4:
- Score and combo are displayed by GameEngine.draw().
"""

import pygame


WIDTH, HEIGHT = 640, 520
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (20, 20, 30)
COLOR_PADDLE = (80, 180, 255)
COLOR_BALL = (240, 240, 240)
COLOR_TEXT = (255, 255, 255)

# Task 3: brick colors
COLOR_NORMAL_BRICK = (80, 180, 255)
COLOR_STRONG_BRICK = (255, 165, 0)
COLOR_UNBREAKABLE_BRICK = (150, 150, 150)

COLOR_BRICK_BORDER = (10, 10, 15)


def draw_brick(surface, brick):
    """
    Draw a brick according to its type.
    """

    if brick.brick_type == "normal":
        color = COLOR_NORMAL_BRICK

    elif brick.brick_type == "strong":
        color = COLOR_STRONG_BRICK

    elif brick.brick_type == "unbreakable":
        color = COLOR_UNBREAKABLE_BRICK

    else:
        color = COLOR_NORMAL_BRICK

    rect = brick.get_rect()

    pygame.draw.rect(
        surface,
        color,
        rect
    )

    pygame.draw.rect(
        surface,
        COLOR_BRICK_BORDER,
        rect,
        1
    )


def draw_scene(surface, paddle, ball, bricks):
    """
    Draw the complete game scene.
    """

    surface.fill(COLOR_BG)

    # Draw bricks
    for brick in bricks:
        draw_brick(
            surface,
            brick
        )

    # Draw paddle
    pygame.draw.rect(
        surface,
        COLOR_PADDLE,
        paddle.get_rect(),
        border_radius=4
    )

    # Draw ball
    pygame.draw.circle(
        surface,
        COLOR_BALL,
        (
            int(ball.x),
            int(ball.y)
        ),
        ball.radius
    )


def draw_text(
    surface,
    font,
    text,
    pos,
    color=COLOR_TEXT
):
    """
    Draw text on the screen.
    """

    surface.blit(
        font.render(
            text,
            True,
            color
        ),
        pos
    )


def draw_banner(surface, font, text):
    """
    Draw a centered banner, used for GAME OVER.
    """

    surf = font.render(
        text,
        True,
        (255, 220, 80)
    )

    rect = surf.get_rect(
        center=(
            surface.get_width() // 2,
            surface.get_height() // 2
        )
    )

    surface.blit(
        surf,
        rect
    )