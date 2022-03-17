from flask import Flask
app = Flask(__name__)
########################
from sfdclib import SfdcSession
from simple_salesforce import Salesforce
from sfdclib import SfdcToolingApi
import json
import csv
import time
import urllib
sf = Salesforce(instance_url='https://mindful-raccoon-e14i2o-dev-ed.my.salesforce.com',session_id='00D5j000001v6Ue!AQUAQCEUtTfzPuwz.kalveSxiOmBOZ8WdsNZYLWQlo8V5CCtPWuVcX71qPoV65F94NkotWZYaH9pKWf6m2r34dL7yRBbivA0')
userRecords = sf.query("SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section FROM SetupAuditTrail WHERE CreatedDate=Today")
i = userRecords['records']
data = sf.query_all_iter("SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section FROM SetupAuditTrail WHERE CreatedDate=Today")
print(type(data))
########################
@app.route("/")
def hello_world():
    return "<p>#### {%   %}  ####</p>"

if __name__ == "__main__":
    app.run(debug=True)