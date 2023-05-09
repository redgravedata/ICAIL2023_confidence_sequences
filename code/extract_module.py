#import required libraries

import pandas as pd
import numpy as np
import hashlib

#***************************************************************************************************************
#function name: unzip_pickle_file
#precondition: None
#postcondition: gzip compression is removed from pickle file and the pickle file is read into a panda dataframe
#***************************************************************************************************************

def unzip_pickle_file(file):
    data = pd.read_pickle(file, 'gzip')
    return data


#***************************************************************************************************************
#function name: add_PRN
#precondition: None
#postcondition: gzip compression is removed from pickle file and the pickle file is read into a panda dataframe
#***************************************************************************************************************

def add_PRN(data, CONST_PRN_prefix):
    indexes = np.asarray(data.iloc[:,0])
    print(len(indexes))
    PRNs = []
    for x in range(len(indexes)):
        y = (str(CONST_PRN_prefix) + "_" + str(indexes[x]))
        #PRN = (str(CONST_PRN_prefix) + "_" + str(labels[0:1]['Index'].values[0]))
        y = hashlib.md5(y.encode())
        hashed_y = y.hexdigest()
        
        PRNs.append(hashed_y)
    return(PRNs)

#***************************************************************************************************************
#function name: aggregate_indexes
#precondition: 
#postcondition: 
#***************************************************************************************************************

def aggregate_indexes(data, total_rounds, sample_labels):
    #make the seed document the first document in the total order
    all_indexes = []
    col = ['Index']
    
    for x in range(0, total_rounds):
        
        #make 200-doc round a dataframe
        df = pd.DataFrame(data['infos'][x]['asked_idx'], columns = col)
        
        #left-join 200-doc dataframe with scores from sample labels)
        df = df.join(sample_labels, on = 'Index', how = 'left')
        #print(df)
        #sort the 200-doc ordering by the score
        df = df.sort_values(by = ['Scores','PRNs'], ascending = False)
        #print(df)
        all_indexes.append(df)
        
    total_order = pd.concat(all_indexes)
    return total_order

#***************************************************************************************************************
#function name: recall_80p_round
#precondition: None
#postcondition: The review round on which recall of 80% is achieved is returned by the function
#***************************************************************************************************************

def recall_80p_round(data):
    last_round = []
    for x in range(1,len(data['mets'])):
        pos_in_training = data['mets'][x][(-1, 'training', 'pos')]
        total_pos = data['mets'][x][(-1, 'training', 'pos')] + data['mets'][x][(-1, 'post-training-above', 'pos')] + data['mets'][x][(-1, 'post-training-below', 'pos')]
        if (pos_in_training / total_pos) > .80:
            last_round = np.append(last_round, x).astype(int)
    return last_round[0]

#***************************************************************************************************************
#function name: remaining_docs
#precondition: 
#postcondition: 
#***************************************************************************************************************

def remaining_docs(sorted_260_array, remaining_array):
    return list(set(sorted_260_array) ^ set(remaining_array)) 

#***************************************************************************************************************
#function name: 
#precondition: 
#postcondition: 
#***************************************************************************************************************

def copy_index_to_column_0(array):
    return np.c_[np.arange(len(array)),array]
