class Dog:
    def __init__(self):
        print("Wang Wang Wang")


class Cat:
    def __init__(self):
        print("Miao Miao Miao")


def fac(animal):
    if animal.lower() == "dog":
        return Dog()
    if animal.lower() == "cat":
        return Cat()
    print("对不起，必须是：dog,cat")