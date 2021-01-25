# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'autodom.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from bagpy import bagreader
from helper_functions import generate_semicircle, read_akermann_topics, odometry
from math import atan2, pi, sin
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.BagButton = QtWidgets.QPushButton(self.centralwidget)
        self.BagButton.setGeometry(QtCore.QRect(10, 10, 111, 25))
        self.BagButton.setObjectName("BagButton")
        self.BagButton.clicked.connect(self.showDialog)  # Add
        self.comboBox_topic_1 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_topic_1.setGeometry(QtCore.QRect(20, 180, 171, 25))
        self.comboBox_topic_1.setObjectName("comboBox_topic_1")
        self.comboBox_topic_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_topic_2.setGeometry(QtCore.QRect(200, 180, 151, 25))
        self.comboBox_topic_2.setObjectName("comboBox_topic_2")
        self.label_topic_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_topic_1.setGeometry(QtCore.QRect(20, 160, 171, 17))
        self.label_topic_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_topic_1.setObjectName("label_topic_1")
        self.label_topic_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_topic_2.setGeometry(QtCore.QRect(200, 160, 151, 17))
        self.label_topic_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_topic_2.setObjectName("label_topic_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 320, 291, 17))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(170, 380, 141, 17))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(20, 380, 141, 17))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(40, 410, 91, 26))
        self.spinBox.setObjectName("spinBox")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setGeometry(QtCore.QRect(190, 410, 101, 26))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(170, 450, 141, 17))
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(190, 480, 101, 26))
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(10, 450, 141, 17))
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(40, 482, 31, 20))
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.spinBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_2.setGeometry(QtCore.QRect(70, 480, 41, 26))
        self.spinBox_2.setObjectName("spinBox_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 50, 131, 91))
        self.groupBox.setObjectName("groupBox")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 60, 112, 23))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 30, 112, 23))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 210, 141, 80))
        self.groupBox_2.setObjectName("groupBox_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_3.setGeometry(QtCore.QRect(0, 30, 112, 23))
        self.radioButton_3.setChecked(True)
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_4.setGeometry(QtCore.QRect(0, 50, 112, 31))
        self.radioButton_4.setObjectName("radioButton_4")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(200, 210, 151, 80))
        self.groupBox_3.setObjectName("groupBox_3")
        self.radioButton_6 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_6.setGeometry(QtCore.QRect(0, 30, 112, 23))
        self.radioButton_6.setChecked(True)
        self.radioButton_6.setObjectName("radioButton_6")
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_5.setGeometry(QtCore.QRect(0, 50, 112, 23))
        self.radioButton_5.setObjectName("radioButton_5")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(30, 350, 121, 16))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(160, 350, 121, 16))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setInvertedAppearance(True)
        self.horizontalSlider_2.setInvertedControls(True)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.AutoButton = QtWidgets.QPushButton(self.centralwidget)
        self.AutoButton.setGeometry(QtCore.QRect(100, 520, 111, 31))
        self.AutoButton.setObjectName("AutoButton")
        self.AutoButton.clicked.connect(self.autodom)  # Add
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(MainWindow, self)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.BagButton.setText(_translate("MainWindow", "Load Rosbag"))
        self.label_topic_1.setText(_translate("MainWindow", "Motor Topic"))
        self.label_topic_2.setText(_translate("MainWindow", "Servo Topic"))
        self.label_6.setText(_translate("MainWindow", "Trim Rosbag Time"))
        self.label_7.setText(_translate("MainWindow", "Wheelbase dist."))
        self.label_8.setText(_translate("MainWindow", "UMBmark lenght"))
        self.label_9.setText(_translate("MainWindow", "Wheel Diameter"))
        self.label_10.setText(_translate("MainWindow", "Motor Roduction"))
        self.label_11.setText(_translate("MainWindow", "1:"))
        self.groupBox.setTitle(_translate("MainWindow", "Type of Robot:"))
        self.radioButton_2.setText(_translate("MainWindow", "Differential"))
        self.radioButton.setText(_translate("MainWindow", "Ackermann"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Type of Data:"))
        self.radioButton_3.setText(_translate("MainWindow", "VESC"))
        self.radioButton_4.setText(_translate("MainWindow", "Inc. Encoder"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Type of Data:"))
        self.radioButton_6.setText(_translate("MainWindow", "VESC"))
        self.radioButton_5.setText(_translate("MainWindow", "Inc. Encoder"))
        self.AutoButton.setText(_translate("MainWindow", "AUTODOM"))

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






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

