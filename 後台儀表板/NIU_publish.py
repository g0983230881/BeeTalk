from flask import Flask,render_template,request,jsonify,Response
import sqlite3
import paho.mqtt.publish as publish
import datetime
import demjson
import cv2
import time

DB_File = "AS.db"
DB_File2 = "AS2.db"
app = Flask(__name__)

#camera = cv2.VideoCapture('rtsp://admin:dh123456@203.145.202.157:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif')#
#camera = cv2.VideoCapture('rtsp://voiplab:voiplab168@192.168.137.91:554/stream1') wifi
#camera = cv2.VideoCapture('rtsp://voiplab:voiplab168@192.168.43.253:554/stream1')#new ap wifi
camera = cv2.VideoCapture('rtsp://voiplab:voiplab168@192.168.43.253:554/stream2')


#host = "203.145.202.162"              # Broker's IP
#topic = "BeeCT"           # Topic
#var =1                          # Declare variable



def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            frame = camera.read()
            continue
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 



@app.route('/') #路由
def index():
    return 'Hello World!'
    
@app.route('/setT/') #路由
def setT():
	data=[]
	time=[]
	conn = sqlite3.connect(DB_File)
    
	c = conn.cursor()
    
	cursor = c.execute("select WEIGHT,substr(DATETIME, 12, 14) from DATA2  order by NO desc  Limit 5")
    
	results = cursor.fetchall()
	conn.commit()
	cursor.close()
	conn.close()
	for i in range(5):
		try:
		    data.append(float(results[4-i][0]))
		    time.append(results[4-i][1])
		except:
		    data.append(0)
		    time.append(i)
	chart={'data':data,'time':time}
	return jsonify(chart) #
@app.route('/setT2/') #
def setT2():
    data=[]
    data2=[]
    time=[]
    conn = sqlite3.connect(DB_File2)
        
    c = conn.cursor()
       
    cursor = c.execute("select IN_COUNT,OUT_COUNT,substr(DATETIME, 12, 14) from DATA2 order by NO desc  Limit 5")
        
    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    for i in range(5):
        try:
            data.append(float(results[4-i][0]))
            data2.append(float(results[4-i][1]))
            time.append(results[4-i][2])
        except:
            data.append(0)
            data2.append(0)
            time.append(i)
    chart={'data':data,'data2':data2,'time':time}
    return jsonify(chart) #
@app.route('/relay/<VAL>')
def relay(VAL):
    print(VAL)
    
    #host = "203.145.202.162" 
    host = "49.159.93.218"              # Broker's IP
    topic = "bee_talk/mesh"           # Topic
    if VAL=="open":
        status="1"
        #publish.single(topic, status, qos=1, hostname=host)
        #time.sleep(5)
        #status="0"
    elif VAL=="close":
        status="2"
    elif VAL=="auto":
        status="0"
        #publish.single(topic, status, qos=1, hostname=host)
        #time.sleep(5)
        #status="0"
    else:
        status="3"
    publish.single(topic, status, qos=1, hostname=host) #publish message
    return""
@app.route('/relay1/<VAL>')
def relay1(VAL):
    print(VAL)
    
    #host = "203.145.202.162" 
    host = "49.159.93.218"              # Broker's IP
    topic = "bee_talk/sugar"           # Topic
    if VAL=="manual":
        status="1"
        publish.single(topic, status, qos=1, hostname=host)
        time.sleep(10)
        status="0"
    #elif VAL=="auto":
        #status="0"
    else:
        status="3"
    publish.single(topic, status, qos=1, hostname=host) #publish message
    return""
@app.route('/bee')  #
def bee():
    return render_template('bee_v2.html')
@app.route('/bee2')  #
def bee2():
    return render_template('bee2.html')    
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)