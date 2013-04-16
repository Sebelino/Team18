#!/usr/bin/env python
#http://kivy.org/docs/api-kivy.input.motionevent.html

import kivy
kivy.require('1.0.9')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.base import EventLoop
from kivy.vector import Vector
from kivy.uix.image import Image


class TouchArea(FloatLayout):
#class GestureHandler(App):

	_touches = []
	_last_touch_pos = {}


	
	def on_touch_down(self, touch):
		print "Touch down!"
		x = touch.x
		y = touch.y
		dx = touch.dx
		dy = touch.dy
		print "Touch uid: " + str(touch.uid)
		
		# Add touch point
		self._touches.append(touch)
		self._last_touch_pos[touch] = touch.pos

		if len(self._touches) == 2:
			print "Multi touch!"
		
		
	def on_touch_move(self, touch):
		touch.scale_for_screen(4096,2400)
		x = touch.x
		y = touch.y
		dx = touch.dx
		dy = touch.dy
		ud = touch.ud
		print "This touch: " + str(x) + ", " + str(y)
		print "Movement: " + str(dx) + ", " + str(dy)
		#print "Touch uid: " + str(touch.uid)
		
		if len(EventLoop.touches) == 2:
			otherTouch = EventLoop.touches[0]
			if otherTouch == touch:
				otherTouch = EventLoop.touches[1]
				print "First touch point moved"
			else:
				print "Second touch point moved"
			
			
			if abs(((touch.sx-otherTouch.x)**2+(touch.y-otherTouch.y)**2)**0.5
			- ((touch.px-otherTouch.sx)**2+(touch.py-otherTouch.y)**2)**0.5) < 0.9:
				print "Same distance"
				#Same distance indicates two-finger swipe or rotate
				
				if touch.dx == otherTouch.dx and touch.dy == otherTouch.dy:
					#Likely a swipe
					print "Swipe!"
				else:
					#Likely a rotation
					print "Rotate!"
				
			else:	#Varying distance indicates pinch
				print "Pinch"

	
	def on_touch_up(self, touch):
		x = touch.x
		y = touch.y
		dx = touch.dx
		dy = touch.dy
		print "Touch up!"
		print "Touch uid: " + str(touch.uid)
		
		
		
		# Remove the touch from our saved touches
		if touch in self._touches: # and touch.grab_state:
			#touch.ungrab(self)
			del self._last_touch_pos[touch]
			self._touches.remove(touch)


		'''
		for search_touch in touches[:]:
			if 'lonely' in search_touch.ud:
				del search_touch.ud['lonely']
				# so here we have a second touch: try to create a deflector:
				if self.parent.stockbar.new_deflectors_allowed == True:
					length = Vector(search_touch.pos).distance(touch.pos)
					# create only a new one if he's not too big and not too small
					if MIN_DEFLECTOR_LENGTH <= length <= self.parent.stockbar.width:
						self.create_deflector(search_touch, touch, length)
					else:
						self.parent.app.sound['no_deflector'].play()
				else:
					self.parent.app.sound['no_deflector'].play()
				
				return True
		
		# if no second touch was found: tag the current one as a 'lonely' touch
		ud['lonely'] = True
		'''

	
class GestureHandler(App):
	def build(self):
		return TouchArea()

if __name__ == '__main__':
	print "Running GestureHandler!"
	GestureHandler().run()
	




















