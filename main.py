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
    """
    generates coordinates for a semicircle, centered at center_x, center_y
    """

    x = np.arange(center_x, center_x+radius+stepsize, stepsize)
    y = np.sqrt(radius**2 - x**2)

    # since each x value has two corresponding y-values, duplicate x-axis.
    # [::-1] is required to have the correct order of elements for plt.plot.
    x = np.concatenate([x,x[::-1]])

    # concatenate y and flipped y.
    y = np.concatenate([y,-y[::-1]])

    return x, y + center_y

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

generate_semicircle(0, UMBmark_lenght, UMBmark_lenght/2, stepsize=0.1)
generate_semicircle(-UMBmark_lenght, UMBmark_lenght, UMBmark_lenght/2, stepsize=0.1)

figure = plt.Figure(figsize=(6,5), dpi=100)
ax = figure.add_subplot(111)
chart_type = FigureCanvasTkAgg(figure, root)
chart_type.get_tk_widget().pack()
ax.scatter(pos_x, pos_y)
ax.set_title('Robot Position in X and Y')
ax.set_ylabel('Y [Meters]')
ax.set_xlabel('X [Meters]')



root.mainloop()
#'''