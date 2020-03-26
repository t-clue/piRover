import pigpio
import time

gpio_pwma = 12
gpio_ain1 = 7
gpio_ain2 = 1
gpio_stanby = 8

pi = pigpio.pi()
pi.set_mode(gpio_pwma, pigpio.OUTPUT)
pi.set_mode(gpio_ain1, pigpio.OUTPUT)
pi.set_mode(gpio_ain2, pigpio.OUTPUT)
pi.set_mode(gpio_stanby, pigpio.OUTPUT)

pi.write(gpio_stanby, 1)
pi.write(gpio_ain1, 0)
pi.write(gpio_ain2, 1)

pi.hardware_PWM(gpio_pin0, 2, 500000)

time.sleep(5)

pi.set_mode(gpio_pwma, pigpio.INPUT)
pi.set_mode(gpio_ain1, pigpio.INPUT)
pi.set_mode(gpio_ain2, pigpio.INPUT)
pi.set_mode(gpio_stanby, pigpio.INPUT)
pi.stop()