import cv2
from datetime import datetime
import os
import threading
import time
import RPi.GPIO as GPIO
import requests

cam = cv2.VideoCapture(0)  #default 0 untuk webcam laptop
                            #selain 0 (1), (2) untuk webcam

pir_sensor = 27
buzzer = 13
dimension = (480,320)

path = os.getcwd() + "/capture"
GPIO.setmode(GPIO.BCM)  #GPIO.setmode(GPIO.BCM) 
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(pir_sensor, GPIO.IN)

def start_open_camera():
    t1  = threading.Thread(target=open_camera)
    t1.start()

def open_camera():
    global frame
    while True:
        ret, frame = cam.read()
        
        if not ret:
            print("failed to open camera")
            break
        
        frame = cv2.resize(frame,dimension)
        
        cv2.imshow("streaming camera", frame) 
                
        key = cv2.waitKey(1) & 0xFF   # membaca input keyboard dari pengguna
        
        if key==ord('q'):
            print("quit by keyboard")
            break
        if key==ord('c'):  #ketika pencet C akan capture kamera
            #name_file = "test.jpg"
            nama_file = datetime.now().strftime("%Y:%m:%d_%h:%m:%S")
            image = cv2.imwrite(path + "/" + nama_file + ".jpg", frame)    #fungsi untuk menyimpan gambar
            print("sukses simpan gambar denga nama file ", nama_file)
            

    cam.release()
    cv2.destroyAllWindows()

def capture_image():
    global frame
    try:
        dt_string = datetime.now().strftime("%Y:%m:%d_%h:%m:%S")
        nama_file = dt_string + ".jpg"
        image = cv2.imwrite(path + "/" + nama_file, frame)    #fungsi untuk menyimpan gambar
        print("sukses simpan gambar denga nama file ", nama_file)
        send_image_to_telegram(nama_file)
    except Exception as e:
        print(f'[FAILED] capture_image= {e}' )

def send_image_to_telegram(file_img):	
	try:
		TOKEN = "5841063976:AAH6AZB5Y-NjnOlR8xTDyrSOlUrTkuNBYIA"  #token bot kelompok
		chat_id = "1328040261"   #ganti chat id pengguna
		image=open(path+'/'+file_img,'rb')
		url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}"
		resp=requests.get(url,files={'photo':image}) 

		if int(resp.status_code)==200:
			print('succes send to telegram')

	except Exception as e:
		print(f'[FAILED] send image to telegram with error = {e}' )

if __name__ == '__main__':
    if not os.path.exists(path):
        print("[INFO] Membuat folder capture")
        os.mkdir(path)
    else:
        print("[INFO] folder capture sudah terbentuk")

    
    start_open_camera() #running dengan menggunakan threading
    
    while True:
        if GPIO.input(pir_sensor): #ketika pir aktif   
            print("[INFO] PIR  terdeteksi")
            capture_image()
        else:
            print("[INFO] PIR tidak terdeteksi")
            
        time.sleep(2)
        