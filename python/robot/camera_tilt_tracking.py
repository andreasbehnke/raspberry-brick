import cv2
import argparse
from RemoteMotorController import RemoteMotorController
from RemoteMotorHat import RemoteMotorHat
from LegoServoMotor import LegoServoMotor


windows_original = "Original"
camera_width = 640
camera_height = 480
tilt_area = 50
tilt_wait = 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--stream', required=True, help='URL of webcam to use, or nothing to use /dev/video0')
    ap.add_argument("--host", type=str, help="servers host name or ip, default is localhost")
    ap.add_argument("--port", type=int, help="servers port, default is 5005")
    args = vars(ap.parse_args())

    host = args["host"]
    if not host:
        host = "localhost"
    port = args["port"]
    if not port:
        port = 5005

    camera = cv2.VideoCapture(args['stream'])

    with open("hsv_values.lst", "r") as hsv_file:
        row = hsv_file.readline().split(",")
        v1_min = int(row[0])
        v2_min = int(row[1])
        v3_min = int(row[2])
        v1_max = int(row[3])
        v2_max = int(row[4])
        v3_max = int(row[5])

    hat = RemoteMotorHat(host, port)
    hat.start()
    tilt_servo = LegoServoMotor(RemoteMotorController(2, hat))
    tilt_servo.left(1)
    tilt = 1
    tilt_wait_count = 0

    while True:
        ret, image = camera.read()

        if not ret:
            break

        frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(frame, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)

            print("x:%.0f" % x, "y:%.0f" % y, "r:%.0f" % radius)

        cv2.imshow(windows_original, image)

        if tilt_wait_count > 0:
            tilt_wait_count = tilt_wait_count - 1

        # tilt control

        if y < tilt_area and tilt > 0 and tilt_wait_count == 0:
            tilt = tilt - 1
            tilt_wait_count = tilt_wait
        elif y > camera_height - tilt_area and tilt < 7 and tilt_wait_count == 0:
            tilt = tilt + 1
            tilt_wait_count = tilt_wait
        tilt_servo.left(tilt)

        if cv2.waitKey(1) & 0xFF is ord('q'):
            break


if __name__ == '__main__':
    main()
