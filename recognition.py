from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import face_recognition
import cv2
import numpy as np
import math
app = Flask(__name__)
socketioApp = SocketIO(app)

# Select the default camera as the capture device
video_capture = cv2.VideoCapture(0)

# Load a sample picture of Robert Downey Junior and learn how to recognize it.
rdj_image = face_recognition.load_image_file("images/rdj.jpg")
rdj_face_encoding = face_recognition.face_encodings(rdj_image)[0]

# Load a sample picture of Mark Campbell and learn how to recognize it.
mark_image = face_recognition.load_image_file("images/mark.jpg")
mark_face_encoding = face_recognition.face_encodings(mark_image)[0]

# Load a sample picture of Mads Mikkleson and learn how to recognize it.
mads_image = face_recognition.load_image_file("images/mads.jpg")
mads_face_encoding = face_recognition.face_encodings(mads_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    rdj_face_encoding,
    mark_face_encoding,
    mads_face_encoding
]
known_face_names = [
    "Robert Downey",
    "Mark Campbell",
    "Mads Mikkelsen"
]

# Initialize variables for the gen_frames function
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Getting the face confidence
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

def gen_frames():  
    while True:
        success, frame = video_capture.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    confidence = face_confidence(face_distances[best_match_index], face_match_threshold=0.6)

                # Add name and confidence % to face_names
                face_names.append(name + " " + confidence)
                
            

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

def run():
    socketioApp.run(app)

if __name__ == '__main__':
    socketioApp.run(app)

