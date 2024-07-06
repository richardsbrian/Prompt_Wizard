import anthropic
from key import get_api_key
import image_utils


def send_image_and_prompt(prompt):
    image_utils.resize_image_with_aspect_ratio("png_files//screenshots//box_screenshot.png", "png_files//screenshots//box_screenshot_resized.png", size=(450, 450))
    image_path = "png_files//screenshots//box_screenshot_resized.png"
    encoded_image_data = image_utils.encode_image_to_base64(image_path)
    image_media_type = "image/png"

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
                        "text": prompt
                    }
                ],
            }
        ],
    )
    print(message)
    return message


if __name__ == "__main__":
    send_image_and_prompt(prompt="Whats happing in this function?")