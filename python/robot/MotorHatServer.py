import socket
from Adafruit_MotorHAT import Adafruit_MotorHAT


class MotorController:

    def __init__(self, num, motor_hat):
        self.motor = motor_hat.getMotor(num)
        self.motor.run(Adafruit_MotorHAT.RELEASE)
        self.motor.setSpeed(0)
        self.direction = Adafruit_MotorHAT.RELEASE
        self.speed = 0

    def update(self, direction, speed):
        if direction != self.direction:
            self.direction = direction
            self.motor.run(direction)
        if speed != self.speed:
            self.speed = speed
            self.motor.setSpeed(speed)


class MotorHatServer:

    def __init__(self, host = "localhost", port = 5005, timeout = 1):
        self.host = host
        self.port = port
        self.timeout = timeout
        motor_hat = Adafruit_MotorHAT(addr=0x60)
        self.controllers = []
        for m in range(0, 4):
            self.controllers.append(MotorController(m, motor_hat))
        self.direction_mapping = {
            "R" : Adafruit_MotorHAT.RELEASE,
            "F" : Adafruit_MotorHAT.FORWARD,
            "B" : Adafruit_MotorHAT.BACKWARD}

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(1)

        while 1:
            print("INFO waiting for connection")
            conn, address = s.accept()
            client_host = address[0]
            conn.settimeout(self.timeout)
            print("INFO " + client_host + ": connected")
            try:
                while 1:
                    data = conn.recv(1024)
                    if not data:
                        break;
                    print("INFO " + client_host + ": received data: " + str(data))
                    conn.sendall(self.dispatch(str(data), client_host))
            except socket.timeout:
                print("WARN " + client_host + ": connection timed out")
            finally:
                conn.close()
            print("INFO " + client_host + ": disconnected")

    def dispatch(self, data, client_host):
        motor_settings = data.split(",")
        if len(motor_settings) != 4:
            print("ERROR " + client_host + ": client sends wrong number of motor settings, must be 4")
            return "ERROR"
        index = 0
        for motor_setting in motor_settings:
            values = motor_setting.split(":")
            if len(values) != 2:
                print("ERROR " + client_host + ": client sends wrong motor settings format, must be [direction]:[speed]")
                return "ERROR"
            try:
                direction = values[0]
                speed = int(values[1])
                self.controllers[index].update(self.direction_mapping.get(direction), speed)
            except ValueError:
                print("ERROR " + client_host + ": speed value could not be parsed to int")
                return "ERROR"
        return "OK"


if __name__ == "__main__":
    server = MotorHatServer()
    server.run()
