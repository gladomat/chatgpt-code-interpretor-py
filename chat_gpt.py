import re
import requests
import uuid
from typing import Callable, Union, List, Dict, Any, Optional
from inspect import signature, Parameter


class ChatGPT:
    def __init__(self, api_key: str, chat_id: Optional[str] = None):
        self.messages = []
        self.functions = []
        self.savefunction = None
        self.loadfunction = None
        self.loaded = False
        self.function_call = "auto"
        self.model = "gpt-3.5-turbo"
        self.api_key = api_key
        self.chat_id = chat_id or str(uuid.uuid4())

    def load(self):
        if callable(self.loadfunction):
            self.messages = self.loadfunction(self.chat_id)
            self.loaded = True

    def set_model(self, model: str):
        self.model = model

    def get_model(self):
        return self.model

    def version(self):
        matches = re.match(r"gpt-(([0-9]+)\.?([0-9]+)?)", self.model)
        if matches:
            return float(matches.group(1))
        return 0.0

    def force_function_call(self, function_name: str, arguments: Optional[dict] = None):
        if function_name == "auto":
            if arguments:
                raise Exception("Arguments must not be set when function_call is 'auto'")
            self.function_call = "auto"
        else:
            self.function_call = {"name": function_name, "arguments": arguments}

    def _add_message(self, role: str, content: Optional[str] = None, function_call: Optional[dict] = None, function_name: Optional[dict] = None):
        message = {"role": role, "content": content}
        if function_call:
            message["function_call"] = function_call
        if function_name:
            message["name"] = function_name
        self.messages.append(message)
        if callable(self.savefunction):
            self.savefunction(message, self.chat_id)

    def smessage(self, system_message: str):
        self._add_message("system", system_message)

    def umessage(self, user_message: str):
        self._add_message("user", user_message)

    def amessage(self, assistant_message: str):
        self._add_message("assistant", assistant_message)

    def fcall(self, function_name: str, function_arguments: str):
        self._add_message("assistant", None, {"name": function_name, "arguments": function_arguments})

    def fresult(self, function_name: str, function_return_value: str):
        self._add_message("function", function_return_value, function_name=function_name)

    def response(self, raw_function_response: bool = False):
        fields = {"model": self.model, "messages": self.messages}
        functions = self._get_functions()
        if functions:
            fields["functions"] = functions
            fields["function_call"] = self.function_call

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=fields).json()

        if "choices" not in response or "message" not in response["choices"][0]:
            error = (
                response.get("error", {}).get("message", "") + " (" + response.get("error", {}).get("type", "") + ")"
            )
            raise Exception(f"Error in OpenAI request: {error}")

        message = response["choices"][0]["message"]
        self.messages.append(message)
        if callable(self.savefunction):
            self.savefunction(message, self.chat_id)

        message = self.messages[-1]
        return self._handle_functions(message, raw_function_response)

    def _handle_functions(self, message: dict, raw_function_response: bool):
        if "function_call" in message:
            if raw_function_response:
                return message

            function_call = message["function_call"]
            function_name = function_call["name"]
            arguments = function_call.get("arguments", [])

            callable_func = self._get_function(function_name)
            if callable_func:
                result = callable_func(arguments)
            else:
                result = f"Function '{function_name}' unavailable."

            self.fresult(function_name, result)
            return self.response()
        return message

    def _get_function(self, function_name: str):
        for function in self.functions:
            if function["name"] == function_name:
                return function["function"]
        return None

    def _get_functions(self):
        functions = []
        for function in self.functions:
            properties = {}
            required = []
            for param in function["parameters"]:
                properties[param["name"]] = {"type": param["type"], "description": param["description"]}
                if param.get("items"):
                    properties[param["name"]]["items"] = param["items"]
                if param.get("required"):
                    required.append(param["name"])

            functions.append(
                {
                    "name": function["name"],
                    "description": function["description"],
                    "parameters": {"type": "object", "properties": properties, "required": required},
                }
            )
        return functions

    def add_function(self, function: Union[Callable, dict]):
        if callable(function):
            function_data = self._parse_function(function)
        else:
            function_data = function
        self.functions.append(function_data)

    def _parse_function(self, function: Callable):
        sig = signature(function)
        function_data = {"function": function, "name": function.__name__, "description": "", "parameters": []}

        # Parse docstring for @param annotations
        doc = function.__doc__ or ""
        for line in doc.split("\n"):
            if "@param" in line:
                parts = line.split("@param")[1].strip().split(" ")
                if len(parts) >= 2:
                    type_name, name = parts[:2]
                    description = " ".join(parts[2:])
                    param_data = {
                        "name": name,
                        "type": type_name,
                        "description": description,
                        "required": not any(
                            [p.default != Parameter.empty for p in sig.parameters.values() if p.name == name]
                        ),
                    }
                    function_data["parameters"].append(param_data)
        return function_data

    def messages(self):
        return self.messages

    def loadfunction(self, loadfunction: Callable, autoload: bool = True):
        self.loadfunction = loadfunction
        if autoload:
            self.load()

    def savefunction(self, savefunction: Callable):
        self.savefunction = savefunction

    def dump(self):
        return self.messages

    def save(self):
        if callable(self.savefunction):
            for message in self.messages:
                self.savefunction(message, self.chat_id)

    def __str__(self):
        return str(self.messages)
