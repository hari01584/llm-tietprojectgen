
from promptflow import tool
from utils_escape_latex import escape_latex
from remove_bad_latex_tokens import remove_bad_tokens

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def correct_company_profile(company_profile_llm_output: str) -> str:
    output = remove_bad_tokens(company_profile_llm_output)
    output = output.replace("\\n", "\n")
    output_lines = output.split("\n")
    # Remove empty lines
    output_lines = [line for line in output_lines if line.strip()]
    # Check if first line contains "\chapter{", If yes then remove it
    first_line = output_lines[0].lower()
    if "\chapter{" in first_line or ("section" in first_line and "company" in first_line):
        output_lines = output_lines[1:]

    final_text = "\n".join(output_lines)

    # Also escape the latex special characters
    final_text = escape_latex(final_text)

    return final_text