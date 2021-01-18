import pandas as pd
from math import sin, cos, pi, tan, radians
import numpy as np

#######################################################
# Helper Functions
#######################################################
def generate_semicircle(center_x, center_y, radius):

    theta = np.linspace(0, np.pi, 30)

    x = np.cos(theta)
    y = np.sin(theta)

    x *= radius
    y *= radius

    return y+center_x,  x + center_y


#######################################################
# Ackermann Odometry:
#######################################################
def read_akermann_topics(bag, motor_topic, servo_topic, wheel_radius, motor_reduction, number_poles):
    if not bag:
        print("Bag file invalid or not selected")
        return 0

    # Get both topic names
    linear_encoder_topic = motor_topic
    angular_encoder_topic = servo_topic

    # Convert values from bag to numpy array
    linear_encoder_data = bag.message_by_topic(linear_encoder_topic)
    linear_encoder_data = pd.read_csv(linear_encoder_data)
    linear_encoder_data = linear_encoder_data["data"].to_numpy()

    angular_encoder_data = bag.message_by_topic(angular_encoder_topic)
    angular_encoder_data = pd.read_csv(angular_encoder_data)
    angular_encoder_data = angular_encoder_data["data"].to_numpy()

    timestamps = bag.message_by_topic(linear_encoder_topic)
    timestamps = pd.read_csv(timestamps)
    timestamps = timestamps["Time"].to_numpy()

    rpm_to_ms = (2 * pi * wheel_radius) / 60  # Convert rpm to meters per second
    speed_rpm = (linear_encoder_data * rpm_to_ms) / (number_poles * motor_reduction)
    servo_angle_rad = np.radians(54.0 * angular_encoder_data - 27.25)  # rads

    return speed_rpm, servo_angle_rad, timestamps


#######################################################
# Calculate Odometry:
#######################################################
def odometry(slider_in, slider_out, speed_rpm, servo_angle_rad, timestamps, wheelbase):
    x = 0
    y = 0
    th = 0

    pos_x = []
    pos_y = []
    pos_th = []
    diff_th = []
    possible_curve_points_x = []
    possible_curve_points_y = []

    start = int(len(speed_rpm)*slider_in)
    stop = int(len(speed_rpm)*slider_out)

    counting = False

    for i in range(start,stop):
        vx = speed_rpm[i]
        vy = 0
        servo_angle = servo_angle_rad[i]
        vth = vx * tan(servo_angle) / wheelbase #rad/s

        if i > 1:
            current_time = timestamps[i-1]
            last_time = timestamps[i]

            dt = (current_time - last_time)
            delta_x = (vx * cos(th) - vy * sin(th)) * dt
            delta_y = (vx * sin(th) + vy * cos(th)) * dt
            delta_th = vth * dt

            x += delta_x
            y += delta_y
            th += delta_th

            pos_x.append(x)
            pos_y.append(y)
            pos_th.append(th)

            diff_th.append(vth)

            if vth > 0.3:
                if not counting:
                    possible_curve_points_x.append(x)
                    possible_curve_points_y.append(y)
                    counting = True
            if vth <= 0.3:
                counting = False
    return pos_x, pos_y, possible_curve_points_x, possible_curve_points_y