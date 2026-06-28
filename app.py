import mediapipe as mp
import cv2
import time
import math

def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

def finger_up(lm, tip, pip, wrist=0):
    return dist(lm[tip], lm[wrist]) > dist(lm[pip], lm[wrist])

def state(hands_landmark):
    lm = hands_landmark.landmark
    index_up  = finger_up(lm, 8, 6)
    middle_up = finger_up(lm, 12, 10)
    ring_up   = finger_up(lm, 16, 14)
    pinky_up  = finger_up(lm, 20, 18)
    thumb_closed = lm[4].x > lm[3].x
    thumb_open   = lm[4].x < lm[3].x
    others_down = not (index_up or middle_up or ring_up or pinky_up)
    is_fist = (dist(lm[8], lm[0])  < dist(lm[6], lm[0])  and dist(lm[12], lm[0]) < dist(lm[10], lm[0]) and dist(lm[16], lm[0]) < dist(lm[14], lm[0]) and dist(lm[20], lm[0]) < dist(lm[18], lm[0]))
    #print(f"idx={index_up} mid={middle_up} ring={ring_up} pinky={pinky_up} thumb_open={thumb_open}")
    if thumb_closed and others_down:
        return 0
    elif thumb_open and others_down:
        return 1
    elif index_up and not (middle_up or ring_up or pinky_up):
        return 2
    elif thumb_closed and pinky_up and ring_up and middle_up and index_up:
        return 3
    else:
        return -1

mp_hnds=mp.solutions.hands
hands=mp_hnds.Hands()
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


if not cap :
    print("couldnt open the camera twin")
    exit()
last_state = -1
last_write_time = 0
WRITE_INTERVAL = 0.1
while True:
    current_time = time.time()
    ret,frame=cap.read()
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result=hands.process(rgb)
    pito=""
        
   
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if result.multi_hand_landmarks is not None:
        with open("state.txt","w") as file:
                        for hands_landmark in result.multi_hand_landmarks:
                            if state(hands_landmark)==0:
                                file.write("left")
                            elif state(hands_landmark)==1:
                                file.write("right")
                            elif state(hands_landmark)==2:
                                file.write("up")
                            elif state(hands_landmark)==3:
                                file.write("down")
                            else:
                                 file.write("x")
        mp.solutions.drawing_utils.draw_landmarks(frame,hands_landmark,mp_hnds.HAND_CONNECTIONS)

    else:
        with open("state.txt", "w") as file:
            file.write("x")

        
                
    
    cv2.imshow("webcame",frame)
cap.release()
cv2.destroyAllWindows()

