
from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(llm_output: str) -> str:
    # Get all data between @BIBLOGRAPY@ and @BIBLOGRAPYEND@
    start = llm_output.find("@BIBLOGRAPY@")
    end = llm_output.find("@BIBLOGRAPYEND@")
    if start == -1 or end == -1:
        return ""
    return llm_output[start + len("@BIBLOGRAPY@"):end]