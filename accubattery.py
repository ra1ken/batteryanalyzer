import os
import time
import csv
import glob

path = "/sys/class/power_supply/BAT0"


def reset():
    logs = glob.glob("log*.txt")

    if logs == []:
        print("no logs present")
    else : 
        print("deleting previous logs")
        for log in logs:
            os.remove(log) 


def bat():
    with open(f"{path}/capacity", "r") as f_in: 
        read = f_in.readline()
        with open(f"logc.txt", "a") as f_out:
            f_out.write(read)
    with open(f"{path}/voltage_now", "r") as f_in: 
        read = f_in.readline()
        with open(f"logv.txt", "a") as f_out:
            f_out.write(read)
    with open(f"/sys/class/thermal/thermal_zone8/temp", "r") as f_in:
        read = f_in.readline()
        with open(f"logt.txt", "a") as f_out: 
            f_out.write(read)
    with open(f"{path}/power_now", "r") as f_in: 
        read = f_in.readline()
        with open(f"logp.txt", "a") as f_out:
            f_out.write(read)
    time.sleep(10)
    # redo to csv

print("choose your mode\n0. run indefinitely (cancel with ctrl+c)\n1. set minutes")
mode = int(input())
if mode == 0 :
    reset()
    while True:
        try:
            bat()
        except KeyboardInterrupt :
            print("\nctrl + c sent, shutting down... log saved to battery.csv")
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
            cyclesmin = cyclesmin - 1
            print(f"currnet small cycle: {cyclesmin}")
        else :
            minutes = minutes - 1
            print(f"current big cycle {minutes}")
else:
    print("invalid choice")





# /sys/class/thermal/thermal_zone8/temp (battery temp) 
# > cat /sys/class/thermal/thermal_zone8/temp 53000
# csv format (for now)
# timestamp,wattage consumption, temp, voltage 
# will make it read and get averages after either a keyboardInterrupt or after a selected time. 