# This holds the person object.
# Has a name which is also used as a label.
# An array of images.


class Person:

    def __init__(self, name='', pictures=[]):
        self.name = name
        self.pictures = pictures

    def __len__(self):
        return len(self.pictures)
