# Python CodeInterpreter

This the python version of the code as implemented by [Unconventional Coding.](https://github.com/unconv/code-interpreter)

Python CodeInterpreter leverages OpenAI's ChatGPT to interact with Python code seamlessly. It allows users to submit Python code, decide whether to run it, and receive the code's output.

## Features:
1. **Interactive Python Code Execution**: After entering your Python code, the system will ask if you want to run it. Upon your confirmation, it will be executed.
2. **Integration with ChatGPT**: The system uses a Python implementation of ChatGPT for interactive dialogue.
3. **Function Handling with OpenAI**: Allows the addition and handling of functions with OpenAI's ChatGPT.
4. **Modular Design**: Easily extendable with more features.

## Modules:

### 1. PythonResult:
- This class encapsulates the output and result code after executing the Python code.

### 2. Utility Functions:
- `run_python_code`: Executes the Python code and returns the output.
- `input_message`: Retrieves user input.

### 3. ChatGPT:
- This class manages interactions with OpenAI's GPT model.
- Supports system, user, and assistant messages.
- Allows the addition and handling of custom functions.
- Supports saving and loading chat logs with optional functions.
  
## How To Use:

1. Ensure you have the required libraries installed, such as `requests` and `re`.
2. Provide your `OPENAI_API_KEY` as an environment variable.
3. Run the main script to start the Python CodeInterpreter.
4. Enter Python code and decide whether to execute it based on the prompts.

```bash
# Sample Interaction:

################################################
#           Python CodeInterpreter             #
################################################

GPT: Hello! I am the Python CodeInterpreter! What would you like to do?
You: <Enter Your Python Code>
```

5. Type "exit", "quit", or "stop" to end the interaction.

## Future Development:

- This framework can be further expanded by adding more functions to ChatGPT.
- Enhancements can be made for error handling, extended integrations, and more.

## License:

- GPL-3.0-or-later
