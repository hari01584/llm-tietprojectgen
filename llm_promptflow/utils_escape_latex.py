def escape_latex(text):
    # Define the common LaTeX special characters and their escaped equivalents
    latex_special_chars = {
        '#': r'\#',
        '$': r'\$',
        '%': r'\%',
        '&': r'\&',
        # '_': r'\_',
        # '{': r'\{',
        # '}': r'\}',
        # '~': r'\textasciitilde{}',  # LaTeX command for tilde
        # '^': r'\textasciicircum{}', # LaTeX command for circumflex
        # '\\': r'\textbackslash{}'   # LaTeX command for backslash
    }

    # Escape the characters in the text
    escaped_text = ''.join(latex_special_chars.get(char, char) for char in text)
    
    return escaped_text

if __name__ == "__main__":
    print(escape_latex("Hello $world$!"))
    print(escape_latex("This is a _test_ of special characters."))
    print(escape_latex("The tilde ~ and circumflex ^ characters are special."))
    print(escape_latex("The backslash \\ is also a special character."))
    print(escape_latex("JP & Morgan."))