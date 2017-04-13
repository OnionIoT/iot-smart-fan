
import time
import oneWire
from temperatureSensor import TemperatureSensor
from omegaMotors import hBridgeMotor

# setup PWM Expansion Channels connected to H-Bridge IC
H_BRIDGE_1A_CHANNEL = 0
H_BRIDGE_2A_CHANNEL = 1
H_BRIDGE_12EN_CHANNEL = 2

# instantiate gpio objects for our switch inputs
directionGPIO = onionGpio.OnionGpio(0)
speed1GPIO = onionGpio.OnionGpio(1)
speed2GPIO = onionGpio.OnionGpio(2)

oneWireGpio = 1 # set the sensor GPIO

tempMax = 40
tempMin = 18
dutyDelta = 0

def calcFanSpeed (temp):
    if (temp > tempMax):
        temp = tempMax
    if (temp < tempMin):
        temp = tempMin
    #FINISH



def fillLookupTable ():
    dirName = os.path.dirname(os.path.abspath(__file__))
    with open( '/'.join([dirName, 'config.json']) ) as f:
    	config = json.load(f)

    dutyDelta = config['dutyMin'] - config['dutyMax']
    #FINISH

if __name__ == '__main__':

    conf = loadConfig

    #FINISH

    if not oneWire.setupOneWire(str(oneWireGpio)):
        print "Kernel module could not be inserted. Please reboot and try again."
        return -1

    # get the address of the temperature sensor
    sensorAddress = oneWire.scanOneAddress()

	# instantiate the temperature sensor object
    sensor = TemperatureSensor("oneWire", { "address": sensorAddress, "gpio": oneWireGpio })
    if not sensor.ready:
        print "Sensor was not set up correctly. Please make sure that your sensor is firmly connected to the GPIO specified above and try again."
        return -1

    # Read value code
    value = sensor.readValue()
