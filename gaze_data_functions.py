def dtype_sdk_gazedata():
    """
        Returns the data type necessary to import raw ET data in a numpy array
    """
    import numpy as np
    dt = np.dtype([('Trigger', np.int), ('ET_timestamp', np.int64), ('Local_timestamp',np.int64), 
                 ('Left', [('Eye_x',np.float_), ('Eye_y',np.float_), ('Eye_z',np.float_),
                 ('Eye_rel_x',np.float_), ('Eye_rel_y',np.float_), ('Eye_rel_z',np.float_), 
                 ('x',np.float_), ('y', np.float_), ('x_3d',np.float_), ('y_3d', np.float_), 
                 ('z_3d', np.float_), ('Pupil',np.float_), ('Validity', np.int)]),('Right', [('Eye_x',np.float_), 
                 ('Eye_y',np.float_), ('Eye_z',np.float_),('Eye_rel_x',np.float_), ('Eye_rel_y',np.float_), 
                 ('Eye_rel_z',np.float_), ('x',np.float_), ('y', np.float_), ('x_3d',np.float_), ('y_3d', np.float_),                 
                 ('z_3d', np.float_), ('Pupil',np.float_), ('Validity', np.int)])])
    
    return dt
    
    
def find_timestamp(timestamp_array, timestamp):
    """
        Returns the index of the closest timestamp in the ET gaze data
        Used to find the row of the closest ET sample of every stimuli onset
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
    return round(len([i for i,right in enumerate(validity_right) if right != 4 and validity_left[i] != 4 ])/float(len(validity_right))*100, 2)


def per_valid_et_data_both_eyes_found(validity_right, validity_left):
    '''
        Returns the percentage of valid ET data.
        Only samples where both eyes were found correctly.
    '''
    return round(len([i for i,right in enumerate(validity_right) if right == 0 and validity_left[i] == 0 ])/float(len(validity_right))*100, 2)