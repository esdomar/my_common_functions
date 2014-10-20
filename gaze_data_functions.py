'''
Functions implemented:
    Opening data:
        - dtype_sdk_gazedata():
        - open_gaze_data(file_path):
    Looking for samples:
        - find_timestamp(timestamp_array, timestamp):
        - num_samples(sampling_rate, time):
    Percentage of data:
        - per_valid_et_data(validity_right, validity_left):
        - per_valid_et_data_both_eyes_found(validity_right, validity_left):
        - per_inside_aoi(x, y, aoi, distance):
        -per_outside_screen(
    Eye average:
    - eye_average(left_eye, right_eye, validity_left, validity_right ):
    - select_average_value(left_eye, right_eye, validity_left, validity_right):
    Transforming data:
        - distance_pixels(x1, y1, x2, y2):
    Preprocessing:
        -


'''

import numpy as np
import math


def dtype_sdk_gazedata():
    """
        Returns the data type necessary to import raw ET data in a numpy array
    """
    dt = np.dtype([('Trigger', np.int), ('ET_timestamp', np.int64), ('Local_timestamp', np.int64),
                 ('Left', [('Eye_x',np.float_), ('Eye_y', np.float_), ('Eye_z', np.float_),
                 ('Eye_rel_x', np.float_), ('Eye_rel_y', np.float_), ('Eye_rel_z', np.float_),
                 ('x', np.float_), ('y', np.float_), ('x_3d',np.float_), ('y_3d', np.float_),
                 ('z_3d', np.float_), ('Pupil', np.float_), ('Validity', np.int)]),('Right', [('Eye_x', np.float_),
                 ('Eye_y', np.float_), ('Eye_z', np.float_),('Eye_rel_x',np.float_), ('Eye_rel_y', np.float_),
                 ('Eye_rel_z', np.float_), ('x', np.float_), ('y', np.float_), ('x_3d', np.float_), ('y_3d', np.float_),
                 ('z_3d', np.float_), ('Pupil', np.float_), ('Validity', np.int)])])
    
    return dt
    
    
def open_gaze_data(file_path):
    dt_gaze_data = dtype_sdk_gazedata()
    return np.loadtxt(file_path, dtype=dt_gaze_data,  delimiter="\t", skiprows=1, ndmin=1)


def find_timestamp(timestamp_array, timestamp):
    """
        Returns the index of the closest timestamp in the ET gaze data
        Used to find the row of the closest ET sample of every stimuli onset
        Returns -1 if the timestamp provided is not within the list of timestamps given
    """
    #import pdb; pdb.set_trace()
    if timestamp < timestamp_array[0] or timestamp > timestamp_array[-1]:
        raise ValueError('Timestamp provided is not within the ET samples')
    value = timestamp
    for i, item in enumerate(timestamp_array):
        if abs(item-timestamp) > value:
            return i - 1
        else:
            value = abs(item-timestamp)
    return -1


def num_samples(sampling_rate, time):
    '''
        Returns the number of samples of a given duration depending on the sampling rate.
    '''
    time = time/float(1000)
    return int(round(sampling_rate*time, 0))
    
    
def per_valid_et_data(validity_right, validity_left):
    '''
        Returns the percentage of valid ET data.
        Any sample where some et data was found will be returned, it doesnt matter what code
    '''
    return round(((len(validity_right) - len([i for i,right in enumerate(validity_right) if right == 4 and validity_left[i] == 4 ]) )  /float(len(validity_right)) )*100, 2)


def per_valid_et_data_both_eyes_found(validity_right, validity_left):
    '''
        Returns the percentage of valid ET data.
        Only samples where both eyes were found correctly.
    '''
    return round(len([i for i,right in enumerate(validity_right) if right == 0 and validity_left[i] == 0 ])/float(len(validity_right))*100, 2)


def eye_average(left_eye, right_eye, validity_left, validity_right ):
    '''
    input: number or list of eye and validity samples.
    All the inputs have to have the same number of elements.
    The function calls "select_average_value" once or several times depending on the
    number of elemennts that is necessary to calculate the average for
    '''
    if type(left_eye) is list:
        if not all(len(lst) == len(left_eye) for lst in [right_eye, validity_right, validity_left]):
            raise ValueError('All the inputs must have the same lengtht')

        average = []
        for sample in range(0, len(left_eye), 1):
            average.append(select_average_value(left_eye[sample], right_eye[sample], validity_left[sample], validity_right[sample]))
    else:
        average = select_average_value(left_eye, right_eye, validity_left, validity_right)

    return average

def select_average_value(left_eye, right_eye, validity_left, validity_right):
    '''
    Returns a list with the average of both eyes:
    if both eyes are valid it returns the average
    if only one eye is valid it returns the value from that eye
    if no eye is valid it returns -1
    '''
    if validity_left == 0 and validity_right == 0:
        return (left_eye + right_eye)/float(2)
    elif validity_left == 4 and validity_right == 4:
        return -1
    elif validity_left == 4 or validity_left == 3:
        return right_eye
    elif validity_right == 4 or validity_right == 3:
        return left_eye
    else:
        return -1


def distance_pixels(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


def per_outside_screen(x, y, x_offset=0.5, y_offset=0.25, x_screen_max=1, y_screen_max=1, x_screen_min=0, y_screen_min=0):

    if type(x) is list and len(x) != len(y):
            raise ValueError('X and Y length must have equal lengths')

    outside = 0
    for i, xsample in enumerate(x):
        if xsample < x_screen_max + x_offset and y[i] < y_screen_max + y_offset:
            if xsample > -x_offset and y[i] > -y_offset:
                if (xsample > x_screen_max and xsample < x_screen_max + x_offset) or (y[i] > y_screen_max and y[i] < y_screen_max + y_offset) or \
                        (xsample < x_screen_min and xsample > -x_offset) or (y[i] < y_screen_min and y[i] > -y_offset):
                    if xsample != -1:
                        outside += 1
    try:
        return round((outside/float(len(x)))*100, 2)
    except:
        return 'error'


def per_inside_aoi(x, y, x_min=0, y_min= 0, x_max=1, y_max= 1):
    '''
    This functions only calculates percentage of data inside a square aoi
    input:  x, y: arrays of the same length with x and y coordinates in pixels
            aoi: center of the aoi
    output: percentage of the data passed to the function were the et data is inside the aoi
    '''
    if type(x) is list and len(x) != len(y):
            raise ValueError('X and Y length must have equal lengths')

    inside=0
    for i, xsample in enumerate(x):
        if xsample > x_min and xsample < x_max and y[i] > y_min and y[i] < y_max:
            inside += 1
    try:
        return round((inside/float(len(x)))*100,2)
    except:
        return 'error'