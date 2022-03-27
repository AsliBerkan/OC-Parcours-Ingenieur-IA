from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from msrest.authentication import CognitiveServicesCredentials
from functools import reduce

import os
import json, time
from dotenv import load_dotenv
load_dotenv()

# Read files 
with open('utterances_train.json', 'r') as outfile:
    utterances_train = json.load(outfile)

# Connection à l'app LUIS
authoringKey = os.environ.get("authoringKey", "")
authoringEndpoint = os.environ.get("authoringEndpoint", "")
    
client = LUISAuthoringClient(authoringEndpoint, CognitiveServicesCredentials(authoringKey))

# Create a LUIS app
default_app_name = "Booking_v2"
version_id = "0.1"

print("Creating App {}, version {}".format(
    default_app_name, version_id))

app_id = client.apps.add({
    'name': default_app_name,
    'initial_version_id': version_id,
    'description': "New App created with LUIS Python sample",
    'culture': 'en-us',
})
print("Created app {}".format(app_id))

# Ajouter un intent, on souhaite que le bot réserve des vols (et uniquement ça pour le moment)
intent_name = "BookFlights"
intent_id = client.model.add_intent(
    app_id,
    version_id,
    intent_name
)
print("{} intent created with id {}".format(
    intent_name,
    intent_id
))

# Add information into the model
print("\nWe'll create five new entities.")
print("The \"Departure\" simple entity will hold the flight departure city.")
print("The \"Destination\" simple entity will hold the flight destination.")
print("The \"StartDate\" simple entity will hold the flight start date.")
print("The \"EndDate\" simple entity will hold the flight end date.")
print("The \"Budget\" simple entity will hold the flight budget.")

entities_list = ["Departure", "Destination", "StartDate", "EndDate", "Budget"]

for enum in entities_list:
    entity_id = client.model.add_entity(app_id, version_id, name=enum)
    print("{} simple entity created with id {}".format(enum, entity_id))

# Ajouter les utterances
for i in range(len(utterances_train)): 
    utterances_result = client.examples.batch(
                app_id,
                version_id,
                [utterances_train[i]]
            )

print("\nUtterances added to the {} intent".format(intent_name))

# Train the app
client.train.train_version(app_id, version_id)
waiting = True
while waiting:
    info = client.train.get_status(app_id, version_id)

    # get_status returns a list of training statuses, one for each model. Loop through them and make sure all are done.
    waiting = any(map(lambda x: 'Queued' == x.details.status or 'InProgress' == x.details.status, info))
    if waiting:
        print ("Waiting 10 seconds for training to complete...")
        time.sleep(10)
    else: 
        print ("trained")
        waiting = False

# Publish the app
print("\nWe'll start publishing your app...")

publish_result = client.apps.publish(
    app_id,
    version_id,
    is_staging=False,
    region='westeurope'
)
endpoint = publish_result.endpoint_url + \
    "?subscription-key=" + authoringKey + "&q="
print("Your app is published. You can now go to test it on\n{}".format(endpoint))