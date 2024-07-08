
def remove_bad_tokens(original: str):
    BAD_TOKENS = [
        "\\newpage"
    ]

    for token in BAD_TOKENS:
        original = original.replace(token, "")

    return original