
# What is MetaClass

# Demo A: a sample MetaClass without any functionality
# A class is an instance of a metaclass
class PersonMeta(type):
    
    def __new__(cls, clsname, superclasses, attributedict):
        print("clsname:", clsname)
        print("superclasses:", superclasses)
        print("attrdict:", attributedict)
        return super().__new__(cls, \
                       clsname, superclasses, attributedict)
  
print("Demo A:")
class Person(object, metaclass=PersonMeta):
    pass

print("Person is the instance of PersonMeta: %s" % isinstance(Person, PersonMeta))
print("Class Person's metaclass is: %s" % Person.__class__)

'''
clsname: Person
superclasses: (<class 'object'>,)
attrdict: {'__module__': '__main__', '__qualname__': 'Person'}
Person is the instance of PersonMeta: True
Class Person's metaclass is: <class '__main__.PersonMeta'>
'''

# Metaclass inheritance

# Demo B: `type` is the base metaclass. A class's metaclass is `type` by default
# if it doesn't specify metaclass when it is created.

class C1:
    pass

print("Demo B:")
print("Class C1's metaclass is: %s" % C1.__class__)
print("Class C1's base class is: %s" % C1.__bases__)

'''
Class C1's metaclass is: <class 'type'>
Class C1's base class is: <class 'object'>
'''

# Demo C: When a class inherits from another class, they share same metaclass.

class Meta1(type):
    pass

class C1(metaclass=Meta1):
    pass

class C2(C1):
    pass

print("Demo C:")
print("Class C1's metaclass is: %s" % C1.__class__)
print("Class C2's metaclass is: %s" % C2.__class__)

'''
Class C1's metaclass is: <class '__main__.Meta1'>
Class C2's metaclass is: <class '__main__.Meta1'>
'''

# Demo D: One class can only have one metaclass. If a class inherits from two classes
# which share different metaclass, it gets a ”metaclass conflict“ error.

class Meta1(type):
    pass

class Meta2(type):
    pass

class C1(metaclass=Meta1):
    pass

class C2(metaclass=Meta2):
    pass

# class C3(C1, C2):
#     pass

print("Demo D:")
'''
TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its base
'''

# Demo E: If one class inhertis from two classes which share different metaclasses, it will get 
# the metaclass that has lower level.

class Meta1(type):
    pass

class Meta2(Meta1):
    pass

class C1(metaclass=Meta1):
    pass

class C2(metaclass=Meta2):
    pass

class C3(C1, C2):
    pass

print("Demo E:")
print("Class C1's metaclass is: %s" % C1.__class__)
print("Class C2's metaclass is: %s" % C2.__class__)
print("Class C3's metaclass is: %s" % C3.__class__)

'''
Class C1's metaclass is: <class '__main__.Meta1'>
Class C2's metaclass is: <class '__main__.Meta2'>
Class C3's metaclass is: <class '__main__.Meta2'>
'''


# Demo F: Another syntax of creating a class

# Normal way:
class Person1(object):

    def __init__(self, age):
        self._age = age

    def get_age(self):
        return self._age

# type syntax:
def init(self, age):
    self._age = age

def get_age(self):
    return self._age

# The first argument is a string – for class name.
# The second argument is a tuple – base classes.
# The third argument is a dictionary - class attributes.
Person2 = type('Person2', (object,), {
    '__init__': init,
    'get_age': get_age
})

print("Demo F:")
p1 = Person1(15)
print("p1's age is: %d" % p1.get_age())
p2 = Person2(20)
print("p2's age is: %d" % p2.get_age())

'''
p1's age is: 15
p2's age is: 20
'''

# Demo G: Generate class dynamically

class_names = ["Person1", "Person2"]

def init(self, age):
    self._age = age

def get_age(self):
    return self._age

for class_name in class_names:
    globals()[class_name] = \
        type(class_name, (object,), {
            '__init__': init,
            'get_age': get_age
        })

print("Demo G:")
p1 = Person1(25)
print("p1's age is: %d" % p1.get_age())
p2 = Person2(30)
print("p2's age is: %d" % p2.get_age())
'''
p1's age is: 25
p2's age is: 30
'''


# Metaclass usecases

# Demo I: Class Verification

class PersonMeta(type):
    def __new__(cls, name, bases, attrs):
        if 'last_name' in attrs and 'family_name' in attrs:
            raise TypeError("Class %s cannot contain both last_name and \
family_name attributes." % name)
        if 'last_name' not in attrs and 'last_name' not in attrs:
            raise TypeError('Class %s must provide either a last_name \
attribute or a family_name attribute.' % name)
        else:
            print('Success')
              
        return super(PersonMeta, cls).__new__(cls, name, bases, attrs)
  
print("Demo I:")
class Person(metaclass = PersonMeta):
    last_name = "Hello"
    family_name = "World"
    
p = Person()
'''
Traceback (most recent call last):
  File "metaclass.py", line 195, in <module>
    class Person(metaclass = PersonMeta):
  File "metaclass.py", line 184, in __new__
    raise TypeError("Class %s cannot contain both last_name and \
TypeError: Class Person cannot contain both last_name and family_name attributes.
'''


# Demo J: Prevent  inheriting the attributes

class PersonMeta(type):
    def __new__(cls, name, bases, attrs):
        # If abstract class, then skip the metaclass function
        if attrs.pop('abstract', False):
            print('Abstract Class:', name)
            return super(PersonMeta, cls).__new__(cls, name, bases, attrs)
        # metaclass functionality
        if 'last_name' in attrs and 'family_name' in attrs:
            raise TypeError("Class %s cannot contain both last_name and \
family_name attributes." % name)
        if 'last_name' not in attrs and 'last_name' not in attrs:
            raise TypeError('Class %s must provide either a last_name \
attribute or a family_name attribute.' % name)
        print('Normal Class:', name)
        return super(PersonMeta, cls).__new__(cls, name, bases, attrs)

print("Demo J:")
class AbsCls(metaclass = PersonMeta):
	abstract = True
	
class NormCls(metaclass = PersonMeta):
	last_name = "Hello"

'''
Abstract Class: AbsCls
Normal Class: NormCls
'''

# Demo K: Singleton


class SingletonMeta(type):
    def __init__(self,*args,**kwargs):
        print("MetaClass __init__() is executed.")
        self.__instance = None
        super().__init__(*args,**kwargs)
        
    def __call__(self, *args, **kwargs):
        print("MetaClass __call__() is executed.")
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
        return self.__instance
 
print("Demo K:")
print("Generate Singleton class by calling __init__() in the MetaClass")
class Singleton(metaclass=SingletonMeta):
    pass

print("Generate objects s1 and s2 by calling __call__() in the MetaClass")
s1 = Singleton()
s2 = Singleton()
print(s1 is s2)

'''
Generate Singleton class by calling __init__() in the MetaClass
MetaClass __init__() is executed.
Generate objects s1 and s2 by calling __call__() in the MetaClass
MetaClass __call__() is executed.
MetaClass __call__() is executed.
True
'''

# Demo L: ORM

class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.colmun_type = column_type
 
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)
 
class StringField(Field):
    def __init__(self, name):
        super().__init__(name, 'varchar(100)')
 
class IntegerField(Field):
    def __init__(self, name):
        super().__init__(name, 'bigint')
 
class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return super().__new__(cls, name, bases, attrs)
        mappings = dict()
        for k,v in attrs.items():
            if isinstance(v,Field):
                print('Found mapping:%s==>%s' % (k, v))
                mappings[k] = v
        for k in mappings.keys(): 
            attrs.pop(k)
        attrs['__table__'] = name.lower()  
        attrs['__mappings__'] = mappings 
        return super().__new__(cls, name, bases, attrs)
 

class Model(dict, metaclass=ModelMetaClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'Model' object has no attribute '%s'" % key)
    def __setattr__(self, key, value):
        self[key] = value
 
    def save(self):
        fields = []
        params = []
        args = []
        for k,v in self.__mappings__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self,k,None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__,','.join(fields),','.join(params))
        print('SQL:%s' % sql)
        print('ARGS:%s' % str(args))
 

print("Demo L:")
class User(Model):
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')

user = User(id=1,name='Job',email='job@test.com',password='pw')
user.save()

'''
Found mapping:id==><IntegerField:id>
Found mapping:name==><StringField:username>
Found mapping:email==><StringField:email>
Found mapping:password==><StringField:password>
SQL:insert into user (id,username,email,password) values (?,?,?,?)
ARGS:[1, 'Job', 'job@test.com', 'pw']
'''