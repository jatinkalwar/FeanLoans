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


def imagev(image_data):
    try:
        print(image_data)
        # split_data = image_data.split(",", 1)
        # base64_encoded_image = split_data[1]
        decoded_data = base64.b64decode(image_data)

    except Exception as e:
        print(f"Error decoding Base64 string: {e}")
        exit()

    # Load the image from the decoded data
    try:
        image = Image.open(BytesIO(decoded_data))

    except Exception as e:
        print(f"Error loading image from decoded data: {e}")
        exit()

    # Convert image to RGB mode if it has an alpha channel (RGBA)
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Save the decoded image as a JPEG file
    initial_output_file_path = "initial_output_image.jpg"
    try:
        image.save(initial_output_file_path, format="JPEG")
    except Exception as e:
        print(f"Error saving image: {e}")
        exit()

    # Now, open the saved JPEG file and compress it
    compressed_output_file_path = f"com.jpg"
    try:
        image.save(compressed_output_file_path, format="JPEG", quality=60)


    except Exception as e:
        print(f"Error compressing and saving image:  {e}")
        exit()
