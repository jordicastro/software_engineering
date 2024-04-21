import pygame
import time
import os
import sys

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)

class TextScroll:
    def __init__(self, area, font, fg_color, bk_color, text, ms_per_line=800):
        """object to display lines of text scrolled in with a delay between each line
        in font and fg_color with background o fk_color with in the area rect"""

        super().__init__()
        self.rect = area.copy()
        self.fg_color = fg_color
        self.bk_color = bk_color
        self.size = area.size
        self.surface = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        self.surface.fill(bk_color)
        self.font = font
        self.lines = text.split('\n')
        self.ms_per_line = ms_per_line
        self.y = 0
        self.y_delta = self.font.size("M")[1]
        self.next_time = None
        self.dirty = False

    def _update_line(self, line):  # render next line if it's time
        if self.y + self.y_delta > self.size[1]:  # line does not fit in remaining space
            self.surface.blit(self.surface, (0, -self.y_delta))  # scroll up
            self.y += -self.y_delta  # backup a line
            pygame.draw.rect(self.surface, self.bk_color,
                             (0, self.y, self.size[0], self.size[1] - self.y))

        text = self.font.render(line, True, self.fg_color)
        # pygame.draw.rect(text, GREY, text.get_rect(), 1)  # for demo show render area
        self.surface.blit(text, (0, self.y))

        self.y += self.y_delta

    # call update from pygame main loop
    def update(self):

        time_now = time.time()
        if (self.next_time is None or self.next_time < time_now) and self.lines:
            self.next_time = time_now + self.ms_per_line / 1000
            line = self.lines.pop(0)
            self._update_line(line)
            self.dirty = True
            self.update()  # do it again to catch more than one event per tick

    # call draw from pygam main loop after update
    def draw(self, screen):
        if self.dirty:
            screen.blit(self.surface, self.rect)
            self.dirty = False


# Test this Class

STORY1 = """FIRST LINE OF TEXT
second line of text
third line of text
** last line of text that fits
this line should force scroll up
and here again for
each line the follows"""

def example1():
    # start up pygame
    os.environ['SDL_VIDEO_WINDOW_POS'] = "1000,100"
    pygame.init()
    # print(sorted(pygame.font.get_fonts()))
    screen = pygame.display.set_mode((505, 250))
    screen.fill(GREY)
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Liberation Sans", 30)
    area = pygame.Rect(20, 20, 400, 142)
    box = area.inflate(2, 2)
    pygame.draw.rect(screen, BLUE, box, 1)
    pygame.display.flip()
    pygame.time.delay(500)
    message = TextScroll(area, font, BLACK, WHITE, STORY1, ms_per_line=500)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        else:
            # screen.fill(pygame.color.Color('black'))
            message.update()
            message.draw(screen)
            pygame.display.flip()
            clock.tick(60)

STORY2 = """No man is an island,
Entire of itself,
Every man is a piece of the continent,
A part of the main.

If a clod be washed away by the sea,
Europe is the less.
As well as if a promontory were.
As well as if a manor of thy friend’s

Or of thine own were:
Any man’s death diminishes me,
Because I am involved in mankind,
And therefore never send to 
know for whom the bell tolls;
It tolls for thee.
  -- John Donne (Year 1624 AD)"""


def example2():
    # start up pygame
    os.environ['SDL_VIDEO_WINDOW_POS'] = "840,500"
    pygame.init()
    # print(sorted(pygame.font.get_fonts()))
    screen = pygame.display.set_mode((1150, 480))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Liberation Sans", 65)
    message = TextScroll(pygame.Rect(25, 0, 1100, 460), font, YELLOW, BLACK, STORY2, ms_per_line=300)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        else:
            # screen.fill(pygame.color.Color('black'))
            message.update()
            message.draw(screen)
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    example1()