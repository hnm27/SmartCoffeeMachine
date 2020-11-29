import json
import datetime
import uuid

class Schedule(object):

    def __init__(self,date,time,day,repeat,coffeetype,cups,_id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.date=date
        self.time=time
        self.day=day
        self.repeat = repeat
        self.coffeetype=coffeetype
        self.cups=cups
    
    #saving the schedule 

    def save_schedule(self):
        file = open("schedules.txt", "a")
        schedulestr= self.date+";"+self.time+";"+self.day+";"+self.repeat+";"+self.coffeetype+";"+self.cups+";"+self._id+"\n"
        file.write(schedulestr)
        file.close()
     
                
        




                 
                    




