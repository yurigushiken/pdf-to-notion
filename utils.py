import os
import logging
import pandas as pd  # Ensure pandas is imported

def ensure_directory_exists(directory_path):
    os.makedirs(directory_path, exist_ok=True)

def read_text_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return ""

def save_text_to_file(text, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        logging.error(f"Error writing to file {file_path}: {e}")

def save_metadata_to_csv(metadata, csv_path):
    df = pd.DataFrame([metadata])
    if not os.path.isfile(csv_path):
        df.to_csv(csv_path, index=False)
    else:
        df.to_csv(csv_path, mode='a', header=False, index=False)

def setup_logging():
    logging.basicConfig(filename='process_log.log', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')
