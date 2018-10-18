import bottle
import os
import random
import json

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
    return StartResponse("#00ff00")


@bottle.post('/move')
def move():
    data = bottle.request.json
    # TODO: Do things with data
    
    forbidden_dirs = checkWrongDirs(data)
    
    direction = random.choice(directions)

    print "Moving %s" % direction
    return MoveResponse(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    print "Game %s ended" % data["game"]["id"]

def checkWrongDirs(data):
    forbidden_dirs = []
    forbidden_spaces = []
    head = data["you"]["body"][0]
    
    for snakes in data["snakes"]:
        forbidden_spaces.extend(snakes["body"])
    
    #Left
    if forbidden_spaces.contains({
        "x": head["x"] - 1,
        "y": head["y"]
    }):
        forbidden_dirs.extend('left')
    #Right
    if forbidden_spaces.contains({
        "x": head["x"] + 1,
        "y": head["y"]
    }):
        forbidden_dirs.extend('right')
    #Up
    if forbidden_spaces.contains({
        "x": head["x"],
        "y": head["y"] - 1
    }):
        forbidden_dirs.extend('up')
    #Down
    if forbidden_spaces.contains({
        "x": head["x"],
        "y": head["y"] + 1
    }):
        forbidden_dirs.extend('down')
    return forbidden_dirs

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=True)
