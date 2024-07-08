import json
from promptflow.client import load_flow
from promptflow.core import Flow

import streamlit as st
import os

from promptflow.entities import OpenAIConnection
from promptflow.executor._result import LineResult

open_ai_connection = OpenAIConnection(
    api_key="<OpenAI Key>"
)

# # Add the connection
# client.connections.create_or_update(connection_name, connection_details)

# Get path of this directory where this file is located
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
# Go one directory up to get to the root directory
ROOT_DIR = os.path.abspath(os.path.join(DIR_PATH, os.pardir))
# The path to promptflow files are one directory below, go
PATH_LLM_PROMPTFLOW = os.path.join(ROOT_DIR, "llm_promptflow")

flow_path = PATH_LLM_PROMPTFLOW

def execute_flow(**args):
    # Dump args to a file
    with open("args.json", "w") as f:
        json.dump(args, f)
    
    flow = Flow.load(flow_path)
    # f = load_flow(flow_path)
    flow_result: LineResult = flow.invoke(inputs={**args}, connections={
        "openai_connection": open_ai_connection._to_execution_connection_dict()
    })

    return flow_result.output

if __name__ == "__main__":
    dict_input = {
        "company_profile": "I work in J. P. Morgan which is a progressive US Bank",
        "introduction": "I am backend developer, working over transaction searches of various merchants of Chase Bank. Currently the problem of search is high and it is not very intuitive, This project improves by adding good UI on it",
        "introduction_images": [["img_name1.png","JP Morgan logo"],["chart_growth.png","Chart showing growth of JP Morgan in recent years"]],
        "background_input": "I am backend developer, working over transaction searches of various merchants of Chase Bank. Currently the problem of search is high and it is not very intuitive, This project improves by adding good UI on it",
        "background_images": [["img_name1.png","JP Morgan logo"],["chart_growth.png","Chart showing growth of JP Morgan in recent years"]],
        "objectives_input": "1. To improve the search functionality of the transaction search\n2. To make the search more intuitive and user friendly",
        "methodology_input": "1. We will use the latest technologies like React, Node.js, and MongoDB\n2. We will use the latest technologies like React, Node.js, and MongoDB, Using latest meets of Scrumm and git/etc",
        "methodology_images": [],
        "methodology_keywords": ["React", "Node.js", "MongoDB", "Scrumm", "git"],
        "observation_findings_input": "The current search is not very intuitive and user friendly, Tools like react are amazing, scrumm meetings amazing",
        "limitations_input": "1. The project is limited to the search functionality of the transaction search\n2. The project is limited to the search functionality of the transaction search",
        "conclusions_future_work_input": "In future we can add more features like voice search, and more intuitive search",
    }

    flow_result = execute_flow(**dict_input)
    print(flow_result["bibliography"])