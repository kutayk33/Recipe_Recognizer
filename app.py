# Libraries
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from imageio.core.util import asarray
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import os

# Dictionary to save the informations
dic = {}

## Form Recognizer Configuration ##

# Endpoint and Key
endpoint_f = "https://recettesfromrecognizer.cognitiveservices.azure.com/"
key_f = "dee1ba127bbf442489c58a86932ae162"

# Authenticate the client object
form_recognizer_client = FormRecognizerClient(endpoint_f, AzureKeyCredential(key_f))

# Model ID (The Model that we have trined on Azure Labeling Tool)
model_id = "491ce87f-878c-4eaf-8bc4-a336a4a209a5"

# image path
image_path = os.path.join("test_images", "test3.jpg")


# Open and test the image
with open(image_path, "rb") as f:
    poller = form_recognizer_client.begin_recognize_custom_forms(
        model_id=model_id, form=f
    )
# Result of the test for new image
forms = poller.result()

# To get cles and valeurs
for recognized_form in forms:
    for name, field in recognized_form.fields.items():
        print(
            " '{}' : ({}) Accuracy  \n '{}' \n".format(
                name,
                field.confidence,
                field.value,
            )
        )
        dic[name] = field.value

## Costum Vision Configuration ##

# Endpoint and Key
endpoint_c = "https://testdeletes123.cognitiveservices.azure.com/"
key_c = "de6ba6ab6d3246e48cdba750fbd0f17e"

# Authenticate the client object
computervision_client = ComputerVisionClient(
    endpoint_c, CognitiveServicesCredentials(key_c)
)

# Open the test image
im = Image.open(image_path)
img = open(image_path, "rb")

# Detect the photo on the image :)
detected_object = computervision_client.detect_objects_in_stream(img)

# This example detects different kinds of objects with bounding boxes in a remote image.
X = ""
Xw = ""
Y = ""
Yh = ""

if len(detected_object.objects) == 0:
    print("No objects detected.")

else:
    for object in detected_object.objects:
        X = object.rectangle.x
        Xw = object.rectangle.x + object.rectangle.w
        Y = object.rectangle.y
        Yh = object.rectangle.y + object.rectangle.h

# Create Box
box = (X, Y, Xw, Yh)

# Crop Image
area = im.crop(box)
area.show()
# Convert the image to an array
image_array = asarray(area)
dic["image"] = image_array

# Save Image
# area.save("images_extract/TEST.png", "PNG")

# print(dic)

