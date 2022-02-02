import pigpio
import time

class ServoDriver:

    def __init__(self, pin):
        self.pi = pigpio.pi()
        self._pin = pin

        self.set_pin_mode()
        self.set_degree(0)

    def set_pin_mode(self):
        self.pi.set_mode(self._pin, pigpio.OUTPUT)

    def set_degree(self, degree):
        if not(0 <= degree <= 180):
            TypeError("Range of degree is 0...180")
        self.current_degree = degree
        value = int(degree / 180.0 * 2000 + 500)
        self.pi.set_servo_pulsewidth(self._pin, value)

    # velocityは角速度を指定
    def set_degree_with_velocity(self, degree, velocity):
        if not(0 <= degree <= 180):
            TypeError("Range of degree is 0...180")

        start_degree = self.current_degree
        # 1度動かす際にかかる秒数を計算
        second_per_degree = 1.0 / float(velocity)

        if(degree - start_degree >= 0):
            for i in range(1, degree - start_degree + 1):
                self.set_degree(start_degree + i)
                time.sleep(second_per_degree)

        elif(degree - start_degree < 0):
            for i in range(-1, degree - start_degree - 1, -1):
                self.set_degree(start_degree + i)
                time.sleep(second_per_degree)

    def clean(self):
        self.pi.set_mode(self._pin, pigpio.INPUT)
        self.pi.stop()


if __name__ == '__main__':

    gpio_pwm = 18

    driver = ServoDriver(gpio_pwm)
    degree_list = [0, 30, 60, 90, 60, 30, 0]
    for degree in degree_list:
        driver.set_degree_with_velocity(degree, 100)
        time.sleep(1)

    driver.clean()
