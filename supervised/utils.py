import os
import requests
import time


def download_profile_picture(url, name):
    """Downloads profile picture from Google Scholar and saves it with the author's name

    Args:
        url (str): URL of the profile picture
        name (str): Name of the author to use in filename

    Returns:
        str: Path to saved image file, or None if download failed
    """
    if not url:
        return None

    try:
        os.makedirs("images", exist_ok=True)

        clean_name = "".join(
            x for x in name if x.isalnum() or x in (" ", "-", "_")
        ).rstrip()
        image_path = os.path.join("images", f"{clean_name}.jpg")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        max_retries = 1
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                break
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429 and attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                raise

        with open(image_path, "wb") as f:
            f.write(response.content)

        return image_path

    except Exception as e:
        print(f"Failed to download profile picture: {str(e)}")
        return None
