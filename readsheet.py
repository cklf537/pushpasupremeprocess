import gspread
from oauth2client.service_account import ServiceAccountCredentials
import dropbox
import os
import configparser

# read configuration
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()

# Reading Google spreedshert from cloud.
# use creds to create a client to interact with the Google Drive API
scope = [
    config['GCP.SPREEDSHEET']['gcp.scope.spreedsheet'],
    config['GCP.SPREEDSHEET']['gcp.scope.drive']
    ]
creds = ServiceAccountCredentials.from_json_keyfile_name(config['GCP.SPREEDSHEET']['gcp.key.file'], scope)
client = gspread.authorize(creds)
gsFileName = config['GCP.SPREEDSHEET']['gcp.spreedsheet.name']
gs_read_column= config['GCP.SPREEDSHEET']['gcp.spreedsheet.column']

def readFrom_googleSheets(file_name):
    # sheet = client.open("email-address")
    sheet = client.open(file_name)
    # Extract and print all of the values
    # list_of_hashes = sheet.sheet1.range('B2:')
    data = sheet.sheet1.col_values(int(gs_read_column))
    for val in data:
        if val is not None:
            print(val.strip() + "\n")
            # print(len(val))


#Dropbox 
dbx = dropbox.Dropbox(config['DROPBOX']['dbx.token'])
Upload_to_path = f"{config['DROPBOX']['dbx.uploadto.path']}"
upload_from_path = config['DROPBOX']['dbx.uploadfrom.path']
mdDataObject = []

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

# Execute methods
readFrom_googleSheets(gsFileName)
# upload_files(dbx, upload_from_path, Upload_to_path)

