import os


class Recorders:
    """class of recorders of the experiment"""

    def __init__(self, setting):
        """initialize the recorders

        Args:
            setting: setting of the experiment
        """
        self.data_path = setting.data_path
        self.condition_num = setting.condition_num_per_ppt()
        self.header = self.get_header()
        self.ppt_seq = 1
        self.init_csv()
        self.ppt_id = self.set_id()
        self.ppt_cmplt = 0
        self.ppt_age = 0
        self.ppt_gender = ""
        self.ppt_edu = ""
        self.ppt_race = ""
        self.ppt_data = [str(self.ppt_seq),
                         str(self.ppt_id),
                         str(self.ppt_cmplt)]

    def init_csv(self):
        """initialize the csv file
        create a new csv file if no such file
        else get the sequence of the participant
        """
        if os.path.exists(self.data_path):
            self.get_seq()
        else:
            data_file = open(self.data_path, 'w')
            data_file.write(','.join(self.header) + '\n')
            data_file.close()

    def set_id(self):
        """The ID is defaulted to the same as participant sequence."""
        return self.ppt_seq

    def read_csv(self):
        """read the csv file"""
        file = open(self.data_path, "r")
        lines = file.readlines()
        return lines

    def get_seq(self):
        """get the sequence of current participant"""
        lines = self.read_csv()
        current_ppt_seq = len(lines)
        self.ppt_seq = current_ppt_seq

    def get_header(self):
        """set the header based on the condition num for each participant"""
        header = ["sequence",
                  "ID",
                  "completed",
                  "age",
                  "gender",
                  "education_level",
                  "race"]
        trial_info = ["condition",
                      "urn_positions",
                      "choice",
                      "ball_color"]
        for i in range(1, self.condition_num + 1):
            prefix = str(i) + "_"
            for info in trial_info:
                header.append(prefix + info)
        return header

    def completed(self):
        """modify self.ppt_complt to 1 if the participant completed all the
        trials"""
        self.ppt_cmplt = 1
        self.ppt_data[2] = str(self.ppt_cmplt)

    def append_demographics(self):
        """append demographic information to the self.ppt_data"""
        self.ppt_data = [str(self.ppt_seq),
                         str(self.ppt_id),
                         str(self.ppt_cmplt),
                         str(self.ppt_age),
                         self.ppt_gender,
                         self.ppt_edu,
                         self.ppt_race]

    def append_trial_data(self, condition_name, urn_positions, choice,
                          ball_color):
        """

        Args:
            condition_name: name of current condition
            urn_positions: positions (i.e. sequence) of urns
            choice: choice the participant
            ball_color: color of the ball drawn by the participant

        """
        self.ppt_data += [condition_name, urn_positions, choice, ball_color]

    def data_to_csv(self):
        """append experiment data to csv"""
        data_file = open(self.data_path, "a")
        data_file.write(','.join(self.ppt_data) + '\n')
