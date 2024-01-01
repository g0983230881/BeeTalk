from flask import Flask,render_template,request,jsonify
import sqlite3
import paho.mqtt.publish as publish
import datetime
import demjson
DB_File = "AS.db"
app = Flask(__name__)

@app.route('/') #路由
def index():
    return 'Hello World!'
@app.route('/tt')  #路由
def tt():
    return render_template('tt.html')
if __name__=='__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)
