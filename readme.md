PDF to Notion
This project automates the process of extracting text from PDFs, converting the text into a structured format, and uploading the data to a Notion database. It leverages the Claude Haiku language model to organize data such as the title, URL, authors, publication year, tags, and abstract, replacing the manual work of metadata entry.

Directory Structure
scss
Copy code
pdf-to-notion/
├── .gitignore
├── README.md
├── config_template.py
├── config.py (ignored)
├── credentials/
│   └── pdf-to-notion-cf92c3eb37ee.json (ignored)
├── database_to_notion.py
├── ignore folder/ (ignored)
├── metadata/
│   ├── metadata.csv (ignored)
│   └── example_metadata.csv
├── PDFs/
│   └── *.pdf (ignored)
├── pdf_to_txt.py
├── process_log.log (ignored)
├── txt/
│   └── *.txt (ignored)
├── txt_to_database.py
└── utils.py
Setup Instructions
1. Clone the Repository:
sh
Copy code
git clone https://github.com/your-username/pdf-to-notion.git
cd pdf-to-notion
2. Create and Activate a Virtual Environment:
sh
Copy code
python -m venv pdf-to-notion-env
source pdf-to-notion-env/bin/activate  # On Windows use: pdf-to-notion-env\Scripts\activate
3. Install Dependencies:
sh
Copy code
pip install -r requirements.txt
4. Configure the Project:
Rename config_template.py to config.py.
Fill in your API keys and other necessary information in config.py.
5. Set Up Your Notion Database:
Create a new database in Notion with the following properties:

Name (title)
Authors (rich_text)
Publication Year (rich_text)
Tags (multi_select)
PDF Link (url)
Abstract (rich_text)
Usage
1. Convert PDFs to Text:
Run the pdf_to_txt.py script to extract text from your PDFs and save them as .txt files:

sh
Copy code
python pdf_to_txt.py
2. Extract Metadata from Text Files and Save to CSV:
Run the txt_to_database.py script to extract metadata from the text files and save it to a CSV file:

sh
Copy code
python txt_to_database.py
3. Upload Metadata to Notion:
Run the database_to_notion.py script to upload the metadata from the CSV file to your Notion database:

sh
Copy code
python database_to_notion.py
.gitignore
The .gitignore file is set up to ignore sensitive and large files:

bash
Copy code
# Ignore the credentials directory
credentials/

# Ignore the ignore folder directory
ignore folder/

# Ignore metadata.csv but keep example_metadata.csv
metadata/metadata.csv

# Ignore all PDFs and text files but keep the directories
PDFs/*
!PDFs/.gitkeep
txt/*
!txt/.gitkeep

# Ignore the process_log.log file
process_log.log

# Ignore the config.py file
config.py
Make sure to include an example metadata.csv in the metadata directory for users to reference.

Notes
Ensure your Google Drive and Notion API credentials are correctly set up in the config.py file.
Share your Google Drive folder with the service account email from your Google API credentials.
This project aims to streamline the process of managing and organizing PDF documents, making it easier to keep track of important information and access it efficiently.






