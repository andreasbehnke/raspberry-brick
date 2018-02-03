from Adafruit_MotorHAT import Adafruit_MotorHAT

class MotorController:
    direction_mapping = {
        "R": Adafruit_MotorHAT.RELEASE,
        "F": Adafruit_MotorHAT.FORWARD,
        "B": Adafruit_MotorHAT.BACKWARD}

    def __init__(self, num, motor_hat):
        self.motor = motor_hat.getMotor(num)
        self.motor.run(Adafruit_MotorHAT.RELEASE)
        self.motor.setSpeed(0)
        self.direction = Adafruit_MotorHAT.RELEASE
        self.speed = 0

    def update(self, direction, speed):
        if direction != self.direction:
            self.direction = direction
            direction_val = MotorController.direction_mapping.get(direction)
            if not direction_val:
                raise ValueError
            self.motor.run(direction_val)
        if speed != self.speed:
            self.speed = speed
            self.motor.setSpeed(speed)

    def stop(self):
        self.update('R', 0)
