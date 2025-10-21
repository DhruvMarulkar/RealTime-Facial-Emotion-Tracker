import cv2
from deepface import DeepFace
import pandas as pd
from datetime import datetime

# Initialize webcam
cap = cv2.VideoCapture(0)
emotion_log = []

print("Press 'q' to quit...")

# Keep track of last top emotion
last_top_emotion = None

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        cv2.putText(frame, "No face detected", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Crop face for DeepFace
            face_img = frame[y:y+h, x:x+w]

            try:
                # Analyze emotion
                result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
                emotions = result[0]['emotion']
                top_emotion = max(emotions, key=emotions.get)
                confidence = emotions[top_emotion]

                # Only log if emotion changed
                if top_emotion != last_top_emotion:
                    emotion_log.append({
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "emotion": top_emotion,
                        "confidence": round(confidence, 2)
                    })
                    last_top_emotion = top_emotion

                # Display top emotion above rectangle
                cv2.putText(frame, f"{top_emotion} ({confidence:.2f})",
                            (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (0, 255, 255), 2)

            except Exception:
                cv2.putText(frame, "Emotion detection failed", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Show frame
    cv2.imshow("Emotion Tracker", frame)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam
cap.release()
cv2.destroyAllWindows()

# Save CSV
df = pd.DataFrame(emotion_log)
csv_file = "emotion_log.csv"

try:
    existing = pd.read_csv(csv_file)
    df.to_csv(csv_file, mode='a', index=False, header=False)
except FileNotFoundError:
    df.to_csv(csv_file, index=False, header=True)

print(f"✅ Emotion log saved to {csv_file}")
