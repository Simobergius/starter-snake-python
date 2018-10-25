import snake
import test_data

def doTest(test, expected):
    print("Starting test case")
    snake_under_test = snake.snake(False)
    result = test(snake_under_test)
    if not result in expected:
        print("TEST FAIL!: expected '%s' Got: '%s'" % (expected, result))
    else:
        print("TEST PASS!")

def test(snake):
    return snake.doAction(test_data.data1)

def test2(snake):
    return snake.doAction(test_data.data2)

def test3(snake):
    return snake.doAction(test_data.data3)



#doTest(test, ['right'])
#doTest(test2, ['right'])
doTest(test3, ['up','down'])

