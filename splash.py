# Displays the splash
# importing required library
import pygame
import time
 
# activate the pygame library .
pygame.init()
RES = (1280, 720)
 
# create the display surface object
# of specific dimension..e(X, Y).
scrn = pygame.display.set_mode(RES)
 
# set the pygame window name
pygame.display.set_caption('Splash Image')
 
# create a surface object, image is drawn on it.
imp = pygame.image.load("logo.jpg").convert()
imp = pygame.transform.scale(imp, RES)
 
# Using blit to copy content from one surface to other
scrn.blit(imp, (0, 0))
 
# paint screen one time
pygame.display.flip()


time.sleep(5)
 
# deactivates the pygame library
pygame.quit()
