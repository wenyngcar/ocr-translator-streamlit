import cv2
import numpy as np


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)


def process_image():
    img = cv2.imread("./images/uploaded_image.jpg")
    # Convert image to gray.
    gray_image = grayscale(img)

    # Take the brightness.
    mean_brightness = np.mean(gray_image)

    if mean_brightness < 127:
        # Invert the pixel values.
        gray_image = cv2.bitwise_not(gray_image)

    # Binarize the iamge.
    thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)

    # Remove the noise of image.
    no_noise = noise_removal(im_bw)

    cv2.imwrite("./images/processed_image.jpg", no_noise)
