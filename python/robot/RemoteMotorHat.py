import socket
import time
import thread


class RemoteMotorHat:

    def __init__(self, host="localhost", port=5005, delay=100):
        self.host = host
        self.port = port
        self.delay = delay
        self.speeds = [0, 0, 0, 0]
        self.directions = ['R', 'R', 'R', 'R']
        self.running = True

    def start(self):
        self.running = True
        thread.start_new_thread(self.run, ())

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        while self.running:
            command = ''
            for m in range(4):
                if m > 0:
                    command += ','
                command += self.directions[m] + ':' + str(self.speeds[m])
            start = time.time()
            s.sendall(command)
            result = s.recv(1024)
            end = time.time()
            duration = (end - start) * 1000
            print(result + " " + str(duration) + "ms " + command)
            if result != 'OK':
                break
            time.sleep(self.delay / 1000)

    def stop(self):
        self.running = False
