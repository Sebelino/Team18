from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.stencilview import StencilView

##################################################################
#-------------------- Load Images -------------------------------#
##################################################################
profileBarImg = Image(allow_stretch=True, keep_ratio=False,
                      source='pics/happysign.png',
                      size_hint=(1,1),
                      pos_hint={'y':0})
mainBackgroundImg = Image(allow_stretch=True, keep_ratio=False,
                          source='pics/art.png',
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
    return ['wave', 'punch', 'faint']

def getListOfMacros():
    """Returns a list of Macros/Windows Functions, requested from Controller."""
    #TODO
    return ['leftclick', 'rightclick', 'middleclick']


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
def createMapping():
    """ Creates a new mapping with default values."""
    #TODO
    pass

def editMapping(index, editGesture, editMacro, newGesture, newMacro):
    """ Edits the mapping with the given index.

    The parameters specify:
    editGesture - boolean value, if the gesture is changing.
    editMacro - boolean value, if the Windows macro/function is changing.
    newGesture - Gesture value, the new Gesture.
                  (does nothing if editGesture is False).
    newMacro - Macro value, the new Windows Macro/Function.
                   (does nothing if editMacro is False)."""
    #TODO
    #Change function parameters/arguments perhaps
    pass

def removeMapping(index):
    """ Removes the mapping with the given index."""
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

#Profile name box
profileNameTextBox = TextInput( size_hint = (0.3, profileBarHeight),
                                pos_hint = {'x':0.65, 'y':profileBarPosY},
                                text = getCurrentProfile(),
                                multiline = False
                                )



#This is the profile selection thing.
#currently, its a button that opens a drop down menu
chooseProfileWidget = Button(text='flu',
                        size_hint=(0.3,profileBarHeight),
                        pos_hint={'x':.15, 'y':profileBarPosY})

d = DropDown(max_height=100, bar_width=15)

for profile in getListOfProfiles():
    btn = Button(text=profile, color=(0,0,0,1), size_hint_y=None, height=20)
    btn.bind(on_release=lambda btn: d.select(btn.text))
    d.add_widget(btn)




#add profile button
createProfileButton = Button( size_hint = (0.05, profileBarHeight),
                              pos_hint = {'x':0.5, 'y':profileBarPosY},
                              background_normal = 'pics/plus_btn_up.png',
                              background_down = 'pics/plus_btn_down.png')

#delete profile button
deleteProfileButton = Button( size_hint = (0.05, profileBarHeight),
                              pos_hint = {'x':0.75, 'y':0.3},
                              background_normal = 'pics/cross_btn_up.png',
                              background_down = 'pics/cross_btn_down.png')

#bind actions
#updates both choose profiles text, and profile name bar.
def updateTextBoxes(profileName):
    chooseProfileWidget.text = profileName
    profileNameTextBox.text = profileName

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

#profile chooser action
chooseProfileWidget.bind(on_release=d.open)
def pickProf(inst, name):
    updateTextBoxes(name)
    selectProfile(name)
d.bind(on_select=pickProf)

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

# mappings stuff
mappingBox = ScrollView(do_scroll_x = False,
                        size_hint=(1, 0.7),
                        pos_hint={'y':0.1})
mappingBoxContent = FloatLayout()
mappingBoxContent.add_widget(blackBorderImg)
mappingBox.add_widget(mappingBoxContent)


heightOfAMapping = 32



def updateMappings():
    """ A general function for updating the shown mappings. """
    mappingBoxContent.clear_widgets()
    index = 0
    for mapping in getListOfMappings(getCurrentProfile()):
        boxBackground = FloatLayout(size_hint=(1,0.2))
        box = BoxLayout(orientation='horizontal')#, height = heightOfAMapping)
        boxBackground.add_widget(Image(allow_stretch=True, keep_ratio=False,
                                       source='pics/mapping_border.png',
                                       size_hint=(1,1),
                                       pos_hint={'y':0}))
        #create delete button
        delButton = Button(size_hint=(0.05, 0.9),
                           #pos_hint={'x':0.03 ,'y':0.05},
                           background_normal='pics/cross_btn_up.png',
                           background_down = 'pics/cross_btn_down.png')
        delButton.bind(on_release=lambda btn: removeButtonActions(index))
        box.add_widget(delButton)

        boxBackground.add_widget(box)
        mappingBoxContent.add_widget(boxBackground)
        index += 1
        
def removeButtonActions(index):
    removeMapping(index)
    updateMappings()

##################################################################
# ------------------Main building class ------------------------_#
##################################################################
class MainGUI(App):

    def build(self):
        root = BoxLayout(orientation='vertical')
        #top bar, choose profile bar
        #topBar = StencilView()
        topBar = FloatLayout(size_hint=(1,0.3))
        topBar.add_widget(profileBarImg)
        topBar.add_widget(chooseProfileWidget)
        topBar.add_widget(profileNameTextBox)
        topBar.add_widget(createProfileButton)
        topBar.add_widget(deleteProfileButton)

        #main area
        mainArea = FloatLayout()
        mainArea.add_widget(mainBackgroundImg)
        mainArea.add_widget(titleMappings)
        mainArea.add_widget(mappingBox)
        updateMappings()
       
        #add all to root
        root.add_widget(topBar)
        root.add_widget(mainArea)
        return root
        

#and Main

if __name__ == '__main__':
    MainGUI().run()
