from dotenv import dotenv_values

def get_api_key():
    env_values = dotenv_values(".env")
    specific_variable = "ANTHROPIC_API_KEY"
    if specific_variable in env_values:
        ANTHROPIC_API_KEY = env_values[specific_variable]
        return ANTHROPIC_API_KEY
    else:
        print(f"{specific_variable} not found in the .env file")
