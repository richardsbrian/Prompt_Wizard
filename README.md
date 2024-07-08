# Wizard Desktop Helper

 Wizard Desktop Helper is a screenshot tool POC that allows you to prompt Anthropic's Claude API. It is designed to make capturing screenshots and generating prompts easy and integrated.

![ ](https://github.com/richardsbrian/desktop_helper/blob/main/png_files/wizard_things/wiz.png)

## Installation
-Clone the Repository



git clone <https://github.com/richardsbrian/desktop_helper>


-Use pip to install the necessary libraries.

**pip install -r requirements.txt**

-Set Up Environment Variables

Create a **.env** file in the project directory and add your Anthropic API key.
 The first line of the .env file should be: **ANTHROPIC_API_KEY="your-API-key"**

## Usage
Run the Application
Execute the main script. To start the application use: **python main.py**

Once the application is running, click the Start button.

Capture a Screenshot
Press **Ctrl + Alt + W** to take a screenshot.

Add a Prompt
After taking a screenshot, you can add a prompt to the image and press **Enter**.

## Features
Capture screenshots with a keyboard shortcut.
Integrate prompts with screenshots using Anthropic's Claude API.

## Dependencies
Python 3.x
Libraries specified in requirements.txt


## License
This project is licensed under the MIT License.

## Contact Information
If you have any questions or feedback, please open an issue in the repository or contact the maintainer at [richardsbrian@live.com].
