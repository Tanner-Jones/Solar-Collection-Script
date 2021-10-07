import csv
import time
import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_bme280


# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads1 = ADS.ADS1115(i2c, address=0x48)
#ads2 = ADS.ADS1115(i2c, address=0x49)
ads3 = ADS.ADS1115(i2c, address=0x4A)

# Create differential input between pins 0-1 and 2-3
chan1 = AnalogIn(ads1, ADS.P0, ADS.P1)
chan2 = AnalogIn(ads1, ADS.P2, ADS.P3)
#chan3 = AnalogIn(ads2, ADS.P0, ADS.P1)
#chan4 = AnalogIn(ads2, ADS.P2, ADS.P3)
chan5 = AnalogIn(ads3, ADS.P0, ADS.P1)
chan6 = AnalogIn(ads3, ADS.P2, ADS.P3)

gains = (2/3, 1, 2, 4, 8, 16)
g = gains[0]
ads1.gain = g
#ads2.gain = g
ads3.gain = g

sampleRate = 1

# create BME object or temp detection
#bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
#bme280.sea_level_pressure = 1013.25





# Establish the name of the file
date = time.strftime("%m-%d-%Y_%H:%M:%S")
timeout = time.time() + 122400
filename = 'CSVs/Test-'+ date +'.csv'
print(filename)
outputKeys = ['Time','SCV1','SCC2','LOADV5','LOADC6','DIFF', 'SCP', 'LOADP', 'TEMP']

# Loop printing measurements every second.
# print('Press Ctrl-C to quit.')

#Scaling factors for voltage and current transducer read-ins
v = 10
a = 6


def get_voltage(chanNum):
    try:
        value = (chanNum.voltage)*v
    except OSError:
        value = "NaN"
    return value

def get_current(chanNum):
    try:
        value = (chanNum.voltage)*a
    except OSError:
        value = "NaN"
    return value


def get_power(chanV, chanI):
    if (chanV == "NaN"):
        value = "NaN"
    elif (chanI == "NaN"):
        value = "NaN"
    else:
        value = chanV*chanI
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
            'SCV1': get_voltage(chan1),
            'SCC2': get_current(chan2),
            #'PVV3': (chan3.voltage)*v,
            #'PVC4': (chan4.voltage)*a,
            'LOADV5': get_voltage(chan5),
            'LOADC6': get_current(chan6),
            #'DIFF':   current_diff,
            'SCP': get_power(get_voltage(chan1),get_current(chan2)),
            #'PVP': ((chan3.voltage)*v)*((chan4.voltage)*a),
            'LOADP': get_power(get_voltage(chan5),get_current(chan6)),
            #'TEMP': bme280.temperature
        }
  
       
        filewriter.writerow(Outputs)
        csvfile.flush()
        
        if time.time() > timeout:
            print("Time's up!")
            break
        
        time.sleep(sampleRate - ((time.time() - start_time) % sampleRate)


#plot csv values across figures

        


