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
    
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": metadata.get('Name', 'Unknown Title')
                        }
                    }
                ]
            },
            "Authors": {
                "rich_text": [
                    {
                        "text": {
                            "content": metadata.get('Authors', 'Unknown Authors')
                        }
                    }
                ]
            },
            "Publication Year": {
                "rich_text": [
                    {
                        "text": {
                            "content": metadata.get('Publication_Year', 'Unknown Year')
                        }
                    }
                ]
            },
            "Tags": {
                "multi_select": [
                    {
                        "name": metadata.get('Tags', 'No Tag')
                    }
                ]
            },
            "PDF Link": {
                "url": metadata.get('PDF_link', 'No PDF Link')
            },
            "Abstract": {
                "rich_text": [
                    {
                        "text": {
                            "content": metadata.get('Abstract', 'No Abstract')
                        }
                    }
                ]
            }
        }
    }
    
    response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=data)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
    return response.json()

def update_notion_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    
    # Print the columns of the DataFrame to verify the column names
    print("Debug: Columns in CSV file:", df.columns.tolist())
    
    for index, row in df.iterrows():
        metadata = {
            "Name": row['Name'],
            "Authors": row['Authors'],
            "Publication_Year": row['Publication_Year'] if pd.notnull(row['Publication_Year']) else 'Unknown Year',
            "Tags": row['Tags'],
            "PDF_link": row.get('PDF_link', 'No PDF Link'),
            "Abstract": row.get('Abstract', 'No Abstract')
        }
        response = create_notion_page(metadata)
        if response.get('id'):
            print(f"Updated Notion for {metadata['Name']} by {metadata['Authors']}")
        else:
            print(f"Failed to update Notion for {metadata['Name']} by {metadata['Authors']}")

if __name__ == "__main__":
    setup_logging()
    csv_path = r"C:\Users\yurig\My Drive\!PDFs\pdf-to-notion\metadata\metadata.csv"
    update_notion_from_csv(csv_path)
