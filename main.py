import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
import system_prompt
from call_function import available_functions, call_function

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found. Did you create a .env file?")

client = genai.Client(api_key=api_key)
model_name = "gemini-2.5-flash"


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

    # Verbose output for initial prompt
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    # Agentic loop - allow model to iterate on task until done
    max_iterations = 20
    for iteration in range(max_iterations):
        # Call Gemini with the conversation history
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt.system_prompt,
                temperature=0
            ),
        )

        # Token metadata check
        usage = response.usage_metadata
        if usage is None:
            raise RuntimeError("No usage metadata returned. The API request may have failed.")

        # Verbose output for token usage
        if args.verbose:
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")

        # Add the model's response candidates to conversation history
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # Process function calls if any
        function_calls = response.function_calls
        if function_calls:
            # Collect function results
            function_results = []
            
            for fc in function_calls:
                # Call the function using our call_function helper
                function_call_result = call_function(fc, verbose=args.verbose)
                
                # Validate the response structure
                if not function_call_result.parts:
                    raise Exception("Function call result has no parts")
                
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Function response is None")
                
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Function response.response is None")
                
                # Add to our list of function results
                function_results.append(function_call_result.parts[0])
                
                # Print the result if verbose
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            
            # Append function results to messages for next iteration
            messages.append(types.Content(role="user", parts=function_results))
        else:
            # No function calls - model has final response
            print("Final response:")
            print(response.text)
            # Break out of loop - task is complete
            break
    else:
        # Loop completed without breaking - max iterations reached
        print("\n⚠️  Warning: Maximum iterations reached without final response.")
        print("The agent did not complete the task within the allowed iterations.")
        exit(1)


if __name__ == "__main__":
    main()
