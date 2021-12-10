This readme is for using "boundary_detection.py". Step-by-step instructions on downloading and running the script.

Download instructions:

1. The files required to run this script efficiently can be obtained from the following Git repository: https://github.com/venuspgdm/GrassNet
2. The folder has the following structure:

    submission
        |_  boundary_detection.py
        |_  grass.py
        |_  readme.txt
        |_  raw_data
        |_  grassnet.ipynb (Not used in this boundary detect method)

3. Make sure that there is relevant python version available on your computer. (Checked on version: 3.7.4)
4. All modules used in this script need to be downloaded using pip if using an independent python shell. The modules used in this script are as follows:

    a. argparse
    b. os
    c. cv2 (opencv-python)
    d. sys
    e. numpy
    f. matplotlib

Aim of this script:

1. This script takes an image directly or a video as an input
2. Detects the boundary of the grass filled region
3. Draws a contour on the potential regions.
4. Outputs an image or video

Script run instructions:

1. This script is run by passing arguments. These areguments can be divided into two categories. (1) Direct (2) Flags. The direct arguments take a string as an input and the flag arguments take either 1 or 0 as input. The following arguments are available for this script:

    Direct arguments:
    -d   :   Current directory
    -i   :   Image name with extension or Video name with extension

    Flag arguments:
    -pf  :   Flag to notify if the image is coming from a video or a directory
    -rf  :   Flag to read and store all images in the directory
    -df  :   Flag to display plots
    -vf  :   Verbose flag

2. The following syntax can be used in the terminal opened in the directory where the files are downloaded:

    python3 boundary_detection.py -d <current directory> -i <image or video name> -pf <0/1> -rf <0/1> -df <0/1> -vf <0/1>

    E.g.: python3 boundary_detection.py -d /Users/venus_mac/Downloads/final_submission/raw_data/ -i IMG_8944.jpeg -pf 0 -rf 0 -df 0 -vf 0

Working of the script:

1. When an image is given as an input:
    a. Read the input image in BGR format
    b. Convert the image from BGR to HSV format
    c. The script uses the green color intensity values obtained from the HSV format to identify grass
    d. The image is then padded with empty pixels (This amount of padding can be changed in grass.py: "__init__")
    e. The image is then converted to binary based on the intensity values(Green-black, Nongreen-white)
    f. A method of image erosion and dilation is used to improve the quality of the image in binary
    g. This step is nevessary because the grass in an image is very noisy based on the brightness of the sun. As sometimes it appears white in certain angles.
    h. The erosion and dilation are done multiple times and with different kernel sizes.
    i. These iterations and kernel sizes can be modified in grass.py functions: "no_dilation_steps" and "no_erosion_steps"
    j. Contours are drawn on the modified image.
    k. Sometimes, the contours are drawn around small pathes of dry grass as they are not green in color.
    l. In order to avoid this, a minimum length of the contour to be drawn is set in grass.py function "contour_len_tresh"
    m. The final image with contours is saved in the current directory