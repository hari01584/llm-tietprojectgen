
from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: str) -> str:
    output = input1
    # Replace \n with new line
    output = output.replace("\\n", "\n")
    print(output)
    return output
