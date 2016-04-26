# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from matplotlib import pyplot as plt
from flower_detection.shapedetector import ShapeDetector
from flower_detection.colorlabeler import ColorLabeler
import numpy as np
import urllib
import cv2
import os
import imutils

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

def shapes(request):

	# load the image, convert it to grayscale, blur it slightly,
	# and threshold it
	image = cv2.imread('octa.png')
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
	result = 'result.png'

	# find contours in the thresholded image
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	arr = []
	# loop over the contours
	for c in cnts:
		# compute the center of the contour
		M = cv2.moments(c)
		if (M["m00"] == 0):
			M["m00"]=1
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])

		# draw the contour and center of the shape on the image

		cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
		cv2.circle(image, (cX, cY), 7, (0, 255, 0), -1)
		cv2.putText(image, "center", (cX - 20, cY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)



	cv2.imwrite(result, image)
	result_data = open(result, "rb").read()
	return HttpResponse(result_data, content_type="image/png")

def shapes2(request):

	# load the image and resize it to a smaller factor so that
	# the shapes can be approximated better
	image = cv2.imread('LcKe78Bca.png')
	resized = imutils.resize(image, width=300)
	ratio = image.shape[0] / float(resized.shape[0])

	# convert the resized image to grayscale, blur it slightly,
	# and threshold it
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

	# find contours in the thresholded image and initialize the
	# shape detector
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	sd = ShapeDetector()

	# loop over the contours
	for c in cnts:
		# compute the center of the contour, then detect the name of the
		# shape using only the contour
		M = cv2.moments(c)

		cX = int((M["m10"] / M["m00"]) * ratio)
		cY = int((M["m01"] / M["m00"]) * ratio)
		shape = sd.detect(c)

		# multiply the contour (x, y)-coordinates by the resize ratio,
		# then draw the contours and the name of the shape on the image
		c=c.astype(np.float_)
		c *= ratio
		c=c.astype(np.int32)
		cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
		cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, (60, 255, 123), 2)

	result = 'result.png'
	cv2.imwrite(result, image)
	result_data = open(result, "rb").read()
	return HttpResponse(result_data, content_type="image/png")

@csrf_exempt #disable csrf
def colorShapeFromImg(request):
	if request.method == 'POST':
		# load the image and resize it to a smaller factor so that
		# the shapes can be approximated better
		image = cv2.imdecode(np.fromstring(request.FILES['file'].read(), np.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)

		resized = imutils.resize(image, width=300)
		ratio = image.shape[0] / float(resized.shape[0])

		# blur the resized image slightly, then convert it to both
		# grayscale and the L*a*b* color spaces
		blurred = cv2.GaussianBlur(resized, (5, 5), 0)
		gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
		lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
		thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

		# find contours in the thresholded image
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]

		# initialize the shape detector and color labeler
		sd = ShapeDetector()
		cl = ColorLabeler()

		response = {}

		# loop over the contours
		for c in cnts:
			# compute the center of the contour
			M = cv2.moments(c)
			cX = int((M["m10"] / M["m00"]) * ratio)
			cY = int((M["m01"] / M["m00"]) * ratio)

			# detect the shape of the contour and label the color
			shape = sd.detect(c)
			color = cl.label(lab, c)

			response['shape']=shape
			response['color']=color

			# multiply the contour (x, y)-coordinates by the resize ratio,
			# then draw the contours and the name of the shape and labeled
			# color on the image
			c=c.astype(np.float_)
			c *= ratio
			c=c.astype(np.int32)
			text = "{} {}".format(color, shape)
			cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
			cv2.putText(image, text, (cX, cY),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

		return response
		result = 'result.png'
		cv2.imwrite(result, image)
		result_data = open(result, "rb").read()
		return HttpResponse(result_data, content_type="image/png")

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

