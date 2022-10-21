# google-drive-exporter
Python script to export files from Google Drive

# Examples of use:

    export.py
      (export all files in their default formats)

    export.py --type spreadsheet
      (export all spreadsheets in the default format)

    export.py --type spreadsheet --export-formats spreadsheet:csv
      (export all spreadsheets in the csv format)

    export.py --export-formats spreadsheet:pdf,document:rtf
      (export all files with their default export formats except
       spreadsheets to be exported to pdf and documents to be
       exported to rtf)

    export.py --destination-dir /tmp/google-files
      (export all files in their default formats but put them in the
       directory /tmp/google-files)

This script uses service account credentials to access your Google Docs
and download them.

# CAVEATS

1. The script can only download documents that the service account has
permission to download.

# How to create a service account

1. Go to the [Google Developer's
Console](https://console.developers.google.com/).

1. Log in with your usual Google credentials.

1. Click on the "Credentials" link.

1. Click on the "Create Credentials" pull-down and choose "Service account
key".

1. On the "Service account" pull-down choose "New service account".

1. For "Key type" choose JSON.

1. Click the "Create" button.

1. Be sure to save the JSON secret file. This is what you will use to
access your files. The script looks for this secret in the file
`client_secret.json`.

1. To download a Google Drive file your must grant view permission on that file
to this e-mail address.

# Libraries required:
* oauth2client
* google-api-python-client

They can be installed by using:
`pip install google-api-python-client oauth2client`

