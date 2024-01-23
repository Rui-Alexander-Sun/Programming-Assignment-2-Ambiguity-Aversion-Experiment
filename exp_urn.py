import random


def random_portion(size, n):
    """ split balls into n parts of different colors

    Args:
        size: the total amount of balls
        n: amount of colors

    Returns:
        portions: a list of int for each part
    """
    random_integers = sorted(random.sample(range(0, size + 1), n - 1))
    portions = []
    last = 0
    for i in random_integers:
        portion = i - last
        portions.append(portion)
        last = i
    portions.append(size - last)
    return portions


class Urns:
    """ class of urn"""

    def __init__(self, name, colors, image_path="urn.png"):
        """ initialize urn with name and amount of colors

        Args:
            name: name of urn
            colors: colors of balls in this urn
            image_path: path of urn image
        """
        self.name = name
        self.colors = colors
        self.color_num = []
        self.image_path = image_path


class FixUrns(Urns):
    """ class of fix-mix urns"""

    def __init__(self, name, colors, color_num, image_path="urn.png"):
        """ initialize urn with name, colors, color_num

        Args:
            name: name of urn
            colors: a list containing colors, make sure the names of
                    colors correspond to the path of ball images
            color_num: a list containing int indicating the amount of each color
            image_path: path of urn image
        """
        super().__init__(name, colors, image_path)
        self.size = sum(color_num)
        self.color_num = color_num

    def set_instruction(self, urn_name):
        """set instruction for fix-mix urn in each trial

        Args:
            urn_name: e.g. Urn A

        Returns:
            instruction: instruction text
        """
        i = 0
        text = ""
        for color in self.colors:
            num = self.color_num[0]
            if num == 1:
                marble = "marble"
            else:
                marble = "marbles"
            text += str(num) + " " + color + " " + marble + ", "
            i += 1
        text = text[0:-2]
        instruction = urn_name + " contains " + text + "."
        return instruction


class RandomUrns(Urns):
    """ class of random-mix urns"""

    def __init__(self, name, colors, size, image_path="urn.png"):
        """initialize urn with name, colors, size

        Args:
            name: name of urn
            colors: a list containing colors, make sure the names of
                    colors correspond to the path of ball images
            size: the total amount of the balls in this urn
            image_path: path of urn image
        """
        super().__init__(name, colors, image_path)
        self.size = size
        self.color_num = random_portion(self.size, len(colors))

    def set_instruction(self, urn_name):
        """set instruction for random-mix urn in each trial

        Args:
            urn_name: e.g. Urn A

        Returns:
            instruction: instruction text
        """
        instruction = (urn_name + " contains " + str(self.size) +
                       " marbles in an unknown color ratio. "
                       "\nThe mixture of marbles in " + urn_name +
                       " is decided by \nthe computer programming randomly."
                       " \nEvery possible mixture in " + urn_name +
                       " is equally possible.")
        return instruction
