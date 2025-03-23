#!/bin/bash

# Configuration
WORKDIR="$HOME/.jackpot-sniper"
EXTENSION_DIR="$WORKDIR/extension"
USER_DATA_DIR="$WORKDIR/chrome_user_data"
GITHUB_API_RELEASES="https://api.github.com/repos/jackpotsniper/extension/releases/latest"

# Ensure dependencies are installed
dependencies=(curl unzip)
for dep in "${dependencies[@]}"; do
    if ! command -v "$dep" &> /dev/null; then
        echo "Error: $dep is not installed. Please install it and try again."
        exit 1
    fi
done

# Function to find Chrome
find_chrome() {
    local chrome_locations=(
        "/usr/bin/google-chrome"
        "/usr/bin/chromium"
        "/usr/bin/chrome"
        "$HOME/.local/bin/google-chrome"
    )
    for path in "${chrome_locations[@]}"; do
        if [ -x "$path" ]; then
            echo "$path"
            return
        fi
    done
    echo "" # Return empty string if not found
}

# Get local version
get_local_version() {
    if [ -f "$EXTENSION_DIR/manifest.json" ]; then
        grep -oP '(?<="version": ")\d+\.\d+' "$EXTENSION_DIR/manifest.json"
    else
        echo "0.0"
    fi
}

# Get latest version from GitHub
get_latest_version() {
    local response=$(curl -s "$GITHUB_API_RELEASES")
    local latest_version=$(echo "$response" | sed -n 's/.*"tag_name": "v\([^"]*\)".*/\1/p')
    local zip_url=$(echo "$response" | sed -n 's/.*"browser_download_url": "\([^"]*\.zip\)".*/\1/p')
    echo "$latest_version $zip_url"
}

# Download and extract extension
download_and_extract_extension() {
    local zip_url="$1"
    local zip_path="$WORKDIR/extension.zip"

    echo "Downloading extension..."
    curl -L -o "$zip_path" "$zip_url"

    if [ -d "$EXTENSION_DIR" ]; then
        rm -rf "$EXTENSION_DIR"
    fi
    mkdir -p "$EXTENSION_DIR"
    unzip -o -qq "$zip_path" -d "$EXTENSION_DIR"
    rm "$zip_path"
    echo "Extension updated successfully."
}

# Start Chrome
start_chrome() {
    local chrome_path=$(find_chrome)
    if [ -n "$chrome_path" ]; then
        "$chrome_path" --load-extension="$EXTENSION_DIR" --user-data-dir="$USER_DATA_DIR" &
    else
        echo "Chrome not found. Please install Chrome and try again."
    fi
}

# Main execution
mkdir -p "$WORKDIR"
read latest_version zip_url <<< $(get_latest_version)
local_version=$(get_local_version)

if [ -z "$zip_url" ]; then
    echo "Failed to retrieve extension download URL."
    exit 1
fi

if [ ! -d "$EXTENSION_DIR" ] || [ "$local_version" != "$latest_version" ]; then
    echo "Updating extension $local_version >> $latest_version"
    download_and_extract_extension "$zip_url"
fi

echo "Starting Chrome..."
start_chrome
