import pygame

def setup_module(module):
    pygame.init()

def teardown_module(module):
    pygame.quit()

def test_screen():
    X, Y = pygame.display.Info().current_w, pygame.display.Info().current_h
    assert X > 0
    assert Y > 0