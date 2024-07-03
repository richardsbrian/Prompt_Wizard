from PIL import Image

def resize_image_with_aspect_ratio(input_path, output_path, size=(200, 200)):
    """
    Resizes the input image to the specified size while maintaining the aspect ratio.
    The closest edge will match the desired size, and the other edge will be scaled accordingly.

    :param input_path: Path to the input PNG file.
    :param output_path: Path to save the resized PNG file.
    :param size: Tuple specifying the desired size (width, height) to resize the image to. Default is (200, 200).
    """
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


# Example usage
resize_image_with_aspect_ratio('png_files\\screenshots\\box_screenshot.png', 'png_files\\screenshots\\box_screenshot_resized.png', (450, 450))
