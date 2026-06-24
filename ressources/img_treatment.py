import warnings
warnings.filterwarnings('ignore') # Ignore the warnings that appear in the terminal
import numpy as np 
import cv2 as cv
import os

def img_filters(img):
     """
     Function wich take an image in parameter, applied filters on it and create a file with all the new filtered images

     parameter :
        - img : image taken in parameters (can be a str (pathto the image) or an ndarray)
     """
     # ===========================================================
     # VERIFICATION OF THE FILE AND THE IMAGE TAKEN IN PARAMETERS
     # ===========================================================
     output_file = "filtered_images"
     if not os.path.exists(output_file): # If there is no existing folder
          os.makedirs(output_file) # Create the file
     img_save = {}

     if isinstance(img, str): # If the image is a path, we read it using OpenCV
                img2treat = cv.imread(img)
     elif isinstance(img, np.ndarray) : # Otherwise, if the given image is an ndarray, we keep it as is.
                img2treat = img
     else: # Otherwise, an error is returned
                print("/!\ Error. This is not the attend type (str or ndarray)")
                return
     img_save["img_upscale.jpg"] = img2treat # Saving the image to a dictionary

     # =============
     # COLOR SPACES
     # =============
     # ----- RGB -----
     B, G, R = cv.split(img2treat) # Separation of the 3 channels
     img_save["filtered_img_R.jpg"] = R
     img_save["filtered_img_G.jpg"] = G
     img_save["filtered_img_B.jpg"] = B

     # ----- CMY -----
     C, M, Y = cv.split(img2treat) # Separation of the 3 channels
     img_save["filtered_img_C.jpg"] = C
     img_save["filtered_img_M.jpg"] = M
     img_save["filtered_img_Y.jpg"] = Y
     img_save["img_filtre_CMY_inverse.jpg"] = cv.bitwise_not(img2treat)

     # ----- HSV -----
     img_hsv = cv.cvtColor(img2treat, cv.COLOR_BGR2HSV) # Converts the image to HSV color space
     H, S, V = cv.split(img_hsv) # Separation of the 3 channels
     img_save["filtered_img_H.jpg"] = H
     img_save["filtered_img_S.jpg"] = S
     img_save["filtered_img_V.jpg"] = V

     # ----- LAB -----
     img_lab = cv.cvtColor(img2treat, cv.COLOR_RGB2LAB) # Converts the image to the LAB color space
     L2, A2, B2 = cv.split(img_lab) # Separation of the 3 channels
     img_save["filtered_img_L2.jpg"] = L2
     img_save["filtered_img_A2.jpg"] = A2
     img_save["filtered_img_B2.jpg"] = B2

     # ----- YUV -----
     img_yuv = cv.cvtColor(img2treat, cv.COLOR_BGR2YUV) # Converts to YUV color space
     Y2, U2, V2 = cv.split(img_yuv) # Separation of the 3 channels
     img_save["filtered_img_Y2.jpg"] = Y2
     img_save["filtered_img_U2.jpg"] = U2
     img_save["filtered_img_V2.jpg"] = V2

     # ----- GRAY LEVEL AND CONTRAST -----
     img_gray = cv.cvtColor(img2treat, cv.COLOR_BGR2GRAY) # Converts to grayscale
     img_gray = cv.equalizeHist(img_gray)
     clahe = cv.createCLAHE(clipLimit=3.0, tileGridSize=(8,8)) # 
     img_clahe = clahe.apply(img_gray) # Application du filtre clahe
     img_save["filtered_img_GRAY.jpg"] = img_gray
     img_save["filtered_img_CLAHE.jpg"] = img_clahe
     _, bw = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)
     _, bw_inv = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY_INV)
     img_save["filtered_img_BLACK&WHITE.jpg"] = bw
     img_save["filtered_img_BLACK&WHITE_inv.jpg"] = bw_inv

     # ==========================
     # PHYSICAL FILTERS AND EDGES
     # ==========================
     img_blur = cv.bilateralFilter(img_clahe, 9, 75, 75) # Bilateral filter: a filter that smooths the grain of the metal while stopping when edges are detected; the parameters are smoothing strength and edge sensitivity

     # ----- SOBEL -----
     grad_x = cv.Sobel(img_blur, cv.CV_32F, 1, 0, ksize=3) # Calculate the gradient along the X-axis and detect all vertical edges
     grad_y = cv.Sobel(img_blur, cv.CV_32F, 0, 1, ksize=3) # Calculate the gradient along the Y-axis and detect all horizontal edges
     raw_sobel = cv.convertScaleAbs(cv.addWeighted(grad_x, 0.5, grad_y, 0.5, 0))
     img_save["img_bords_sobel_brut.jpg"] = cv.bitwise_not(raw_sobel) # Invert to black on white

     # ----- CANNY -----
     canny = cv.Canny(img_blur, 50, 150) # Filter that draws only solid lines 1 px thick
     img_save["img_bords_canny.jpg"] = cv.bitwise_not(canny) # Invert to black on white

     # ----- TOPOGRAPHY -----
     kernel_rect = cv.getStructuringElement(cv.MORPH_RECT, (25, 25)) # Creates a rectangle core of the size specified in the settings
     blackhat = cv.morphologyEx(img_blur, cv.MORPH_BLACKHAT, kernel_rect) # The black hat filter highlights everything that is darker than the surrounding background, and the rest turns black
     tophat = cv.morphologyEx(img_blur, cv.MORPH_TOPHAT, kernel_rect) # The top hat filter highlights everything that is lighter than the surrounding background
     raw_topography = cv.add(blackhat, tophat) # Add the two filters together to get the number that appears in black on a white background
     normalized_topography = cv.normalize(raw_topography, None, 0, 255, cv.NORM_MINMAX) # Normalizes the topographic filter image
     img_save["img_topo.jpg"] = cv.bitwise_not(normalized_topography) # Invert to black on white

     # =============
     # BINARIZATION
     # =============
     # ----- OTSU -----
     _, otsu = cv.threshold(img_blur, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU) # Thresholding using the Otsu method
     img_save["img_bin_otsu.jpg"] = otsu

     # ----- ADAPTIVE -----
     adaptative = cv.adaptiveThreshold(img_blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 31, 5) # Thresholding using adaptive method
     img_save["img_bin_adaptatif.jpg"] = adaptative

     # ----- BINARY TOPOGRAPHY -----
     _, binary_topography = cv.threshold(normalized_topography, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU) # Image thresholding using the topographic filter
     img_save["img_bin_topographie.jpg"] = binary_topography

     # ==============
     # IMAGES SAVING
     # ==============
     for file_name, image_data in img_save.items():
          path = os.path.join(output_file, file_name)
          cv.imwrite(path, image_data)

     return output_file
