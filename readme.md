# PDF to Notion

This project automates the process of extracting text from PDFs, converting the text into a structured format, and uploading the data to a Notion database. It leverages the Claude Haiku language model to organize data such as the title, URL, authors, publication year, tags, and abstract, replacing the manual work of metadata entry. The project integrates with Google Drive for PDF storage and retrieval and requires API credentials for both Google Drive and Notion.

## Directory Structure

pdf-to-notion/
├── .gitignore
├── README.md
├── config_template.py
├── config.py (ignored)
├── credentials/
│ └── pdf-to-notion-cf92c3eb37ee.json (ignored)
├── database_to_notion.py
├── ignore folder/ (ignored)
├── metadata/
│ ├── metadata.csv (ignored)
│ └── example_metadata.csv
├── PDFs/
│ └── README.md (indicating this is where the PDFs should go)
├── pdf_to_txt.py
├── process_log.log (ignored)
├── txt/
│ └── README.md (indicating this is where the text files should go)
├── txt_to_database.py
└── utils.py

markdown
Copy code

## Prerequisites

1. **Python**: Make sure you have Python installed on your system.
2. **Notion Account**: You need a Notion account and a Notion database.
3. **Google Drive API Credentials**: Set up Google Drive API and obtain the credentials JSON file.
4. **Claude Haiku API**: You need an API key for the Claude Haiku language model.

## Setup Instructions

### Step 1: Clone the Repository

Clone the repository to your local machine:

```sh
git clone https://github.com/your-username/pdf-to-notion.git
cd pdf-to-notion
Step 2: Create and Activate a Virtual Environment
Create a virtual environment to manage your project dependencies:

sh
Copy code
python -m venv pdf-to-notion-env
source pdf-to-notion-env/bin/activate  # On Windows use: pdf-to-notion-env\Scripts\activate
Step 3: Install Dependencies
Install the required Python packages:

sh
Copy code
pip install -r requirements.txt
Step 4: Configure the Project
Rename config_template.py to config.py:

sh
Copy code
mv config_template.py config.py
Fill in your API keys and other necessary information in config.py:

Google Drive API credentials: Download your credentials JSON file from Google Cloud Console and place it in the credentials directory.
Notion API token: Obtain your Notion API token and Notion database ID and add them to config.py.
Claude Haiku API key: Add your Claude Haiku API key to config.py.
Step 5: Set Up Your Notion Database
Create a new database in Notion with the following properties:

Name (title)
Authors (rich_text)
Publication Year (rich_text)
Tags (multi_select)
PDF Link (url)
Abstract (rich_text)
Usage
Convert PDFs to Text
Run the pdf_to_txt.py script to extract text from your PDFs and save them as .txt files:

sh
Copy code
python pdf_to_txt.py
Extract Metadata from Text Files and Save to CSV
Run the txt_to_database.py script to extract metadata from the text files and save it to a CSV file:

sh
Copy code
python txt_to_database.py
Upload Metadata to Notion
Run the database_to_notion.py script to upload the metadata from the CSV file to your Notion database:

sh
Copy code
python database_to_notion.py
Additional Notes
Ensure your Google Drive and Notion API credentials are correctly set up in the config.py file.
Share your Google Drive folder with the service account email from your Google API credentials.
This setup helps streamline the process of managing PDF metadata and integrating it seamlessly with Notion, making it an efficient tool for organizing and accessing your documents.