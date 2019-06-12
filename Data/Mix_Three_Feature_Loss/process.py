import linecache,random



def Random_Num(index,number):
    '''
    Generate a list of index from index randomly
     index : the index of files
     number : the length of list generated
     return : a list of index  
    '''
    return random.sample(list(index),number)

file_open='Mix_all_loss.csv'
label_open='Mix_all_label.csv'
file_save=open('Disorder_loss.csv','wt')
label_save=open('Disorder_label.csv','wt')
index=[n for n in range(0,600)] # 手动删除了每个文件的前20行数据
Random_index=Random_Num(index,600)
# print(Random_index)
for num in Random_index:
    line=linecache.getline(file_open,num+1)
    label=linecache.getline(label_open,num+1)
    file_save.writelines(line)
    label_save.writelines(label)
file_save.close()
label_save.close()









