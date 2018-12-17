import sqlite3
import urllib.request, json
from urllib.request import urlopen
import serial
import datetime
import time
import re
from time import gmtime, strftime
from time import localtime, strftime
import configparser
import os

configParser = configparser.RawConfigParser()   
configFilePath = r'config.txt'
configParser.read(configFilePath)
myAPI = configParser.get('sys_config','ThingSpeak_API')
COM=configParser.get('sys_config','COM_port_number')
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 
url =configParser.get('sys_config','IFTTT_Url') 
method = "POST"
headers = {"Content-Type" : "application/json"}
baud=configParser.get('sys_config','Baud_rate')

ser=serial.Serial()

ser.baudrate = int(baud) 

ser.port = COM 

print("connected to: " + ser.portstr)

try:
    ser.open()
    
except:
    print('Serial connect fail') 



# ser = serial.Serial(
#             port=COM,\
#             baudrate=int(baud),\
#             parity=serial.PARITY_NONE,\
#             stopbits=serial.STOPBITS_ONE,\
#             bytesize=serial.EIGHTBITS,\
#             timeout=0)

# print("connected to: " + ser.portstr)

# if ser.is_open()==True:
#     print('connection established.')
#this will store the line
seq = []
count = 1
ifttt_count=0

conn = sqlite3.connect('ABB_LGR.db')
cs= conn.cursor()

def create_table():
    cs.execute('CREATE TABLE IF NOT EXISTS ABB_LGR(unix REAL, datestamp TEXT, keyword TEXT, time_ TEXT, CxF REAL, CxF_sd REAL , H2O REAL, H2O_sd REAL )')

create_table()

def send_ifttt(value2,value3):
    global ifttt_count
    ifttt_count+=1
    if ifttt_count==3:
        try:
            read_time=strftime("%d %b %Y %H:%M:%S +0800", localtime())
            list_time=read_time.split()
            alarm_time=list_time[1]+'_'+list_time[2]+'_'+list_time[4]
            obj = {"value1":alarm_time,"value2": value2,"value3":value3}
            json_data = json.dumps(obj).encode("utf-8")
            request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
            with urllib.request.urlopen(request) as response:
                response_body = response.read().decode("utf-8")
            ifttt_count=0
        except:
            read_time=strftime("%a, %d %b %Y %H:%M:%S +0800", localtime())
            list_time=read_time.split()
            Log = open('Error_log.txt' ,'a+')
            Log_txt='\n'+list_time[1]+'_'+list_time[2]+'_'+list_time[3]+'_'+list_time[4]+'_'+'IFTTT connect error'
            Log.write(Log_txt)
            print('IFTTT Error!!')
            ifttt_count=0

def upload_TS(data1,data2,data3,data4,data5):
    global count
    try:
        conne = urlopen(baseURL + '&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s' % (data1, data2,data3,data4,data5))
        # Closing the connection
        print(conne.read())
        conne.close()
    except Exception as e:
        read_time=strftime("%a, %d %b %Y %H:%M:%S +0800", localtime())
        list_time=read_time.split()
        error_message=str(e)
        Log = open('Error_log.txt' ,'a+')
        Log_txt='\n'+list_time[1]+'_'+list_time[2]+'_'+list_time[3]+'_'+list_time[4]+'_'+error_message
        Log.write(Log_txt)
        count+=1
        print('ERROR :',error_message)

def save_data(value1,value2,value3,value4,value5):
    try:
        time_= value1
        HF= float(value2)*1000
        H2O= float(value4)*1000
        HF_sd=float(value3)*1000
        H2O_sd=float(value5)*1000
        unix= time.time()
        date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        keyword = 'python'
        test=[unix, date, keyword, time_, HF, HF_sd, H2O, H2O_sd]
        print(unix, date, keyword, time_, HF, HF_sd, H2O, H2O_sd)
        cs.execute("INSERT INTO ABB_LGR(unix, datestamp, keyword, time_, CxF, CxF_sd, H2O, H2O_sd) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", test)
        conn.commit()
    except:
        print('database write error !!')


while True:
    if ser.isOpen()==False:
        print('Serial connect fail')
        time.sleep(1)
        print('reconnecting to '+ ser.portstr+'...')
        try:
            ser.open()
        except:
            #print('reconnecting....')
            time.sleep(1)
            continue

    try:
        for c in ser.read():
            joined_seq = ''
            seq.append(chr(c)) #convert from ANSII
            joined_seq = ''.join(str(v) for v in seq) #Make a string from array

            if chr(c) == 'd':
                #if len(joined_seq)>400:
                #    if len(joined_seq)<500:
                        #print(len(joined_seq))
                        #print(joined_seq)
                list_of_records = joined_seq.split(',')
                        #print(list_of_records)

                        # if len(list_of_records)<4:
                        #     record=',data lost !!'
                        #     #save_data(record)
                        #     seq = []
                        #     count += 1
                        #     continue
                        #if count%5==0:
                        #print(list_of_records[2])
                        #print(float(list_of_records[2]))
                        #print(list_of_records[4])
                        #print(float(list_of_records[4]))
                        #if len(list_of_records[0])>22 :
                save_data(list_of_records[0], list_of_records[3], list_of_records[4], list_of_records[5], list_of_records[6])
                        #print(T0,T1,T2,T3,Humi)
                        #print("to save data")

                        # if list_of_records[3]=='FAULT_OPEN':
                        #     Item='TC Fault Open'
                        #     value='T0'
                        #     #send_ifttt(Item,value) 

                        # if list_of_records[3]!='FAULT_OPEN':
                        #     T0= float(list_of_records[3])
                        #     if T0>40:
                        #         Item='Room High Temp Warning!!'
                        #         value=T0
                        #         #send_ifttt(Item,value) 

                        #if count%20==0:
                            #upload_TS(list_of_records[3], list_of_records[5], list_of_records[7], list_of_records[9],list_of_records[11])
                seq = []
                # count += 1
                # break
    except:
        print('Serial port disconnected !!')
        time.sleep(1)
        ser.close()
        continue


ser.close()


