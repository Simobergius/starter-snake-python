
import random
import json
import pprint
import point
import helpers

class snake:
    def __init__(self, useDebug):
        self.lastDir = 'up'
        self.strategy = 'eat'
        self.nearestApple = { "x": 0, "y": 0 }
        self.distanceToNearestApple = 100000000000
        self.target = { "x": 0, "y": 0 }
        self.useDebug = useDebug

    def debug(self, str):
        if self.useDebug:
            print(str)

    def doAction(self, data):
        self.head = point.topoint(data["you"]["body"][0])
        self.data = data
        #Figure out direction im heading
        self.lastDir = (self.head - point.topoint(data["you"]["body"][1])).todir()
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
        #    self.debug("Changing target, new:")
        #    self.debug(self.target)
        
        self.debug("Head: ")
        self.debug(self.head)
        
        self.forbidden_points = []
        self.getForbiddenPoints()
        forbidden_dirs = self.checkWrongDirs()
        
        self.findNearestApple()
        self.target = point.topoint(self.nearestApple)
        self.debug("Target:")
        self.debug(self.target)
        self.debug("Forbidden dirs:")
        self.debug(forbidden_dirs)
        
        directions = list(helpers.basic_dirs)
        self.debug("helpers.basic_dirs")
        self.debug(helpers.basic_dirs)
        for dir in forbidden_dirs:
            if dir in directions:
                directions.remove(dir)
        
        #direction = random.choice(directions)
        return self.chooseDir(directions)
    def getForbiddenPoints(self):
        points = []
        
        for snake in self.data["board"]["snakes"]:
            if not snake["health"] == 0:
                points.extend(snake["body"])
        
        #Add upper & lower limits
        for i in range(0, self.data["board"]["width"]):
            points.append(point.point(i,-1))
            points.append(point.point(i,self.data["board"]["height"]))
        
        #Add right and left limits
        for i in range(0, self.data["board"]["height"]):
            points.append(point.point(-1,i))
            points.append(point.point(self.data["board"]["width"],i))
            
        self.forbidden_points = points
        
    def checkWrongDirs(self):
        forbidden_dirs = []
        forbidden_spaces = self.forbidden_points
        for snake in self.data["board"]["snakes"]:
            #Add forbidden spaces next to larger snake' heads
            if snake["id"] != self.data["you"]["id"]:
                if len(snake["body"]) >= len(self.data["you"]["body"]):
                    forbidden_spaces.append(point.topoint(snake["body"][0]) + point.topoint('left'))
                    forbidden_spaces.append(point.topoint(snake["body"][0]) + point.topoint('right'))
                    forbidden_spaces.append(point.topoint(snake["body"][0]) + point.topoint('up'))
                    forbidden_spaces.append(point.topoint(snake["body"][0]) + point.topoint('down'))
        

        
        #Translate forbidden_spaces into forbidden_dirs (directions that would cause immediate death, no-go dirs)
        #Left
        if self.head + point.topoint('left') in forbidden_spaces:
            forbidden_dirs.extend(['left'])
        
        #Right
        if self.head + point.topoint('right') in forbidden_spaces:
            forbidden_dirs.extend(['right'])
        #Up
        if self.head + point.topoint('up') in forbidden_spaces:
            forbidden_dirs.extend(['up'])
        #Down
        if self.head + point.topoint('down') in forbidden_spaces:
            forbidden_dirs.extend(['down'])
        return forbidden_dirs
    
    def chooseDir(self, dirs):
        dirsToTarget = self.findCompassDirFromPointToPoint(self.head, self.target)
        self.debug("checkWrongDirs")
        self.debug("dirs")
        self.debug(dirs)
        self.debug("dirsToTarget")
        self.debug(dirsToTarget)
        
        #TODO: Use findFarthestDeadEnd to choose dir when multiple choices
        # check points in front of head
        point_in_front = self.head + point.topoint(self.lastDir)
        turn_ccw_dir = (point.topoint(self.lastDir).rotateCCW()).todir()
        turn_cw_dir = (point.topoint(self.lastDir).rotateCW()).todir()
        
        if point_in_front in self.forbidden_points:
            # counterclockwise or clockwise
            dirs = self.findFarthestDeadEnd([turn_ccw_dir, turn_cw_dir])
        elif point_in_front + point.topoint(self.lastDir).rotateCCW() in self.forbidden_points and point_in_front + point.topoint(self.lastDir).rotateCW() in self.forbidden_points:
            #straight, counterclockwise or clockwise
            dirs = self.findFarthestDeadEnd([turn_ccw_dir, turn_cw_dir, self.lastDir])
        elif point_in_front + point.topoint(self.lastDir).rotateCCW() in self.forbidden_points:
            # straight or counterclockwise
            dirs = self.findFarthestDeadEnd([turn_ccw_dir, self.lastDir])
        elif point_in_front + point.topoint(self.lastDir).rotateCW() in self.forbidden_points:
            # straight or clockwise
            dirs = self.findFarthestDeadEnd([self.lastDir, turn_cw_dir])
        
        goodDirs = []
        for dir in dirs:
            if dir in dirsToTarget:
                goodDirs.append(dir)
                
        self.debug("Good dirs:")
        self.debug(goodDirs)
        
        
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
        
        return chosenDir
        
    def findNearestApple(self):
        apples = self.data["board"]["food"]
        distanceToNearestApple = 10000000 # fugly but works
        for apple in apples:
            pointFromHeadToaApple = self.head - apple
            if pointFromHeadToaApple.dist() < distanceToNearestApple:
                self.nearestApple = apple
                distanceToNearestApple = pointFromHeadToaApple.dist()
                self.distanceToNearestApple = distanceToNearestApple
        
    def findNearestAppleToPoint(self, point):
        apples = self.data["board"]["food"]
        distanceToNearestApple = 10000000 # fugly but works
        for apple in apples:
            fromPointToApple = point - apple
            if fromPointToApple.dist() < distanceToNearestApple:
                nearestApple = apple
                distanceToNearestApple = fromPointToApple.dist()
        return nearestApple
    
    def findCompassDirFromPointToPoint(self, source, dest):
        directions = [ 'up', 'down', 'left', 'right' ]
        if source.x < dest.x:
            # Go Right
            if 'left' in directions:
                directions.remove('left')
        elif source.x > dest.x:
            # Go Left
            if 'right' in directions:
                directions.remove('right')
        else:
            # We are on same X axis -> go straight up or down
            if 'left' in directions:
                directions.remove('left')
            if 'right' in directions:
                directions.remove('right')
            
        if source.y < dest.y:
            # Go down
            if 'up' in directions:
                directions.remove('up')
        elif source.y > dest.y:
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
        
    def findFarthestDeadEnd(self, dirs):
        self.debug("findFarthestDeadEnd(dirs=%s)" % str(dirs))
        #Remove dirs that are immediately blocked
        for dir in dirs:
            if self.head + point.topoint(dir) in self.forbidden_points:
                dirs.remove(dir)

        contiguous_spaces = {k: [self.head + point.topoint(k)] for k in dirs}
        border_spaces = {k: [self.head + point.topoint(k)] for k in dirs}
        possible_dirs = []
        while True:
            for dir in dirs:
                if len(contiguous_spaces) == 1:
                    # One valid dir remaining
                    possible_dirs.extend(list(contiguous_spaces.keys()))
                    return possible_dirs
                new_point_found = False
                #find contiguous segment, keep count
                for pointvar in border_spaces[dir]:
                    #find one valid point next to border point in list
                    for i, basic_dir in enumerate(helpers.basic_dirs):
                        newpoint = pointvar + point.topoint(basic_dir)
                        #check if point is already in a segment
                        newpoint_in_other_segments = False
                        for dir2 in contiguous_spaces:
                            if dir2 == dir:
                                continue
                            if newpoint in contiguous_spaces[dir2]:
                                #Check here if point is already in other dirs' continuous segments -> remove other
                                #Keep it as possible
                                possible_dirs.append(dir2)
                                del contiguous_spaces[dir2]

                        if not (newpoint in self.forbidden_points or newpoint_in_other_segments):
                            contiguous_spaces[dir].append(newpoint)
                            border_spaces[dir].append(newpoint)
                            new_point_found = True

                        if i == len(helpers.basic_dirs) - 1:
                            #If all 4 dirs have been checked and no new point found
                            #Remove from border
                            del border_spaces[dir][pointvar]
                        break
                    if new_point_found:
                        break
                if new_point_found:
                    break
                else:
                    # No new point found for a dirs' continuous segment -> finished -> choose some other dir
                    self.debug("Deleting segment: %s %s" % (dir, str(contiguous_spaces[dir])))
                    del contiguous_spaces[dir]
                
                