import snake
import test_data
import time

def doTest(test, expected):
    print("Starting test case")
    snake_under_test = snake.snake(False)
    start_time = time.time()
    result = test(snake_under_test)
    if not result in expected:
        print("TEST FAIL!: expected '%s' Got: '%s'" % (expected, result))
    else:
        print("TEST PASS! Elapsed time: %f milliseconds" % ((time.time() - start_time) * 1000))

def test(snake):
    return snake.doAction(test_data.data1)

def test2(snake):
    return snake.doAction(test_data.data2)

def test3(snake):
    return snake.doAction(test_data.data3)

def test4(snake):
    return snake.doAction(test_data.data4)

def test5(snake):
    return snake.doAction(test_data.data5)


doTest(test, ['right'])
doTest(test2, ['right'])
doTest(test3, ['up','down'])
doTest(test4, ['down'])
doTest(test5, ['down', 'left', 'right'])
