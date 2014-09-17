

def open_csv(path, delimiter = '\t', skip = 1, columns = []): 
    import csv
    output = []
    with open(path, 'rb') as csvfile:
        file = csv.reader(csvfile, delimiter = delimiter)
        for i in range(skip):
            next(file, None) #Skip headers
        for row in file:
            import pdb ; pdb.set_trace()
            try: 
                if not columns:
                    output = [row[i] for i in row if i in [columns]]
                else:
                    output.append(map(float,row[columns]))
            except:
                pass
    return output
    
def write_line(file,line):
    for item in line:
        file.write(str(item) + "\t")
        file.write('\n')
    return

def as_string(list):
    return [str(i) for i in list]