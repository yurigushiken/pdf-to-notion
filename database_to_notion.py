import pandas as pd
import requests
from config import NOTION_TOKEN, NOTION_DATABASE_ID
from utils import setup_logging

def create_notion_page(metadata):
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Convert all metadata values to strings to avoid JSON encoding issues
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": str(metadata.get('Name', 'Unknown Title'))
                        }
                    }
                ]
            },
            "Authors": {
                "rich_text": [
                    {
                        "text": {
                            "content": str(metadata.get('Authors', 'Unknown Authors'))
                        }
                    }
                ]
            },
            "Publication Year": {
                "rich_text": [
                    {
                        "text": {
                            "content": str(metadata.get('Publication_Year', 'Unknown Year'))
                        }
                    }
                ]
            },
            "Tags": {
                "multi_select": [
                    {
                        "name": str(metadata.get('Tags', 'No Tag'))
                    }
                ]
            },
            "PDF Link": {
                "url": str(metadata.get('PDF_link', 'No PDF Link'))
            },
            "Abstract": {
                "rich_text": [
                    {
                        "text": {
                            "content": str(metadata.get('Abstract', 'No Abstract'))
                        }
                    }
                ]
            }
        }
    }

    try:
        response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=data)
        response.raise_for_status()  # Raises an error for bad status codes
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return {}

def check_entry_exists(name):
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    query = {
        "filter": {
            "property": "Name",
            "title": {
                "equals": name
            }
        }
    }
    
    response = requests.post(f'https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query', headers=headers, json=query)
    
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            return True
    else:
        print(f"Failed to query Notion database: {response.status_code} - {response.text}")
    return False

def update_notion_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    
    # Print the columns of the DataFrame to verify the column names
    print("Debug: Columns in CSV file:", df.columns.tolist())
    
    # Reverse the DataFrame to process from bottom to top
    for index, row in df.iloc[::-1].iterrows():
        metadata = {
            "Name": str(row['Name']),
            "Authors": str(row['Authors']),
            "Publication_Year": str(row['Publication_Year']) if pd.notnull(row['Publication_Year']) else 'Unknown Year',
            "Tags": str(row['Tags']),
            "PDF_link": str(row.get('PDF_link', 'No PDF Link')),
            "Abstract": str(row.get('Abstract', 'No Abstract'))
        }
        
        # Check if the entry already exists
        if check_entry_exists(metadata['Name']):
            print(f"Entry already exists for {metadata['Name']}, skipping...")
            continue
        
        response = create_notion_page(metadata)
        if response and response.get('id'):
            print(f"Updated Notion for {metadata['Name']} by {metadata['Authors']}")
        else:
            print(f"Failed to update Notion for {metadata['Name']} by {metadata['Authors']}")

if __name__ == "__main__":
    setup_logging()
    csv_path = r"C:\Users\yurig\My Drive\[03] projects\[01] GitHub\pdf-to-notion\metadata\metadata.csv"
    update_notion_from_csv(csv_path)
