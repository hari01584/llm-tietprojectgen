
from promptflow import tool
import requests
# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def search_and_scrape(query: str) -> str:
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    # Http request to the url
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        return response.text
    else:
        return "{}"
