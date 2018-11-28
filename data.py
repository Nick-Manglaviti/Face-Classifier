# The purpose of this python file will be to take images from
# a main directory and create arrays that contain the image
# and corresponding label. These will then be split into folds
# to allow for Cross-Validation.

import os
import cv2
import numpy
import person as p
import fold

# The Default values for the data constructor if none is selected.
PEOPLE_PATH = './People'


class Data:

    # Constructor for Data
    def __init__(self, path, train, test):
        self.people = []
        self.people_count = 0
        self.others = []
        if os.path.isdir(path):
            self.path = path
        else:
            print("This path is not a valid directory")
            raise ValueError
        self.path = path
        if (train + test) == 1.0:
            self.train = train
            self.test = test
        else:
            print("Values for train and test don't add to 1.0, using default values...")
            self.train = .6
            self.test = .4
        print("Train: {0} Test: {1}".format(self.train, self.test))
        self.read_path()


    # Method: Gather all images with the respective label for all people.
    def read_path(self):
        for directory in os.listdir(self.path):
            print("\nLooking through " + directory)
            person_path = os.path.join(self.path, directory)
            if os.path.isdir(person_path):
                images = []
                label = os.path.basename(person_path)
                for img in os.listdir(person_path):
                    if img.endswith('.jpg') or img.endswith('.JPG'):
                        print(img)
                        image = cv2.imread(os.path.join(person_path, img))
                        images.append(img)
                if images.__len__() < 6:
                    print("Not enough images. Must be more than 5")
                else:
                    images = numpy.array(images)
                    person = p.Person(label, images)
                    person.person_to_string()


    # Method: Format image.

    # Method: Split data based on the parameter in the constructor into folds.


if __name__ == '__main__':

    data1 = Data(PEOPLE_PATH, .6, .4)
