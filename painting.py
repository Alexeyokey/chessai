import os

from PIL import Image


def figures_with_circles(name_of_folder):
    current_folder = name_of_folder
    figures = """bRbNbBbQbKbBbNbRbPwPwRwNwBwQwKwBwNwR"""
    im2 = Image.open('images/circle.png')
    for i in range(0, len(figures), 2):
        figure = figures[i:i + 2]
        figure_name = f'{figure}.png'
        if figure_name in os.listdir(f'sprites/{current_folder}'):
            im1 = Image.open(f'sprites/{current_folder}/{figure}.png')
            if im1.size == (80, 80):
                im1 = Image.open(f'sprites/{current_folder}/{figure}.png')
                im1 = im1.convert('RGBA')
                im1.paste(im2, (0, 0), mask=im2)
                im1.save(f'green/{figure}.png')
            else:
                return False
        else:
            return False
    return True
