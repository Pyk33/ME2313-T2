from ftplib import FTP
import os
import zipfile

# FTP server details
ftp_host = "ftp.cmegroup.com"
ftp_directory = "/sdr"

# Local directory to save .csv and .zip files
local_directory = os.path.expanduser("~/Desktop/Trioptima/Raw data")

# Function to download files from FTP server recursively
def download_files_from_ftp(ftp, ftp_directory, local_directory):
    try:
        ftp.cwd(ftp_directory)
        files = ftp.nlst()
        for file_name in files:
            remote_file_path = ftp_directory + '/' + file_name
            local_file_path = os.path.join(local_directory, file_name)
            if (file_name.lower().endswith('.csv')):
                with open(local_file_path, 'wb') as local_file:
                    ftp.retrbinary(f"RETR {remote_file_path}", local_file.write)
                print(f"Downloaded .csv file: {file_name}")
            elif (file_name.lower().endswith('.zip')):
                with open(local_file_path, 'wb') as local_file:
                    ftp.retrbinary(f"RETR {remote_file_path}", local_file.write)
                print(f"Downloaded .zip file: {file_name}")
                # Extract .zip file
                with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
                    zip_ref.extractall(local_directory)
                print(f"Extracted .zip file: {file_name}")
                # Delete the original .zip file
                os.remove(local_file_path)
                print(f"Deleted .zip file: {file_name}")
            elif '.' not in file_name:
                download_files_from_ftp(ftp, remote_file_path, local_directory)
    except Exception as e:
        print(f"Failed to download files: {e}")

# Create local directory if it doesn't exist
os.makedirs(local_directory, exist_ok=True)

# Connect to FTP server and start downloading files
try:
    with FTP(ftp_host) as ftp:
        ftp.login()  # Log in anonymously
        download_files_from_ftp(ftp, ftp_directory, local_directory)
except Exception as e:
    print(f"Failed to connect to FTP server: {e}")
