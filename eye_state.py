import time
import func
import cv2 as cv
import mediapipe as mp
import numpy as np
import math as m
import websockets
import asyncio


cap = cv.VideoCapture(0)
mp_draw = mp.solutions.drawing_utils
drawing_spec = mp_draw.DrawingSpec(thickness=1, circle_radius=1)
mp_facemesh = mp.solutions.face_mesh
# eye_cascade = cv.CascadeClassifier(r'C:\Users\Samuel Mensah\Face_tilt\haarcascade_eye_tree_eyeglasses.xml')
# face_cascade = cv.CascadeClassifier(r'C:\Users\Samuel Mensah\Face_tilt\haarcascade_frontalface_default.xml') 

FACE_OVAL=[ 10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103,67, 109]

# lips indices for Landmarks
LIPS=[ 61, 146, 91, 181, 84, 17, 314, 405, 321, 375,291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95,185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78 ]
LOWER_LIPS =[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
UPPER_LIPS=[ 185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78] 
# Left eyes indices 
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
LEFT_EYEBROW =[ 336, 296, 334, 293, 300, 276, 283, 282, 295, 285 ]

# right eyes indices
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]  
RIGHT_EYEBROW=[ 70, 63, 105, 66, 107, 55, 65, 52, 53, 46 ]

# def detect_faces(img, gray):
#     """
#         Converts image to grayscale and applies pretrained haar cascade of frontal face
#         detection to get relevant data points of the face
#         @param -> [img] - frame captured from hardware | [gray] - grayscale version of image
#         @return -> [faces] - face related info | [faces_present] - are faces peresent | [total_faces] - total # of faces
#     """
    # faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
    # for face in faces:
    #     (x, y, w, h) = face
    #     cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # return faces

# def detect_eyes(img, gray, face):
#     """
#         Highlights the eyes in a detected face
#         @param -> [img] - frame captured from hardware | [gray] - grayscale version of image
#         @return -> [eyes] - eye related info | [total_eyes] - total number of eyes detected
#     """
    # (x, y, w, h) = face
    # roi_gray_face = gray[y:y + h, x:x + w]
    # roi_color_face = img[y:y + h, x:x + w]
    # eyes = eye_cascade.detectMultiScale(
    #     roi_gray_face, 1.1, 5, minSize=(30, 30), maxSize=(80, 80))
    # total_eyes = len(eyes)
    # for eye in eyes:
    #     (ex, ey, ew, eh) = eye
    #     cv.rectangle(roi_color_face, (ex, ey),
    #                   (ex + ew, ey + eh), (0, 255, 0), 2)
    # return eyes, total_eyes



# def read_eyes(face, total_eyes):
#     """
#         Tracks the eyes around the region of interest to draw insights
#         @param -> [face] - face related info | [eyes] - eye related info | [total_eyes] - total number of eyes detected
#         @return -> None
#     """
#     (x, y, w, h) = face
#     return total_eyes
    # if total_eyes >= 2:
    #     cv.putText(img, 'Eyes open', text_position,
    #                 cv.FONT_HERSHEY_PLAIN, 3, (100, 100, 0), 2)
    # elif total_eyes == 1:
    #     positional_ratio = eyes[0][0] / abs(w - eyes[0][0])
    #     if positional_ratio >= 1.0:
    #         cv.putText(img, 'Right closed', text_position,
    #                     cv.FONT_HERSHEY_PLAIN, 3, (100, 100, 0), 2)
    #     else:
    #         cv.putText(img, 'Left closed', text_position,
    #                     cv.FONT_HERSHEY_PLAIN, 3, (100, 100, 0), 2)
    # elif total_eyes == 0:
    #     cv.putText(img, 'Eyes closed', text_position,
    #                 cv.FONT_HERSHEY_PLAIN, 3, (100, 100, 0), 2)
    # else:
    #     pass
    


async def talk(msg):
    url = "ws://192.168.100.178:81"

    async with websockets.connect(url) as ws:
        while True:
            await ws.send(msg)




def landmarks_draw(img, results, draw_mesh=False):
    height, width = img.shape[:2]      
    coord_mesh = [(int(coord.x * width), int(coord.y * height)) for coord in results.multi_face_landmarks[0].landmark]
    
    if draw_mesh:
        [cv.circle(img, point, 1,(0, 255, 0), 1, -1) for point in coord_mesh]
    return coord_mesh



def Euclidean_d(pt1, pt2):
  x1, y1 = pt1
  x2, y2 = pt2
  distance = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
  return distance


def Eye_state(img, landmarks, right_eye_landmarks, left_eye_landmarks):
  # Right eyes 
  # horizontal line 
  rh_right = landmarks[right_eye_landmarks[0]]
  rh_left = landmarks[right_eye_landmarks[8]]
  # vertical line 
  rv_top = landmarks[right_eye_landmarks[12]]
  rv_bottom = landmarks[right_eye_landmarks[4]]
  # draw lines on right eyes 
#   cv.line(img, rh_right, rh_left, func.PURPLE, 2)
#   cv.line(img, rv_top, rv_bottom, func.WHITE, 2)    
  # LEFT_EYE 
  # horizontal line 
  lh_right = landmarks[left_eye_landmarks[0]]
  lh_left = landmarks[left_eye_landmarks[8]]    
  # vertical line 
  lv_top = landmarks[left_eye_landmarks[12]]
  lv_bottom = landmarks[left_eye_landmarks[4]]   
  #drawing lines on left Eye
#   cv.line(img, lh_right, lh_left, func.PURPLE, 2)
#   cv.line(img, lv_top, lv_bottom, func.WHITE, 2) 
  # Finding Distance Right Eye
  rh_dist = Euclidean_d(rh_right, rh_left)
  rv_dist = Euclidean_d(rv_top, rv_bottom)
  # Finding Distance Left Eye
  lv_dist = Euclidean_d(lv_top, lv_bottom)
  lh_dist = Euclidean_d(lh_right, lh_left)    
  # Finding ratio of LEFT and Right Eyes
  REratio = int(rh_dist/rv_dist)
  LEratio = int(lh_dist/lv_dist)
  # ratio = (REratio+leRatio)/2 
  return REratio, LEratio
  






prev_t = 0
with mp_facemesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, frame = cap.read()
   
    if not success:
      print("empty camera frame.")
      continue

    frame = cv.cvtColor(cv.flip(frame, 1), cv.COLOR_BGR2RGB)
    
    frame.flags.writeable = False
    results = face_mesh.process(frame)

    # Draw the face mesh annotations on the frame.
    frame.flags.writeable = True
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    # 
    if results.multi_face_landmarks:
        print("face found!")
        coord = landmarks_draw(frame, results, draw_mesh=False)
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        # faces = detect_faces(frame, gray_frame)
        # for face in faces:
        #             eyes, total_eyes = detect_eyes(frame, gray_frame, face)
        #             (x, y, w, h) = face
        
        L_EyeState, R_EyeState = Eye_state(frame, coord, RIGHT_EYE, LEFT_EYE)
        Open_range = [2, 3, 4]
        close_range = [5, 6, 7]

        if L_EyeState in close_range:  
            cv.putText(frame, 'Left Eye: CLOSED', (20, 300), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            asyncio.get_event_loop().run_until_complete(talk("On"))
        elif L_EyeState in Open_range:
          cv.putText(frame, 'Left Eye: OPENED', (20, 300), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        
        
        if R_EyeState in close_range:  
          cv.putText(frame, 'Right Eye: CLOSED', (400, 300), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
          asyncio.get_event_loop().run_until_complete(talk("Off"))
        elif R_EyeState in Open_range :
          cv.putText(frame, 'Right Eye: OPENED', (400, 300), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                  
        cv.putText(frame, str(round(L_EyeState, 2)), (20, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        cv.putText(frame, str(round(R_EyeState, 2)), (500, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        # frame = func.fillPolyTrans(frame, [coord[p] for p in FACE_OVAL], (45, 78, 0), opacity=0.4)
        # frame = func.fillPolyTrans(frame, [coord[p] for p in LIPS], (45, 78, 0), opacity=0.4)
        # frame = func.fillPolyTrans(frame, [coord[p] for p in LOWER_LIPS], (45, 78, 0), opacity=0.4)
        # frame = func.fillPolyTrans(frame, [coord[p] for p in UPPER_LIPS], (45, 78, 0), opacity=0.4)
        frame = func.fillPolyTrans(frame, [coord[p] for p in RIGHT_EYE], (45, 78, 0), opacity=0.4)
        frame = func.fillPolyTrans(frame, [coord[p] for p in LEFT_EYE], (45, 78, 0), opacity=0.4)
        # frame = func.fillPolyTrans(frame, [coord[p] for p in RIGHT_EYEBROW], (45, 78, 0), opacity=0.4)
        # frame = func.fillPolyTrans(frame, [coord[p] for p in LEFT_EYEBROW], (45, 78, 0), opacity=0.4)

        # [cv.circle(frame,coord[p], 1, func.GREEN , -1, cv.LINE_AA) for p in LIPS]
        # [cv.circle(frame,coord[p], 1, func.BLACK ,- 1, cv.LINE_AA) for p in RIGHT_EYE]
        # [cv.circle(frame,coord[p], 1, func.BLACK , -1, cv.LINE_AA) for p in LEFT_EYE]

        # [cv.circle(frame,coord[p], 1, func.BLACK , -1, cv.LINE_AA) for p in RIGHT_EYEBROW]
        # [cv.circle(frame,coord[p], 1, func.BLACK , -1, cv.LINE_AA) for p in LEFT_EYEBROW]
        # [cv.circle(frame,coord[p], 1, func.RED , -1, cv.LINE_AA) for p in FACE_OVAL] 
    else:
        print("""No face detected!
        Check lighting  and make sure your face is in frame. """)
    # if results.multi_face_landmarks:
    #   for facial_landmarks in results.multi_face_landmarks:
    #     mp_draw.draw_landmarks(
    #         image=frame,
    #         landmark_list=face_landmarks,
    #         connections=None,
    #         landmark_drawing_spec=drawing_spec,
    #         connection_drawing_spec=drawing_spec, landmark_color=(0, 34, 0))
    curr_t = time.time()
    fps = 1 / (curr_t - prev_t)
    prev_t = curr_t
    cv.putText(frame, f'FPS: {int(fps)}', (20, 70), cv.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)
    cv.imshow('feed', frame)
    if cv.waitKey(5) & 0xFF == ord('x'):
      break
cap.release
