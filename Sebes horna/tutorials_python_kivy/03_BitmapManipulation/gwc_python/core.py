"""
////////////////////////////////////////////////////////////////////////////////
//
//  IDEUM
//  Copyright 2011-2013 Ideum
//  All Rights Reserved.
//
//  Gestureworks Core
//
//  File:    core.py
//  Authors:  Ideum
//
//  NOTICE: Ideum permits you to use, modify, and distribute this file only
//  in accordance with the terms of the license agreement accompanying it.
//
////////////////////////////////////////////////////////////////////////////////

Bindings for the GestureWorks Core library. See the README that accompanied this release for 
a detailed overview.

"""
from GWCUtils import _PointEventArray, _GestureEventArray, GestureEvent
from ctypes import cdll, POINTER, c_bool
import sys
    
class GestureWorksCore:

    """Attempts to load the GestureWorks DLL from the specified path. If no path is given,
    attempts to lead the DLL from the current directory.
     
    """
    def __init__(self, dll_path='.'):
        self.loaded_dll = True
        try:
            self._dll = cdll.LoadLibrary(dll_path)
        except WindowsError, e:
            print e
            if str(e).__contains__('Error 126'):
                sys.stderr.write('ERROR: Could not find GestureWorksCore DLL in the specified path.')
                print dll_path
            else:
                sys.stderr.write(str(e))
            self.loaded_dll = False

       
    """Initialize internal GestureWorks state
    
    screen width and height are given for the screen that will be receiving touch
    
    """     
    def initializeGestureWorks(self, screen_width=1920, screen_height=1080):
        if not self.loaded_dll:
            sys.stderr.write('ERROR: GestureWorksCore library was not properly loaded.')
            return
        self._dll.initializeGestureWorks(screen_width, screen_height)

    
    """Tell GestureWorks to process the current frame
    
    Returns True on success
    
    """
    def processFrame(self):
        if not self.loaded_dll:
            return False

        self._dll.processFrame()
        return True


    """Register the application window with GestureWorks for touch events
    
    name is the name of the process as Windows sees it.
    Returns True on success
    
    """
    def registerWindow(self, name):
        print "Registering", name
        if not self.loaded_dll:
            return False
        self._dll.registerWindowForTouchByName.restype = c_bool
        return self._dll.registerWindowForTouchByName(name)
       
        
    """Load GML definitions from the specified file.
    More than one GML file can be loaded.
    
    Returns True on success
    
    """
    def loadGML(self, gml_path):
        if not self.loaded_dll:
            return False
        self._dll.loadGML.restype = c_bool
        return self._dll.loadGML(gml_path)
       
        
    """Notify GestureWorks that the screen has been resized"""
    def resizeScreen(self, width, height):
        if not self.loaded_dll:
            return False
        self._dll.resizeScreen(width, height)
       
        
    """Get the point events that were created in the call to processFrame
    
    Returns a list of PointEvents
    
    """
    def consumePointEvents(self):
        if not self.loaded_dll:
            sys.stderr.write('ERROR: GestureWorksCore library was not properly loaded.')
            return
        self._dll.consumePointEvents.restype = POINTER(_PointEventArray)
        array = self._dll.consumePointEvents()[0]
        events = []
        for i in range(0, array.size):
            if not array.events[i]: break
            events.append(array.events[i])
        return events 
    
    
    """Get the gesture events that were created in the call to processFrame
    
    Returns a list of GestureEvents
    
    """
    def consumeGestureEvents(self):
        self._dll.consumeGestureEvents.restype = POINTER(_GestureEventArray)
        array = self._dll.consumeGestureEvents()[0]
        events = []
        for i in range(0, array.size):
            if not array.events[i]: break
            events.append(GestureEvent(array.events[i]))
        return events
    
    
    """Enables processing of the specified gesture on the touch object.
    
    gesture_name is defined in the GML and touch_name is defined in the call to registerTouchObject.
    GML must be loaded prior to issuing this command.
    
    Returns True on success
    
    """
    def addGesture(self, touch_name, gesture_name):
        self._dll.addGesture.restype = c_bool
        return self._dll.addGesture(touch_name, gesture_name)
      
      
    """Remove a gesture from a touch object
    
    gesture_name is defined in the GML and touch_name is defined in the call to registerTouchObject.
    
    Returns True on success
    
    """
    def removeGesture(self, touch_name, gesture_name):
        self._dll.removeGesture.restype = c_bool
        return self._dll.removeGesture(touch_name, gesture_name)
    
    
    """Enable a gesture on a touch object
    
    The gesture must have been previously added with a call to addGesture.
    Gestures are enabled by default.
    
    Returns True on success
    
    """
    def enableGesture(self, touch_name, gesture_name):
        self._dll.enableGesture.restype = c_bool
        return self._dll.enableGesture(touch_name, gesture_name)


    """Disable processing for a gesture on a touch object
    
    The gesture must have been added with a call to addGesture.
    
    Returns True on success
    
    """
    def disableGesture(self, touch_name, gesture_name):
        self._dll.disableGesture.restype = c_bool
        return self._dll.disableGesture(touch_name, gesture_name)
    
            
    """Register a touch object with GestureWorks by name
    
    name is arbitrary and defined in the application.
    
    Returns True on success
    
    """
    def registerTouchObject(self, name):
        self._dll.registerTouchObject.restype = c_bool
        return self._dll.registerTouchObject(name)
        
        
    """Deregister a touch object by name
    
    Returns True on success
    
    """    
    def deregisterTouchObject(self, name):
        self._dll.derigesterTouchObject.restype = c_bool
        return self._dll.deregisterTouchObject(name)
        
        
    """Assign a touch point to a touch object if they have been determined to collide.
    
    touch_name is the name given by registerTouchObject and point_id is the integer given by 
    GestureWorks when we consume point events.
    
    Return True on success
    
    """
    def addTouchPoint(self, touch_name, point_id):
        self._dll.addTouchPoint.restype = c_bool
        return self._dll.addTouchPoint(touch_name, point_id)
            
        