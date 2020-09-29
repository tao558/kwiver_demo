# First get the image to be used in the pipeline
import requests

url = "https://raw.githubusercontent.com/Kitware/kwiver/master/examples/images/soda_circles.jpg"
im_loc = "images/soda_circles.jpg"

f = open(im_loc,'wb')
f.write(requests.get(url).content)
f.close()


# Now load the image as a vital type
from PIL import Image
import numpy as np
import kwiver.vital.types as kvt

np_image = np.array(Image.open(im_loc))
vital_im = kvt.Image(np_image)
im_container = kvt.ImageContainer(vital_im)


# Run the pipeline
from kwiver.sprokit.adapters import adapter_data_set, embedded_pipeline

path_to_pipe_file = "pipelines/hough_detector.pipe"

ep = embedded_pipeline.EmbeddedPipeline()
ep.build_pipeline(path_to_pipe_file)

ep.start()

ads_in = adapter_data_set.AdapterDataSet.create()
ads_in["image"] = im_container
ep.send(ads_in)
ep.send_end_of_input()

while True:
    ads_out = ep.receive()
    if ads_out.is_end_of_data():
        break

import time
time.sleep(5)
ep.stop()