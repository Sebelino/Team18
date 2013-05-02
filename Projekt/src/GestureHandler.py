#!/usr/bin/env python

import Gesture as OwnGesture
from kivy.app import App

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.gesture import Gesture, GestureDatabase

from my_gestures import cross, circle, check, square, s
import Queue

def simplegesture(name, point_list):
    """
    A simple helper function
    """
    g = Gesture()
    g.add_stroke(point_list)
    g.normalize()
    g.name = name
    return g


def on_touch_down(self, touch):
    # start collecting points in touch.ud
    # create a line to display the points
    userdata = touch.ud
    with self.canvas:
        Color(1, 1, 0)
        d = 30.
        Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d, d))
        userdata['line'] = Line(points=(touch.x, touch.y))
    return None    #TODO Return actual gesture object

def on_touch_move(self, touch):
    # store points of the touch movement
    try:
        touch.ud['line'].points += [touch.x, touch.y]
        return True
    except (KeyError), e:
        pass

    return None    #TODO Return actual gesture object

def on_touch_up(self, touch):
    # touch is over, display informations, and check if it matches some
    # known gesture.
    g = simplegesture(
            '',
            zip(touch.ud['line'].points[::2], touch.ud['line'].points[1::2])
            )
    # print the gesture representation, you can use that to add
    # gestures to my_gestures.py
    print "gesture representation:", gdb.gesture_to_str(g)

    gesture = OwnGesture.Gesture(gdb.gesture_to_str(g))

    # erase the lines on the screen, this is a bit quick&dirty, since we
    # can have another touch event on the way...
    self.canvas.clear()
    
    return gesture    #TODO Return actual gesture object







gdb = GestureDatabase()
# add pre-recorded gestures to database
gdb.add_gesture(cross)
gdb.add_gesture(check)
gdb.add_gesture(circle)
gdb.add_gesture(square)
gdb.add_gesture(s)





