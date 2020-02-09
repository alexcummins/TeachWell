import json
import glob
import os
import sys
import time
import uuid
from twisted.internet import task, reactor
import requests
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, \
    OperationStatusType
from msrest.authentication import CognitiveServicesCredentials
import random
import threading

f = open("../../react-canvasjs-chart-samples/public/summaryData.json", "w")
f.write("")

def get_engagement(agg):
    engagement = 0
    for e in agg:
        switcher = {
            'anger': 0,
            'contempt': 0,
            'disgust': 0,
            'fear': 0,
            'happiness': agg["happiness"] * 0.25,
            'neutral': agg["neutral"],
            'sadness': 0,
            'surprise': agg["surprise"]
        }
        engagement += switcher.get(e)
    return engagement


snapshots = []
starttime = time.time()

def get_snapshot():
    with open("../../react-canvasjs-chart-samples/public/data.json", "r") as dataf:
        data2 = list(dataf)

    with open("../../react-canvasjs-chart-samples/public/summaryData.json", "r") as f:
        data = list(f)

    threading.Timer(10, get_snapshot).start()
    s = {}
    s["x"] = time.time() - starttime
    e = get_engagement(detectandidentifyfaces())
    s["y"] = str(int(e * 100))

    eng = {}

    eng["e"] = str(int(e * 100))
    eng["ne"] = str(int((1 - e) * 100))

    temp = str(eng).replace(",", ",\n")

    temp2 = temp.replace("'", '"')

    if (len(data2) == 0):
        data2.append(temp2)
    else:
        data2[0] = temp2




    if(len(data) == 0):
        data.append("[ \n")
        data.append("\t\t {}".format(s))
    else:
        data[0] = "[ \n"
        data[len(data) - 2] = data[len(data) - 2] + ","
        data[len(data) - 1] = "\t\t {}".format(s)

    data.append("\n]")

    for i in range(len(data)):
        data[i] = data[i].replace("'", '"')

    with open("../../react-canvasjs-chart-samples/public/summaryData.json", "w") as f:
        f.writelines(data)

    with open("../../react-canvasjs-chart-samples/public/data.json", "w") as dataf:
        dataf.writelines(data2)



def getMainEmotion(emot):
    emotion = {'anger': emot.anger, 'contempt': emot.contempt, 'disgust': emot.disgust, 'fear': emot.fear,
               'happiness': emot.happiness, 'neutral': emot.neutral, 'sadness': emot.sadness, 'surprise': emot.surprise}

    max_emotion = 0

    for e in emotion:
        if emotion[e] > max_emotion:
            max_emotion = emotion[e]

    for e in emotion:
        if emotion[e] == max_emotion:
            return e

    return 'ERROR'


def aggEmotion(emotion, agg):
    aggNew = {}
    for e in agg:
        switcher = {
            'anger': emotion.anger,
            'contempt': emotion.contempt,
            'disgust': emotion.disgust,
            'fear': emotion.fear,
            'happiness': emotion.happiness,
            'neutral': emotion.neutral,
            'sadness': emotion.sadness,
            'surprise': emotion.surprise
        }
        aggNew[e] = float(agg[e]) + float(switcher.get(e, 0))
    return aggNew


KEY = os.environ["FACE_SUBSCRIPTION_KEY"]
ENDPOINT = os.environ['FACE_ENDPOINT']  # Create an authenticated FaceClient.

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

### TRAINING OF GROUPS

PERSON_GROUP_ID = 'tank-top-high-school' + str(random.randint(0, 100000000000))

# Used for the Snapshot and Delete Person Group examples.
TARGET_PERSON_GROUP_ID = str(uuid.uuid4())  # assign a random ID (or name it anything)

'''
Create the PersonGroup
'''
# Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
print('Person group:', PERSON_GROUP_ID)
# TODO: THis shouldn't need commenting out hmm
face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)
# face_client.person_group.get('tank-top-high-school')

# Define woman friend
kaz = face_client.person_group_person.create(PERSON_GROUP_ID, "kaz")
# Define man friend
alex = face_client.person_group_person.create(PERSON_GROUP_ID, "alex")
# Define child friend
adele = face_client.person_group_person.create(PERSON_GROUP_ID, "adele")
john = face_client.person_group_person.create(PERSON_GROUP_ID, "john")

'''
Detect faces and register to correct person
'''
# Find all jpeg images of friends in working directory
# kaz_images = [file for file in glob.glob('src/resource/*') if file.startswith("kaz")]
# alex_images = [file for file in glob.glob('resource/*') if file.startswith("alex")]
# adele_images = [file for file in glob.glob('resource/*') if file.startswith("adele")]


kaz_images = [file for file in glob.glob('resource/kaz*.jpeg')]
alex_images = [file for file in glob.glob('resource/alex*.jpeg')]
adele_images = [file for file in glob.glob('resource/adele*.jpeg')]
john_images = [file for file in glob.glob('resource/john*.jpeg')]
# adele_images.append(file for file in glob.glob('resource/adele1.jpeg'))

print(len(kaz_images))

iddict = {}

# Add to a woman person
for image in kaz_images:
    w = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, kaz.person_id, w)
    print("KAZ ID: " + str(kaz.person_id))

iddict[str(kaz.person_id)] = "Kaz"

# Add to a man person
for image in alex_images:
    m = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, alex.person_id, m)
    print("ALEX ID: " + str(alex.person_id))

iddict[str(alex.person_id)] = "Alex"

# Add to a child person
for image in adele_images:
    ch = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, adele.person_id, ch)
    print("ADELE ID: " + str(adele.person_id))

iddict[str(adele.person_id)] = "Adele"

# Add to a child person
for image in john_images:
    ch = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, john.person_id, ch)
    print("ADELE ID: " + str(john.person_id))

iddict[str(john.person_id)] = "John"

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

def detectandidentifyfaces():
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
    time.sleep(7)
    # count = 0
    # while (True):
    #     count += 1
    #     if count > 20:
    #         raise Exception("Couldn't get image response from Meraki camera in time allocated")
    #     try:
    #         camera_image_name = os.path.basename(camera_image_url)
    #         detected_faces = face_client.face.detect_with_url(url=str(camera_image_url), return_face_attributes='emotion')
    #         break
    #     except Exception:
    #         time.sleep(0.5)
    camera_image_name = os.path.basename(camera_image_url)
    detected_faces = face_client.face.detect_with_url(url=str(camera_image_url), return_face_attributes=['emotion'])
    face_ids = []
    face_id_map = {}
    print("printing face ids from detect")
    for face in detected_faces:
        print(face)
        face_ids.append(face.face_id)
        face_id_map[face.face_id] = face
    print("Length: " + str(len(detected_faces)))
    if len(detected_faces) == 0:
        print("NO FACES DETECTED")
        exit(1)
    # Identify faces
    results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
    # results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
    print('Identifying faces in {}'.format("Meraki image from camera"))
    if not results:
        print('No person identified in the person group for faces from {}.'.format("Meraki camera image"))
    # First one is what we just got second one is from trained model
    for person in results:
        if len(person.candidates) == 0:
            print("Unregistered face detected")
            results.remove(person)
        else:
            print(
                'Person for face ID {} candidate {} is identified in {} with a confidence of {}.'.format(person.face_id,
                                                                                                         iddict[str(
                                                                                                             person.candidates[
                                                                                                                 0].person_id)],
                                                                                                         "Camera image",
                                                                                                         person.candidates[
                                                                                                             0].confidence))  # Get topmost confidence score
    print(len(results))
    emotion_map = {}

    engagement_score = 0

    emotion_agg = {'anger': 0, 'contempt': 0, 'disgust': 0, 'fear': 0,
                   'happiness': 0, 'neutral': 0, 'sadness': 0, 'surprise': 0}

    for person in results:
        face_id = face_id_map[person.face_id]
        emotions = face_id.face_attributes.emotion
        # emotions_json = json.loads(str(face_id.face_attributes.emotion))
        emotion_map[str(face_id)] = emotions
        emotion_agg = aggEmotion(emotions, emotion_agg)
        print("Person {} has emotion {} {}".format(iddict[person.candidates[0].person_id], getMainEmotion(emotions), emotions))

    for e in emotion_agg:
        emotion_agg[e] = emotion_agg[e] / len(results)

    print("AGG {} ".format(emotion_agg))

    return emotion_agg


get_snapshot()




# camera_image_name = os.path.basename(camera_image_url)
# detected_faces = face_client.face.detect_with_url(url=str(camera_image_url))
# detected_faces = face_client.face.detect_with_url(url="https://spn2.meraki.com/stream/jpeg/snapshot/e4f394dc9815dd48VHOGUwN2E0YjQyMjRmNDY5ZTNmZjdjY2MwNzRmOWZjYjE3OWZjNjRkOTMyZmQyOGQ3OGZjMjgwYzk2OTA3YmU5N2C98BJIhQbKv0YJTyY1gaF7hzFWv2r-q6w4BFsPwOE6gOfu9j-CtLJOJlBxqc81OGyLK2s_gmKmT781UGBF-Co4qfOwNCNpm_y5FkIY7ua0HFW1BuByTriTi1yL7_W3h2Q1Ceh9232Yd87EyUH46Z4ZA1fq4TFgYgT1Cr_hJUYDCowaRqCY-UYPMPkDxktGpfTIM8J-M40JL8kUEm3urww")
