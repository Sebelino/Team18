import kivy
kivy.require('1.0.9')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.base import EventLoop
from kivy.vector import Vector
from kivy.uix.image import Image


class GestureHandler(App):
		
	def on_touch_down(self, touch):
		ud = touch.ud
		
		touches = EventLoop.touches
		nrOfTouches = len(touches)
		
		if nrOfTouches > 1
			print "Multi touch event: " + nrOfTouches + " touch points"
		elif nrOfTouches == 1
			print "Single touch event"
		
		
		'''
		Jag tar fram touch-punkterna så man har nåt att jobba med.
		'''
		
		
		''' Lite kod från DeflectTouch-spelet som kanske kan vara till hjälp
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
		
		

if __name__ == '__main__':
	print "Running GestureHandler!"
	GestureHandler().run()
	




















