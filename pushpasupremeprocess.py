import gspread
from oauth2client.service_account import ServiceAccountCredentials
import dropbox
import os
import configparser
from util import *
import gcspreadsheet
from imagestriper import *

# Default configuration
config_file = 'config-dev.ini'
config_details = getConfigProperties(config_file)

# Google spreedshert configuration.
scope = [
    config_details['GCP.SPREEDSHEET'][0]['gcp.scope.spreedsheet'],
    config_details['GCP.SPREEDSHEET'][1]['gcp.scope.drive']
    ]
creds = ServiceAccountCredentials.from_json_keyfile_name(config_details['GCP.SPREEDSHEET'][2]['gcp.key.file'], scope)
client = gspread.authorize(creds)
gsFileName = config_details['GCP.SPREEDSHEET'][3]['gcp.spreedsheet.name']
gs_read_column= config_details['GCP.SPREEDSHEET'][4]['gcp.spreedsheet.read.column']
gs_write_column= config_details['GCP.SPREEDSHEET'][6]['gcp.spreedsheet.write.column']
gs_sheet_id = config_details['GCP.SPREEDSHEET'][5]['gcp.file.id']

# Dropbox Configuration
dbx = dropbox.Dropbox(config_details['DROPBOX'][0]['dbx.token'])
Upload_to_path = f"{config_details['DROPBOX'][1]['dbx.uploadto.path']}"
upload_from_path = config_details['DROPBOX'][2]['dbx.uploadfrom.path']
mdDataObject = []

# Fb config
user_name = config_details['FB'][0]['fb.user.name']
password= config_details['FB'][1]['fb.user.pwd']

def process_google_sheets(cred, scope, spreadsheetId, readColumn, metaData, writeColumn):
    gcspreadsheet.process_gcp_spreadsheet(
        cred, 
        scope,
        spreadsheetId,
        readColumn,
        metaData,
        writeColumn)

#Dropbox 
# Upload files from local folder to dropbox folder 
def process_dbx_assets(DropBox, fromFolder, toFolder):
    print('Uploading files...')
    path = os.listdir(fromFolder)
    for file in path:
        fileToUpload = toFolder + "/" + file
        try:
            f = open(os.path.join(os.path.join(upload_from_path), file) ,'rb')
            DropBox.files_upload(f.read(), fileToUpload, mode=dropbox.files.WriteMode.overwrite)
            mdDataObject.append(read_File(fileToUpload))
        except Exception as e:
            print(e)

def read_File(dbx_file_Name):
    md, file = dbx.files_download(dbx_file_Name)
    link = dbx.sharing_create_shared_link(md.path_display).url
    return update_file_metadata_object(link)

def update_file_metadata_object(file_meta_data):
    metaDataObject = []
    metaDataObject.append(file_meta_data)
    return metaDataObject;

def process_Fb_posts():
    parms = [
        *gcspreadsheet.getValuesFromGCPSheet(creds, gs_sheet_id, gs_read_column),
        user_name,
        password,
        upload_from_path]
    stripImagesFromSource(parms)


def main():
    print('Analayz files...')
    print('Download source assets...')
    process_Fb_posts()
    print('Download source assets complete!')
    print('Upload assets to dropbox...')
    process_dbx_assets(dbx, upload_from_path, Upload_to_path)
    print('Upload assets to dropbox complete!')
    print('Update GCP spreadsheet...')
    process_google_sheets(
        creds, 
        scope,
        gs_sheet_id,
        gs_read_column,
        mdDataObject,
        gs_write_column
    )
    print('Update GCP spreadsheet complete!')

if __name__ == '__main__':
    main()


