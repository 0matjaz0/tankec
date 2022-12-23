import RPi.GPIO as GPIO
import time


class DCMotor:
    def __init__(self, pwm_pin, hbridge_sw1_pin, hbridge_sw2_pin):
        self.pwm_pin = pwm_pin
        self.s1_pin = hbridge_sw1_pin
        self.s2_pin = hbridge_sw2_pin
        self.PWM_FREQ = 100
        self.pwm_duty = 0
        GPIO.setmode(GPIO.BCM)  # choose SOC numbering scheme
        GPIO.setup(self.s1_pin, GPIO.OUT)
        GPIO.setup(self.s2_pin, GPIO.OUT)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwm_pin, self.PWM_FREQ)

    def start(self):
        self.pwm.start(self.pwm_duty)

    def stop(self):
        self.pwm.stop()

    def set_speed(self, speed):
        """ set speed to integer in [-100:100], negative means backward"""
        self.pwm_duty = speed
        if speed > 0:  # go forward
            self.s1_state = True
            self.s2_state = False
        else  # go backward
            self.s1_state = False
            self.s2_state = True
        self.pwm.ChangeDutyCycle(self.pwm_duty)


motor_left = DCMotor(pwm_pin=22, hbridge_sw1_pin=25, hbridge_sw2_pin=8)
motor_right = DCMotor(pwm_pin=10, hbridge_sw1_pin=23, hbridge_sw2_pin=24)

motor_left.start()
motor_left.set_speed(20)
time.sleep(2)  # let it run 2 seconds
motor_left.stop()

time.sleep(2)  # quiet 2 seconds

motor_left.start()  # see if it remembered pwm duty cycle from last run
time.sleep(2)  # let it run 2 seconds
motor_left.stop()


GPIO.cleanup()

# todo: implement direction setting
# GPIO.output(25, True)
# GPIO.output(8, False)
# GPIO.output(23, True)
# GPIO.output(24, False)

