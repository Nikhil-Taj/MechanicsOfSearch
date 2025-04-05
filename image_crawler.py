import requests
import os
import re
import json

# Your Pexels API Key
api_key = 'FMDpGR8maOXrttBYbDnJv2r1qLVnGd0CLZyikBPfgeYmWgT6SX2mtP8q'  # Replace with your actual API key
url = 'https://api.pexels.com/v1/search'

# Create the images directory if it doesn't exist
image_folder = 'images'
if not os.path.exists(image_folder):
    os.mkdir(image_folder)

# Function to sanitize the filename
def sanitize_filename(filename):
    """Sanitize the image URL to be a valid filename."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Function to check if the URL ends with a valid image extension
def is_valid_image(url):
    """Check if the URL points to a valid image file (jpg, jpeg, png, gif, svg, webp)."""
    valid_image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']
    return any(url.lower().endswith(ext) for ext in valid_image_extensions)

# Function to download the image and save it
def download_image(img_url, image_folder="images", downloaded_urls=set()):
    """Download an image from the URL and save it to the folder."""
    
    # Skip URLs already downloaded
    if img_url in downloaded_urls:
        print(f"Skipping already downloaded image: {img_url}")
        return

    # Ensure URL ends with an image file extension
    if not is_valid_image(img_url):
        print(f"Skipping non-image URL: {img_url}")
        return

    img_name = os.path.join(image_folder, sanitize_filename(img_url.split("/")[-1]))

    # Print image URL to debug
    print(f"Attempting to download image: {img_url}")

    try:
        # Fetch the image with a request and allow redirects
        response = requests.get(img_url, allow_redirects=True)

        # Check if the response status code is valid and the content type is image
        if response.status_code == 200 and 'image' in response.headers['Content-Type']:
            with open(img_name, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded image: {img_url}")
            downloaded_urls.add(img_url)  # Add to the set of downloaded URLs
        else:
            print(f"Failed to download image (not an image or invalid URL): {img_url}")
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

# Function to fetch images from Pexels API
def fetch_images_from_pexels(query, count=50, page=1):
    """Fetch images from Pexels API."""
    headers = {'Authorization': api_key}
    params = {'query': query, 'per_page': count, 'page': page}

    response = requests.get(url, headers=headers, params=params)

    # Check the response status code
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch images, Status Code: {response.status_code}")
        return None

# Function to extract image URLs and metadata from the Pexels API response
def extract_image_data(response):
    """Extract image URLs and metadata from Pexels API response."""
    image_data = []
    if response and 'photos' in response:
        for image in response['photos']:
            image_info = {
                'url': image['src']['original'],  # Image URL
                'description': image.get('alt', 'No description'),  # Alt text or description
                'photographer': image['photographer'],  # Photographer's name
                'tags': [tag['title'] for tag in image.get('tags', [])]  # Tags if available
            }
            image_data.append(image_info)
    return image_data

# Function to fetch and download images
def fetch_and_download_images(query, total_images=1000, batch_size=50):
    """Fetch and download images in batches from Pexels API."""
    downloaded_urls = set()
    images_downloaded = 0
    page = 1
    all_image_data = []  # List to hold the textual surrogate data

    # Loop to fetch and download in batches
    while images_downloaded < total_images:
        print(f"Fetching batch {page} of {batch_size} images for query: {query}")
        response = fetch_images_from_pexels(query, batch_size, page)
        
        if response:
            image_data = extract_image_data(response)
            all_image_data.extend(image_data)  # Add image metadata to the list
            for img in image_data:
                download_image(img['url'], image_folder, downloaded_urls)
                images_downloaded += 1
                if images_downloaded >= total_images:
                    break
        
        page += 1  # Increment page number for the next batch
        print(f"Images downloaded so far: {images_downloaded} / {total_images}")

    print(f"Completed downloading {images_downloaded} images.")

    # Save the image data (textual surrogates) to a JSON file
    with open("image_data.json", "w") as json_file:
        json.dump(all_image_data, json_file, indent=4)  # Save image metadata (textual surrogates)

    print(f"Image data saved to 'image_data.json'")

# Start downloading images
fetch_and_download_images("random", total_images=1000, batch_size=50)


