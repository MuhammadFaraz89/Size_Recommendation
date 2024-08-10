import cv2
import numpy as np
import imutils
from imutils import perspective
from scipy.spatial import distance
import matplotlib.pyplot as plt

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def giveSizeAccordingToMeasurement(measurement):
    size = ''
    min_diff = 1000
    sizechart = {'48':'S', '53':'M', '58': 'L', '63':'XL', '68':'XXL', '73':'XXXL'}
    for key in sizechart.keys():
        diff = abs(measurement - int(key))
        if diff < min_diff:
            size = sizechart[key]
            min_diff = diff
    return size

def visualize(image, title="Image"):
    plt.figure(figsize=(10, 10))
    plt.imshow(image, cmap="gray")
    plt.title(title)
    plt.show()

def get_size(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            return 'Error: Image not found!'
        
        image = imutils.resize(image, width=500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)
        
        visualize(edged, "Edged Image")

        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        if len(cnts) == 0:
            return 'Error: No contours found!'
        
        c = max(cnts, key=cv2.contourArea)
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        visualize(image, "Contours Detected")

        ((x, y), (w, h), angle) = cv2.minAreaRect(c)
        box = cv2.boxPoints(((x, y), (w, h), angle))
        box = np.array(box, dtype="int")
        
        if len(box) == 0:
            return 'Error: No valid points found!'
        
        box = perspective.order_points(box)
        (tl, tr, br, bl) = box
        
        tltrX, tltrY = midpoint(tl, tr)
        blbrX, blbrY = midpoint(bl, br)
        
        tlblX, tlblY = midpoint(tl, bl)
        trbrX, trbrY = midpoint(tr, br)
        
        dA = distance.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = distance.euclidean((tlblX, tlblY), (trbrX, trbrY))
        
        dimA = min(dA, dB)
        pixelsPerMetric = dimA / 24.0
        
        dimA = dimA / pixelsPerMetric

        print(f"Contour Area: {cv2.contourArea(c)}")
        print(f"Measured Width: {dimA}")
        print(f"Pixels Per Metric: {pixelsPerMetric}")

        size = giveSizeAccordingToMeasurement(dimA)
        print(f"Predicted Size: {size}")
        
        return size
    except Exception as e:
        return 'Error: {}'.format(str(e))

def process_upload(filepath):
    return get_size(filepath)
