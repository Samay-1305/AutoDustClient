from time import sleep
import RPi.GPIO as GPIO
from datetime.datetime import now as current_time

class Control:
    def __init__(self):
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BOARD)
        self.motor_interface_pins = [3, 5] #Motor Interface Pins
        self.distance_control_pins = [8, 10] #Trig, Echo
        self.distance_headroom = 2
        self.GPIO.setup(self.motor_interface_pins[0], GPIO.OUT)
        self.GPIO.setup(self.motor_interface_pins[1], GPIO.OUT)
        self.GPIO.setup(self.distance_control_pins[0], GPIO.OUT)
        self.GPIO.setup(self.distance_control_pins[1], GPIO.IN)
        self.distance_threshhold = self.distance() - self.distance_headroom

    def rotate(self, val):
        try:
            pin = self.pins[int(val)]
            self.GPIO.output(pin, GPIO.HIGH)
            sleep(5)
            self.GPIO.output(pin, GPIO.LOW)
            sleep(0.5)
            self.distance_threshhold = self.distance() - self.distance_headroom
            return True
        except Exception as MotorError:
            print("{}: {}".format(current_time().strftime("%d-%m-%Y %H:%M:%S"), MotorError))
            return False

    def listen_for_change(self):
        listening = True
        while listening:
            cur_distance = self.distance()
            if cur_distance < self.distance_threshhold:
                listening = False
        return True

    def distance(self):
        self.GPIO.output(self.distance_control_pins[0], True)
        sleep(0.00001)
        self.GPIO.output(self.distance_control_pins[0], False)
    
        start_time = cur()
        stop_time = cur()
    
        while self.GPIO.input(self.distance_control_pins[1]) == 0:
            start_time = current_time()
    
        while self.GPIO.input(self.distance_control_pins[1]) == 1:
            stop_time = current_time()
    
        time_taken = stop_time - start_time
        distance = (time_taken * 34300) / 2
    
        return distance

    def release(self):
        self.GPIO.cleanup()
