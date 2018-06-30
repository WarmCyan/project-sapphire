import datetime
import time

schedule = []

def getSchedule():
    global schedule

    schedule = []

    with open("schedule.dat", 'r') as f:

        for line in f:
            schedule.append(line.rstrip())


def writeSchedule():
    global schedule

    with open("schedule.dat", 'w') as f:
        
        for line in schedule:
            if line != "\n":
                f.write(line + "\n")
    
def getNextTime():
    now = datetime.datetime.now()
    then = now + datetime.timedelta(0,11)

    schedule.append(str(int(then.timestamp())) + " hi")

getNextTime()
writeSchedule()

while True:
    print("checking schedule...")
    getSchedule()

    for line in schedule:
        parts = line.rstrip().split(' ')

        now = datetime.datetime.now()

        if datetime.datetime.fromtimestamp(int(parts[0])) < now:
            string = ""
            for part in parts[1:]:
                string += part
            print(string)
            schedule = []
            getNextTime()
            writeSchedule()
    time.sleep(5) 
