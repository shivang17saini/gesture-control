import cv2
import mediapipe as mp
import pyautogui
import math
import numpy as np

# --- Constants for Configuration ---
SMOOTHING_FACTOR = 0.2  # Increase for more lag but smoother movement
FRAME_REDUCTION = 100   # Size of the border around the active control area
CLICK_THRESHOLD = 0.045 # Distance for a click gesture (thumb to finger)
SCROLL_MODE_THRESHOLD = 0.06 # Distance between index and middle to enter scroll mode
THUMB_AWAY_THRESHOLD = 0.1   # Distance thumb must be away to activate scroll
SCROLL_SENSITIVITY = 120 # Fixed amount to scroll by

# Disable pyautogui's fail-safe to allow cursor control to the edge of the screen
pyautogui.FAILSAFE = False

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Start webcam capture
cap = cv2.VideoCapture(0)

# --- State Variables ---
# For smoothing cursor movement
cursor_x, cursor_y = 0, 0
# To prevent continuous clicks from a single gesture
click_lock = False

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip the image horizontally for a natural, mirror-like effect
    image = cv2.flip(image, 1)
    image_height, image_width, _ = image.shape

    # --- Draw the control area bounding box ---
    cv2.rectangle(image, (FRAME_REDUCTION, FRAME_REDUCTION), 
                  (image_width - FRAME_REDUCTION, image_height - FRAME_REDUCTION), 
                  (0, 0, 255), 2) # Red box

    # Convert the BGR image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and find hands
    results = hands.process(rgb_image)
    
    # Flag to check if a click gesture is active in the current frame
    is_click_gesture_active = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks for visualization
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # --- Extract Key Landmark Positions ---
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP] # Pinky knuckle

            # --- 1. Cursor Movement (Mapped to Control Area) ---
            # Map hand position from within the red box to the entire screen
            target_x = np.interp(index_tip.x, 
                                 (FRAME_REDUCTION / image_width, 1 - FRAME_REDUCTION / image_width), 
                                 (0, screen_width))
            target_y = np.interp(index_tip.y, 
                                 (FRAME_REDUCTION / image_height, 1 - FRAME_REDUCTION / image_height), 
                                 (0, screen_height))
            
            # Exponential smoothing for fluid cursor motion
            cursor_x = cursor_x + (target_x - cursor_x) * SMOOTHING_FACTOR
            cursor_y = cursor_y + (target_y - cursor_y) * SMOOTHING_FACTOR

            # Move mouse, clamping values to screen boundaries to be safe
            pyautogui.moveTo(max(0, min(screen_width, cursor_x)), max(0, min(screen_height, cursor_y)))

            # --- 2. Single & Double Click Gestures ---
            double_click_dist = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
            single_click_dist = math.hypot(thumb_tip.x - middle_tip.x, thumb_tip.y - middle_tip.y)
            
            # A. Double Click (Index Finger + Thumb)
            if double_click_dist < CLICK_THRESHOLD:
                is_click_gesture_active = True
                if not click_lock:
                    pyautogui.doubleClick()
                    print("Double Click!")
                    click_lock = True
                    cv2.circle(image, (int(index_tip.x * image_width), int(index_tip.y * image_height)), 15, (0, 0, 255), cv2.FILLED)
            
            # B. Single Click (Middle Finger + Thumb)
            elif single_click_dist < CLICK_THRESHOLD:
                is_click_gesture_active = True
                if not click_lock:
                    pyautogui.click()
                    print("Single Click!")
                    click_lock = True
                    cv2.circle(image, (int(middle_tip.x * image_width), int(middle_tip.y * image_height)), 15, (0, 255, 0), cv2.FILLED)
            
            # C. Release Click Lock when no click gesture is active
            if not is_click_gesture_active:
                click_lock = False

            # --- 3. Updated Scrolling Gesture ---
            scroll_mode_dist = math.hypot(index_tip.x - middle_tip.x, index_tip.y - middle_tip.y)
            thumb_away = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y) > THUMB_AWAY_THRESHOLD
            
            # Activate scroll only if a click is not being performed
            if scroll_mode_dist < SCROLL_MODE_THRESHOLD and thumb_away and not is_click_gesture_active:
                # Check if pinky is straight up (tip is above knuckle)
                if pinky_tip.y < pinky_pip.y:
                    pyautogui.scroll(SCROLL_SENSITIVITY)
                    print("Scrolling Up")
                    cv2.putText(image, "Scrolling Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                # Check if pinky is pointing down (tip is below knuckle)
                elif pinky_tip.y > pinky_pip.y:
                    pyautogui.scroll(-SCROLL_SENSITIVITY)
                    print("Scrolling Down")
                    cv2.putText(image, "Scrolling Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('AI Virtual Mouse', image)

    # Exit by pressing 'q'
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

