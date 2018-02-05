import cv2
import argparse
from motorctrl.RemoteMotorController import RemoteMotorController
from motorctrl.RemoteMotorHat import RemoteMotorHat
from motorctrl.LegoServoMotor import LegoServoMotor
from motorctrl.LegoMotorL import LegoMotorL


windows_original = "Original"
camera_width = 640
camera_height = 480
tilt_area = 70
tilt_wait = 3
pan_area = 0.1
pan_motor_factor = 130


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

    # initialize motors
    hat = RemoteMotorHat(host, port)
    hat.start()
    tilt_servo = LegoServoMotor(RemoteMotorController(2, hat))
    tilt_servo.left(1)
    tilt = 1
    tilt_wait_count = 0
    left_motor = LegoMotorL(RemoteMotorController(0, hat))
    right_motor = LegoMotorL(RemoteMotorController(1, hat))

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

            if tilt_wait_count > 0:
                tilt_wait_count = tilt_wait_count - 1

            # tilt control
            if y < tilt_area and tilt > -7 and tilt_wait_count == 0:
                tilt = tilt - 1
                tilt_wait_count = tilt_wait
            elif y > camera_height - tilt_area and tilt < 7 and tilt_wait_count == 0:
                tilt = tilt + 1
                tilt_wait_count = tilt_wait

            # pan control
            # normalize x value of center to range -1 ... 0 ... 1
            x_rel = 2 * x / camera_width - 1
            pan_motor = 0
            if abs(x_rel) > pan_area:
                pan_motor = x_rel * pan_motor_factor
            pan_motor_value = int(abs(pan_motor))

            # change motor values
            if tilt < 0:
                tilt_servo.right(abs(tilt))
            else:
                tilt_servo.left(tilt)
            if pan_motor == 0:
                left_motor.update('R', 0)
                right_motor.update('R', 0)
            elif pan_motor > 0:
                # turn right
                left_motor.update('F', pan_motor_value)
                right_motor.update('B', pan_motor_value)
            elif pan_motor < 0:
                # turn left
                left_motor.update('B', pan_motor_value)
                right_motor.update('F', pan_motor_value)
        else:
            left_motor.update('R', 0)
            right_motor.update('R', 0)

        cv2.imshow(windows_original, image)
        if cv2.waitKey(1) & 0xFF is ord('q'):
            break


if __name__ == '__main__':
    main()
