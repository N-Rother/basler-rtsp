import argparse
import sys
import socket

import cv2
from pypylon import pylon
import imagezmq

parser = argparse.ArgumentParser()
parser.add_argument('host')
parser.add_argument('-x', '--width', type=int, default=1920)
parser.add_argument('-y', '--height', type=int, default=1080)
parser.add_argument('-e', '--exposure', type=int, default=33000)
parser.add_argument('-c', '--compression', type=int, default=95)
args = parser.parse_args()

sender = imagezmq.ImageSender(connect_to=args.host)
sender_name = socket.gethostname()
# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
# Grabing Continusely (video) with minimal delay
camera.Open()

camera.ExposureTime.SetValue(args.exposure)
camera.Height.SetValue(args.height)
camera.Width.SetValue(args.width)
camera.CenterX.SetValue(True)
camera.CenterY.SetValue(True)

camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()


# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), args.compression]

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        img = cv2.imgencode('.jpg', img, encode_param)

        sender.send_image(sender_name, img)
    grabResult.Release()

# Releasing the resource
camera.StopGrabbing()

