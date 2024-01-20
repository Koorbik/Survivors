from csv import reader
from os import walk
import pygame


def import_csv(path):
    """
    This function reads a CSV file and returns a list of lists representing the CSV data.

    :param path: The path to the CSV file.
    :return: A list of lists where each inner list represents a row in the CSV file.
    """
    terrain = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain.append(list(row))
        return terrain


def import_folder(path):
    """
    This function reads all image files in a directory and returns a list of Pygame surfaces representing the images.

    :param path: The path to the directory containing the image files.
    :return: A list of Pygame surfaces where each surface represents an image file in the directory.
    """
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    return surface_list
