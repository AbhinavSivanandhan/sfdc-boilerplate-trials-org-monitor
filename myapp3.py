from flask import Flask
from sfdclib import SfdcSession
from simple_salesforce import Salesforce
from sfdclib import SfdcToolingApi
import json
import csv
import time
import urllib
from pivottablejs import pivot_ui
app = Flask(__name__)
########################
sf = Salesforce(username='abhinav.sivanandhan@mindful-raccoon-e14i2o.com',password='abcde12345', security_token='vGoaEvzwHd2KZThFCFoIBrQDa')
data = sf.query_all_iter("SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section FROM SetupAuditTrail WHERE CreatedDate=THIS_MONTH")
COLUMN_NAMES=['Id','Action','CreatedBy','Display','Delegate User']
df = pd.DataFrame(columns=COLUMN_NAMES)
for row in data:
    for key, value in row.items():
        df[key]=value
print(df)
pivot_ui(df,outfile_path=’pivottablejs.html’)
HTML(‘pivottablejs.html’)
########################
@app.route("/")
def hello_world():
    return "<p>#### {%   %}  ####</p>"

if __name__ == "__main__":
    app.run(debug=True)