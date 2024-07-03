import base64
import anthropic
from key import get_api_key

# Specify the path to the local PNG image
image_path = "output.png"
image_media_type = "image/png"

# Read the image file in binary mode and encode to base64
with open(image_path, "rb") as image_file:
    encoded_image_data = base64.b64encode(image_file.read()).decode("utf-8")

OPENAI_API_KEY = get_api_key()

client = anthropic.Anthropic(api_key=OPENAI_API_KEY)
message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": encoded_image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "What's happening here?"
                }
            ],
        }
    ],
)
print(message)