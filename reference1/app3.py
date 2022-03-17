
from sfdclib import SfdcSession
from simple_salesforce import Salesforce
from sfdclib import SfdcToolingApi
import json
import csv
import time
import urllib

# Start of the main program

sessionId = '00D5j000001v6Ue!AQUAQG9HthPzNw83Mqh6OTNLpbOt2iqgz8A4RyY3d6JKx0bkrlrm1vLdzGRQvQvEmTQl3PGEM2Yy..QlFSKaYI8Do9K3_Nto'
devInstance = 'mindful-raccoon-e14i2o-dev-ed'

s = SfdcSession(session_id=sessionId,instance=devInstance)
sf = Salesforce(instance_url='https://mindful-raccoon-e14i2o-dev-ed.my.salesforce.com',session_id='00D5j000001v6Ue!AQUAQG9HthPzNw83Mqh6OTNLpbOt2iqgz8A4RyY3d6JKx0bkrlrm1vLdzGRQvQvEmTQl3PGEM2Yy..QlFSKaYI8Do9K3_Nto')

userRecords = sf.query("SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section FROM SetupAuditTrail WHERE CreatedDate=Today")

i = userRecords['records']
#print(i)

data = sf.query_all_iter("SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section FROM SetupAuditTrail WHERE CreatedDate=Today")
for row in data:
   #print(row)
    for key, value in row.items():
        print(key, value)
    print()
   # print(type(row))
   # print(row['attributes'])
    # process(row)
