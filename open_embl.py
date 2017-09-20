import os

def read_file(path_file):
    if os.path.exists(path_file):
        #print 'found'
        q_int = open(path_file).readlines()
        #print q_int
        return q_int

    else:
        print 'file not found: %s'%path_file
        return []


def filter_list(data):

    
    for i,element in enumerate(data):
        #print element
        
        if 'Sample:   c' in element:

            #print element
            start = i+1
            #print start

        if 'creator:' in element:
            end = i-1

    data_1=data[start:end]
    #print data_1
    return data_1
    

def final_columns(data_1):
    q=[]
    intensity=[]
    error=[]
    
    for element in data_1:
        pre_column = element.split(' ')
        q.append(pre_column[2])
        intensity.append(float(pre_column[5]))
        error.append(pre_column[8])

    for i,element in enumerate(error):
        final_error = element.split('\n')[0]
        error[i] = final_error
    
    return q,intensity,error
    #print intensity

def give_columns(name_file):

    dades_brutes=read_file(name_file)
    columnes_no_header=filter_list(dades_brutes)
    q,intensity,error=final_columns(columnes_no_header)
    #print intensity
    return q,intensity,error

#a,b,c = give_columns('/home/dani/Desktop/all_python/training_p_u/January_SAXS/img_0009_00100.dat')
#give_columns('/home/dani/Desktop/all_python/training_p_u/January_SAXS/img_0009_00192.dat')

#print b

#print '/home/dani/Desktop/all_python/training_p_u/January_SAXS/img_0009_00192.dat' == '/home/dani/Desktop/all_python/training_p_u/January_SAXS/img_0009_00192.dat'
#ddd
