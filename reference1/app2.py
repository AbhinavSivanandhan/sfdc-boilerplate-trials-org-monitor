from sfdclib import SfdcSession
from simple_salesforce import Salesforce
from sfdclib import SfdcToolingApi
import json
import csv
import time
import urllib

def getCountofRecForField(fieldName, objectName):
    userRecords = sf.query(
        "SELECT Count(" + fieldName + ") FROM " + objectName + "")
    print(userRecords)
    i = userRecords['records']
    return i[0]['expr0']

def getOrgManualChanges():
    #Select+Id,EntityDefinition.MasterLabel+From+ValidationRule+WHERE+Active+=+true
    #SELECT ValidationName, Active, EntityDefinition.DeveloperName FROM ValidationRule WHERE TableEnumOrId='Account'
    userRecords = sf.query("SELECT ValidationName, Active, EntityDefinition.DeveloperName FROM ValidationRule")
    print(userRecords)
    i = userRecords['records']
    return i[0]['expr0']

# Start of the main program

sessionId = '00D5j000001v6Ue!AQUAQG9HthPzNw83Mqh6OTNLpbOt2iqgz8A4RyY3d6JKx0bkrlrm1vLdzGRQvQvEmTQl3PGEM2Yy..QlFSKaYI8Do9K3_Nto'
devInstance = 'mindful-raccoon-e14i2o-dev-ed'

s = SfdcSession(session_id=sessionId,instance=devInstance)
sf = Salesforce(instance_url='https://mindful-raccoon-e14i2o-dev-ed.my.salesforce.com',session_id='00D5j000001v6Ue!AQUAQG9HthPzNw83Mqh6OTNLpbOt2iqgz8A4RyY3d6JKx0bkrlrm1vLdzGRQvQvEmTQl3PGEM2Yy..QlFSKaYI8Do9K3_Nto')

#tooling = SfdcToolingApi(s)
#print(getOrgManualChanges())
userRecords = sf.query("SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section FROM SetupAuditTrail WHERE CreatedDate=Today")
#print(userRecords)
i = userRecords['records']
print(i)

#print(i[0]['expr0'])
#print(len(i))