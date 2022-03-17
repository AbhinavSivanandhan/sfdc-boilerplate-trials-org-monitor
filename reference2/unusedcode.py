from sfdclib import SfdcSession
from simple_salesforce import Salesforce
from sfdclib import SfdcToolingApi
import json
import csv
import time
import urllib


def getApexRef():
    apexRecords = tooling.anon_query(
        "SELECT ApiVersion,Id,IsValid,Name FROM ApexClass WHERE NamespacePrefix = null and ((not name like '%Test%') and (not name like '%UT%'))")
    #apexRecords = tooling.anon_query("SELECT ApiVersion,Id,IsValid,Name FROM ApexClass WHERE Id = '01p31000007FWWDAA4'")
    apexClassRecords = apexRecords['records']

    methodRefFile = open('classdetail.csv', 'w', newline='')
    methodWriter = csv.writer(methodRefFile)
    methodWriter.writerow(['Class Name', 'Class Id', 'Num of Reference',
                          'Reference Object Name', 'Refernce Object Type'])

    for apexClass in apexClassRecords:
        classId = apexClass["Id"]
        print("Processing ..", classId)
        className = apexClass["Name"]
        queryResult = tooling.anon_query(
            "SELECT MetadataComponentName, MetadataComponentType FROM MetadataComponentDependency WHERE RefMetadataComponentId ='" + classId + "'")
        refRecords = queryResult['records']
        numOfRef = queryResult['size']

        if numOfRef == 0:
            methodWriter.writerow([className, classId, numOfRef, '', ''])

        for ref in refRecords:
            methodWriter.writerow(
                [className, classId, numOfRef, ref['MetadataComponentName'], ref['MetadataComponentType']])

    methodRefFile.close()


def getUserRef():
    userRecords = tooling.anon_query("SELECT Id,Name,Username FROM User")

    #userRecord = tooling.get('/sobjects/User/005c0000007srbKAAQ?fields=isActive')
    print(userRecords)


def processFieldRef(fieldBatch, fileRef, fieldDict):

    inClause = "'" + "','".join(fieldBatch) + "'"
    queryStr = ('select RefMetadataComponentName, RefMetadataComponentId, RefMetadataComponentType,' +
                'MetadataComponentName,MetadataComponentType,MetadataComponentId' +
                ' FROM MetadataComponentDependency WHERE RefMetadataComponentId IN (XXXX)')
    queryStr = queryStr.replace('XXXX', inClause)
    data = {
        "operation": "query",
        "query": queryStr
    }
    resp = tooling.post('/jobs/query', json.dumps(data))
    jobId = resp['id']
    jobState = resp['state']
    jobResult = ''

    if jobState != 'UploadComplete':
        print("It seems the there was some problem, stopping processing")
        raise SystemExit(0)

    # wait while the job is being processed
    while jobState == 'UploadComplete' or jobState == 'InProgress':
        print("waiting for job to complete currently ", jobState)
        time.sleep(5)
        jobResp = tooling.get('/jobs/query/'+jobId)
        jobState = jobResp['state']
    # end of while

    if jobState == 'JobComplete':
        print("Job Completed getting result")
        jobResult = tooling.get_textBody('/jobs/query/' + jobId + '/results')
        refData = jobResult.split('\n')
        refData = refData[:-1]  # deleting the last empty row
        fieldCollection = []  # this is to hold list for same fields
        curFieldName = ''
        nextFieldName = ''
        tempRefList = []  # this is temp
        fieldRefNum = 0
        # this collection of unique id's for this batch
        processedFieldSet = set([])

        for ref in refData:
            item = ''.join(ref)
            item = item.replace('"', '')
            itemAr = item.split(",")
            processedFieldSet.add(itemAr[1])
            tempRefList.clear()  # make sure everything is clear
            # a fix for unicode values in the layout names
            refCompName = itemAr[3]
            refCompName = refCompName.encode("ascii", "ignore")
            refCompName = refCompName.decode()
            # end of fix
            if not curFieldName and not nextFieldName:
                # set everything up we are just starting
                curFieldName = itemAr[0]
                nextFieldName = itemAr[0]
                fieldRefNum = fieldRefNum + 1
            else:  # this is not first iteration
                # check the current field name first
                curFieldName = itemAr[0]
                # if it is not equal that means all reference to previous field have been processed
                if curFieldName != nextFieldName:
                    # add the num of ref to list and
                    # dump the data we have collected so far into file
                    for field in fieldCollection:
                        field.insert(5, fieldRefNum)
                    # using a copy to make sure no side effects
                    fileRef.writerows(fieldCollection.copy())
                    # reset everything
                    fieldCollection.clear()
                    fieldRefNum = 1
                    nextFieldName = curFieldName
                else:  # another for same field so just increase the count
                    fieldRefNum = fieldRefNum + 1
                # end of if not equal to comparison

                # add to the collection for the field
                tempRefList.insert(
                    0, fieldDict[itemAr[1]]['objectName'])  # object Name
                tempRefList.insert(
                    1, fieldDict[itemAr[1]]['objectId'])  # object Id
                tempRefList.append(itemAr[0] + "__c")  # field name
                tempRefList.append(
                    fieldDict[itemAr[1]]['namespace'])  # field name
                tempRefList.append(itemAr[1])  # field Id
                tempRefList.append(refCompName)  # ref component name
                tempRefList.append(itemAr[4])  # ref type
                tempRefList.append(itemAr[5])  # ref component id
                fieldCollection.append(tempRefList.copy())
                tempRefList.clear()
        # end of for refData
        # last collection would still be there let's dump that also
        if len(fieldCollection):
            for field in fieldCollection:
                field.insert(5, fieldRefNum)
            fileRef.writerows(fieldCollection.copy())
            fieldCollection.clear()
    print(len(processedFieldSet), " unique fields processed ")
    return processedFieldSet
# 3end of function


def getFieldReference():
    customObjectDict = {}
    customObjectRecords = tooling.anon_query(
        "select Id,DeveloperName from CustomObject")

    print(customObjectRecords['size'], " Custom Objects found")
    for customObject in customObjectRecords['records']:
        customObjectDict[customObject["Id"]
                         ] = customObject["DeveloperName"] + "__c"

    methodRefFile = open('fieldDetail.csv', 'w', newline='')
    refWriter = csv.writer(methodRefFile)
    refWriter.writerow(['Object Name', 'Object Id', 'Field Name', 'Namespace',
                       'Field Id', 'Num of Ref', 'Ref Comp Name', 'Ref Type', 'Ref Comp Id'])

    fieldRefFile = open('fieldDictionary.csv', 'w', newline='')
    fieldWriter = csv.writer(fieldRefFile)
    fieldWriter.writerow(
        ['Field Name', 'Field Id', 'Object Name', 'Object Id'])

    customFieldRecords = tooling.anon_query(
        "select Id,DeveloperName,TableEnumOrId,NamespacePrefix from CustomField")
    print(customFieldRecords['size'], " Custom Fields Found")
    nextBatchURL = customFieldRecords['nextRecordsUrl']
    nextBatchURL = nextBatchURL.replace('/services/data/v51.0/tooling', '')
    fieldDictonary = {}
    # these lists will be used for comparison and identify non ref fields
    while nextBatchURL != '':

        if nextBatchURL == 'Last':
            nextBatchURL = ''
            print("Starting processing of ", len(
                customFieldRecords['records']))

        for fieldRec in customFieldRecords['records']:
            fieldDictonary[fieldRec['Id']] = {'objectId': fieldRec['TableEnumOrId'],
                                              'objectName': customObjectDict[fieldRec['TableEnumOrId']] if fieldRec['TableEnumOrId'] in customObjectDict.keys() else fieldRec['TableEnumOrId'],
                                              'fieldName': fieldRec['DeveloperName'] + "__c",
                                              'namespace': fieldRec['NamespacePrefix'] or ''
                                              }

            fieldWriter.writerow([fieldRec['DeveloperName'], fieldRec['Id'],
                                  fieldDictonary[fieldRec['Id']]['objectName'],
                                  fieldDictonary[fieldRec['Id']]['objectId']])
        if nextBatchURL:
            customFieldRecords.clear()
            print("Getting next batch", nextBatchURL)
            customFieldRecords = tooling.get(nextBatchURL)
            print(customFieldRecords)
            print('i am here')
            if 'nextRecordsUrl' in customFieldRecords.keys():
                nextBatchURL = customFieldRecords['nextRecordsUrl']
                nextBatchURL = nextBatchURL.replace(
                    '/services/data/v51.0/tooling', '')
            else:
                print("This is the last batch")
                nextBatchURL = 'Last'
        # end of if nextBatch URL
    # end of while
    fieldRefFile.close()  # we have got the field dictionary
    # this is the complete list of custom field id's
    fieldList = list(fieldDictonary.keys())
    refFieldSet = set([])
    print("Starting processing of ", len(fieldList), 'custom fields')
    # now we need to break it into managable chunks for processing
    batchSize = 2000
    fieldBatchList = [list(fieldList[i:i+batchSize])
                      for i in range(len(fieldList))[::batchSize]]
    print(len(fieldBatchList), "Batches created")
    batchNum = 1
    for fieldBatch in fieldBatchList:
        print("Processing of ", batchNum, " with ", len(fieldBatch), "Started")
        processedSet = processFieldRef(fieldBatch, refWriter, fieldDictonary)
        refFieldSet.update(processedSet)
        print(batchNum, " Processing Complete")
        batchNum = batchNum + 1

    missingFields = list(set(fieldList) - refFieldSet)
    missingFieldList = []
    print("Processing Missing Fields ", len(missingFields))
    for missingField in missingFields:

        missingFieldList.append([fieldDictonary[missingField]['objectName'],
                                 fieldDictonary[missingField]['objectId'],
                                 fieldDictonary[missingField]['fieldName'],
                                 fieldDictonary[missingField]['namespace'],
                                 missingField, 0, '', '', ''
                                 ])
    refWriter.writerows(missingFieldList)


def queryBulkAPI(queryStr):

    jobResult = ''
    data = {
        "operation": "query",
        "query": queryStr
    }
    resp = tooling.post('/jobs/query', json.dumps(data))

    if str(type(resp)) == "<class 'list'>":
        if 'errorCode' in resp[0].keys():
            jobResult = "Query Failed :: " + \
                resp[0]['errorCode'] + " :: " + resp[0]['message']
            return jobResult

    jobId = resp['id']
    jobState = resp['state']
    jobResult = ''

    if jobState != 'UploadComplete':
        print("It seems the there was some problem, stopping processing")
        raise SystemExit(0)

    # wait while the job is being processed
    while jobState == 'UploadComplete' or jobState == 'InProgress':
        print("waiting for job to complete currently ", jobState)
        time.sleep(5)
        jobResp = tooling.get('/jobs/query/'+jobId)
        jobState = jobResp['state']
    # end of while

    if jobState == 'JobComplete':
        print("Job Completed getting result")
        jobResult = tooling.get_textBody('/jobs/query/' + jobId + '/results')

    return jobResult


def queryAllRecords(queryStr):
    consolidatedDict = {}
    nextURL = ''
    queryResult = tooling.anon_query(queryStr)
    if 'nextRecordsUrl' in queryResult.keys():
        nextURL = queryResult['nextRecordsUrl']
        nextURL = nextURL.replace('/services/data/v51.0/tooling', '')
    consolidatedDict.update(queryResult['records'][0])
    while nextURL != '':

        queryResult = tooling.get(nextURL)
        consolidatedDict.update(queryResult['records'][0])
        if 'nextRecordsUrl' in queryResult.keys():
            nextURL = queryResult['nextRecordsUrl']
            nextURL = nextURL.replace('/services/data/v51.0/tooling', '')
        else:
            print("This is the last batch")
            nextURL = ''

    return consolidatedDict


def getCountofRecForField(fieldName, objectName):
    userRecords = sf.query(
        "SELECT Count(" + fieldName + ") FROM " + objectName + "")
    print(userRecords)
    i = userRecords['records']
    return i[0]['expr0']

def getOrgManualChanges():
    #Select+Id,EntityDefinition.MasterLabel+From+ValidationRule+WHERE+Active+=+true
    #SELECT ValidationName, Active, EntityDefinition.DeveloperName FROM ValidationRule WHERE TableEnumOrId='Account'
    userRecords = sf.query(
    "Select Id,Name From User WHERE name like '%abhinav%'")
    print(userRecords)
    i = userRecords['records']
    return i[0]['expr0']


#######################################################################################
#######################################################################################
# Start of the main program
#######################################################################################
#######################################################################################

sessionId = '!AQIAQKIxmMxjbY6N1Yks_bXjtFCDYV7bi74AG9KV80tM5tK5KHvLZ_6dLID0uq3OpCsLStBE4WVYfSN5OZjnWBTrd.KacaSh'
qaInstance = 'stryker--sit2.my'
devInstance = 'stryker--techgov.my'
stage = 'stryker--stage.my'

s = SfdcSession(
    session_id=sessionId,
    instance=devInstance
)
sf = Salesforce(instance='mindful-raccoon-e14i2o-dev-ed.lightning.force.com',
                session_id='!AQUAQG9HthPzNw83Mqh6OTNLpbOt2iqgz8A4RyY3d6JKx0bkrlrm1vLdzGRQvQvEmTQl3PGEM2Yy..QlFSKaYI8Do9K3_Nto')

tooling = SfdcToolingApi(sf)
# queryStr = "select count((Contract_Discount__c)) from Quote_Trending_History__c"
# encodedStr = urllib.parse.urlencode({'q':queryStr})
# encodedStr = "?" + encodedStr
#resp = tooling.query_data("select count(Control_Room_Phone__c) from Account")
# #https://stryker--sit2.my.salesforce.com/services/data/v51.0/tooling/query/?q=select+count%28Contract_Discount__c%29+from+Quote_Trending_History__c
# print(resp)
# print(encodedStr)

#labelQuery = "select name, value, Id, MasterLabel from ExternalString where NamespacePrefix = null"
#queryResult = queryAllRecords(labelQuery)
#queryResult = tooling.anon_query(labelQuery)
# print(queryResult)
# getFieldReference()
# getUserRef()

#print(getCountofRecForField('Mobile_Ph__c', 'PGP_Contact__c'))

print(getOrgManualChanges())