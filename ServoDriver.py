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
        degree = (degree / 180 * 1.9 + 0.5) / 20 * 100 # servo data sheet https://akizukidenshi.com/download/ds/towerpro/SG90_a.pdf
        value = int(degree * 10 ** 4)
        self.pi.hardware_PWM(self._pin, 50, value)

    def clean(self):
        self.pi.set_mode(self._pin, pigpio.INPUT)
        self.pi.stop()


if __name__ == '__main__':

    gpio_pwm = 19

    driver = ServoDriver(gpio_pwm)
    degree_list = [0, 60, 90, 120, 180]
    for degree in degree_list:
        driver.set_degree(degree)
        time.sleep(1)

    driver.clean()
