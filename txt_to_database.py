import os
import pandas as pd
from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, NOTION_TOKEN, NOTION_DATABASE_ID
from utils import read_text_from_file, save_metadata_to_csv, setup_logging, ensure_directory_exists

class MetadataExtractor:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)

    def extract_metadata(self, text):
        messages = [
            {
                "role": "user",
                "content": (
                    f"Extract the following metadata from the provided academic text:\n\n{text[:2000]}"
                    "\n\nName (this means title of the PDF excluding author), Authors, Publication Year, Tags, PDF Link, Abstract\n\nExample Output:\n"
                    "Name: The Impact of Social Media on Academic Performance\n"
                    "Authors: John Doe, Jane Smith\nPublication Year: 2021\n"
                    "Tags: Social Media\n"
                    "PDF Link: https://example.com\n"
                    "Abstract: This study explores the impact of social media on the academic performance of university students."
                )
            }
        ]

        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=800,
                messages=messages
            )
            
            # Print the response object to understand its structure
            print("Debug: Full response object from Claude:\n", response)
            
            # Correctly accessing the response content
            response_content = response.content[0].text
            print("Debug: Full response text from Claude:\n", response_content)  # Debugging information
            lines = response_content.split('\n')
            
            metadata = {
                "Name": "Unknown Name",
                "Authors": "Unknown Authors",
                "Publication_Year": "Unknown Year",
                "Tags": "Unknown Tag",
                "PDF_link": "Unknown PDF Link",
                "Abstract": "Unknown Abstract"
            }
            
            for line in lines:
                if 'name:' in line.lower():
                    metadata["Name"] = line.split(':', 1)[1].strip()
                elif 'authors:' in line.lower():
                    metadata["Authors"] = line.split(':', 1)[1].strip()
                elif 'publication year:' in line.lower():
                    metadata["Publication_Year"] = line.split(':', 1)[1].strip()
                elif 'tags:' in line.lower():
                    metadata["Tags"] = line.split(':', 1)[1].strip()
                elif 'pdf link:' in line.lower():
                    metadata["PDF_link"] = line.split(':', 1)[1].strip()
                elif 'abstract:' in line.lower():
                    metadata["Abstract"] = line.split(':', 1)[1].strip()
            
            return metadata
        except Exception as e:
            print(f"An error occurred: {e}")
            return {
                "Name": "Error",
                "Authors": "Error",
                "Publication_Year": "Error",
                "Tags": "Error",
                "PDF_link": "Error",
                "Abstract": "Error"
            }

def process_text_files(input_directory, csv_path):
    extractor = MetadataExtractor(api_key=ANTHROPIC_API_KEY)
    
    ensure_directory_exists(os.path.dirname(csv_path))
    
    for root, dirs, files in os.walk(input_directory):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                text = read_text_from_file(file_path)
                
                print(f"Debugging: Text content from {filename}:", text[:500])  # Print first 500 characters
                
                metadata = extractor.extract_metadata(text)
                save_metadata_to_csv(metadata, csv_path)
                
                print(f"Processed {filename}")

if __name__ == "__main__":
    setup_logging()
    input_directory = r"C:\Users\yurig\My Drive\!PDFs\pdf-to-notion\txt"
    csv_path = r"C:\Users\yurig\My Drive\!PDFs\pdf-to-notion\metadata\metadata.csv"
    
    if not os.path.exists(input_directory):
        print(f"Error: Input directory {input_directory} does not exist")
    else:
        process_text_files(input_directory, csv_path)

