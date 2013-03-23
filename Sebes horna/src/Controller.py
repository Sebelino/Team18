import GestureHandler
import ProfileManager
import CommandHandler

while True:
    if !GestureHandler.containsGesture():
        sleep(0.01)
        continue
    gesture = GestureHandler.poll()
    command = ProfileManager.getCommand(gesture)
    CommandHandler.execute(command)
