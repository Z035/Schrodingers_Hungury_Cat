def gen_func(x, y):
    for i in range(x):
        yield i + y
    while True:
        yield 'Nothing left'


def gen_gen_func(y):
    for i in range(y):
        yield gen_func(5, i)


generator_generator = gen_gen_func(5)
generator1 = next(generator_generator)
generator2 = next(generator_generator)

print(next(generator1))
print(next(generator1))
print(next(generator1))
print(next(generator1))
print('')
print(next(generator2))
print(next(generator2))
print(next(generator2))
print(next(generator2))
