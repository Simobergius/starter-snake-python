import bottle
import os
import random
import json
import pprint

from api import *


@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data
    
    print "Starting game %s" % data["game"]["id"]
    print json.dumps(data, sort_keys=True, indent=4)
    return StartResponse("#00ff00")


@bottle.post('/move')
def move():
    data = bottle.request.json
    # TODO: Do things with data
    
    forbidden_dirs = checkWrongDirs(data)
    print "Forbidden dirs: "
    print forbidden_dirs
    
    directions = [ 'up', 'down', 'left', 'right' ]
    for dir in forbidden_dirs:
        directions.remove(dir)
    
    #direction = random.choice(directions)
    direction = chooseDir(data, directions)

    print "Moving %s" % direction
    return MoveResponse(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data
    print json.dumps(data["you"], sort_keys=True, indent=4)

    print "Game %s ended" % data["game"]["id"]

def checkWrongDirs(data):
    forbidden_dirs = []
    forbidden_spaces = []
    head = data["you"]["body"][0]
    
    for snake in data["board"]["snake"]:
        forbidden_spaces.extend(snake["body"])
        
        #Add forbidden spaces next to larger snake' heads
        if len(snake["body"]) >= len(data["you"]["body"]):
            print "snake %s is larger -> avoid" % snake["name"]
            forbidden_spaces.extend({
                                        "x": snake["body"][0]["x"] - 1,
                                        "y": snake["body"][0]["y"]
                                    })
            forbidden_spaces.extend({
                                        "x": snake["body"][0]["x"] + 1,
                                        "y": snake["body"][0]["y"]
                                    })
            forbidden_spaces.extend({
                                        "x": snake["body"][0]["x"],
                                        "y": snake["body"][0]["y"] - 1
                                    })
            forbidden_spaces.extend({
                                        "x": snake["body"][0]["x"],
                                        "y": snake["body"][0]["y"] + 1
                                    })
        
    #Left
    if {
        "x": head["x"] - 1,
        "y": head["y"]
    } in forbidden_spaces or head["x"] == 0:
        forbidden_dirs.extend(['left'])
    
    #Right
    if {
        "x": head["x"] + 1,
        "y": head["y"]
    } in forbidden_spaces or head["x"] == data["board"]["width"] - 1:
        forbidden_dirs.extend(['right'])
    #Up
    if {
        "x": head["x"],
        "y": head["y"] - 1
    } in forbidden_spaces or head["y"] == 0:
        forbidden_dirs.extend(['up'])
    #Down
    if {
        "x": head["x"],
        "y": head["y"] + 1
    } in forbidden_spaces or head["y"] == data["board"]["height"] - 1:
        forbidden_dirs.extend(['down'])
    return forbidden_dirs

def chooseDir(data, dirs):
    head = data["you"]["body"][0]
    nearestApple = findNearestApple(data)
    dirsToApple = findCompassDirFromPointToPoint(head, nearestApple)
    
    print "Dirs to neares apple"
    print dirsToApple
    
    goodDirs = []
    for dir in dirs:
        if dir in dirsToApple:
            goodDirs.extend([dir])
    
    print "GoodDirs:"
    print goodDirs
    if len(goodDirs) > 0:
        return random.choice(goodDirs)
    else:
        return random.choice(dirs)
    
def findNearestApple(data):
    head = data["you"]["body"][0]
    nearestApple = data["board"]["food"][0]
    shortestDistance = calculateDistance(nearestApple, head)
    for apple in data["board"]["food"]:
        if calculateDistance(apple, head) < shortestDistance:
            nearestApple = apple
            shortestDistance = calculateDistance(apple, head)
    print "NearestApple:"
    print nearestApple
    print "Distance:"
    print shortestDistance
    return nearestApple
    
def calculateDistance(pointa, pointb):
    return abs(pointa["x"] - pointb["x"] + pointa["y"] - pointb["y"])

def findCompassDirFromPointToPoint(source, dest):
    directions = [ 'up', 'down', 'left', 'right' ]
    if source["x"] <= dest["x"]:
        # Go Right
        directions.remove('left')
    else:
        # Go Left
        directions.remove('right')
        
    if source["y"] <= dest["y"]:
        # Go down
        directions.remove('up')
    else:
        # Go up
        directions.remove('down')
    
    return directions
    
# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=True)
