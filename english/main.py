import mediapipe as mp  # Import the MediaPipe library for image processing.
import math  # Import the math library for mathematical functions.
import cv2  # Import OpenCV for video capture and processing.
import pyautogui  # Import pyautogui to control the mouse and keyboard.
import speech_recognition as sr  # Import the library for speech recognition.
import os  # Import the os library to execute system commands.
import time  # Import the time library to handle wait times.

# Initialize video capture from the default camera (index 0).
cap = cv2.VideoCapture(0)

# Create a speech recognition object.
recognizer = sr.Recognizer()

def write():
    """Function to listen and recognize voice commands."""
    with sr.Microphone() as source:  # Use the microphone as the audio source.
        audio = recognizer.listen(source)  # Listen to the audio.
        try:
            # Try to recognize the audio using Google Speech Recognition in Spanish (Mexico).
            text = recognizer.recognize_google(audio, language="es-MX")
            return text  # Return the recognized text.
        except sr.UnknownValueError:
            print("Could not understand the audio.")  # Handle the error if the audio is not understood.
        except sr.RequestError as e:
            print("Request error:", str(e))  # Handle request errors.

# Check if the camera opened correctly.
if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()  # Exit the program if the camera cannot be opened.

# Initialize MediaPipe Face Mesh for facial mesh detection.
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils  # Utilities for drawing on the image.

# Conversion factor to adjust the measured distance to centimeters (adjust according to calibration).
factor_conversion = 100  # For example, 100 pixels = 1 cm

# Start the Face Mesh.
with mp_face_mesh.FaceMesh() as face_mesh:
    while True:  # Main loop to process each video frame.
        ret, frame = cap.read()  # Read a frame from the camera.
        if not ret:
            print("Error: Could not read the frame.")
            break  # Exit the loop if the frame cannot be read.
        
        frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirror view.
        
        height, width, _ = frame.shape  # Get the dimensions of the frame.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the frame to RGB.
        results = face_mesh.process(frame_rgb)  # Process the frame to detect the facial mesh.
        
        reference = height // 2  # Define a reference line in the vertical center of the frame.
        
        if results.multi_face_landmarks:  # Check if faces were detected.
            for face_landmarks in results.multi_face_landmarks:  # Iterate over each detected face.
                # Extract the coordinates of the facial mesh landmarks.
                x_nose = face_landmarks.landmark[1].x
                y_nose = face_landmarks.landmark[1].y
                
                x_forehead = face_landmarks.landmark[9].x
                y_forehead = face_landmarks.landmark[9].y
                
                x_cheek = face_landmarks.landmark[13].x
                y_cheek = face_landmarks.landmark[13].y
                
                x_cheek1 = face_landmarks.landmark[14].x
                y_cheek1 = face_landmarks.landmark[14].y
                
                # Draw the landmarks on the frame.
                cv2.circle(frame, (int(width // 2), int(reference)), 1, (0, 0, 0), 2)  # Reference line.
                cv2.circle(frame, (int(x_cheek * frame.shape[1]), int(y_cheek * frame.shape[0])), 1, (255, 0, 0), 2)  # Left cheek.
                cv2.circle(frame, (int(x_cheek1 * frame.shape[1]), int(y_cheek1 * frame.shape[0])), 1, (255, 0, 0), 2)  # Right cheek.
                cv2.circle(frame, (int(x_nose * frame.shape[1]), int(y_nose * frame.shape[0])), 1, (0, 255, 0), 2)  # Nose.
                cv2.circle(frame, (int(x_forehead * frame.shape[1]), int(y_forehead * frame.shape[0])), 1, (0, 0, 255), 2)  # Forehead.
                cv2.line(frame, (int(x_nose * frame.shape[1]), int(y_nose * frame .shape[0])), (int(x_forehead * frame.shape[1]), int(y_forehead * frame.shape[0])), (255, 0, 0), 2)  # Line between nose and forehead.
                
                # Calculate head tilt.
                vector_x = x_nose - x_forehead  # Difference in the x direction.
                vector_y = y_nose - y_forehead  # Difference in the y direction.
                tilt = math.degrees(math.atan2(vector_y, vector_x))  # Convert to degrees.
                
                # Get the current mouse position.
                mouse_position = pyautogui.position()
                x_mouse = mouse_position[0]  # Mouse x coordinate.
                y_mouse = mouse_position[1]  # Mouse y coordinate.
                
                scroll = False  # Variable to control scrolling.
                
                # Interpret the tilt angle to move the mouse.
                if tilt < 85:  # If the tilt is less than 85 degrees, move the mouse to the right.
                    x_mouse += 10
                elif tilt > 95:  # If the tilt is greater than 95 degrees, move the mouse to the left.
                    x_mouse -= 10
                
                # Control vertical mouse movement based on nose position.
                if y_nose * frame.shape[0] > reference + 10:  # If the nose is below the reference, move the mouse down.
                    y_mouse += 10
                elif y_nose * frame.shape[0] < reference - 10:  # If the nose is above the reference, move the mouse up.
                    y_mouse -= 10
                
                # Move the mouse to the new calculated position.
                pyautogui.moveTo(x_mouse, y_mouse, 0.1)  # Smoothly move the mouse to the new position.
                
                # Check if the mouth is open by measuring the distance between the cheeks.
                mouth_distance = math.sqrt((x_cheek1 - x_cheek) ** 2 + (y_cheek1 - y_cheek) ** 2)  # Calculate the distance between the cheeks.
                mouth_distance = mouth_distance * factor_conversion  # Convert the distance to centimeters.
                
                if mouth_distance > 2:  # If the mouth is open, simulate a mouse click.
                    pyautogui.click()
                
                # Voice command recognition if the mouth is very open.
                if mouth_distance > 4:  # If the mouth is very open, listen for a voice command.
                    text = str(write())  # Call the function to recognize the voice command.
                    # Execute actions based on the recognized voice command.
                    if text.lower() == "turn off computer":
                        os.system("shutdown -s")  # Turn off the computer.
                    elif text.lower() == "lower the volume":
                        pyautogui.press("volumedown")  # Lower the volume.
                    elif text.lower() == "raise the volume":
                        pyautogui.press("volumeup")  # Raise the volume.
                    elif "open" in text.lower():  # If the command is to open a program.
                        program = text.lower().replace("open", "").strip()  # Extract the program name.
                        pyautogui.press("win")  # Open the start menu.
                        pyautogui.write(program)  # Type the program name.
                        time.sleep(5)  # Wait a moment for the program to open.
                        pyautogui.press("enter")  # Press Enter to open the program.
                    elif text.lower() == "close":
                        pyautogui.hotkey("alt", "f4")  # Close the active window.TURN OFF THE pc
                        
                    elif text.lower() == "minimize":
                        pyautogui.hotkey("win", "m")  # Minimize all windows.
                    elif text.lower() == "down":
                        pyautogui.scroll(-1000)  # Scroll down.
                    elif text.lower() == "up":
                        pyautogui.scroll(1000)  # Scroll up.
                    else:  # If the command is not recognized, type the text.
                        for letter in text:  # Iterate over each letter of the text.
                            pyautogui.press(letter)  # Press each letter.
                        pyautogui.press("enter")  # Press Enter to send the text.
                
        cv2.imshow('Face Mesh', frame)  # Show the processed frame with the facial mesh.

        if cv2.waitKey(1) & 0xFF == ord('q'):  # If the 'q' key is pressed, exit the loop.
            break

cap.release()  # Release the video capture.
cv2.destroyAllWindows()  # Close all OpenCV windows.