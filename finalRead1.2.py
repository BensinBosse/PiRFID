import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys
import re




#NFC Reader
reader = SimpleMFRC522()

#Options to luanch Chrome in fullscreen kiosk
chrome_options = Options()
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--kiosk")
chrome_options.add_argument("--start-fullscreen")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("disable-setuid-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("file:///home/pi/pi-rfid/web/index.html")


textComp = 0

def read():
    try:
        global textComp
        id, text = reader.read()
        #print(text)

        try:
            int(text)

        except ValueError:
            time.sleep(2)
            read()

        text = str(int(text))
        print(text)

        if (text != textComp):
            textComp = text
            driver.get("file:///home/pi/pi-rfid/web/" + text + ".html")
            #print(text)
            time.sleep(0.5)
            read()

        else:
            pass
            time.sleep(1)
            read()

	

    except KeyboardInterrupt:
        GPIO.cleanup
        raise
time.sleep(4)
read()

