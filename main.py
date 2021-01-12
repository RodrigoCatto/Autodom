#conda activate autodom

import bagpy
from bagpy import bagreader
import pandas as pd
from math import sin, cos, pi, tan, radians
import numpy as np
import tkinter as tk
from tkinter import filedialog as fd


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

print(linear_encoder_data)

encoder_type = "" #VESC (erpm), DIGITAL ENCODER (ticks)
wheel_base_dist = 0

number_poles = 2
motor_reduction = 4
wheel_radius = 0.043 #Meters
rpm_to_ms = (2*pi*wheel_radius)/60 #Convert rpm to meters per second
vx = (linear_encoder_data * rpm_to_ms)/ (number_poles * motor_reduction)



'''
#######################################################
# Diff. Odometry:
#######################################################
right_encoder_topic = ""
left_encoder_topic = ""
encoder_type = "" #VESC (erpm), DIGITAL ENCODER (ticks)
wheel_base_dist = 0

ticks_per_rotation = 0
erpm_to_rpm = 0


window = tk.Tk()
greeting = tk.Label(text="Hello, Tkinter")
greeting.pack()
window.mainloop()
'''