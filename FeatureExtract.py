from datetime import datetime
import numpy as np 
import os
# ------------------------------------------ STEP TWO 

# ---- 目前仅考虑单台机器登陆情况，多台机器登陆的情况需要单独考虑！！！

class IndexError(Exception):
    pass

user_sets=['ASD0577', 'AAL0706', 'ASM0575', 'GCG0951', 'AAV0450', 'TDG0962', 'CCM0136', 'FRR0832', 'KPP0452', 'ABM0845', 'MJB0588', 'WJD0576', 'ILH0958', 'FEB0306', 'JJB0700', 'AHD0848', 'LDM0587', 'MLG0475', 'NCK0295', 'YJV0699']

USERNAME='YJV0699'
MACHINE='xxxxxxx'
# username='AAM0658-1'
data_set={0:'logon.csv',1:'device.csv',2:'email.csv',3:'http.csv',4:'file.csv',5:'psychometric.csv'}


# TODO 
def feature_extract():
    '''
    '''
    pass
# TODO
# 角色分析



# DONE 
def path_check(path):
    folders=os.path.exists(path)
    if not folders:
        print("Create new folders: ' %s ' successfully!"%(path))
        os.makedirs(path)
    else:
        print("The folder  ' %s ' exits, Please check!"%(path))
        os._exit(0)

def new_log(file_in,file_out):
    '''
    delete the id in the first column
    '''
    file_in=open(file_in,'r')
    file_out=open(file_out,'wt')
    for line in file_in:
        line=line.split(',')
        if MACHINE in line:
            newline=','.join(line[1:])
            file_out.writelines(newline)
    file_in.close()

def combine_time_log(file_in,file_out):
    '''
    combine data in the same day
    file_in: the new logdata in new folder 
    '''
    files_in=open(file_in,'r')
    date_set=['null']
    for line in files_in:
        line=line.split(' ')
        if line[0] not in date_set:
            date_set.append(line[0])
    # print (date_set)
    files_in.close()

    i=0
    files_in=open(file_in,'r')
    files_out=open(file_out,'wt')
    newline=''
    for line in files_in:
        line=line.strip()
        line=line.replace(' ',',')
        if date_set[i] in line:
            newline=newline+' ; '+line
            # print(1)
        else:
            files_out.writelines(newline+'\n')
            newline=line
            i=i+1

def find_weekday(time):
    '''
    find weekdays for time_two from time_one in weekday: day_one
    Arg:
     time: for example, 01/04/2010
    Return:
     weekday: 1:Monday 2:Tuesday ...
    '''
    week=datetime.strptime(time,'%m/%d/%Y').weekday()+1
    return (week)
    
def count_time(time_logon,time_logoff):
    '''
    count the logoning time 
    Arg:
     time_longon: for example, 07:20:00
     time_logoff: for example, 15:20:00
    return:
     last_time: float, the number of hours of online.
    '''
    time_logon=datetime.strptime(time_logon,'%H:%M:%S')
    time_logoff=datetime.strptime(time_logoff,'%H:%M:%S')
    last_time=(time_logoff-time_logon).total_seconds()/3600
    last_time=round(last_time,2)
    return last_time
    # print(last_time)
    # print(type(last_time))


# 数据合并的时候应当从相应的时间位进行判定
# ----------------- 单个用户不同日志特征分析：
def log_feature(file_input):
    '''

    file_input: logon2.csv 
    '''
    # file_output=open(file_out,'wt')

    files_in=open(file_input,'r')
    data_dicts={}
    m=1
    for line in files_in:
        # print (m)
        m=m+1
        if line !='\n':
            # data_list=[]
            line=line.strip()
            time_line=line.split(',')
            week_time=time_line[0] # format: 01/04/2010
            # ----- 星期几
            weekday=find_weekday(week_time)
            # ----- 登陆机器的总数
            computer_number=1
            # ----------------------- 第一台机器 在一天之内---------------------------
            # ----- 登陆的机器编号
            computer_id=1
            # ----- 该机器一天内登陆的总次数
            numebr_logon=line.count('Logon')
            # 
            line=line.split(' ; ')
            # ----- 第一次登陆具体时间
            first_logon=line[0].split(',')[1] # format: 07:20:00
            first_logoff=line[1].split(',')[1]
            first_logon_time=datetime.strptime(first_logon,'%H:%M:%S') 
            first_logoff_time=datetime.strptime(first_logoff,'%H:%M:%S')
            first_logon_hour=first_logon_time.hour
            first_logon_minutes=first_logon_time.minute
            first_logoff_hour=first_logoff_time.hour
            first_logoff_minutes=first_logoff_time.minute
            # print(first_logoff_hour)

            # ----- 最后一次登陆具体时间
            last_logon=line[-2].split(',')[1]
            last_logoff=line[-1].split(',')[1]
            last_logon_time=datetime.strptime(last_logon,'%H:%M:%S') 
            last_logoff_time=datetime.strptime(last_logoff,'%H:%M:%S')
            last_logon_hour=last_logon_time.hour
            last_logon_minutes=last_logon_time.minute
            last_logoff_hour=last_logoff_time.hour
            last_logoff_minutes=last_logoff_time.minute
            # print(last_logoff_hour)
            
            # ----- 登陆的总时长 (最后一次退出时间减去第一次登陆时间)
            online_time=count_time(first_logon,last_logoff)
           
            data_list=[[weekday,numebr_logon,first_logon_hour,first_logon_minutes,first_logoff_hour,first_logoff_minutes,last_logon_hour,last_logon_minutes,last_logoff_hour,last_logoff_minutes,online_time],[]]
            data_dicts[week_time]=data_list

            
    files_in.close()
    # file_output.close()
    return data_dicts

def device_feature(file_input,log_dicts):
    '''

    file_input: device2.csv 
    '''
    files_in=open(file_input,'r')
    m=0
    for line in files_in:
        if line !='\n':
            line=line.strip()
            time_line=line.split(',')
            week_time=time_line[0] # format: 01/04/2010
            # ----- 星期几
            weekday=find_weekday(week_time)
            # ----- 使用U盘的机器的总数
            computer_number=1
            # ----------------------- 第一台机器 在一天之内---------------------------
            # ----- 使用U盘的机器编号
            computer_id=1
            # ----- 该机器一天内使用U盘的总次数
            numebr_use_device=line.count('Connect')
         
            # 数据拼接
            data_device=[weekday,numebr_use_device]
            log_dicts[week_time][0]=log_dicts[week_time][0]+data_device
            # print (log_dicts[week_time])
            # exit(0)
    files_in.close()
    return log_dicts

def email_feature(file_input,http_dicts):
    '''
    file_inout: email2.csv

    features are marked with : '-----' in the comments 
    '''
    files_in=open(file_input,'r')
    for line in files_in:
        if line !='\n':
            line=line.strip()
            time_line=line.split(',')
            week_time=time_line[0] # format: 01/04/2010
            # ----- 星期几
            weekday=find_weekday(week_time)
            #
            line=line.split(' ; ')
            # ----- 发送邮件总次数：
            Number_email=len(line)
            #
            data_email=[]
            for i in range(len(line)):
                eamil_set=[]
                new_line=line[i].replace(';',',')
                new_line=new_line.split(',')
                for string in new_line:
                    # print(string)
                    if '@' in string and (string not in eamil_set):
                        eamil_set.append(string)
                # ----- 每次接收邮件的人数：
                Number_receiver=len(eamil_set)-1
                # 发件人邮箱：
                source_email=eamil_set[-1]
                # ----- 每次发件人邮箱是私人还是公司邮箱
                if '@dtaa.com' in source_email:
                    source_email_type=0
                else:
                    source_email_type=1
                receiver_email=eamil_set[:-1]
                Number_company_email=0
                for address in receiver_email:
                    if '@dtaa.com' in address:
                        Number_company_email+=1
                # ----- 每次收件人邮箱为公司邮箱的个数
                # ----- 每次收件人邮箱为私人邮箱的个数
                Number_private_email=Number_receiver-Number_company_email
                # 发件人邮箱所在的索引值（第一次出现）
                source_email_index=new_line.index(source_email)
                # 邮件大小的索引值
                size_index=source_email_index
                while not new_line[size_index].isdigit():
                    size_index=size_index+1
                # ----- 每次邮件大小: （KB）
                size_email=round(float(new_line[size_index])/1024,2)
                # 附件值的索引值
                attachment_index=size_index+1
                # ----- 每次附件的个数:
                attachment_count=int(new_line[attachment_index])

                # 数据拼接
                data_email=data_email+[Number_receiver,source_email_type,Number_company_email,Number_private_email,size_email,attachment_count]
            # print(len(data_email[:24])) 
            http_dicts[week_time][0]=http_dicts[week_time][0]+[weekday,Number_email]
            http_dicts[week_time][1]=http_dicts[week_time][1]+data_email[:24]

               
            # exit(0)
    files_in.close()
    # print(log_dicts)
    return http_dicts

def file_feature(file_input):
    '''
    暂且不考虑，因为个人电脑上存放的不应该是私密数据;另外，数据中也几乎没有体现出与恶意用户相关的部分。
    file_input: file2.csv
    '''
    files_in=open(file_input,'r')
    for line in files_in:
        if line !='\n':
            line=line.strip()
            time_line=line.split(',')
            week_time=time_line[0] # format: 01/04/2010
            # ----- 星期几
            weekday=find_weekday(week_time)
            # 访问文件的次数
    files_in.close()

def http_feature(file_input,device_dicts):
    '''

    file_input: http2.csv 
    '''
    files_in=open(file_input,'r')
    for line in files_in:
        if line !='\n':
            line=line.strip()
            time_line=line.split(',')
            week_time=time_line[0] # format: 01/04/2010
            # ----- 星期几
            weekday=find_weekday(week_time)
            # 
            line=line.split(' ; ')
            # ----- 访问网页的总次数
            Numeber_webs=len(line)
            
            # 数据拼接
            data_http=[weekday,Numeber_webs]
            device_dicts[week_time][0]=device_dicts[week_time][0]+data_http

    files_in.close()
    return device_dicts
            # exit(0)

def list_complemetion(lists,set_length):
    while len(lists)<set_length:
        lists.append(0)
    return lists

def mix_complemention(dicts,columns,set_length):
    '''
    对输入的dicts 数据维度进行统一，dicts 的value中有两个list,columns=0时 操作第一个lists；colums=1时操作第二个lists
    '''
    for (key,value) in dicts.items():
        while len(value[columns])<set_length:
            value[columns].append(0)
    return dicts


# ----------------- 单个用户行为序列分析    

def file_sequence(file_in,file_type):
    '''
    generate the sequence according to date
     Arg:
      file_in:
      file_type: int (0-4, 0:logon, 1:device, 2:email, 3:file, 4:http)
     Return:
      a dict of sequences, key: date; value: actions and time.
    '''

    type_set={0:'logon', 1:'device', 2:'email', 3:'file', 4:'http'}
    type_words=type_set[file_type]
    files_in=open(file_in,'r')
    sequences_set={}
    for line in files_in:
        if line !='\n':
            line=line.split(' ; ')
            # print (len(line))
            for records in line:
                if file_type==0 and 'Logon'in records:
                    type_words= 'logon'
                elif file_type==0 and 'Logoff'in records:
                    type_words= 'logoff'
                if file_type==1 and 'Connect' in records:
                    type_words= 'Connect'
                elif file_type==1 and 'Disconnect' in records:
                    type_words='Disconnect'
                records=records.split(',')
                if records[0] in sequences_set:
                    # 同一天的不同时刻记录拼接
                    values=records[1]+'#'+type_words
                    sequences_set[records[0]]=sequences_set[records[0]]+' & '+values
                else:
                    values=records[1]+'#'+type_words
                    sequences_set[records[0]]=values
    files_in.close()
    return(sequences_set)

def sequence_combine(sequence_one,sequence_two):
    '''
    combine two sequence dicts according to key (date).
     Arg:
      sequence_one: dicts
      sequence_two: dicts 
     Return: a combined dict.
    '''

    for (date,record) in sequence_two.items():
        if date in sequence_one:
            new_record=sequence_one[date]+' & '+record
            sequence_one[date]=new_record
        else:
            print ('some date missed! Please change the combination order')
            exit(0)
        # print(sequence_one)
        # exit(0)
    return(sequence_one)
    # return(sequence_one)
     
def sort_actions_One_Day(Day_records):
    '''
    sort actions in One day through time.
        Arg：
         Day_records: a string composed of time and actions (08:56:00#logon & 17:05:00#logoff...)
        Return: a string of sorted sequence of actions. 
    '''
    line=Day_records.split(' & ')
    length=len(line)
    actions_dict={}
    time_dict=[]
    actions_sorted=[]
    for temp_data in line:
        # temp_data[0:8] 为时间数据， temp_data[9:]为行为数据，其中中间丢弃了‘#’符号
        actions_dict[temp_data[0:8]]=temp_data[9:]
        time_dict.append(temp_data[0:8])
    time_sorted=quick_sort_datetime(time_dict)
    for time_string in time_sorted:
        actions_sorted.append(actions_dict[time_string])
    action_sequence=','.join(actions_sorted)
    return action_sequence,length

def sort_actions_InSequence(sequence_in,save_file):
    '''
    sort actions day by day in the dict through time.
     Arg:
      sequence_in: a dict (the disordered sequence)
     Return: a dict (the ordered sequence)
    ''' 
    files=open(save_file,'wt')
    max_length=0
    for (date,records) in sequence_in.items():
        actions_sequence,day_actions_length=sort_actions_One_Day(records)
        files.writelines(date+' : '+actions_sequence+'\n')
        if day_actions_length>max_length:
            max_length=day_actions_length
    print( USERNAME,'_maxlength: ',max_length)
    return max_length

def quick_sort(array):
    '''
    quick sort algorithm
        Arg:
         array: a list 
        Return: a list
               
    '''
    smaller_list=[]
    bigger_list=[]
    equal_list=[]
    if len(array)<=1:
        return array
    else:    
        middle_key=array[0]
        for records in array:
            if records < middle_key:
                smaller_list.append(records)
            elif records > middle_key:
                bigger_list.append(records)
            else:
                equal_list.append(records)
        smaller_list=quick_sort(smaller_list)
        bigger_list=quick_sort(bigger_list)
        return smaller_list+equal_list+bigger_list

def quick_sort_datetime(array):
    '''
    quick sort algorithm for datetime class.
     Arg:
         array: a list (elements belong to datetime class)
     Return: a list (elements belong to string)
    '''
    smaller_list=[]
    bigger_list=[]
    equal_list=[]
    if len(array)<=1:
        return array
    else:    
        middle_key=datetime.strptime(array[0],'%H:%M:%S')
        for records in array:
            datetime_records=datetime.strptime(records,'%H:%M:%S')
            if datetime_records < middle_key:
                smaller_list.append(records)
            elif datetime_records > middle_key:
                bigger_list.append(records)
            else:
                equal_list.append(records)
        smaller_list=quick_sort(smaller_list)
        bigger_list=quick_sort(bigger_list)
        return smaller_list+equal_list+bigger_list

def sequence_code(sequence_files_in,sequence_code_save,sequence_len):

    code_dict={'logon':1,'Connect':2,'Disconnect':3,'http':4,'email':5,'logoff':6}
    file_in=open(sequence_files_in,'r')
    file_out=open(sequence_code_save,'wt')
    file_out.close()
    file_out=open(sequence_code_save,'a+')
    for line in file_in:
        line=line.strip()
        line=line.split(' : ')
        week_day=find_weekday(line[0])
        sequences=line[1].split(',')
        sequence_codes=[]
        for actions in sequences:
            sequence_codes.append(code_dict[actions])
        sequence_codes=list_complemetion(sequence_codes,sequence_len)
        sequence_codes=np.reshape(sequence_codes,(1,sequence_len))
        np.savetxt(file_out,sequence_codes,fmt='%f',delimiter=',')
    file_out.close()
 

# step 3 ---------------------------------------特征图部分
# 需要新建 feature 文件夹
def Feature_generate(file_in,file2_in,file3_in,file4_in):
    '''
    Generate features for every user
    '''
    path=USERNAME+'/feature'
    path_check(path)
    file_out=USERNAME+'/feature/data_out.csv'
    log_dicts=log_feature(file_in)
    device_dicts=device_feature(file2_in,log_dicts)
    new_device_dicts=mix_complemention(device_dicts,0,13)
    http_dicts=http_feature(file4_in,new_device_dicts)
    new_http_dicts=mix_complemention(http_dicts,0,15)
    email_dicts=email_feature(file3_in,new_http_dicts)
    # 第一部分数据补全到24位
    new_email_dicts=mix_complemention(email_dicts,0,24)
    # 第二部分数据补全到24位
    new_email_dicts2=mix_complemention(new_email_dicts,1,24)
    # # print (new_email_dicts)
    # print(new_device_dicts)
    # 数据保存
    data_save=open(file_out,'a+')
    for (key,value) in new_email_dicts2.items():
        values=np.array(value[0]+value[1])
        values=np.reshape(values,(-1,48))
        np.savetxt(data_save,values,fmt='%f',delimiter=',')
    data_save.close()

# step 4 ---------------------------------------- 行为序列部分
# 新建 sequence 文件夹
def Sequence_generate(file_in,file2_in,file3_in,file4_in):
    path=USERNAME+'/sequence'
    path_check(path)
    ActionSeq_save_path=USERNAME+'/sequence/actions_sequence.csv'
    sequence_temp=USERNAME+'/sequence/sequence_temp.csv'
    sequence_code_save=USERNAME+'/sequence/sequence_code.csv'

    logon_time_sequence=file_sequence(file_in,0)
    device_time_sequence=file_sequence(file2_in,1)
    email_time_sequence=file_sequence(file3_in,2)
    http_time_sequence=file_sequence(file4_in,4)

    Final_Sequence=sequence_combine(logon_time_sequence,device_time_sequence)
    Final_Sequence=sequence_combine(Final_Sequence,email_time_sequence)
    Final_Sequence=sequence_combine(Final_Sequence,http_time_sequence)
    max_length=sort_actions_InSequence(Final_Sequence,ActionSeq_save_path)

    file_temp=open(sequence_temp,'wt')
    file_temp.writelines(str(Final_Sequence))
    file_temp.close()
    # -------------- sequence code
    sequence_code(ActionSeq_save_path,sequence_code_save,max_length)

    # --------------------------


