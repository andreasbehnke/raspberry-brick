import argparse
import socket
#from Adafruit_MotorHAT import Adafruit_MotorHAT
import MotorController

class MotorHatServer:

    def __init__(self, host="localhost", port=5005, timeout=1):
        self.host = host
        self.port = port
        self.timeout = timeout
        motor_hat = Adafruit_MotorHAT(addr=0x60)
        self.controllers = []
        for m in range(1, 4):
            self.controllers.append(MotorController(m, motor_hat))

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
            except socket.error:
                print("WARN " + client_host + ": socket error")
            finally:
                conn.close()
                for motor_controller in self.controllers:
                    motor_controller.stop()
            print("INFO " + client_host + ": disconnected")

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run socket server for listening to moter hat events')
    parser.add_argument("--host", type=str, help="host name or ip to listen to, default is localhost")
    parser.add_argument("--port", type=int, help="port to listen to, default is 5005")
    parser.add_argument("--timeout", type=int, help="client connection timeout, default is 1 second")
    args = parser.parse_args();
    host = args.host
    if not host:
        host = "localhost"
    port = args.port
    if not port:
        port = 5005
    timeout = args.timeout
    if not timeout:
        timeout = 1
    server = MotorHatServer(host, port, timeout)
    server.run()
