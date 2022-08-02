import cv2
import imagezmq

hub = imagezmq.ImageHub()

while True:
    _, image = hub.recv_image()
    cv2.namedWindow('receiver', cv2.WINDOW_NORMAL)
    cv2.imshow("receiver", image)
    k = cv2.waitKey(1)
    if k == 27:
        break
    hub.send_reply(b'OK')
