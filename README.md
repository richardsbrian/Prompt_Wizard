# ![ ](https://github.com/richardsbrian/desktop_helper/blob/main/png_files/for_README/wiz.png)  Wizard Desktop Helper ![ ](https://github.com/richardsbrian/desktop_helper/blob/main/png_files/for_README/wiz_flip.png)

Wizard Desktop Helper is a proof-of-concept tool designed to streamline the process of capturing and analyzing screenshots by integrating with Anthropic's Claude API. This innovative tool enhances productivity and efficiency by allowing users to prompt the Claude API with a simple hotkey press.



## Installation
-Clone the Repository



git clone <https://github.com/richardsbrian/desktop_helper>


-Use pip to install the necessary libraries.

**pip install -r requirements.txt**

-Set Up Environment Variables

Create a **.env** file in the project directory and add your Anthropic API key.
 The first line of the .env file should be: **ANTHROPIC_API_KEY="your-API-key"**

# Usage
## Run the Application

To start the application use: **python main.py**

Once the application is running, click the Start button.

![ ](https://github.com/richardsbrian/desktop_helper/blob/main/png_files/for_README/start.png)

The program will minimize itself and await a screenshot call 


## Capture a Screenshot

Press **Ctrl + Alt + W** to take a screenshot.

The wizard will appear in the screen's bottom left corner and give you instructions.

![ ](https://github.com/richardsbrian/desktop_helper/blob/main/png_files/for_README/wiz_drag.png)

Click and drag over the content you wish to ask a question about

![ ](https://github.com/richardsbrian/desktop_helper/blob/main/png_files/for_README/drag.png)

## Add a Prompt

After taking a screenshot, you can add a prompt to the image and press **Enter**.

![ ](https://github.com/richardsbrian/desktop_helper/blob/main/png_files/for_README/ask.png)

then a response will be generated

![ ](https://github.com/richardsbrian/desktop_helper/blob/main/png_files/for_README/response.png)


## License
This project is licensed under the MIT License.

## Contact Information
If you have any questions or feedback, please open an issue in the repository or contact the maintainer at [richardsbrian@live.com].
