import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "J9TkeeMtnn5g4DJ9eQOGKLmVcj0NwMk6-TnxAO5h81dC"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": [["FULL_TIME_POSITION","PREVAILING_WAGE","YEAR","SOC_N"]],
                                   "values": [[0, 36067.0, 2016.0, 2]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7936d869-f0bd-44bc-8c1b-cd43273dfbd8/predictions?version=2021-06-02', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
predictions = response_scoring.json()
print(predictions)
