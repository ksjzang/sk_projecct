import cv2
import cv2.aruco as aruco
import numpy as np
import time
import expansion

# motor setting
exp0 = expansion.Expansion(address=0x09)
exp1 = expansion.Expansion(address=0x0A)
exp2 = expansion.Expansion(address=0x0B)

exp0.controller_enable()
exp1.controller_enable()
exp2.controller_enable()

# origin point
exp2.set_motor_power(1, 0)
time.sleep(0.1)
exp2.reset_encoder(1)

def left(power):
    exp0.set_motor_power(1, power)
    exp0.set_motor_power(2, power)
    exp1.set_motor_power(1, power)
    exp1.set_motor_power(2, power)

def right(power):
    exp0.set_motor_power(1, -power)
    exp0.set_motor_power(2, -power)
    exp1.set_motor_power(1, -power)
    exp1.set_motor_power(2, -power)

def stop():
    exp0.set_motor_power(1, 125)
    exp0.set_motor_power(2, 125)
    exp1.set_motor_power(1, 125)
    exp1.set_motor_power(2, 125)

def putting():
    exp2.set_motor_degree(1, -100, -90)
    time.sleep(0.1)
    while exp2.read_motor_busy(1):
        print("busy")
        time.sleep(0.1)

    time.sleep(1.5)

    exp2.set_motor_degree(1, 250, 70)
    time.sleep(0.1)
    while exp2.read_motor_busy(1):
        print("busy")
        time.sleep(0.1)

    time.sleep(1)
    exp2.set_motor_power(1, 0)
    print("stop!")

    exp2.set_motor_degree(1, 50, 0)
    time.sleep(0.1)
    while exp2.read_motor_busy(1):
        print("busy")
        time.sleep(0.1)

    exp2.set_motor_power(1, 0)
    print('finish')

# camera
#------------------------------------------------------

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

start_time = time.time()
while True:
    # Flush old frames
    for _ in range(3):
        cap.read()
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        marker_corners = corners[0][0]
        center = np.mean(marker_corners, axis=0)
        center_x = int(center[0])
        print(time.time()-start_time, center_x, flush=True)

    # 115~120
    if center_x < 110:
        right(20)
    elif center_x > 130:
        left(20)
    else:
        stop()
        time.sleep(10)
        putting()
        break
print('finish')