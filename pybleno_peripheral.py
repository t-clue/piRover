from pybleno import *
from MotorDriver import *

bleno = Bleno()

APPROACH_SERVICE_UUID = '5DBD7BF8-0539-4CA0-9534-8738123D9DBC'
APPROACH_CHARACTERISTIC_UUID = '18A19BD2-C200-4761-BE91-95A48CC30B6A'


class ApproachCharacteristic(Characteristic):

    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': APPROACH_CHARACTERISTIC_UUID,
            'properties': ['read', 'write', 'notify'],
            'value': None
        })

        self._value = "matsu"
        self._updateValueCallback = None

        gpio_pwma = 12
        gpio_ain1 = 7
        gpio_ain2 = 26

        gpio_pwmb = 13
        gpio_bin1 = 6 
        gpio_bin2 = 5 

        self.driver_a = MotorDriver(gpio_ain1, gpio_ain2, gpio_pwma)
        self.driver_b = MotorDriver(gpio_bin1, gpio_bin2, gpio_pwmb)

    def onReadRequest(self, offset, callback):
        print('onReadRequest')
        callback(Characteristic.RESULT_SUCCESS, self._value)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        print('EchoCharacteristic - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))

        if self._updateValueCallback:
            print('EchoCharacteristic - onWriteRequest: notifying');
            self._updateValueCallback(self._value)
            self.driver_a.set_accel(data)

        
        callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print('ApproachCharacteristic - onSubscribe')
        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        print('ApproachCharacteristic - onUnsubscribe')
        self._updateValueCallback = None


def onStateChange(state):
    print('on -> stateChange: ' + state)

    if (state == 'poweredOn'):
        bleno.startAdvertising('Approach', [APPROACH_SERVICE_UUID])
    else:
        bleno.stopAdvertising()


bleno.on('stateChange', onStateChange)

approachCharacteristic = ApproachCharacteristic()


def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': APPROACH_SERVICE_UUID,
                'characteristics': [
                    approachCharacteristic
                ]
            })
        ])


bleno.on('advertisingStart', onAdvertisingStart)

bleno.start()


import time

counter = 0

def task():
    global counter
    counter += 1
    approachCharacteristic._value = counter

    if approachCharacteristic._updateValueCallback:

        print('Sending notification with value : ' + str(approachCharacteristic._value))

        notificationBytes = str(approachCharacteristic._value).encode()
        approachCharacteristic._updateValueCallback(notificationBytes)
        print(notificationBytes)
        print(approachCharacteristic._value)

while True:
#    task()
    time.sleep(1)

