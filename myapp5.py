from sfdclib import SfdcSession
from simple_salesforce import Salesforce
from sfdclib import SfdcToolingApi
import json
import csv
import time
import urllib
from pivottablejs import pivot_ui
import pandas as pd
from flask import Flask, request, render_template
app = Flask(__name__)

########################
sf = Salesforce(username='abhinav.sivanandhan@mindful-raccoon-e14i2o.com',password='abcde12345', security_token='vGoaEvzwHd2KZThFCFoIBrQDa')
data = sf.query_all_iter("SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section FROM SetupAuditTrail WHERE CreatedDate=THIS_YEAR")
COLUMN_NAMES=['Id','Action','CreatedBy','Display','Delegate User']
df = pd.DataFrame(columns=COLUMN_NAMES)
for row in data:
    print(row)
    for key, value in row.items():
        df[key]=value
print(df)
#pivot_ui(df,outfile_path='pivottablejs.html')
#https://towardsdatascience.com/two-essential-pandas-add-ons-499c1c9b65de
########################
@app.route("/")
def hello_world():
    return render_template("index.html", column_names=df.columns.values, row_data=list(df.values.tolist()),
                           link_column="Id", zip=zip)
    #return HTML('pivottablejs.html')

if __name__ == "__main__":
    app.run(debug=True)