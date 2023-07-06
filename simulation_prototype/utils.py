import pygame


def create_surface(surface_size):
    surface = pygame.Surface(surface_size, pygame.SRCALPHA)
    return surface


def bound(value, lower_bound, upper_bound):
    if value < lower_bound:
        return lower_bound
    if value > upper_bound:
        return upper_bound
    else:
        return value
