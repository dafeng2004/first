import numpy as np

#读取数据
p = r'D:\software\tmp\Sheet1.csv'
#D:\software\tmp\SS300_200606_201907.csv--D:\software\tmp\sz461_200906_201907.csv
with open(p,encoding = 'ANSI') as f:
    data = np.loadtxt(f,str,delimiter = ',', skiprows = 1,usecols = (1,2,3))
    #取唯一的代码值
    sk_name_list=np.unique(data[1:,[0]]).tolist()[1:]

sk_peak_date=[]
sk_peak_date2=np.array([],dtype=str)
sk_pairs=np.empty(shape=[0,2],dtype=str)
sk_pair=[]
#循环计算各个代码
for sk_name in sk_name_list:
    #print(sk_name+'\n')
    #取有收盘价的数据－子数组,跳过空值
    idx_array=data[np.where((data[:,0]==sk_name)&(data[:,2]!=''))]
    #取日期
    sk_date_array=idx_array[:,1]
    #取价格
    print(sk_name)
    sk_close_str_array=idx_array[:,2]
    sk_close_array=sk_close_str_array.astype(np.float16)
    #转价格为列表
    sk_close_list=sk_close_array.tolist()
    #求列表差，正负号
    doublediff = np.diff(np.sign(np.diff(sk_close_list)))
    #求最大值(顶点)索引
    peak_locations1 = np.where(doublediff == -2)[0] + 1
    low_locations1 = np.where(doublediff == 2)[0] + 1
    #取顶极值点对应数据
    sk_high_date_array2=sk_date_array[peak_locations1]
    sk_high_close_array2=sk_close_array[peak_locations1]
    sk_high_close_list2=sk_close_array[peak_locations1].astype(np.float16).tolist()
    #求列表差，正负号
    doublediff = np.diff(np.sign(np.diff(sk_high_close_list2)))
    peak_locations2=np.where(doublediff == -2)[0] + 1
    #取低极值点对应数据
    sk_low_date_array2=sk_date_array[low_locations1]
    sk_low_close_array2=sk_close_array[low_locations1]
    sk_low_close_list2=sk_close_array[low_locations1].astype(np.float16).tolist()
    #求列表差，正负号
    doublediff = np.diff(np.sign(np.diff(sk_low_close_list2)))
    low_locations2=np.where(doublediff == 2)[0] + 1
        
    if len(peak_locations2)>2 :
        peak_date_str=sk_name+',H'+',H'.join(sk_high_date_array2[peak_locations2].tolist())
        peak_date_str=peak_date_str+',L'+',L'.join(sk_low_date_array2[low_locations2].tolist())
        sk_peak_date.append(peak_date_str)

#循环比较，是否存在顶点时间相同占比0.7的两组数，列出
for i in range(0,len(sk_peak_date)-1):
      for j in range(i+1,len(sk_peak_date)-1):#print(prev_one[1])
          list1=sk_peak_date[i].split(',')
          list2=sk_peak_date[j].split(',')
          list1_name=list1[0]
          list2_name=list2[0]
          min_len=min(len(list1),len(list2))-1
          inter_sect1=np.intersect1d(list1,list2)
          if len(inter_sect1)>min_len*0.90 and min_len>6:
              result1=[]
              result1.append(list1_name)
              result1.append(list2_name)
              result1.append(inter_sect1)
              sk_pair=np.array([list1_name,list2_name])
              sk_pairs=np.append(sk_pairs,sk_pair)
              sk_peak_date2=np.append(sk_peak_date2,np.array(result1),axis=0)
print(sk_peak_date2)

file=open('d:/software/tmp/record1.csv','a')
for one in range(0,int(sk_peak_date2.size/3)):
    tmp=sk_peak_date2[one*3+2].tolist()
    tmp=','.join(tmp)
    tmp='H,'+sk_peak_date2[one*3]+','+sk_peak_date2[one*3+1]+','+tmp+'\n'
    file.writelines(tmp)
file.close()
