import pygame, sys

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


# def render():
#         # Render background
#         game.background()

#         # Define the font for player names
#         font = pygame.font.Font(None, 36)

#         # Update and draw player lines and names for red players
#         for i, player in enumerate(game.red_players):
#             game.red_lines[i].setPlayer(player)
#             game.red_lines[i].draw(game.screen)
#             text = font.render(player, True, (255, 0, 0))  # Red color for red players
#             game.screen.blit(text, (10, i*40))  # Adjust the position as needed

#         # Update and draw player lines and names for green players
#         for i, player in enumerate(game.green_players):
#             game.green_lines[i].setPlayer(player)
#             game.green_lines[i].draw(game.screen)
#             text = font.render(player, True, (0, 255, 0))  # Green color for green players
#             game.screen.blit(text, (game.X - 100, i*40))  # Adjust the position as needed

#         # Draw input boxes
#         for box in game.input_boxes:
#             box.draw(game.screen)
        # Draw buttons

# pass in the game object from 
def runGame(redTeam,greenTeam):
    running = True
    pygame.init()
    desktop = pygame.display.Info()
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
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

    # Divide each rectangle into a 15 row by 2 column grid
    row_height = top_left_rect.height // 15
    column_width = top_left_rect.width // 2


    # Create bottom half section
    bottom_rect = pygame.Rect(0, Y // 2, X, Y // 2)

    # Create text box for game events

    while running:

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


        # Fill the screen with colors
        screen.fill(red, top_left_rect)
        screen.fill(green, top_right_rect)
        screen.fill((0, 0, 0), bottom_rect)
        #render(game)

        

        pygame.display.flip()
        
        clock.tick(60)



#runGame()