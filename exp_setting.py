from random import shuffle
from exp_urn import RandomUrns, FixUrns
from exp_condition import Conditions
from exp_trial import Trials


class Settings:
    """ class of experiment settings

    Default settings of the experiment
    You can easily modify the settings to change the whole experiment
    """

    def __init__(self):
        """
        between: True, if between-subject design,
                 False, if within-subject design
        min_age: minimum age to participate the experiment
        data_path: csv data file path
        ui_path: ui file path
        image_path: urn image path
        pages_before_trials: amount of pages before the trials
        conditions: amount of conditions
        trial_geo_list: geometric information for trials

        """
        self.between = False
        self.min_age = 18
        self.data_path = self.set_data_path()
        self.ui_path = 'experiment.ui'
        self.image_path = "images/"
        self.urn_path = self.image_path + "urn.png"
        self.ball_path = self.image_path + "ball_"
        self.ball_file_extension = ".png"
        self.pages_before_trials = 3
        self.conditions = self.set_conditions()
        self.trial_geo_list = [100, 100, 800, 600]

    def set_data_path(self):
        data_path = "data.csv"
        if self.between:
            data_path = "between_" + data_path
        else:
            data_path = "within_" + data_path
        return data_path

    def set_conditions(self):
        """ get conditions for this experiment

        Instantiate urn object and condition object you need in this experiment
        You could instantiate as many urns or conditions as you want,
        which makes it very easy to extend the experiment
        See exp_urn.py, exp_condition.py for reference

        return:
            a list containing condition object
        """
        urn_2_random = RandomUrns("urn_2_random",
                                  ["blue", "red"],
                                  2,
                                  self.urn_path)
        urn_2_equal = FixUrns("urn_2_equal",
                              ["blue", "red"],
                              [1, 1],
                              self.urn_path)
        urn_10_random = RandomUrns("urn_10_random",
                                   ["blue", "red"],
                                   10,
                                   self.urn_path)
        urn_10_equal = FixUrns("urn_10_equal",
                               ["blue", "red"],
                               [5, 5],
                               self.urn_path)
        urn_100_random = RandomUrns("urn_100_random",
                                    ["blue", "red"],
                                    100,
                                    self.urn_path)
        urn_100_equal = FixUrns("urn_100_equal",
                                ["blue", "red"],
                                [50, 50],
                                self.urn_path)

        urns1 = [urn_2_random, urn_2_equal]
        urns2 = [urn_10_random, urn_10_equal]
        urns3 = [urn_100_random, urn_100_equal]

        shuffle(urns1)
        shuffle(urns2)
        shuffle(urns3)

        condition1 = Conditions("size2", urns1)
        condition2 = Conditions("size10", urns2)
        condition3 = Conditions("size100", urns3)

        return [condition1, condition2, condition3]

    def choose_condition(self, recorder):
        """choose the condition for participants sequentially
        if between-subject design

        """
        # amount of conditions
        condition_num = len(self.conditions)
        if self.between:
            lines = recorder.read_csv()
            existing_ppt = len(lines) - 1
            index = existing_ppt % condition_num
            current_condition = self.conditions[index]
            self.conditions = [current_condition]

    def set_trials(self):
        """ get trials for this experiment

        Instantiate trials object
        See exp_trial.py for reference

        return:
            a list containing trial objects
        """
        trials = []
        i = 1
        for condition in self.conditions:
            trial = Trials("trial" + str(i), condition, self.trial_geo_list)
            trials.append(trial)
            i += 1
        shuffle(trials)
        return trials

    def condition_num_per_ppt(self):
        """ get the amount of conditions each participant would be assigned to

        return:
            an int,
                1 if between-subject design
                len(self.conditions) if within-subject design
        """
        if self.between:
            return 1
        else:
            return len(self.conditions)
