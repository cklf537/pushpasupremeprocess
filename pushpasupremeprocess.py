import gspread
from oauth2client.service_account import ServiceAccountCredentials
import dropbox
import os
import configparser
from util import *
import gcspreadsheet

# read configuration
config_file = 'config-dev.ini'
config_details = getConfigProperties(config_file)
dbx = dropbox.Dropbox(config_details['DROPBOX'][0]['dbx.token'])
Upload_to_path = f"{config_details['DROPBOX'][1]['dbx.uploadto.path']}"
upload_from_path = config_details['DROPBOX'][2]['dbx.uploadfrom.path']
mdDataObject = []

# Reading Google spreedshert from cloud.
# use creds to create a client to interact with the Google Drive API
scope = [
    config_details['GCP.SPREEDSHEET'][0]['gcp.scope.spreedsheet'],
    config_details['GCP.SPREEDSHEET'][1]['gcp.scope.drive']
    ]
creds = ServiceAccountCredentials.from_json_keyfile_name(config_details['GCP.SPREEDSHEET'][2]['gcp.key.file'], scope)
client = gspread.authorize(creds)
gsFileName = config_details['GCP.SPREEDSHEET'][3]['gcp.spreedsheet.name']
gs_read_column= config_details['GCP.SPREEDSHEET'][4]['gcp.spreedsheet.column']

def readFrom_googleSheets():
    gcspreadsheet.process_gcp_spreadsheet(
        creds, 
        scope,
        config_details['GCP.SPREEDSHEET'][5]['gcp.file.id'],
        config_details['GCP.SPREEDSHEET'][4]['gcp.spreedsheet.column'])
    # # sheet = client.open("email-address")
    # sheet = client.open(file_name)
    # # Extract and print all of the values
    # # list_of_hashes = sheet.sheet1.range('B2:')
    # data = sheet.sheet1.col_values(int(gs_read_column))
    # print(sheet.worksheets())
    # sheet.sheet1.update('E2', "Hello World");
    # print(sheet.worksheet())
    # for val in data:
    #     if val is not None:
    #         print(val.strip() + "\n")
    #         # print(len(val))


#Dropbox 
# Upload files from local folder to dropbox folder 
def upload_files(DropBox, fromFolder, toFolder):
    path = os.listdir(fromFolder)
    for file in path:
        fileToUpload = toFolder + "/" + file
        try:
            f = open(os.path.join(os.path.join(upload_from_path), file) ,'rb')
            DropBox.files_upload(f.read(), fileToUpload, mode=dropbox.files.WriteMode.overwrite)
            mdDataObject = read_File(fileToUpload)
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

def main():
    upload_files(dbx, upload_from_path, Upload_to_path)
    readFrom_googleSheets()

if __name__ == '__main__':
    main()


