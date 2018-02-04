import cv2
import argparse


window_color_range_adjustment = "Color Range Adjustment"
windows_original = "Original"

def callback(value):
    pass


def setup_trackbars():
    cv2.namedWindow(window_color_range_adjustment, 0)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in "HSV":
            cv2.createTrackbar("%s_%s" % (j, i), window_color_range_adjustment, v, 255, callback)


def get_trackbar_values():
    values = []

    for i in ["MIN", "MAX"]:
        for j in "HSV":
            v = cv2.getTrackbarPos("%s_%s" % (j, i), window_color_range_adjustment)
            values.append(v)

    return values


def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--stream', required=False, help='URL of webcam to use, or nothing to use /dev/video0')
    args = vars(ap.parse_args())
    return args


def main():
    args = get_arguments()

    if args['stream']:
        camera = cv2.VideoCapture(args['stream'])
    else:
        camera = cv2.VideoCapture(0)

    setup_trackbars()

    while True:
        ret, image = camera.read()

        if not ret:
            break

        frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values()

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

        preview = cv2.bitwise_and(image, image, mask=mask)
        cv2.imshow(window_color_range_adjustment, preview)
        cv2.imshow(windows_original, image)

        if cv2.waitKey(1) & 0xFF is ord('q'):
            with open("hsv_values.lst", "w") as hsv_file:
                hsv_file.write("%s,%s,%s,%s,%s,%s" % (v1_min, v2_min, v3_min, v1_max, v2_max, v3_max))
            break


if __name__ == '__main__':
    main()
