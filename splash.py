# importing required library
import pygame
import time
 
# activate the pygame library .
pygame.init()

# create the display surface object
# of specific dimension..e(X, Y).
screen = pygame.display.set_mode()
 
# set the pygame window name
pygame.display.set_caption('Splash Image')
 
# create a surface object, image is drawn on it.
imp = pygame.image.load("logo.jpg").convert()
imp = pygame.transform.scale(imp, (screen.get_size()))
 
# Using blit to copy content from one surface to other
screen.blit(imp, (0, 0))
 
# paint screen one time
pygame.display.flip()

# stays open for 5 seconds
time.sleep(5)
 
# deactivates the pygame library
pygame.quit()
