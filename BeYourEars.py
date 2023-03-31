import pyaudio
import wave
from aip import AipSpeech
import re
import jieba
import jieba.analyse
import pymysql
from PIL import Image
import matplotlib.pyplot as plt
import os

def start_audio(time = 5,save_file="record.wav"):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = time  #the time of recording
    WAVE_OUTPUT_FILENAME = save_file	#file name
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        #start
        frames.append(data)
	    
    stream.stop_stream()
    stream.close()
    p.terminate()
    #store
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')	
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

#baidu API
APP_ID = 'Scugsrz5aeAdqWlmfSnrWdyr'
API_KEY = 'Scugsrz5aeAdqWlmfSnrWdyr'
SECRET_KEY = 'hidwXPb04yMxZ7K2CsGtaB77M3g1DUgu'
 
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
 
#read audio 
def get_file_content(filePath):
    with open(filePath,'rb') as fp:
        return fp.read()
 
def get_text():
    result = client.asr(get_file_content('record.wav'), 'wav', 16000, {'dev_pid': 1536,})
    txtfile = open('voice.txt','w',encoding='utf-8')
    #write text

    text=str(result)
    try:
        text_list=re.findall('\[.*?\]', text)
        txtfile.write(str(text_list[0])[2:-2])
        txtfile.close()
    except:
        return 0

def readText(filename):
    #read the file
    f = open(filename, "r",encoding='utf-8')
    str = f.readline()
    #search keywords
    global keywords
    keywords = jieba.analyse.extract_tags(str, topK=10)
    return keywords

def photos():
    #link database
    conn = pymysql.connect(host="localhost", port=3306, user='root', passwd='123456', db="schema1")
    cursor = conn.cursor()
    list_path = []
    for keyword in keywords:
        #search photo_path
        cursor.execute("select photo_path from word where word =%s",(keyword,))
        result = cursor.fetchall()
        
        photo_path = str(result)
        #store as list (photo_path : str)
        list_path.append(str(photo_path[3:-5]))#delete the signs
    return list_path
    cursor.close()

#order of functions
"""
    start_audio()
    get_text()
    list_word = readText('voice.txt')  
    list_path = photos()
    display(list_path, list_word)
"""

