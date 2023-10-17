import os
import subprocess
import json
from chat_gpt import ChatGPT


class PythonResult:
    def __init__(self, output: str, result_code: int):
        self.output = output
        self.result_code = result_code


def run_python_code(code: str) -> PythonResult:
    temp_file = "/tmp/code.py"

    with open(temp_file, "w") as f:
        f.write(code)

    result = subprocess.run(["python3", temp_file], capture_output=True, text=True)

    os.remove(temp_file)

    return PythonResult(result.stdout, result.returncode)


def input_message(message: str = "") -> str:
    return input(message).strip()


def python(code: str) -> str:
    styled_code = "\n".join(f"# {row.ljust(45)} #" for row in code.split("\n"))

    print("\n" + "#" * 49)
    print("# I WANT TO RUN THIS PYTHON CODE:               #")
    print(styled_code)
    print("#" * 49)

    answer = ""
    while answer not in ["yes", "no"]:
        answer = input_message("\nDo you want to run this code? (yes/no)")

    if answer != "yes":
        print("\nSKIPPED RUNNING CODE")
        return "User rejected code. Please ask for changes or what to do next."

    result = run_python_code(code)

    return json.dumps({"output": result.output, "result_code": result.result_code})


if not os.path.exists("./data"):
    os.makedirs("./data")

# Assuming a Python version of ChatGPT is available in the current directory
chatgpt = ChatGPT(os.environ.get("OPENAI_API_KEY"))
chatgpt.smessage("You are an AI assistant...")
chatgpt.add_function(python)

print("################################################")
print("#           Python CodeInterpreter             #")
print("################################################\n")

print("GPT: Hello! I am the Python CodeInterpreter! What would you like to do?\nYou: ")

while True:
    message = input_message()

    if message == "":
        print("You haven't provided anything. Please try again.\nYou: ")
        continue

    if message in ["exit", "quit", "stop"]:
        print("\nGPT: Thanks!\n")
        exit()

    # Assuming the Python version of ChatGPT has a method 'umessage' and 'response'
    chatgpt.umessage(message)
    print("\n\nGPT:", chatgpt.response()['content'], "\nYou: ")
