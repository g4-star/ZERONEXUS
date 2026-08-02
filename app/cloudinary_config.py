import cloudinary
import cloudinary.uploader

from flask import current_app


# =====================================================
# Configure Cloudinary
# =====================================================

def configure_cloudinary():

    cloudinary.config(
        cloud_name=current_app.config.get("CLOUDINARY_CLOUD_NAME"),
        api_key=current_app.config.get("CLOUDINARY_API_KEY"),
        api_secret=current_app.config.get("CLOUDINARY_API_SECRET"),
        secure=True
    )


# =====================================================
# Upload Image
# =====================================================

def upload_image(file):

    configure_cloudinary()

    result = cloudinary.uploader.upload(

        file,

        folder="zeronexus/profile_images",

        resource_type="image"

    )

    return result["secure_url"]


# =====================================================
# Delete Image
# =====================================================

def delete_image(public_id):

    configure_cloudinary()

    cloudinary.uploader.destroy(
        public_id
    )