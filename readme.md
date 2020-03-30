# Weather Inference

This is a basic weather inference app created during my run of the FastAI course v3.

It only has 2 output classes as I wanted to keep the dataset gathering and training time down as it's only a demo.

Currently deployed here (backend not written yet) http://experiments.pythonanywhere.com/

## Note
The trained model isn't that good - it's easy to find raining images which are miss-classified.
* Training was shortened as I was running locally on CPU, but I did cycle through fine tuning + LR Find a couple of times and didn't keep track of epochs
* Validation error rate was ~6.8%
* Dataset ended up being pretty small, so likely I need more training data to resolve that + I may have biassed the dataset with manual selection and manual cleaning.

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
**Not Written Yet**

I'll probably go with [Flask](https://palletsprojects.com/p/flask/) as the backend as:
* the model is already in Python (so no coversions or bridge libraries to worry about)
* means I can use https://www.pythonanywhere.com/ for free hosting
* it's much lighter weight/less setup than Django & simple to work with from a static frontend


## Exploring

### BentoML
https://github.com/bentoml/BentoML

BentoMl aims to simplify packaging & deployment of a pre-trained model to various clouds.  It produces API endpoints automatically based on simple patterns from their "handlers" module.

Handlers are available for common inference tasks (image classifier, value predictions etc.) in most common ML frameworks.

The endpoints it produces have a Swagger/OpenAPI test harness auto-generated, which is great for testing and for documenting to developers (Connexion API framework from Zalando has a similar trick on that front).

It looked like a good option to shorten deployment and reduce time spent pandering to the specific needs of cloud vendors or other platforms.  I did have a fair amount of trouble getting things running - likely mostly down to version incompatibilityies/dependency specification issues & I did get it running.
(I've found with most of these tools, they're not that mature/don't have a wide enough user-base to resillient across version changes in various dependencies or in Python itself)

Deployment comes via Dockerisation (it auto-generates a Dockerfile, environment vars file, setup script etc. which could shorten time-to-deploy) and integration with a couple of cloud API's and/or some manual [deployment instructions from BentoML](https://docs.bentoml.org/en/latest/deployment/index.html).

I need to decide whether the additional dependencies are worth it vs a more hand-rolled approach - should be clearer once I've deployed to a host using BentoML tooling.

```sh
# can't use Python 3.8 with bentoml, needs at least 3.7, pytorch seems to need 3.7 still
conda create -n bentoml python=3.7 -y
conda activate bentoml
# installations for IDE extensions, Pylint etc. + image processing libs
conda install -n bentoml autopep8 pylint Pillow imageio -y
# bentoml not available via conda install, fastai installed via conda doesn't work with this, so use pip for that too
pip install bentoml fastai

# running
cd ./backend
python run_bento.py
```
**Appears to be working!**
`bento_bundles` directory is ~94MB - pretty sure that's just the model/config files i.e. not including any dependencies.


| Test image | Source |
| ---------- | ------ |
| rain.jog   | https://unsplash.com/photos/mODxn7mOzms |
| sun.jpg    | https://images.unsplash.com/photo-1529923123842-3310dfdc0b10?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80 |

#### Issues:


* [x] `bentoml serve SunRainClassification:latest`
  * `AttributeError: 'zipimport.zipimporter' object has no attribute 'path'`     
  * Workaround in `~/Applications/anaconda3/lib/python3.6/site-packages/bentoml/utils/pip_pkg.py`
    * at line 79, enclose the "searched modules" code in an id, checking that the object has the attribute: `path` as follows:
      ```python
       if hasattr(m.module_finder, "path"): #this line is the workaround 
           path = m.module_finder.path
           is_local = self.is_local_path(path)
           self.searched_modules[m.name] = ModuleInfo(
               m.name, path, is_local, m.ispkg
           )
      ```
    * no idea what side effects that will have, but it got me up and running - submitting an image via the Swagger test harness works!
* [x] `serve` by saved path `bentoml serve "inference/bento_bundles/SunRainClassification"`
  * expects `either specify the file path of the BentoService saved bundle, or the BentoService id in the form of "name:version"`
  * stupid typo - works with correct path `bentoml serve "inference/bentoml_bundles/SunRainClassification"`
* [ ] Generated API endpoint requires image data, so I'll need to pull the image in in JS before pushing it to the server (probably use that as an opportunity to shrink it first)
* [ ] Need to actually deploy it somehwere and test a live version



## Discarded Options
### Algorithmia
[Algorithmia](https://algorithmia.com/) seems like a great option if you're wortking in Pytorch or Tensorflow directly.  It produces an endpoint you can call directly for training or inference, using an API key for access.
https://docs.fast.ai/basic_train.html#Saving-and-loading-models

#### But :
* the format is a bit proprietary, so you've got another set of conventions to consider when making your production stack
* FastAI isn't avaialble for import, so within the deployed algo, you need to work in Pytorch/Caffe/Tensorflow etc.
* working with a FastAI pre-trained model is beyond my skills right now - I've burnt a bunch of time trying to get it running, but realistically, I needed to export the model differently from FastAI
* https://algorithmia.com/algorithms/stephanie/pytorchjitgpu/source
### PythonAnywhere
PythonAnyhwhere offers free Python App hosting (AFAIK CPU only).
Great option for prototyping/hobby websites, pretty flexibly, but difficult to use with FastAI due to the size of the dependencies.

* Prepare env in PythonAnywhere (install FastAI and relevant framework(s))
  * need to tread carefully due to disk space (500MB) and web console (max output per command) limitations https://www.pythonanywhere.com/forums/topic/14196/
    * watch put for pip cache
  * Can't use PythonAnywhere free tier - disk limit 500MB PyTorch 1.4 > 700MB tarballed
    * even the CPU version unzips to >500MB

It might be possible to get TorchScript or Tensorflow inference running within the 500MB space limits.

## TODO:

* add a direct URL entry/selection option for files on the web
* Confirm Flask, FastAI or Starlette as backend
  * or jump ship and go with Node.js hosting 
    * https://github.com/zeit/now/tree/master/examples
    * https://forums.fast.ai/t/puting-the-model-into-production-web-apps/29011
    * https://medium.com/@zachcaceres/deploying-a-deep-learning-image-classification-model-with-fastai-python-and-nodejs-cdc491b56368
    * https://course.fast.ai/deployment_zeit.html
    * https://zeit.co/docs/runtimes#official-runtimes/python
    * https://github.com/nikhilno1/healthy-or-not/blob/master/heroku-deploy.md
* Docker deployment (somewhere)
  * https://hub.docker.com/r/ryangrahamnc/fastai-cpu
  * https://hub.docker.com/r/gilmoreno/fastai
  * https://hub.docker.com/r/nebfield/fastai-cpu
  * https://hub.docker.com/r/morphles/fastai
  * https://hub.docker.com/r/dimitrijd/fastai
  * https://hub.docker.com/r/chrispeely/guitarid
  * https://hub.docker.com/r/fr0zenbanana/mushroom-helper
* Connexion API framework - https://connexion.readthedocs.io/en/latest/
  * Connexion example for FastAI - https://github.com/IaroslavR/fastai-rest-server-template
  * https://jobs.zalando.com/en/tech/blog/connexion-zalando-open-source/?gh_src=4n3gxh1%3Fgh_src%3D4n3gxh1
    * https://github.com/elvinx/connexion-example
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


## ML Model
Based on the workflow used for the pet classifier in lesson2 of the FastAIv3 course.
See: https://github.com/BestWillInTheWorld/fast.ai-course/blob/master/lesson2-download/lesson2-download.ipynb