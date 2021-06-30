from os import RTLD_NOW
from googleapiclient.discovery import build
import util

def process_gcp_spreadsheet(token, scope, sheetId, rangeName, dbxobject=[]):
    creds = token
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        if len(dbxobject) > 0:
             dbxAssetIds = util.stripDbxObjectId(dbxobject)
             for key, row in enumerate(values):
                gsEntry = util.stripAndCompareFBAndDBXId(dbxAssetIds, row[0])
                if gsEntry is not None:
                    values = [[gsEntry],]
                    body = {'values': values}
                    sheet.values().update(
                        spreadsheetId=sheetId, 
                        range='D'+str(key+1)+':'+'D'+str(key+1), 
                        valueInputOption="RAW", 
                        body=body).execute()