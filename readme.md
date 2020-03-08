# Weather Inference

This is a basic weather inference app created during my run of the FastAI course v3.

It only has 2 output classes as I wanted to keep the dataset gathering and training time down as it's only a demo.

Currently deployed here (backend not written yet) http://experiments.pythonanywhere.com/

# Frontend

Bulma CSS framework with minor customisation + illustrations.

Consider using steps component to make the process clear: https://github.com/aramvisser/bulma-steps


## Resources:

* Deep Learning Course: [FastAI](https://course.fast.ai)
* CSS Framework: [Bulma](http://bulma.io)
* Icon Font: [Fontawesome](https://fontawesome.com)
* Illustrations: 
  * [Undraw](https://undraw.co)
  * [GraphicMaker](https://designs.ai/graphicmaker)
* Placeholder Images (while laying out)
  * [Fill Murray](https://www.fillmurray.com/1920/1080")
  * [Placehold.it](http://placehold.it/256x256)


# Backend

I chose [Flask](https://palletsprojects.com/p/flask/) as the backend as:
* the model is already in Python (so no coversions or bridge libraries to worry about)
* means I can use https://www.pythonanywhere.com/ for free hosting
* it's much lighter weight/less setup than Django & simple to work with from a static frontend

## TODO:
* Confirm Flask, FastAI or Starlette as backend
  * or jump ship and go with Node.js hosting 
    * https://github.com/zeit/now/tree/master/examples
    * https://forums.fast.ai/t/puting-the-model-into-production-web-apps/29011
    * https://medium.com/@zachcaceres/deploying-a-deep-learning-image-classification-model-with-fastai-python-and-nodejs-cdc491b56368
* Prepare env in PythonAnywhere (install FastAI and relevant framework(s))
  * need to tread carefully due to disk space (500MB) and web console (max output per command) limitations https://www.pythonanywhere.com/forums/topic/14196/
  * watch put for pip cache
* add a direct URL entry/selection option for files on the web
* Starlette 
  * https://mc.ai/fast-ai-2019-lesson-2-production-sgd-from-scratch/
  * example: https://medium.com/@lankinen/fastai-model-to-production-this-is-how-you-make-web-app-that-use-your-model-57d8999450cf
  * https://forums.fast.ai/t/easy-vision-model-deployment/41109
  * https://towardsdatascience.com/how-to-deploy-your-machine-learning-web-app-to-digital-ocean-64bd19ce15e2
  * https://forums.fast.ai/t/deploying-classification-app-with-starlette-and-nginx-as-a-reverse-proxy/30070
* Flask
  * https://www.roytuts.com/python-flask-file-upload-example/
  * https://palletsprojects.com/p/flask/

* Embedding in Notebook:
  * https://medium.com/@pierre_guillou/deep-learning-web-app-by-fastai-v1-3ab4c20b7cac
  * https://forums.fast.ai/t/puting-the-model-into-production-web-apps/29011/103