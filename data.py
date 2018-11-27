# The purpose of this python file will be to take images from
# a main directory and create arrays that contain the image
# and corresponding label. These will then be split into folds
# to allow for Cross-Validation.
import os
import person
import fold

# The Default values for the data constructor if none is selected.
PEOPLE_PATH = './People'

class Data:

    # Constructor for Data
    def __init__(self, path, train, test):
        self.people = []
        self.people_count = 0
        self.others = []
        if (train + test) == 1.0:
            self.train = train
            self.test = test
        else:
            print("Values for train and test don't add to 1.0, using default values...")
            self.train = .6
            self.test = .4

    # Method: Gather all images with the respective label for all people.

    # Method: Split data based on the parameter in the constructor into folds.


if __name__ == '__main__':
    print()

