import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout

class ListView(FloatLayout):
    '''This class allows for a listview.

    Note: when creating one, make sure size_hint is set to (None, None),
    otherwise it will break. Otherwise should work just fine.

    '''

    
    scroll = None
    box = None
    __childHeight = 20
    childc = 0

    slider = None

    def __init__(self, childHeight, **kwargs):
        super(ListView,self).__init__(**kwargs)
        self.__childHeight = childHeight
        scroll = ScrollViewFixed(bar_width=30,
                            bar_margin=-30,
                            bar_color=[0.8,.8,.8,.99],
                            do_scroll_y = True,
                            do_scroll_x = False,
                            pos_hint= {'x':0,'y':0},
                            size_hint = (None,None),
                            size = self.size)
        box = BoxLayout(orientation='vertical',size_hint=(None,None),
                                size = self.size)
        scroll.add_widget(box)
        super(ListView, self).add_widget(scroll)
        s = Slider(orientation='vertical', value_normalized = 0.5, 
                   size_hint =(None,None), padding = 20,
                   size = (30, self.size[1]), pos_hint = {'x':1, 'y':0})
        scroll.slider = s
        def scrollMoves(slid,pos):
            scroll.scroll_y = pos
        s.bind(value_normalized=scrollMoves)
        super(ListView, self).add_widget(s, 1)
        self.scroll = scroll
        self.box = box

    def add_widget(self, widget, index = 0):
        #first, make sure the widget size is correct.
        widget.size_hint = (None, None)
        widget.size = (self.size[0], self.__childHeight)
        
        self.childc += 1
        self.box.size = (self.box.size[0],self.childc * self.__childHeight)
        self.box.add_widget(widget, index) #then add widget

    def remove_widget(self, widget):
        self.box.remove_widget(widget)
        childc -= 1
        self.box.size = (self.box.size[0],self.childc * self.__childHeight)
    
class ScrollViewFixed(ScrollView):
    ''' This class is basically the same as a ScrollView,
    except that the scrolling update method is overridden.
    The difference is that four lines of code has been removed.
    Those 4 lines made the scroll bar dissapear when not active for
    a few seconds.

    '''
    slider = None

    def __init__(self,**kwargs):
        super(ScrollViewFixed,self).__init__(**kwargs)      

    def update_from_scroll(self, *largs):
        if not self._viewport:
            return
        vp = self._viewport

        if self.do_scroll_x:
            self.scroll_x = min(1, max(0, self.scroll_x))
        if self.do_scroll_y:
            self.scroll_y = min(1, max(0, self.scroll_y))

        # update from size_hint
        if vp.size_hint_x is not None:
            vp.width = vp.size_hint_x * self.width
        if vp.size_hint_y is not None:
            vp.height = vp.size_hint_y * self.height

        if vp.width > self.width:
            sw = vp.width - self.width
            x = self.x - self.scroll_x * sw
        else:
            x = self.x
        if vp.height > self.height:
            sh = vp.height - self.height
            y = self.y - self.scroll_y * sh
        else:
            y = self.top - vp.height
        vp.pos = x, y
        #own code for slider/scrollbar
        if self.slider != None:
            self.slider.value_normalized = self.scroll_y

    
