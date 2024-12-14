#!/usr/bin/env python3

def announce(fun):
    def wrapper():
        print(f"Running Function {fun.__name__} ")
        fun()
        print(f"Done Running Function {fun.__name__}")
    return wrapper

@announce
def use_decor():
    print("This is a function to practice decorators")

people = [
    {"Name":"APerson","House":"AHouse"},
    {"Name":"CPerson","House":"CHouse"},
    {"Name":"BPerson","House":"BHouse"}

]
i = 0
def fun(obj):
    i += 1
    if i > 2:
        exit(1)
    print(obj)
    return obj["Name"]
people.sort(key=fun)
print(people)