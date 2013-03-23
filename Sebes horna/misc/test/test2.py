	def on_touch_move(self,touch): #executed when a finger moves, which is all the time.
		#touches = getCurrentTouches() #leftover from pymt. need to find a kivy equivalent.
		for t in touches:
			self.TouchPositions['touch%s' % (touch.id)] = [(touch.x,touch.y)]
		#print "%s\n%s\n\n" % (self.TouchPositions) # sanity check
		i = 0
		self.touchlist = []  #list is reset to empty so we start fresh on every move.
		for k,v in self.TouchPositions.iteritems():
			i = i + 1
			#this hurts my brain, so lemme explain...
			#k is the touch id name
			#i is the iterator. it helps keep the number of touches.
			#v[0] is a tuple that contains the touches coordinates, as is v[1], v[2], and v[3].

			self.Touchlist.append(v)
			#now we have a simple touch# = (x,y) formula that we can exploit.
