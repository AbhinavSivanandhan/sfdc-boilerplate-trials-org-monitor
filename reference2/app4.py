from sfdclib import SfdcSession
from simple_salesforce import Salesforce
from sfdclib import SfdcToolingApi
import json
import csv
import time
import urllib
sf = Salesforce(instance_url='https://mindful-raccoon-e14i2o-dev-ed.my.salesforce.com',session_id='00D5j000001v6Ue!AQUAQA_dCetjuHdso.E6sg.syEdvMNdvRVtRpuuaFERW67Fx6iCRZuwIVuGcBO2EcUzrdmkMi0tVx9ClMNz5uYG8ftgrFLAu')
#userRecords = sf.query("SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section FROM SetupAuditTrail WHERE CreatedDate=Today")
#i = userRecords['records']
data = sf.query_all_iter("SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section FROM SetupAuditTrail WHERE CreatedDate=THIS_MONTH")
print(type(data))
for row in data:
    for key, value in row.items():
        print(key, value)
    
