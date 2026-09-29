from picamera2 import Picamera2
import time
from datetime import datetime
import requests
from LocationParser import getLocationUrl

import serial
import time


import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

if not ports:
    print("No serial ports found")
else:
    for i, port in enumerate(ports):
        print(f"{i}: {port.device} - {port.description}")

capture = False

BOT_TOKEN = ""
CHAT_ID = ""


def send_telegram(filename):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    # filename = "pngtree-open.png"

    with open(filename, 'rb') as img:
        response = requests.post(url, data={
            'chat_id': CHAT_ID
        }, files={
            'photo': img
        })

    print("Sent image to Telegram:", response.status_code)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={getLocationUrl()}"

    response = requests.get(url=url)
    print("Sent Location to Telegram:", response.status_code)



# Configure serial (Pi 5 UART)
ser = serial.Serial(
    port="/dev/ttyAMA0",  # default UART
    baudrate=115200,
    timeout=1
)

def send_command(cmd, delay=1):
    ser.write((cmd + '\r').encode())
    time.sleep(delay)
    response = ser.read_all().decode(errors='ignore')
    print(response)
    return response

def send_sms(phone_number, message):
    print("Initializing SIM800...")

    send_command("AT")              # Check module
    ser.readline()
    ser.readline()
    ser.readline()
    send_command("AT+CMGF=1")      # Set text mode
    ser.readline()
    ser.readline()
    ser.readline()
    # Set recipient
    ser.write(f'AT+CMGS="{phone_number}"\r'.encode())
    time.sleep(1)
    ser.readline()
    ser.readline()
    ser.readline()

    # Send message + CTRL+Z
    ser.write((message + "\x1A").encode())
    time.sleep(3)
    ser.readline()
    ser.readline()
    ser.readline()
    ser.readline()
    ser.readline()
    ser.readline()
    print("SMS Sent!")


from mpu6050 import mpu6050
import time
# Initialize sensor
sensor = mpu6050(0x68)
# Read data





import RPi.GPIO as GPIO
import time

BUTTON_PIN = 21  # GPIO17 (Pin 11)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def buttonIsPresed():
    
    try:
        
        accel_data = sensor.get_accel_data()
        gyro_data = sensor.get_gyro_data()
        print(f"\rAccelerometer: {accel_data}", end="")
        # print(f"Gyroscope: {gyro_data}")
        time.sleep(.5)
         # Extract values
        accel_x = accel_data['x']
        accel_y = accel_data['y']
        accel_z = accel_data['z']

        if accel_x < -4 or accel_x > 4 or  accel_y < -4 or accel_y > 4 :
            return True

        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("\rButton Pressed", end="")
            return True
        else:
            # print("Button Released")
            return False

    except KeyboardInterrupt:
        GPIO.cleanup()



while(True):    
    if buttonIsPresed():
        capture = True
    
    if capture:
        capture = False
        picam2 = Picamera2()
        config = picam2.create_still_configuration(
            main={"size": (1920, 1080)}
        )
        picam2.configure(config)
        picam2.start()
        time.sleep(2)


        # Generate unique filename
        file_name = "captured_image.jpg"
        picam2.capture_file(file_name)
        print("file_name:", file_name)

        picam2.stop()
        send_telegram(file_name)

        send_sms("", "Hello Your Vehicle in a car crash, SOS "+getLocationUrl())




