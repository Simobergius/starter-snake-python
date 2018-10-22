
import random
import json
import pprint

class snake:
    def __init__(self):
        self.lastDir = 'up'
        self.strategy = 'eat'
        self.nearestApple = { "x": 0, "y": 0 }
        self.distanceToNearestApple = 100000000000
        self.target = { "x": 0, "y": 0 }
    def doAction(self, data):
        self.head = data["you"]["body"][0]
        self.data = data
        
        #if self.target == self.head or not self.target in self.data["board"]["food"]:
        #    #When target reached or target is not apple
        #    #Use current position to choose next target
        #    if self.head["x"] < self.data["board"]["width"] / 2:
        #        #Left side of map
        #        if self.head["y"] < self.data["board"]["height"] / 2:
        #            #Upper Left -> find apple in lower right
        #            self.target = self.findNearestAppleToPoint({ "x": 0, "y": data["board"]["height"]})
        #        else:
        #            #Lower left -> find apple in lower right
        #            self.target = self.findNearestAppleToPoint({ "x": data["board"]["width"], "y": data["board"]["height"]})
        #    else:
        #        #Right side of map
        #        if self.head["y"] < self.data["board"]["height"] / 2:
        #            #Upper right -> find apple in upper left
        #            self.target = self.findNearestAppleToPoint({ "x": 0, "y": 0})
        #        else:
        #            #Lower right -> find apple in upper right
        #            self.target = self.findNearestAppleToPoint({ "x": data["board"]["width"], "y": 0})
        #        
        #    print "Changing target, new:"
        #    print self.target
        
        print "Head: "
        print self.head
        
        forbidden_dirs = self.checkWrongDirs()
        
        self.findNearestApple()
        self.target = self.nearestApple
        print "Target:"
        print self.target
        
        directions = [ 'up', 'down', 'left', 'right' ]
        for dir in forbidden_dirs:
            directions.remove(dir)
        
        #direction = random.choice(directions)
        return self.chooseDir(directions)
    
    def checkWrongDirs(self):
        forbidden_dirs = []
        forbidden_spaces = []
        
        for snake in self.data["board"]["snakes"]:
            forbidden_spaces.extend(snake["body"])
            
            #Add forbidden spaces next to larger snake' heads
            if snake["id"] != self.data["you"]["id"]:
                if len(snake["body"]) >= len(self.data["you"]["body"]):
                    forbidden_spaces.append({
                                                "x": snake["body"][0]["x"] - 1,
                                                "y": snake["body"][0]["y"]
                                            })
                    forbidden_spaces.append({
                                                "x": snake["body"][0]["x"] + 1,
                                                "y": snake["body"][0]["y"]
                                            })
                    forbidden_spaces.append({
                                                "x": snake["body"][0]["x"],
                                                "y": snake["body"][0]["y"] - 1
                                            })
                    forbidden_spaces.append({
                                                "x": snake["body"][0]["x"],
                                                "y": snake["body"][0]["y"] + 1
                                            })
            
        #Left
        if {
            "x": self.head["x"] - 1,
            "y": self.head["y"]
        } in forbidden_spaces or self.head["x"] == 0:
            forbidden_dirs.extend(['left'])
        
        #Right
        if {
            "x": self.head["x"] + 1,
            "y": self.head["y"]
        } in forbidden_spaces or self.head["x"] == self.data["board"]["width"] - 1:
            forbidden_dirs.extend(['right'])
        #Up
        if {
            "x": self.head["x"],
            "y": self.head["y"] - 1
        } in forbidden_spaces or self.head["y"] == 0:
            forbidden_dirs.extend(['up'])
        #Down
        if {
            "x": self.head["x"],
            "y": self.head["y"] + 1
        } in forbidden_spaces or self.head["y"] == self.data["board"]["height"] - 1:
            forbidden_dirs.extend(['down'])
        return forbidden_dirs
    
    def chooseDir(self, dirs):
        dirsToTarget = self.findCompassDirFromPointToPoint(self.head, self.target)
        
        goodDirs = []
        for dir in dirs:
            if dir in dirsToTarget:
                goodDirs.extend([dir])
                
        print "Good dirs:"
        print goodDirs
        
        if len(goodDirs) > 0:
            if self.lastDir in goodDirs:
                chosenDir = self.lastDir
            else:
                chosenDir = random.choice(goodDirs)
        else:
            if self.lastDir in dirs:
                chosenDir = self.lastDir
            else:
                chosenDir = random.choice(dirs)
        
        self.nextGameState = self.data
            
        self.lastDir = chosenDir
        
        return chosenDir
        
    def findNearestApple(self):
        apples = self.data["board"]["food"]
        distanceToNearestApple = 10000000
        for apple in apples:
            if self.calculateDistance(apple, self.head) < distanceToNearestApple:
                self.nearestApple = apple
                distanceToNearestApple = self.calculateDistance(apple, self.head)
                self.distanceToNearestApple = distanceToNearestApple
        
    def findNearestAppleToPoint(self, point):
        apples = self.data["board"]["food"]
        distanceToNearestApple = 10000000
        for apple in apples:
            if self.calculateDistance(apple, point) < distanceToNearestApple:
                nearestApple = apple
                distanceToNearestApple = self.calculateDistance(apple, nearestApple)
        return nearestApple
    
    def calculateDistance(self, pointa, pointb):
        return abs(pointa["x"] - pointb["x"]) + abs(pointa["y"] - pointb["y"])
    
    def findCompassDirFromPointToPoint(self, source, dest):
        directions = [ 'up', 'down', 'left', 'right' ]
        if source["x"] < dest["x"]:
            # Go Right
            if 'left' in directions:
                directions.remove('left')
        elif source["x"] > dest["x"]:
            # Go Left
            if 'right' in directions:
                directions.remove('right')
        else:
            # We are on same X axis -> go straight up or down
            if 'left' in directions:
                directions.remove('left')
            if 'right' in directions:
                directions.remove('right')
            
        if source["y"] < dest["y"]:
            # Go down
            if 'up' in directions:
                directions.remove('up')
        elif source["y"] > dest["y"]:
            # Go up
            if 'down' in directions:
                directions.remove('down')
        else:
            # We are on same Y axis -> go straight left or right
            if 'up' in directions:
                directions.remove('up')
            if 'down' in directions:
                directions.remove('down')
        return directions