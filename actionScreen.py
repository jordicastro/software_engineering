from splash import splashScreen
from gui import InputBox, InputLine, Button
from database import Database
import pygame, sys, socket

# pygame setup

# Main game loop
def events():
    # Check for events
    for event in pygame.event.get():
        # Check for the quit event
        if event.type == pygame.QUIT:
            # Quit the game
            pygame.quit()
            sys.exit()
        # Check for the fullscreen toggle event
        if event.type == pygame.KEYDOWN:
            # Toggle fullscreen mode
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            # Check for the quit event
            if event.key == pygame.K_ESCAPE:
                # Quit the game
                pygame.quit()
                sys.exit()

def runGame():
    running = True
    pygame.init()
    desktop = pygame.display.Info()
    screen = pygame.display.set_mode((desktop.current_w-10, desktop.current_h-50))
    clock = pygame.time.Clock()

    #Screen coordinates
    X = int(screen.get_width())
    Y = int(screen.get_height())

    # Initializing Color
    red = (128, 23, 23)
    green = (17, 122, 13)

    # Create top half sections
    top_left_rect = pygame.Rect(0, 0, X // 2, Y // 2)
    top_right_rect = pygame.Rect(X // 2, 0, X // 2, Y // 2)

    # Create text boxes for code names and game scores
    code_names_textbox = InputBox(top_left_rect.x + 10, top_left_rect.y + 10, top_left_rect.width - 20, top_left_rect.height - 20)
    game_scores_textbox = InputBox(top_right_rect.x + 10, top_right_rect.y + 10, top_right_rect.width - 20, top_right_rect.height - 20)

    # Divide each rectangle into a 15 row by 2 column grid
    row_height = top_left_rect.height // 15
    column_width = top_left_rect.width // 2


    # Create bottom half section
    bottom_rect = pygame.Rect(0, Y // 2, X, Y // 2)

    # Create text box for game events
    game_events_textbox = InputBox(bottom_rect.x + 10, bottom_rect.y + 10, bottom_rect.width - 20, bottom_rect.height - 20)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill the screen with colors
        screen.fill(red, top_left_rect)
        screen.fill(green, top_right_rect)
        screen.fill((0, 0, 0), bottom_rect)

        # Draw text boxes
        code_names_textbox.draw(screen)
        game_scores_textbox.draw(screen)
        game_events_textbox.draw(screen)

        pygame.display.update()
        clock.tick(60)

