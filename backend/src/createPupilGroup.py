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

from backend.src.main import face_client

#
# kaz_image_url = 'data:image/jpeg;base64,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'
# kaz_image_name = os.path.basename(kaz_image_url)
# detected_faces = face_client.face.detect_with_url(url=kaz_image_url)
# kaz_face_ID = detected_faces[0].face_id
#
# alex_image_url = 'https://media-exp1.licdn.com/dms/image/C4E03AQHoWqfdfZHpAQ/profile-displayphoto-shrink_200_200/0?e=1586995200&v=beta&t=RAjGxW0iXzs6atbCDaW5LyoWnhBS8PogTXi3zlblTY8'
# alex_image_name = os.path.basename(kaz_image_url)
# detected_faces = face_client.face.detect_with_url(url=alex_image_url)
# alex_face_ID = detected_faces[0].face_id
#
# terence_image_url = 'https://media-exp1.licdn.com/dms/image/C5603AQFkAa_4aT6n_g/profile-displayphoto-shrink_200_200/0?e=1586995200&v=beta&t=FWXb2GOgCekYREpnrbqI97zc5HdLsPkMQ8pcaUYw1UQ'
# terence_image_name = os.path.basename(kaz_image_url)
# detected_faces = face_client.face.detect_with_url(url=terence_image_url)
# terence_face_ID = detected_faces[0].face_id
#
# adele_image_url = 'https://media-exp1.licdn.com/dms/image/C4D03AQEC1SmPM_JcCQ/profile-displayphoto-shrink_200_200/0?e=1586995200&v=beta&t=9nTo3xP-37CQtftC2wdCxXfKuM-2lqNUzu5Dkkqfosc'
# adele_image_name = os.path.basename(kaz_image_url)
# detected_faces = face_client.face.detect_with_url(url=adele_image_url)
# adele_face_ID = detected_faces[0].face_id
#
# if not detected_faces:
#     raise Exception('No face detected from image {}'.format(adele_image_url))
#
# faces = [kaz_face_ID, alex_face_ID, terence_face_ID, adele_face_ID]

# Used in the Person Group Operations,  Snapshot Operations, and Delete Person Group examples.
# You can call list_person_groups to print a list of preexisting PersonGroups.
# SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
# PERSON_GROUP_ID = 'Tank Top High School Pupils'
#
# # Used for the Snapshot and Delete Person Group examples.
# TARGET_PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)
#
# '''
# Create the PersonGroup
# '''
# # Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
# print('Person group:', PERSON_GROUP_ID)
# face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)
#
# # Define woman friend
# kaz = face_client.person_group_person.create(PERSON_GROUP_ID, "kaz")
# # Define man friend
# alex = face_client.person_group_person.create(PERSON_GROUP_ID, "alex")
# # Define child friend
# adele = face_client.person_group_person.create(PERSON_GROUP_ID, "adele")
#
# '''
# Detect faces and register to correct person
# '''
# # Find all jpeg images of friends in working directory
# kaz_images = [file for file in glob.glob('*.jpg') if file.startswith("kaz")]
# alex_images = [file for file in glob.glob('*.jpg') if file.startswith("alex")]
# adele_images = [file for file in glob.glob('*.jpg') if file.startswith("adele")]
#
# # Add to a woman person
# for image in kaz_images:
#     w = open(image, 'r+b')
#     face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, kaz.person_id, w)
#
# # Add to a man person
# for image in alex_images:
#     m = open(image, 'r+b')
#     face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, alex.person_id, m)
#
# # Add to a child person
# for image in adele_images:
#     ch = open(image, 'r+b')
#     face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, adele.person_id, ch)
#
# '''
# Train PersonGroup
# '''
# print()
# print('Training the person group...')
# # Train the person group
# face_client.person_group.train(PERSON_GROUP_ID)
#
# while (True):
#     training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
#     print("Training status: {}.".format(training_status.status))
#     print()
#     if (training_status.status is TrainingStatusType.succeeded):
#         break
#     elif (training_status.status is TrainingStatusType.failed):
#         sys.exit('Training the person group has failed.')
#     time.sleep(5)