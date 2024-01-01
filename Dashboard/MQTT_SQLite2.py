import paho.mqtt.client as mqtt
import datetime,sqlite3
import demjson
DB_File = "AS2.db"
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("bee_talk/in_out")
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
        c.execute("insert into DATA2(NO,IN_COUNT,OUT_COUNT,DATETIME) VALUES("+str(KEY)+",'"+str(message['bee_in'])+"','"+str(message['bee_out'])+"','"+datetime_str+"')")
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