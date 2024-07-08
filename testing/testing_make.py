import json
# Add one directory up in path
import sys
import tempfile
sys.path.append("..")

from llm_executor.call_promptflow import execute_flow
from latex_executor.compile_latex import compile_latex

if __name__ == "__main__":
    with open("testing/args.json", "r") as f:
        dict_input = json.load(f)

    # Execute flow first
    data_llm_result = execute_flow(**dict_input)
    with open("testing/data_llm_result.json", "w") as f:
        json.dump(data_llm_result, f)

    # with open("testing/data_llm_result.json", "r") as f:
    #     data_llm_result = json.load(f)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Compile the latex
        compile_latex("", temp_dir, data_llm_result)