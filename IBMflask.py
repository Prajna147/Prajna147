import numpy as np
import pandas as pd
from flask import Flask, request, render_template, jsonify
import pickle
import os
import requests
import json

API_KEY = "J9TkeeMtnn5g4DJ9eQOGKLmVcj0NwMk6-TnxAO5h81dC"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
model = pickle.load(open('Visarf.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    
    features_name = ['FULL_TIME_POSITION', 'PREVAILING_WAGE', 'YEAR','SOC_N']
    
  
    payload_scoring = {"input_data": [{"field": [["FULL_TIME_POSITION","PREVAILING_WAGE","YEAR","SOC_N"]],
                                   "values": [[0, 36067.0, 2016.0, 2]]}]}
    
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7936d869-f0bd-44bc-8c1b-cd43273dfbd8/predictions?version=2021-06-02', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    pred=predictions['predictions'][0]['values'][0][0]
    if(pred==0):
     output="CERTIFIED"
     print("CERTIFIED")
    elif(pred==1):
     output="CERTIFIED-WITHDRAWN"
     print("CERTIFIED-WITHDRAWN")
    elif(pred==2):
     output="DENIED"
     print("DENIED")
    elif(pred==3):
     output="WITHDRAWN"
     print("WITHDRAWN")
    elif(pred==4):
     output="PENDING QUALITY AND COMPLIANCE REVIEW - UNASSIGNED"
     print("PENDING QUALITY AND COMPLIANCE REVIEW - UNASSIGNED")    
    elif(pred==5):
     output="REJECTED"
     print("REJECTED")
    else:
     output="INVALIDATED"
     print("INVALIDATED")
    df = pd.DataFrame(features_value, columns=features_name)
    output = model.predict(df)
 
    print(output)

    return render_template('resultVA.html', prediction_text= output)


if __name__ == '__main__':
  
    app.run(debug=True)