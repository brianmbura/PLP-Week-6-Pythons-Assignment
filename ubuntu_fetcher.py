import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    """Extract filename from URL or generate one if missing"""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:  
        filename = "downloaded_image.jpg"
    return filename

def generate_unique_filename(filename, content):
    """Avoid duplicates by hashing image content"""
    file_hash = hashlib.md5(content).hexdigest()[:8]
    name, ext = os.path.splitext(filename)
    return f"{name}_{file_hash}{ext}"

def fetch_image(url):
    """Download and save image from a given URL"""
    try:
        # Create directory if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)

        # Fetch image
        headers = {"User-Agent": "UbuntuFetcher/1.0"}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()

        # Validate content type (only allow images)
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            print(f"✗ Skipped (not an image): {url}")
            return

        # Extract or generate filename
        filename = get_filename_from_url(url)

        # Ensure no duplicate images are saved
        filepath = os.path.join("Fetched_Images", filename)
        if os.path.exists(filepath):
            filename = generate_unique_filename(filename, response.content)
            filepath = os.path.join("Fetched_Images", filename)

        # Save image in binary mode
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}\n")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Allow multiple URLs
    urls = input("Please enter one or more image URLs (comma separated): ").split(",")
    urls = [u.strip() for u in urls if u.strip()]

    for url in urls:
        fetch_image(url)

    print("Connection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
