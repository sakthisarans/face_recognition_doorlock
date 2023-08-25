import RPi.GPIO as GPIO
import time

relay=8
pir=10



def relayon():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False) 
	GPIO.setup(relay,GPIO.OUT)
	GPIO.output(relay,GPIO.LOW)
	
def relayoff():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False) 
	GPIO.setup(relay,GPIO.OUT)
	GPIO.output(relay,GPIO.HIGH)
	


