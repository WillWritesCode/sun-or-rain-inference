from bentoml import load
# 1) import the custom BentoService
from classes.bentoml_service import SunRainClassification
from fastai.vision import *

def pack_and_save_bento(output_path):
    # 2) `pack` it with required artifacts
    service = SunRainClassification()
    learn = load_learner("inference", "sun_rain_classifier.pkl")
    service.pack("sun_rain_classifier", learn)

    # 3) save your BentoSerivce
    service.save_to_dir(output_path)


#  4) Load bento service
def load_service():
    BASE_PATH = "inference/bentoml_bundles"
    SERVICE_PATH = f"{BASE_PATH}/SunRainClassification"
    if not os.path.isdir(SERVICE_PATH):
        if not os.path.isdir(BASE_PATH):
            os.mkdir(BASE_PATH)
        pack_and_save_bento(BASE_PATH)
    return load(SERVICE_PATH)
