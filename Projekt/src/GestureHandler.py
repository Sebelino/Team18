#!/usr/bin/env python

import Gesture as OwnGesture
from kivy.app import App

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.gesture import Gesture, GestureDatabase
import win32api
import win32con

from my_gestures import cross, circle, check, square, s
import Queue

activeTouches = dict()

def simplegesture(name, point_list):
    """
    A simple helper function
    """
    g = Gesture()
    g.add_stroke(point_list)
    g.normalize()
    g.name = name
    return g


def on_touch_down(touch):
    # start collecting points in touch.ud
    touch.scale_for_screen(4096,2400)
    (x,y) = (int(touch.x) ,int(touch.y))
    win32api.SetCursorPos((x, 2400-y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,2400-y,0,0)
    userdata = touch.ud
    userdata['line'] = Line(points=(touch.x, touch.y))
    
    activeTouches.update({touch.uid : {0 : (touch.x, touch.y)}})
    
    return None    #TODO Return actual gesture object

def on_touch_move(touch):
    # store points of the touch movement
    touch.scale_for_screen(4096,2400)
    (x,y) = (int(touch.x) ,int(touch.y))
    print "TAUTTCH!!"+str((x,2400-y))
    win32api.SetCursorPos((x, 2400-y))

    try:
        touch.ud['line'].points += [touch.x, touch.y]
        activeTouches[touch.uid].update({(len(activeTouches[touch.uid])) : (touch.x, touch.y)})
        print activeTouches
    except (KeyError), e:
        pass

    return None    #TODO Return actual gesture object

def on_touch_up(touch):
    touch.scale_for_screen(4096,2400)
    (x,y) = (int(touch.x) ,int(touch.y))
    win32api.SetCursorPos((x, 2400-y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,2400-y,0,0)
    # touch is over, display informations, and check if it matches some
    # known gesture.
    g = simplegesture(
            '',
            zip(touch.ud['line'].points[::2], touch.ud['line'].points[1::2])
            )
    # print the gesture representation, you can use that to add
    # gestures to my_gestures.py
    print "gesture representation:", gdb.gesture_to_str(g)

    gesture = OwnGesture.Gesture("name", False, gdb.gesture_to_str(g))
    
    del activeTouches[touch.uid]
    
    return gesture    #TODO Return actual gesture object







gdb = GestureDatabase()
# add pre-recorded gestures to database
gdb.add_gesture(cross)
gdb.add_gesture(check)
gdb.add_gesture(circle)
gdb.add_gesture(square)
gdb.add_gesture(s)





