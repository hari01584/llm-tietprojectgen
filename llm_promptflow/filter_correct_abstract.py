
from promptflow import tool
from utils_escape_latex import escape_latex
from remove_bad_latex_tokens import remove_bad_tokens
# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def correct_abstract(llm_output: str) -> str:
    output = remove_bad_tokens(llm_output)
    output = output.replace("\\n", "\n")
    output_lines = output.split("\n")
    output_lines = [line for line in output_lines if line.strip()]
    first_line = output_lines[0].lower()
    if "\chapter{" in first_line or ("section" in first_line and "abstract" in first_line):
        output_lines = output_lines[1:]

    text = "\n".join(output_lines)
    return escape_latex(text)