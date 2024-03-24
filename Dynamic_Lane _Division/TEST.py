import cv2
import numpy as np
import serial

# Load the car cascade classifier
car_cascade = cv2.CascadeClassifier('haarcascade_car.xml')

# Define serial communication with Arduino
arduino = serial.Serial('COM6', 9600)  # Adjust COM port and baud rate as needed

def detect_cars(frame, prev_frame_cars, left_lane_cars, right_lane_cars):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect cars in the frame
    cars = car_cascade.detectMultiScale(gray, 1.15, 4)

    # Count cars in the left and right lanes
    current_left_lane_cars = 0
    current_right_lane_cars = 0
    for (x, _, _, _) in cars:
        if x < frame.shape[1] / 2:  # Car in the left lane
            current_left_lane_cars += 1
        else:  # Car in the right lane
            current_right_lane_cars += 1

    # Update the car counts for left and right lanes
    left_lane_cars += current_left_lane_cars - prev_frame_cars[0]
    right_lane_cars += current_right_lane_cars - prev_frame_cars[1]

    # Draw rectangles around the cars
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the car counts on the frame
    cv2.putText(frame, 'Left Lane Cars: {}'.format(left_lane_cars), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, 'Right Lane Cars: {}'.format(right_lane_cars), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return len(cars), left_lane_cars, right_lane_cars

def count_cars(video_path):
    # Create a VideoCapture object to capture the video
    cap = cv2.VideoCapture(video_path)

    left_lane_cars = 0
    right_lane_cars = 0
    prev_frame_cars = (0, 0)
    while True:
        # Read the next frame
        ret, frame = cap.read()
        if not ret:
            break

        # Detect and count cars in the frame
        frame_cars, left_lane_cars, right_lane_cars = detect_cars(frame, prev_frame_cars, left_lane_cars, right_lane_cars)
        prev_frame_cars = (left_lane_cars, right_lane_cars)

        # Check conditions to trigger Arduino
        if left_lane_cars >= 8 and right_lane_cars < 5:
            arduino.write(b'1')  # Sending signal to Arduino

        # Display the frame
        cv2.imshow('Car Detection', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object
    cap.release()

    # Close all windows
    cv2.destroyAllWindows()

    return left_lane_cars, right_lane_cars

video_path = 'lanedectvid.mp4'  # Path to your video file
left_lane_cars, right_lane_cars = count_cars(video_path)
print("Total number of cars detected in the left lane:", left_lane_cars)
print("Total number of cars detected in the right lane:", right_lane_cars)
