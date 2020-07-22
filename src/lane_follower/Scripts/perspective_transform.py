import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
from combined_thresh import combined_thresh
import os


def perspective_transform(img):
	"""
	Execute perspective transform
	"""
	img_size = (img.shape[1], img.shape[0])
	# src = np.float32(
	# 	[[85, 185], #60 --This is for IGVC test real track images
	# 	 [500, 185],
	# 	 [0, 300], #20
	# 	 [585, 300]])
	# src = np.float32(
	# 	[[470, 40], #60 -- 1st Dataspeed's test
	# 	 [569, 40],
	# 	 [184, 253], #20
	# 	 [876, 253]])
	src = np.float32(
		[[331, 99], #60 -- 1st Dataspeed's test
		 [700, 99],
		 [12, 270], #20
		 [1040, 270]])
	# src = np.float32(
	# 	[[351, 99], #60 -- Dataspeed July 14 Straight
	# 	 [700, 99],
	# 	 [65, 270], #20
	# 	 [1040, 270]])
	# src = np.float32(
	# 	[[450, 50], #60 -- 2nd Dataspeed's test
	# 	 [595, 50],
	# 	 [120, 270], #20
	# 	 [975, 270]])
	dst = np.float32(
		 [[0, 0],
		 [img.shape[1], 0],
		 [0, img.shape[0]],
		 [img.shape[1], img.shape[0]]])

	m = cv2.getPerspectiveTransform(src, dst)
	m_inv = cv2.getPerspectiveTransform(dst, src)

	warped = cv2.warpPerspective(img, m, img_size, flags=cv2.INTER_LINEAR)
	unwarped = cv2.warpPerspective(warped, m_inv, (warped.shape[1], warped.shape[0]), flags=cv2.INTER_LINEAR)  # DEBUG

	return warped, unwarped, m, m_inv


if __name__ == '__main__':
	img_file = os.path.dirname(os.path.abspath(__file__))+'/saves/112_new.png'

	# with open('calibrate_camera.p', 'rb') as f:
	# 	save_dict = pickle.load(f)
	# mtx = save_dict['mtx']
	# dist = save_dict['dist']

	img = mpimg.imread(img_file)
	# img = cv2.undistort(img, mtx, dist, None, mtx)

	img, abs_bin, mag_bin, dir_bin, hls_bin = combined_thresh(img)

	warped, unwarped, m, m_inv = perspective_transform(img)

	plt.subplot(3,1,1)
	plt.imshow(img)
	plt.subplot(3,1,2)
	plt.imshow(warped, cmap='gray', vmin=0, vmax=1)
	plt.subplot(3,1,3)
	plt.imshow(unwarped, cmap='gray', vmin=0, vmax=1)
	fig = plt.gcf()
	fig.set_size_inches(18.5, 10.5)
	plt.show()
