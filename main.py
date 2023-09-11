import cv2
import numpy as np
import requests
from PIL import Image
import os


class FashionStylist:
    def __init__(self):
        self.api_key = "YOUR_API_KEY"  # Replace with your own API key
        self.base_url = "https://api.example.com"  # Replace with your API endpoint

    def get_recommendations(self, user_style, user_body_type, user_budget):
        url = f"{self.base_url}/recommendations"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "style": user_style,
            "body_type": user_body_type,
            "budget": user_budget
        }
        response = requests.post(url, headers=headers, json=data)
        recommendations = response.json()
        return recommendations

    def mix_and_match(self, user_clothes):
        url = f"{self.base_url}/mix-and-match"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "multipart/form-data"
        }
        files = []
        for i, image_path in enumerate(user_clothes):
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image)
            # Optimize: Avoid saving multiple files by using a temporary directory
            image_filename = f"temp_{i}.jpg"
            image_pil.save(image_filename)
            files.append(("image", open(image_filename, "rb")))
        response = requests.post(url, headers=headers, files=files)
        mix_and_match_results = response.json()
        # Optimize: Remove temporary directory after use
        for file in files:
            os.remove(file[1].name)
        return mix_and_match_results

    def try_on_clothes(self, user_image, clothes_image):
        url = f"{self.base_url}/try-on"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "multipart/form-data"
        }
        user_image = cv2.imread(user_image)
        user_image = cv2.cvtColor(user_image, cv2.COLOR_BGR2RGB)
        user_image_pil = Image.fromarray(user_image)
        user_image_pil.save("temp_user.jpg")
        clothes_image = cv2.imread(clothes_image)
        clothes_image = cv2.cvtColor(clothes_image, cv2.COLOR_BGR2RGB)
        clothes_image_pil = Image.fromarray(clothes_image)
        clothes_image_pil.save("temp_clothes.jpg")
        files = [
            ("user_image", open("temp_user.jpg", "rb")),
            ("clothes_image", open("temp_clothes.jpg", "rb"))
        ]
        response = requests.post(url, headers=headers, files=files)
        try_on_result = response.json()
        # Optimize: Remove temporary files after use
        os.remove(files[0][1].name)
        os.remove(files[1][1].name)
        return try_on_result

    def share_outfit(self, user_outfit, social_media_platform):
        url = f"{self.base_url}/share-outfit"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "outfit": user_outfit,
            "platform": social_media_platform
        }
        response = requests.post(url, headers=headers, json=data)
        return response.status_code, response.json()

    def purchase_item(self, item_id, user_info):
        url = f"{self.base_url}/purchase"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "item_id": item_id,
            "user_info": user_info
        }
        response = requests.post(url, headers=headers, json=data)
        return response.status_code, response.json()

    def provide_feedback(self, user_feedback):
        url = f"{self.base_url}/feedback"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "feedback": user_feedback
        }
        response = requests.post(url, headers=headers, json=data)
        return response.status_code, response.json()


# Usage example:
fashion_stylist = FashionStylist()

# Get personalized recommendations
recommended_items = fashion_stylist.get_recommendations(
    "casual", "hourglass", 100
)
print("Recommended items:", recommended_items)

# Mix and match user's clothes
user_clothes = ["shirt.jpg", "pants.jpg", "shoes.jpg"]
mix_and_match_results = fashion_stylist.mix_and_match(user_clothes)
print("Mix and match results:", mix_and_match_results)

# Try on clothes virtually
try_on_result = fashion_stylist.try_on_clothes(
    "user_image.jpg", "clothes_image.jpg"
)
print("Virtual try-on result:", try_on_result)

# Share outfit on social media
status_code, response = fashion_stylist.share_outfit("outfit.jpg", "instagram")
print("Share outfit response:", status_code, response)

# Purchase item
status_code, response = fashion_stylist.purchase_item(
    "item123", {"name": "John", "email": "john@example.com"}
)
print("Purchase item response:", status_code, response)

# Provide feedback
status_code, response = fashion_stylist.provide_feedback("Great experience!")
print("Provide feedback response:", status_code, response)
