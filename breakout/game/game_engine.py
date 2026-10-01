"""
GameEngine: owns the paddle, ball, and bricks.

Task 1:
- Fix brick destruction so bricks are removed when their
  hit count reaches zero.

Task 2:
- Add 3 lives.
- Add game-over state.
- Add restart functionality using the R key.

Task 3:
- Add NORMAL, STRONG, and UNBREAKABLE brick types.
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

        # Task 2: lives and game-over state
        self.lives = 3
        self.game_over = False

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

                # Task 3:
                # First row    -> Unbreakable
                # Second row  -> Strong
                # Remaining   -> Normal

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
        Completely restart the game.

        Resets:
        - Paddle
        - Ball
        - Bricks
        - Lives
        - Game-over state
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

        self.lives = 3
        self.game_over = False

    def handle_input(self, keys_pressed):
        # Don't allow normal gameplay during GAME OVER
        if self.game_over:
            return

        dx = 0

        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed

        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed

        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):
        # Task 2:
        # Press R to restart after GAME OVER
        if self.game_over and key == pygame.K_r:
            self._restart_game()

    def update(self):
        # Stop the game completely during GAME OVER
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

                # Task 3:
                # Unbreakable bricks are never destroyed.
                if brick.is_breakable():

                    brick.hits_remaining -= 1

                    # Task 1:
                    # Remove brick when its durability reaches zero.
                    if brick.hits_remaining <= 0:
                        self.bricks.remove(brick)

                break

        # Ball missed the paddle
        if self.ball.is_below(HEIGHT):

            # Task 2:
            # Lose one life.
            self.lives -= 1

            if self.lives <= 0:
                # No lives remaining
                self.game_over = True

            else:
                # Continue with another life
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

        # Task 2: display lives
        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 35)
        )

        # Task 2: GAME OVER message
        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                "GAME OVER - Press R to Restart"
            )