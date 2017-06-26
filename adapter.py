class Person(object):

    def __init__(self, name):
        self.name = name

    def say(self):
        print 'the person say hello'

    def __string__(self):
        return '<Person: %s>' % self.name


class Dog(object):

    def __init__(self, name):
        self.name = name

    def shout(self):
        print 'Dog wang wang ~~'


    def __string__(self):
        return '<Dog: %s>' % self.name


class Car(object):

    def __init__(self, name):
        self.name = name

    def blow(self):
        print 'Car bi bi bi '


    def __str__(self):
        return '<Car %s>' % self.name


class Adapter(object):

    def __init__(self, obj, adapted_methods):
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __string__(self):
        return str(self.obj)


if __name__ == '__main__':
    objects = [Person('Frank AK')]
    dog = Dog('Luck')
    objects.append(Adapter(dog, dict(say=dog.shout)))
    car = Car('Jeep')
    objects.append(Adapter(car, dict(say=car.blow)))

    for i in objects:
        #all have the same method 
        i.say()
