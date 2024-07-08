
from promptflow import tool
from search_duckduckgo import search_and_scrape
import json

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def enrich_all_keywords(tags: list[str]) -> str:
    # Simply use SERP to search for each tags and get about it
    enriched_data = {}
    keep_keys = ["Abstract", "AbstractText"]
    keep_related_keys = ["Text", "FirstURL"]

    for tag in tags:
        try:
            searched_data = search_and_scrape(tag)
            data = json.loads(searched_data)
            # Filter the data to keep only the keys we want (only first level)
            filtered_data = {k: v for k, v in data.items() if k in keep_keys}
            # Also add some related data
            if "RelatedTopics" in data:
                related_topics = data["RelatedTopics"][:2]
                filtered_data["more_info"] = {}
                for topic in related_topics:
                    if "Text" in topic and "FirstURL" in topic:
                        filtered_data["more_info"][topic["FirstURL"]] = topic["Text"]

            enriched_data[tag] = json.loads(json.dumps(filtered_data)) # Prevent reference
        except Exception as e:
            print(f"Error while enriching tag {tag}: {e}")
            continue

    return json.dumps(enriched_data)

# if __name__ == '__main__':
#     tags = ["FastAPI"]
#     data = enrich_all_keywords(tags)
#     print(data)