import cv2

img = []
width = 0
ratio = 0
height = 500

def segment(hlimit,wlimitl,wlimitu):
	global img, width, ratio

	#grayscale
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	#binarize 
	ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)

	#find contours
	im2,ctrs, hier = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
	cv2.CHAIN_APPROX_SIMPLE)

	#sort contours
	sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

	segments = []
	ys = []

	for i, ctr in enumerate(sorted_ctrs):
			# Get bounding box
			x, y, w, h = cv2.boundingRect(ctr)

			if h < hlimit:
				continue
			if w < width*wlimitl or w > width*wlimitu:
				continue

			# Getting ROI
			roi = img[y:y+h, x:x+w]

			#store segment
			segments.append(roi)
			ys.append(y)
			
			#mark reactange
			#cv2.rectangle(img,(x,y),( x + w, y + h ),(90,0,255),2)

	#cv2.imshow('marked areas',img)
	#cv2.waitKey(0)
	return segments, ys

def startSegment():
	global img, width, height, ratio

	img = cv2.imread('test4.png')

	h, w = img.shape[:2]
	ratio = w/h

	if ratio < 3:
		# 2 line plate

		width = int(height*2 * ratio)
		img = cv2.resize(img, (width, height*2))

		segments, ys = segment(height/4,0.03,0.3)

		segu = []
		segl = []
		for i,seg in enumerate(segments):
			if ys[i] < height*2*0.3:
				segu.append(seg)
			else:
				segl.append(seg)
		segments = segu + segl
	else:
		# 1 line plate
		width = int(height * ratio)
		img = cv2.resize(img, (width, height))

		segments = segment(height/2,0.03,0.2)[0]

	return segments

for x in startSegment():
	cv2.imshow('i',x)
	cv2.waitKey(0)
