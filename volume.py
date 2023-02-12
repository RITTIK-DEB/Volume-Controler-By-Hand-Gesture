import cv2
import mediapipe as mp
import time
import numpy as np
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


from mediapipe.python.solutions import hands

mphands = mp.solutions.hands
mppose = mp.solutions.pose
pose = mppose.Pose()
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils
ctime = 0
ptime =0
x1,y1,x2,y2=0,0,0,0
dist=0
##############################
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


volRange=volume.GetVolumeRange()
minvol=volRange[0]
maxvol=volRange[1]
################################
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)

## if camera error cant grab a frame  cap=cv2.VideoCapture(0,cv2.CAP_DSHOW) else cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while True:
    success , img = cap.read()
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgrgb)
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                h , w, c = img.shape
                cx , cy = int(lm.x*w) , int(lm.y*h)
                if id==4:
                    x1=cx
                    y1=cy
                    
                    cv2.circle(img,(x1,y1),3,(255,0,255),cv2.FILLED)
                if id==8:
                    x2=cx
                    y2=cy    
                    cv2.circle(img,(x2,y2),3,(255,0,255),cv2.FILLED)
                    
                px=(x1+x2)//2
                py=(y1+y2)//2
                dist = math.hypot(x2-x1,y2-y1)
                vol=np.interp(dist,[18,120],[minvol,maxvol])
                print(int(dist),vol)
                volume.SetMasterVolumeLevel(vol, None)
                if dist<50:
                    cv2.circle(img,(px,py),5,(0,255,0),cv2.FILLED)
                    
                cv2.circle(img,(px,py),3,(255,0,255),cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
            mpdraw.draw_landmarks(img ,handlms, mphands.HAND_CONNECTIONS)


    ctime=time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.imshow("Image",img)
    cv2.putText(img,str(int(fps)), (40 ,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.waitKey(1)
