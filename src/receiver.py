import time
import cv2
import imagezmq

hub = imagezmq.ImageHub()
prev_tstamp = 0
new_tstamp = 0
while True:
    _, image = hub.recv_image()
    image = cv2.imdecode(image, 1)
    new_tstamp = time.time()
    fps = 1 / (new_tstamp - prev_tstamp)
    prev_tstamp = new_tstamp
    image = cv2.putText(image, str(fps), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
    cv2.namedWindow('receiver', cv2.WINDOW_NORMAL)
    cv2.imshow("receiver", image)
    k = cv2.waitKey(1)
    if k == 27:
        break
    hub.send_reply(b'OK')

