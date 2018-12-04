# The purpose of this python file will be to take images from
# a main directory and create arrays that contain the image
# and corresponding label. These will then be split into folds
# to allow for Cross-Validation.

import os
import cv2
from person import Person
from fold import Fold

# The Default values for the data constructor if none is selected.
PEOPLE_PATH = './People'


class Data:

    def __init__(self, path='', num_folds=5):
        """
        Constructor to initialize the dataset.
        :param path:
        :param num_folds:
        """
        self.people = []
        self.random = Person()
        self.path = path
        self.folds = []
        for x in range(num_folds):
            images = []
            labels = []
            fold = Fold(images, labels)
            self.folds.append(fold)
        if not os.path.isdir(self.path):
            print("This path is not a valid directory")
            raise ValueError
        if len(self.folds) < 3:
            print("Cannot use less than three folds for cross validation")

        self.read_path()
        self.format_images()
        self.split_into_folds()

    def read_path(self):
        """
        Gather all images with the respective label for all people
        with the given path.
        """
        for directory in os.listdir(self.path):
            print("\nLooking through " + directory)
            person_path = os.path.join(self.path, directory)
            if os.path.isdir(person_path):
                images = []
                label = os.path.basename(person_path)
                for image in os.listdir(person_path):
                    if image.endswith('.jpg') or image.endswith('.JPG'):
                        #image = cv2.imread(os.path.join(person_path, image))
                        images.append(image)
                if len(images) < len(self.folds):
                    print(f'Not enough images. Must be more than the amount of folds, {len(self.folds)}')
                else:
                    person = Person(label, images)
                    if person.name == "Random":
                        self.random = person
                    else:
                        self.people.append(person)
        if self.random.name != 'Random' or len(self.random.pictures) < len(self.folds):
            print(f'No random people images were found for the dataset. A directory named Random needs to exist '
                  f'with more pictures than there are folds to compare and test against the others.')
            raise ValueError
        print("This many people in Dataset: {0}".format(len(self.people)))

    def format_images(self):
        """
        This method will rip out the face from the image.
        It will also format it to be computed by a computational graph.
        """
        #face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        #for person in self.people:
        #    for picture in person.pictures:
        #        cv2.imshow('img', picture)
        #        cv2.waitKey(1000)
        #        cv2.destroyAllWindows()

    def split_into_folds(self):
        """
        Split each person's
        images into each fold
        """
        for person in self.people:
            offset = 0
            for x in range(len(self.folds)):
                portion = (len(person.pictures) - offset) // (len(self.folds) - x)
                person.insert_images(offset, portion, self.folds[x].images)
                offset += portion
                while portion > 0:
                    self.folds[x].labels.append(person.name)
                    portion -= 1
        print("Done")



if __name__ == '__main__':

    data1 = Data(PEOPLE_PATH, 5)
