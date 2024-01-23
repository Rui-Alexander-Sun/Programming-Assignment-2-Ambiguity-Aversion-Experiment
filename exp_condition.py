class Conditions:
    """ class of experiment conditions"""

    def __init__(self, name, urns):
        """ initialize conditions class

        Args:
            name: name of condition
            urns: urns in this condition
        """
        self.name = name
        self.urns = urns
        self.urn_positions = self.get_urn_names()

    def get_urn_names(self):
        urn_positions = []
        for urn in self.urns:
            urn_positions.append(urn.name)
        urn_positions = ' '.join(urn_positions)
        return urn_positions
