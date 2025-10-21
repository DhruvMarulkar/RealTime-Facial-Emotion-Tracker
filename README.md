# Real-Time Facial Emotion Tracker

A Python application that detects your facial expressions in real-time using your webcam and logs your **top emotion** to a CSV file. It draws a rectangle around your face and displays your current emotion above it. The CSV only logs when your top emotion changes, keeping the data clean.

---

## Features

- Real-time webcam emotion detection  
- Detects 7 basic emotions: `angry`, `disgust`, `fear`, `happy`, `sad`, `surprise`, `neutral`  
- Draws a **rectangle around the detected face**  
- Displays **top emotion with confidence** above the rectangle  
- Logs emotion to `emotion_log.csv` only when the top emotion changes  
- Handles frames where **no face is detected** gracefully  

