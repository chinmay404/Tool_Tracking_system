import uuid
import qrcode
import csv
import os
import zipfile
import shutil




def generate_qr_code(url, id, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # filename = os.path.join(output_dir, f"{filename}.png")
    filename = f"{filename}.png"
    img.save(filename)

    print(f"Generated QR code for URL: {url} and saved as {filename}")
    
    
def main():
    inp_id = input('uuid Id : ')
    inp_id = inp_id.replace(' ', '')
    url = f'http://192.168.1.6:8000/api/get/product/{inp_id}'
    generate_qr_code(url,inp_id,filename='view')

    
    
    
if __name__ == "__main__":
    main()
