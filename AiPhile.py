"""
-------------------------------------------
-    Author: Asadullah Dal                -
-    =============================        -
-    Company Name: AiPhile                -
-    =============================        -
-    Purpose : Youtube Channel            -
-    ============================         -
-    Link: https://youtube.com/c/aiphile  -
-------------------------------------------
"""
import os
import random

import cv2 as cv
import numpy as np


def get_random_rgb_color():
    """Returns a random RGB color."""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


def get_contrast(color1, color2):
    """Returns the contrast between two RGB colors."""
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return (255 * (r1 - r2) ** 2 + 255 * (g1 - g2) ** 2 + 255 * (b1 - b2) ** 2) ** 0.3


def get_list_of_random_rgb_colors_with_decent_contrast(number_of_colors):
    """Returns a list of random RGB colors with decent contrast."""
    list_of_colors = [(255, 255, 0)]
    for _ in range(number_of_colors):
        r, g, b = get_random_rgb_color()
        while get_contrast((r, g, b), list_of_colors[-1]) < 100:
            r, g, b = get_random_rgb_color()

        # color_list.append([(r, g, b), (br, bg, bb)])
        list_of_colors.append((r, g, b))
    return list_of_colors


def convert_flat_list_to_list_of_two_values(flat_list):
    """Converts a flat list into a list of two two-values lists."""
    list_of_two_values = []
    for i in range(0, len(flat_list), 2):
        sublist = flat_list[i : i + 2]
        list_of_two_values.append(sublist)
    return list_of_two_values


def read_images_from_dir(path, resize_flag=None):
    """
    Reads all images from a directory and returns a list of images.

    Args:
        path (str): The path to the directory containing the images.
        resize_flag (tuple): The resize flag for the images. If None, the images are not resized.

    Returns:
        list: A list of images.
    """

    images = []
    for file in os.listdir(path):
        img_path = os.path.join(path, file)
        img = cv.imread(img_path)
        if resize_flag:
            img = cv.resize(img, resize_flag, interpolation=cv.INTER_CUBIC)
        images.append(img)

    return images


def rect_corners(
    image, rect_points, color, DIV=6, th=2, opacity=0.3, draw_overlay=False
):
    x, y, w, h = rect_points
    top_right_corner = np.array(
        [[x + w // DIV, y], [x, y], [x, y + h // DIV]], dtype=np.int32
    )
    cv.rectangle(image, (x, y), (x + w, y + h), color, th // 2)
    cv.polylines(image, [top_right_corner], False, color, th)
    # top left corner
    top_left_corner = np.array(
        [[(x + w) - w // DIV, y], [x + w, y], [x + w, y + h // DIV]], dtype=np.int32
    )
    cv.polylines(image, [top_left_corner], False, color, th)

    # bottom right corner
    bottom_right_corner = np.array(
        [[x + w // DIV, y + h], [x, y + h], [x, (y + h) - h // DIV]], dtype=np.int32
    )
    cv.polylines(image, [bottom_right_corner], False, color, th)

    # bottom left corner

    bottom_left_corner = np.array(
        [[x + w, (y + h) - h // DIV], [x + w, y + h], [(x + w) - w // DIV, y + h]],
        dtype=np.int32,
    )
    if draw_overlay:
        overlay = image.copy()  # coping the image
        cv.rectangle(overlay, rect_points, color, -1)
        new_img = cv.addWeighted(overlay, opacity, image, 1 - opacity, 0)
        # print(points_list)
        image = new_img

    cv.polylines(image, [bottom_left_corner], False, color, th)

    # cv.circle(image, (x, y), 4, color, 2)
    # cv.circle(image, (x + w, y), 4, (0, 255, 0), 2)
    # cv.circle(image, (x, y + h), 4, (255, 0, 0), 2)
    # cv.circle(image, (x + w, y + h), 4, (0, 0, 255), 2)
    return image


def text_with_background(
    image,
    text,
    position=(30, 30),
    fonts=cv.FONT_HERSHEY_PLAIN,
    scaling=1,
    color=(0, 255, 255),
    bg_color=(0, 0, 0),
    th=1,
    draw_corners=True,
    up=0,
):
    image_h, image_w = image.shape[:2]
    x, y = position
    y = y - up
    (w, h), p = cv.getTextSize(text, fonts, scaling, th)
    cv.rectangle(image, (x - p, y + p), (x + w + p, y - h - p), bg_color, -1)

    if draw_corners:
        rect_points = [x - p, y - h - p, w + p + p, h + p + p]
        # cv.rectangle(image, rect_points, color=(0, 255, 0), thickness=2)
        rect_corners(image, rect_points, color, th=th, DIV=4)

    cv.putText(image, text, (x, y), fonts, scaling, color, th, cv.LINE_AA)


def fill_poly_trans(image, points, color, opacity):
    list_to_np_array = np.array(points, dtype=np.int32)
    overlay = image.copy()  # coping the image
    cv.fillPoly(overlay, [list_to_np_array], color)
    new_image = cv.addWeighted(overlay, opacity, image, 1 - opacity, 0)
    # print(points_list)
    image = new_image
    # cv.polylines(image, [list_to_np_array], True, color, 1, cv.LINE_AA)
    return image


def trans_circle(image, org, radi, color, opacity, outline=0):
    overlay = image.copy()  # coping the image
    cv.circle(overlay, org, radi, color, -1, cv.LINE_AA)
    new_image = cv.addWeighted(overlay, opacity, image, 1 - opacity, 0.1)
    # print(points_list)
    if outline > 0:
        cv.circle(new_image, org, radi, color, outline, cv.LINE_AA)

    image = new_image
    # cv.polylines(image, [list_to_np_array], True, color, 1, cv.LINE_AA)
    return image


if __name__ == "__main__":
    list_of_colors = get_list_of_random_rgb_colors_with_decent_contrast(10)
    list_of_colors.pop(0)
    list_of_colors = convert_flat_list_to_list_of_two_values(list_of_colors)
    fg_color, bg_color = list_of_colors[1]
    # for color in list_of_colors:
    #     print(color)
    # creating empty image using np
    image = np.zeros((800, 800, 3), dtype=np.uint8)
    # turn black color into white color image
    image[image == 0] = 255
    # Draw the transparent circle on the image
    image = trans_circle(image, (400, 400), 80, list_of_colors[2][0], 0.4, 4)
    # create rectangle with corners around that.
    image = rect_corners(image, [255, 255, 290, 290], (0, 0, 0), th=5)
    # Draw text with background
    text_with_background(
        image,
        f"AiPhile is all about Computer Vision",
        (30, 60),
        fonts=cv.FONT_HERSHEY_TRIPLEX,
        scaling=1.11,
        color=fg_color,
        bg_color=bg_color,
    )
    cv.imshow("image", image)
    cv.waitKey(0)
