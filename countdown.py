# importing required library
import pygame,time, sys, os, random
from server import Server

os.environ['SDL_VIDEO_CENTERED'] = '1'

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

def countdown(server: Server):
    # activate the pygame library .
    pygame.init()

    # create the display surface object
    # of specific dimension..e(X, Y).
    screen = pygame.display.set_mode((600,480))

    # set the pygame window name
    pygame.display.set_caption('Countdown')

    # create a surface object, image is drawn on it.
    images: pygame.image = []
    for i in range(31):
        temp = pygame.image.load("resources/countdown_images/" + str(i) + ".tif").convert()
        images.append(temp)
    background = pygame.image.load("resources/countdown_images/background.tif").convert()


    # Using blit to copy content from one surface to other
    screen.blit(background, (0, 0))

    # paint screen one time
    pygame.display.flip()

    clock = pygame.time.Clock()
    i = len(images) - 1 #starting index
    start_time = time.time()
    while time.time() - start_time < 30:
        events()
        timerNum = images[i]
        timerNumWidth = background.get_width()/2-images[i].get_width()/2
        timerNumHeight = background.get_height()/2 - 18

        screen.blit(timerNum, (timerNumWidth, timerNumHeight))
        pygame.display.flip()
        clock.tick(1)
        if(i == 16):
            # ~ Music ~
            tracks = os.listdir('resources/photon_tracks')

            # Select a random track
            track = random.choice(tracks)
    

            # Load and play the track
            pygame.mixer.music.load(os.path.join('resources/photon_tracks', track))
            pygame.mixer.music.play()

        i = i-1

    server.start_traffic()