import bottle
import os
import random
import json
import pprint
import snake
import time
import sys
import filewriter

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
    # TODO: Add snakes dynamically

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data
    # TODO: Add new filewriter in case where multiple snakes are required/requested
    
    writer.setDir(["results", str(data["game"]["id"]), str(data["you"]["id"])])

    print("Starting game %s" % data["game"]["id"])
    print("Snake id: %s" % data["you"]["id"])
    print(json.dumps(data, sort_keys=True, indent=4))
    return StartResponse(argcolor)


@bottle.post('/move')
def move():
    data = bottle.request.json
    # TODO: Do things with data
    # TODO: Write to file in different thread
    try:
        direction = snek.doAction(data)
    except:
        e = sys.exc_info()[1]
        writeFile(str(e) + "_" + str(data["turn"]), json.dumps(data, sort_keys=True, indent=4))



    print("Moving %s" % direction)
    return MoveResponse(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    #Write data to file
    writeFile("end", json.dumps(data, sort_keys=True, indent=4))

    print("Final length: %i" % len(data["you"]["body"]))

    print("Game %s ended" % data["game"]["id"])
    
def writeFile(filename, data):
    writer.write(filename, data)

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
argcolor = '#0000ff'
argport = '8080'
for i, arg in enumerate(sys.argv):
    if arg == '-c':
        if len(sys.argv) > i:
            argcolor = '#%s' % sys.argv[i + 1]
        else:
            print("Please give a color value")
    if arg == '-p':
        if len(sys.argv) > i:
            argport = sys.argv[i + 1]

snek = snake.snake(True)
writer = filewriter.FileWriter()
if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', argport),
        debug=True)
