from azure.cognitiveservices.language.luis.authoring.models import ApplicationCreateObject
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from functools import reduce
from sklearn.metrics import accuracy_score

import pandas as pd
import os
import numpy as np
import json, time
from dotenv import load_dotenv
load_dotenv()

# Get the app_id
app_id = '9451fb4a-dae7-49e4-818a-7b5e0f4a6ca4'

# Read files 
with open('utterances_test.json', 'r') as outfile:
    utterances_test = json.load(outfile)

# Authenticate the prediction runtime client
predictionKey = os.environ.get("predictionKey", "")
predictionEndpoint = os.environ.get("predictionEndpoint", "")

runtimeCredentials = CognitiveServicesCredentials(predictionKey)
clientRuntime = LUISRuntimeClient(endpoint=predictionEndpoint, credentials=runtimeCredentials)

# Boucle de prédiction
predictionResponseList = []
for i in range(len(utterances_test)):
    predictionRequest = {"query" : utterances_test[i]['text']}
    predictionResponse = clientRuntime.prediction.get_slot_prediction(app_id, "Production", predictionRequest)
    predictionResponseList.append(predictionResponse.as_dict())

entities_pred = predictionResponseList[0]['prediction']['entities']
for i in entities_pred:
    print(i)
print(predictionResponseList[0]['prediction']['entities']['Departure'][0])

# Sous forme de dataframe
test = pd.read_csv('test.csv')
predictedDf = test.copy()
predictedDf = predictedDf.reset_index(drop=True)
display(predictedDf.head())
print(predictedDf.shape[0])

predictedDf["pred_or_city"] = np.nan
predictedDf["pred_dst_city"] = np.nan
predictedDf["pred_str_date"] = np.nan
predictedDf["pred_end_date"] = np.nan
predictedDf["pred_budget"] = np.nan
for j in predictedDf.index:
    entities_pred = predictionResponseList[j]['prediction']['entities']
    for i in entities_pred:
        if i == 'Departure':
            predictedDf.loc[j, 'pred_or_city'] = entities_pred['Departure'][0]
        if i == 'Destination':
            predictedDf.loc[j, 'pred_dst_city'] = entities_pred['Destination'][0]
        if i == 'StartDate':
            predictedDf.loc[j, 'pred_str_date'] = entities_pred['StartDate'][0]
        if i == 'EndDate':
            predictedDf.loc[j, 'pred_end_date'] = entities_pred['EndDate'][0]
        if i == 'Budget':
            predictedDf.loc[j, 'pred_budget'] = entities_pred['Budget'][0]
predictedDf.head()

predictedDf.isnull().sum()

predictedDf = predictedDf.replace(np.nan, "")
entities_list = ['Origin city', 'Destination city', 'Start date', 'End date', 'Budget']
entities_gt = ['or_city', 'dst_city', 'str_date', 'end_date', 'budget']
entities_pred = ['pred_or_city', 'pred_dst_city', 'pred_str_date', 'pred_end_date', 'pred_budget']

for i in range(len(entities_list)):
    precision = accuracy_score(predictedDf[entities_gt[i]], predictedDf[entities_pred[i]])
    print('Precision for {} is :'.format(entities_list[i]))
    print(precision)

# Save the prediction of Luis model
predictedDf.to_csv('predicted_df.csv', index=False)