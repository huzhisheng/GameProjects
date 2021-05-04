import os
import time
import pyaudio
import wave
import scipy.io.wavfile as sciwav
from python_speech_features import *
import numpy as np
from tqdm import tqdm
import keyboard
from Test import Test
#最近更改时间2019年12月6日11点37分
#这版本的DTW返回开方的距离
#DTW约束区域为菱形

#2019年12月17日13点37分
#补上实时获取音量最大值
#第一次录音添加自动结束录音


CHUNK = 1024                                                 #底层的缓存的块的大小，底层的缓存由N个同样大小的块组成
FORMAT = pyaudio.paInt16                            #取样值的量化格式 (paFloat32, paInt32, paInt24, paInt16, paInt8 …)
CHANNELS = 2                                                #声道数 
RATE = 8000                                                  #取样频率 
RECORD_SECONDS = 1
FLAG =1
#DTW中计算两帧特征向量之间的距离
def CalculateDistance(i,j,tf,nf,feature_len=38):
    a = 0
    for k in range(0,feature_len):
        a = a+(tf[i][k]-nf[j][k])**2
    return a**0.5

#计算最短路径的
#tf: template_feature
#nf: now_feature
def DTW(tf,nf):                                             
    len_t = len(tf)                       #预存语音梅谱帧数
    len_n = len(nf)                     #实时语音梅谱帧数

    vector_len = len(tf[0])          #特征向量长度
    #print(len_t,'  ',vector_len)
    print("before:",len(tf),',',len(nf),',',vector_len)
    if len_t >len_n:
        for i in range( len_t-len_n):
            nf = np.append(nf,[nf[len_n-1]],axis=0)
        len_n=len_t        
    elif len_t <len_n:
        for i in range( len_n-len_t):
            tf = np.append(tf,[tf[len_t-1]],axis=0)
        len_t=len_n    
    D = CalculateDistance(0,0,tf,nf,vector_len)      #起点距离
    #d = []
    #d.append(D)

    i = 0
    j = 0
    #t =[1]
    #n = [1]
    #k = 0       #计数器，用来查看DTW的执行过程
    max_size = 65535
    min_size = 0
    
    #print(len_t,',',len_n)
    while (i<=len_n-1 and j<=len_t-1):
        #if (j*2>=i and (2*(i-len_n+2)<=j-len_t+1) and i+1<len_n-1) :
        if (j*2>=i and (2*(i-len_n+2)<=j-len_t+1) and i+1<len_n-1) :
            D1 = CalculateDistance(i+1,j,tf,nf,vector_len)
        else:
            D1 = max_size
        #if (j<=2*i and (0.5*(i-len_n+1)>=(j-len_t+2)) and j+1 <len_n-1) :
        if (j<=2*i and (i-len_n>=2*j-2*len_t+1) and j+1 <len_n-1) :
            D2 = CalculateDistance(i,j+1,tf,nf,vector_len)
        else:
            D2 = max_size
        if i+1<=len_n-1 and j+1<=len_t-1:
            #print(j+1)
            D3 = CalculateDistance(i+1,j+1,tf,nf,vector_len)
        min_size = min(D1,D2,D3)
        if min_size ==D1:
            i = i+1  
        elif min_size == D2:
            j = j+1        
        elif min_size == D3:
            i = i+1           
            j = j+1         
        D = D +min_size
    Test.getCpu()
        #d.append(min_size)
       # k = k+1
        #print(k,'   ','( ',i,' ',j,' )' )
    #x = [i for i in range(len(d))]
    #plt.plot(x,d,label="distance")
    #plt.legend()
    #plt.show()

    #print(D)
    return D

#代码来源 https://www.jianshu.com/p/e32d2d5ccb0d
#获取音频特征值MFCC
def get_mfcc(data, rate):
    wav_feature =  mfcc(data, rate,nfft = 1200)
    d_mfcc_feat = delta(wav_feature, 1)
    d_mfcc_feat2 = delta(wav_feature, 2)
    feature = np.hstack((wav_feature, d_mfcc_feat, d_mfcc_feat2))
    return feature

#实时监测麦克风
#volume为声音阈值
def MonitorMicrophone(volume=800):
    p = pyaudio.PyAudio()
    stream = p.open(
            format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            frames_per_buffer = CHUNK,
        )
    
    print ('录音开始 ')
    for i in range(0, 100):
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.short)
        temp = np.max(audio_data)
        
        if temp > volume :
            print ("检测到信号")
            print ('当前阈值：',temp ) 
            return temp          
    return False


#功能：实时获取某时间间隔内音量最大值
#volume为声音阈值
def GetHighestVolume(record_second=1):
    p = pyaudio.PyAudio()
    stream = p.open(
            format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            frames_per_buffer = CHUNK,
        )
    volume = 0
    for i in tqdm(range(0, int(RATE / CHUNK * record_second))):
        data = stream.read(CHUNK)                                                   #data类型为字符串
        audio_data = np.frombuffer(data, dtype=np.short)
        temp = np.max(audio_data)
        if temp >volume:
            volume =temp
    return volume


#代码来源 https://www.jb51.net/article/163992.htm
#data_save_path                                  玩家    “设置指令“    获取的    原始音频数据    保存文件路径，
#                                                                         文件内容为字符串，
#                                                                         文件格式为'.wav'
#data_feature_save_path                     玩家    “设置指令”    获取的音频数据加工后的    “特征值”    保存文件路径，
#                                                                         文件内容为np数组，
#                                                                         文件格式为'.npy'
#ingame_data_save_path                     玩家    ”确认指令“或“在游戏中发出指令”    的     原始音频数据   保存文件路径
#                                                                         文件内容为字符串，
#                                                                         文件格式为'.wav'
#record_second                                   记录时间               如果option=0，则为最大录音时间，超过就立刻结束
 #volume                                              音量阈值
#option                                                option = 0           录音保存，选择录入指令，返回录音时间; 
#                                                           option = 1           与提前录入的语音特征值进行DTW算法比较，返回最大音量volume和匹配距离d
                                                          
def GetMicrophoneData(data_save_path = "TemplateOutput.wav",data_feature_save_path='TemplateOutput.npy',ingame_data_save_path='InGameOutput.wav',volume=800,record_second=5,option=0):
    #初始化音频实例
    p = pyaudio.PyAudio()
    stream = p.open(
            format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            frames_per_buffer = CHUNK,
        )
    #设置文件保存路径
    if option==0 :
        wf = wave.open(data_save_path,"wb")
    elif option==1:
        wf = wave.open(ingame_data_save_path,"wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)


    v= 0
   
    #####################################################################
   #监测麦克风语音
    MonitorMicrophone(volume)
    flag =1
    temp = 0
    endflag =0
    ######################################################################
   
    #检测到麦克风有声音，开始录音和保存数据，并获取特征值
    if option==0:
        time_1 = time.time()
        while(flag==1):
            for i in tqdm(range(0, int(RATE / CHUNK * 5))):
                data = stream.read(CHUNK)                                                   #data类型为字符串
                audio_data = np.frombuffer(data, dtype=np.short)
                temp = np.max(audio_data)
                if temp <volume:
                    endflag =endflag+1
                else:
                    endflag = 0
                time_2=time.time()
                if keyboard.is_pressed('enter') or endflag==3:
                    endflag =0
                    flag =0
                    break
                wf.writeframes(data)                                                               #数据写入文件
                
            
        print("录音时长=",time_2-time_1)
        print("i = ",i)
    elif option==1:
        time_3 = time.time()
        for i in tqdm(range(0,int(RATE / CHUNK * (record_second+0.258)))):
            data = stream.read(CHUNK)                                                   #data类型为字符串
            audio_data = np.frombuffer(data, dtype=np.short)
            v = np.max(audio_data)
            if temp < v:
                temp = v
            wf.writeframes(data)                                                               #数据写入文件
            time_4 =time.time()
        print("第二次录音时间",time_4-time_3)
        print("i = ",i)
    print("volume = ",temp)
    
    if option==0 :
        fs,signal = sciwav.read(data_save_path)                                 #读取模式数据
    elif option==1:
        fs,signal = sciwav.read(ingame_data_save_path)                   #读取实时获取的数据
    feature = get_mfcc(signal,fs)                                                       #获取MFCC特征值


    if option==0 :
        np.save(data_feature_save_path,feature)
    elif option==1:
        tamplate_feature = np.load(data_feature_save_path)
        d = DTW(tamplate_feature,feature)

    print("结束")
    print(len(feature),'\n')
    print(len(feature[0]))

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

    if option==0 :
        return time_2-time_1
    elif option==1:
        return d,int(temp)




if __name__=="__main__":
    volume=5000                #设置音量

    print("按下‘Enter’开始")
    while(True):
        if keyboard.is_pressed('enter'):
            second = GetMicrophoneData(volume=volume,option=0)
            break

    for i in range(0,1000):
        pass

    print("按下‘Enter’开始确认指令")
    while(True):
        if keyboard.is_pressed('enter'):
            v1,d1 = GetMicrophoneData(record_second=second,volume=volume,option=1)
            print()
            break

    success=0
    fail = 0
    skill_level =d1
    level_up = 0
    level_down = 0
    print("按下‘Enter’开始确认指令")
    while(True):
        if keyboard.is_pressed('enter'):
            v2,d2 = GetMicrophoneData(record_second=second,volume=volume,option=1)
            if d2<=1.05*skill_level:
                print("high similarity")
                success = success+1
                skill_level = skill_level - 0.5*d1
                level_up = level_up+1
            else:
                print("low similarity")
                fail = fail+1
                skill_level = skill_level +0.5*d1
                level_down = level_down+1
            print("sucess",success)
            print("fail",fail)
            print("level_up",level_up)
            print("level_down",level_down)
        if keyboard.is_pressed('esc'):
            break
            
 


