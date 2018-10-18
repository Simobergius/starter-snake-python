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
    
    direction = random.choice(directions)

    print "Moving %s" % direction
    return MoveResponse(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data
    print json.dumps(data, sort_keys=True, indent=4)

    print "Game %s ended" % data["game"]["id"]

def checkWrongDirs(data):
    forbidden_dirs = []
    forbidden_spaces = []
    head = data["you"]["body"][0]
    
    for snakes in data["board"]["snakes"]:
        forbidden_spaces.extend(snakes["body"])
    
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

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=True)
