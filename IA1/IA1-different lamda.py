import numpy as np
import pandas as pd
import csv
import os
import copy
import matplotlib.pyplot as plt


train = pd.read_csv('PA1_train.csv', sep=',',header=None)
train = train.values
test = pd.read_csv('PA1_test.csv', sep=',',header=None)
test = test.values
dev = pd.read_csv('PA1_dev.csv', sep=',',header=None)
dev = dev.values
normalized_train_data = np.zeros((10000, 22))  ## take out id and price 
normalized_test_data = np.zeros((6000, 22))  ## take out id 
normalized_dev_data = np.zeros((5597, 22))  ## take out id and price 
y_train_data = np.zeros((10000, ))
y_dev_data = np.zeros((5597, ))
# learning_list = [pow(10, 0),pow(10, -1),pow(10, -2),pow(10, -3),pow(10, -4),pow(10, -5),pow(10, -6),pow(10, -7)]
normalg_list = list()
          

def run_init_diff_learningrate():
    #for ea_l in learning_list:
    # learning = ea_l
    diff_lamda(normalized_train_data, y_train_data, 1)
    plt.plot(normalg_list)


def split_date(cut_head_data, whichForm):
    split_date_data = copy.deepcopy(cut_head_data)
    if whichForm == 'train':
        sd_data = np.zeros((10000,3))
    if whichForm == 'test':
        sd_data = np.zeros((6000,3))
    if whichForm == 'dev':
        sd_data = np.zeros((5597,3))
        
    for idx_r, ea_date_str in enumerate(split_date_data):
        data_features = ea_date_str.split("/")
        for idx in range(0,3):
            sd_data[idx_r,idx] = data_features[idx-1]
        idx_r += 1
    h_data_set = np.hsplit(sd_data,3)
    return h_data_set

def add_in_arrays(count_col, data, min_array, max_array):
    """
    Add the max and the min in an array.
    """
    max_array[count_col] = np.max(data)
    min_array[count_col] = np.min(data)

def norm_data(ea_col, count_col, cut_head_data, min_array, max_array, whichForm):
    """
    Normalize data.
    """
    new_data = (cut_head_data - min_array[count_col]) / (max_array[count_col] - min_array[count_col])
    
    if whichForm == 'train':
        if ea_col == 2:
            new_data =  new_data.reshape((10000,))
        normalized_train_data[:,count_col] = new_data

    if whichForm == 'test':
        if ea_col == 2:
            new_data =  new_data.reshape((6000,))
        normalized_test_data[:,count_col] = new_data
        
    if whichForm == 'dev':
        if ea_col == 2:
            new_data =  new_data.reshape((5597,))
        normalized_dev_data[:,count_col] = new_data


def process_columns():
    """
    Process both test.csv and train.csv 's columns and normalize them
    The final normalized data will store in normalized_train_data and normalized_test_data (without 'id' and 'price' columns )
    """
    
    count_col = 0
    
    # Run through every col in train.csv
    whichForm = 'train'
    min_array = np.zeros((train.shape[1],))
    max_array = np.zeros((train.shape[1],))

    for ea_col in range(train.shape[1]):
        
        orig_data = train[:,ea_col]
        
        cut_head_data = copy.deepcopy(orig_data)
        cut_head_data = cut_head_data[1:]
        
        if ea_col == 2:
            date_data = split_date(cut_head_data, whichForm)
            for ea_date_data in date_data:
                add_in_arrays(count_col, ea_date_data, min_array, max_array)
                norm_data(ea_col, count_col, ea_date_data, min_array, max_array, whichForm)
                count_col += 1
        elif ea_col == 0:
            add_in_arrays(count_col, cut_head_data, min_array, max_array)
            normalized_train_data[:, 0] = cut_head_data
            count_col += 1
        elif ea_col == 1:
            pass
        elif ea_col == 21:
            cut_head_data = cut_head_data.astype(float)
            y_train_data = cut_head_data
        else:
            cut_head_data = cut_head_data.astype(float)
            add_in_arrays(count_col, cut_head_data, min_array, max_array)
            norm_data(ea_col, count_col, cut_head_data, min_array, max_array, whichForm)
            count_col += 1

    ##########################################################################
    
    count_col = 0
    
    # Run through every col in test.csv
    whichForm = 'test'
    min_array = np.zeros((test.shape[1]+1,))
    max_array = np.zeros((test.shape[1]+1,))

    for ea_col in range(test.shape[1]):
        orig_data = test[:,ea_col]
        
        cut_head_data = copy.deepcopy(orig_data)
        cut_head_data = cut_head_data[1:]
        
        if ea_col == 2:
            date_data = split_date(cut_head_data, whichForm)
            for ea_date_data in date_data:
                add_in_arrays(count_col, ea_date_data, min_array, max_array)
                norm_data(ea_col, count_col, ea_date_data, min_array, max_array, whichForm)
                count_col += 1
        elif ea_col == 0:
            add_in_arrays(count_col, cut_head_data, min_array, max_array)
            normalized_test_data[:, 0] = cut_head_data
            count_col += 1
        elif ea_col == 1:
            pass
        else:
            cut_head_data = cut_head_data.astype(float)
            add_in_arrays(count_col, cut_head_data, min_array, max_array)
            norm_data(ea_col, count_col, cut_head_data, min_array, max_array, whichForm)
            count_col += 1


    ##########################################################################
    
    count_col = 0
    
    # Run through every col in dev.csv
    whichForm = 'dev'
    min_array = np.zeros((dev.shape[1],))
    max_array = np.zeros((dev.shape[1],))

    for ea_col in range(dev.shape[1]):
        
        orig_data = dev[:,ea_col]
        
        cut_head_data = copy.deepcopy(orig_data)
        cut_head_data = cut_head_data[1:]
        
        if ea_col == 2:
            date_data = split_date(cut_head_data, whichForm)
            for ea_date_data in date_data:
                add_in_arrays(count_col, ea_date_data, min_array, max_array)
                norm_data(ea_col, count_col, ea_date_data, min_array, max_array, whichForm)
                count_col += 1
        elif ea_col == 0:
            add_in_arrays(count_col, cut_head_data, min_array, max_array)
            normalized_dev_data[:, 0] = cut_head_data
            count_col += 1
        elif ea_col == 1:
            pass
        elif ea_col == 21:
            cut_head_data = cut_head_data.astype(float)
            y_dev_data = cut_head_data
        else:
            cut_head_data = cut_head_data.astype(float)
            add_in_arrays(count_col, cut_head_data, min_array, max_array)
            norm_data(ea_col, count_col, cut_head_data, min_array, max_array, whichForm)
            count_col += 1
            
    return y_train_data, y_dev_data



"""
    The gradient of the linear regression with l2 regularization cost function
    x:input dataset
    y:output dataset
    lamda:regularization factor
    
"""
def grad(w, x, y, lamda):   
    
    sum_up = 0
    N = x.shape[0]      #we need to know how many data in each column(How many rows)

    for i in range(0, N):
        
        sum_up += 2 * (np.dot(w, x[i]) - y[i]) * x[i] + 2 * lamda * w
    return sum_up



"""
The grad_descent function of different learning rate and fixed lamda
w: weight
learning: learning rate
converage: converage limit value
""" 
# def grad_descent (x, y, learning):

#     w = np.zeros(22)
#     converage=0.5

#     for runs in range(1000000):
#         gradient = grad(w, x, y, 0)
#         w = w - (learning * gradient)
#         normalg= np.linalg.norm(gradient)
#         print("normalg: ", normalg)
#         normalg_list.append(normalg)
#         # if runs % 100 == 0:
#         #     print ("w: ", w)
#         if normalg <= converage:
#             print("normalg <= converage!!!")
#             del normalg_list[:]
#             break

#     return normalg, w


'''
    The regularization of different lamda values and fixed learning rate
    x:input dataset
    y:output dataset
    lamda:regularization factor
    rate:learning rat
'''
def diff_lamda(x, y, lamda):
    
    w = np.zeros(22)   #initial w
    rate = 10**(-6) #fixed rate
    converage=0.5

    for runs in range(1000000):
        E = grad(w, x, y, lamda)
        w = w - ( rate * E)
        normalg= np.linalg.norm(E)
        print("normalg: ", normalg)
        normalg_list.append(normalg)
        if normalg <= converage:
            print("normalg <= converage!!!")
            del normalg_list[:]
            break
            
    return normalg, w


'''
    This function is for finding y value for test. file
    w: Best w value
    x: test. file without price column
    y: use y value from train data or validation data
'''
def test_y_value(w, x, y):

    pred_y = np.array([])           #store pred_value

    for i in x:
        value = np.dot(w, i)    
        pred_y = np.append(pred_y, pred_value)

    return pred_y




    
if __name__ == "__main__":
    y_train_data, y_dev_data = process_columns()
    run_init_diff_learningrate()