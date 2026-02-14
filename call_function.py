from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

# Define available functions for the LLM
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

# Import the actual functions lazily to avoid circular imports
def _get_function_map():
    """Lazy load function map to avoid import issues."""
    from functions.get_files_info import get_files_info
    from functions.get_file_content import get_file_content
    from functions.run_python_file import run_python_file
    from functions.write_file import write_file
    
    return {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }


def call_function(function_call, verbose=False):
    """
    Handles calling one of the available functions and returning its result.
    
    Args:
        function_call: A FunctionCall object with name and args properties
        verbose: If True, prints detailed information about the function call
        
    Returns:
        A types.Content object with the function result or error
    """
    # Get the function map (lazy loaded)
    function_map = _get_function_map()
    
    # Get the function name, ensuring it's a string
    function_name = function_call.name or ""
    
    # Print the function call information
    if verbose:
        print(f"Calling function: {function_name}({function_call.args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Check if the function exists in our mapping
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Make a shallow copy of the arguments
    args = dict(function_call.args) if function_call.args else {}
    
    # Override the working_directory argument
    args["working_directory"] = "./calculator"
    
    # Call the function with the arguments
    function_result = function_map[function_name](**args)
    
    # Return the result wrapped in a types.Content object
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
