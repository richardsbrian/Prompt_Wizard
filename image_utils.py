from PIL import Image
import base64


def resize_image_with_aspect_ratio(input_path, output_path, size=(200, 200)):
    with Image.open(input_path) as img:
        original_width, original_height = img.size
        target_width, target_height = size

        # Calculate the scaling factor while maintaining the aspect ratio
        width_ratio = target_width / original_width
        height_ratio = target_height / original_height
        scaling_factor = min(width_ratio, height_ratio)

        # Calculate new size based on the scaling factor
        new_width = int(original_width * scaling_factor)
        new_height = int(original_height * scaling_factor)

        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        resized_img.save(output_path, format='PNG')



def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image_data = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_image_data
    except FileNotFoundError:
        print(f"The file at {image_path} was not found.")
        return None



