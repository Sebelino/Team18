import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Point, GraphicException
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from random import random
from math import sqrt


def calculate_points(x1, y1, x2, y2, steps=5):
    dx = x2 - x1
    dy = y2 - y1
    dist = sqrt(dx * dx + dy * dy)
    if dist < steps:
        return None
    o = []
    m = dist / steps
    for i in xrange(1, int(m)):
        mi = i / m
        lastx = x1 + dx * mi
        lasty = y1 + dy * mi
        o.extend([lastx, lasty])
    return o


class Touchtracer(FloatLayout):
    coloring_mode = False
    global coloring_mode

    def on_touch_down(self, touch):
        win = self.get_parent_window()
        ud = touch.ud
        ud['group'] = g = str(touch.uid)
        with self.canvas:
            ud['color'] = Color(random(), 1, 1, mode='hsv', group=g)
            
            global coloring_mode
            if coloring_mode == False:
                ud['lines'] = (Rectangle(pos=(touch.x, 0), size=(1, win.height), group=g),
                    Rectangle(pos=(0, touch.y), size=(win.width, 1), group=g),
                    Point(points=(touch.x, touch.y), source='particle.png', pointsize=5, group=g))
            else:
                ud['lines'] = (Rectangle(pos=(touch.x, 0), size=(0, 0), group=g),
                    Rectangle(pos=(0, touch.y), size=(0, 0), group=g),
                    Point(points=(touch.x, touch.y), source='particle.png', pointsize=5, group=g))

        global coloring_mode
        if coloring_mode == False:
            ud['label'] = Label(size_hint=(None, None))
            self.update_touch_label(ud['label'], touch)
            self.add_widget(ud['label'])

        touch.grab(self)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        ud = touch.ud
        ud['lines'][0].pos = touch.x, 0
        ud['lines'][1].pos = 0, touch.y

        points = ud['lines'][2].points
        oldx, oldy = points[-2], points[-1]
        points = calculate_points(oldx, oldy, touch.x, touch.y)
        if points:
            try:
                lp = ud['lines'][2].add_point
                for idx in xrange(0, len(points), 2):
                    lp(points[idx], points[idx+1])
            except GraphicException:
                pass

        global coloring_mode
        if coloring_mode == False:
            ud['label'].pos = touch.pos
            self.update_touch_label(ud['label'], touch)

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        ud = touch.ud

        global coloring_mode
        if coloring_mode == False:
            self.canvas.remove_group(ud['group'])
            self.remove_widget(ud['label'])

    def update_touch_label(self, label, touch):
        label.text = 'ID: %s\nPos: (%d, %d)\nClass: %s' % (
            touch.id, touch.x, touch.y, touch.__class__.__name__)
        label.texture_update()
        label.pos = touch.pos
        label.size = label.texture_size[0] + 20, label.texture_size[1] + 20


class TouchtracerApp(App):
    title = 'Touchtracer'
    icon = 'icon.png'

    def toggle_coloring_mode(self, instance):
        global coloring_mode
        coloring_mode = not coloring_mode


    def build(self):
        grouper = Widget()
        parent = Touchtracer()
    
        button_holder = BoxLayout(orientation='vertical', size=(100,100), pos=(900,720))
        button = Button(text="Toggle", size_hint=(1, 1), font_size=100*.15)
        button_holder.add_widget(button)
        button.bind(on_press=None, on_release=self.toggle_coloring_mode)

        def clear_canvas(obj):
            parent.canvas.clear()
        
        clear_holder = BoxLayout(orientation='vertical', size=(100,100), pos=(1010,720))
        clear_button = Button(text="Clear", size_hint=(1, 1), font_size=100*.15)
        clear_holder.add_widget(clear_button)
        clear_button.bind(on_press=None, on_release=clear_canvas)

        grouper.add_widget(parent)
        grouper.add_widget(clear_holder)
        grouper.add_widget(button_holder)

        return grouper

if __name__ in ('__main__', '__android__'):
    TouchtracerApp().run()
