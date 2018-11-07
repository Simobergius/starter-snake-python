
import sys

class FileWriter:
    def __init__(self):
        pass

    def write(self, filename, data):
        file = open(self.dir + filename, "w")
        file.write(data)
        file.close()

    def setDir(self, path):
        self.dir = path + "/"
        pass
