import VideoCapture

cam = VideoCapture.Device(devnum=0)
#cam.displayPropertyPage() ## deprecated
#cam.displayCaptureFilterProperties()
#cam.displayCapturePinProperties()
#cam.setResolution(960, 720)
#cam.setResolution(768, 576) ## PAL
#cam.setResolution(352, 288) ## CIF
cam.saveSnapshot('test.jpg', quality=75, timestamp=3, boldfont=1)
