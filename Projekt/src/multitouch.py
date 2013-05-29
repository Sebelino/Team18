#!/usr/bin/env python

import Gesture as OwnGesture
import math
from kivy.app import App
from kivy.gesture import Gesture, GestureDatabase
from kivy.uix.floatlayout import FloatLayout
from kivy.base import EventLoop
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse


#Assisting reference points when detecting multi-touch
V2SWIPE_REF = list()
H2SWIPE_REF = list()
ROTATE_REF = list()
PINCH_REF = list()
GTHRESHOLD = 32        #TODO Change according to screen size and resolution
GTHRESHOLD2 = GTHRESHOLD*2


#Compute euclidean distance between two points
def dist((x1,y1),(x2,y2)):
    return ((x1-x2)**2+(y1-y2)**2)**0.5


#Determine the sign of a number
def sign(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        #What kind of sorcery is this?
        return -2


class TouchArea(FloatLayout):

    def draw_refpoints(self):
        #Reference point debugging
        
        global V2SWIPE_REF
        global H2SWIPE_REF
        global ROTATE_REF
        global PINCH_REF
        global GTHRESHOLD
        global GTHRESHOLD2
        
        with self.canvas:
            d = 10
            Color(0, 0, 1)
            Ellipse(pos=(V2SWIPE_REF[0][0] - d / 2, V2SWIPE_REF[0][1] - d / 2), size=(d-3, d+3))
            Ellipse(pos=(V2SWIPE_REF[1][0] - d / 2, V2SWIPE_REF[1][1] - d / 2), size=(d-3, d+3))
            Color(0, 1, 0)
            Ellipse(pos=(H2SWIPE_REF[0][0] - d / 2, H2SWIPE_REF[0][1] - d / 2), size=(d+3, d-3))
            Ellipse(pos=(H2SWIPE_REF[1][0] - d / 2, H2SWIPE_REF[1][1] - d / 2), size=(d+3, d-3))
            Color(1, 0, 0)
            Ellipse(pos=(ROTATE_REF[0][0] - d / 2, ROTATE_REF[0][1] - d / 2), size=(d, d))
            Ellipse(pos=(ROTATE_REF[1][0] - d / 2, ROTATE_REF[1][1] - d / 2), size=(d, d))
            Color(1, 1, 0)
            Ellipse(pos=(PINCH_REF[0][0] - d / 2, PINCH_REF[0][1] - d / 2), size=(d, d))
            Ellipse(pos=(PINCH_REF[1][0] - d / 2, PINCH_REF[1][1] - d / 2), size=(d, d))


    def on_touch_down(self, touch):

        #The moment you have two touch points: use their locations as references.
        if len(EventLoop.touches) == 2:
            global V2SWIPE_REF
            global H2SWIPE_REF
            global ROTATE_REF
            global PINCH_REF
            global GTHRESHOLD
            global GTHRESHOLD2
            
            print "Two touch points down"
            t = EventLoop.touches
            V2SWIPE_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)]
            H2SWIPE_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)]
            ROTATE_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)]
            PINCH_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)]
        
            #self.draw_refpoints()
        
        return None


    def on_touch_move(self, touch):
        
        g = None

        if len(EventLoop.touches) == 2:
            global V2SWIPE_REF
            global H2SWIPE_REF
            global ROTATE_REF
            global PINCH_REF
            global GTHRESHOLD
            global GTHRESHOLD2
            
            t = EventLoop.touches

            #Check if qualified for horizontal two-point swipe
            if (abs(dist(t[0].pos,t[1].pos)-dist(H2SWIPE_REF[0],H2SWIPE_REF[1])) < GTHRESHOLD and sign(t[0].x-H2SWIPE_REF[0][0]) != -sign(t[1].x-H2SWIPE_REF[1][0])):
                
                #print "Qualified for horizontal two-point swipe"
                
                #Check if movement is sufficiently large
                if t[0].x - H2SWIPE_REF[0][0] > GTHRESHOLD2 and t[1].x - H2SWIPE_REF[1][0] > GTHRESHOLD2:
                    #Swipe to the right detected. Generate gesture and update the reference point.
                    g = OwnGesture.Gesture("2pswipe right", True, "2pswipe right")
                    H2SWIPE_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)]
                    
                elif t[0].x - H2SWIPE_REF[0][0] < -GTHRESHOLD2 and t[1].x - H2SWIPE_REF[1][0] < -GTHRESHOLD2:
                    #Swipe to the left detected. Generate gesture and update the reference point.
                    g = OwnGesture.Gesture("2pswipe left", True, "2pswipe left")
                    H2SWIPE_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)]
                
                #Otherwise, don't update the reference point
            else:
                H2SWIPE_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)] #Update reference point.
                #print "Disqualified from horizontal two-point swipe"



            #Check if qualified for vertical two-point swipe
            if (abs(dist(t[0].pos,t[1].pos)-dist(V2SWIPE_REF[0],V2SWIPE_REF[1])) < GTHRESHOLD and sign(t[0].y-V2SWIPE_REF[0][1]) != -sign(t[1].y-V2SWIPE_REF[1][1])):
            
                #print "Qualified for vertical two-point swipe"
            
                #Check if movement is sufficiently large
                if t[0].y - V2SWIPE_REF[0][1] > GTHRESHOLD2 and t[1].y - V2SWIPE_REF[1][1] > GTHRESHOLD2:
                    #Swipe upwards detected. Generate gesture and update the reference point.
                    g = OwnGesture.Gesture("2pswipe up", True, "2pswipe up")
                    V2SWIPE_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)]
                    
                elif t[0].y - V2SWIPE_REF[0][1] < -GTHRESHOLD2 and t[1].y - V2SWIPE_REF[1][1] < -GTHRESHOLD2:
                    #Swipe downwards detected. Generate gesture and update the reference point.
                    g = OwnGesture.Gesture("2pswipe down", True, "2pswipe down")
                    V2SWIPE_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)]

                #Otherwise, don't update the reference point
            else:
                V2SWIPE_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)] #Change it
                #print "Disqualified from vertical two-point swipe"

            #Check if qualified for rotation
            if abs(dist(t[0].pos,t[1].pos)-dist(ROTATE_REF[0],ROTATE_REF[1])) < GTHRESHOLD and sign(t[0].x-ROTATE_REF[0][0]) != sign(t[1].x-ROTATE_REF[1][0]) and sign(t[0].x-ROTATE_REF[0][0]) != sign(t[1].x-ROTATE_REF[1][0]):
                
                totd = dist(t[0].pos, ROTATE_REF[0]) + dist(t[1].pos, ROTATE_REF[1])
                
                da = math.atan2(t[0].y-t[1].y, t[0].x-t[1].x)
                aa1 = math.atan2(t[0].y-ROTATE_REF[0][1], t[0].x-ROTATE_REF[0][0])
                aa2 = math.atan2(t[1].y-ROTATE_REF[1][1], t[1].x-ROTATE_REF[1][0])

                ra1 = math.fmod((da-aa1+4*math.pi),2*math.pi)
                ra2 = math.fmod((da-aa2+4*math.pi),2*math.pi)
                
                print "Qualified for rotation"
                
                '''
                print "da: " + str(da)
                
                print "aa1: " + str(aa1)
                print "aa2: " + str(aa2)
                
                print "ra1: " + str(ra1)
                print "ra2: " + str(ra2)
                
                print "totd: " + str(totd)
                '''
                
                #Check if movement is sufficiently large
                if totd > GTHRESHOLD2 and (ra1 < math.pi or aa1 == 0.0) and (ra2 > math.pi or aa2 == 0.0):
                    #Rotation clockwise detected. Generate gesture and update the reference point.
                    g = OwnGesture.Gesture("rotation cw", True, "rotation cw")
                    ROTATE_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)]
                    
                elif totd > GTHRESHOLD2 and (ra1 > math.pi or aa1 == 0.0) and (ra2 < math.pi or aa2 == 0.0):
                    #Rotation counterclockwise detected. Generate gesture and update the reference point.
                    g = OwnGesture.Gesture("rotation ccw", True, "rotation ccw")
                    ROTATE_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)]

                #Otherwise, don't update the reference point
            else:
                print "Disqualified for rotation"
                ROTATE_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)]  #Change it


            #Check if qualified for pinch
            if abs(dist(t[0].pos,t[1].pos)-dist(PINCH_REF[0],PINCH_REF[1])) > GTHRESHOLD2:
                
                if dist(t[0].pos,t[1].pos)-dist(PINCH_REF[0],PINCH_REF[1]) > GTHRESHOLD2:
                    #Pinch outwards detected. Generate gesture and update the reference point.
                    g = OwnGesture.Gesture("pinch out", True, "pinch out")
                    PINCH_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)]
                
                elif dist(t[0].pos,t[1].pos)-dist(PINCH_REF[0],PINCH_REF[1]) < -GTHRESHOLD2:
                    #Pinch inwards detected. Generate gesture and update the reference point.
                    g = OwnGesture.Gesture("pinch in", True, "pinch in")
                    PINCH_REF = [(t[0].x,t[0].y),(t[1].x,t[1].y)]

            #self.draw_refpoints()

        if g != None:
            print "     ###\n" + g.stringRepresentation + "\n     ###"
        return g


    def on_touch_up(self, touch):
        
        if len(EventLoop.touches) < 2:
            global V2SWIPE_REF
            global H2SWIPE_REF
            global ROTATE_REF
            global PINCH_REF
            #Clear multi-touch reference points
            V2SWIPE_REF = []
            H2SWIPE_REF = []
            ROTATE_REF = []
            PINCH_REF = []

        return None    #TODO Return actual gesture object


class MultitouchDetector(App):
    def build(self):
        return TouchArea()

if __name__ == '__main__':
    print "Running MultitouchDetector!"
    MultitouchDetector().run()



