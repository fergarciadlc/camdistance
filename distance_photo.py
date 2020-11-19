# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 15:23:37 2020

@author: Fernando Garcia (fergarciadlc)
"""
import cv2
import json

# Constants
PHOTO_PATH = "photos-test/50mm 2m.JPG"
SCALE_FACTOR = 6

# Camera
with open("config.json", "r") as fp:
    data = json.load(fp)
object_height_mm = data["object"]["height_mm"]


class Camera:
    def __init__(self, model, focal_length, sensor_height_mm, sensor_width_mm, sensor_height_px, sensor_width_px):
        self.model = model
        self.focal_length = focal_length
        self.sensor_height_mm = sensor_height_mm
        self.sensor_width_mm = sensor_width_mm
        self.sensor_height_px = sensor_height_px
        self.sensor_width_px = sensor_width_px

    def __str__(self):
        message = \
            f"Camera: {self.model} \n" \
            f"Focal Length =  {self.focal_length} mm\n" \
            f"Sensor = {self.sensor_width_px} x {self.sensor_height_px} px / " \
            f"{self.sensor_width_mm} x {self.sensor_height_mm} mm"
        return message


cam = Camera(
    model=data["camera"]["model"],
    focal_length=data["camera"]["focal_length"],
    sensor_height_mm=data["camera"]["sensor_height_mm"],
    sensor_width_mm=data["camera"]["sensor_width_mm"],
    sensor_height_px=data["camera"]["sensor_height_px"],
    sensor_width_px=data["camera"]["sensor_width_px"]
)
print(cam)
print(f"\nObject height = {object_height_mm / 10:.4f} cm")

# import image
img = cv2.imread(PHOTO_PATH)
img = cv2.resize(img, (int(img.shape[1] / SCALE_FACTOR), int(img.shape[0] / SCALE_FACTOR)))

# Initial points
pt1 = (0, 0)
pt2 = (0, 0)
topLeft_clicked = False
botRight_clicked = False
img_copy_flag = False

global thickness
font = cv2.FONT_HERSHEY_DUPLEX
font_size = 7.5 * 1 / SCALE_FACTOR
text_size = cv2.getTextSize("Distance", font, font_size, 2)[0]
rec1 = (0, int(7 / 9 * img.shape[0]))
rec2 = (int(text_size[0] * 1.3), int(img.shape[0]))


def show_camera_info():
    rec_a = (img.shape[1] - int(text_size[0] * 1.3), int(7 / 9 * img.shape[0]))
    rec_b = (img.shape[1], img.shape[0])
    cv2.rectangle(img, rec_a, rec_b, (255, 255, 255), -1)
    cv2.putText(img, f"{cam.model}",
                (rec_a[0], int(rec_a[1] + text_size[1] * 1) - int(SCALE_FACTOR * 0.625)),
                font,
                font_size * 0.7, (0, 0, 0),
                thickness)
    cv2.putText(img, f"F = {cam.focal_length} mm",
                (rec_a[0], int(rec_a[1] + text_size[1] * 2.5) - int(SCALE_FACTOR * 0.625)),
                font,
                font_size * 0.7, (0, 0, 0),
                thickness)
    cv2.putText(img, f"{cam.sensor_width_px}x{cam.sensor_height_px} px",
                (rec_a[0], int(rec_a[1] + text_size[1] * 3.5) - int(SCALE_FACTOR * 0.625)),
                font,
                font_size * 0.7, (0, 0, 0),
                thickness)
    cv2.putText(img, f"OH = {object_height_mm} mm",
                (rec_a[0], int(rec_a[1] + text_size[1] * 4.5) - int(SCALE_FACTOR * 0.625)),
                font,
                font_size * 0.7, (0, 0, 0),
                thickness)


def calculate_distance(measure_in_px):
    object_height_on_sensor = cam.sensor_height_mm * measure_in_px / cam.sensor_height_px
    distance_from_camera_mm = object_height_mm * cam.focal_length / object_height_on_sensor
    return distance_from_camera_mm


def draw_info():
    global thickness
    cv2.rectangle(img, rec1, rec2, (255, 255, 255), -1)
    if SCALE_FACTOR > 8:
        thickness = 1
    else:
        thickness = 2
    cv2.putText(img, "Distance", (rec1[0], rec1[1] + text_size[1]), font, font_size, (0, 0, 0), thickness)


draw_info()
show_camera_info()
img_copy = img.copy()


# mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global pt1, pt2, topLeft_clicked, botRight_clicked, img_copy_flag

    # clean image
    if event == cv2.EVENT_RBUTTONDOWN:
        img_copy_flag = True
        pt1 = (0, 0)
        pt2 = (0, 0)
        topLeft_clicked = False
        botRight_clicked = False
    else:
        img_copy_flag = False

    # get mouse click
    if event == cv2.EVENT_LBUTTONDOWN:

        if topLeft_clicked and botRight_clicked:
            topLeft_clicked = False
            botRight_clicked = False
            pt1 = (0, 0)
            pt2 = (0, 0)

        if not topLeft_clicked:
            pt1 = (x, y)
            topLeft_clicked = True
            img_copy_flag = True

        elif not botRight_clicked:
            pt2 = (x, y)
            botRight_clicked = True
            img_copy_flag = False


# Set windows and callback functions
cv2.namedWindow(winname=PHOTO_PATH)
cv2.setMouseCallback(PHOTO_PATH, draw_rectangle)

while True:
    if topLeft_clicked:
        cv2.circle(img, center=pt1, radius=4, color=(0, 0, 255), thickness=-1)

    # drawing rectangle
    if topLeft_clicked and botRight_clicked:
        measure_px = abs(pt1[1] - pt2[1]) * SCALE_FACTOR
        cv2.rectangle(img, pt1, pt2, (0, 0, 255), 2)
        draw_info()
        distance = calculate_distance(measure_px)
        cv2.putText(img, f"{measure_px} px",
                    (rec1[0], rec1[1] + int(text_size[1] * 2.5) - int(SCALE_FACTOR * 0.625)),
                    font,
                    font_size * 0.8, (0, 0, 0),
                    thickness)
        cv2.putText(img, f"{distance / 10:.4f} cm",
                    (rec1[0], rec1[1] + int(text_size[1] * 3.75) - int(SCALE_FACTOR * 0.625)),
                    font,
                    font_size * 0.8, (0, 0, 0),
                    thickness)
        cv2.putText(img, f"{distance / 1000:.4f} m",
                    (rec1[0], rec1[1] + int(text_size[1] * 4.75) - int(SCALE_FACTOR * 0.625)),
                    font,
                    font_size * 0.8, (0, 0, 0),
                    thickness)

    if cv2.waitKey(20) & 0xFF == 27:  # ESC key to quit
        break

    if img_copy_flag:
        img = img_copy.copy()
        cv2.imshow(PHOTO_PATH, img)

    cv2.imshow(PHOTO_PATH, img)  # Name of actual window

cv2.destroyAllWindows()
