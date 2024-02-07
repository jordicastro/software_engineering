# This is Nicholas's Branch
# Below is an implementation of Pong with Pygames
# Only for testing purposes

import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20
PADDLE_SPEED = 10
BALL_SPEED = 5
CENTER_WIDTH = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class PongGame:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.paddle_width = PADDLE_WIDTH
        self.paddle_height = PADDLE_HEIGHT
        self.ball_size = BALL_SIZE
        self.paddle_speed = PADDLE_SPEED
        self.ball_speed = BALL_SPEED
        self.left_paddle = pygame.Rect(50, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.right_paddle = pygame.Rect(WIDTH - PADDLE_WIDTH - 50, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect((WIDTH - BALL_SIZE) // 2, (HEIGHT - BALL_SIZE) // 2, BALL_SIZE, BALL_SIZE)
        self.ball_direction = random.choice([1, -1])
        self.ball_speed_x = BALL_SPEED * self.ball_direction
        self.ball_speed_y = BALL_SPEED * random.choice([1, -1])
        self.center_width = pygame.Rect(WIDTH // 2, 0, CENTER_WIDTH, HEIGHT)

        self.left_wins = 0
        self.right_wins = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        # Move paddles
        keys = pygame.key.get_pressed()
        # Left paddle
        if keys[pygame.K_w] and self.left_paddle.y > 0:
            self.left_paddle.y -= self.paddle_speed
        if keys[pygame.K_s] and self.left_paddle.y < HEIGHT - PADDLE_HEIGHT:
            self.left_paddle.y += self.paddle_speed
        # Right paddle
        if keys[pygame.K_UP] and self.right_paddle.y > 0:
            self.right_paddle.y -= self.paddle_speed
        if keys[pygame.K_DOWN] and self.right_paddle.y < HEIGHT - PADDLE_HEIGHT:
            self.right_paddle.y += self.paddle_speed

        # Move ball
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        # Ball collisions with paddles
        if self.ball.colliderect(self.left_paddle) or self.ball.colliderect(self.right_paddle):
            self.ball_speed_x *= -1.1

        # Ball collisions with walls
        if self.ball.y <= 0 or self.ball.y >= HEIGHT - BALL_SIZE:
            self.ball_speed_y *= -1

        # Ball goes out of bounds (score point)
        if self.ball.x < 0 or self.ball.x > WIDTH:
            if self.ball.x < 0:
                self.right_wins += 1
            if self.ball.x > WIDTH:
                self.left_wins += 1
            self.ball.x = (WIDTH - BALL_SIZE) // 2
            self.ball.y = (HEIGHT - BALL_SIZE) // 2
            self.ball_speed_x = BALL_SPEED * self.ball_direction
            self.ball_speed_y = BALL_SPEED * random.choice([1, -1])

    def draw(self, screen):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, self.left_paddle)
        pygame.draw.rect(screen, WHITE, self.right_paddle)
        pygame.draw.rect(screen, WHITE, self.center_width)
        pygame.draw.ellipse(screen, RED, self.ball)

def print_text(text, x, y, color):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")
font = pygame.font.Font(None, 36)

# Main code
def main():

    pong_game = PongGame()
    clock = pygame.time.Clock()

    while True:
        pong_game.handle_events()
        pong_game.update()
        pong_game.draw(screen)

        print_text(f"Left: {pong_game.left_wins}", WIDTH // 2 - 100, HEIGHT - 30, WHITE)
        print_text(f"Right: {pong_game.right_wins}", WIDTH // 2 + 30, HEIGHT - 30, WHITE)

        pygame.display.flip()
        clock.tick(60)

    

if __name__ == "__main__":
    main()
