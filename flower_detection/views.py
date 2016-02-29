# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from matplotlib import pyplot as plt
import numpy as np
import urllib
import json
import cv2
import os

# define the path to the face detector
FACE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_frontalface_default.xml".format(
	base_path=os.path.abspath(os.path.dirname(__file__)))

@csrf_exempt
def detect(request):
	# initialize the data dictionary to be returned by the request
	data = {"success": False}

	# check to see if this is a post request
	if request.method == "POST":
		# check to see if an image was uploaded
		if request.FILES.get("image", None) is not None:
			# grab the uploaded image
			image = _grab_image(stream=request.FILES["image"])

		# otherwise, assume that a URL was passed in
		else:
			# grab the URL from the request
			url = request.POST.get("url", None)

			# if the URL is None, then return an error
			if url is None:
				data["error"] = "No URL provided."
				return JsonResponse(data)

			# load the image and convert
			image = _grab_image(url=url)

		# convert the image to grayscale, load the face cascade detector,
		# and detect faces in the image
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		detector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
		rects = detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5,
			minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

		# construct a list of bounding boxes from the detection
		rects = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in rects]

		# update the data dictionary with the faces detected
		data.update({"num_faces": len(rects), "faces": rects, "success": True})

	# return a JSON response
	return JsonResponse(data)

def findContours(request):
	im = cv2.imread('flower2.jpg')
	initial_mean_color = cv2.mean(im)

	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,127,255,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#cv2.drawContours(im, contours, -1, (123,255,31), 3)


	# img = cv2.imread('octa.png')
	# ret,thresh = cv2.threshold(img,127,255,0)
	# contours,hierarchy = cv2.findContours(thresh, 1, 2)

	cnt = contours[0]


	M = cv2.moments(cnt)
	#centroids
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])

	#contour area
	area = cv2.contourArea(cnt)

	#contour perimeter
	perimeter = cv2.arcLength(cnt,True)

	#contour approximation
	epsilon = .01*cv2.arcLength(cnt,True)
	approx = cv2.approxPolyDP(cnt,epsilon,True).tolist()

	#convex hull
	hull = cv2.convexHull(cnt).tolist()

	#convexity
	isContourConvex = cv2.isContourConvex(cnt)

	jsonData = {
		"centroid":{
			"cx":cx,
			"cy":cy
		},
		"area":area,
		"perimeter":perimeter,
		"approx":approx,
		"approx-length":len(approx),
		"hull":hull,
		"hull-length":len(hull),
		"is-convour-convx":isContourConvex,
		"initial_mean_color":initial_mean_color
	}

	return JsonResponse(jsonData)

def featureDetection(request):
	jsonData = {
		"success":False
	}
	img = cv2.imread('flower.png')
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
	corners = np.int_(corners)

	for i in corners:
		x,y = i.ravel()
		cv2.circle(img,(x,y),3,255,-1)

	plt.imshow(img),plt.show()


	jsonData.update({"success":True})

	return JsonResponse(jsonData)

def _grab_image(path=None, stream=None, url=None):
	# if the path is not None, then load the image from disk
	if path is not None:
		image = cv2.imread(path)

	# otherwise, the image does not reside on disk
	else:	
		# if the URL is not None, then download the image
		if url is not None:
			resp = urllib.urlopen(url)
			data = resp.read()

		# if the stream is not None, then the image has been uploaded
		elif stream is not None:
			data = stream.read()

		# convert the image to a NumPy array and then read it into
		# OpenCV format
		image = np.asarray(bytearray(data), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
	# return the image
	return image
