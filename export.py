# https://developers.google.com/drive/v3/web/quickstart/python

from __future__ import print_function
import httplib2
import os
import re
import pprint

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

# Create a file with the given contents
def spew(contents, filename):
    with open(filename,'w') as f:
        f.write(contents)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
    Credentials, the obtained credential.
    """

    #store = oauth2client.file.Storage('hello.txt')
    #flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    #flow.user_agent = APPLICATION_NAME
    #credentials = tools.run_flow(flow, store)

    scopes      = [SCOPES]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET_FILE, scopes=scopes)
    http_auth   = credentials.authorize(Http())

    return http_auth

# Remove spaces form a string
def normalize_filename(name):
    # Squish multiple spaces to a single space
    normalized = re.sub(r"\s+", ' ', name)

    # Replace spaces with underscores
    normalized =  re.sub(r"\s", '_', normalized)

    return normalized

def process_current(service, results):
    items = results.get('files', [])
    for item in items:
        name           = item['name']
        id             = item['id']
        googleMimeType = item['mimeType']

        driveType = 'vnd.google-apps.spreadsheet'

        # This one is supposed to be MS Excel compatible
        mimeType  = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        # OpenOffice compatible
        mimeType  = 'application/x-vnd.oasis.opendocument.spreadsheet'

        #mimeType  = 'text/csv'

        match = re.search(re.escape(driveType), googleMimeType)
        if (match):
            print('{0}/{2} ({1})'.format(name, id, googleMimeType))
            resultsOfExport = service.files().export(fileId=id, mimeType=mimeType).execute()
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(resultsOfExport)
            spew(resultsOfExport, normalize_filename(name))

def main():
    """Shows basic usage of the Google Drive API.
    Creates a Google Drive API service object and outputs the names and
    IDs for up to 10 files.
    """
    http_auth = get_credentials()
    service = discovery.build('drive', 'v3', http=http_auth)

    first_pass = True
    nextPageToken = None
    while (first_pass or nextPageToken):
        results = service.files().list(pageSize=10,
                                       pageToken=nextPageToken,
                                       fields="nextPageToken, kind, files(id, name, mimeType)").execute()
        nextPageToken = results.get('nextPageToken')
        process_current(service, results)
        first_pass = False


if __name__ == '__main__':
    main()
