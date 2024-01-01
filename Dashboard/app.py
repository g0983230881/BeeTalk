from flask import Flask,render_template,request,jsonify
import sqlite3
import paho.mqtt.publish as publish
import datetime
import demjson
DB_File = "AS.db"
app = Flask(__name__)  #绑定app

@app.route('/') #路由
def index():
    return 'Hello World!'
@app.route('/setT/') #路由
def setT():
	data=[]
	data2=[]
	time=[]
	conn = sqlite3.connect(DB_File)
    
	c = conn.cursor()
    
	cursor = c.execute("select round(avg(WEIGHT),2),substr(DATETIME, 12, 14) from DATA2 group by substr(DATETIME, 1, 14) order by NO desc  Limit 10")
    
	results = cursor.fetchall()
	conn.commit()
	cursor.close()
	conn.close()
	for i in range(10):
		try:
		    data.append(float(results[9-i][0]))
		    time.append(results[9-i][1])
		except:
		    data.append(0)
		    time.append(i)
	chart={'data':data,'time':time}
	return jsonify(chart) #回傳JSON資料

# @app.route('/relay/<VAL>')
# def relay(VAL):
	# print(VAL)
	# host = "203.145.202.162"              # Broker's IP
	# topic = "NIU"           # Topic
	# if VAL=="open":
		# status="1"
	# elif VAL=="close":
	    # status="0"
	# else:
	    # status="3"
	# publish.single(topic, status, qos=1, hostname=host) #publish message
	# return""
@app.route('/CHART')  #路由
def CHART():
    return render_template('CHART.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)
