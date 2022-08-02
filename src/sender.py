import sys
import socket

from pypylon import pylon
import imagezmq

sender = imagezmq.ImageSender(connect_to=sys.argv[1])
sender_name = socket.gethostname()
# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()
camera.ExposureTime.SetValue(33000)

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        sender.send_image(sender_name, img)
    grabResult.Release()

# Releasing the resource
camera.StopGrabbing()

