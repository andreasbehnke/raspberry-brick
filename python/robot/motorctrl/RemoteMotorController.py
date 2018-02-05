class RemoteMotorController:

    def __init__(self, num, remote_motor_hat):
        self.hat = remote_motor_hat
        self.num = num

    def update(self, direction, speed):
        self.hat.directions[self.num] = direction
        self.hat.speeds[self.num] = speed

    def stop(self):
        self.hat.directions[self.num] = 'R'
        self.hat.speeds[self.num] = 0
