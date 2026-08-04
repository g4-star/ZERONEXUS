import cloudinary
import cloudinary.uploader

from flask import current_app


def configure_cloudinary():

    cloudinary.config(
        cloud_name=current_app.config.get(
            "CLOUDINARY_CLOUD_NAME"
        ),

        api_key=current_app.config.get(
            "CLOUDINARY_API_KEY"
        ),

        api_secret=current_app.config.get(
            "CLOUDINARY_API_SECRET"
        ),

        secure=True
    )



# ==========================================
# Upload Profile Images
# ==========================================

def upload_image(file):

    configure_cloudinary()

    result = cloudinary.uploader.upload(
        file,
        folder="zeronexus/profile_images",
        resource_type="image"
    )

    return result["secure_url"]



# ==========================================
# Upload Project ZIP Files
# ==========================================

def upload_project_file(file):

    configure_cloudinary()

    result = cloudinary.uploader.upload(
        file,
        folder="zeronexus/projects",
        resource_type="raw"
    )

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"],
        "filename": result.get(
            "original_filename"
        )
    }



# ==========================================
# Delete Cloud File
# ==========================================

def delete_file(public_id):

    configure_cloudinary()

    cloudinary.uploader.destroy(
        public_id,
        resource_type="raw"
    )