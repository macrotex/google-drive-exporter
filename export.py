# Adapted from https://developers.google.com/drive/v3/web/quickstart/python

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

DEBUG = True

SCOPES             = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME   = 'Drive API Python Exporter'


# A convenience hash to map from short document type to official
# Google mime-type. See also
# https://developers.google.com/drive/v3/web/mime-types
TYPE_TO_GOOGLE_MIME_TYPE = {
    'audio':        'application/vnd.google-apps.audio',
    'document':     'application/vnd.google-apps.document',
    'drawing':      'application/vnd.google-apps.drawing',
    'file':         'application/vnd.google-apps.file',
    'folder':       'application/vnd.google-apps.folder',
    'form':         'application/vnd.google-apps.form',
    'fusiontable':  'application/vnd.google-apps.fusiontable',
    'map':          'application/vnd.google-apps.map',
    'photo':        'application/vnd.google-apps.photo',
    'presentation': 'application/vnd.google-apps.presentation',
    'script':       'application/vnd.google-apps.script',
    'sites':        'application/vnd.google-apps.sites',
    'spreadsheet':  'application/vnd.google-apps.spreadsheet',
    'unknown':      'application/vnd.google-apps.unknown',
    'video':        'application/vnd.google-apps.video',
}

# https://developers.google.com/drive/v3/web/manage-downloads
DOCUMENT_TYPE_TO_MIME_TYPE = {
    'html':        'text/html',
    'text':        'text/plain',
    'rtf':         'application/rtf',
    'open-office': 'application/vnd.oasis.opendocument.text',
    'pdf':         'application/pdf',
    'ms-word':     'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
}
SPREADSHEET_TYPE_TO_MIME_TYPE = {
    'ms-excel':    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'open-office': 'application/x-vnd.oasis.opendocument.spreadsheet',
    'pdf':         'application/pdf',
    'csv':         'text/csv',
}

TYPE_TO_EXPORTS = {
    'spreadsheet': SPREADSHEET_TYPE_TO_MIME_TYPE,
    'document':    DOCUMENT_TYPE_TO_MIME_TYPE,
}

# Create a file with the given contents
def spew(contents, filename):
    with open(filename,'w') as f:
        f.write(contents)

def get_credentials():
    """Gets valid user credentials from storage.

    Returns:
    Credentials, the obtained credential.
    """

    scopes      = [SCOPES]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET_FILE, scopes=scopes)
    http_auth   = credentials.authorize(Http())

    return http_auth

def progress(msg):
    if (DEBUG):
        print('progress: ' + msg)

# Normalize a filename (replace spaces with underscores, etc.)
def normalize_filename(name):
    # Squish multiple spaces to a single space
    normalized = re.sub(r"\s+", ' ', name)

    # Replace spaces with underscores
    normalized =  re.sub(r"\s", '_', normalized)

    return normalized

def process_current(service, results, filter_google_mimetype, export_mimetype):
    items = results.get('files', [])
    for item in items:
        name           = item['name']
        id             = item['id']
        google_mimetype = item['mimeType']

        if (google_mimetype == filter_google_mimetype):
            progress('exporting \'{0}\'({1}): mimetype: {2}'.format(name, id, google_mimetype))
            results_of_export = service.files().export(fileId=id, mimeType=export_mimetype).execute()
            normalized_filename = normalize_filename(name)
            spew(results_of_export, normalized_filename)
            progress('exported to file {0}'.format(normalized_filename))


def main():
    """Shows basic usage of the Google Drive API.
    Creates a Google Drive API service object and outputs the names and
    IDs for up to 10 files.
    """
    http_auth = get_credentials()
    service = discovery.build('drive', 'v3', http=http_auth)

    type        = 'spreadsheet'
    export_type = 'ms-excel'

    filter_google_mimetype = TYPE_TO_GOOGLE_MIME_TYPE[type]
    progress("filtering on type " + type + " (" + filter_google_mimetype + ")")

    export_mimetype = TYPE_TO_EXPORTS[type][export_type]
    progress("exporting to type " + export_type + " (" + export_mimetype + ")")

    first_pass = True
    nextPageToken = None
    while (first_pass or nextPageToken):
        results = service.files().list(pageSize=10,
                                       pageToken=nextPageToken,
                                       fields="nextPageToken, kind, files(id, name, mimeType)").execute()
        nextPageToken = results.get('nextPageToken')
        process_current(service, results, filter_google_mimetype, export_mimetype)
        first_pass = False

    progress('Finished')

if __name__ == '__main__':
    main()
