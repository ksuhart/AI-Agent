from functions.get_file_content import get_file_content

def print_result(label, result):
    print(f"{label}:")
    print(result[:200] + "...")
    print(result)
    print()

if __name__ == "__main__":
    # 1. Large lorem test
    result1 = get_file_content("calculator", "lorem.txt")
    print("get_file_content(\"calculator\", \"lorem.txt\"):")
    print(f"Length: {len(result1)}")
    print("Ends with truncation message:", result1.endswith('characters]'))
    print()

    # 2. main.py
    result2 = get_file_content("calculator", "main.py")
    print("get_file_content(\"calculator\", \"main.py\"):")
    print_result("Result", result2)

    # 3. pkg/calculator.py
    result3 = get_file_content("calculator", "pkg/calculator.py")
    print("get_file_content(\"calculator\", \"pkg/calculator.py\"):")
    print_result("Result", result3)

    # 4. Outside working directory
    result4 = get_file_content("calculator", "/bin/cat")
    print("get_file_content(\"calculator\", \"/bin/cat\"):")
    print_result("Result", result4)

    # 5. Nonexistent file
    result5 = get_file_content("calculator", "pkg/does_not_exist.py")
    print("get_file_content(\"calculator\", \"pkg/does_not_exist.py\"):")
    print_result("Result", result5)

