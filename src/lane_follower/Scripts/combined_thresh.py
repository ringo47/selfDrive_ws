import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
import os


def abs_sobel_thresh(img, orient='x', thresh_min=10, thresh_max=100):

	#Takes an image, gradient orientation, and threshold min/max values

	# Convert to grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	# Apply x or y gradient with the OpenCV Sobel() function
	# and take the absolute value
	if orient == 'x':
		abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0))
	if orient == 'y':
		abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 0, 1))
	# Rescale back to 8 bit integer
	scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
	# Create a copy and apply the threshold
	binary_output = np.zeros_like(scaled_sobel)
	# Here I'm using inclusive (>=, <=) thresholds, but exclusive is ok too
	binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1

	# Return the result
	return binary_output

def mag_thresh(img, sobel_kernel=3, mag_thresh=(30, 100)):

	#Return the magnitude of the gradient
	#for a given sobel kernel size and threshold values

	# Convert to grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	# Take both Sobel x and y gradients
	sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
	sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
	# Calculate the gradient magnitude
	gradmag = np.sqrt(sobelx**2 + sobely**2)
	# Rescale to 8 bit
	scale_factor = np.max(gradmag)/255
	gradmag = (gradmag/scale_factor).astype(np.uint8)
	# Create a binary image of ones where threshold is met, zeros otherwise
	binary_output = np.zeros_like(gradmag)
	binary_output[(gradmag >= mag_thresh[0]) & (gradmag <= mag_thresh[1])] = 1

	# Return the binary image
	return binary_output


def dir_threshold(img, sobel_kernel=3, thresh=(0, np.pi/2)):

	#Return the direction of the gradient
	#for a given sobel kernel size and threshold values

	# Convert to grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	# Calculate the x and y gradients
	sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
	sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
	# Take the absolute value of the gradient direction,
	# apply a threshold, and create a binary image result
	absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))
	binary_output =  np.zeros_like(absgraddir)
	binary_output[(absgraddir >= thresh[0]) & (absgraddir <= thresh[1])] = 1
	binary_output = binary_output.astype(np.uint8)
	# Return the binary image
	return binary_output


def hls_thresh(img, thresh=(100, 255)):

	#Convert RGB to HLS and threshold to binary image using only S channel
	hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
	s_channel = hls[:,:,2]
	binary_output = np.zeros_like(s_channel)
	binary_output[(s_channel > thresh[0]) & (s_channel <= thresh[1])] = 1
	return binary_output

def hls_thresh2(img):
	# Using inRange() to threshold both white and yellow separately.
	hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
	# White areas in image
	# H value can be arbitrary, thus within [0 ... 360] (OpenCV: [0 ... 180])
	# L value must be relatively high (we want high brightness), e.g. within [0.7 ... 1.0] (OpenCV: [0 ... 255])
	# S value must be relatively low (we want low saturation), e.g. within [0.0 ... 0.3] (OpenCV: [0 ... 255])
	white_lower = np.array([np.round(  0 / 2), np.round(0.7 * 255), np.round(0.00 * 255)])
	white_upper = np.array([np.round(360 / 2), np.round(1.00 * 255), np.round(0.30 * 255)])
	white_mask = cv2.inRange(hls, white_lower, white_upper)

	# Yellow areas in image
	# H value must be appropriate (see HSL color space), e.g. within [40 ... 60]
	# L value can be arbitrary (we want everything between bright and dark yellow), e.g. within [0.0 ... 1.0]
	# S value must be above some threshold (we want at least some saturation), e.g. within [0.35 ... 1.0]
	yellow_lower = np.array([np.round( 35/ 2 ), np.round(0.00 * 255), np.round(0.2 * 255)])
	yellow_upper = np.array([np.round( 65 / 2 ), np.round(1.00 * 255), np.round(1.00 * 255)])
	yellow_mask = cv2.inRange(hls, yellow_lower, yellow_upper)
	binary_output = cv2.bitwise_or(yellow_mask, white_mask)


	return binary_output


def combined_thresh(img):
	# print(type(img))
	# print(img.shape)
	# print(img.dtype)
	abs_bin = abs_sobel_thresh(img, orient='x', thresh_min=50, thresh_max=255)
	mag_bin = mag_thresh(img, sobel_kernel=3, mag_thresh=(50, 255))
	dir_bin = dir_threshold(img, sobel_kernel=15, thresh=(0.7, 1.3))
	#hls_bin = hls_thresh(img, thresh=(170, 255))
	hls_bin = hls_thresh2(img)
	combined = np.zeros_like(dir_bin)
	#combined[((abs_bin == 1) | ((mag_bin == 1) & (dir_bin == 1))) & (hls_bin == 1)] = 1
	combined[((abs_bin == 1) | ((mag_bin == 1) & (dir_bin == 1)))] = 1
	combined = cv2.bitwise_and(combined,combined, mask = hls_bin)
	#combined[(combined == 1) & (hls_bin == 1)] = 1

	#print(abs_bin.dtype,mag_bin.dtype,dir_bin.dtype,combined.dtype, hls_bin.dtype)
	return combined, abs_bin, mag_bin, dir_bin, hls_bin  # DEBUG datatype


if __name__ == '__main__':
	img_file = os.path.dirname(os.path.abspath(__file__))+'/saves/112_new.png'
	img = mpimg.imread(img_file)
	if img.dtype == 'float32':
		img = np.array(img)*255
		img = np.uint8(img)
	# with open('calibrate_camera.p', 'rb') as f:
	# save_dict = pickle.load(f)
	# mtx = save_dict['mtx']
	# dist = save_dict['dist']


	# img = cv2.undistort(img, mtx, dist, None, mtx)
	combined, abs_bin, mag_bin, dir_bin, hls_bin = combined_thresh(img)
	print(abs_bin.dtype,mag_bin.dtype,dir_bin.dtype,combined.dtype, hls_bin.dtype)
	
	plt.subplot(2, 3, 1)
	plt.title("Absolute Binary")
	plt.imshow(abs_bin, cmap='gray')

	plt.subplot(2, 3, 2)
	plt.title("Gradient Magnitude")
	plt.imshow(mag_bin, cmap='gray')

	plt.subplot(2, 3, 3)
	plt.title("Gradient Direction")
	plt.imshow(dir_bin, cmap='gray')

	plt.subplot(2, 3, 4)
	plt.title("Original")
	plt.imshow(img)

	plt.subplot(2, 3, 5)
	plt.title("HLS Threshold")
	plt.imshow(hls_bin, cmap='gray')

	plt.subplot(2, 3, 6)
	plt.title("Combined Threshold")
	plt.imshow(combined, cmap='gray')

	plt.tight_layout()
	plt.show()
	
	# #NEW
	# lines = cv2.HoughLinesP(np.uint8(combined), 2, np.pi/180, 100, np.array([]), 50, 80)
	# line_image = np.zeros((combined.shape[0], combined.shape[1], 3), dtype=np.uint8)
	# try:
	# 	for line in lines:
	# 		for x1,y1,x2,y2 in line:
	# 				cv2.line(line_image, (x1, y1), (x2, y2), [255, 0, 0], 20)
	# except TypeError:
	# 	pass
                
	# a = 1
	# b = 1
	# c = 0    
	# # Resultant weighted image is calculated as follows: original_img * a + img * b + c
	# Image_with_lines = cv2.addWeighted(img2, a, line_image, b, c)
	# plt.imshow(Image_with_lines)
	# plt.show()

	# cv2.imshow("HLS", np.uint8(binary_output))
	# if cv2.waitKey(1) & 0xFF == ord('q'):
	# 	cv2.destroyAllWindows()

	# while(True):
	# 	cv2.imshow("HLS", np.float64(combined))
	# 	if cv2.waitKey(1) & 0xFF == ord('q'):
	# 		cv2.destroyAllWindows()
	# 		break
