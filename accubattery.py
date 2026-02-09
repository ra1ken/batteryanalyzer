import os
import time
import datetime as dt
import csv

path = "/sys/class/power_supply/BAT0"

def header():
    header =  ['capacity' , 'voltage', 'temperature', 'wattage', 'unix_timestamp'] 
    print("writing header...")
    with open(f"battery.csv" , "w") as f:
        f.write(", ".join(map(str,header)) + "\n")

def reset():
    if os.path.exists("battery.csv"):
        os.remove("battery.csv")
        print("removing previous test")
        header()
    else:
        print("no battery.csv present")
        header()
        

def bat():
    with open(f"{path}/capacity", "r") as f_in: 
        read = f_in.readline()
        capacity = read
    with open(f"{path}/voltage_now", "r") as f_in: 
        read = f_in.readline()
        voltage = read
    with open(f"/sys/class/thermal/thermal_zone8/temp", "r") as f_in:
        read = f_in.readline()
        temp = read
    with open(f"{path}/power_now", "r") as f_in: 
        read = f_in.readline()
        wattage = read
    data = [capacity.strip(),(int(voltage)/1000000),int(temp)/1000,int(wattage.strip())/1000000,int(dt.datetime.now().timestamp())]
    print(data)
    with open(f"battery.csv" , "a") as f:
        f.write(", ".join(map(str,data))  + "\n")
    time.sleep(10)

def avg():
    for i in range (1,4):
        array = []
        with open('battery.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            rowCount = 0

            for row in csv_reader:
                    if rowCount == 0:
                        rowCount =+ 1
                    else:
                        cislo = float(row[i])
                        rowCount = rowCount+ 1
                        array.append(cislo)
        total = sum(array)
        totalRows = rowCount -1
        avg = total/totalRows
        if i == 1:
            print(f"voltage: {round(avg, 2)}V")
        elif i == 2:
            print(f"internal temperature: {round(avg, 2)}°C")
        elif i == 3:
            print(f"wattage: {round(avg, 2)}W")


print("choose your mode\n0. run indefinitely (cancel with ctrl+c)\n1. set minutes")
mode = int(input())
if mode == 0 :
    reset()
    while True:
        try:
            bat()
        except KeyboardInterrupt :
            print("\nctrl + c sent, here are your averages, full log in battery.csv")
            avg()
            break
elif mode == 1:
    reset()
    print("enter amount of minutes") 
    minutes = int(input())
    print(f"minutes: {minutes}")
    while minutes > 0:
        print("starting small cycle")
        cyclesmin = 6
        while cyclesmin > 0:
            bat()
            cyclesmin -= 1
            print(f"currnet small cycle: {cyclesmin}")
        else :
            minutes = minutes - 1
            print(f"current big cycle {minutes}")
            if minutes == 0:
                print("finished! here are your averages, full log in battery.csv")
                avg()
else:
    print("invalid choice")