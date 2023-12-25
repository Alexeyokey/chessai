import os

from PIL import Image


def figures_with_circles(name_of_folder):
    current_folder = name_of_folder
    figures = """bRbNbBbQbKbBbNbRbPwPwRwNwBwQwKwBwNwR"""
    im2 = Image.open('images/figure_circle.png')
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


# def figures_with_circles(n, name):
#     with Image.open(name) as img:
#         for i in range(n):
#             for j in range(n):
#                 new_img = img.crop((j * 80, i * 80, j * 80 + 80, i * 80 + 80))
#                 new_img.save(f"board/{i}{j}.png")
#
# figures_with_circles(8, "board.png")