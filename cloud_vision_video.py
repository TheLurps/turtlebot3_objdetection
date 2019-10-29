import io
import os
import sys
import cv2
import math
import random

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the video file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    sys.argv[1])

video = cv2.VideoCapture(file_name)
count = 0

categories = []
colors = []

#fourcc = video.get(cv2.CAP_PROP_FOURCC)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
fps = video.get(cv2.CAP_PROP_FPS)
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

print("Load video file: %s with %f FPS in %d x %d" %
      (file_name, fps, width, height))
writer = cv2.VideoWriter(
    sys.argv[2],
    fourcc,
    fps,
    (width, height))

while (video.isOpened()):
    print("Read frame %d" % count)
    ret, frame = video.read()

    if ret == True:
        count += 1
        #cv2.imshow("frame", frame)

        cv2.imwrite("frame.jpg", frame)
        # Loads the image into memory
        with io.open("frame.jpg", "rb") as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        # Performs label detection on the image file
        response = client.object_localization(image=image)
        objects = response.localized_object_annotations

        output = ""
        for obj in objects:
            if(obj.score >= 0.5):
                output += "," + obj.name + "," + \
                    str(round(obj.score, 2))

                new_category = True
                for c in categories:
                    if c[0] == obj.name:
                        new_category = False
                        break
                if new_category:
                    categories.append(obj.name)
                    colors.append([random.randint(
                        0, 255), random.randint(0, 255), random.randint(0, 255)])

                category_num = categories.index(obj.name)
                color = (
                    (colors[category_num][0], colors[category_num][1], colors[category_num][2]))

                for vertex in obj.bounding_poly.normalized_vertices:
                    output += (',{},{}'.format(vertex.x, vertex.y))

                x1 = int(math.floor(
                    obj.bounding_poly.normalized_vertices[0].x * 640))
                x2 = int(math.floor(
                    obj.bounding_poly.normalized_vertices[1].x * 640))
                y1 = int(math.floor(
                    obj.bounding_poly.normalized_vertices[0].y * 480))
                y2 = int(math.floor(
                    obj.bounding_poly.normalized_vertices[2].y * 480))
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, obj.name, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, lineType=cv2.LINE_AA)

                print(output)

        writer.write(frame)
        cv2.imshow("result", frame)

    else:
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


video.release()
writer.release()
cv2.destroyAllWindows()
