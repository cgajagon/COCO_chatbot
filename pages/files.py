import streamlit as st

import streamlit as st
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


folder_id = st.secrets.gcs.folder_id
file = "./service_account.json"


def get_drive_service():
    # Create credentials using the service account file
    creds = service_account.Credentials.from_service_account_file(
        file,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    # Build the Drive API service
    service = build("drive", "v3", credentials=creds)
    return service


def list_files_in_folder(service, folder_id):
    """
    Returns a list of files (dict with 'id' and 'name') contained in the given folder.
    """
    files = []
    page_token = None
    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces="drive",
            fields="nextPageToken, files(id, name)",
            pageToken=page_token
        ).execute()
        for file in response.get("files", []):
            files.append(file)
        page_token = response.get("nextPageToken", None)
        if page_token is None:
            break
    return files


def download_file_from_drive(service, file_id):
    """
    Downloads file content (in bytes) from Google Drive by file_id.
    """
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh.read()


# Initialize the Drive API client
drive_service = get_drive_service()

# Set the page title and icon
st.title("Document Browser")
st.info("Explore the key files used to train and enhance our chatbot’s performance. Each file type contributes to delivering accurate and relevant responses:")
st.divider()

# List all files from the specified Google Drive folder
with st.spinner("Loading files..."):
    try:
        files = list_files_in_folder(drive_service, folder_id)
    except Exception as e:
        st.error(f"An error occurred while listing files: {e}")

    if not files:
        st.info("No files found in this Google Drive folder.")

    for file in files:
        file_name = file["name"]
        st.write(file_name)
        st.divider()
