import paho.mqtt.client as mqtt
import datetime,sqlite3
import demjson

##
import requests
token = 'EbZasFPM7y6HPYvT7HlKvYwwg8w2vfWaJ4DYDTpxDVp'## notify金鑰 博宇的(每月上限500封 測試請注意數量)
##

DB_File = "AS.db"
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("bee_talk")
def on_message(client, userdata, msg):
    datetime_str = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")# 獲得當地時間
    message =demjson.decode(str(msg.payload, encoding = "utf-8"))#解析資料
    conn = sqlite3.connect(DB_File)
    c = conn.cursor()
    cursor = c.execute("select * from DATA2 order by NO desc")
    #cursor = d.execute("select * from DATA2 order by NO desc")
    #執行查詢語法
    r=cursor.fetchone()
    print(r)
    KEY=0
    if r!=None:
        if len(r)==0:
            KEY=1
        else:
            KEY=r[0]+1
    else:
        KEY=1
    try:    
        c.execute("insert into DATA2(NO,OUT_TEMP,OUT_HUMID,IN_TEMP,IN_HUMID,WEIGHT,VOL,RSSI,DATETIME) VALUES("+str(KEY)+
        ",'"+str(message['out_temp'])+"','"+str(message['out_hum'])+"','"+str(message['in_temp'])+"' ,'"+str(message['in_hum'])+"' ,'"+str(message['weight'])+"' ,'"+str(message['vol'])+"' ,'"+str(message['rssi'])+"' ,'"+datetime_str+"')")  
        
        ##
        command = "select * from DATA2 where NO=%s || NO=%s "
        c.execute(command,str(KEY),str(KEY-1))#抓前一筆及這筆的資料
        r=cursor.fetchall()
        r1=r[0]#當前這筆
        r2=r[1]#前一筆
        dif=float(r1[5])-float(r2[5])#每筆的第6個項目為重量 算重量差
        print(r1[5],r2[5])
        if(dif>1):#5秒降了1公斤
            requests.post(  #發送LINE Notify通知
              url='https://notify-api.line.me/api/notify',
              headers={
             'Authorization': f'Bearer {token}'
              },
              data={
             'message': '目前偵測為重量驟降，若非開箱請盡速前往查看!!'
              })
        ##
        
        #c.execute("insert into DATA2(NO,IN_TEMP,IN_HUMID,DATETIME) VALUES("+str(KEY)+
        #",'"+str(message['in_temp'])+"','"+str(message['in_hum'])+"','"+datetime_str+"')")
    except:
        pass
    #執行新增語法
    conn.commit()#執行
    cursor.close()
    print("Table created successfully")
    conn.close()#關閉連線

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("49.159.93.218", 1883, 60)
client.loop_forever()