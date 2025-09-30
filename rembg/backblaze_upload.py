import os
import base64
import hashlib
from urllib.parse import urlparse
import aiohttp

from rembg.config import (
    BACKBLAZE_KEY_ID,
    BACKBLAZE_KEY,
    BACKBLAZE_BUCKET_ID,
    BACKBLAZE_API_AUTH_URL,
)

def get_image_name(url: str) -> str:
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path).split(".")[0] + ".png"

async def authorize_backblaze() -> dict:
    try:
        encoded_auth = base64.b64encode(f"{BACKBLAZE_KEY_ID}:{BACKBLAZE_KEY}".encode()).decode()
        headers = {
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/json"
        }
        print("Authorizing with Backblaze...")
        print(encoded_auth)
        async with aiohttp.ClientSession() as session:
            async with session.get(BACKBLAZE_API_AUTH_URL, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                token = data["authorizationToken"]
                api_url = data["apiInfo"]["storageApi"]["apiUrl"] + "/b2api/v4/b2_get_upload_url"
                return {"token": token, "api_url": api_url}
    except Exception as e:
        raise RuntimeError(f"Backblaze authorization failed: {e}")

async def get_upload_url(api_url: str, token: str) -> dict:
    try:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }
        data = {"bucketId": BACKBLAZE_BUCKET_ID}

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers, params=data) as response:
                response.raise_for_status()
                data = await response.json()
                return {
                    "upload_url": data["uploadUrl"],
                    "token": data["authorizationToken"]
                }
    except Exception as e:
        raise RuntimeError(f"Failed to get Backblaze upload URL: {e}")

async def upload_image(upload_url: str, token: str, image: bytes, image_name: str) -> dict:
    try:
        headers = {
            "Authorization": token,
            "X-Bz-File-Name": image_name,
            "Content-Type": "b2/x-auto",
            "Content-Length": str(len(image)),
            "X-Bz-Content-Sha1": hashlib.sha1(image).hexdigest(),
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(upload_url, headers=headers, data=image) as response:
                response.raise_for_status()
                result = await response.json()
                print(result)
                return result
    except Exception as e:
        raise RuntimeError(f"Image upload failed: {e}")