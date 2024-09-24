import cv2

# Read the image from file
image = cv2.imread('xdd.jpg')
print(image.shape)

# Display the image in a window
cv2.imshow('Image', image)

# Wait for a key press indefinitely or for a specified amount of time in milliseconds
cv2.waitKey(0)

# Destroy all the windows created by OpenCV
cv2.destroyAllWindows()