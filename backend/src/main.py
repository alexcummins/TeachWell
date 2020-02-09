import http.client
import asyncio
import io
import requests
import json
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
import random

KEY = os.environ["FACE_SUBSCRIPTION_KEY"]
ENDPOINT = os.environ['FACE_ENDPOINT']  # Create an authenticated FaceClient.

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

### TRAINING OF GROUPS

PERSON_GROUP_ID = 'tank-top-high-school-pupil9' + str(random.randint(0,1000000000000000000))

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

print("Getting snapshot from camera:")

url = "https://api.meraki.com/api/v0/networks/L_575897802350005364/cameras/Q2FV-UGQQ-3DF4/snapshot"

payload = "{}"
headers = {
    'Accept': "*/*",
    'Content-Type': "application/json",
    'X-Cisco-Meraki-API-Key': "96850833f85705851d736e34914eea6db9360280",
    'User-Agent': "PostmanRuntime/7.20.1",
    'Cache-Control': "no-cache",
    'Postman-Token': "96ff806f-e342-4f9a-897d-1cda4bcafe46,ad85cf6c-ff31-431e-8420-2e011457af30",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "2",
    'Referer': "https://api.meraki.com/api/v0/networks/L_575897802350005364/cameras/Q2FV-UGQQ-3DF4/snapshot",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)

jsonResponse = json.loads(response.text)
print(jsonResponse['url'])
camera_image_url = jsonResponse['url']

print("Using snapshot in response:")

print(camera_image_url)

# TODO: Need to sleep before we request as it needs to prepare url?
time.sleep(3)

count = 0
while (True):
    count += 1
    if count > 12:
        raise Exception("Couldn't get image response from Meraki camera in time allocated")
    try:
        camera_image_name = os.path.basename(camera_image_url)
        detected_faces = face_client.face.detect_with_url(url=str(camera_image_url))
        break
    except Exception:
        time.sleep(0.5)

face_ids = []
for face in detected_faces:
    face_ids.append(face.face_id)
print("Length: " + str(len(detected_faces)))

# Identify faces
results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
print('Identifying faces in {}'.format("Meraki image from camera"))
if not results:
    print('No person identified in the person group for faces from {}.'.format("Meraki camera image"))
for person in results:
    print('Person for face ID {} candidate {} is identified in {} with a confidence of {}.'.format(person.face_id, person.candidates, "Camera image", person.candidates[0].confidence)) # Get topmost confidence score



# camera_image_name = os.path.basename(camera_image_url)
# detected_faces = face_client.face.detect_with_url(url=str(camera_image_url))
# detected_faces = face_client.face.detect_with_url(url="https://spn2.meraki.com/stream/jpeg/snapshot/e4f394dc9815dd48VHOGUwN2E0YjQyMjRmNDY5ZTNmZjdjY2MwNzRmOWZjYjE3OWZjNjRkOTMyZmQyOGQ3OGZjMjgwYzk2OTA3YmU5N2C98BJIhQbKv0YJTyY1gaF7hzFWv2r-q6w4BFsPwOE6gOfu9j-CtLJOJlBxqc81OGyLK2s_gmKmT781UGBF-Co4qfOwNCNpm_y5FkIY7ua0HFW1BuByTriTi1yL7_W3h2Q1Ceh9232Yd87EyUH46Z4ZA1fq4TFgYgT1Cr_hJUYDCowaRqCY-UYPMPkDxktGpfTIM8J-M40JL8kUEm3urww")



