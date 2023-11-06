import os
import pandas as pd
import requests

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
    excel_file_path = r'X:\Operations\Clay_VM_Bear\Data\PIMIDs and text URLs.xlsx'
    images_folder = r'X:\Operations\Clay_VM_Bear\Data\images'

    open_and_save_images(excel_file_path, images_folder)

if __name__ == "__main__":
    main()
