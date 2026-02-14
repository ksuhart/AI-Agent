import subprocess
import sys

def run_calculator(expression):
    """Run the calculator with the given expression."""
    try:
        result = subprocess.run(
            ["uv", "run", "calculator/main.py", expression],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return f"Error: {e}", 1

def check_precedence_in_code():
    """Check what the + precedence value is in the code."""
    try:
        with open("calculator/pkg/calculator.py", "r") as f:
            content = f.read()
            # Look for the precedence line
            for line in content.split("\n"):
                if '"+":' in line and "precedence" not in line.lower():
                    continue
                if '"+":' in line or '"+": ' in line:
                    return line.strip()
    except Exception as e:
        return f"Error reading file: {e}"
    return "Could not find + precedence in code"

def main():
    print("=" * 70)
    print("CALCULATOR BUG CHECKER")
    print("=" * 70)
    print()
    
    # Check the code
    print("📝 Checking precedence in code:")
    precedence_line = check_precedence_in_code()
    print(f"   {precedence_line}")
    print()
    
    # Determine expected state
    if '"+": 3' in precedence_line or '"+":3' in precedence_line:
        expected_result = "20"
        state = "BROKEN"
        color = "🔴"
    elif '"+": 1' in precedence_line or '"+":1' in precedence_line:
        expected_result = "17"
        state = "FIXED"
        color = "🟢"
    else:
        expected_result = "unknown"
        state = "UNKNOWN"
        color = "⚠️"
    
    print(f"{color} Code status: {state}")
    print(f"   Expected result for '3 + 7 * 2': {expected_result}")
    print()
    
    # Test the calculator
    print("🧪 Testing calculator with '3 + 7 * 2':")
    output, returncode = run_calculator("3 + 7 * 2")
    
    if returncode != 0:
        print(f"   ❌ ERROR: Calculator failed to run")
        print(f"   Output: {output}")
        sys.exit(1)
    
    print(f"   Output: {output}")
    print()
    
    # Parse the result
    try:
        if '"result": 20' in output or '"result": 20.0' in output:
            actual_result = "20"
        elif '"result": 17' in output or '"result": 17.0' in output:
            actual_result = "17"
        else:
            actual_result = "unknown"
            print(f"   ⚠️  WARNING: Could not parse result from output")
    except:
        actual_result = "unknown"
    
    # Verify result matches expected
    print("=" * 70)
    print("RESULTS:")
    print("=" * 70)
    
    if actual_result == "17":
        print("✅ Calculator is WORKING CORRECTLY")
        print("   Result: 17 (correct: 7 * 2 = 14, then 3 + 14 = 17)")
        if state == "BROKEN":
            print("   ⚠️  But code shows precedence 3 - might be cached?")
    elif actual_result == "20":
        print("❌ Calculator is BROKEN")
        print("   Result: 20 (wrong: 3 + 7 = 10, then 10 * 2 = 20)")
        print("   This means + has higher precedence than *")
        if state == "FIXED":
            print("   ⚠️  But code shows precedence 1 - might be cached?")
    else:
        print("⚠️  Could not determine calculator state")
        print(f"   Actual result: {actual_result}")
    
    print()
    print("=" * 70)
    
    # Additional test cases
    print()
    print("📊 Additional Test Cases:")
    test_cases = [
        ("2 + 3 * 4", "14", "If working correctly"),
        ("10 - 2 * 3", "4", "If working correctly"),
        ("1 + 2 + 3 * 4", "15", "If working correctly"),
    ]
    
    for expr, expected, note in test_cases:
        output, returncode = run_calculator(expr)
        if returncode == 0:
            print(f"   '{expr}' → {output}")
        else:
            print(f"   '{expr}' → ERROR")
    
    print()
    print("=" * 70)
    
    # Instructions
    if actual_result == "20":
        print()
        print("🔧 TO FIX: Run your agent with:")
        print('   python main.py "Fix the bug: 3 + 7 * 2 shouldn\'t be 20."')
        print()
    elif actual_result == "17":
        print()
        print("🎉 Calculator is working! Ready to submit tests.")
        print()

if __name__ == "__main__":
    main()
