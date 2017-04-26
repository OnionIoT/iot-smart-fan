import os
import sys
import json
import oneWire
from temperatureSensor import TemperatureSensor
from omegaMotors import OmegaPwm, hBridgeMotor

# PWM channels for case fan, plus additional channels for H-bridge operation
H_BRIDGE_1A_CHANNEL = 1
H_BRIDGE_2A_CHANNEL = 2
FAN_PWM_CHANNEL = 0

oneWireGpio = 3 # mark the sensor GPIO

tempMax = 0
tempMin = 0

dutyMax = 0
dutyMin = 0
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




if __name__ == '__main__':
    dirName = os.path.dirname(os.path.abspath(__file__))
    with open( '/'.join([dirName, 'config.json']) ) as f:
        config = json.load(f)

    dutyMin = float(config['dutyMin'])
    dutyMax = float(config['dutyMax'])

    tempMin = float(config['tempMin'])
    tempMax = float(config['tempMax'])

    dutyStep = (dutyMax - dutyMin)/(tempMax - tempMin )

    fan = OmegaPwm(FAN_PWM_CHANNEL)
    fan._setFrequency(config['frequency'])


    if not oneWire.setupOneWire(str(oneWireGpio)):
        print "Kernel module could not be inserted. Please reboot and try again."


    #~~~ SENSOR SETUP BEGIN

    sensorAddress = oneWire.scanOneAddress()

	# instantiate the temperature sensor object
    sensor = TemperatureSensor("oneWire", { "address": sensorAddress, "gpio": oneWireGpio })
    success = sensor.ready

    #~~~ SENSOR SETUP END

    if not success:
        print "Sensor was not set up correctly. Please make sure that your sensor is firmly connected to the GPIO specified above and try again."
        sys.exit(0)
    else:
        # read temp value
        temp = sensor.readValue()
        # get the corresponding duty
        duty = calcFanSpeed(temp)
        # give 'er!
        fan.setDutyCycle(duty)

