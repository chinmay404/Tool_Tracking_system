import uuid
import qrcode
import csv
import os
import zipfile
import shutil

# Function to generate QR code for an ID and save it to a file
def generate_qr_code(url, id, output_dir):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    filename = os.path.join(output_dir, f"qr_code_{id}.png")
    img.save(filename)

    print(f"Generated QR code for URL: {url} and saved as {filename}")

def main():
    csv_filename = input("Enter the CSV filename: ")
    choice = input('')

    temp_dir = "temp_qr_codes"
    os.makedirs(temp_dir, exist_ok=True)

    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Read and discard the header row
        for row in csv_reader:
            if row:  
                id = row[0]
                url = f'http://192.168.1.6:8000/api/get/product/{id}'
                # else:
                #     url= f'http://192.168.60.63:8000/api/activate/product/{id}'
                generate_qr_code(url, id, temp_dir)

    zip_filename = "csv_filename.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, temp_dir))

    # Use shutil.rmtree to remove the directory and its contents
    shutil.rmtree(temp_dir)

    print(f"Generated QR codes have been zipped as {zip_filename}")

if __name__ == "__main__":
    main()
