from dotenv import load_dotenv
load_dotenv()

import os
import cloudinary
import cloudinary.api

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

print("Cloud:", cloudinary.config().cloud_name)
print("Key:", cloudinary.config().api_key)

try:
    print(cloudinary.api.ping())
except Exception as e:
    print(type(e).__name__)
    print(e)