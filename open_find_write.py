def open_csv(path, delimiter = '\t', skip = 1, columns = []): 
    import csv
    '''
        * Requires module numpy as np to work
        Open only float data
        the column variable is list containing the number of columns that want to be imported
        for importing all the columns, no argument required
    '''
    output = np.array([],dt)
    with open(path, 'rb') as csvfile:
        file = csv.reader(csvfile, delimiter = delimiter)
        for i in range(skip):
            next(file, None) #Skip headers
        for row in file:
            import pdb ; pdb.set_trace()
            try: 
                if columns:
                    output.append([row[i] for i,el in enumerate(row) if i in columns])
                else:
                    output.append(map(float,row[columns]))
            except:
                print 'elements must be integers or float numbers, no strings allowed'
    return output

def find_files(path, name):
    from os import listdir
    """ 
        Looks in the directory "path".
        Returns a list with the files starting with 'name'.
    """
    n.file = []
    for item in listdir(path):
        if item.startswith(name):
            nfile.apend(item)
    return nfile

    
def write_line(file, line, delimiter = '\t'):
    '''
        Writes a line to a text file already open. 
        The line must be saved in a list format
    '''
    for item in line:
        file.write(str(item) + delimiter)
        file.write('\n')
    return

def as_string(list):
    '''
        Converts all the elements in a list to string
    '''
    return [str(i) for i in list]