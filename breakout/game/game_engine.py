"""
GameEngine: owns the paddle, ball, and bricks.

Task 1:
- Fix brick destruction.

Task 2:
- Add lives, game over, and restart.

Task 3:
- Add normal, strong, and unbreakable bricks.

Task 4:
- Add score and combo multiplier.
"""

import pygame

from game.paddle import Paddle
from game.ball import Ball
from game.brick import Brick
from game.collision import handle_ball_brick_collision
from game.renderer import WIDTH, HEIGHT

BRICK_ROWS = 4
BRICK_COLS = 8
BRICK_WIDTH = 68
BRICK_HEIGHT = 22
BRICK_GAP = 6
BRICK_TOP_MARGIN = 50

# Task 4
POINTS_PER_BRICK = 10


class GameEngine:
    def __init__(self):
        self.paddle = Paddle(
            x=WIDTH / 2,
            y=HEIGHT - 30
        )

        self.ball = Ball(
            x=WIDTH / 2,
            y=HEIGHT - 50
        )

        self.bricks = self._build_bricks()

        # Task 2
        self.lives = 3
        self.game_over = False

        # Task 4
        self.score = 0
        self.combo = 1

    def _build_bricks(self):
        bricks = []

        total_width = (
            BRICK_COLS * (BRICK_WIDTH + BRICK_GAP)
            - BRICK_GAP
        )

        start_x = (WIDTH - total_width) / 2

        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):

                x = start_x + col * (
                    BRICK_WIDTH + BRICK_GAP
                )

                y = BRICK_TOP_MARGIN + row * (
                    BRICK_HEIGHT + BRICK_GAP
                )

                # Task 3
                if row == 0:
                    brick_type = Brick.UNBREAKABLE

                elif row == 1:
                    brick_type = Brick.STRONG

                else:
                    brick_type = Brick.NORMAL

                bricks.append(
                    Brick(
                        x,
                        y,
                        BRICK_WIDTH,
                        BRICK_HEIGHT,
                        brick_type
                    )
                )

        return bricks

    def _reset_ball(self):
        self.ball = Ball(
            x=WIDTH / 2,
            y=HEIGHT - 50
        )

    def _restart_game(self):
        """
        Restart the complete game.
        """

        self.paddle = Paddle(
            x=WIDTH / 2,
            y=HEIGHT - 30
        )

        self.ball = Ball(
            x=WIDTH / 2,
            y=HEIGHT - 50
        )

        self.bricks = self._build_bricks()

        # Task 2
        self.lives = 3
        self.game_over = False

        # Task 4
        self.score = 0
        self.combo = 1

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        dx = 0

        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed

        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed

        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):
        # Task 2
        if self.game_over and key == pygame.K_r:
            self._restart_game()

    def update(self):
        if self.game_over:
            return

        self.ball.update()

        self.ball.bounce_off_walls(WIDTH)

        # Paddle collision
        if (
            self.ball.get_rect().colliderect(
                self.paddle.get_rect()
            )
            and self.ball.vy > 0
        ):
            self.ball.bounce_off_paddle(
                self.paddle.get_rect()
            )

        # Brick collision
        for brick in self.bricks:

            if handle_ball_brick_collision(
                self.ball,
                brick
            ):

                # Unbreakable bricks never lose durability
                if brick.is_breakable():

                    brick.hits_remaining -= 1

                    # Brick has been completely destroyed
                    if brick.hits_remaining <= 0:

                        # Task 4:
                        # Award points only when the brick
                        # is actually destroyed.
                        self.score += (
                            POINTS_PER_BRICK * self.combo
                        )

                        # Increase combo for the next
                        # consecutive brick destruction.
                        self.combo += 1

                        # Task 1:
                        # Remove destroyed brick.
                        self.bricks.remove(brick)

                break

        # Ball missed the paddle
        if self.ball.is_below(HEIGHT):

            # Task 2
            self.lives -= 1

            # Task 4:
            # Missing the ball resets the combo.
            self.combo = 1

            if self.lives <= 0:
                self.game_over = True

            else:
                self._reset_ball()

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.paddle,
            self.ball,
            self.bricks
        )

        # Existing brick counter
        renderer.draw_text(
            surface,
            font,
            f"Bricks left: {len(self.bricks)}",
            (10, 10)
        )

        # Task 2
        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 35)
        )

        # Task 4
        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 60)
        )

        renderer.draw_text(
            surface,
            font,
            f"Combo: {self.combo}x",
            (10, 85)
        )

        # Task 2
        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                "GAME OVER - Press R to Restart"
            )