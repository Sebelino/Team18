#!/usr/bin/env python

import win32api, win32con
import time

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.core.window import Window
#from kivy.gesture import Gesture, GestureDatabase

#Set screen size before running the application
ASPECT_RATIO = 2400.0/4096.0
#ASPECT_RATIO = 9.0/16.0 # Standard Widescreen 16:9
FSW = 4096/4
FSH = 2400/4
BALL_IMG = "ball_small.png"
GOAL_IMG = "Football_goal.png"
MSG_IMG = "goal_msg.png"

class Goal(FloatLayout):
	"""
	Football!
	"""

	def build(self):
		print "build"
	
	def __init__(self, *args, **kwargs):
		super(Goal, self).__init__(*args, **kwargs)
		print "__init__ is run"
		gimg = Image(source=GOAL_IMG)
		self.add_widget(gimg)
		gimg.pos = (0,0)
		#Window.fullscreen = True
		Window.size = (FSW, FSH)
	
	def on_pause(self):
		return True
	
	def on_touch_down(self, touch):
		userdata = touch.ud
		(w, h) = Window.size
		sc = max(float(w)/FSW,float(h)/FSH)
		# start collecting points in touch.ud
		self.canvas.clear
		gimg = Image(source=GOAL_IMG)
		self.add_widget(gimg)
		bimg = Image(source=BALL_IMG)
		self.add_widget(bimg)
		(xpos, ypos) = (int(touch.x)-w/2, int(touch.y)-h/2)
		bimg.size = (10,10) #(int(60.0*sc), int(60.0*sc))
		bimg.pos = (xpos, ypos)
		#print '{0} and {1}'.format(float(w)/FSW,float(h)/FSH) 2115
		#print sc
		print '{0} and {1}'.format(touch.x, touch.y)
		#print '{0} and {1}'.format(xpos, ypos)
		if touch.x > FSW/20 and touch.x < w-FSW/20 and touch.y > h*0.2 and touch.y < h*0.88:
			print "GOAL!"
			mimg = Image(source=MSG_IMG)
			self.add_widget(mimg)
		#with self.canvas:
			#Color(1, 1, 1)
			#d = 60.
			#Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d, d))
		return True
	
	#def on_touch_move(self, touch):
		# For later use

	#def on_touch_up(self, touch):
		#self.remove_widget(bimg)

	
class Football(App):
	def build(self):
		return Goal()

if __name__ == '__main__':
	Football().run()

