import os
import requests
import json
import io
import pytesseract
from PIL import Image

class ImageToTextService:
    def _fetch_image_bytes(self, image_id: str) -> bytes:
        """
        Fetches the image file from the WhatsApp API.
        """
        token = os.getenv("WHATSAPP_TOKEN")
        url = f"https://graph.facebook.com/v19.0/{image_id}"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            image_url = resp.json()["url"]
            image_data = requests.get(image_url, headers=headers).content
            return image_data
        else:
            print(f"Error fetching image metadata: {resp.status_code} - {resp.text}")
            return None

    def describe(self, image_id: str) -> str:
        """
        Processes an image file using OCR to extract text.
        """
        print(f"Processing image with ID: {image_id} using OCR.")
        
        image_bytes = self._fetch_image_bytes(image_id)
        if not image_bytes:
            return "Could not fetch the image from WhatsApp."
        
        try:
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image)
            
            if text.strip():
                # We return the OCR result as a structured string for Brenda to process.
                return f"An image was received containing the text: {text.strip()}"
            else:
                return "An image was received, but no text could be extracted."
        except Exception as e:
            print(f"Error during image OCR processing: {e}")
            return "An image was received, but an error occurred while processing it."