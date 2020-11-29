from flask import Flask, render_template, redirect, request, jsonify
import datetime
from gpiozero import LED,Button,LEDBoard
from time import sleep
from Schedule import Schedule
import RPi.GPIO as GPIO
import time
import threading 
from json import JSONEncoder
import json
from signal import pause
import warnings

app = Flask(__name__)
warnings.simplefilter("ignore")
status_led =LED(24)
espresso_led =LED(17)
despresso_led =LED(27)
americano_led=LED(25)
hw_led =LED(22)
button = Button(16) #on/off
buttonr=Button(21) #2cups
buttonl=Button(20) #1cup

# Homepage
@app.route("/home")
def home():
   status = check_status_led()
   return render_template('index.html', status=status)

# Turn on LED
@app.route("/on")
def ledon():
   if check_status_led()=="OFF":
      status_led.blink(n=10)
      sleep(10)
      status_led.on()
   return redirect("/home") 

# Turn off LED  
@app.route("/off")
def ledoff():
   if check_status_led()=="ON":
      status_led.blink(n=10)
      sleep(10)
      status_led.off()
   return redirect("/home")

# Check on or off

@app.route("/checkstatus")
def getstatus():
   return check_status_led()

#Normal functionality of the Coffee Machine

def buttonfunctionality():
   while True:
      if button.is_pressed and check_status_led()=="OFF":
         status_led.blink(n=10)
         sleep(10)
         status_led.on()
      if button.is_pressed and check_status_led()=="ON":
         status_led.blink(n=10)
         sleep(10)
         status_led.off()
      if buttonl.is_pressed and despresso_led.value==0:
         if check_status_led()=="ON":
            despresso_led.blink(n=1)
            sleep(2)
            despresso_led.on()
            sleep(10)
            despresso_led.off()
      if buttonr.is_pressed and despresso_led.value==0: #for the middle button - 2cups
         if check_status_led()=="ON":
            despresso_led.blink(n=2)
            sleep(6)
            despresso_led.on()
            sleep(10)
            despresso_led.off()

#heck status - on or off (status led)

def check_status_led():
   if status_led.value == 0:
      return "OFF"
   else:return "ON"

# Check if machine is free

def machine_status():
   if espresso_led.value == 0 and americano_led.value == 0 and  despresso_led.value == 0 and hw_led.value == 0:
      return "FREE"
   else: return "BUSY"

# make coffee according to type and number of cups
   
def dotask(ctype,num):
   if ctype=="a": 
      if num==1:
         print(num)
         americano_led.blink(n=1)
         sleep(2)
      else:
         print(num)
         americano_led.blink(n=2)
         sleep(6) 
      americano_led.on()
      sleep(10)
      americano_led.off()
   if ctype=="e":
      if num=="1":
         espresso_led.blink(n=1)
         sleep(2)
      else:
         espresso_led.blink(n=2)
         sleep(6)
         
      espresso_led.on()
      sleep(10)
      espresso_led.off()
   if ctype=="de":
      
      if num=="1":
         despresso_led.blink(n=1)
         sleep(2)
      else:
         despresso_led.blink(n=2)
         sleep(6)
      despresso_led.on()
      sleep(10)
      despresso_led.off()
   if ctype=="hw":
      
      if num=="1":
         hw_led.blink(n=1)
         sleep(2)
      else:
         hw_led.blink(n=2)
         sleep(6)
      hw_led.on()
      sleep(10)
      hw_led.off()
      
# Make Americano

@app.route("/makeA/<string:num>",methods=["POST"])
def makeA(num):
   status = check_status_led()
   if status=="ON":
      if machine_status()=="FREE":
         if checkcup()==True:
            threading.Thread(target=dotask,args=("a",num,)).start()
            return render_template('index.html', jsonfile="0", status=status)
         else:
            return render_template('index.html', jsonfile="1", status=status)
      else:
         return render_template('index.html', jsonfile="3", status=status)
   else:
     return render_template('index.html', jsonfile="2", status=status)


#Make Double Espresso

@app.route("/makeDE/<string:num>", methods=["POST"])
def makeE(num):
   status = check_status_led()
   if status=="ON":
      if machine_status()=="FREE":
         if checkcup()==True:
            threading.Thread(target=dotask,args=("de",num,)).start()
            return render_template('index.html', jsonfile="0", status=status)
         else:
            return render_template('index.html', jsonfile="1", status=status)
      else:
         return render_template('index.html', jsonfile="3", status=status)
   else:
      return render_template('index.html', jsonfile="2", status=status)

# Make Espresso

@app.route("/makeE/<string:num>", methods=["POST"])
def makeDE(num):
   status = check_status_led()
   if status=="ON":
      if machine_status()=="FREE":
         if checkcup()==True:
            threading.Thread(target=dotask,args=("de",num,)).start()
            return render_template('index.html', jsonfile="0", status=status)
         else:
            return render_template('index.html', jsonfile="1", status=status)
      else:
         return render_template('index.html', jsonfile="3", status=status)
   else:
      return render_template('index.html', jsonfile="2", status=status)

# Make Hot Water

@app.route("/makeHW/<string:num>", methods=["POST"])
def makehotwater(num):
   status = check_status_led()
   if status=="ON":
      if machine_status()=="FREE":
         if checkcup()==True:
            threading.Thread(target=dotask,args=("hw",num,)).start()
            return render_template('index.html', jsonfile="0", status=status)
         else:
            return render_template('index.html', jsonfile="1", status=status)
      else:
         return render_template('index.html', jsonfile="3", status=status)
   else:
      return render_template('index.html', jsonfile="2", status=status)

#Cup detection

def checkcup():
   #GPIO Mode (BOARD / BCM)
   GPIO.setmode(GPIO.BCM)
   
   #set GPIO Pins
   GPIO_TRIGGER = 18
   
   GPIO_ECHO = 23
   
   #set GPIO direction (IN / OUT)
   GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
   GPIO.setup(GPIO_ECHO, GPIO.IN)
   GPIO.output(GPIO_TRIGGER, True)
   # set Trigger after 0.01ms to LOW
   time.sleep(0.00001)
   GPIO.output(GPIO_TRIGGER, False)
 
   StartTime = time.time()
   StopTime = time.time()
   
    # save StartTime
   while GPIO.input(GPIO_ECHO) == 0:
      StartTime = time.time()
   
   # save time of arrival
   print("next")
   while GPIO.input(GPIO_ECHO) == 1:
      StopTime = time.time()
 
   # time difference between start and arrival
   TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
   distance = (TimeElapsed * 34300) / 2
   if distance<4:
      print(str(distance))
      return True
   else:
      print(str(distance))
      return False

def turnonstatus():
   if check_status_led()=="OFF":
      status_led.blink(n=10)
      sleep(10)
      status_led.on()


# Schedules

def run_schedule():
   while True:
      typestringcof = check_schedule()
      if typestringcof is not None:
         print(typestringcof)
         typestring= typestringcof.split(":")
         ctype = typestring[0]
         cups = typestring[1]
         print(ctype)

         if ctype == "Americano":
            if check_status_led()=="OFF":
               status_led.blink(n=10)
               sleep(10)
               status_led.on()
            if machine_status()=="FREE":
               threading.Thread(target=dotask,args=("a",cups,)).start()
            sleep(20)
               
         if ctype == "Espresso":
            if check_status_led()=="OFF":
               status_led.blink(n=10)
               sleep(10)
               status_led.on()
            if machine_status()=="FREE":
               threading.Thread(target=dotask,args=("e",cups,)).start()
            sleep(20)

         if ctype == "Double Espresso":
            if check_status_led()=="OFF":
               status_led.blink(n=10)
               sleep(10)
               status_led.on()
            if machine_status()=="FREE":
               threading.Thread(target=dotask,args=("de",cups,)).start()
            sleep(20)

         if ctype == "Hot Water":
            if check_status_led()=="OFF":
               status_led.blink(n=10)
               sleep(10)
               status_led.on()
            if machine_status()=="FREE":
               threading.Thread(target=dotask,args=("hw",cups,)).start()
            sleep(20)
      sleep(45)

# Save a schedule to the Txt file

@app.route("/set_schedule",methods = ["POST"])
def set_schedule():
   repeat = request.form["repeat"] 
   if repeat == "0" : #no-repeat
      date= request.form["date"]
      time= request.form["time"]
      day = "None"
   elif repeat == "1" :  #everyday
      time= request.form["time"]
      date= "None"
      day="None"
   else: #everyweek
      day= request.form["day"]
      time= request.form["time"]
      date = "None"
   
   coffeetype= request.form["coffeetype"]
   cups = request.form["cups"]
   s = Schedule(date,time,day,repeat,coffeetype,cups)
   s.save_schedule()
   return redirect("/home")

#get all schedules

@app.route("/get_schedules",methods = ["GET"])
def get_schedules():
   schedules=get_all_schedules()
   status=check_status_led()
   return render_template("/schedules.html",schedules=schedules,status=status)

def getbyid(id):
   schedules=get_all_schedules()
   for s in schedules:
      if s._id == id:
         return s

#get schedules from txt file

def get_all_schedules():
   schedules=[]
   schedlist=[]
   file = open("schedules.txt","r")
   
   for s in file:
      schedules.append(s)
   file.close()
   for s in schedules:
      wordlist=[]
      wordlist=s.split(";")
      date = wordlist[0]
      nowtime = wordlist[1]
      day = wordlist[2]
      repeat = wordlist[3]
      coffeetype = wordlist[4]
      cups= wordlist[5]
      _id=wordlist[6]
      this_sched=Schedule(date,nowtime,day,repeat,coffeetype,cups,_id)
      schedlist.append(this_sched)
   return schedlist

#check schedule in the txt file

def check_schedule():
   now = datetime.datetime.now()
   schedules= get_all_schedules()
   for s in schedules:
      if s.date == now.strftime("%Y-%m-%d") and s.time == now.strftime("%H:%M") and s.repeat=="0": #no-repeat
         return s.coffeetype+":"+s.cups
         
      if s.day == now.strftime("%A") and s.repeat == "2" and s.time == now.strftime("%H:%M"): #everyweek
         return s.coffeetype+":"+s.cups
         
      if s.repeat == "1" and s.time == now.strftime("%H:%M"): #everyday
         return s.coffeetype+":"+s.cups         
   return None


if __name__ == "__main__":
   thread1= threading.Thread(target=buttonfunctionality)
   thread1.daemon=True
   thread1.start()
   thread2= threading.Thread(target=run_schedule)
   thread2.daemon=True
   thread2.start()
   app.run(host='192.168.1.17', port=8000, debug=True) # INSERT R-PI IP Address
   
   
   








