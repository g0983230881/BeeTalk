from flask import Flask, render_template, Response
import cv2

class VideoCamera(object):
    def __init__(self):
        # 通過opencv獲取實時視頻流
        self.video = cv2.VideoCapture("rtsp://voiplab:voiplab168@192.168.137.91:554/stream1") 
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # 因為opencv讀取的圖片并非jpeg格式，因此要用motion JPEG模式需要先將圖片轉碼成jpg格式圖片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

app = Flask(__name__)


def index():
    # jinja2模板，具體格式保存在index.html檔案中
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        # 使用generator函式輸出視頻流， 每次請求輸出的content型別是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')  # 這個地址回傳視頻流回應
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')   

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  