# The purpose of this python file will be to take images from
# a main directory and create arrays that contain the image
# and corresponding label. These will then be split into folds
# to allow for Cross-Validation.

import os
import cv2
import numpy as np
from person import Person
from fold import Fold

# The Default values for the data constructor if none is selected.
PEOPLE_PATH = './People'
CASCADE_PATH = '/usr/local/lib/python3.6/dist-packages/cv2/data/haarcascade_frontalface_default.xml'


class Data:

    def __init__(self, path='', num_folds=5):
        """
        Constructor to initialize the dataset.
        :param path:
        :param num_folds:
        """
        self.people = []
        self.random = 0
        self.path = path
        self.folds = []
        self.num_folds = num_folds
        if not os.path.isdir(self.path):
            print("This path is not a valid directory")
            raise ValueError
        if self.num_folds < 3:
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
                        image = cv2.imread(os.path.join(person_path, image))
                        images.append(image)
                if len(images) < self.num_folds:
                    print(f'Not enough images. Must be more than the amount of folds, {self.num_folds}')
                else:
                    person = Person(label, images)
                    if person.name == "Random":
                        self.random = 1
                    self.people.append(person)
        if self.random == 0:
            print(f'No random people images were found for the dataset. A directory named Random needs to exist '
                  f'with more pictures than there are folds to compare and test against the others.')
            raise ValueError
        print("This many people in Dataset: {0}".format(len(self.people) - 1))

    def format_images(self):
        """
        This method will rip out the face from the image.
        It will also format it to be computed by a computational graph.
        """
        for person in self.people:
                for picture in person.pictures:
                    frame_gray = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
                    cascade = cv2.CascadeClassifier(CASCADE_PATH)

                    face_rect = cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))
                    if len(face_rect) > 0:
                        color = (255, 255, 255)
                        for rect in face_rect:
                            cv2.rectangle(picture, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color, thickness=2)
                            x, y = rect[0:2]
                            width, height = rect[2:4]
                            image = picture[y - 10: y + height, x: x + width]
                            cv2.imshow('img', image)
                            cv2.waitKey(1500)
                            cv2.destroyAllWindows()

    def split_into_folds(self):
        """
        Split each person's
        images into each fold
        """
        for x in range(self.num_folds):
            images = []
            labels = []
            for person in self.people:
                portion = len(person) // (self.num_folds - x)
                images += person.pictures[0:portion]
                labels += [person.name] * portion
                del person.pictures[0:portion]
            if (len(images) >= self.num_folds) and (len(labels) == len(images)):
                fold = Fold(images, labels)
                self.folds.append(fold)
            else:
                raise ValueError
        print('done')


if __name__ == '__main__':

    data1 = Data(PEOPLE_PATH, 5)
