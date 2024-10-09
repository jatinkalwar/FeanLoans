import base64
from PIL import Image
from io import BytesIO

from fastapi import UploadFile
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from starlette.responses import JSONResponse

imagekit = ImageKit(
    private_key='private_Ljx7dcaXUYlkgXTkEmRO0hXgga8=',
    public_key='public_3qwqV6qN+2dieni1N+oxY2PDwM0=',
    url_endpoint='https://ik.imagekit.io/Thirddb'
)

def uploadfile(filee):
    try:
        # Open the file as a file-like object
        # Reset file pointer in case it was read before
        # Or 'utf-8' depending on the encoding
        with open("uploaded_new_sp.png", "rb") as image_file:
            # Read the image file as bytes
            image_data = image_file.read()
            # Encode bytes to Base64
            base64_image = base64.b64encode(image_data).decode('utf-8')

        upload = imagekit.upload(
            file=f"data:image/jpeg;base64,{filee}",  # Use the file stream
            file_name="hjdgfh.jpg",  # Use the original file name
            options=UploadFileRequestOptions(
                tags=["tag1", "tag2"]
            ))

        return upload.response_metadata.raw['url']

        # )

        # return upload.response_metadata.raw['url']
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return "fail"

