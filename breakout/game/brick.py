"""
Brick: a single block.

Task 3 adds three brick types:
- NORMAL: destroyed after 1 hit
- STRONG: destroyed after 2 hits
- UNBREAKABLE: cannot be destroyed
"""

import pygame


class Brick:
    NORMAL = "normal"
    STRONG = "strong"
    UNBREAKABLE = "unbreakable"

    def __init__(
        self,
        x,
        y,
        width,
        height,
        brick_type=NORMAL
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.brick_type = brick_type

        if brick_type == self.NORMAL:
            self.hits_remaining = 1
            self.color = (80, 180, 255)

        elif brick_type == self.STRONG:
            self.hits_remaining = 2
            self.color = (255, 165, 0)

        elif brick_type == self.UNBREAKABLE:
            self.hits_remaining = None
            self.color = (150, 150, 150)

        else:
            raise ValueError(f"Unknown brick type: {brick_type}")

    def get_rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    def is_breakable(self):
        return self.brick_type != self.UNBREAKABLE