import os

def capture_image():

    image = "/data/data/com.termux/files/home/Nyra/image.jpg"

    os.system(f'termux-camera-photo -c 0 "{image}"')

    return image
