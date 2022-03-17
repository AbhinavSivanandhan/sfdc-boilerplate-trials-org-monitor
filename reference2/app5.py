from sfdclib import SfdcSession
from simple_salesforce import Salesforce
from sfdclib import SfdcToolingApi
import json
import csv
import time
import urllib
import pandas as pd
sf = Salesforce(instance_url='https://mindful-raccoon-e14i2o-dev-ed.my.salesforce.com',session_id='00D5j000001v6Ue!AQUAQA_dCetjuHdso.E6sg.syEdvMNdvRVtRpuuaFERW67Fx6iCRZuwIVuGcBO2EcUzrdmkMi0tVx9ClMNz5uYG8ftgrFLAu')
data = sf.query("SELECT Id, Action, CreatedBy.Name, CreatedDate, Display, Section FROM SetupAuditTrail WHERE CreatedDate=THIS_MONTH")
df_table = pd.DataFrame(data)
print(df_table.head())
