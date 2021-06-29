import gspread
from oauth2client.service_account import ServiceAccountCredentials
import dropbox

# Reading Google spreedshert from cloud.
# use creds to create a client to interact with the Google Drive API
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
creds = ServiceAccountCredentials.from_json_keyfile_name('prodrobox-00d33c384cec.json', scope)
client = gspread.authorize(creds)
# sheet = client.open("email-address")
sheet = client.open("sample")

# Extract and print all of the values
# list_of_hashes = sheet.sheet1.range('B2:')
data = sheet.sheet1.col_values(1)
for val in data:
    if val is not None:
        print(val.strip() + "\n")
        # print(len(val))


#Dropbox 
dbx = dropbox.Dropbox('sl.Azkq32j4xzC0cBCAYd83q5j04-fDLHhIp5KVdAMzXKAEFMM51jZPI-XXEB7qAt_B2yZZUZCYQ2HNTjB-nMeuLOpWCRIOiHXU3W2EbYtLbfwKywcLsQ1dVCmXEqp3o1suAIbiBbw')
usrAccount= dbx.users_get_current_account();
dbx.files_get_preview("/home")
print(usrAccount)
