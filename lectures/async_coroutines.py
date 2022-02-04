from inspect import getgeneratorstate


# корутины (декоратор, который позволяет избежать отправки None)

##############
def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner
##############

class ExampleException(Exception):
    pass

@coroutine
def get_average():
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print('Done')
            break
        except ExampleException:
            print(".................")
            break
        else:
            count += 1
            summ += x
            average = round(summ / count, 2)
            print(average)

    return average                  # если выпадет ошибка, то отдастся последний результат


g = get_average()
# g.send(None)            # запускаем генератор    с декоратором coroutine НЕ НУЖНО
print(getgeneratorstate(g))
g.send(1)
g.send(10)
g.send(9)
g.throw(StopIteration)
# g.throw(ExampleException)

####################

