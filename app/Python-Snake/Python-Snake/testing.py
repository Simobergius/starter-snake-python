import snake
import test_data
import time
import sys

def doTest(test, expected):
    print("Starting test case %s" % str(test))
    snake_under_test = snake.snake(False)
    start_time = time.time()
    try:
        result = test(snake_under_test)
    except:
        result = sys.exc_info()[1]
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

def test52(snake):
    return snake.doAction(test_data.data52)

def test53(snake):
    return snake.doAction(test_data.data53)

def test54(snake):
    return snake.doAction(test_data.data54)

def test6(snake):
    return snake.doAction(test_data.data6)

def test7(snake):
    return snake.doAction(test_data.data7)

#doTest(test, ['right'])
#doTest(test2, ['right'])
#doTest(test3, ['up','down'])
#doTest(test4, ['down'])
#doTest(test5, ['down', 'left', 'right'])
#doTest(test52, ['down', 'up', 'right'])
#doTest(test53, ['up', 'left', 'right'])
#doTest(test54, ['down', 'left', 'up'])
#doTest(test6, ['up'])
doTest(test7, ['left'])
