import warnings
warnings.filterwarnings('ignore') # Ignore the warnings that appear in the terminal
import torch # AI Engine
import numpy as np 
import cv2 as cv
from basicsr.archs.rrdbnet_arch import RRDBNet # Mathematical models for upscaling
from realesrgan import RealESRGANer # framework for using the upscaling model
import os

model_path = 'code/RealESRGAN_x4plus.pth' # The Path to the Upscaling Model

def upscaling(img):
        """
        Function that takes an image path or a NumPy array as a parameter and returns an upscaled version of the image using the Real-ESRGAN model.

        parameter :
            - img : path to the image file (string) or the image data (NumPy ndarray) to be upscaled

        outputs :
            - img_upscale : the processed and upscaled image as a NumPy array
            - None : if the provided input type is incorrect
        """

        if isinstance(img, str): # If the image is a path, read it using OpenCV
                img_upscale = cv.imread(img)
        elif isinstance(img, np.ndarray) : # Otherwise, if the given ipage is an ndarray, we keep it as is.
                img_upscale = img
        else: # Otherwise, an error is returned
                print("/!\ Error: This is not the expected type.")
                return None

        if torch.backends.mps.is_available(): # If there's a Mac GPU
                device = torch.device('mps') # The device used is the Mac GPU
        elif torch.cuda.is_available(): # If there is an NVIDIA GPU
                device = torch.device('cuda')# The device used is the Nvidia GPU
        else : # If no GPU is detected
                device = torch.device('cpu') # The device being used is the machine's CPU

        state_dict = torch.load(model_path, map_location = device)['params_ema'] # Loads the memory into the available device and retrieves the training data

        model = RRDBNet(num_in_ch = 3, # 3 color channels supported for input
                        num_out_ch = 3, # 3 color output channels
                        num_feat = 64, # Model architecture settings /!\ Do not modify
                        num_block = 23, # Model architecture settings /!\ Do not modify
                        num_grow_ch = 32, # Model architecture settings /!\ Do not modify
                        scale = 4 # To multiply the size by the factor
                        )
        model.load_state_dict(state_dict, strict= True) # Chargement du modèle

        upsampler = RealESRGANer(scale = 4, # To multiply the size by the factor
                                model_path = model_path, # Path to the upscaling model
                                model = model, # Loading the model
                                tile = 256, # Split the image into several 256x256 sections
                                tile_pad = 10, # 10-pixel overflow beyond the square to prevent artifacts during reassembly
                                pre_pad = 0, 
                                half = False # To avoid mathematical errors
                                )

        img_upscale, _ = upsampler.enhance(img_upscale, outscale=4) # the process of creating the image from the model

        return img_upscale
