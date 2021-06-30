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
        print('Name, Major:')
        if len(dbxobject) > 0:
            for key, row in enumerate(values):
                util.stripAndCompareFBAndDBXId(dbxobject, row[0])
                # Print columns A and E, which correspond to indices 0 and 4.
                print(row)