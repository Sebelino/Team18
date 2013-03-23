from VideoCapture import Device

## use the first video-device which is found
## devnum=1 uses the second one and so on
cam = Device(devnum=0)

## uncomment one or both of the following lines to display
## the dialog-boxes which allow changing the video size
#cam.displayCaptureFilterProperties()
#cam.displayCapturePinProperties()
#cam.setResolution(640,480)

## simplest form
cam.saveSnapshot('image1.jpg')

## the quality keyword argument can be used with JPEGs: 0-100, default 75
cam.saveSnapshot('image2.jpg', quality=30)

## PIL can produce many different picture file-formats
cam.saveSnapshot('image3.gif')

## use timestamp=1 to include time and date
## timestamp=2 adds a shadow, 3 a light outline, and 4 a heavy outline
cam.saveSnapshot('image4.bmp', timestamp=1)

## a bold fontstyle is also available
cam.saveSnapshot('image5.jpg', timestamp=3, boldfont=1)

## the position of the timestamp can be specified with two characters:
## t=top, b=bottom;   l=left, c=center, r=right
cam.saveSnapshot('image6.jpg', timestamp=2, textpos='tc')
