import socket
import time
import argparse

'''
This is a client sending commands to MotorHatServer.
Provide a file containing a list of commands:

F:0,B:0,R:0,R:0
F:10,B:10,R:0,R:0
F:20,B:20,R:0,R:0
F:30,B:30,R:0,R:0
F:40,B:40,R:0,R:0
F:50,B:50,R:0,R:0
F:60,B:60,R:0,R:0
F:70,B:70,R:0,R:0
...

'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is a client sending commands to MotorHatServer.')
    parser.add_argument("--host", type=str, help="servers host name or ip, default is localhost")
    parser.add_argument("--port", type=int, help="servers port, default is 5005")
    parser.add_argument("--repeat", type=int, help="number of times on command should be repeated, default is 100")
    parser.add_argument("commands", type=str, help="name of file containing commands")
    args = parser.parse_args();
    host = args.host
    if not host:
        host = "localhost"
    port = args.port
    if not port:
        port = 5005
    repeat = args.repeat
    if not repeat:
        repeat = 100
    commands = args.commands

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    with open(commands) as commandFile:
        command = commandFile.readline()
        while command:
            for i in range(0, repeat):
                start = time.time()
                s.sendall(command)
                result = s.recv(1024)
                end = time.time()
                duration = (end - start) * 1000
                print(result + " " + str(duration) + "ms " + command)
            command = commandFile.readline()
    s.close()

