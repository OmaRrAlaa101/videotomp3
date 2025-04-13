import urllib.request
import os
import zipfile
import shutil

def download_ffmpeg():
    print("Downloading FFmpeg...")
    url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n6.1-latest-win64-gpl-6.1.zip"
    zip_path = "ffmpeg.zip"
    
    # Download the file
    urllib.request.urlretrieve(url, zip_path)
    print("Download complete!")
    
    # Create ffmpeg directory if it doesn't exist
    os.makedirs("C:\\ffmpeg\\bin", exist_ok=True)
    
    # Extract the zip file
    print("Extracting files...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("ffmpeg_temp")
    
    # Move the files to the correct location
    bin_dir = None
    for root, dirs, files in os.walk("ffmpeg_temp"):
        if "bin" in dirs:
            bin_dir = os.path.join(root, "bin")
            break
    
    if bin_dir:
        for file in os.listdir(bin_dir):
            src = os.path.join(bin_dir, file)
            dst = os.path.join("C:\\ffmpeg\\bin", file)
            shutil.copy2(src, dst)
    
    # Clean up
    os.remove(zip_path)
    shutil.rmtree("ffmpeg_temp")
    print("FFmpeg installation complete!")
    print("FFmpeg has been installed to C:\\ffmpeg\\bin")

if __name__ == "__main__":
    download_ffmpeg() 