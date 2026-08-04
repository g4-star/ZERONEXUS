import cloudinary.uploader

from app.cloudinary_config import configure_cloudinary


# =====================================================
# Upload Project ZIP to Cloudinary
# =====================================================

def upload_project_file(file):

    configure_cloudinary()

    result = cloudinary.uploader.upload(
        file,
        folder="zeronexus/projects",
        resource_type="raw"
    )

    size_bytes = result.get("bytes", 0)

    return {

        "url": result.get("secure_url"),

        "public_id": result.get("public_id"),

        "name": file.filename,

        "size": f"{round(size_bytes / 1024, 2)} KB"

    }