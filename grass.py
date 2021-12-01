import numpy as np


class Grass:
    '''
    Grass class is used to maintain the constants and thresholds for grass boundary detection
    '''
    
    def __init__(self, pad_size=10):
        '''
            This function sets the padding size for the image. Default value is 10.
        '''
        self.pad_size = pad_size

    def get_padsize(self):
        '''
            This function returns the padsize for the image.
        '''
        return self.pad_size

    def get_min_green_intensity(self):
        '''
            This function is used to set the minimum intensity values of the green color.
            Modify intensity value as per requirement (For different color)
        '''
        intensity = 38
        return intensity

    def get_max_green_intensity(self):
        '''
            This function is used to set the maximum intensity values of the green color.
            Modify intensity value as per requirement (For different color)
        '''
        intensity = 83
        return intensity

    def no_dilation_steps(self):
        '''
            This function is used to set the minimum intensity values of the green color.
            Modify steps as per required no. of iterations
            Modify kernel_size with which dilation needs to be done
        '''
        steps = 20
        kernel_size = 3
        return np.ones((kernel_size, kernel_size), np.uint8), steps

    def no_erosion_steps(self):
        '''
            This function is used to set the minimum intensity values of the green color.
            Modify steps as per required no. of iterations
            Modify kernel_size with which dilation needs to be done
        '''
        steps = 35
        kernel_size = 7
        return np.ones((kernel_size, kernel_size), np.uint8), steps

    def contour_len_tresh(self):
        '''
            This function is used to set the threshold for minimum contour length for which the boundary can be drawn. 
        '''
        return 10000
