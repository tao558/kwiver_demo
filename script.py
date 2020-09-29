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

    dos = ads_out["detected_object_set"]


import time
time.sleep(0.1)
ep.stop()
print("Detected object set generated:", dos, end="\n\n\n")




# Now save the detected object set with another pipeline
path_to_pipe_file = "pipelines/save_dos.pipe"

ep = embedded_pipeline.EmbeddedPipeline()
ep.build_pipeline(path_to_pipe_file)
ep.start()

ads_in = adapter_data_set.AdapterDataSet.create()
ads_in["detected_object_set"] = dos
ads_in["image_file_name"] = im_loc

ep.send(ads_in)
ep.send_end_of_input()

while True:
    ep.receive()

    if ep.at_end():
        break



# The detected object set length and image name should be
# "pickled" to a file. Try loading them:
import pickle
time.sleep(1)
loaded_data = pickle.load(open("set_length_and_image_name.p", "rb"))
loaded_dos_length = loaded_data["set_length"]
loaded_im_loc = loaded_data["image_name"]

assert(loaded_dos_length == len(dos))
assert(loaded_im_loc == im_loc)

print("Loaded set length:", loaded_dos_length, "expected length:", len(dos))
print("loaded image loc:", loaded_im_loc, "expected image loc:", im_loc, end="\n\n\n")