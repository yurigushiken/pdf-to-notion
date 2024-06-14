import os
import time
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils import ensure_directory_exists, save_text_to_file, setup_logging
from config import SERVICE_ACCOUNT_FILE, GOOGLE_DRIVE_FOLDER_ID

# Set the Tesseract command path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define the scope of the service
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)
        print("Google Drive service initialized successfully.")
        return service
    except Exception as e:
        print(f"Failed to create Google Drive service: {e}")
        return None

def list_files_in_folder(service, folder_id, max_retries=5):
    query = f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder'"
    file_list = []
    page_token = None
    for attempt in range(max_retries):
        try:
            while True:
                results = service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType, parents)", pageToken=page_token).execute()
                items = results.get("files", [])
                file_list.extend(items)
                page_token = results.get("nextPageToken", None)
                if page_token is None:
                    break
            # Recursively list files in subfolders
            folder_query = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
            folders = service.files().list(q=folder_query, fields="nextPageToken, files(id, name)").execute().get("files", [])
            for folder in folders:
                print(f"Entering folder: {folder['name']} (ID: {folder['id']})")
                file_list.extend(list_files_in_folder(service, folder["id"], max_retries))
            return file_list
        except HttpError as error:
            print(f"An error occurred: {error}")
            time.sleep(2 ** attempt)  # Exponential backoff
    return file_list

def find_file_id(service, file_name):
    print("Debug: Listing all files in the folder")
    file_list = list_files_in_folder(service, GOOGLE_DRIVE_FOLDER_ID)
    print(f"Debug: Total files found: {len(file_list)}")
    for file in file_list:
        print(f"Checking file: {file['name']} with ID: {file['id']}")
        if file["name"] == file_name:
            print(f"Found file: {file_name} with ID: {file['id']}")
            return file["id"]
    print(f"No file found with the name: {file_name}")
    return None

def generate_shareable_link(service, file_id, max_retries=5):
    for attempt in range(max_retries):
        try:
            permission = {"type": "anyone", "role": "reader"}
            service.permissions().create(fileId=file_id, body=permission, fields="id").execute()
            file = service.files().get(fileId=file_id, fields="webViewLink").execute()
            print(f"Generated shareable link: {file['webViewLink']} for file ID: {file_id}")
            return file["webViewLink"]
        except HttpError as error:
            print(f"An error occurred while generating shareable link: {error}")
            time.sleep(2 ** attempt)  # Exponential backoff
    return None

def get_google_drive_url(file_path):
    service = get_drive_service()
    if not service:
        return "Failed to initialize Google Drive service"

    file_name = os.path.basename(file_path)
    print(f"Searching for file: {file_name} in Google Drive folder ID: {GOOGLE_DRIVE_FOLDER_ID}")
    
    file_id = find_file_id(service, file_name)
    if file_id:
        return generate_shareable_link(service, file_id)
    return "URL not found"

def extract_text_from_pdf(file_path):
    try:
        with fitz.open(file_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""

def ocr_page(page):
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return pytesseract.image_to_string(img)

def extract_text_with_ocr(file_path):
    text = extract_text_from_pdf(file_path)
    if not text.strip():
        try:
            with fitz.open(file_path) as doc:
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    text += ocr_page(page)
        except Exception as e:
            print(f"Error performing OCR on {file_path}: {e}")
    return text

def process_pdfs(input_directory, output_directory):
    for root, dirs, files in os.walk(input_directory):
        for filename in files:
            if filename.endswith('.pdf'):
                file_path = os.path.join(root, filename)
                
                # Create the corresponding output directory
                relative_path = os.path.relpath(root, input_directory)
                output_dir = os.path.join(output_directory, relative_path)
                ensure_directory_exists(output_dir)
                
                output_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
                
                # Debug: Print paths and check if output file exists
                print(f"Processing {filename}")
                print(f"Output file path: {output_file_path}")
                
                # Skip processing if the text file already exists
                if os.path.exists(output_file_path):
                    print(f"Skipped {filename} (already processed)")
                    continue
                
                text = extract_text_with_ocr(file_path)
                
                # Add the title (filename), Google Drive URL, and tag at the beginning of the text
                title = os.path.splitext(filename)[0]
                google_drive_url = get_google_drive_url(file_path)
                tag = os.path.basename(root)  # Use the folder name as the tag
                text = f"{title}\n\n{google_drive_url}\n\nTag: {tag}\n\n{text}"
                
                save_text_to_file(text, output_file_path)
                print(f"Processed {filename} and saved to {output_file_path}")

if __name__ == "__main__":
    setup_logging()
    input_directory = r"C:\Users\yurig\My Drive\[03] projects\[01] GitHub\pdf-to-notion\PDFs"
    output_directory = r"C:\Users\yurig\My Drive\[03] projects\[01] GitHub\pdf-to-notion\txt"
    process_pdfs(input_directory, output_directory)