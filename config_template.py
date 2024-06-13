import os

# API keys and tokens
ANTHROPIC_API_KEY = "your_anthropic_api_key"
NOTION_TOKEN = "your_notion_token"
NOTION_DATABASE_ID = "your_notion_database_id"

# Google Drive API credentials and folder ID
SERVICE_ACCOUNT_FILE = r'path_to_your_credentials_file.json'
GOOGLE_DRIVE_FOLDER_ID = 'your_google_drive_folder_id'

if not ANTHROPIC_API_KEY or not NOTION_TOKEN:
    raise ValueError("API keys not found in environment variables. Please set them before running the script.")

if not SERVICE_ACCOUNT_FILE or not GOOGLE_DRIVE_FOLDER_ID:
    raise ValueError("Google Drive credentials or folder ID not found. Please set them before running the script.")

