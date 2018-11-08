
import sys
import os

class FileWriter:
    def __init__(self):
        pass

    def write(self, filename, data):
        file = open(self.dir + filename + ".json", "w")
        file.write(data)
        file.close()

    def setDir(self, path):
        path_str = ""
        for dir in path:
            path_str = path_str + dir + "/"
            if not os.path.isdir(path_str):
                os.mkdir(path_str)
        self.dir = path_str
        pass
