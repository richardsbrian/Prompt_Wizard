import pyautogui
import os

def take_screenshot(filename='screenshot.png', region=None):
    try:
        # Create the directory if it doesn't exist
        os.makedirs('png_files/screenshots', exist_ok=True)
        
        # Construct the full file path
        full_path = os.path.join('png_files/screenshots', filename)
        
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        
        # Save the screenshot to the specified path
        screenshot.save(full_path)
        print(f"Screenshot saved as {full_path}")
    except Exception as e:
        print(f"Error taking screenshot: {e}")
