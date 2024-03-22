import os
import yaml


class Helper:

    LOCATORS_PATH = os.path.join(os.path.dirname(__file__), "locators")

    def __init__(self):
        pass

    # function to read data from file
    def get_locators(self, filename):
        locators = {}
        file_path = os.path.join(self.LOCATORS_PATH, filename)
        # load yaml file in dictionary
        with open(file_path, "r") as file:
            locators = yaml.load(file, Loader=yaml.FullLoader)
        return locators
