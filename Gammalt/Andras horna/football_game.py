from math import sqrt
from random import random, randint
import string
from kivy.app import App
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Ellipse, Line, Point, GraphicException

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


class FootballGame(Widget):
    coloring_mode = False
    global coloring_mode

    def on_touch_down(self, touch):
        win = self.get_parent_window()
        userdata = touch.ud
        userdata['group'] = group_uid = str(touch.uid)

        with self.canvas:
            userdata['color'] = Color(random(), 1, 1, mode='hsv', group=group_uid)
            #d = 10
            #userdata['point'] = Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d, d), group=group_uid)
            userdata['crosshair'] = (
                Rectangle(pos=(touch.x, 0), size=(1, win.height), group=group_uid),
                Rectangle(pos=(0, touch.y), size=(win.width, 1), group=group_uid),
                Point(points=(touch.x, touch.y), source='particle.png', pointsize=5, group=group_uid))
            #userdata['line'] = Line(points=(touch.x, touch.y), group=group_uid)      

        global coloring_mode
        if coloring_mode == False:
            userdata['label'] = Label(size_hint=(None, None))
            self.update_touch_label(userdata['label'], touch)
            self.add_widget(userdata['label'])
        touch.grab(self)

        return True 

    def on_touch_move(self, touch):
        #touch.ud['line'].points += [touch.x, touch.y]
        
        if touch.grab_current is not self:
            return
        userdata = touch.ud
        userdata['crosshair'][0].pos = touch.x, 0
        userdata['crosshair'][1].pos = 0, touch.y

        points = userdata['crosshair'][2].points
        oldx, oldy = points[-2], points[-1]
        points = calculate_points(oldx, oldy, touch.x, touch.y)
        if points:
            try:
                lp = userdata['crosshair'][2].add_point
                for idx in xrange(0, len(points), 2):
                    lp(points[idx], points[idx+1])
            except GraphicException:
                pass
        
        global coloring_mode
        if coloring_mode == False:
            userdata['label'].pos = touch.pos
            self.update_touch_label(userdata['label'], touch)

    # Using a dirty global boolean to handle different modes, but it works.
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

class FootballApp(App):

    pointcounter_bjorn = Label(text='Bjorn: 0', size_hint=(1, .5), font_size=28) 
    pointcounter_henrik = Label(text='Henrik: 0', size_hint=(1, .5), font_size=28)
    
    # FIX Needs more lists to traverse to create scene, instead of all this manual stuff.
    # FIX button_list should hold all buttons and just cycle through and add them to parent.
    # FIX Generate a random starting position list for button positions instead of manually assigning.
    def build(self):
        parent = Widget()
        painter = FootballGame()
        #button_list = []
        #score_button_layout = BoxLayout(orientation='vertical', size=(500+375, 500+250), pos=(2000, 200))
        #score_button_layout2 = BoxLayout(orientation='vertical', size=(400, 300), pos=(900,1500))
        pointcounter_layout = BoxLayout(orientation='vertical', size=(400,200), pos=(0, 1500))
        
        score_button_b = Button(text='Bjorn', size_hint=(1, 1), font_size=72)
        score_button_h = Button(text='Henrik', size_hint=(1, 1), font_size=72)
        
        parent.add_widget(painter)
        #parent.add_widget(score_button_layout)
        #parent.add_widget(score_button_layout2)
        parent.add_widget(pointcounter_layout)

        score_button_b = self.add_kick_button('Bjorn', (875, 750), (2000, 200), button_function_down=None, button_function_up=self.score_goal)
        score_button_h = self.add_kick_button('Henrik', (400, 300), (900, 1500), button_function_down=None, button_function_up=self.score_goal)
        parent.add_widget(score_button_b)
        parent.add_widget(score_button_h)

        score_button_b15 = self.add_kick_button('B 15', (100, 100), (1500, 100), self.animate_random_move, self.score_goal)
        parent.add_widget(score_button_b15)

        score_button_h15 = self.add_kick_button('H 15', (100,100), (1900, 100), self.animate_random_move, self.score_goal)
        parent.add_widget(score_button_h15)

        score_button_h30 = self.add_kick_button('H 30', (75, 75), (1675, 375), self.animate_random_move, self.score_goal)
        parent.add_widget(score_button_h30)

        score_button_b30 = self.add_kick_button('B 30', (75, 75), (1375, 375), self.animate_random_move, self.score_goal)
        parent.add_widget(score_button_b30)

        # Funky fix to get clear to work for the painter canvas, proper implementation not forthcoming.
        # However, the canvas currently does not hold the touch events after on_touch_up occurs.
        def clear_canvas(obj):
            painter.canvas.clear()
        
        clear_button = self.add_kick_button('Clear', (100, 100), (10, 10), clear_canvas)
        parent.add_widget(clear_button)
        # Clear button was added, end of funky stuff.

        toggle_button = self.add_kick_button('Toggle', (100, 100), (120,10), self.toggle_coloring_mode)
        parent.add_widget(toggle_button)
      
        pointcounter_layout.add_widget(self.pointcounter_bjorn)
        pointcounter_layout.add_widget(self.pointcounter_henrik)

        #score_button_layout.add_widget(score_button_b)
        #score_button_layout2.add_widget(score_button_h)

        #score_button_b.bind(on_press=self.animate_random_move, on_release=self.score_goal)
        #score_button_h.bind(on_press=self.animate_random_move, on_release=self.score_goal)

        return parent

    # FIX Here we're adding the spinning head animation! Later!
    def graphical_reward(self, pos):
        pass
    
    # Button action that toggles the coloring mode global. Somewhat dirty, using a global.
    def toggle_coloring_mode(self, instance):
        global coloring_mode
        coloring_mode = not coloring_mode

    # FIX Needs to handle incorrectly formatted target labels.
    def score_goal(self, obj):
        numbers_at = []
        for i in range(0,9):
            n = obj.text.find(str(i))
            if n > 0:
                numbers_at.append(n)
        numbers_at.sort()

        try:
            if obj.text[0] == 'B':
                start = self.pointcounter_bjorn.text.find(':') + 2
                if numbers_at != []:
                    self.pointcounter_bjorn.text = self.pointcounter_bjorn.text[:start] + (str(int(self.pointcounter_bjorn.text[start:]) + int(obj.text[numbers_at[0]:])))
                else:   
                    self.pointcounter_bjorn.text = self.pointcounter_bjorn.text[:start] + (str(int(self.pointcounter_bjorn.text[start:]) + 1))
            elif obj.text[0] == 'H':
                start = self.pointcounter_henrik.text.find(':') + 2
                if numbers_at != []:
                    self.pointcounter_henrik.text = self.pointcounter_henrik.text[:start] + (str(int(self.pointcounter_henrik.text[start:]) + int(obj.text[numbers_at[0]:])))
                else:
                    self.pointcounter_henrik.text = self.pointcounter_henrik.text[:start] + (str(int(self.pointcounter_henrik.text[start:]) + 1))
            else:
                print "Can't add points if neither H or B button-prefix exists."

        except IndexError, e:
            print "Caught IndexError, didn't add any points. Error was:", e


    # Bjorns favorit, bevarad for framtida bruk.
    def animate_score_button(instance):
        animation = Animation(pos=(100, 100), t='out_bounce')
        animation += Animation(pos=(200, 100), t='out_bounce')
        animation &= Animation(size=(500, 500))
        animation += Animation(size=(100, 50))

        animation.start(instance)

    # Just nudges the object up and to the right a little.
    def animate_continuous(instance):
        animation = Animation(pos=(instance.pos[0]+100, instance.pos[1]+100))
        animation += Animation(pos=(instance.pos[0]+200, instance.pos[1]+200), t='out_circ')

        animation.start(instance)  

    def animate_random_move(self, instance):
        animation = Animation(pos=(instance.pos[0]+randint(-150,150),instance.pos[1]+randint(-150,150)), t='in_circ')    
        #animation += Animation()

        animation.start(instance)

    # Returns a BoxLayout with a button inside. The button will have functions bound unless empty args are passed.
    def add_kick_button(self, button_name, button_size, button_pos, button_function_down=animate_continuous, button_function_up=None):
        button_holder = BoxLayout(orientation='vertical', size=button_size, pos=button_pos)
        button = Button(text=button_name, size_hint=(1, 1), font_size=button_size[0]*.15)
        button_holder.add_widget(button)

        button.bind(on_press=button_function_down, on_release=button_function_up)

        return button_holder


if __name__ == '__main__':
    FootballApp().run()