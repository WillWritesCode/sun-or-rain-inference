from classes.bentoml_packager import load_service
from fastai.vision import *
import os.path

service = load_service()

# 5) test that it works
img = open_image("test_images/sun.jpg")
print(service.predict(img))

img = open_image("test_images/rain.jpg")
print(service.predict(img))
