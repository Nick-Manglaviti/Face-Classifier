# This holds the person object.
# Has a name which is also used as a label.
# An array of images.


class Person:

    def __init__(self, name, pictures):
        self.name = name
        self.pictures = pictures

    def person_to_string(self):
        print(self.name)
        print(len(self.pictures))

