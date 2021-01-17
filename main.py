#conda activate autodom

import bagpy
from bagpy import bagreader
import pandas as pd
from math import sin, cos, pi, tan, radians
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog as fd

def generate_semicircle(center_x, center_y, radius, stepsize=0.1):

    theta = np.linspace(0, np.pi, 30)

    x = np.cos(theta)
    y = np.sin(theta)

    x *= radius
    y *= radius

    return y+center_x,  x + center_y
#######################################################
# Open Bag file
#######################################################
#filename = fd.askopenfilename()
bag = bagreader('akermann.bag')
#print(bag.topic_table["Topics"])


#######################################################
# Ackermann Odometry:
#######################################################
linear_encoder_topic = "/commands/motor/speed"
angular_encoder_topic = "/commands/servo/position"

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


encoder_type = "" #VESC (erpm), DIGITAL ENCODER (ticks)
wheelbase = 0.274
UMBmark_lenght = 3
number_poles = 2
motor_reduction = 4
wheel_radius = 0.043 #Meters
rpm_to_ms = (2*pi*wheel_radius)/60 #Convert rpm to meters per second
speed_rpm = (linear_encoder_data * rpm_to_ms)/ (number_poles * motor_reduction)



#speed_rpm_val = linear_encoder_data*120*rpm_to_ms/1000

servo_angle_rad = np.radians(54.0 * angular_encoder_data - 27.25)  # rads

x = 0
y = 0
th = 0

pos_x = []
pos_y = []
pos_th = []

slider_in = 0.0
slider_out = 0.3

start = int(len(speed_rpm)*slider_in)
stop = int(len(speed_rpm)*slider_out)

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

#'''
root= tk.Tk()

l = tk.Label(root, bg='white', fg='black', width=20, text='empty')
l.pack()

def print_selection(v):
    l.config(text='you have selected ' + v)


s = tk.Scale(root, label='End Point in %', from_=0, to=100, orient=tk.HORIZONTAL, length=200, showvalue=0, tickinterval=10,
             resolution=5, command=print_selection)
s.pack()

# Generate real path
semi_circle_right_x, semi_circle_right_y = generate_semicircle(0, UMBmark_lenght/2, UMBmark_lenght/2, stepsize=0.01)
semi_circle_left_x, semi_circle_left_y = generate_semicircle(-UMBmark_lenght, UMBmark_lenght/2, -UMBmark_lenght/2, stepsize=0.01)
top_line_x, top_line_y = [0, -UMBmark_lenght], [0, 0] # Top line
bottom_line_x, bottom_line_y = [0, -UMBmark_lenght], [UMBmark_lenght, UMBmark_lenght] # Bottom line

figure = plt.Figure(figsize=(6,5), dpi=100)
ax = figure.add_subplot(111)
chart_type = FigureCanvasTkAgg(figure, root)
chart_type.get_tk_widget().pack()
ax.plot(semi_circle_right_x, semi_circle_right_y,semi_circle_left_x, semi_circle_left_y, top_line_x, top_line_y, bottom_line_x, bottom_line_y)
ax.scatter(pos_x, pos_y)
ax.set_title('Robot Position in X and Y')
ax.set_ylabel('Y [Meters]')
ax.set_xlabel('X [Meters]')


root.mainloop()
#'''