#conda activate autodom

from bagpy import bagreader
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
from helper_functions import generate_semicircle, read_akermann_topics, odometry
from math import atan2, pi, sin

#######################################################
# Open Bag file
#######################################################
#filename = fd.askopenfilename()
bag = bagreader('akermann.bag')
#print(bag.topic_table["Topics"])

motor_topic = "/commands/motor/speed"
servo_topic = "/commands/servo/position"



#######################################################
# Input Params for Ackermann:
#######################################################
encoder_type = "" #VESC (erpm), DIGITAL ENCODER (ticks)
wheelbase = 0.274
UMBmark_length = 3
number_poles = 2
motor_reduction = 4
wheel_radius = 0.043 #Meters

slider_in = 0.0
slider_out = 0.3

speed_rpm, servo_angle_rad, timestamps, length = read_akermann_topics(bag, motor_topic, servo_topic, wheel_radius, motor_reduction, number_poles)
pos_x, pos_y, possible_curve_points_x, possible_curve_points_y, diff_th = odometry(slider_in, slider_out, speed_rpm, servo_angle_rad, timestamps, wheelbase)

start = int(len(speed_rpm) * slider_in)
stop = int(len(speed_rpm) * slider_out)
plt.plot(timestamps[start:stop-2], diff_th)
plt.show()

alpha = atan2(possible_curve_points_y[1]-1.5, possible_curve_points_x[1]-(-3))
nominal_wheelbase = wheelbase*pi - wheelbase*alpha/ pi

beta = atan2(possible_curve_points_y[0], possible_curve_points_x[0])
R = 1.5/sin(beta)
drl = R+beta/ R-beta

print("Nominal wheelbase: " + str(nominal_wheelbase))
print("Dr/Dl: " + str(drl))

#######################################################
# User Interface:
#######################################################
root= tk.Tk()
root.title("Autodom Tool")

# Callback functions
def openfile():
    return filedialog.askopenfilename()

def print_selection(v):
    l.config(text='you have selected ' + v)

# Button to choose rosbag file
button = tk.Button(root, text="Choose Bag File", command=openfile)  # <------
button.pack()

# Label to display slider value
l = tk.Label(root, bg='white', fg='black', width=20, text='empty')
l.pack()

# Slider
s = tk.Scale(root, label='End Point in %', from_=0, to=100, orient=tk.HORIZONTAL, length=200, showvalue=0, tickinterval=10,
             resolution=5, command=print_selection)
s.pack()

# Generate real path
semi_circle_right_x, semi_circle_right_y = generate_semicircle(0, UMBmark_length / 2, UMBmark_length / 2)
semi_circle_left_x, semi_circle_left_y = generate_semicircle(-UMBmark_length, UMBmark_length / 2, -UMBmark_length / 2)
top_line_x, top_line_y = [0, -UMBmark_length], [0, 0] # Top line
bottom_line_x, bottom_line_y = [0, -UMBmark_length], [UMBmark_length, UMBmark_length] # Bottom line

# Plot Odometry and Real Path
figure = plt.Figure(figsize=(6,5), dpi=100)
ax = figure.add_subplot(111)
chart_type = FigureCanvasTkAgg(figure, root)
chart_type.get_tk_widget().pack()
ax.plot(semi_circle_right_x, semi_circle_right_y,'g', semi_circle_left_x, semi_circle_left_y,'g',  top_line_x, top_line_y, 'g', bottom_line_x, bottom_line_y, 'g')
ax.plot(pos_x, pos_y, 'b')
ax.scatter(possible_curve_points_x, possible_curve_points_y)
ax.set_title('Robot Position in X and Y')
ax.set_ylabel('Y [Meters]')
ax.set_xlabel('X [Meters]')
red_patch = mpatches.Patch(color='green', label='Real Path')
blue_patch = mpatches.Patch(color='blue', label='Sensor Data')
ax.legend(handles=[red_patch, blue_patch])

root.mainloop()
