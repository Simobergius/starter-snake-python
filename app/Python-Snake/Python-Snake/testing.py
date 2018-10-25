import snake

data = {
    'board': {
        'snakes': [
            {'body': [
                {'x': 5, 'y': 5}, 
                {'x': 5, 'y': 6},
                {'x': 4, 'y': 6},
                {'x': 3, 'y': 6},
                {'x': 3, 'y': 5},
                {'x': 3, 'y': 4},
                {'x': 4, 'y': 4},
                {'x': 5, 'y': 4},
                {'x': 6, 'y': 4},
                {'x': 7, 'y': 4}
               ], 
               'health': 100,
               'id': 'testsnake',
               'length': 10,
               'name': 'testsnake',
               'object': 'snake'
            }
        ],
        'height': 10,
        'width': 10,
        'food': [
                {'x': 2, 'y': 2},
        ]
    },
    'you': {
        'body': [
            {'x': 5, 'y': 5}, 
            {'x': 5, 'y': 6},
            {'x': 4, 'y': 6},
            {'x': 3, 'y': 6},
            {'x': 3, 'y': 5},
            {'x': 3, 'y': 4},
            {'x': 4, 'y': 6},
            {'x': 5, 'y': 6},
            {'x': 6, 'y': 6},
            {'x': 7, 'y': 6}
        ], 
        'health': 100,
        'id': 'testsnake',
        'length': 10,
        'name': 'testsnake',
        'object': 'snake'
    }
}        
        
#interface World {
#  object: 'world';
#  id: number;
#  you: Snake;
#  snakes: List<Snake>;
#  height: number;
#  width: number;
#  turn: number;
#  food: List<Point>;
#}
snake = snake.snake()

print(snake.doAction(data))