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
    print "You:"
    print json.dumps(data["you"], sort_keys=True, indent=4)
    # TODO: Do things with data
    
    head = data["you"]["body"][0]
    next_from_head = data["you"]["body"][1]
    
    if next_from_head.x > head.x:
        #Dont go right
        forbidden_dir = 'right'
    elif next_from_head.x < head.x:
        #Dont go left
        forbidden_dir = 'left'
    elif next_from_head.y > head.y:
        #Dont go down
        forbidden_dir = 'down'
    elif next_from_head.y < head.y:
        #Dont go up
        forbidden_dir = 'up'
        
    directions = ['up', 'down', 'left', 'right']
    directions.remove(forbidden_dir)
    direction = random.choice(directions)
    direction == forbidden_dir

    print "Moving %s" % direction
    return MoveResponse(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    print "Game %s ended" % data["game"]["id"]


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=True)
