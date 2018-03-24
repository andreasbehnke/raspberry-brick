
import socket
import sys
from Adafruit_MotorHAT import Adafruit_MotorHAT
from MotorController import MotorController


class MotorHatService:

    def __init__(self, host="localhost", port=5005, timeout=1):
        self.host = host
        self.port = port
        self.timeout = timeout
        motor_hat = Adafruit_MotorHAT(addr=0x60)
        self.controllers = []
        for m in range(1, 4):
            self.controllers.append(MotorController(m, motor_hat))

    def run(self):
        print("INFO starting motorhat service @" + self.host + ":" + str(self.port))
        sys.stdout.flush()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(1)

        while 1:
            print("INFO waiting for connection")
            sys.stdout.flush()
            conn, address = s.accept()
            client_host = address[0]
            conn.settimeout(self.timeout)
            print("INFO " + client_host + ": connected")
            sys.stdout.flush()
            try:
                while 1:
                    data = conn.recv(1024)
                    if not data:
                        break;
                    conn.sendall(self.dispatch(str(data), client_host))
            except socket.timeout:
                print("WARN " + client_host + ": connection timed out")
            except socket.error:
                print("WARN " + client_host + ": socket error")
            finally:
                conn.close()
                for motor_controller in self.controllers:
                    motor_controller.stop()
            print("INFO " + client_host + ": disconnected")
            sys.stdout.flush()

    def dispatch(self, data, client_host):
        motor_settings = data.split(",")
        if len(motor_settings) != 4:
            print("ERROR " + client_host + ": client sends wrong number of motor settings, must be 4")
            return "ERROR"
        for index in range(0, 3):
            motor_setting = motor_settings[index]
            values = motor_setting.split(":")
            if len(values) != 2:
                print("ERROR " + client_host + ": client sends wrong motor settings format, must be [direction]:[speed]")
                return "ERROR"
            try:
                direction = values[0]
                speed = int(values[1])
                self.controllers[index].update(direction, speed)
            except ValueError:
                print("ERROR " + client_host + ": client send invalid speed value or direction value [R|F|B]")
                return "ERROR"
        return "OK"
