import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys
import re
import os



#NFC Reader
reader = SimpleMFRC522()

#Options to luanch Chrome in fullscreen kiosk +
#öppnar förstasidan
chrome_options = Options()
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--kiosk")
chrome_options.add_argument("--start-fullscreen")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("disable-setuid-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("file:///home/pi/pi-rfid/web/webbsidor/index.html")


textComp = 0
web_list = os.listdir("/home/pi/pi-rfid/web/webbsidor")



#Funktion för att läsa korten och sätte rätt sida till dem

def read():
    try:
        global textComp
        id, text = reader.read()

        try:
            int(text)

        except ValueError:
            time.sleep(2)
            return
            
        text = str(int(text))
        print(text)
        
        if text != textComp:
            textComp = text
            
            if text + ".html" in web_list:
                driver.get("file:///home/pi/pi-rfid/web/" + text + ".html")
            
            else:
                driver.get("file:///home/pi/pi-rfid/web/index.html")
            
            #print(text)
            time.sleep(0.5)

        else:
            pass
            time.sleep(1)
        


    except KeyboardInterrupt:
        GPIO.cleanup
        raise
    
time.sleep(4)

while True:
    read()


