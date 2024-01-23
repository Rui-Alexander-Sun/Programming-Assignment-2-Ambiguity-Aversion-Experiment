from random import choices
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel
from PyQt6.QtCore import QPropertyAnimation, QRect
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi


def get_ball(colors, color_num):
    return choices(colors, color_num)[0]


def draw_ball(current_trial, button_name):
    for urn in current_trial.urns:
        if urn.name == button_name:
            colors = urn.colors
            num = urn.color_num
            ball = get_ball(colors, num)
            return ball


class ExperimentWindow(QMainWindow):
    """class of experiment window, inherited from QMainWindow"""

    def __init__(self, trials, setting, recorder):
        """

        Args:
            trials: trials in this experiment
            setting: settings for this experiment
            recorder: recorder for this experiment
        """
        super().__init__()

        self.recorder = recorder
        self.setting = setting
        self.pages_before_trials = setting.pages_before_trials

        loadUi(self.setting.ui_path, self)

        # Connect push button with switching to next page
        self.pushButton_1.clicked.connect(self.to_demography)
        self.pushButton_2.clicked.connect(self.to_trials)
        self.pushButton_3.clicked.connect(self.switch_to_next_page)
        self.trials = trials
        self.init_trials()

    def init_trials(self):
        """insert trial widgets into stacked widgets of main window"""
        i = self.pages_before_trials
        for trial in self.trials:
            self.stackedWidget.insertWidget(i, trial)
            i += 1

    def to_demography(self):
        """switch to demographic widget"""
        if self.checkBox.isChecked():
            self.switch_to_next_page()
        else:
            self.warning_unchecked.setText('Please tick the check box.')

    def warn_message(self, widget_name):
        """show warning message for blank information"""
        self.warning_blank.setText(f'Please fill in {widget_name} information.')

    def age_not_satisfied(self):
        """show warning message if participants' age do not meet the
        requirements of this experiment"""
        self.warning_blank.setText(
            "Sorry, you are not eligible for this experiment"
            " for the reason of age.")

    def to_trials(self):
        """switch to trial widgets"""
        age_value = self.age.value()

        # participants under min_age are not allowed to continue
        if age_value < self.setting.min_age:
            self.age_not_satisfied()
        # show warning message
        else:
            if self.gender.currentText() == "":
                self.warn_message(self.gender.objectName())
            elif self.education.currentText() == "":
                self.warn_message(self.education.objectName())
            elif self.race.currentText() == "":
                self.warn_message(self.race.objectName())
            else:
                self.recorder.ppt_age = self.age.value()
                self.recorder.ppt_gender = self.gender.currentText()
                self.recorder.ppt_edu = self.education.currentText()
                self.recorder.ppt_race = self.race.currentText()
                self.recorder.append_demographics()
                self.switch_to_next_page()

    def find_all_buttons(self):
        """find all the buttons on the current widget

        Returns:
            buttons: all QPushButton objects on this widget
        """
        current_page_widget = self.stackedWidget.currentWidget()
        buttons = current_page_widget.findChildren(QPushButton)
        return buttons

    def connect_all_buttons(self):
        """connect buttons on the trial widgets"""
        buttons = self.find_all_buttons()
        # if the participant clicked any buttons
        # i. information in this trial would be recorded
        # ii. an animation would start
        for button in buttons:
            button.clicked.connect(self.record_trial_info)
            button.clicked.connect(self.draw)

    def disconnect_all_buttons(self):
        """disconnect buttons on the trial widget
        call this function during the animation in case repetitive clicks
        """
        buttons = self.find_all_buttons()
        for button in buttons:
            button.clicked.disconnect(self.record_trial_info)
            button.clicked.disconnect(self.draw)

    def record_trial_info(self):
        """record information in this trial by modifying the values in
        the settings"""
        current_index = self.stackedWidget.currentIndex()
        current_trial = self.trials[current_index - self.pages_before_trials]
        self.condition_name = current_trial.condition_name
        self.urn_positions = current_trial.urn_positions
        self.button_clicked_name = self.button_clicked()
        self.ball_color = draw_ball(current_trial, self.button_clicked_name)
        self.recorder.append_trial_data(self.condition_name,
                                        self.urn_positions,
                                        self.button_clicked_name,
                                        self.ball_color)

    def button_clicked(self):
        """find the button which was clicked by the participant

        Returns:
            button_name: name of the clicked button
        """
        sender_button = self.sender()
        button_name = sender_button.objectName()
        return button_name

    def switch_to_next_page(self):
        """switch to the next page"""
        current_index = self.stackedWidget.currentIndex()
        next_index = (current_index + 1) % self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(next_index)
        current_index = self.stackedWidget.currentIndex()
        # if current page is the final page
        # record the information of this experiment
        # elif current page is trial page, connect buttons
        if current_index == self.stackedWidget.count() - 1:
            self.recorder.completed()
            self.recorder.data_to_csv()
        elif current_index >= self.pages_before_trials and current_index < len(
                self.trials) + self.pages_before_trials:
            self.connect_all_buttons()

    def draw(self):
        """show an animation of drawing ball"""

        # find the chosen urn
        current_page_widget = self.stackedWidget.currentWidget()
        labels = current_page_widget.findChildren(QLabel)
        urn_name = "image_" + self.button_clicked_name
        for label in labels:
            if label.objectName() == urn_name:
                urn_chosen = label

        # get the geometric information of the urn
        urn_geometry = urn_chosen.geometry()
        x, y, width, height = (
            urn_geometry.x(),
            urn_geometry.y(),
            urn_geometry.width(),
            urn_geometry.height())

        # set the geometric information of the ball
        ball_height = round(height * 0.2)
        ball_width = ball_height
        ball_x = round(x + width * 0.5 - ball_width * 0.5)
        ball_y = round(y + height * 0.1)
        end_x = ball_x
        end_y = round(ball_y - height * 0.1)

        # instantiate a QLabel
        ball_png_path = self.setting.ball_path + \
                         self.ball_color +\
                         self.setting.ball_file_extension
        ball_png = QPixmap(ball_png_path)
        self.ball = QLabel(self.stackedWidget.currentWidget())
        self.ball.setGeometry(ball_x, ball_y, ball_width, ball_height)
        self.ball.setPixmap(ball_png)
        self.ball.setScaledContents(True)
        self.ball.show()

        # instantiate a QPropertyAnimation
        self.anim = QPropertyAnimation(self.ball, b'geometry')
        self.anim.setDuration(1000)
        self.anim.setStartValue(QRect(ball_x, ball_y, ball_width, ball_height))
        self.anim.setEndValue(QRect(end_x, end_y, ball_width, ball_height))
        self.anim.start()
        self.disconnect_all_buttons()
        # switch to the next page after the anim finished
        self.anim.finished.connect(self.switch_to_next_page)

    def closeEvent(self, event):
        """record the data if and only if the participant exit the experiment
        before completing it"""
        if self.recorder.ppt_cmplt != 1:
            self.recorder.data_to_csv()
        super().closeEvent(event)
