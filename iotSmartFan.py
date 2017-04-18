import os
import sys
import json
import oneWire
from temperatureSensor import TemperatureSensor
from omegaMotors import OmegaPwm, hBridgeMotor

# mark the PWM Expansion Channels connected to H-Bridge IC
# change these if you use different pins!
H_BRIDGE_1A_CHANNEL = 0
H_BRIDGE_2A_CHANNEL = 1
H_BRIDGE_12EN_CHANNEL = 2

oneWireGpio = 1 # mark the sensor GPIO

tempMax = 40
tempMin = 18

dutyMax = 100
dutyMin = 60
dutyStep = 0

def calcFanSpeed (temp):

    # restricting the temperature within the operating range.
    if (temp > tempMax):
        temp = tempMax
    if (temp < tempMin):
        return 0

    tempDelta = temp - tempMin


    duty = dutyMin + (dutyStep * float(tempDelta))

    return duty



def loadConfig ():
    dirName = os.path.dirname(os.path.abspath(__file__))
    with open( '/'.join([dirName, 'config.json']) ) as f:
    	config = json.load(f)
    return config


if __name__ == '__main__':
    conf = loadConfig()

    dutyMin = float(conf['dutyMin'])
    dutyMax = float(conf['dutyMax'])

    tempMin = float(conf['tempMin'])
    tempMax = float(conf['tempMax'])

    dutyStep = (dutyMax - dutyMin)/(tempMax - tempMin )

    if not oneWire.setupOneWire(str(oneWireGpio)):
        print "Kernel module could not be inserted. Please reboot and try again."

    # setup the motor, use OmegaPwm instead of hBridgeMotor if you're using a case fan!
    motor = hBridgeMotor(H_BRIDGE_12EN_CHANNEL, H_BRIDGE_1A_CHANNEL, H_BRIDGE_2A_CHANNEL)

    # SENSOR SETUP BEGIN
    sensorAddress = oneWire.scanOneAddress()

	# instantiate the temperature sensor object
    sensor = TemperatureSensor("oneWire", { "address": sensorAddress, "gpio": oneWireGpio })
    success = sensor.ready
    # SENSOR SETUP END

    if not success:
        print "Sensor was not set up correctly. Please make sure that your sensor is firmly connected to the GPIO specified above and try again."
        sys.exit(0)
    else:
        # read temp value
        temp = sensor.readValue()
        # get the corresponding duty
        duty = calcFanSpeed(temp)
        # give 'er!
        motor.spinForward(duty)

