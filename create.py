import cv2
import numpy as np
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter


## Inverts the image pixels
def create_img():
## invert the mask image
	image = Image.open("C:/Users/nikhi/Desktop/wil/New folder/shape/plot_shapes/1373.png")
	image_data = np.asarray(image);
	pix = image.load()

## access each pixel using the for loop
	for i in range(len(image_data)):
		for j in range(len(image_data[0])):
			##if the pixel is white change it to black
				if(pix[i,j] == (0,0,0,0)):
					pix[i,j] = (0,0,0,255) 
			## if the pixel is black change it to white
				elif(pix[i,j] == (0,0,0,255)):
					pix[i,j] = (0,0,0,0)

## Save the image
	image.save("inverted_img.png")


	## enhance the cloudless image
def enhance_image(image_date):
	field_day = Image.open("C:/Users/nikhi/Desktop/project_images/cloudless timeseries/{}.png".format(image_date))
	enhancer = ImageEnhance.Brightness(field_day)
	enhancer.enhance(2.5).filter(filter=ImageFilter.EDGE_ENHANCE_MORE).save(r"C:/Users/nikhi/Desktop/project_images/enhancer/{}.png".format(image_date))




## select a image and apply kmeans
def apply_kmeans(image_date):
    
	field_day = cv2.imread("C:/Users/nikhi/Desktop/project_images/enhancer/{}.png".format(image_date))
	Z = field_day.reshape((-1,3))
# convert to np.float32
	Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	K = 5
	ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

# Now convert back into uint8, and make original image
	center = np.uint8(center)
	res = center[label.flatten()]
	res2 = res.reshape((field_day.shape))

	#cv2.imshow('res2',res2)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	cv2.imwrite("C:/Users/nikhi/Desktop/project_images/kmeans/clustered_field-{}.png".format(image_date),res2)


def trial():
	## store the mask image in an object called mask
	mask = Image.open("C:/Users/nikhi/Documents/Python Scripts/wil project/w.jpeg")
	## super impose the mask_inverted image on ndvi image
	superimpose_img = Image.open("C:/Users/nikhi/Documents/Python Scripts/wil project/enhance.png")
	superimpose_img.paste(mask,(0,0),mask)
	superimpose_img.save("C:/Users/nikhi/Documents/Python Scripts/wil project/result.png")


## intensify the green pixels
def intensify_green(image_date):
	img = cv2.imread("C:/Users/nikhi/Desktop/project_images/kmeans/clustered_field-{}.png".format(image_date))

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	greenMask = cv2.inRange(hsv, (26, 10, 30), (97, 100, 255))

	img[greenMask == 255] = (0, 255, 0)

	cv2.imwrite("C:/Users/nikhi/Desktop/project_images/intensify_greenColor/{}.png".format(image_date),img)


## superimpose the sugarcane mask image on the clustered image
def mask_superimpose(image_date):
	## store the mask image in an object called mask
	mask = Image.open("C:/Users/nikhi/Desktop/project_images/mask.png")
	## super impose the mask_inverted image on ndvi image
	superimpose_img = Image.open("C:/Users/nikhi/Desktop/project_images/intensify_greenColor/{}.png".format(image_date))
	superimpose_img.paste(mask,(0,0),mask)
	superimpose_img.save("C:/Users/nikhi/Desktop/project_images/superimpose_mask/masked-{}.png".format(image_date))



## superimpose the a particular plot number on a clsutered image
def plot_superimpose(image_date,plot_no):
	## store the particular plot shape mask in an object called plot_mask
	plot_mask = Image.open("C:/Users/nikhi/Desktop/project_images/plot_shapes/{}.png".format(plot_no))
	superimpose_img = Image.open("C:/Users/nikhi/Desktop/project_images/superimpose_mask/masked-{}.png".format(image_date))
	superimpose_img.paste(plot_mask,(0,0),plot_mask)
	superimpose_img.save("C:/Users/nikhi/Desktop/project_images/imposedPlot_shapes/maskPlot-{}.png".format(image_date))


## count the number of green pixels in the image using hue 
def count_greenPixels(image_date):
	# get the rgb and hsv format of the image
	rgb_format = Image.open("C:/Users/nikhi/Desktop/project_images/imposedPlot_shapes/maskPlot-{}.png".format(image_date)).convert('RGB')
	hsv_format = rgb_format.convert('HSV')

	# Create a numpy array from the images to access the pixel values
	rgb_np = np.array(rgb_format)
	hsv_np = np.array(hsv_format)

	# Extract Hue
	H = hsv_np[:,:,0]

	# filter all the green pixel values where the values range from 100 to 140 in hsv
	low,high = 100,140

	# Rescale to 0-255, rather than 0-360 because we are using uint8
	low = int((low * 255) / 360)
	high = int((high * 255) / 360)
	green = np.where((H>low) & (H<high))

	# Convert all the green pixels to white 
	rgb_np[green] = [255,255,255]

	count = green[0].size

	# print the number pixels matching the criteria specified above
	print("Pixels matched: {}".format(count))
	Image.fromarray(rgb_np).save("C:/Users/nikhi/Desktop/project_images/result/{}.png".format(image_date))
	return(count)