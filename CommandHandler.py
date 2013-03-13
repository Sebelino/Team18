
import win32api, win32con

def click(x,y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
  

def scroll(x,y):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,x,y,-120,0)


click(100,100)	
scroll(100,100)
