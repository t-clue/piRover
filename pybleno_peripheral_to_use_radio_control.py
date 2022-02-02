from pybleno import *
from MotorDriver import *
from ServoDriver import *

bleno = Bleno()

APPROACH_SERVICE_UUID = '5DBD7BF8-0539-4CA0-9534-8738123D9DBC'
APPROACH_CHARACTERISTIC_LEFT_UUID = '18A19BD2-C200-4761-BE91-95A48CC30B6A'
APPROACH_CHARACTERISTIC_RIGHT_UUID = '1849B1F6-A1A3-47F0-BEF2-5EEA1FF18640'
APPROACH_CHARACTERISTIC_GIMBAL_UUID = '572E7DBE-308F-11EB-ADC1-0242AC120002'

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
    def __init__(self, velocity):
        super().__init__(APPROACH_CHARACTERISTIC_GIMBAL_UUID, "ApproachCharacteristicGimbal")

        gpio_pin = 18
        self.driver = ServoDriver(gpio_pin)
        self.velocity = velocity

    def didGetData(self, data):
        print("data: " + str(int(data)))
        self.driver.set_degree_with_velocity(int(data), self.velocity)

def onStateChange(state):
    print('on -> stateChange: ' + state)

    if (state == 'poweredOn'):
        bleno.startAdvertising('Approach', [APPROACH_SERVICE_UUID])
    else:
        bleno.stopAdvertising()

bleno.on('stateChange', onStateChange)

approachCharacteristicGimbal = ApproachCharacteristicGimbal(100)

def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': APPROACH_CHARACTERISTIC_GIMBAL_UUID,
                'characteristics': [
                    approachCharacteristicGimbal,
                ]
            })
        ])


bleno.on('advertisingStart', onAdvertisingStart)

bleno.start()

while True:
    time.sleep(1)

