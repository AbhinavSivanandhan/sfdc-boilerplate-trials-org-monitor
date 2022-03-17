from sfdclib import SfdcSession
from simple_salesforce import Salesforce
from sfdclib import SfdcToolingApi
import json
import csv
import time
import urllib
import pandas as pd
#sf = Salesforce(instance_url='https://mindful-raccoon-e14i2o-dev-ed.my.salesforce.com',session_id='00D5j000001v6Ue!AQUAQA_dCetjuHdso.E6sg.syEdvMNdvRVtRpuuaFERW67Fx6iCRZuwIVuGcBO2EcUzrdmkMi0tVx9ClMNz5uYG8ftgrFLAu')
sf = Salesforce(username='abhinav.sivanandhan@mindful-raccoon-e14i2o.com',password='abcde12345', security_token='vGoaEvzwHd2KZThFCFoIBrQDa')
data = sf.query_all_iter("SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section FROM SetupAuditTrail WHERE CreatedDate=THIS_MONTH")
print(type(data))
COLUMN_NAMES=['Id','Action','CreatedBy','Display','Delegate User']
df = pd.DataFrame(columns=COLUMN_NAMES)
for row in data:
    for key, value in row.items():
        df[key]=value
print(df)
    
