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

import thread
import time
import os
import sys
import DatabaseAdapter as db
from kivy.base import EventLoop

def executeController():
    time.sleep(1)
    os.system("python Controller.py")

thread.start_new_thread(executeController,())

gestures = db.getGestures()
print(gestures[0][0])
print(gestures[1][0])

##################################################################
#---------------------- Config ----------------------------------#
##################################################################

"""Create a small cute window, unresizeable"""

Config.set('kivy','window_icon', 'smiley_ic.png')
Config.set('graphics','fullscreen',0)
Config.set('graphics','resizable',0)
Config.set('graphics','width',650)
Config.set('graphics','height',500)

PICPATH = '../pics'
font = '../font/segoeui.ttf'

######################################################
## -----------------------Mapping Display Class -----#
######################################################
"""
OK, so, this class exists as a component that keeps all the
mappings in a neat scrollable list. Because it might be a mess,
and I might forget stuff, here are some important info about
usage:

1. When creating this object, MUST set the attributes size and
   size_hint. Size will be the size of the widget, and size_hint
   should be set to (None, None), otherwise the behavior is undefined.
2. Attribute mappingHeight is the height of one mapping, it better be
   set before adding mappings (althought it is set to 40 by default),
   otherwise it will break.
3. Attribute proportions are the sizes, in percentages, of each of the
   five components of a mapping. Better also be changed before adding
   mappings, otherwise will break (set by default though).
4. There are lots of options for setting Images, attributes should have
   (long :/) describing names. Set images before adding mappings.
5. When adding a mapping, it should be in the format of a tuple with
   two string attributes. Otherwise, might get exceptions.
6. MappingDisplay is a FloatLayout with two children: a background
   image and a ScrollView. If adding children directly, it will behave
   like a FloatLayout. The ScrollView contains a BoxLayout with
   vertical orientation. One annoying thing is that BoxLayout has its
   children positioned from the bottom and up, while I want it the other
   way. Anyway, its taken care of in the code. Just keep in mind for the
   Controller, that when a mapping is created, put it last in the list.
"""
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

    #TODO - solve this somehow.
    #Buttons in the scrollview dont work if this part below
    # is not commented away
    '''On touch events'''
    
    def on_touch_down(self, touch):
        print str(touch.device)
        if str(touch.device) == "multitouchtable":
            print "touch"
        elif str(touch.device) == "mouse":
            print "mouse click"
            super(MappingDisplay, self).on_touch_down(touch)
  
    '''End of on-touch events'''

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
                        bold = True,
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
                      bold = True,
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
    return getListOfProfiles()[0]
    

def getListOfMappings(profile):
    """Returns a list of mappings, requested from Controller."""
    #TODO
    return db.getMappings()

def getListOfGestures():
    """Returns a list of available Gestures, requested from Controller."""
    #TODO
    return [('KameHameHA', TextInput(text='WAVE\nJO\nNEJ\nblod',readonly = True)),
            ('punch',TextInput(text='kALABALALAMMMMMMMMMMMMmmmASDN',readonly = True)),
            ('Hadoken',TextInput(text='kALABALALAMMMMMMMMMMMMmmmASDN',readonly = True)),
            ('Two-finger swipe', Image(source=PICPATH+'/two_swipe.gif', allow_stretch=True,
                            keep_ratio=False))]

def getListOfMacros():
    """Returns a list of Macros/Windows Functions, requested from Controller."""
    #TODO
    return [('leftclick', TextInput(text='U DUNNO WUT LEFTCLICK IS',readonly = True)),
            ('rightclick',TextInput(text='RaaALABALALAMMMMMMMMMMMMMMMMMMMMMmmmASDN',readonly = True)),
            ('faint', Image(source=PICPATH+'/art.png', allow_stretch=True,
                            keep_ratio=False))]


#-------- Profile management ---------#

def createProfile(profileName):
    """ Creates a new profile with the given name.

    Must return the name of the newly created profile."""
    #TODO
    print "creating profile " + profileName
    return profileName

def editProfile(oldProfileName, newProfileName):
    """ Changes the name of a profile to the new name."""
    print "changing name from " + oldProfileName + " to " + newProfileName 
    #TODO
    pass

def selectProfile(profileName):
    """ Selects the profile with the given name."""
    print "selecting profile " + profileName
    #TODO
    pass

def removeProfile(profileName):
    """ Removes the profile with the given name."""
    print "removing profile " + profileName
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
def createMacro(macro):
    """ Creates a new Macro. """
    pass

def removeMacro(macro):
    """ Removes the specified Macro. """
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

class IndexButton(Button):
    index = 0
    def __init__(self,**kwargs):
        super(IndexButton,self).__init__(**kwargs)

#bind buttons to call these two functions
def displayEditMappingPopup(index, gestOrMacro):
    if gestOrMacro == 'gesture':
        allEvents=getListOfGestures()
    elif gestOrMacro == 'macro':
        allEvents=getListOfMacros()
    content = BoxLayout(orientation='vertical')
    #Dropdown for choosing gesture/macro
    pickEventBtn = Button(size_hint_y=0.25, text=allEvents[0][0])
    dd = DropDown(max_height=100, bar_width=5)

    i = 0
    for eve in allEvents:
        btn = IndexButton(text=eve[0], color=(0,0,0,1), size_hint_y=None, height=20)
        btn.index = i
        btn.bind(on_release=lambda btn: selectEvent(btn.index))
        dd.add_widget(btn)
        i += 1
    def selectEvent(ind):
        dd.select(ind)
        pickEventBtn.text=allEvents[ind][0]
        content.remove_widget(content.children[1])
        widge = allEvents[ind][1]
#        if isinstance(widge, TextInput):
#            def unfocus(inst,touch):
#                widge.focus = False
#            widge.bind(on_touch_up=unfocus)
#TODO move this binding to the gestListOfGestures method
        content.add_widget(widge,1)
    pickEventBtn.bind(on_release=dd.open)
    
#    dd.bind(on_select=pickGest)
    #Button that signals you're done
    doneBtn = Button(text='Done', size_hint_y=0.2)
    def doneBtn_callback(btn):
        if gestOrMacro == 'gesture':
            editMapping(index, pickEventBtn.text, None)
        elif gestOrMacro == 'macro':
            editMapping(index, None, pickEventBtn.text)
        popup.dismiss()
    doneBtn.bind(on_release=doneBtn_callback)

    #initialize starting values
    content.add_widget(pickEventBtn)
    content.add_widget(allEvents[0][1])
    content.add_widget(doneBtn)

    if gestOrMacro == 'gesture':
        title = 'Set gesture'
    elif gestOrMacro == 'macro':
        title = 'Set Windows Function'
    
    popup = Popup(title=title,
                  content=content,
                  size_hint=(None, None), size=(400, 300))
    popup.open()

##################################################################
# ------------------Main building class ------------------------_#
##################################################################
class GestureMapper(App):

    def build(self):
        root = BoxLayout(orientation='vertical')
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
        mainArea.add_widget(addMappingButton)
        #updateMappings()
       
        #add all to root
        root.add_widget(topBar)
        root.add_widget(mainArea)
        
        return root
        

#and Main

if __name__ == '__main__':
    GestureMapper().run()
