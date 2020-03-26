import pigpio
import time

class MotorDriver:

    def __init__(self, in1, in2, pwm):
        self._power_percentage = int(0)
        self._direction = True  #True -> cw, False -> ccw
        self.pi = pigpio.pi()

        self._IN1 = in1
        self._IN2 = in2
        self._PWM = pwm

        self.set_pin_mode()
        self._set_pin_state()

    def set_pin_mode(self):
        self.pi.set_mode(self._IN1, pigpio.OUTPUT)
        self.pi.set_mode(self._IN2, pigpio.OUTPUT)
        self.pi.set_mode(self._PWM, pigpio.OUTPUT)

    def set_direction(self, is_cw):
        if type(is_cw) is not bool:
            TypeError("Type of is_cw is bool")
        self._direction = is_cw
        self._set_pin_state()

    def set_accel(self, percentage):
        if type(percentage) is not int:
            TypeError("Type of percentage is bool")
        if percentage < 0 or 100 <= percentage:
            TypeError("Range of percentage is 0...100")
        value = int(percentage * 10 ** 4)
        self.pi.hardware_PWM(self._PWM, 50, value)

    def clean(self):
        self.pi.set_mode(self._IN1, pigpio.INPUT)
        self.pi.set_mode(self._IN2, pigpio.INPUT)
        self.pi.set_mode(self._PWM, pigpio.INPUT)

    def _set_pin_state(self):
        self.pi.write(self._IN1, self._in1_value())
        self.pi.write(self._IN2, self._in2_value())

    def _in1_value(self):
        if self._direction:
            return 1
        else:
            return 0

    def _in2_value(self):
        if self._direction:
            return 0
        else:
            return 1


if __name__ == '__main__':

    gpio_pwma = 12
    gpio_ain1 = 7
    gpio_ain2 = 26

    gpio_pwmb = 13
    gpio_bin1 = 5
    gpio_bin2 = 6

    gpio_stanby = 8

    pi = pigpio.pi()
    pi.set_mode(gpio_stanby, pigpio.OUTPUT)

    driver_a = MotorDriver(gpio_ain1, gpio_ain2, gpio_pwma)
    driver_b = MotorDriver(gpio_bin1, gpio_bin2, gpio_pwmb)
    accel_list = [10, 40, 59, 99]
    for accle in accel_list:
        driver_a.set_accel(accle)
        driver_b.set_accel(accle)
        time.sleep(1)

    driver_a.set_direction(False)
    driver_b.set_direction(False)
    for accle in accel_list:
        driver_a.set_accel(accle)
        driver_b.set_accel(accle)
        time.sleep(1)

    driver_a.clean()
    driver_b.clean()

    pi = pigpio.pi()
    pi.set_mode(gpio_pwma, pigpio.OUTPUT)
    pi.set_mode(gpio_ain1, pigpio.OUTPUT)
    pi.set_mode(gpio_ain2, pigpio.OUTPUT)

    pi.set_mode(gpio_pwmb, pigpio.OUTPUT)
    pi.set_mode(gpio_bin1, pigpio.OUTPUT)
    pi.set_mode(gpio_bin2, pigpio.OUTPUT)

    pi.set_mode(gpio_stanby, pigpio.OUTPUT)

    pi.write(gpio_stanby, 1)
    pi.write(gpio_ain1, 0)
    pi.write(gpio_ain2, 1)

    pi.write(gpio_bin1, 0)
    pi.write(gpio_bin2, 1)

    duty_list = [100000, 300000, 500000, 800000] 
    for duty in duty_list:
        pi.hardware_PWM(gpio_pwma, 50, duty)
        pi.hardware_PWM(gpio_pwmb, 50, duty)
        time.sleep(1)	

    pi.set_mode(gpio_pwma, pigpio.INPUT)
    pi.set_mode(gpio_ain1, pigpio.INPUT)
    pi.set_mode(gpio_ain2, pigpio.INPUT)

    pi.set_mode(gpio_pwmb, pigpio.INPUT)
    pi.set_mode(gpio_bin1, pigpio.INPUT)
    pi.set_mode(gpio_bin2, pigpio.INPUT)

    pi.set_mode(gpio_stanby, pigpio.INPUT)
    pi.stop()
