# Autodom

This is a GUI tool to help roboticists in creating and calibrating the odometry for robots using a simple and intuitive interface.

# Installing

```
pip install PyQt5
pip install matplotlib
pip install bagpy
pip install numpy
pip intall pandas
```

# Files

* **Pyqt.py** This is the main code
* **helper_functions.py** This is where all functions are
* **mplwidget.py** This is the class for the matplotlib widget

# Milestones
* Import rosbag :white_check_mark:
* Choose the plattaform (Ackermann | Diff.) :white_check_mark:
* Choose the topics :white_check_mark:
* Trim rosbag time :white_check_mark:
* Odometry for Car-Like robots
  * Supported Inputs: VESC | Incremental Encoder :black_square_button:
* Odometry for Diff. Drive robots :black_square_button:
  * Supported Inputs: Incremental Encontrei :black_square_button:
* Odometry visualization :white_check_mark:
* Odometry calibration :black_square_button:
