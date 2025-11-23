import cv2 as cv
#from engine.object_detection import ObjectDetection

#Load the object detection model
#od = ObjectDetection("models/yolo11m.pt")

# Sample code for loading a video!
# capture = cv.VideoCapture('demo/vehicles_4.mp4');

# Initialize webcam
capture = cv.VideoCapture(0)
if not capture.isOpened():
    raise RuntimeError("Could not open webcam\n")

# Read and show first frame
isTrue, frame = capture.read()
cv.imshow('Video', frame)

# Let the user draw a bounding box (drag a rectangle on the paused frame)
print("Hi! Please drag a rectangle with your mouse pointer around the object you'd like to track! Here are the formal instructions :D")
bbox = cv.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)
cv.destroyWindow("Select Object")

# IDEA: bindingBoxArea = bbox.area

# MOST RECENT CHANGE: testing KCF for tracker (fast!) instead of CSRT (slower but accurate!)
# Create a tracker: CSRT is accurate and stable (slower),  KCF is fast with good balance for accuracy! MOSSE not recognized in this program; faster but less accurate (best for fast-moving or small objects)!
tracker = cv.TrackerKCF_create()  # alternatives: TrackerKCF_create(), TrackerMOSSE_create() (the MOSSE option is not recognized!)

# Initialize tracker with first frame and bounding box
keepTracking = tracker.init(frame, bbox)

while True:
    # Read current frame
    isTrue, frame = capture.read()

    # Update tracker
    keepTracking, bbox = tracker.update(frame)

    if keepTracking:
         # Tracking success: draw rectangle
        (x, y, w, h) = [int(v) for v in bbox]
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Find section of image to focus on!
        roi = frame[y:y+h, x:x+w]

        # Process for finding edges of objects:

        # 1. Set the image's color to grayscale for greater accuracy!
        gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)

        # 2. Get the image's threshold! This means dividing the image into two binary categories:
        # First = foreground; second = background! --> Using shading values!
        ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        #edges = cv.Canny(gray, 50, 150)

        contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contour = max(contours, key=cv.contourArea)

        # Use the object's contour to calculate the minimum area for a bounding rectangle around the contour!
        # Values returned include the center (x, y,) dimensions (width, height), and angle of rotation!
        

        rect = cv.minAreaRect(contour)

        center, (w, h), angle = rect

        if w < h:
            angle = 90 + angle
            rect = cv.minAreaRect(contour)

        box = cv.boxPoints(rect)
        box = box.astype(int)
        box[:, 0] += x
        box[:, 1] += y
        cv.drawContours(frame, [box], 0, (0, 255, 255), 2)
        
        center, (w, h), angle = rect
        cv.putText(frame, f"Angle: {angle:.2f}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        
        cv.putText(frame, "Tracking", (10, 25), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    else:
         # If object tracking fails
         cv.putText(frame, "Lost object", (10, 25), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    
    #Display current frame
    cv.imshow("Object Tracker in webcam (press q to quit)!", frame)

    #detect objects in the current frame!
    #bboxes, class_ids, scores = od.detect(frame)
    #print(bb);
    
    
    if (cv.waitKey(20)) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()