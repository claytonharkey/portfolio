# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 16:04:51 2023

@author: Clayton.Harkey
"""

import os
import pandas as pd
import requests
import csv
from PIL import Image
import pytesseract

#START EXTRACTION OF IMAGES FROM URLS

def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        else:
            print(f"Failed to download image from URL: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")

def open_and_save_images(excel_file_path, images_folder):
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    try:
        df = pd.read_excel(excel_file_path)  # Assuming the URLs are in the second column of the Excel file

        for index, row in df.iterrows():
            image_url = row[1]
            if image_url.lower().endswith('.jpg'):
                image_filename = os.path.basename(image_url)
                save_path = os.path.join(images_folder, image_filename)
                download_image(image_url, save_path)

    except FileNotFoundError:
        print("Excel file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    excel_file_path = r'C:\Users\Clayton.Harkey\Data\PIMIDs and text URLs.xlsx'
    images_folder = r'C:\Users\Clayton.Harkey\Data\imageTest'

    open_and_save_images(excel_file_path, images_folder)

if __name__ == "__main__":
    main()

#START OCR MODEL
def extract_words_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return ""

def process_images_in_folder(folder_path, output_csv_file):
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Image", "Extracted Text"])

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_path = os.path.join(folder_path, filename)
                extracted_text = extract_words_from_image(image_path)
                writer.writerow([filename, extracted_text])

if __name__ == "__main__":
    folder_path = r"C:\Users\Clayton.Harkey\Data\imageTest"  
    output_csv_file = r"C:\Users\Clayton.Harkey\Data\outputTest.csv"  

    process_images_in_folder(folder_path, output_csv_file)
    print("Extraction complete. CSV file created.")
