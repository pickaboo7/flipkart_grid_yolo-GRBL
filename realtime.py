import cv2
from ultralytics import YOLO

model = YOLO('best_top.pt')

video_path = "14boxes_piyaanshlaptop.mp4"
cap = cv2.VideoCapture(video_path)

# Get the video's frame rate and resolution
fps = int(cap.get(cv2.CAP_PROP_FPS))
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width, height)

# Create a cv2.VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # or use 'MP4V' for .mp4 format
out = cv2.VideoWriter('output_video.avi', fourcc, fps, size)

while cap.isOpened():

    success, frame = cap.read()

    if success:
        results = model(frame)
        annotated_frame = results[0].plot()

        out.write(annotated_frame)  # Write the annotated frame to the video file

        cv2.imshow("Object Detection and Segmentation", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
out.release()  # Finalize the video file.
cv2.destroyAllWindows()
