import cv2 as cv
import numpy as np

def find_circle(img_path):
    """
    Function that takes a given parameter (a path to an image) and returns a circle detected in the image, along with a copy of the image

    parameter :
        - img_path : path to the image in which a circle is to be found

    outputs :
        - circles : parameters for the circle search
        - output : a copy of the processed image 
    """
    img = cv.imread(img_path)
    output = img.copy()
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Conversion of BGR image to Gray

    img_gray = cv.medianBlur(img_gray, 5) # Noise Reduction Through Blurring

    circles = cv.HoughCircles( # Circle Detection
        img_gray, # Image source
        cv.HOUGH_GRADIENT, # Circle Detection Method
        dp=1, # Inverse relationship between the accumulator's resolution and the image's resolution
        minDist=img_gray.shape[0]//2, # Minimum distance between the center and the circle to be detected
        param1=50, # Upper threshold for the internal Canny edge detector
        param2=30, # Center detection threshold      
        minRadius=0, # Minimum radius of the circles to be detected
        maxRadius=0 # Maximum radius of the circles to be detected
    )

    return circles, output

def flatten(circle, input):
    """
    Function that, given the provided parameters (coordinates of a circle and an image), returns a flattened image of the circle

    parameters :
        - circle: parameters for finding the circle
        - input: image to be flattened

    output :
        - flatten_img: image flattened by the process using the two provided parameters
    """
    if circle is not None: # Draw a circle only if he finds one
        circle = np.uint16(np.around(circle)) # Formation of the circle
        x = circle[0][0][0] # Get the x-coordinate of the center
        y = circle[0][0][1] # Get the y-coordinate of the center
        r = circle[0][0][2] # Get the radius of a circle
        cv.circle(input, (x, y), r, (0, 255, 0), 2)  # Circle Perimeter
        cv.circle(input, (x, y), 2, (0, 0, 255), 3)  # Main point

    circumference = int(2 * np.pi * r) # Calculate the circumference of the circle

    unfolded_img = cv.warpPolar( # Single-line image display
        input, # Inputed image
        (r, circumference), # The dimensions of the image to be transformed
        (x,y), # Center of the circle for distortion
        r, # Radius of the circle
        cv.INTER_LINEAR| cv.WARP_POLAR_LINEAR) # Combining interpolation methods and the warppolar mode to realign the image into a single line

    flatten_img = cv.rotate(unfolded_img, cv.ROTATE_90_COUNTERCLOCKWISE)

    return flatten_img
    
