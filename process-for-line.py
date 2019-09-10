import numpy as np 
import linecache
from FeatureExtract import path_check


# --------------------------------------- STEP THREE

def count_line(files_in):
    file_open=open(files_in,'r')
    count=0
    for line in file_open:
        count+=1
    return count   

def data_generator(files_name,num_days=5):
    # 删除最后一行数据，因为可能会有缺漏
    counts=count_line(files_name)-1
    real_counts=counts-num_days+1
    print (real_counts)   
    for i in range(real_counts):
        data_index=i+1
        label_index=data_index+4
        data_one=np.array(linecache.getline(files_name,data_index).strip().split(',')+linecache.getline(files_name,data_index+1).strip().split(',')+linecache.getline(files_name,data_index+2).strip().split(',')+linecache.getline(files_name,data_index+3).strip().split(','))
        labe_data=np.array(linecache.getline(files_name,label_index).strip().split(','))
        # print(np.shape(labe_data))
        # print (data_one)
        # exit (0)
        yield (data_one,labe_data)



# types='ActionSequence'
types='FeatureMap'
def type_check():
    if types=='FeatureMap':
    # -------- file_name for feture map
        files_name=USERNAME+'/feature/data_out.csv'
        data_all=USERNAME+'/feature/data_all.csv'
        label_all=USERNAME+'/feature/label_all.csv'
        data_train=USERNAME+'/feature/data_train.csv'
        data_test=USERNAME+'/feature/data_test.csv'
        label_train=USERNAME+'/feature/label_train.csv'
        label_test=USERNAME+'/feature/label_test.csv'
    # -------- file_name for action sequence 
    else:
        files_name=USERNAME+'/sequence/sequence_code.csv'
        data_all=USERNAME+'/sequence/data_all.csv'
        label_all=USERNAME+'/sequence/label_all.csv'
        data_train=USERNAME+'/sequence/data_train.csv'
        data_test=USERNAME+'/sequence/data_test.csv'
        label_train=USERNAME+'/sequence/label_train.csv'
        label_test=USERNAME+'/sequence/label_test.csv'


# # step one ------------------------------------- generate data with several days
# 数据先清空
def data_clean(data_all,label_all):
    data_save=open(data_all,'wt')
    label_save=open(label_all,'wt')
    data_save.close()
    label_save.close()
# 数据保存
def generate_data(data_all,label_all,files_name):
    '''
    we extract every five data for our datatset,
    the former four data are used for input data, the fivth data are used as label. 
    '''
    data_save=open(data_all,'a+')
    label_save=open(label_all,'a+')
    batch_size=10
    num_days_for_OneSequence=5
    # 删除最后一行数据，因为可能会有缺漏
    counts=count_line(files_name)-1  # the number of data
    real_counts=counts-num_days_for_OneSequence+1   
    rounds=int(real_counts/batch_size)
    print (rounds)
    for i in range(rounds):
        i=i*10
        data_batch=[]
        label_batch=[]
        for j in range (batch_size):
            data_index=i+j+1
            label_index=data_index+4
            data_one=linecache.getline(files_name,data_index).strip().split(',')+linecache.getline(files_name,data_index+1).strip().split(',')+linecache.getline(files_name,data_index+2).strip().split(',')+linecache.getline(files_name,data_index+3).strip().split(',')
            labe_data=linecache.getline(files_name,label_index).strip().split(',')
            data_batch.append(data_one)
            label_batch.append(labe_data)
           
        data_batch=np.array(data_batch)
        label_batch=np.array(label_batch)
        
        data_batch2=data_batch.astype('float32')
        label_batch2=label_batch.astype('float32')
        
        # print (data_batch[0])
        # exit(0)
        np.savetxt(data_save,data_batch2,fmt='%f',delimiter=',')
        np.savetxt(label_save,label_batch2,fmt='%f',delimiter=',')

    data_save.close()
    label_save.close()
    
# step two----------------------------------------------- 划分 train and test ---------------------------------------------
def train_test_generate(data_all,label_all,train_data_save,train_label_save,test_data_save,test_label_save,rate=0.8):
    '''
    we extract 'rate' (the defaults is 0.8) percent data for training, and the rest for testing. 
    
    '''
    
    data_in=open(data_all,'r')
    label_in=open(label_all,'r')
    data_train=open(train_data_save,'wt')
    data_test=open(test_data_save,'wt')
    label_train=open(train_label_save,'wt')
    label_test=open(test_label_save,'wt')
    data_num=count_line(data_all)
    train_num=data_num*rate
    # print(train_num)
    index=0
    for line in data_in:
        if index<train_num:
            data_train.writelines(line)
        else:
            data_test.writelines(line)
        index=index+1

    data_train.close()
    data_test.close()

    index=0
    for label in label_in:
        if index<train_num:
            label_train.writelines(label)
        else:
            label_test.writelines(label)
        index=index+1
    label_train.close()
    label_test.close()
    data_in.close()
    label_in.close()




if __name__ == "__main__":

    types='FeatureMap'
    USERNAME=''
   
    user_sets=['EDB0714','TNM0961','HXL0968'] # 29 32 33
    for username in user_sets:
        USERNAME=username
        if types=='FeatureMap':
            # -------- file_name for feture map
            files_name=USERNAME+'/feature/data_out.csv'
            data_all=USERNAME+'/feature/data_all.csv'
            label_all=USERNAME+'/feature/label_all.csv'
            data_train=USERNAME+'/feature/data_train.csv'
            data_test=USERNAME+'/feature/data_test.csv'
            label_train=USERNAME+'/feature/label_train.csv'
            label_test=USERNAME+'/feature/label_test.csv'
            # -------- file_name for action sequence 
        else:
            files_name=USERNAME+'/sequence/sequence_code.csv'
            data_all=USERNAME+'/sequence/data_all.csv'
            label_all=USERNAME+'/sequence/label_all.csv'
            data_train=USERNAME+'/sequence/data_train.csv'
            data_test=USERNAME+'/sequence/data_test.csv'
            label_train=USERNAME+'/sequence/label_train.csv'
            label_test=USERNAME+'/sequence/label_test.csv'    

        data_clean(data_all,label_all)
        # generate the data for deep learning model
        generate_data(data_all,label_all,files_name)
        # extract training data and test data
        train_test_generate(data_all,label_all,data_train,label_train,data_test,label_test,rate=0.7)


                