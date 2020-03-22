from datetime import datetime
import re

def log(text):
    """Prints the given text with a current timestamp

    Parameters:
    text (str):  The text to print
    """
    print(datetime.now().strftime('[%Y/%m/%d %H:%M:%S] - ') + text)

def clean_input(text):
    """Removes any web formatting & replaces it with regular text

    Parameters:
    text (str):  The text to have its formatting removed

    Returns:
    str: Text with formatting removed
    """
    text = text.strip()
    text = re.sub(r"[\n\t]+", "", text)
    text = text.replace("&amp;", "&")
    text = text.replace("&gt;", ">")
    text = text.replace("&lt;", "<")
    text = text.replace("&nbsp;", " ")
    text = text.replace("&quot;", '"')
    text = text.replace("&apos;", "'")
    text = text.replace("&#62;", ">")
    text = text.replace("&#60;", "<")
    text = text.replace("&#160;", " ")
    text = text.replace("&#34;", '"')
    text = text.replace("&#39;", "'")
    text = text.replace("&#32;", " ")
    return text

def dirty_output(text):
    """Replaces problematic characters with web accessible ones

    Parameters:
    text (str):  The text to be formatted

    Returns:
    str: Text with formatting
    """
    text = text.replace("&", "&amp;")
    return text