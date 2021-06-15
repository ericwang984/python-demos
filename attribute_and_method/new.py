
# How __new__ function works?

# Demo A: Call __new__ befor __init__
class Person(object):
    
    def __new__(cls):
        print("__new__ called")
        return super().__new__(cls)
    
    def __init__(self):
        print("__init__ called")

print("Demo A:")     
a = Person()
'''
__new__ called
__init__ called
'''

# Demo B: __new__ returns a current class instance and pass it to 'self' of the __init__
class Person(object):
    
    def __new__(cls):
        print("__new__ called")
        instance = super().__new__(cls)
        print(type(instance))
        print(instance)
        print(id(instance))
        return instance
    
    def __init__(self):
        print("__init__ called")
        print(id(self))

print("Demo B:")
b = Person()
'''
__new__ called
<class '__main__.Person'>
<__main__.Person object at 0x1093c1580>
4449899904
__init__ called
4449899904
'''

# Demo C: If __new__ return None, __init__ will not be called.
class Person(object):
    
    def __new__(cls):
        print("__new__ called")

    def __init__(self):
        print("__init__ called")

print("Demo C:")
c = Person()
'''
__new__ called
'''

# Demo D: If __new__ return an instance of other class, __init__ will never be called.
# And __new__ will init an instance of other class.
class Animal(object):

    def __init__(self):
        pass

class Person(object):
    
    def __new__(cls):
        print("__new__ called")
        return Animal()

    def __init__(self):
        print("__init__ called")

print("Demo D:")
d = Person()
print(type(d))
print(d)
'''
__new__ called
<class '__main__.Animal'>
<__main__.Animal object at 0x10fea3550>
'''

# Demo E: If __new__ does not accept parameters apart form cls, 
# we can not set varialbes when init the instance 
class Person(object):
    
    def __new__(cls):
        print("__new__ called")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, name):
        print("__init__ called")
        self.name = name

# print("Demo E:")
# e = Person("Eric")
# print(e.name)
'''
Traceback (most recent call last):
  File "new.py", line 102, in <module>
    e = Person("Eric")
TypeError: __new__() takes 1 positional argument but 2 were given
'''

# Demo F: So if we want to rewrite __new__ function, have to set "*args,**kwargs" as parameters of 
# __new__function, or specific parameters we need.
class Person(object):
    
    def __new__(cls, *args,**kwargs):  # Or def __new__(cls, name)
        print("__new__ called")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, name):
        print("__init__ called")
        self.name = name

print("Demo E:")
f = Person("Eric")
print(f.name)
'''
__new__ called
__init__ called
Eric
'''


# Use cases for __new__ function

# Demo G: Custom metaclass

class PersonMetaClass(type):
    # name: the class name
    # bases: a tuple of the base classes from which the class inherits.
    # attrs: a dictionary containing attributes of the class. It becomes
    # the __dict__ attribute of the class.
    def __new__(cls, name, bases, attrs):
        attrs['sex'] = ['male', 'female']
        return super().__new__(cls, name, bases, attrs)

class Person(object, metaclass=PersonMetaClass):
    pass

print("Demo G:")
g = Person()
print(g.sex) 
'''
['male', 'female']
'''

#Demo H: Another way to custom attributes in metaclass
class PersonMetaClass(type):
    
    def __new__(cls, name, bases, attrs):
        x = super().__new__(cls, name, bases, attrs)
        x.sex = ['male', 'female']
        return x

class Person(object, metaclass=PersonMetaClass):
    pass

print("Demo H:")
h = Person()
print(h.sex)
'''
['male', 'female']
'''

# Demo I: Singleton with __new__() method

class SinglePerson(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        pass
print("Demo I:")
i1 = SinglePerson()
i2 = SinglePerson()
print(id(i1))
print(id(i2))
'''
4447074768
4447074768
'''

# Demo J: Factory with __new__() method

class Teacher(object):
    title = 'teacher'

class Student(object):
    title = 'student'


class PersonFactory(object):

    person = {'teacher': Teacher, 'student': Student }

    def __new__(cls, name):
        if name in cls.person.keys():
            return cls.person[name]()
        return None

j1 = PersonFactory("teacher")
print(j1.title)
j2 = PersonFactory("student")
print(j2.title)
'''
teacher
student
'''
