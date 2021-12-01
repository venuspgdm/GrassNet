"""
Project : GrassNet - An independent tool to detect grass and its boundaries from background.
Aim     : Detect boundaries of the grass in the given image
Author : Venus Pagidimarri
Version : 1.0
Date    : November 24th, 2021

Inputs:
    1. -pf  :   Flag to notify if the image is coming from a video or a directory
    2. -d   :   Current directory
    3. -i   :   Image name
    4. -rf  :   Flag to read all images in the directory
    5. -df  :   Flag to display plots
    6. -vf  :   Verbose flag

Output:
    1. Image with boundary around grass
    
"""

import argparse
import os
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from grass import Grass

# parser holds all the input arguments
parser = argparse.ArgumentParser(description='Detect boundaries of the grass in the given image')
parser.add_argument('-pf', '--pathFlag', type=int, required=True,
                    help='Flag to notify if the image is coming from a video or a directory')
parser.add_argument('-d', '--file_dir', type=str, required=True, help='Current directory')
parser.add_argument('-i', '--img_name', type=str, required=False, help='Image name')
parser.add_argument('-rf', '--readfileFlag', type=int, required=True, help='Flag to read all images in the directory')
parser.add_argument('-df', '--displayPlotFlag', type=int, required=True, help='Flag to display plots')
parser.add_argument('-vf', '--verboseFlag', type=int, required=False, help='verbose flag')

args = parser.parse_args()

# Photos holds the path to the raw data
Photos = args.file_dir

if args.readfileFlag:
    if os.path.isdir(args.file_dir):
        
        # lists holds all the image names from the input directory
        lists = []
        for file_name in os.listdir(Photos):
            image_array = cv2.imread(Photos + file_name)
            lists.append(image_array)
    else:
        sys.exit('Error: Folder not Found!')


if args.pathFlag:

    # bound_detect is an object of grass class
    bound_detect = Grass(10)

    if not os.path.isfile(Photos + args.img_name):
        sys.exit('Error: File not found in the provided directory!')

    image_array = cv2.imread(Photos + args.img_name, 1)
    hsv = cv2.cvtColor(image_array, cv2.COLOR_BGR2HSV)

    pad_size = bound_detect.get_padsize()
    BLACK = [0, 0, 0]
    image_color_pad = cv2.copyMakeBorder(image_array, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_CONSTANT,
                                         value=BLACK)

    hue = hsv[:, :, 0]
    hue_binary = (hue[:, :] < bound_detect.get_max_green_intensity()) * (
            hue[:, :] > bound_detect.get_min_green_intensity())
    hue_numbers = hue_binary.astype(np.uint8)
    constant = hue_numbers * 255

    kernel_small = bound_detect.no_dilation_steps()[0]
    kernel_big = bound_detect.no_erosion_steps()[0]
    img_dilation = cv2.dilate(constant, kernel_small, iterations=bound_detect.no_dilation_steps()[1])  # usually 20
    img_erosion = cv2.erode(img_dilation, kernel_big, iterations=bound_detect.no_erosion_steps()[1])  # usually 35

    # Padding the eroded image to create a black frame around it (enclosing it)
    hue_numbers = cv2.copyMakeBorder(img_erosion, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_CONSTANT, value=0)

    # Thresholding the image
    ret, thresh = cv2.threshold(hue_numbers, 200, 240, cv2.THRESH_BINARY)  # Convert to binary graph

    #  Contour detection The first one is the result of the binary value, the second is a bunch of contour points, and the third is the level.
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #  Contour feature
    print('No. of contours: ', len(contours))

    if args.verboseFlag:
        for i, cnt in enumerate(contours):
            print('Contour: ', i)
            print('\tArea: ', cv2.contourArea(cnt))  # Calculated area
            print('\tPerimeter', cv2.arcLength(cnt, True))  # Calculate the perimeter, True means closed

    #  Draw contour
    draw_img = image_color_pad.copy()

    cnt_no = 0
    for i, cnt in enumerate(contours):
        if cv2.arcLength(cnt, True) > bound_detect.contour_len_tresh():
            cnt_no = cnt_no+1
            res = cv2.drawContours(draw_img, contours, i, (0, 0, 255), 50)

    print('No. of contours drawn: ', cnt_no)

    # Display images
    plt.subplot(151), plt.imshow(cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)), plt.title('Original')
    plt.xticks([]), plt.yticks([])

    plt.subplot(152), plt.imshow(hue_binary, cmap='gray'), plt.title('Hue thresold')
    plt.xticks([]), plt.yticks([])

    plt.subplot(153), plt.imshow(img_dilation, cmap='gray'), plt.title('Dilated')
    plt.xticks([]), plt.yticks([])

    plt.subplot(154), plt.imshow(img_erosion, cmap='gray'), plt.title('Eroded')
    plt.xticks([]), plt.yticks([])

    plt.subplot(155), plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB)), plt.title('Contoured')
    plt.xticks([]), plt.yticks([])

    plt.savefig('image_contour_8962.png')

    if args.displayPlotFlag:
        plt.show()
