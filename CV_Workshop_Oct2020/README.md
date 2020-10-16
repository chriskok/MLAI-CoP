Installation: 
- git clone --recursive https://github.com/chriskok/MLAI-CoP
- download pre-trained weights from https://github.com/matterport/Mask_RCNN/releases and move the downloaded file into the Mask_RCNN/samples repository
- pip install requirements.txt (highly suggest using the tensorflow and keras versions specified, because tf 2 and recent keras versions have syntax changes)
- OR conda install the requirements (might have issues with 'imgaug' and 'opencv-python' if using conda install --file requirements.txt so I suggest you install those two seperately first)
- python setup.py install
- Follow along the tutorial in Mask_RCCN/samples/demo.ipynb
