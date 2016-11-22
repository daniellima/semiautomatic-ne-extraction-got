from functools import total_ordering


@total_ordering
class EN:
    def __init__(self, ne_as_string):
        self._original = None
        self._canonico = None
        self.owords = None
        self.cwords = None
        self.sentence = None
        self.in_doubt = False

        self.season = None
        self.episode = None
        self.line = None
        self.start_index = None
        self.end_index = None

        self.original = ne_as_string
        self.canonico = ne_as_string
        self.classification = "other"

    @property
    def canonico(self):
        return self._canonico

    @canonico.setter
    def canonico(self, value):
        self._canonico = value

        if value is not None:
            self.cwords = value.split(" ")
        else:
            self.cwords = []

    @property
    def original(self):
        return self._original

    @original.setter
    def original(self, value):
        self._original = value

        if value is not None:
            self.owords = value.split(" ")
        else:
            self.owords = []

    def __str__(self):
        return "{0} ({1}) - {2}".format(self.canonico, self.original, self.classification)

    def __eq__(self, other):
        return self.canonico == other.canonico

    def __lt__(self, other):
        return self.canonico.__lt__(other.canonico)

    def __hash__(self):
        return self.canonico.__hash__()
