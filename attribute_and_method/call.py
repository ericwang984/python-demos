

# Demo A: Custom function is callable. It can be called by __call__() method.

def test():
    print("Function test() is called")

print("Demo A:")
print("Function test() is callable: %s" % callable(test))
test()
test.__call__()

'''
Function test() is callable: True
Function test() is called
Function test() is called
'''


# Demo B: Python build-in functions are callable. It can be called by __call__() method.

print("Demo B:")
print("Build-in function int() is callable: %s" % callable(int))
print(int(3))
print(int.__call__(3))
'''
Build-in function int() is callable: True
3
3
'''

# Demo C: Instance object is not callable if __call__() method is not defined.
class Person(object):
    pass

print("Demo C:")
c = Person()
print("Object c is callable: %s" % callable(c))

'''
Object c is callable: False
'''

# Demo D: Instance object is callable if __call__() method is defined.
class Person(object):

    def __call__(self):
        print("Method __call__() is called")

print("Demo D:")
d = Person()
print("Object d is callable: %s" % callable(d))
d()

'''
Object d is callable: True
Method __call__() is called
'''

# __call__() function usecases:

# Validator
class Validator(object):
    def __call__(self, value):
        return True if len(value) > 3 else False

print("Demo E:")
r = Validator()
print(r("aa"))
print(r("aaaaaa"))
'''
False
True
'''

# Decorator

class ClsDeco:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(f'Running {self.func.__name__}')
        self.func()
        print('End')

@ClsDeco  # 等价于 bar = ClsDeco(bar)
def foo():
    print('do something')

print("Demo F:")
foo()

'''
Running foo
do something
End
'''

