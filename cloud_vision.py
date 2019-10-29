import io
import os
import sys

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    sys.argv[1])

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.object_localization(image=image)
objects = response.localized_object_annotations

output = file_name
for obj in objects:
    if(obj.score >= 0.5):
        output += "," + obj.name + "," + \
            str(round(obj.score, 2))

        for vertex in obj.bounding_poly.normalized_vertices:
            output += (',{},{}'.format(vertex.x, vertex.y))

print output
