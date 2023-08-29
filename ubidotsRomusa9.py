import time
import requests
import math
import random
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
PIR = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)

TOKEN = "BBFF-4YlVDsxgumjO0eKxjYWtmZfAZDODRG"  # Put your TOKEN here
DEVICE_LABEL = "romusa9"  # Put your device label here 
VARIABLE_LABEL_1 = "pir"


def build_payload(variable_1):
    value_1 = GPIO.input(27)

    payload = {variable_1: value_1}  #dictionary / JSON

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        print(req.json())
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1)

    print("[INFO] Attemping to send data")
    print("[INFO] send payload to ubidots => " + str(payload))
    post_request(payload)   #kirim data ke ubidots
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(5)
        print("\n")
