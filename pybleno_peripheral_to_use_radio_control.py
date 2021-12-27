from pybleno import *
from MotorDriver import *
from ServoDriver import *

bleno = Bleno()

APPROACH_SERVICE_UUID = '5DBD7BF8-0539-4CA0-9534-8738123D9DBC'

class ApproachCharacteristic(Characteristic):
    def __init__(self, uuid, name):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write', 'notify'],
            'value': None
        })
        self.name = name

        self._value = "matsu"
        self._updateValueCallback = None

    def onReadRequest(self, offset, callback):
        print('onReadRequest')
        callback(Characteristic.RESULT_SUCCESS, self._value)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        print('EchoCharacteristic - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        if self._updateValueCallback:
            print('EchoCharacteristic - onWriteRequest: notifying');
            self._updateValueCallback(self._value)
            self.didGetData(data)
        callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print(self.name + ' - onSubscribe')
        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        print(self.name + ' - onUnsubscribe')
        self._updateValueCallback = None

    def didGetData(self, data):
        return

class ApproachCharacteristicGimbal(ApproachCharacteristic):
    def __init__(self):
        super().__init__(APPROACH_CHARACTERISTIC_GIMBAL_UUID, "ApproachCharacteristicGimbal")

        gpio_pin = 18
        self.driver = ServoDriver(gpio_pin)

    def didGetData(self, data):
        self.driver.set_degree(int(data))

def onStateChange(state):
    print('on -> stateChange: ' + state)

    if (state == 'poweredOn'):
        bleno.startAdvertising('Approach', [APPROACH_SERVICE_UUID])
    else:
        bleno.stopAdvertising()

bleno.on('stateChange', onStateChange)

approachCharacteristicGimbal = ApproachCharacteristicGimbal()

def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': APPROACH_SERVICE_UUID,
                'characteristics': [
                    approachCharacteristicGimbal,
                ]
            })
        ])


bleno.on('advertisingStart', onAdvertisingStart)

bleno.start()

while True:
    time.sleep(1)

