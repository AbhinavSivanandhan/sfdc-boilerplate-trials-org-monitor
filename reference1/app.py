from simple_salesforce import Salesforce
sf = Salesforce(instance='https://login.salesforce.com/', session_id='!AQUAQG9HthPzNw83Mqh6OTNLpbOt2iqgz8A4RyY3d6JKx0bkrlrm1vLdzGRQvQvEmTQl3PGEM2Yy..QlFSKaYI8Do9K3_Nto')
sf.query("SELECT Id, Email FROM Contact WHERE LastName like '%a%' limit 1")