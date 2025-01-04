import subprocess
from datetime import datetime
import os

import picamera
# Function that handles photo capture using the Raspberry Pi camera
# Returns the path of the saved photo

def snap_photo():
    # Initialize the Raspberry Pi camera
    if not os.path.isdir('temp'):
        os.mkdir('temp')
    camera = picamera.PiCamera()
    try:
        # Set the resolution of the camera (optional)
        camera.resolution = (768, 768) 
        # Capture a photo
        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"photo_{date}.jpg"
        camera.capture(filename)
        camera.close()
        return filename
    except:
        print("Camera Failed.")
