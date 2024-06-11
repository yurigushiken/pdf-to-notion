PDF to Notion
This project automates the process of extracting text from PDFs, converting the text into a structured format, and uploading the data to a Notion database.

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
Clone the repository:

sh
Copy code
git clone https://github.com/your-username/pdf-to-notion.git
cd pdf-to-notion
Create and activate a virtual environment:

sh
Copy code
python -m venv pdf-to-notion-env
source pdf-to-notion-env/bin/activate   # On Windows use: pdf-to-notion-env\Scripts\activate
Install dependencies:

sh
Copy code
pip install -r requirements.txt
Configure the project:

Rename config_template.py to config.py.
Fill in your API keys and other necessary information in config.py.
Set up your Notion database:

Create a new database in Notion with the following properties:
Name (title)
Authors (rich_text)
Publication Year (rich_text)
Tags (multi_select)
PDF Link (url)
Abstract (rich_text)
Usage
Convert PDFs to text:

Run the pdf_to_txt.py script to extract text from your PDFs and save them as .txt files:

sh
Copy code
python pdf_to_txt.py
Extract metadata from text files and save to CSV:

Run the txt_to_database.py script to extract metadata from the text files and save it to a CSV file:

sh
Copy code
python txt_to_database.py
Upload metadata to Notion:

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

# Ignore all PDFs and text files
PDFs/
txt/

# Ignore the process_log.log file
process_log.log

# Ignore the config.py file
config.py
Make sure to include an example metadata.csv in the metadata directory for users to reference.

Notes
Ensure your Google Drive and Notion API credentials are correctly set up in the config.py file.
Share your Google Drive folder with the service account email from your Google API credentials.
This should help you get started with the project and provide clear instructions for others who want to use it.