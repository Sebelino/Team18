from gwc_python.core import GestureWorksCore
from gwc_python.GWCUtils import TOUCHADDED, TOUCHREMOVED, TOUCHUPDATE, rotateAboutCenter

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.factory import Factory
from math import radians


class TouchObject(Scatter):
    def on_touch_move(self, touch): return

class ExampleApp(App):
    def __init__(self, gw, max_objects=2):
        self.gw = gw
        self.touch_points = {}
        self.touch_objects = {}
        self.max_objects = max_objects
        self.has_received_gesture = False
        
        # schedule our processing cycle
        Clock.schedule_interval(self.updateGestureWorks, 1./60)
        super(ExampleApp, self).__init__()
        
    def hitTest(self, x, y):
        for obj in self.touch_objects.values():
            (local_x, local_y) = rotateAboutCenter(x, y, obj.center_x, obj.center_y, radians(-obj.rotation))
            if (abs(local_x - obj.center_x) <= obj.width*obj.scale/2) and (abs(local_y - obj.center_y) <= obj.height*obj.scale/2):
                return obj
        
    def processTouchEvents(self, touches):
        for touch in touches:
            touch_x = touch.position.x

            # We need to convert kivy y coordinate to GestureWorks y coordinate
            touch_y = self.root.height - touch.position.y

            if touch.status == TOUCHADDED:
                obj = self.hitTest(touch_x, touch_y)
                if obj:
                    self.gw.addTouchPoint(obj.name, touch.point_id)
            elif touch.status == TOUCHREMOVED:
                # Handle touch removed 
                pass
            elif touch.status == TOUCHUPDATE:
                # Handle touch updates
                pass
                
    """Translate the object based on the event deltas"""
    def handleDrag(self, obj, gesture_event): 
        obj.center_x += gesture_event.values['drag_dx']
        obj.center_y -= gesture_event.values['drag_dy']
        
        # Make sure the objects stay on the screen
        obj.center_x = max(min(obj.center_x, self.root.width), 0)
        obj.center_y = max(min(obj.center_y, self.root.height), 0)
                
    """Rotate the object around the center of the event"""
    def handleRotate(self, obj, gesture_event):
        theta = gesture_event.values['rotate_dtheta']
        obj.rotation -= theta
        if gesture_event.n:
            obj.center = rotateAboutCenter(obj.center_x, obj.center_y, gesture_event.x, self.root.height - gesture_event.y, radians(-theta))        
    
    """Scale the object"""
    def handleScale(self, obj, gesture_event):
        dsx = gesture_event.values['scale_dsx']
        obj.scale += dsx
        obj.scale = max(min(obj.scale, 6), .5) # Scale bounds
                
    """Update our touch objects based on gesture events we receive"""
    def processGestureEvents(self, gesture_events):
        for e in gesture_events:
            obj = self.touch_objects[e.target]
            {'n-drag': self.handleDrag,
             'n-rotate': self.handleRotate,
             'n-scale': self.handleScale}[e.gesture_id](obj, e)
    
    """Tell GestureWorks to process a frame of data"""
    def updateGestureWorks(self, *args):
        self.gw.processFrame()
        point_events = gw.consumePointEvents()
        gesture_events = gw.consumeGestureEvents()
        if len(gesture_events) != 0:
            self.has_received_gesture = True;
        self.processTouchEvents(point_events)
        self.processGestureEvents(gesture_events)
        
        if not self.has_received_gesture:
            buf = self.root.width / (len(self.touch_objects) + 1)
            for obj in self.touch_objects.values():
                obj.center = (buf, self.root.height / 2)
                buf += buf
        
    def build(self):
        # Register our app window with GestureWorks
        if not self.gw.registerWindow('Kivy'):
            print('Unable to register touch window')
            exit()
            
        for i in range(0, self.max_objects):
            container = TouchObject()
            container.name = 'object_{}'.format(i)
            container.add_widget(Image(source='media/logo.png'))
            container.scale = 2
            self.root.add_widget(container)
            self.touch_objects.update({container.name: container})
            
            # Tell GestureWorks about our touch object and add gestures to it
            self.gw.registerTouchObject(container.name)
            self.gw.addGesture(container.name, 'n-drag')
            self.gw.addGesture(container.name, 'n-rotate')
            self.gw.addGesture(container.name, 'n-scale')
            
Factory.register('TouchObject', TouchObject)
if __name__ == '__main__':
    # Initialize GestureWorksCore with the location of the library
    gw = GestureWorksCore('C:\\path\\to\\GestureWorksCore\\GestureWorksCore32.dll')
    if not gw.loaded_dll: 
        print 'Unable to load GestureWorksCore'
        exit()
        
    try:
        # Load a basic GML file
        gw.loadGML('C:\\path\\to\\GestureWorksCore\\basic_manipulation.gml')
    except WindowsError, e:
        print 'Unable to load GML'
        exit()  
        
    gw.initializeGestureWorks(1920, 1080)
    app = ExampleApp(gw)
    app.run()