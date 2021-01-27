from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from helper_functions import generate_semicircle, read_akermann_topics, odometry
from PyQt5.QtWidgets import QFileDialog
import matplotlib.patches as mpatches
from PyQt5 import QtWidgets, uic
from bagpy import bagreader
import sys



class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('autodom.ui', self)
        self.fileName = None
        self.setWindowTitle("Autodom Tool")
        self.BagButton.clicked.connect(self.showDialog)
        self.AutoButton.clicked.connect(self.autodom)
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        self.MplWidget.canvas.axes.set_title('Robot Position in X and Y')
        self.MplWidget.canvas.axes.set_ylabel('Y [Meters]')
        self.MplWidget.canvas.axes.set_xlabel('X [Meters]')
        self.SliderIn.valueChanged.connect(self.value_changed)
        self.SliderOut.valueChanged.connect(self.value_changed)
        self.labelSliderIn.setText("t_begin: 0%")
        self.labelSliderOut.setText("t_end: 100%")


    def showDialog(self, MainWindow):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                  "Rosbag Files (*.bag)", options=options)
        if self.fileName:
            self.statusbar.showMessage("File loaded: " + self.fileName)
            self.bag = bagreader(self.fileName)
            topics_list = self.bag.topic_table["Topics"].values.tolist()
            for topic in topics_list:
                self.comboBox_topic_1.addItem(topic)
                self.comboBox_topic_2.addItem(topic)

    def value_changed(self):
        self.labelSliderIn.setText("t_begin: " + str(100 - float(self.SliderIn.value())) + "%")
        self.labelSliderOut.setText("t_end: " + str(float(self.SliderOut.value())) + "%")

    def autodom(self):

        if not self.fileName:
            self.statusbar.showMessage("Select rosbag file first")
            return

        wheelbase = 0.274
        UMBmark_length = 3
        number_poles = 2
        motor_reduction = 4
        wheel_radius = 0.043  # Meters

        topic_1 = self.comboBox_topic_1.currentText()
        topic_2 = self.comboBox_topic_2.currentText()

        slider_in = 1 - float(self.SliderIn.value())/100 #0.0
        slider_out = float(self.SliderOut.value())/100 #0.3

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

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(semi_circle_right_x, semi_circle_right_y, 'g', semi_circle_left_x, semi_circle_left_y, 'g', top_line_x,
                top_line_y, 'g', bottom_line_x, bottom_line_y, 'g')
        self.MplWidget.canvas.axes.plot(pos_x, pos_y, 'b')
        self.MplWidget.canvas.axes.scatter(possible_curve_points_x, possible_curve_points_y)
        red_patch = mpatches.Patch(color='green', label='Real Path')
        blue_patch = mpatches.Patch(color='blue', label='Sensor Data')
        self.MplWidget.canvas.axes.legend(handles=[red_patch, blue_patch])
        self.MplWidget.canvas.draw()




if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())