import keyboard
import math
import cv2
import pyautogui
import mediapipe as mp

capture = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

while True:
    ret, frame = capture.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            indexFinger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

            if indexFinger_y < thumb_y:  # if index is up
                handGesture_y = 'pointing up'
                if handGesture_y == 'pointing up':
                    pyautogui.press('volumeup')
            elif indexFinger_y > thumb_y:  # if index is down
                handGesture_y = 'pointing down'
                if handGesture_y == 'pointing down':
                    pyautogui.press('volumedown')
            else:
                handGesture_y = 'unknown'

    # elif results.multi_hand_landmarks:
    #     for hand_landmarks in results.multi_hand_landmarks:
    #         mp_drawing.draw_landmarks(
    #             frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    #
    #         thumb_tip = (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * frame.shape[1],
    #                      hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * frame.shape[0])
    #         index_tip = (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1],
    #                      hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0])
    #
    #         distance = calculate_distance(thumb_tip, index_tip)
    #
    #
    #         if distance < 50:
    #             keyboard.send('brightnessup')
    #         else:
    #             keyboard.send('brightnessdown')

    cv2.imshow('Hand Gesture', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()



