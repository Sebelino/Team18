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

##################################################################
#---------------------- Config ----------------------------------#
##################################################################

"""Create a small cute window, unresizeable"""

Config.set('kivy','window_icon', 'smiley_ic.png')
Config.set('graphics','fullscreen',0)
Config.set('graphics','resizable',0)
Config.set('graphics','width',650)
Config.set('graphics','height',500)


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
    mappingHeight = 40
    proportions = (0.08, 0.3, 0.11, 0.40, 0.11)
    positions = [1,1,1,1,1]
    sizes = [1,1,1,1,1]
    
    def __init__(self,**kwargs):
        #call the constructor of the flowlayout
        #this exists to keep the standard kivy syntax
        super(MappingDisplay,self).__init__(**kwargs)

        scroll = ScrollView(bar_width=15,
                            do_scroll_y = True,
                            do_scroll_x = False,
                            pos_hint= {'x':0,'y':0},
                            size_hint = (None,None),
                            size = self.size)
        
        self.layout = BoxLayout(orientation='vertical',size_hint=(None,None),
                                size = self.size)
        scroll.add_widget(self.layout)
        self.add_widget(scroll)
        pos = 0
        self.positions[0] = 0
        self.sizes[0] = int(self.size[0] * self.proportions[0])
        for i in range(1,5):
            self.sizes[i] = int(self.size[0] * self.proportions[i])
            self.positions[i] = self.proportions[i-1] + self.positions[i-1]     

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
        border_y = 0.05
        delBtn = Button(background_normal = self.deleteButtonImagePathUp,
                        background_down = self.deleteButtonImagePathDown,
                        pos_hint={'x':0.01, 'y':border_y},
                        size_hint = (None,None),
                        size = (self.mappingHeight - border*2, \
                                self.mappingHeight - border*2)
                        )
        
        gesture = Label(color = (0,0,0,1),
                        text = mapping[0],
                        bold = True,
                        pos_hint = {'x':self.positions[1], 'y':border_y},
                        size_hint = (None,None),
                        size = (self.sizes[1] - border*2, \
                                self.mappingHeight - border*2)
                        )
        
        gestureInfoBtn = Button(background_normal = self.gestureEditButtonImageUp,
                                background_down = self.gestureEditButtonImageDown,
                                pos_hint = {'x':self.positions[2], 'y':border_y},
                                size_hint = (None,None),
                                size = (self.mappingHeight - border*2, \
                                        self.mappingHeight - border*2)
                                )
        
        macro = Label(color = (0,0,0,1),
                      text = mapping[1],
                      bold = True,
                      pos_hint = {'x':self.positions[3], 'y':border_y},
                      size_hint = (None,None),
                      size = (self.sizes[3] - border*2, \
                              self.mappingHeight - border*2)
                      )
        
        macroInfoBtn = Button(background_normal = self.macroEditButtonImageUp,
                              background_down = self.macroEditButtonImageDown,
                              pos_hint = {'x':self.positions[4], 'y':border_y},
                              size_hint = (None,None),
                              size = (self.mappingHeight - border*2, \
                                      self.mappingHeight - border*2)
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

##################################################################
#-------------------- Load Images -------------------------------#
##################################################################
profileBarImg = Image(allow_stretch=True, keep_ratio=False,
                      source='pics/background_top.png',
                      size_hint=(1,1),
                      pos_hint={'y':0})
mainBackgroundImg = Image(allow_stretch=True, keep_ratio=False,
                          source='pics/background_bot.png',
                          size_hint=(1,1),
                          pos_hint={'y':0})
blackBorderImg = Image(allow_stretch=True, keep_ratio=False,
                       source='pics/black_border.png',
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
    return ['Hue','Boo','Traktor']

def getCurrentProfile():
    """Returns the currently selected profile, requested from Controller."""
    #TODO
    return getListOfProfiles()[0]
    

def getListOfMappings(profile):
    """Returns a list of mappings, requested from Controller."""
    #TODO
    return [('yes','no'), ('click','boom')]

def getListOfGestures():
    """Returns a list of available Gestures, requested from Controller."""
    #TODO
    return [('wave', TextInput(text='WAVE\nJO\nNEJ\nblod',readonly = True)),
            ('punch',TextInput(text='kALABALALAMMMMMMMMMMMMmmmASDN',readonly = True)),
            ('faint', Image(source='pics/happysign.png', allow_stretch=True,
                            keep_ratio=False))]

def getListOfMacros():
    """Returns a list of Macros/Windows Functions, requested from Controller."""
    #TODO
    return [('leftclick', TextInput(text='U DUNNO WUT LEFTCLICK IS',readonly = True)),
            ('rightclick',TextInput(text='RaaALABALALAMMMMMMMMMMMMMMMMMMMMMmmmASDN',readonly = True)),
            ('faint', Image(source='pics/art.png', allow_stretch=True,
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
jojo = 0
def createMapping():
    jojo = 0
    """ Creates a new mapping with default values."""
    mappingBox.addMapping(('Gesture' + str(jojo), 'Macro' + str(jojo)))
    jojo += 1
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

profileBarPosY = 0.65
profileBarHeight = 0.25

#Profile selection, is a boxlayout with 2 components:
#1. a label with a static text saying "current profile"
#2. A button with a dropdown Menu for the profile selection action
profileSelection = BoxLayout(orientation='vertical',
                             size_hint = (0.4,0.6),
                             pos_hint = {'x':0.05,'y':0.3})

profileSelection.add_widget(Label(text='[color=000000][b] Current profile' \
                                        '[/b][/color]',
                                  markup=True,
                                  size_hint_y=0.35))

profileSelectionButton = Button(markup=True,
                background_normal='pics/button_profile_selection_up.png',
                background_down='pics/button_profile_selection_down.png'    )
def profileSelectionButtonTextSet(profileName):
    btntext=kivy.utils.escape_markup(profileName)
    profileSelectionButton.text = '[size=14][color=000000]' + \
                                  btntext + '[/color][/size]'
profileSelectionButtonTextSet(getCurrentProfile())

d = DropDown(max_height=100, bar_width=15)
for profile in getListOfProfiles():
    btn = Button(text=profile, color=(0,0,0,1), size_hint_y=None, height=20,
                 background_normal = 'pics/dropdown_choice.png')
    btn.bind(on_press=lambda btn: d.select(btn.text))
    d.add_widget(btn)

profileSelection.add_widget(profileSelectionButton)
                                 
#add profile button, a simple button
createProfileButton = Button( size_hint = (None,None),
                              size = (40,40),
                              pos_hint = {'x':0.48, 'y':0.35},
                              background_normal = 'pics/plus_btn_up.png',
                              background_down = 'pics/plus_btn_down.png')


#Profile name box
#Consists, like the profile selection, of a BoxLayout with 2 components,
# a label with explanation text and the textbox

profileNameBox = BoxLayout(orientation='vertical',
                           size_hint = (0.37, 0.5),
                           pos_hint = {'x':0.62, 'y':0.5})

profileNameBox.add_widget(Label(text='[color=000000][b] Profile name' \
                                        '[/b][/color]',
                                  markup=True))
                           
profileNameTextBox = TextInput(multiline = False,
                               font_size = 13)

def profileNameTextBoxTextSet(profileName):
    text=kivy.utils.escape_markup(profileName)
    profileNameTextBox.text = text
    
profileNameTextBoxTextSet(getCurrentProfile()) #TODO

profileNameBox.add_widget(profileNameTextBox)

#delete profile button
deleteProfileButton = Button(size_hint = (None, None), size = (100,35),
                            pos_hint = {'x':0.75, 'y':0.15},
                            text='[color=443333]Delete profile',
                            markup = True,
                            background_normal = 'pics/button_profile_delete_up.png',
                            background_down = 'pics/button_profile_delete_down.png')

#bind actions
#updates both choose profiles text, and profile name bar.
def updateTextBoxes(profileName):
    profileSelectionButtonTextSet(profileName)
    profileNameTextBoxTextSet(profileName)
    profileNameTextBox.cancel_selection()
    profileNameTextBox.focus = False

#profile chooser action
profileSelectionButton.bind(on_release=d.open)
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
titleMappings = Label(text='[color=000000][b][size=36]Mappings[/size][/b][/color]',
                      size_hint=(1,0.1),
                      pos_hint={'y':0.9},
                      markup = True)

# mapping thingy

mappingBox = MappingDisplay(size = (500, 275), size_hint=(None,None),
                            pos_hint = {'x':0.05,'y':0.1})
#mappingBox.pos_hint = {'x':0.1,'y':0.1}
                           # pos_hint={'x':0.2, 'y':0.2})
mappingBox.mappingImagePath = 'pics/mapping_border.png'
mappingBox.deleteButtonImagePathUp = 'pics/cross_btn_up.png'
mappingBox.deleteButtonImagePathDown = 'pics/cross_btn_down.png'
mappingBox.gestureEditButtonImageUp = 'pics/info_btn_up.png'
mappingBox.gestureEditButtonImageDown = 'pics/info_btn_down.png'
mappingBox.macroEditButtonImageUp = 'pics/info_btn_up.png'
mappingBox.macroEditButtonImageDown = 'pics/info_btn_down.png'
for mapp in getListOfMappings(getCurrentProfile()):
    mappingBox.addMapping(mapp)

#add mapping button
addMappingButton = Button(text = '[size=14][color=55ff55]Create Mapping',
                          size_hint = (None,None),
                          size = (120,30),
                          pos_hint = {'x':0.75,'y':0.90},
                          markup=True)
addMappingButton.bind(on_release=lambda btn:createMapping())

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
        topBar.add_widget(profileNameBox)      #profile renaming
        topBar.add_widget(createProfileButton) #create profile button
                               
        topBar.add_widget(deleteProfileButton)
        

        #main area
        mainArea = FloatLayout()
        mainArea.add_widget(mainBackgroundImg)
        mainArea.add_widget(titleMappings)
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
