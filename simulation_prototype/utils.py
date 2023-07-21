import pygame
import csv


class Node:
    """ A node class for any Grid-Based Pathfinding"""
    def __init__(self, coordinates: tuple, parent=None):
        self.coordinates = coordinates
        self.parent = parent

        self.g = self.h = self.f = 0

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def __hash__(self):
        return hash(self.coordinates)

    # for heap queue
    def __lt__(self, other):
        return self.f < other.f

    # for heap queue
    def __gt__(self, other):
        return self.f > other.f


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


def append_to_csv(filename, data):
    # Open the file in append mode
    with open(filename, 'a') as f:
        # Create a csv writer
        writer = csv.writer(f)
        # Write the data
        writer.writerow(data)