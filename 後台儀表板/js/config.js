// let ADDR_IP_CAM = "CamIP";  //camera IP
// let PORT_IP_CAM_API = "CamPort";  //camera HTTP port 
// let VIDEO_FILE_NAME = "MJPG file name"; //MJPG file name

let ADDR_iframe1 = "//iottalk.niu.edu.tw/test/SwitchSet/Sensor_Controll/3/"; //Remote control
let height_iframe1 = "100%"; 
let ADDR_iframe2 = "//iottalk.niu.edu.tw/test/dashboard/demo/Sensor_O?token=d816e124-5207-47f5-946c-e97552ce68e1"; //Dashboard webpage
let height_iframe2 = "100%";

let config = {
    cameras: {
        "cam1": {
            displayName: "豬舍攝影機",
            mjpegUrl: "./cam/cam1.php",
            controlEnabled: false
        },
    }
}
