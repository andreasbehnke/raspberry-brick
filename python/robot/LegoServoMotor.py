"""
Represents a lego servo motor 88004 and allows remote and
local control using MotorController or RemoteMotorController
"""


class LegoServoMotor:
    offset = 28

    def __init__(self, motor_controller):
        self.motor_controller = motor_controller
        motor_controller.stop()

    '''
    turn servo n steps left with step in range [0,7] 
    '''
    def left(self, step):
        self.motor_controller.update('F', step * 32 + LegoServoMotor.offset)

    '''
    turn servo n steps right with step in range [0,7] 
    '''
    def right(self, step):
        self.motor_controller.update('B', step * 32 + LegoServoMotor.offset)
