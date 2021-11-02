import csv
import time
import adafruit_ads1x15.ads1115 as ADS
import board
import math
import busio
from adafruit_ads1x15.analog_in import AnalogIn


# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads1 = ADS.ADS1115(i2c, address=0x48)
ads2 = ADS.ADS1115(i2c, address=0x49)
ads3 = ADS.ADS1115(i2c, address=0x4A)
ads4 = ADS.ADS1115(i2c, address=0x4B)

# Create differential input between pins 0-1 and 2-3
chan1 = AnalogIn(ads1, ADS.P0, ADS.P1)
chan2 = AnalogIn(ads1, ADS.P2, ADS.P3)
chan3 = AnalogIn(ads2, ADS.P0, ADS.P1)
chan4 = AnalogIn(ads2, ADS.P2, ADS.P3)
chan5 = AnalogIn(ads3, ADS.P0, ADS.P1)
chan6 = AnalogIn(ads3, ADS.P2, ADS.P3)
chan7 = AnalogIn(ads4, ADS.P0, ADS.P1)
chan8 = AnalogIn(ads4, ADS.P2, ADS.P3)

gains = (2/3, 1, 2, 4, 8, 16)
g = gains[0]
ads1.gain = g
ads2.gain = g
ads3.gain = g
ads4.gain = gains[5]

sampleRate = 2




# Establish the name of the file
date = time.strftime("%m-%d-%Y_%H:%M:%S")
timeout = time.time() + 122400
filename = 'CSVs/Test-'+ date +'.csv'
print(filename)
outputKeys = ['Time','SCV1','SCC2', 'PVV3', 'PVC4', 'LOADV5','LOADC6','DIFF', 'PYRA']

# Loop printing measurements every second.
# print('Press Ctrl-C to quit.')

#Scaling factors for voltage and current transducer read-ins
v = 10
v_solar = 30
a = 6
pyra = 69.9 * (10 ** -6)


def get_pyra(chanNum):
    try:
        value = (chanNum.voltage)/pyra
    except OSError:
        value = math.nan
    return value

def get_voltage(chanNum, factor):
    try:
        value = (chanNum.voltage)*factor
    except OSError:
        value = math.nan
    return value

def get_current(chanNum):
    try:
        value = (chanNum.voltage)*a
    except OSError:
        value = math.nan
    return value

def pyra_wait(chanNum):
    current_time = time.strftime("%M%S")
    if (int(current_time[0:2]) % 5 == 0 and int(current_time[2:]) < sampleRate):
        value = get_pyra(chanNum)
    else:
        value = None
    return value

# Open file for csv
with open(filename,'w') as csvfile:
    filewriter = csv.DictWriter(csvfile, outputKeys)
    filewriter.writeheader()
    while True:
        start_time = time.time()
        #if time.time() > timeout:
        #current_diff = chan2.voltage*a - chan6.voltage*a
        Outputs = {
            'Time' : time.strftime("%m:%d-%H:%M:%S"),
            'SCV1': get_voltage(chan1, v),
            'SCC2': get_current(chan2),
            'PVV3': get_voltage(chan3, v_solar),
            'PVC4': get_current(chan4)
            'LOADV5': get_voltage(chan5, v),
            'LOADC6': get_current(chan6),
            'PYRA': pyra_wait(chan8)
        }
       
        filewriter.writerow(Outputs)
        csvfile.flush()
        
        if time.time() > timeout:
            print("Time's up!")
            break
        
        time.sleep(sampleRate - ((time.time() - start_time) % sampleRate))


#plot csv values across figures

        


