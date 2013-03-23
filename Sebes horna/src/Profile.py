#!/usr/bin/python

class Profile:
    def __init__(self):
        self.name = "(Unnamed)"
        self.map = dict()    # Contains gesture -> command pairs.

    def addMapping(gesture,command):
        map[gesture] = command

    def getSimilar(gesture):
        return map[gesture]
