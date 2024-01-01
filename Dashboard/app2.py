from flask import Flask,render_template,request,jsonify
app = Flask(__name__)  #绑定app
import pymysql,datetime
 

@app.route('/') #路由
def index():
    return 'Hello World!'

@app.route('/NIUGET',methods=['GET']) #路由
def NIUGET():
    print("溫度:")
    print(request.args.get('temp'))#獲取http get中的temp數值
    #print("濕度:")
    #print(request.args.get('humid'))#獲取http get中的humid數值
    datetime_str = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    db=pymysql.connect(host="localhost",user="root",passwd="",db="sensor")
    cursor = db.cursor()
    cursor.execute("select * from temp")
    db.commit()
    results = cursor.fetchall()
    db.close()
    KEY=0
    if len(results)==0:
        KEY==1
    else:
        KEY=results[len(results)-1][0]+1
    print(KEY)
    db=pymysql.connect(host="localhost",user="root",passwd="",db="sensor")
    cursor = db.cursor()
    cursor.execute("insert into temp(ID,tempvalue,date) VALUES("+str(KEY)+",'"+request.args.get('temp')+"','"+datetime_str+"')")
    db.commit()
    db.close()
    return ""
    
# @app.route('/NIUPOST',methods=['POST']) #路由
# def NIUPOST():
    # print(request.headers)#獲取http header的內容
    # print(request.json)#獲取json資料內容
    # print("溫度:")
    # print(request.json['temp'])#獲取內容
    # print("濕度：")
    # print(request.json['humid'])#獲取內容
    # return ""

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)
