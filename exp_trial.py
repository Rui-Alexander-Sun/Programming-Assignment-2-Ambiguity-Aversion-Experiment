from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class Trials(QWidget):
    """class of trials"""

    def __init__(self, name, condition, geo_list):
        """

        Args:
            name: name of this trial
            condition: condition of this trial
            geo_list: geometric information of this trial

        """
        super().__init__()
        self.setObjectName(name)
        self.condition_name = condition.name
        self.urns = condition.urns
        self.urn_positions = condition.urn_positions
        self.geo_list = geo_list
        self.image_labels = []
        self.init_ui()

    def init_ui(self):
        """initialize ui widget"""
        self.setWindowTitle('Trial')
        self.setGeometry(*self.geo_list)

        self.layout = QGridLayout(self)

        self.load_images()

        self.setLayout(self.layout)

    def load_images(self):
        """set image_labels, caption_labels, instruction labels,
        push_buttons for each urn

        automatic layout

        """
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'x', 'Y', 'Z']
        row = 0
        col = 0
        i = 0
        for urn in self.urns:

            caption_text = 'Urn ' + alphabet[i]

            # create image labels
            image_label = QLabel(self)
            image_label.setObjectName("image_" + urn.name)
            pixmap = QPixmap(urn.image_path)
            image_label.setPixmap(pixmap.scaledToWidth(
                int(self.geo_list[2] / len(self.urns))))
            image_label.setPixmap(pixmap.scaledToHeight(
                int(self.geo_list[3] / len(self.urns))))
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # create caption labels
            caption_label = QLabel(self)
            caption_label.setText(caption_text)
            caption_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # create instruction labels
            instruction_label = QLabel(self)
            instruction_text = urn.set_instruction(caption_text)
            instruction_label.setText(instruction_text)

            # Create push buttons to choose the urn
            urn_button = QPushButton(self)
            urn_button.setObjectName(urn.name)
            urn_button.setText("choose " + caption_text)

            # add them to layout
            self.image_labels.append((image_label, caption_label, urn_button))
            self.layout.addWidget(image_label, row, col)
            self.layout.addWidget(caption_label, row + 1, col)
            self.layout.addWidget(instruction_label, row + 2, col)
            self.layout.addWidget(urn_button, row + 3, col)

            # 2 images per row, one pack every 3 rows
            col += 1
            if col > 1:
                col = 0
                row += 4
            i += 1
