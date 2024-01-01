import cv2
import queue
import time
import threading
q=queue.Queue()

def Receive():
    print("start Revive")
    cap=cv2.VideoCapture('rtsp://admin:dh123456@203.145.202.157:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif')
    ret,frame=cap.read()
    q.put(frame)
    while ret:
        ret,frame=cap.read()
        q.put(frame)

def Display():
    print("Start Displaying")
    ret,frame=cap.read()
    while True:
        if q.empty() !=True:
            frame.get()
            cv2.imshow("frame1",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
if __name__=='__main__':
    p1=threading.Thread(target=Receive)
    p2=threading.Thread(target=Display)
    p1.start()
    p2.start()
# import cv2
# cap=cv2.VideoCapture('rtsp://admin:dh123456@203.145.202.157:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif')

# ret,frame=cap.read()
# while ret:
    # ret,frame=cap.read()
    # cv2.imshow("frame",frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break
        
# cv2.destroyAllWindows()
# cap.release()