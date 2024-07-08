
import re
from promptflow import tool

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def aggregate_biblography(company_profile_llm_raw: str, background_llm_raw: str, methodology_llm_raw: str, introduction_llm_raw) -> str:
    # Aggregate the bibliography from all LLM outputs
    bibliography_list = []
    llm_outputs = [company_profile_llm_raw, background_llm_raw, methodology_llm_raw, introduction_llm_raw] # Add more :0

    all_citations_keys = set()
    for llm_output in llm_outputs:
        # Extract all citations key from latex formatted text
        pattern = r'\\cite\{([^}]+)\}'
        matches = re.findall(pattern, llm_output)

        # Print matches
        for match in matches:
            # If there are multiple citations in a single \cite{}, split them
            keys = match.split(",")
            for key in keys:
                all_citations_keys.add(key)

    return ", ".join(all_citations_keys)