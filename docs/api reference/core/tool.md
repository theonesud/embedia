# Tool

`Tool` is an abstract class.
Your `Tool` subclass needs to define the `_run` method and return a `ToolReturn` model.
Your `Tool` subclass constructor also needs to call the `Tool` constructor with your tool's documentation in the `ToolDocumentation` model.

A `Tool` is how you can give your LLMs agency in the real world. The `_run` function of your `Tool` subclass can contain any arbitrary code. And since every `Tool` is documented in a standard format, the LLMs can read it and understand how to use them.

`Embedia` comes with a few prebuilt tools. Some of them are:
- `PythonInterpreter`: Takes in a Python code string and runs it with the current interpreter
- `Terminal`: Takes in a shell command and runs it in a shell of your choice
- `FileRead`: Takes in a file path returns the contents of the file
- `FileWrite`: Takes in a file path and data and writes the data to the file
- `FolderSearch`: Takes in a folder path and a filename and returns the location of the file if found

If you provide the `Tool` documentation to your LLM, and give it a use case, it can generate the arguments for the tool. This is how they get the agency in the world (Check the `ToolUser` agent documentation for more).

## ToolDocumentation and ToolReturn

Before we move on to the next step, let's understand the `ToolDocumentation`, `ParamDocumentation` and `ToolReturn` [Pydantic models](https://docs.pydantic.dev/latest/usage/models/).

`ToolDocumentation` is used to create documentation for your tool. The parameters it requires are the `name` (Tool's name), `desc` (Tool's description) and `params` (A list of `ParamDocumentation`).

`ParamDocumentation` is used to document the parameters of your tool. The parameters it requires are the `name` (Parameter's name) and `desc` (Parameter's description).

`ToolReturn` is used to define the output structure of your tool. The parameters it requires are the `output` and `exit_code`.
The `output` can be of any type and the `exit_code` can be only 0 or 1 (0 is default). 0 specifying that the tool ran successfully and 1 specifying that the tool ran unsuccessfully. You can return the error message in the `output` parameter in case of an unsuccessful run.

They can be defined as follows:

`Run in CodeSandbox`

```python
from embedia import ToolDocumentation, ParamDocumentation, ToolReturn

docs = ToolDocumentation(
    name="Post Request",
    desc="Sends a post request to a url",
    params=[
        ParamDocumentation(
            name="url",
            desc="The url to send the request to (Type: str)"
        ),
        ParamDocumentation(
            name="data",
            desc="The data to send (Type: dict)"
        ),
        ParamDocumentation(
            name="headers",
            desc="The headers to send (Type: dict)"
        ),
    ]
)
print(docs)

resp = ToolReturn(
    output={
        "status_code": 200,
        "message": "Request sent successfully"
    },
    exit_code=0
)
print(resp)

```
### Output
```
name='Post Request' desc='Sends a post request to a url' params=[ParamDocumentation(name='url', desc='The url to send the request to (Type: str)'), ParamDocumentation(name='data', desc='The data to send (Type: dict)'), ParamDocumentation(name='headers', desc='The headers to send (Type: dict)')]
output={'status_code': 200, 'message': 'Request sent successfully'} exit_code=0
```

## Basic Usage

Let's create a PrintTool. It takes a string as input and prints it.

> Remember to add `async` before the definition of `_run` and `await` before calling the subclass instance.

`Run in CodeSandbox`

```python
import asyncio
from embedia import Tool, ToolDocumentation, ParamDocumentation, ToolReturn


class PrintTool(Tool):
    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="Print Tool",
            desc="Prints whatever you want",
            params=[ParamDocumentation(name="text", desc="The text to be printed. Type: String")]
        ))

    async def _run(self, text: str):
        print(text)
        return ToolReturn(output='done', exit_code=0)


if __name__ == '__main__':
    printer = PrintTool()
    asyncio.run(printer('Hello World!'))
```

## Output

```
[time: 2023-09-07T16:52:48.159331+05:30] [id: 140534956818384] [event: Tool Start]
Tool: PrintTool
Args: ('Hello World!',)
Kwargs: {}
Hello World!

[time: 2023-09-07T16:52:48.159554+05:30] [id: 140534956818384] [event: Tool End]
Tool: PrintTool
ExitCode: 0
Output:
done
```

Since `ToolDocumentation`, `ParamDocumentation` and `ToolReturn` are all [Pydantic models](https://docs.pydantic.dev/latest/usage/models/), `Embedia` has simplified your effort by converting Python dictionaries to these models internally.

This simplifies the above code as follows:

`Run in CodeSandbox`

```python
import asyncio
from embedia import Tool


class PrintTool(Tool):
    def __init__(self):
        super().__init__(docs={
            "name": "Print Tool",
            "desc": "Prints whatever you want",
            "params": [{"name": "text", "desc": "The text to be printed. Type: String"}]
        })

    async def _run(self, text: str):
        print(text)
        return {'output': 'done'}


if __name__ == '__main__':
    printer = PrintTool()
    asyncio.run(printer('Hello World!'))
```
### Output
```
[time: 2023-09-07T17:00:25.133763+05:30] [id: 140344500518864] [event: Tool Start]
Tool: PrintTool
Args: ('Hello World!',)
Kwargs: {}
Hello World!

[time: 2023-09-07T17:00:25.133994+05:30] [id: 140344500518864] [event: Tool End]
Tool: PrintTool
ExitCode: 0
Output:
done
```

## Asking for human confirmation before running the tool

You can ask for human confirmation at any point in your `_run` function by calling the `self.human_confirmation` async method. It has a `details` parameter (type: dict). `details` will be displayed while asking for confirmation. You should construct the `details` dict with what you want the human to see before confirming.

Eg: You're creating a `DataAnalysis` tool. The input of this tool is a task (in plain English) and you want the tool to write the code for it and run it.

The sections of this tool's `_run` function can be something like:
- Give the task to a `CodingLanguageExpert Persona` and get the code
- Ask for human confirmation using `self.human_confirmation` with the code in the `details` parameter
- If the human confirms, run the code and return the output

> Remember to add `await` before calling `self.human_confirmation` because it is async.

Adding human confirmation to the PrintTool would look something like this:

`Run in CodeSandbox`

```python
import asyncio
from embedia import Tool


class PrintTool(Tool):
    def __init__(self):
        super().__init__(docs={
            "name": "Print Tool",
            "desc": "Prints whatever you want",
            "params": [{"name": "text", "desc": "The text to be printed. Type: String"}]
        })

    async def _run(self, text: str):
        await self.human_confirmation(details={"text": text})
        print(text)
        return {'output': 'done'}


if __name__ == '__main__':
    printer = PrintTool()
    asyncio.run(printer('Hello World!'))
```

### Output
```
[time: 2023-09-08T18:31:10.648109+05:30] [id: 140332688735104] [event: Tool Start]
Tool: PrintTool
Args: ('Hello World!',)
Kwargs: {}

Tool: PrintTool
Details: {'text': 'Hello World!'} Confirm (y/n):
```
If the user inputs `y`, the code successfully moves forward like so:
```
[time: 2023-09-08T18:34:28.908597+05:30] [id: 140214040132480] [event: Tool End]
Tool: PrintTool
ExitCode: 0
Output:
done
```
If the user inputs anything else, it raises `UserDeniedError`:
```
embedia.utils.exceptions.UserDeniedError: Tool: PrintTool Details: {'text': 'Hello World!'}
```