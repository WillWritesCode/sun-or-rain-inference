from bentoml import BentoService, api, env, artifacts
from bentoml.artifact import FastaiModelArtifact
from bentoml.handlers import FastaiImageHandler

from fastai.vision import *
from fastai.imports import *

@env(pip_dependencies=['fastai','torchvision'])
@artifacts([FastaiModelArtifact('sun_rain_classifier')])
class SunRainClassification(BentoService):
    
    @api(FastaiImageHandler)
    def predict(self, image):
        result = self.artifacts.sun_rain_classifier.predict(image)
        return str(result)
