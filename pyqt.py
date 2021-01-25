import sys
import matplotlib
matplotlib.use('QT5Agg')
from bagpy import bagreader
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore, QtWidgets, uic
from helper_functions import generate_semicircle, read_akermann_topics, odometry
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure



class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('autodom.ui', self)
        self.BagButton.clicked.connect(self.showDialog)
        self.AutoButton.clicked.connect(self.autodom)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setGeometry(200, 200, 300, 300)
        self.toolbar = NavigationToolbar(self.canvas, self)


    def showDialog(self, MainWindow):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if self.fileName:
            print(self.fileName)
            self.bag = bagreader(self.fileName)
            topics_list = self.bag.topic_table["Topics"].values.tolist()
            for topic in topics_list:
                self.comboBox_topic_1.addItem(topic)
                self.comboBox_topic_2.addItem(topic)

    def autodom(self):
        wheelbase = 0.274
        UMBmark_length = 3
        number_poles = 2
        motor_reduction = 4
        wheel_radius = 0.043  # Meters

        topic_1 = self.comboBox_topic_1.currentText()
        topic_2 = self.comboBox_topic_2.currentText()

        slider_in = 0.0
        slider_out = 0.3

        speed_rpm, servo_angle_rad, timestamps, length = read_akermann_topics(self.bag, topic_1, topic_2,
                                                                              wheel_radius, motor_reduction,
                                                                              number_poles)
        pos_x, pos_y, possible_curve_points_x, possible_curve_points_y, diff_th = odometry(slider_in, slider_out,
                                                                                           speed_rpm, servo_angle_rad,
                                                                                           timestamps, wheelbase)

        # Generate real path
        semi_circle_right_x, semi_circle_right_y = generate_semicircle(0, UMBmark_length / 2, UMBmark_length / 2)
        semi_circle_left_x, semi_circle_left_y = generate_semicircle(-UMBmark_length, UMBmark_length / 2,
                                                                     -UMBmark_length / 2)
        top_line_x, top_line_y = [0, -UMBmark_length], [0, 0]  # Top line
        bottom_line_x, bottom_line_y = [0, -UMBmark_length], [UMBmark_length, UMBmark_length]  # Bottom line

        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot(semi_circle_right_x, semi_circle_right_y,'g', semi_circle_left_x, semi_circle_left_y,'g',  top_line_x, top_line_y, 'g', bottom_line_x, bottom_line_y, 'g')
        self.canvas.draw()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())