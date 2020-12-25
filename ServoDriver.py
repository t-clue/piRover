import pigpio
import time

class ServoDriver:

    def __init__(self, pin):
        self.pi = pigpio.pi()
        self._pin = pin

        self.set_pin_mode()

    def set_pin_mode(self):
        self.pi.set_mode(self._pin, pigpio.OUTPUT)

    def set_degree(self, degree):
        if not(0 <= degree <= 180):
            TypeError("Range of degree is 0...180")
        value = int((degree - 90) / 90 * 990 + 1500)
        self.pi.set_servo_pulsewidth(self._pin, value)

    def clean(self):
        self.pi.set_mode(self._pin, pigpio.INPUT)
        self.pi.stop()


if __name__ == '__main__':

    gpio_pwm = 17

    driver = ServoDriver(gpio_pwm)
    degree_list = [0, 60, 90, 120, 180]
    for degree in degree_list:
        driver.set_degree(degree)
        time.sleep(1)

    driver.clean()
