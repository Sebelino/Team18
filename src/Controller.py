import GestureHandler
import ProfileManager
import CommandHandler
import thread
import time

thread.start_new_thread(GestureHandler.initialisera,())
while True:
    if not GestureHandler.containsGestureii():
        time.sleep(0.01)
        continue
    gesture = GestureHandler.pollii()
    command = ProfileManager.getCommand(gesture)
    CommandHandler.execute(command)

