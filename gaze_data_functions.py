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
    value = timestamp
    for i, item in enumerate(timestamp_array):
        if abs(item-timestamp) > value:
            return i - 1
        else:
            value = abs(item-timestamp)
    raise ValueError('Timestamp provided is not within the ET samples')