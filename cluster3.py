import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim
# ssim being the structural similarity index

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

# placeholder image array, will be replaced with a passed-in
# array of cluster image filenames
pics = ["puppy.jpg", "puppy2.jpg", "pizza.jpg", "pizza2.jpg", "puppy3.jpg", "puppy4.jpg"]
size = len(pics)
mseArr = []
ssimArr = []
for i in range(0, size):
  mseArr.append(0)
  ssimArr.append(0)
  for j in range(0, size):
    if(i != j):
      imageA = cv2.imread(pics[i])
      imageA = cv2.resize(imageA, (500, 500))
      imageB = cv2.imread(pics[j])
      imageB = cv2.resize(imageB, (500, 500)) 
      err = mse(imageA, imageB)
      s = ssim(imageA, imageB, multichannel=True)
      mseArr[i] = mseArr[i] + err;
      ssimArr[i] = ssimArr[i] + abs(s);

if(size < 4):
  print(pics)
else:
  tmp=list(ssimArr)
  ssimArr.sort()
  mostSim = tmp.index(ssimArr[-1])
  secondSim = tmp.index(ssimArr[-2])
  thirdSim = tmp.index(ssimArr[-3])
  fourthSim = tmp.index(ssimArr[-4])
  if(ssimArr[-3] == ssimArr[-4]):
    if(mseArr[thirdSim] > mseArr[fourthSim]):
      thirdSim = fourthSim
  returnArr = [pics[mostSim], pics[secondSim], pics[thirdSim]]
  print(returnArr)
