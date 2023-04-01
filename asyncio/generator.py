

#if a function contains a yield then it becomes a generator function
def generator():
    print("a")
    yield 1
    print("b")
    yield 2
    print("c")
    yield 3

#calling a generator function does not execute it. A generator object is returned.
generator_object = generator()

#next can be called to run the generator function up to the next yield, returning the value
print(next(generator_object))
#a
#1
print(next(generator_object)) #2
#b
#2
print(next(generator_object)) #3
#c
#3

#a generator object is iteratable
for value in generator():
    print(value)