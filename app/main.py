import bottle
import os
import random
import json
import pprint
import snake

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
    return StartResponse("#00ffff")


@bottle.post('/move')
def move():
    data = bottle.request.json
    # TODO: Do things with data
    direction = snake.doAction(data)

    print "Moving %s" % direction
    return MoveResponse(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data
    print json.dumps(len(data["you"]["body"]), sort_keys=True, indent=4)

    print "Game %s ended" % data["game"]["id"]
    
# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
snake = snake.snake()
if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=True)
