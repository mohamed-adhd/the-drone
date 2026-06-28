import mediapipe as mp
import cv2
import time
def state(hands_landmark):
    fingered=0
    if hands_landmark.landmark[4].x<hands_landmark.landmark[3].x and hands_landmark.landmark[7].x>hands_landmark.landmark[6].y and hands_landmark.landmark[11].x>hands_landmark.landmark[10].y and hands_landmark.landmark[15].x>hands_landmark.landmark[14].y and hands_landmark.landmark[18].x>hands_landmark.landmark[19].y:
        return 0
    elif hands_landmark.landmark[4].x>hands_landmark.landmark[3].x and hands_landmark.landmark[7].x>hands_landmark.landmark[6].y and hands_landmark.landmark[11].x>hands_landmark.landmark[10].y and hands_landmark.landmark[15].x>hands_landmark.landmark[14].y and hands_landmark.landmark[18].x>hands_landmark.landmark[19].y:
        return 1
    elif hands_landmark.landmark[8].y<hands_landmark.landmark[5].y and hands_landmark.landmark[11].x>hands_landmark.landmark[10].y and hands_landmark.landmark[15].x>hands_landmark.landmark[14].y and hands_landmark.landmark[18].x>hands_landmark.landmark[19].y:
        return 2
    elif hands_landmark.landmark[8].y>hands_landmark.landmark[5].y and hands_landmark.landmark[11].x>hands_landmark.landmark[10].y and hands_landmark.landmark[15].x>hands_landmark.landmark[14].y and hands_landmark.landmark[18].x>hands_landmark.landmark[19].y:
        return 3 
    else:
        return -1

mp_hnds=mp.solutions.hands
hands=mp_hnds.Hands()
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)


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
    
    cv2.imshow("webcame",frame)
cap.release()
cv2.destroyAllWindows()

