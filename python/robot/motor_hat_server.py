import argparse
from motorctrl.MotorHatServer import MotorHatServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run socket server for listening to moter hat events')
    parser.add_argument("--host", type=str, help="host name or ip to listen to, default is localhost")
    parser.add_argument("--port", type=int, help="port to listen to, default is 5005")
    parser.add_argument("--timeout", type=int, help="client connection timeout, default is 1 second")
    args = parser.parse_args()
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
