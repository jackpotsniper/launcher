import os
import json
import zipfile
import requests
import shutil
import subprocess
from pathlib import Path

# Configuration
WORKDIR_DIR = str(Path.home().joinpath(".jackpot-sniper"))
EXTENSION_DIR = os.path.join(WORKDIR_DIR, "extension")
USER_DATA_DIR = os.path.join(WORKDIR_DIR, "chrome_user_data")
GITHUB_API_RELEASES = f"https://api.github.com/repos/jackpotsniper/extension/releases/latest"

# Chrome possible locations for Windows
CHROME_LOCATIONS = [
    os.path.expandvars("%ProgramFiles%\\Google\\Chrome\\Application\\chrome.exe"),
    os.path.expandvars("%ProgramFiles(x86)%\\Google\\Chrome\\Application\\chrome.exe"),
    os.path.expandvars("%LocalAppData%\\Google\\Chrome\\Application\\chrome.exe"),
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
]

def find_chrome():
    """Find Chrome executable on Windows."""
    for path in CHROME_LOCATIONS:
        if os.path.exists(path):
            return path
    
    # Linux or Mac
    whichCmdResult = subprocess.run(['which', 'chrome'], capture_output=True, text=True)
    chromePath = repr(whichCmdResult.stdout).replace('\'', '').replace('\\n', '')

    if chromePath != "":
        return "chrome"

    whichCmdResult = subprocess.run(['which', 'google-chrome'], capture_output=True, text=True)
    chromePath = repr(whichCmdResult.stdout).replace('\'', '').replace('\\n', '')

    if chromePath != "":
        return "google-chrome"

    return ""

def get_local_version():
    """Read the version from the local manifest.json file."""
    manifest_path = os.path.join(EXTENSION_DIR, "manifest.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        return manifest.get("version", "0.0")
    return "0.0"

def get_latest_version():
    """Fetch the latest version from GitHub releases."""
    try:
        response = requests.get(GITHUB_API_RELEASES, timeout=10)
        response.raise_for_status()
        release_data = response.json()
        return release_data["tag_name"][1:], release_data["assets"][0]["browser_download_url"]  # Tag + ZIP URL
    except requests.RequestException as e:
        print(f"Failed to fetch latest GitHub release: {e}")
        return "0.0.0", None

def download_and_extract_extension(zip_url):
    """Download and extract the latest extension version from GitHub."""
    try:
        response = requests.get(zip_url, stream=True, timeout=10)
        response.raise_for_status()
        zip_path = os.path.join(WORKDIR_DIR, "extension.zip")

        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Extract and overwrite
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            if os.path.exists(EXTENSION_DIR):
                shutil.rmtree(EXTENSION_DIR)
            zip_ref.extractall(EXTENSION_DIR)

        os.remove(zip_path)
        print("Extension updated successfully.")
    except requests.RequestException as e:
        print(f"Failed to download extension: {e}")

def start_chrome():
    """Launch Chrome with the unpacked extension and user-data directory."""
    chrome_path = find_chrome()
    if chrome_path:
        subprocess.Popen([
            chrome_path,
            f"--load-extension={EXTENSION_DIR}",
            f"--user-data-dir={USER_DATA_DIR}"
        ])
    else:
        print("Chrome not found. Please install Chrome and try again.")

# Main Execution
if __name__ == "__main__":
    if not os.path.exists(WORKDIR_DIR):
        os.makedirs(WORKDIR_DIR)

    local_version = get_local_version()
    latest_version, zip_url = get_latest_version()

    if not zip_url:
        raise Exception("Extension download url not provided from github api")

    if not os.path.exists(EXTENSION_DIR):
        print("Downloading latest extension...")
        download_and_extract_extension(zip_url)
    else: 
        if local_version != latest_version:
            print("Updating extension " + local_version + " >> " + latest_version)
            download_and_extract_extension(zip_url)

    print("Starting Chrome...")
    start_chrome()
