from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
import win32api, win32con


class MyPaintWidget(Widget):

    clicks = 0
    def click(self,x,y):
	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    
    def on_touch_down(self, touch):
        with self.canvas:
            if self.clicks%2 == 0:
                Color(1, 1, 0)
            else:
                Color(1,0.5,0.5)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            self.clicks += 1
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

    def on_touch_up(self, touch):
        print touch.x
        print touch.y
        #self.click(int(touch.x),int(touch.y))
        win32api.SetCursorPos((int(touch.x),int(touch.y)))

class MyPaintApp(App):
    def build(self):
        parent = Widget()
        painter = MyPaintWidget()
        clearbtn = Button(text='Clear')
        parent.add_widget(painter)
        parent.add_widget(clearbtn)

        def clear_canvas(obj):
            painter.canvas.clear()
        clearbtn.bind(on_release=clear_canvas)

        return parent


if __name__ == '__main__':
    MyPaintApp().run()

