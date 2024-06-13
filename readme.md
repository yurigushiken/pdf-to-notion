# PDF to Notion

This project automates the process of extracting text from PDFs, converting the text into a structured format, and uploading the data to a Notion database. It uses the Claude Haiku language model to organize data such as the title, URL, authors, publication year, tags, and abstract, replacing the manual work of metadata entry. The project integrates with Google Drive for PDF storage and retrieval and requires API credentials for both Google Drive and Notion.

## Workflow:
- put PDFs in Google Drive dir on PC
- run pdf_to_txt.py to create language model-ready .txt versions of PDFs
- run txt_to_database.py to get Claude 3 to read first 1200 tokens of .txt file and write to metadata.csv
- run database_to_notion.py to upload meetadata.csv contents to Notion
## Screenshots:
- Start Here: PDFs in a Google Drive-linked directory
![Screenshot](./screenshots/Screenshot%202024-06-12%20221932.png)

- Next: .txt files created as preparation for language processing  
![Screenshot](./screenshots/Screenshot%202024-06-12%20221947.png)

- The Result: Formatted line entry - compare to the original file names! (some errors due to: missing data/language processing/text formatting). 
- Please note the direct link to your file in Google Drive - highly convenient access!
![Screenshot](./screenshots/Screenshot%202024-06-12%20222101.png)

## Example use cases:
- All PDF entries in notion
![Screenshot](./screenshots/Screenshot%202024-06-12%20224412.png)

- example use case: filters for specific tags (example: filter for specific class)
![Screenshot](./screenshots/Screenshot%202024-06-11%20123601.png)

- Example entry
![Screenshot](./screenshots/Screenshot%202024-06-11%20123639.png)



## Prerequisites

Before you start, you will need:

- **Google Drive API credentials**: Create new project and service acccount with editor priveliges. Download your credentials JSON file from the Google Cloud Console.
- **Google Drive folder sharing**: Share your target PDF folder with your Google service account email address.
- **Notion integration**: Create a new integration with Notion. Obtain your Notion API token and Notion database ID.
- **Notion Page Connections**: Connect your Notion page to your new integration (wtihin Notion page menu).
- **Claude Haiku API key**: Add your Claude Haiku API key.

## Setup Instructions

### Step 1: Clone the Repository

Clone the repository to your local machine:

    git clone https://github.com/your-username/pdf-to-notion.git
    cd pdf-to-notion

### Step 2: Create and Activate a Virtual Environment

Create a virtual environment to manage your project dependencies:

    python -m venv pdf-to-notion-env
    source pdf-to-notion-env/bin/activate # On Windows use: pdf-to-notion-env\Scripts\activate

### Step 3: Install Dependencies

Install the required Python packages:

    pip install fitz pytesseract google-auth google-api-python-client anthropic

### Step 4: Configure the Project

Rename config_template.py to config.py:

    mv config_template.py config.py

Fill in your API keys and other necessary information in config.py.

- **Google Drive API credentials**: Place your credentials JSON file in the credentials directory.
- **Notion API token**: Add your Notion API token and Notion database ID to config.py.
- **Claude Haiku API key**: Add your Claude Haiku API key to config.py.

### Step 5: Set Up Your Notion Database

Create a new database in Notion with the following properties:

- Name (title)
- Authors (rich_text)
- Publication Year (rich_text)
- Tags (multi_select)
- PDF Link (url)
- Abstract (rich_text)

## Usage

### Convert PDFs to Text

Run the `pdf_to_txt.py` script to extract text from your PDFs and save them as .txt files:

    python pdf_to_txt.py

**Detailed Steps:**
- Sets up Google Drive API credentials and initializes the Google Drive service.
- Lists files in a specified Google Drive folder.
- Extracts text from each PDF file (using OCR if necessary).
- Adds metadata (title, Google Drive URL, and tag) to the extracted text. This creates conditions favorable for the language model in the next step (`txt_to_database.py`)
- Saves the extracted text and metadata to a corresponding text file in the output directory.

### Extract Metadata from Text Files and Save to CSV

Run the `txt_to_database.py` script to extract metadata from the text files and save it to a CSV file:

    python txt_to_database.py

**Detailed Steps:**
- Initializes the connection to the Claude Haiku API.
- Prompt to Claude Haiku: The script sends a prompt to Claude Haiku that includes a snippet of the text (default 1200 tokens - about 1 page - you can adjust for more context) and asks it to extract metadata in a Name,Authors,Publication_Year,Tags,PDF_link,Abstract format.
- Walks through the specified input directory and processes each text file.
- Extracts metadata such as Name, Authors, Publication Year, Tags, PDF Link, and Abstract from the text from first 1200 tokens.
- Saves the extracted metadata to a CSV file.

### Upload Metadata to Notion

Run the `database_to_notion.py` script to upload the metadata from the CSV file to your Notion database:

    python database_to_notion.py

**Detailed Steps:**
- Sets up headers for Notion API requests.
- Defines functions to create a new Notion page and check if an entry already exists in the Notion database.
- Reads the CSV file containing metadata.
- For each row in the CSV, extracts metadata and checks if an entry with the same name already exists in the Notion database.
- Creates a new page in Notion if no matching entry is found; otherwise, updates the existing entry if there are changes.

## Additional Notes

Ensure your Google Drive and Notion API credentials are correctly set up in the config.py file.
Share your Google Drive folder with the service account email from your Google API credentials.
This setup helps streamline the process of managing PDF metadata and integrating it seamlessly with Notion, making it an efficient tool for organizing and accessing your documents.
