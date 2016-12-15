from abc import ABCMeta, abstractmethod

class Frontend(metaclass=ABCMeta):
    """ This is an interface for a frontend object so that various
    frontends can be hooked up."""

    def __init__(self):
        return

    @abstractmethod
    def display(self, info):
        raise NotImplementedError("This is an interface!")

    @abstractmethod
    def input(self, prompt):
        raise NotImplementedError("This is an interface!")



class ConsoleFrontend(Frontend):
    def display(self, info):
        print(info)

    def input(self, prompt):
        return input(prompt + " ")

class ApplescriptFrontend(Frontend):
    pass


class LuaFrontend(Frontend):
    pass

class SmsFrontend(Frontend):
    pass



c = ConsoleFrontend()
try:
    l = LuaFrontend()
    print("Uh oh. This should throw an error because abstract methods aren't defined.")
except TypeError:
    print("Good! Abstract methods work!")

c.display("Hello, world")
c.input("Where are you?")
c.display(c.input("How are you?"))

