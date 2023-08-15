from abc import ABC, abstractmethod
from x import y

class Vehicle(ABC):
    def __init__(self, name):
        self.name = name
        self.value

    @abstractmethod
    def run(self):
        pass

class Car(Vehicle):
    def run(self):
    	class Runner:
        	pass
        return "Car is running"

@decorate
class Motorcycle(Vehicle):
    def run(self):
        return "Motorcycle is running"

@decorator1
@decorator2(arg1, arg2)
@decorator3.decorate()
@decorator3.decorate().decorate2(arg1)
def run(vehicle1, vehicle2):
    x = 5
    print('start')
    vehicle1.run()
    print('stop')

vehicle = Car()
run(vehicle)