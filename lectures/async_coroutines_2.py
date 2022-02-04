def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


class ExampleException(Exception):
    pass

# делегирующий генератора - это генератора, который вызывает другой генератор (когда нам нужно один генератор разбить на несколько)
# подгенератор - вызываемый генератор


def subgen():
    for i in 'name':
        yield i


def delegator(g):
    for i in g:
        yield i


sg = subgen()
d = delegator(sg)

print(next(d))
print(next(d))
print(next(d))
print(next(d))

##########################


# @coroutine
def subgen():
    while True:
        try:
            message = yield
        except ExampleException:
            print('ExampleException')
        else:
            print('.........', message)


@coroutine
def delegator(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except ExampleException as e:
    #         g.throw(e)
    yield from g


sg = subgen()
d = delegator(sg)
d.send('ok')
d.send('is')
d.throw(ExampleException)

# yield from заменяет цикл в делегирующем генераторе и берет на себя передачу данных в подгенератор
# делегирующий генератор остается заблокированным, пока пожгенератор не закончит свою работу


####
def a():
    yield from 'name'


g = a()
print(next(g))
print(next(g))
####
