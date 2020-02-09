import http.client
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
from msrest.authentication import CognitiveServicesCredentials

KEY = os.environ["FACE_SUBSCRIPTION_KEY"]
ENDPOINT = os.environ['FACE_ENDPOINT'] # Create an authenticated FaceClient.

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

### TRAINING OF GROUPS

PERSON_GROUP_ID = 'tank-top-high-school-pupil9'

# Used for the Snapshot and Delete Person Group examples.
TARGET_PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)

'''
Create the PersonGroup
'''
# Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
print('Person group:', PERSON_GROUP_ID)
# TODO: THis shouldn't need commenting out hmm
face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

# Define woman friend
kaz = face_client.person_group_person.create(PERSON_GROUP_ID, "kaz")
# Define man friend
alex = face_client.person_group_person.create(PERSON_GROUP_ID, "alex")
# Define child friend
adele = face_client.person_group_person.create(PERSON_GROUP_ID, "adele")

'''
Detect faces and register to correct person
'''
# Find all jpeg images of friends in working directory
# kaz_images = [file for file in glob.glob('src/resource/*') if file.startswith("kaz")]
# alex_images = [file for file in glob.glob('resource/*') if file.startswith("alex")]
# adele_images = [file for file in glob.glob('resource/*') if file.startswith("adele")]


kaz_images = [file for file in glob.glob('resource/kaz.jpeg')]
alex_images = [file for file in glob.glob('resource/alex.jpeg')]
adele_images = [file for file in glob.glob('resource/adele.jpeg')]

print(len(kaz_images))

# Add to a woman person
for image in kaz_images:
    w = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, kaz.person_id, w)

# Add to a man person
for image in alex_images:
    m = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, alex.person_id, m)

# Add to a child person
for image in adele_images:
    ch = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, adele.person_id, ch)

'''
Train PersonGroup
'''
print()
print('Training the person group...')
# Train the person group
face_client.person_group.train(PERSON_GROUP_ID)

while (True):
    training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
    print("Training status: {}.".format(training_status.status))
    print()
    if (training_status.status is TrainingStatusType.succeeded):
        break
    elif (training_status.status is TrainingStatusType.failed):
        sys.exit('Training the person group has failed.')
    time.sleep(5)


### DETECTION OF PEOPLE:

# conn = http.client.HTTPConnection("api,meraki,com")

# payload = "{}"

# headers = {
    # 'Accept': "*/*",
    # 'Content-Type': "application/json",
    # 'cache-control': "no-cache",
    # 'Postman-Token': "62485006-55c4-495a-aa86-ddd6d0aaf024"
    # }

# conn.request("POST", "api,v0,networks,L_575897802350005364,cameras,Q2FV-UGQQ-3DF4,snapshot", payload, headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))

# kaz_image_url =
# kaz_image_name = os.path.basename(kaz_image_url)
# detected_faces = face_client.face.detect_with_url(url=kaz_image_url)

