import cloudinary.uploader

from app.cloudinary_config import configure_cloudinary


def upload_project_file(file):

    configure_cloudinary()

    result = cloudinary.uploader.upload(
        file,
        folder="zeronexus/projects",
        resource_type="raw"
    )

    return {
        "url": result.get("secure_url"),
        "name": file.filename,
        "size": result.get("bytes")
    }
