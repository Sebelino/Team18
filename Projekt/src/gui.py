# -*- coding: cp1252 -*-
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.uix.slider import Slider
from kivy.properties import NumericProperty
from kivy.graphics import Color,Ellipse,Line
from kivy.gesture import Gesture,GestureDatabase
import Gesture as OwnGesture
from listview import ListView, ScrollViewFixed
# import Controller

import thread
import time
import os
import sys
import DatabaseAdapter as db                     #Spaghetti-dependency. Fixa!
import GestureHandler
from kivy.base import EventLoop
import Queue

##################################################################
#---------------------- Config ----------------------------------#
##################################################################

"""Create a small cute window, unresizeable"""

Config.set('kivy','window_icon', 'smiley_ic.png')
Config.set('graphics','fullscreen',0)
Config.set('graphics','resizable',0)
Config.set('graphics','width',650)
Config.set('graphics','height',500)

PICPATH = '../resources/pics'
font = '../resources/font/segoeui.ttf'

######################################################
## -----------------------Mapping Display Class -----#
######################################################
"""
OK, so, this class exists as a component that keeps all the
mappings in a neat scrollable list. Because it might be a mess,
and I might forget stuff, here is some important info about
usage:

1. When creating this object, you MUST set the attributes size and
   size_hint. Size will be the size of the widget, and size_hint
   should be set to (None, None), otherwise the behavior is undefined.
2. Attribute mappingHeight is the height of one mapping, it better be
   set before adding mappings (although it is set to 40 by default),
   otherwise it will break.
3. Attribute proportions are the sizes, in percentages, of each of the
   five components of a mapping. Better also be changed before adding
   mappings, otherwise will break (set by default though).
4. There are lots of options for setting Images, attributes should have
   (long :/) describing names. Set images before adding mappings.
5. When adding a mapping, it should be in the format of a tuple with
   two string attributes. Otherwise, might get exceptions
6. MappingDisplay is a FloatLayout with two children: a background
   image and a ScrollView. If adding children directly, it will behave
   like a FloatLayout. The ScrollView contains a BoxLayout with
   vertical orientation. One annoying thing is that BoxLayout has its
   children positioned from the bottom and up, while I want it the other
   way. Anyway, its taken care of in the code. Just keep in mind for the
   Controller, that when a mapping is created, append it to the list.
"""
def simplegesture(name, point_list):
    """
    A simple helper function
    """
    g = Gesture()
    g.add_stroke(point_list)
    g.normalize()
    g.name = name
    return g
class MappingDisplay(FloatLayout):
    #if have_background is true, a background image is set
    have_background = False
    mappingImagePath = None
    deleteButtonImagePathUp = None
    deleteButtonImagePathDown = None
    layout = None
    gestureEditButtonImageUp = None
    gestureEditButtonImageDown = None
    macroEditButtonImageUp = None
    macroEditButtonImageDown = None
    mappingHeight = 25

    def __init__(self,**kwargs):
        #call the constructor of the flowlayout
        #this exists to keep the standard kivy syntax
        super(MappingDisplay,self).__init__(**kwargs)

        scroll = ScrollViewFixed(bar_width=30,
                            bar_margin=-30,
                            bar_color=[0.8,.8,.8,.99],
                            do_scroll_y = True,
                            do_scroll_x = False,
                            pos_hint= {'x':0,'y':0},
                            size_hint = (None,None),
                            size = self.size)
        
        self.layout = BoxLayout(orientation='vertical',size_hint=(None,None),
                                size = self.size)
        scroll.add_widget(self.layout)
        self.scroll = scroll
        self.add_widget(scroll)

        #now implement a scrollbar
        s = Slider(orientation='vertical', value_normalized = 0.5, 
                   size_hint =(None,None), padding = 20,
                   size = (30, self.size[1]), pos_hint = {'x':1, 'y':0})
        scroll.slider = s
        def scrollMoves(slid,pos):
            scroll.scroll_y = pos
        s.bind(value_normalized=scrollMoves)
        self.add_widget(s, 1)
        

    def setBackgroundImage(self, image_widget):
        lastIndex = len(self.children)
        if self.have_background == False:
            self.add_widget(image_widget, lastIndex)
            self.have_background = True
            
    def addMapping(self, mapping):
        mappingWidget = MappingInstance(size_hint = (None, None),
                                        size = (self.size[0], self.mappingHeight))
        mappingWidget.owner = self
        
        mappingWidget.add_widget(Image(allow_stretch=True, keep_ratio=False,
                                       source=self.mappingImagePath,
                                       size_hint=(None,None),
                                       size = mappingWidget.size,
                                       pos_hint={'x':0,'y':0}))
        border = 2
        border_y = 0.06
        
        delBtn = Button(background_normal = self.deleteButtonImagePathUp,
                        background_down = self.deleteButtonImagePathDown,
                        pos_hint={'x':0.005, 'y':border_y},
                        size_hint = (None,None),
                        size = (50, self.mappingHeight - border*2),
                        font_name = font,
                        text = '[color=000000][size=12]Remove', markup=True
                        )
        
        gesture = Label(color = (0,0,0,1),
                        text = mapping[0],
                        bold = True, markup= True,
                        pos_hint = {'x':0.12, 'y':border_y},
                        size_hint = (None,None),
                        size = (150, self.mappingHeight - border*2),
                        font_name = font, halign = 'left',text_size=(150,None),
                        font_size = 12
                        )
        
        gestureInfoBtn = Button(background_normal = self.gestureEditButtonImageUp,
                                background_down = self.gestureEditButtonImageDown,
                                pos_hint = {'x':0.43, 'y':border_y},
                                size_hint = (None,None),
                                size = (40, self.mappingHeight - border*2),
                                text = '[color=000000][size=12]Edit', markup=True,
                                font_name = font
                                )
        
        macro = Label(color = (0,0,0,1),
                      text = mapping[1],
                      bold = True, markup = True,
                      pos_hint = {'x':0.61, 'y':border_y},
                      size_hint = (None,None),
                      size = (150, self.mappingHeight - border*2),
                      font_name = font, halign = 'left', text_size=(150, None),
                      font_size = 12
                      )
        
        macroInfoBtn = Button(background_normal = self.macroEditButtonImageUp,
                              background_down = self.macroEditButtonImageDown,
                              pos_hint = {'x':0.915, 'y':border_y},
                              size_hint = (None,None),
                              size = (40, self.mappingHeight - border*2),
                              text = '[color=000000][size=12]Edit', markup=True,
                              font_name = font
                              )
        mappingWidget.add_widget(macroInfoBtn)
        mappingWidget.add_widget(macro)
        mappingWidget.add_widget(gestureInfoBtn)
        mappingWidget.add_widget(gesture)
        mappingWidget.add_widget(delBtn)
        mappingWidget.bindButtons()
        self.layout.add_widget(mappingWidget)
        self.updateMappings()

    def removeMapping(self, index):
        i = len(self.layout.children) - 1 - index
        self.layout.remove_widget(self.layout.children[i])
        self.updateMappings()
        removeMapping(index)

    def updateMappings(self):
        self.layout.size = (self.size[0], \
                            len(self.layout.children)*self.mappingHeight)
        for i in reversed(range(len(self.layout.children))):
            self.layout.children[i].index = len(self.layout.children) - i - 1

    def editMapping(self,index,gesture,macro):
        i = len(self.layout.children) - index - 1
        mapping = self.layout.children[i]
        if gesture != None:
            mapping.children[1].text = gesture
        if macro != None:
            mapping.children[3].text = macro

    def showInfo(self,index,which):
        displayEditMappingPopup(index, which)
        
class GestureCreator(FloatLayout):
    '''On touch events'''
    queue = Queue.Queue()

    def __init__(self,**kwargs):
        super(GestureCreator,self).__init__(**kwargs)
        self.gdb = GestureDatabase()
    
    def on_touch_down(self, touch):
        print str(touch.device)
        if str(touch.device) == "multitouchtable":
            print "touch"
        elif str(touch.device) == "mouse":
            print "mouse click"
        # start collecting points in touch.ud
        # create a line to display the points
        userdata = touch.ud
        with self.canvas:
            Color(1, 0, 0)
            d = 10.
            Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d, d))
            userdata['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        # store points of the touch movement
        try:
            touch.ud['line'].points += [touch.x, touch.y]
            return True
        except (KeyError), e:
            pass

    def containsGesture():
        return not queue.empty()

    def poll():
        return queue.get()

    def on_touch_up(self, touch):
        # touch is over, display informations, and check if it matches some
        # known gesture.
        g = simplegesture(
                '',
                zip(touch.ud['line'].points[::2], touch.ud['line'].points[1::2])
                )
        # print the gesture representation, you can use that to add
        # gestures to my_gestures.py
        print "gesture representation:", self.gdb.gesture_to_str(g)

        gesture = OwnGesture.Gesture(self.gdb.gesture_to_str(g))
        self.queue.put(gesture)

        # erase the lines on the screen, this is a bit quick&dirty, since we
        # can have another touch event on the way...
        #self.canvas.clear()

    def containsGesture():
        return not queue.empty()
    '''End of on-touch events'''


class MacroCreator(FloatLayout):
    layout = None
    def __init__(self,**kwargs):
        super(MacroCreator,self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical',size_hint=(None,None),size = (100,100))
        nameBox = TextInput(multiline = False,font_size = 13)
        #nameBox.add_widget(self.layout)
        self.add_widget(nameBox)

class MappingInstance(FloatLayout):
    index = 0
    owner = None
    
    def __init__(self,**kwargs):
        super(MappingInstance,self).__init__(**kwargs)

    def __delBtn_callback(self,btn):
        self.owner.removeMapping(self.index)

    def __infoBtnGest_callback(self,btn):
        self.owner.showInfo(self.index, 'gesture')

    def __infoBtnMac_callback(self,btn):
        self.owner.showInfo(self.index, 'macro')

    def bindButtons(self):
        self.children[0].bind(on_release=self.__delBtn_callback)
        self.children[2].bind(on_release=self.__infoBtnGest_callback)
        self.children[4].bind(on_release=self.__infoBtnMac_callback)


##################################################################
#-------------------- touch block Popup Class -------------------#
##################################################################

#This class disables touch on popups

class touchBlockedPopup(Popup):
    #On touch events
    def on_touch_down(self, touch):
        print "Touch down!"
        print "Touch uid: " + str(touch.uid)

        if len(EventLoop.touches) > 1:
            print "Multi touch!"
        
        if str(touch.device) == "mouse":
            super(touchBlockedPopup, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        print "Touch move!"
        print "uid: " + str(touch.uid)
        if str(touch.device) == "mouse":
            super(touchBlockedPopup, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        print "Touch up!"
        print "uid: " + str(touch.uid)
        if str(touch.device) == "mouse":
            super(touchBlockedPopup, self).on_touch_up(touch)


##################################################################
#-------------------- Event Popup Class -------------------------#
##################################################################
class EventPopup(Popup):
    '''A class which is a very specialized popup.

    To use, simply initiate an instance with one parameter, which is a
    string and should be set to either 'gesture' or 'macro'. Call
    setDropdownWithExplanation to update the list of gestures or windows
    functions. Call open(index) to open the popup. The index should be
    the index of the mapping where the popup was summoned from.
    '''
    
    container = None
    gestureOrMacro = 'gesture'
    index = 0
    
    def __init__(self, gestureOrMacro, **kwargs):
        super(EventPopup,self).__init__(**kwargs)
        self.container = FloatLayout()
        self.gestureOrMacro = gestureOrMacro
        self.size=(400,300)
        self.size_hint=(None, None)
        self.auto_dismiss = False
        self.separator_color = (0.625, 0.625, 0.625, 1)
        self.separator_height = 1
        self.__setTitle()
        self.__addCancelAcceptButtons()
        self.__addCreateEventButton()
        self.container.add_widget(Widget())
        self.container.add_widget(Widget())
        #these two widgets are placeholders.
        self.content = self.container

    def open(self, index):
        '''Override open method.

        Call it like Popup's open, but with an index signaling
        which mapping (by index) the popup is for'''
        self.index = index
        super(EventPopup, self).open()

    # Now comes some private methods to keep the contructor clean.
    # Note that these methods are called once from the __init__
    # method, please do not call them
     
    def __setTitle(self):
        ''' Set the title of the popup.

        Note that this method is called once from the __init__
        method, please do not call it.'''
        if self.gestureOrMacro == 'gesture':
            self.background = PICPATH+'/set_gesture_popup.png'
        elif self.gestureOrMacro == 'macro':
            self.background = PICPATH+'/set_macro_popup.png'

    def __addCancelAcceptButtons(self):
        '''Private method to set buttons.'''

        #Button that signals cancel
        cancelBtn = Button(text='[color=000000]Cancel', markup=True,
                           size_hint=(None,None), size = (140, 25),
                           pos_hint = {'right':0.98, 'y':0},
                           background_normal = PICPATH+'/button_up.png',
                           background_down = PICPATH+'/button_down.png')

        cancelBtn.bind(on_release= lambda btn: self.dismiss())
        
        #Button that signals accept
        doneBtn = Button(text='[color=000000]Ok', markup=True,
                         size_hint=(None,None), size = (140, 25),
                         pos_hint = {'x':0.02, 'y':0},
                         background_normal = PICPATH+'/button_up.png',
                         background_down = PICPATH+'/button_down.png')
    
        def doneBtn_callback(btn):
            if self.gestureOrMacro == 'gesture':
                editMapping(self.index, self.container.children[1].text, None)
            elif self.gestureOrMacro == 'macro':
                editMapping(self.index, None, self.container.children[1].text)
            self.dismiss()
        doneBtn.bind(on_release=doneBtn_callback)

        #add buttons to container
        self.container.add_widget(cancelBtn)
        self.container.add_widget(doneBtn)

    def __addCreateEventButton(self):
        '''private method to create createEvent button'''

        eventBtn = Button(markup=True,
                          size_hint=(None,None), size = (95, 28),
                          pos_hint = {'right':0.99, 'top':0.97},
                          background_normal = PICPATH+'/button_up.png',
                          background_down = PICPATH+'/button_down.png')
        
        if self.gestureOrMacro == 'gesture':
            eventBtn.text = '[color=000000][font='+font+'][size=11]'+ \
                            'Customize'
            def eventBtn_callback(btn):
                manageGestures()
                #self.dismiss() TODO
            eventBtn.bind(on_release=eventBtn_callback)
        elif self.gestureOrMacro == 'macro':
            eventBtn.text = '[color=000000][font='+font+'][size=11]'+ \
                            'Customize'
            def eventBtn_callback(btn):
                manageMacros()
                #self.dismiss() TODO
            eventBtn.bind(on_release=eventBtn_callback)
                          
        self.container.add_widget(eventBtn)

    def setDropdownWithExplanation(self, allEvents):

        #remove the previous widgets
        self.container.remove_widget(self.children[0])
        self.container.remove_widget(self.children[0])

        #make sure all widgets are correct size
        for eve in allEvents:
            w = eve[1]
            w.size_hint = (0.95, 0.6)
            w.pos_hint = {'x':0.025, 'y':0.2}

        pickEventBtn = Button(text='[color=000000]'+allEvents[0][0], 
                          markup=True, size_hint=(0.7,0.12),
                          pos_hint = {'x':0.01, 'y': 0.85},
                          background_normal = PICPATH+'/button_up_dropdown.png',
                          background_down = PICPATH+'/button_down_dropdown.png',
                          text_size = (250,None), halign='left',
                          font_size = 13
                          )

        dd = DropDown(max_height=250, bar_width=5)

        i = 0
        for eve in allEvents:
            btn = IndexButton(text=eve[0], color=(0,0,0,1),
                         size_hint_y=None, height=20,
                         background_normal = PICPATH+'/dropdown_choice.png',
                         text_size = (250,None), halign='left')
            btn.index = i
            btn.bind(on_release=lambda btn: selectEvent(btn.index))
            dd.add_widget(btn)
            i += 1
                
        def selectEvent(ind):
            dd.select(ind)
            pickEventBtn.text='[color=000000]'  \
                                        + allEvents[ind][0]
            self.container.remove_widget(self.container.children[0])
            self.container.add_widget(allEvents[ind][1])
       
        pickEventBtn.bind(on_release=dd.open)
        self.container.add_widget(pickEventBtn)
        self.container.add_widget(allEvents[0][1])
    
class IndexButton(Button):
    '''Helper class for EventPopup.

    Is a simple button with an extra variable'''
    index = 0
    def __init__(self,**kwargs):
        super(IndexButton,self).__init__(**kwargs)


##################################################################
#-------------- Confirm Popup Class and function-----------------#
##################################################################
'''
This is the class ConfirmPopup. It is used for creating a popup to
confirm a specific action. Usage:

An object is already created and there is no need to create more.
The object is called simply "confirm" (see beneath class definition).
There is only one method: open(title, function, *args).
 - title should be a string, it will be the title of the popup.
 - function is the function to call if the user confirms the action.
 - *args is a list of arguments. It is the Python way of having
   multiple arguments in a list. These are the arguments that will go
   into function. Note that currently only up to three arguments are
   supported, but it is fairly simply (but tedious) to add support
   for more.

Example 1 argument: confirm.open("Are you sure you want to delete profile?",
                      deleteProfileAction,
                      getCurrentProfile())

Example 3 args: confirm.open("Are you sure you want to print this?",
                              evilPrintFunc,
                              page1, page2, page3)

Example no args: confirm.open("Are you sure you want to close the program?",
                               exit)
'''



class ConfirmPopup(Popup):
    function = None
    args = []
    
    def __init__(self,**kwargs):
        super(ConfirmPopup,self).__init__(**kwargs)
        container = FloatLayout()
        self.size=(350,120)
        self.size_hint=(None, None)
        self.auto_dismiss = False
        self.separator_color = (0.625, 0.625, 0.625, 1)
        self.separator_height = 1
        self.title_size = '10sp'
        #self.background=PICPATH+'/white_background.png'
        btnsize = (100, 27)
        yesBtn = Button(size_hint = (None,None), size = btnsize,
                        text = "[color=000000]Accept", markup = True,
                        pos_hint = {'x':0.05, 'y':0.05}, 
                        background_normal = PICPATH+'/button_up.png',
                        background_down = PICPATH+'/button_down.png')
        yesBtn.bind(on_release = self.callFunction)
        noBtn = Button(size_hint = (None,None), size = btnsize,
                        text = "[color=000000]Cancel", markup = True,
                        pos_hint = {'right':0.95, 'y':0.05}, 
                        background_normal = PICPATH+'/button_up.png',
                        background_down = PICPATH+'/button_down.png')        
        noBtn.bind(on_release = lambda(btn): self.dismiss())

        container.add_widget(yesBtn)
        container.add_widget(noBtn)
        self.content = container

    def open(self, title, function, *args):
        self.title = title
        self.function = function
        self.args = args
        super(ConfirmPopup,self).open()

    def callFunction(self, btn):
        argc = len(self.args)
        if(argc == 0):
            self.function()
        elif(argc == 1):
            self.function(args[0])
        elif(argc == 2):
            self.function(args[0], args[1])
        elif(argc == 3):
            self.function(args[0], args[1], args[2])
        self.dismiss()

confirm = ConfirmPopup()


##################################################################
#-------------------- Load Images -------------------------------#
##################################################################
profileBarImg = Image(allow_stretch=True, keep_ratio=False,
                      source=PICPATH+'/background_top.png',
                      size_hint=(1,1),
                      pos_hint={'y':0})
mainBackgroundImg = Image(allow_stretch=True, keep_ratio=False,
                          source=PICPATH+'/background_bot.png',
                          size_hint=(1,1),
                          pos_hint={'y':0})
blackBorderImg = Image(allow_stretch=True, keep_ratio=False,
                       source=PICPATH+'/black_border.png',
                       size_hint=(1,1),
                       pos_hint={'y':0})


                      
##################################################################
#--------------------- Functions --------------------------------#
##################################################################

"""
These are functions that communicate with the Controller module.

Note that it is not possible to specify exactly what the function
is supposed to do here in the GUI, because the GUI does not know
the specifics. See Controller for more info about the functions.
"""

#-------- Requests -------------------#
def getListOfProfiles():
    """Returns a list of profiles, requested from Controller."""
    #TODO
    return ['HueZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ','Boo','Traktor',
            'Captain MintberryCrunch', 'Internet', 'Halo', 'Pale tree']

def getCurrentProfile():
    """Returns the currently selected profile, requested from Controller."""
    #TODO
    return getListOfProfiles()[4]
    

def getListOfMappings(profile):
    """Returns a list of mappings, requested from Controller."""
    #TODO
    return db.getMappings()

def getListOfGestures():
    """Returns a list of available Gestures, requested from Controller."""
    table = db.getGestures()
    return [(r[0],TextInput(text=('' if r[1] is None else r[1]),readonly=True)) for r in table]
#    return [('KameHameHA', TextInput(text='WAVE\nJO\nNEJ\nblod',readonly = True)),
#            ('punch',TextInput(text='kALABALALAMMMMMMMMMMMMmmmASDN',readonly = True)),
#            ('Hadoken',TextInput(text='kALABALALAMMMMMMMMMMMMmmmASDN',readonly = True)),
#            ('Two-finger swipe', Image(source=PICPATH+'/two_swipe.gif', allow_stretch=True,
#                            keep_ratio=False))]

def getListOfCustomGestures():
    """Returns a list of all Custom gestures"""
    return ["RAH", "BLO", "PATETISK" ]

def getListOfMacros():
    """Returns a list of Macros/Windows Functions, requested from Controller."""
    table = db.getCommands()
    return [(r[0],TextInput(text=('' if r[1] is None else r[1]),readonly=True)) for r in table]
#    return [('leftclick', TextInput(text='U DUNNO WUT LEFTCLICK IS',readonly = True)),
#            ('rightclick',TextInput(text='RaaALABALALAMMMMMMMMMMMMMMMMMMMMMmmmASDN',readonly = True)),
#            ('faint', Image(source=PICPATH+'/art.png', allow_stretch=True,
#                            keep_ratio=False))]

def getListOfCustomMacros():
    """Returns a list of all Custom gestures"""
    return ["RAH", "BLO", "PATETISKMACRO" ]

def getMacroInfo(macro):
    pass
    return ["macro", "stop;write;stop;", "text", "stops and writes"]
           
#-------- Profile management ---------#

def createProfile(profileName):
    """ Creates a new profile with the given name.

    Must return the name of the newly created profile."""
    #TODO
    print "Creating profile " + profileName
    return profileName

def editProfile(oldProfileName, newProfileName):
    """ Changes the name of a profile to the new name."""
    print "Changing name from " + oldProfileName + " to " + newProfileName 
    #TODO
    pass

def selectProfile(profileName):
    """ Selects the profile with the given name."""
    print "Selecting profile " + profileName
    #TODO
    pass

def removeProfile(profileName):
    """ Removes the profile with the given name."""
    print "Removing profile " + profileName
    #TODO
    pass

#------------- Mappings ----------------#
def createMapping(createCounter):
    """ Creates a new mapping with default values."""
    mappingBox.addMapping(('Gesture' + str(createCounter[0]), 'Macro' + str(createCounter[0])))
    createCounter[0] += 1
    pass

def editMapping(index, newGesture, newMacro):
    """ Edits the mapping with the given index.

    The parameters specify:
    newGesture - Gesture value, the new Gesture.
    newMacro - Macro value, the new Windows Macro/Function.
    If they are set to None, nothing will change.
    """
    print [index, newGesture, newMacro]
    mappingBox.editMapping(index, newGesture, newMacro)
    #TODO 
    #Change function parameters/arguments perhaps
    pass

def removeMapping(index):
    """ Removes the mapping with the given index."""
    print 'removing mapping ' + str(index)
    #TODO
    pass

#-------------- Gestures ----------------#
def createGesture(gesture):
    """ Creates the gesture. """
    pass

def removeGesture(gesture):
    """ Removes the specified gesture. """
    pass

#-------------- Macros/Windows functions ------------------#
def createMacro():
    """ Creates a new Macro. """
    pass

def editMacro(macro, newScript, descType, desc):
    """edits macro 'macro' from the script newScript,
       to description desc, which is of type descType"""
    print macro, newScript, "\n" ,descType, desc

def removeMacro(macro):
    """ Removes the specified Macro. """
    print "removing macro ", macro
    pass

##################################################################
# ------------------ Components --------------------------------_#
##################################################################

#------------------ ProfileBar ----------------------------------#
#Profile selection, is a boxlayout with 2 components:
#1. a label with a static text saying "current profile"
#2. A button with a dropdown Menu for the profile selection action

profileSelectionLabel = Label(text='[color=000000][b]Select profile',
                              markup=True,
                              size_hint=(None, None),
                              size = (250, 30),
                              pos_hint = {'x':0.05, 'y':0.6})

profileSelection = Button(markup=True,
                background_normal=PICPATH+'/button_up_dropdown.png',
                background_down=PICPATH+'/button_up_dropdown.png',
                size_hint = (None, None),
                size = (250, 30),
                pos_hint = {'x':0.05, 'y':0.4},
                halign = 'left',
                text_size=(240,None),
                  )

def profileSelectionButtonTextSet(profileName):
    btntext=kivy.utils.escape_markup(profileName)
    profileSelection.text = '[size=14][color=000000]' + btntext
profileSelectionButtonTextSet(getCurrentProfile())
#For the dropdown, the max_height is set to 400.
#This means, that up to 20 profiles can fit before scroll starts
#being relevant.
d = DropDown(max_height=410, bar_width=15)
for profile in getListOfProfiles():
    btn = Button(text=profile, color=(0,0,0,1), size_hint_y=None, height=20,
                 background_normal = PICPATH+'/dropdown_choice.png',
                 halign = 'left', text_size = (240,None))
    btn.bind(on_press=lambda btn: d.select(btn.text))
    d.add_widget(btn)
                                 
#add profile button, a simple button
createProfileButton = Button( size_hint = (None,None),
                              size = (120,25),
                              pos_hint = {'x':0.03, 'y':0.1},
                              background_normal = PICPATH+'/button_up.png',
                              background_down = PICPATH+'/button_down.png',
                              font_name = font,
                              text = "[color=000000][size=15]New profile",
                              markup=True)


#Profile name box
#Consists, like the profile selection, of a BoxLayout with 2 components,
# a label with explanation text and the textbox

profileNameBox = BoxLayout(orientation='vertical',
                           size_hint = (0.4, 0.5),
                           pos_hint = {'x':0.55, 'y':0.2})

profileNameBox.add_widget(Label(text='[color=000000][b]Change profile name',
                                  markup=True,
                                size_hint_y = 0.8))
                           
profileNameTextBox = TextInput(multiline = False,
                               font_size = 13)

def profileNameTextBoxTextSet(profileName):
    text=kivy.utils.escape_markup(profileName)
    profileNameTextBox.text = text
    
profileNameTextBoxTextSet(getCurrentProfile()) #TODO

profileNameBox.add_widget(profileNameTextBox)

#delete profile button
deleteProfileButton = Button(size_hint = (None, None), size = (120,25),
                            pos_hint = {'x':0.25, 'y':0.1},
                            text='[color=000000]Delete profile',
                            markup = True,
                            background_normal = PICPATH+'/button_up.png',
                            background_down = PICPATH+'/button_down.png')

#bind actions
#updates both choose profiles text, and profile name bar.
def updateTextBoxes(profileName):
    profileSelectionButtonTextSet(profileName)
    profileNameTextBoxTextSet(profileName)
    profileNameTextBox.cancel_selection()
    profileNameTextBox.focus = False
    titleMappings.text = '[color=000000][b][size=30]' + profileName

#profile chooser action
profileSelection.bind(on_release=d.open)
def pickProf(inst, name):
    updateTextBoxes(name)
    selectProfile(name)
d.bind(on_select=pickProf)

#name text box action
def profileNameTextBoxAction(txtbox):
    editProfile(getCurrentProfile(), txtbox.text)
    updateTextBoxes(txtbox.text)
profileNameTextBox.bind(on_text_validate = profileNameTextBoxAction)

#create profile button action
def createProfileButtonAction(btn):
    newProfileName = createProfile('Untitled Profile')
    updateTextBoxes(newProfileName)
    profileNameTextBox.focus = True
    profileNameTextBox.select_all()
createProfileButton.bind(on_release=createProfileButtonAction)

#delete profile button
def deleteProfileButtonAction(btn):
    confirm.open("Are you sure you want to delete profile\n" +
                 getCurrentProfile() + "?", delProf)

def delProf():
    removeProfile(getCurrentProfile())
    updateTextBoxes(getCurrentProfile())
    
deleteProfileButton.bind(on_release = deleteProfileButtonAction)

# -------------------Main Area -----------------------------#

#main title
titleMappings = Label(text='[color=000000][b][size=30]' + getCurrentProfile(),
                      size_hint=(1,0.1),
                      pos_hint={'y':0.91},
                      markup = True)

#Labels for Gestures and Windows Functions
gestureLabel = Label(text='[color=000000][b][size=16]Gesture',
                     size_hint=(0.2,0.05),
                     pos_hint={'x':0.16,'y':0.85},
                     font_name = font,
                     markup = True)

macroLabel = Label(text='[color=000000][b][size=16]Windows Function',
                   size_hint=(0.2,0.05),
                   pos_hint={'x':0.52, 'y':0.85},
                   font_name = font,
                   markup = True)

mcreator = MacroCreator(size = (200, 75), size_hint=(None,None),
                            pos_hint = {'x':0.02,'y':0.04})

#gcreator = GestureCreator(size = (200, 75), size_hint=(None,None),
#                            pos_hint = {'x':0.02,'y':0.04})
# mapping thingy

mappingBox = MappingDisplay(size = (500, 275), size_hint=(None,None),
                            pos_hint = {'x':0.05,'y':0.1})
#mappingBox.pos_hint = {'x':0.1,'y':0.1}
                           # pos_hint={'x':0.2, 'y':0.2})
mappingBox.mappingImagePath = PICPATH+'/mapping_border.png'
mappingBox.deleteButtonImagePathUp = PICPATH+'/button_up.png'
mappingBox.deleteButtonImagePathDown = PICPATH+'/button_down.png'
mappingBox.gestureEditButtonImageUp = PICPATH+'/button_up.png'
mappingBox.gestureEditButtonImageDown = PICPATH+'/button_down.png'
mappingBox.macroEditButtonImageUp = PICPATH+'/button_up.png'
mappingBox.macroEditButtonImageDown = PICPATH+'/button_down.png'
for mapp in getListOfMappings(getCurrentProfile()):
    mappingBox.addMapping(mapp)

#add mapping button
addMappingButton = Button(text = '[size=14][color=000000]New Mapping',
                          size_hint = (None,None),
                          size = (110,20),
                          pos_hint = {'x':0.8,'y':0.85},
                          markup=True,
                          background_normal = PICPATH+'/button_up.png',
                          background_down = PICPATH+'/button_down.png')
counter = [1]
addMappingButton.bind(on_release=lambda btn:createMapping(counter))

#popups from infobutton
gesturePopup = EventPopup('gesture')
macroPopup = EventPopup('macro')

#bind buttons to call these two functions
def displayEditMappingPopup(index, gestOrMacro):
    if gestOrMacro == 'gesture':
        allEvents=getListOfGestures()
        gesturePopup.setDropdownWithExplanation(allEvents)
        gesturePopup.open(index)
    elif gestOrMacro == 'macro':
        allEvents=getListOfMacros()
        macroPopup.setDropdownWithExplanation(allEvents)
        macroPopup.open(index)


############
# Manage custom events
############

'''
This is the class CustomizeEventPopup.

It is the popup that pops up when the user clicks on the button
"customize" in the event popup. Basically, the class consists of a
popup (opens with open()), with a title and a content (of course...).
The content is a floatlayout with three components: one ListView for
listing all custom events, and two buttons: create new and done.
The create button calls either the createMacro() function, or the
more complicated createGestureCallback(). The Done button simply dismisses
the popup. Each component in the listview is either a CustomGestureWidget
or a CustomMacroWidget. More info on them below.

To use the popup, two instances have already been created. Simply call
cepg.open() or cegm.open() to open the popups. 
'''


class CustomizeEventPopup(Popup):
    gestureOrMacro = "gesture"
    container = None

    def __init__(self, gestureOrMacro, **kwargs):
        super(CustomizeEventPopup, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.auto_dismiss = False
        self.gestureOrMacro = gestureOrMacro
        content = FloatLayout()
        self.container = content

        #set create button
        createBtn = Button(size_hint = (None, None), size = (150, 25),
                           pos_hint = {'x': 0.05, 'y': 0.03}, markup = True,
                           background_normal = PICPATH+'/button_up.png',
                           background_down = PICPATH+'/button_down.png')
        def createBtn_callback(btn):
            if gestureOrMacro == 'gesture':
                createGestureCallback()
            else:
                createMacro()
                self.refresh()
        createBtn.bind(on_release=createBtn_callback)
        
        #set done button
        doneBtn = Button(size_hint = (None, None), size = (150, 25),
                         text = "[color=000000]Done", markup = True,
                         pos_hint = {'right': 0.95, 'y': 0.03},
                         background_normal = PICPATH+'/button_up.png',
                         background_down = PICPATH+'/button_down.png')
        doneBtn.bind(on_release=lambda(btn):self.dismiss())

        #Do some event-specific stuff
        if gestureOrMacro == "gesture":
            self.title = "Manage Custom Gestures"
            createBtn.text = "[color=000000]Create new gesture"
        else:
            self.title = "Manage Custom Macros"
            createBtn.text = "[color=000000]Create new macro"

        #add widgets
        content.add_widget(doneBtn)
        content.add_widget(createBtn)
        self.container = ListView(25, size_hint = (None, None),
                                    size = (340, 260),
                                    pos_hint = {'x':0, 'y':0.2})
        content.add_widget(self.container)
        self.content = content
        

        self.refresh()
        
    def refresh(self):
        while len(self.container.box.children) > 0:
            self.container.remove_widget(self.container.box.children[0])
        if self.gestureOrMacro == 'gesture':
            eventList = getListOfCustomGestures()
        else:
            eventList = getListOfCustomMacros()
        i = 0
        for event in eventList:
            if self.gestureOrMacro == 'gesture':
                self.container.add_widget(CustomGestureWidget(i, self, event))
            else:
                self.container.add_widget(CustomMacroWidget(i, self, event))
            i += 1


'''
For context, see comment above class CustomizeEventPopup.
This is a boxlayout with 2 components: one label with the gesture name,
and a button for deleting this gesture. Note that the "label" is actually
a button, but its fine because Button actually inherits from Label, and
in the button you can set background image.
'''

class CustomGestureWidget(BoxLayout):
    index = 0
    owner = None
    name = "My gesture"
    
    def __init__(self, index, owner, name, **kwargs):
        super(CustomGestureWidget, self).__init__(**kwargs)
        #set various variables
        self.index = index
        self.owner = owner
        self.name = name
        self.spacing = 3
        #now create button
        delBtn = Button(text='Delete', font_size = 12, color = (0,0,0,1),
                        background_normal = PICPATH+'/button_up.png',
                        background_down = PICPATH+'/button_down.png')
        #bind button
        def delBtn_callback(btn):
            removeGesture(name)
            owner.refresh()
            print "Removing gesture ", name
        delBtn.bind(on_release=delBtn_callback)
        #build self
        self.add_widget(Button(text=name, color = (0,0,0,1),
                        text_size = (260,None), halign='left',
                        size_hint_x = 4.5, font_size = 12,
                        background_normal = PICPATH+'/dropdown_choice.png',
                        background_down = PICPATH+'/dropdown_choice.png'))
        self.add_widget(delBtn)

        
'''
For context, see comment above class CustomizeEventPopup.
This is similar to the CustomGestureWidget, except that there also is a
button for editing this macro, which calls the EditMacroCallback function.
'''

class CustomMacroWidget(BoxLayout):
    index = 0
    owner = None
    name = "My macro"
    
    def __init__(self, index, owner, name, **kwargs):
        super(CustomMacroWidget, self).__init__(**kwargs)
        #set various variables
        self.index = index
        self.owner = owner
        self.name = name
        self.spacing = 3
        #now create buttons
        editBtn = Button(text='Edit', font_size = 12, color = (0,0,0,1),
                         background_normal = PICPATH+'/button_up.png',
                         background_down = PICPATH+'/button_down.png')
        delBtn = Button(text='Delete', font_size = 12, color = (0,0,0,1),
                        background_normal = PICPATH+'/button_up.png',
                        background_down = PICPATH+'/button_down.png')

        #bind buttons
        editBtn.bind(on_release=lambda(btn):editMacroCallback(name))
        def delBtn_callback(btn):
            print "Removing macro ", name
            removeMacro(name)
            owner.refresh()
        delBtn.bind(on_release=delBtn_callback)
        
        #build self
        self.add_widget(Button(text=name, color = (0,0,0,1),
                        text_size = (220,None), halign='left',
                        size_hint_x = 4.5, font_size = 12,
                        background_normal = PICPATH+'/dropdown_choice.png',
                        background_down = PICPATH+'/dropdown_choice.png'))
        self.add_widget(editBtn)
        self.add_widget(delBtn)


#### End classes

#### End classes definitions


cepg = CustomizeEventPopup('gesture')
cepm = CustomizeEventPopup('macro')

def manageGestures():
    cepg.open()

def manageMacros():
    cepm.open()

#####################################################
## Create events functions, classes and popups here
#####################################################

class EditMacroPopup(Popup):
    textAreaName = None
    textAreaDesc = None
    textAreaScript = None
    container = None
    macro = "the awesome macro"
    
    def __init__(self, **kwargs):
        super(EditMacroPopup, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (500, 500)
        self.title = "Edit macro"
        self.title_size = 20
        self.auto_dismiss = False
        container = FloatLayout()

        #create buttons
        acceptButton = Button(size_hint = (None, None), size = (120, 26),
                              pos_hint = {'x':0.05, 'y':0}, color = (0,0,0,1),
                              text = "Accept",
                              background_normal = PICPATH+'/button_up.png',
                              background_down = PICPATH+'/button_down.png')
        def acceptButton_callback(btn):
            editMacro(self.textAreaName.text, self.textAreaScript.text,
                      'text', self.textAreaDesc.text)
            cepm.refresh()
            self.dismiss()
        acceptButton.bind(on_release=acceptButton_callback)
        cancelButton = Button(size_hint = (None, None), size = (120, 26),
                              pos_hint = {'right':0.95, 'y':0}, color = (0,0,0,1),
                              text = "Cancel",
                              background_normal = PICPATH+'/button_up.png',
                              background_down = PICPATH+'/button_down.png')
        cancelButton.bind(on_release=lambda(btn):self.dismiss())

        #create textinputs
        self.textAreaName = TextInput(multiline = False, font_size = 13,
                                      size_hint = (0.4, 0.07),
                                      pos_hint = {'x':0, 'y': 0.88})
        self.textAreaDesc = TextInput(multiline = True, font_size = 13,
                                      size_hint = (0.4, 0.2),
                                      pos_hint = {'x':0, 'y': 0.63})
        self.textAreaScript = TextInput(multiline = True, font_size = 11,
                                      size_hint = (1, 0.47),
                                      pos_hint = {'x':0, 'y': 0.1})

        #add widgets
        container.add_widget(Label(font_size=15, text="Macro name",
                                   size_hint = (1, 0.05),
                                   pos_hint = {'x':0, 'y':0.95},
                                   halign='left', text_size=(450,None)))
        container.add_widget(self.textAreaName)
        container.add_widget(Label(font_size=15, text="Macro description",
                                   size_hint = (1, 0.05),
                                   pos_hint = {'x':0, 'y':0.83},
                                   halign='left', text_size=(450,None)))       
        container.add_widget(self.textAreaDesc)
        container.add_widget(Label(font_size=15, text="Macro script",
                                   size_hint = (1, 0.05),
                                   pos_hint = {'x':0, 'y':0.57},
                                   halign='left', text_size=(450,None)))        
        container.add_widget(self.textAreaScript)
        container.add_widget(acceptButton)
        container.add_widget(cancelButton)

        self.container = container
        self.content = container

    def open(self, macro):
        '''overriding open function'''
        self.macro = macro
        macInfo = getMacroInfo(macro)
        self.textAreaName.text = macInfo[0]
        self.textAreaDesc.text = macInfo[3]
        self.textAreaScript.text = macInfo[1]
        super(EditMacroPopup, self).open()
        

######## Edit macros
emp = EditMacroPopup()
        
def editMacroCallback(macro):
    emp.open(macro)

def createGestureCallback():
    print "Will now open create gesture popup"
    pass;

#def createMacro():
#    pass;


##################################################################
# ------------------Main building class ------------------------_#
##################################################################
class GestureMapper(App):

    def build(self):
        root = TouchArea(orientation='vertical')
        #top bar, choose profile bar
        #topBar = StencilView()
        topBar = FloatLayout(size_hint=(1,0.3))
        topBar.add_widget(profileBarImg)       #background image
        topBar.add_widget(profileSelection)    #profile selection
        topBar.add_widget(profileSelectionLabel) #profile selection title label
        topBar.add_widget(profileNameBox)      #profile renaming
        topBar.add_widget(createProfileButton) #create profile button
        topBar.add_widget(deleteProfileButton)

        #this part below does so that when the user clicks somewhere
        #on the topbar which is not in the profile name text box.
        #In that case, the action is the same as normal press of "enter".
        #Its a small but convinient quality change
        def touch_unfocus_profileNameBox(self, touch):
            if not profileNameTextBox.collide_point(touch.x, touch.y) \
               and profileNameTextBox.focus == True:
            
                profileNameTextBoxAction(profileNameTextBox)
        
        topBar.bind(on_touch_down = touch_unfocus_profileNameBox)

        #main area
        mainArea = FloatLayout()
        mainArea.add_widget(mainBackgroundImg)
        mainArea.add_widget(titleMappings)
        mainArea.add_widget(macroLabel)
        mainArea.add_widget(gestureLabel)
        mainArea.add_widget(mappingBox)
        #mainArea.add_widget(mcreator)
        mainArea.add_widget(addMappingButton)
        #updateMappings()
       
        #add all to root
        root.add_widget(topBar)
        root.add_widget(mainArea)
        
        return root


#kristoffers klass
class TouchArea(BoxLayout):

    #On touch events
    def on_touch_down(self, touch):
        print "Touch down!"
        print "Touch uid: " + str(touch.uid)

        if len(EventLoop.touches) > 1:
            print "Multi touch!"
        
        if str(touch.device) == "mouse":
            super(TouchArea, self).on_touch_down(touch)
        elif str(touch.device) == "multitouchtable":
            Controller.on_touch_down(touch)
        

    def on_touch_move(self, touch):
        print "Touch move!"
        print "uid: " + str(touch.uid)
        if str(touch.device) == "mouse":
            super(TouchArea, self).on_touch_move(touch)
        elif str(touch.device) == "multitouchtable":
            Controller.on_touch_down(touch)
        

    def on_touch_up(self, touch):
        print "Touch up!"
        print "uid: " + str(touch.uid)
        if str(touch.device) == "mouse":
            super(TouchArea, self).on_touch_up(touch)
        elif str(touch.device) == "multitouchtable":
            Controller.on_touch_down(touch)


#and Main

if __name__ == '__main__':
    GestureMapper().run()

