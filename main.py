from PyQt6.QtWidgets import QApplication
from exp_window import ExperimentWindow
from exp_recorder import Recorders
from exp_setting import Settings

# instantiate setting object, recorder object
setting = Settings()
recorder = Recorders(setting)

# choose conditions based on experiment design(see settings.between)
# one condition per participant if between
# all conditions for every participant if within
setting.choose_condition(recorder)

# create a QApp
app = QApplication([])

# get trials objects
trials = setting.set_trials()

# instantiate an experiment window
window = ExperimentWindow(trials, setting, recorder)
window.show()
app.exec()
