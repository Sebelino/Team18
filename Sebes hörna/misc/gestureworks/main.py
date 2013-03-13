#:kivy 1.5.0
#:import kivy kivy
#:import win kivy.core.window

FloatLayout:
        canvas:
                Color:
                        rgb: 0, 0, 0
from gwc_python.core import GestureWorksCore
from gwc_python.GWCUtils import TOUCHREMOVED

from kivy.app import App
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Ellipse, Line
from kivy.core.window import Window
from kivy.uix.label import Label

class MultitouchApp(App):
    def __init__(self, gw):
        self.gw = gw
        Window.clearcolor = (.64, .64, .64, 1)
        self.active_points = {}

        super(MultitouchApp, self).__init__()

    def build(self):
        pass
if __name__ == '__main__':
    gw = GestureWorksCore('C:\\path\\to\\GestureworksCore\\GestureWorksCore32.dll')
    if not gw.loaded_dll: 
        print 'Unable to load GestureWorksCore'
        exit()
    gw.initializeGestureWorks(1920, 1080)
    app = MultitouchApp(gw)
    app.run()

Clock.schedule_interval(self.updateGestureWorks, 1.0/60)

    def updateGestureWorks(self, *args):
        self.root.canvas.clear()
        self.gw.processFrame()
        point_events = gw.consumePointEvents()
        self.processTouchEvents(point_events)
        self.drawTouchPoints()

    def processTouchEvents(self, touches):
        for touch in touches:
            if touch.status != TOUCHREMOVED:
                self.active_points.update({touch.point_id: touch})
            else:
                self.active_points.pop(touch.point_id)

    def drawTouchPoints(self):
        for touch in self.active_points.values():

            touch_y = int(self.root.height - touch.position.y)
            touch_x = int(touch.position.x)

            with self.root.canvas:
                Color(*get_color_from_hex('ffe354'))
                Ellipse(pos=(touch_x - 20, touch_y + 20), size=(40,40))
                Line(circle=(touch_x, touch_y + 40, 30, 0, 360), width=2)
        
                label = Label(text='ID: {}\nX: {} | Y: {}'.format(touch.point_id, touch_x, touch_y))
                label.center_x = touch_x + 80
                label.center_y = touch_y + 80
                label.color = (1,1,1)

    def build(self):
        if not self.gw.registerWindow('Kivy'):
            print('Unable to register touch window')
            exit()
