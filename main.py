import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found. Did you create a .env file?")

client = genai.Client(api_key=api_key)


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="JuniorAI Gemini Client")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    # Build messages list (Boot.dev tests look for this)
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]





    # Call Gemini with the user's prompt
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=args.user_prompt
    )

    # Token metadata check
    usage = response.usage_metadata
    if usage is None:
        raise RuntimeError("No usage metadata returned. The API request may have failed.")


    # Verbose output
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")

    # Always print the model's response




    print(response.text)


if __name__ == "__main__":
    main()

