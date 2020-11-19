# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 15:27:11 2020

@author: Fernando Garcia (fergarciadlc)
"""


def main():
    # Camera aspects
    sensor_height_mm = 14.9
    sensor_width_mm = 22.3
    sensor_height_px = 4000
    sensor_width_px = 6000

    focal_length = float(input("Focal Length (mm) = "))
    object_height_mm = float(input("real object height (mm) = "))
    object_height_px = float(input("object height (pixels) = "))

    object_height_on_sensor = sensor_height_mm * object_height_px / sensor_height_px
    distance = object_height_mm * focal_length / object_height_on_sensor

    distance_cm = distance / 10
    distance_m = distance / 1000

    print(f"\n{distance} mm \n{distance_cm} cm\n{distance_m} m")


if __name__ == "__main__":
    main()
