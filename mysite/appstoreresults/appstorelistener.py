#VAR NAMES MUST BE CHANGED

from googleapiclient.discovery import build
from google.oauth2 import service_account
import sqlite3

# Replace with your API key file name and database file name
API_KEY_FILE = 'api_key.json'
DB_FILE = 'mydatabase.db'

# Connect to the database
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# Authenticate the API client using your API key
creds = service_account.Credentials.from_service_account_file(API_KEY_FILE)
service = build('androidpublisher', 'v3', credentials=creds)

# Query the API for each app in your database
c.execute("SELECT package_name, version_number FROM apps")
for row in c.fetchall():
    package_name = row[0]
    current_version = row[1]
    app = service.edits().get(packageName=package_name, editId='latest').execute()
    latest_version = app['track']['releases'][0]['versionCodes'][0]
    if current_version != latest_version:
        print(f"{package_name} is outdated! Current version: {current_version}, latest version: {latest_version}")
        # Flag the app as outdated or update its version number in the database
