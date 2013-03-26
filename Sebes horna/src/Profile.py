#!/usr/bin/python

class Profile:
    def __init__(self):
        self.name = "(Unnamed)"
        self.map = dict()    # Contains gesture -> command pairs.

    def addMapping(self,gesture,command):
        self.map[gesture] = command

    def get(self,gesture):
        return self.map[gesture]

    def getSimilar(self,gesture):
        return self.map[gesture]
