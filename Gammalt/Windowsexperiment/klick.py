import win32api, win32con

def click(x,y):
	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
def move(x,y):
	win32api.SetCursorPos((x,y))

pressad = True
while True:
    delayfactor = 3000
    if win32api.GetAsyncKeyState(ord('R')):
        delayfactor = 300000
    elif win32api.GetAsyncKeyState(ord('X')):
        delayfactor = 30000
    for i in range(delayfactor): nop=0
    if win32api.GetAsyncKeyState(win32con.VK_UP):
        tempx,tempy = win32api.GetCursorPos()
        win32api.SetCursorPos((tempx,tempy-1))
    if win32api.GetAsyncKeyState(win32con.VK_DOWN):
        tempx,tempy = win32api.GetCursorPos()
        win32api.SetCursorPos((tempx,tempy+1))
    if win32api.GetAsyncKeyState(win32con.VK_LEFT):
        tempx,tempy = win32api.GetCursorPos()
        win32api.SetCursorPos((tempx-1,tempy))
    if win32api.GetAsyncKeyState(win32con.VK_RIGHT):
        tempx,tempy = win32api.GetCursorPos()
        win32api.SetCursorPos((tempx+1,tempy))
    tempx,tempy = win32api.GetCursorPos()
    if win32api.GetAsyncKeyState(ord('Z')):
        if not pressad:
            pressad = True
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,tempx,tempy,0,0)
            print "Pressar nu"
    else:
        if pressad:
            pressad = False
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,tempx,tempy,0,0)
            print "Slutar pressa nu"
