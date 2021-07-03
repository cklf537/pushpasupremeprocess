from os import RTLD_NOW
from googleapiclient.discovery import build
import util

def process_gcp_spreadsheet(token, scope, sheetId, readRange, dbxobject=[], writeRange='D:D'):
    values = getValuesFromGCPSheet(token, sheetId, readRange)
    if not values[0]:
        print('No data found.')
    else:
        if len(dbxobject) > 0:
             dbxAssetIds = util.stripDbxObjectId(dbxobject)
             for key, row in enumerate(values[0]):
                gsEntry = util.stripAndCompareFBAndDBXId(dbxAssetIds, row[0])
                if gsEntry is not None:
                    value = [[gsEntry],]
                    body = {'values': value}
                    values[1].values().update(
                        spreadsheetId=sheetId, 
                        # range='D'+str(key+1)+':'+'D'+str(key+1), 
                        range=writeRange+str(key+1)+':'+writeRange+str(key+1), 
                        valueInputOption="RAW", 
                        body=body).execute()
                else:
                    pass

def getValuesFromGCPSheet(token, sheetId, readRange):
    service = build('sheets', 'v4', credentials=token)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheetId, range=readRange).execute()
    values = result.get('values', [])
    return [values, sheet]